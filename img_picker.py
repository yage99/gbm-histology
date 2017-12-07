'''
This script picks the top 20 best histology image from the input
directory to the output directory according to the image pixel
density. This is the preprocess of the massive images.

This script use parallel couputing, task pool it set to 20 by
default. Change it according to your machine configuration.
'''


import os
import shutil
from TCGAMaxim.utils import printProgressBar
import pickle
from multiprocessing import Pool
import time
import sys
import numpy as np
from skimage import io, color
import re
import subprocess32 as sp


def calc_density(image_file, threshold=150):
    rgb = io.imread(image_file)
    lab = color.rgb2lab(color.rgba2rgb(rgb))

    pixel_count = lab.shape[0] * lab.shape[1]
    # the a channel should bigger than 10 (red)
    color_count = np.sum(np.logical_and(lab[:, :, 1] > 10,
                                        lab[:, :, 2] > -30))

    return color_count / float(pixel_count)


task_count = 0
task_sum = 0
id_matcher = re.compile("TCGA-\w{2}-\w{4}-\w{3}-\w{2}-\w{3}")


def calc_task(folder, image_file):

    density = calc_density(os.path.join(folder, image_file))

    # blank files
    if(density < 0.05):
        sp.call(['mv', os.path.join(folder, image_file),
                 '/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-processed-blanks'])
        return None

    return (folder, image_file, density)


last_show_time = 0


def task_callback(result):
    global task_count, last_show_time

    if(result is not None):
        folder, image_file, density = result
        id = id_matcher.search(image_file).group()

        if id in patients:
            patients[id][image_file] = density
        else:
            patients[id] = {image_file: density}

    task_count = task_count + 1

    # used_time_str = ("%d:%d" % (int(used_time / 60), int(used_time % 60)))

    if(last_show_time != time.time()):
        printProgressBar(task_count, task_sum, time_start=start_time,
                         length=30)
        last_show_time = time.time()


patients = {}
start_time = 0


def main(folder, target_folder, task_pool=20,
         tmpfilename="image_metas.pkl"):
    print("data file name: %s" % tmpfilename)
    if not os.path.isfile(tmpfilename):
        print "image density not exists, calculating"
        global task_count, task_sum, patients, start_time

        patients = {}

        task_sum = len(os.listdir(folder))

        task_count = 0
        pool = Pool(task_pool)
        # i = 0
        start_time = time.time()
        for image_file in os.listdir(folder):
            # i = i + 1
            # if i==10:
            #    break
            # calc_task(folder, image_file)
            pool.apply_async(calc_task, (folder, image_file, ),
                             callback=task_callback)
        pool.close()
        pool.join()

        with open(tmpfilename, "wb") as output:
            pickle.dump(patients, output)

        time_task_end = time.time()
        time_used = time_task_end - start_time
        print("timed used: %dh%dm%ds" % (time_used / 3600,
                                         (time_used % 3600) / 60,
                                         time_used % 60))
    else:
        print "using existing density file: %s" % tmpfilename
        patients = pickle.load(open(tmpfilename, "rb"))

    print "start copy file"

    copy_all_count = len(patients) * 40
    copy_count = 0
    time_start = time.time()
    for id in patients:
        if not os.path.exists(os.path.join(target_folder, id)):
            os.mkdir(os.path.join(target_folder, id))
        for key, value in sorted(patients[id].iteritems(),
                                 key=lambda (k, v): (v, k))[-40:]:
            try:
                shutil.copyfile(os.path.join(folder, key),
                                os.path.join(target_folder, id, key))
            except:
                pass
            copy_count = copy_count + 1
            printProgressBar(copy_count, copy_all_count,
                             time_start=time_start, prefix=id,
                             length=30)

    print "copy finished"


if __name__ == "__main__":
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], tmpfilename=sys.argv[3])
    elif len(sys.argv) > 1:
        main("/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-processed",
             "/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-selected",
             tmpfilename=sys.argv[1])
    else:
        main("/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-processed",
             "/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-selected")
