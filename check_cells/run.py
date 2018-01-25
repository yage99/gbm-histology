import os
import glob
import subprocess as sp
from multiprocessing import Pool, Value
import sys
import re
import time
import math

sys.path.append('../')
from TCGAMaxim.utils import printProgressBar  # noqa: E402
from calc_nuclei_threshold import calc_nuclei_threshold  # noqa: E402

thread_count = Value('d', 0)
task_count = Value('d', 0)


RECALC_THRESHOLD_FLAG = False
threshold_reg = re.compile(r'(threshold_.*)*.png$')


def calc_threshold_task(image_file):
    if not RECALC_THRESHOLD_FLAG and "threshold" in image_file:
        return image_file
    threshold = calc_nuclei_threshold(image_file)
    new_file_name = threshold_reg.sub(
        'threshold_%f.png' % threshold, image_file)

    if new_file_name != image_file:
        sp.call(['mv', image_file, new_file_name])
    return new_file_name


def main(folder, working_dir='.', filelist_name='filelist',
         thread_num=20, recalc_threshold=False):
    global RECALC_THRESHOLD_FLAG

    RECALC_THRESHOLD_FLAG = recalc_threshold
    print 'recalculate threshold for each image'

    origin_filelist = []

    def recurse_find(folder):
        for file in os.listdir(folder):
            if(os.path.isdir(os.path.join(folder, file))):
                recurse_find(os.path.join(folder, file))
            elif file.endswith('png'):
                png_file = os.path.join(os.path.abspath(folder), file)
                origin_filelist.append(png_file)

    recurse_find(folder)
    pool = Pool(thread_num)

    filelist = []

    def calc_threshold_callback(data):
        filelist.append(data)
    time_start = time.time()
    for image_file in origin_filelist:
        pool.apply_async(calc_threshold_task, (image_file, ),
                         callback=calc_threshold_callback)

    while len(filelist) < len(origin_filelist):
        printProgressBar(len(filelist), len(origin_filelist),
                         time_start=time_start)
        time.sleep(0.5)
    pool.close()
    pool.join()

    pool = Pool(thread_num)

    with open(os.path.join(working_dir, filelist_name),
              'w') as filelist_file:
        for item in filelist:
            filelist_file.write(item + "\n")

    all_img_count = len(filelist)
    img_per_task = math.ceil(all_img_count / float(thread_num))

    print 'Starting tasks'
    thread_total = 0
    result_folders = glob.glob('outputs*')
    command = ['rm', '-r']
    command.extend(result_folders)
    sp.call(command)
    for i in range(thread_num):
        # sp.call(['rm', '-rf', 'outputs%d' % i])
        sp.call(['mkdir', os.path.join(working_dir, 'outputs%d' % i)])

        start = i * img_per_task + 1
        end = (i + 1) * img_per_task
        if end > all_img_count:
            end = all_img_count
        pool.apply_async(generating_task,
                         (working_dir, filelist_name, i, start, end,))

        thread_total += 1

    time_start = time.time()
    while(True):
        if thread_count.value >= thread_total:
            break

        printProgressBar(task_count.value,
                         all_img_count,
                         prefix=("%d/%d"
                                 % (thread_count.value,
                                    thread_total)),
                         time_start=time_start)
        time.sleep(0.5)

    pool.close()
    pool.join()


def generating_task(working_dir, filelist_name, thread_index,
                    start, end):

    output_folder = os.path.join(working_dir,
                                 'outputs%d' % thread_index)
    print "generating batch file %d" % thread_index
    sp.call(['cellprofiler', '-p',
             os.path.join(working_dir, 'check_cells.cpproj'),
             '-cr',
             '--file-list',
             os.path.join(working_dir, filelist_name),
             '-o',
             output_folder,
             '-t', os.path.expanduser('~/tmp')])

    print "Task %d started (%d - %d)" % (thread_index, start, end)
    subprocess = sp.Popen(['cellprofiler', '-p',
                           os.path.join(output_folder,
                                        'Batch_data.h5'),
                           '-cr', '-f', '%d' % start,
                           '-l', '%d' % end,
                           '-t', os.path.expanduser('~/tmp')],
                          stdout=sp.PIPE,
                          stderr=sp.PIPE)

    img_num_retriver = re.compile('Image # ([0-9]*)')
    last_num = start
    with open(os.path.join(output_folder, 'log.log'),
              'w') as log_file:
        for line in iter(subprocess.stderr.readline, b''):

            if img_num_retriver.search(line) is not None:
                num = int(img_num_retriver.search(line).group(1))

                if last_num != num:
                    with task_count.get_lock():
                        task_count.value += (num - last_num)

                    last_num = num
            else:
                log_file.write(line)

    print "Task %d finished" % thread_index

    with thread_count.get_lock():
        thread_count.value += 1


if __name__ == '__main__':
    main('../data/svs-selected')
