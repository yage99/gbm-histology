import os
import subprocess as sp
from multiprocessing import Pool, Value
import sys
import re
import time

sys.path.append('../')
from TCGAMaxim.utils import printProgressBar  # noqa: E402

thread_count = Value('d', 0)
task_count = Value('d', 0)


def main(folder, working_dir='.', filelist_name='filelist',
         project_file='pipeline.cpproj',
         thread_num=20):
    filelist = []

    def recurse_find(folder):
        for file in os.listdir(folder):
            if(os.path.isdir(os.path.join(folder, file))):
                recurse_find(os.path.join(folder, file))
            else:
                filelist.append(os.path.join(folder, file))

    recurse_find(folder)

    with open(os.path.join(working_dir, filelist_name),
              'w') as filelist_file:
        for item in filelist:
            filelist_file.write(item + "\n")

    pool = Pool(thread_num)

    all_img_count = len(filelist)
    img_per_task = 100
    thread_total = all_img_count / img_per_task
    
    print 'Starting tasks'
    for i in range(thread_total):
        sp.call(['rm', '-rf', 'outputs%d' % i])
        sp.call(['mkdir', os.path.join(working_dir, 'outputs%d' % i)])

        start = i * img_per_task
        if start == 0:
            start = 1
        end = (i + 1) * img_per_task
        if end > all_img_count:
            end = all_img_count
        pool.apply_async(generating_task,
                         (working_dir, project_file, filelist_name,
                          i, start, end,))

    time_start = time.time()
    while(True):
        if thread_count.value >= thread_total:
            break

        printProgressBar(task_count.value,
                         all_img_count,
                         prefix=("%d/%d"
                                 % (thread_count.value,
                                    thread_total)),
                         time_start=time_start,
                         length=50)
        time.sleep(0.5)

    pool.close()
    pool.join()


def generating_task(working_dir, project_file, filelist_name, thread_index,
                    start, end):
    
    output_folder = os.path.join(working_dir,
                                 'outputs%d' % thread_index)
    print "generating batch file %d" % thread_index
    sp.call(['cellprofiler', '-p',
             os.path.join(working_dir, project_file),
             '--file-list',
             os.path.join(working_dir, filelist_name),
             '-o',
             output_folder])

    subprocess = sp.Popen(['cellprofiler', '-p',
                           os.path.join(output_folder,
                                        'Batch_data.h5'),
                           '-cr', '-f', '%d' % start,
                           '-l', '%d' % end],
                          stdout=sp.PIPE,
                          stderr=sp.PIPE)
    
    print "Task %d started" % thread_index
    img_num_retriver = re.compile('# ([0-9]*)')
    err = re.compile('error', flags=re.I)
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

            # only write error messages
            if err.search(line) is not None:
                log_file.write(line)

    print "Task %d finished" % thread_index

    with thread_count.get_lock():
        thread_count.value += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        main('/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-best')
    elif len(sys.argv) == 4:
        main(folder=sys.argv[1], working_dir=sys.argv[2],
             project_file=sys.argv[3])
    else:
        print('''
Usage:

    python run.sh <sourcedir> <working_dir> <project_file_name>

    This script will create 20(by default) threads to run cellprofiler and
make 20 output dirs to store output files.
    Make sure you have a right cellprofiler project which contains a batch
generator module.


''')
