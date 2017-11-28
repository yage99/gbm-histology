'''
This script picks the top 20 best histology image from the input
directory to the output directory according to the image pixel
density. This is the preprocess of the massive images.

This script use parallel couputing, task pool it set to 20 by
default. Change it according to your machine configuration.
'''


from PIL import Image
import os
import shutil
from TCGAMaxim.utils import printProgressBar
import pickle
from multiprocessing import Pool
import time
import sys


def rgb2lab(inputColor):
    num = 0
    RGB = [0, 0, 0]

    for value in inputColor:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float(XYZ[0]) / 95.047
    # ref_X =  95.047   Observer=2 degree, Illuminant= D65
    XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ:
        if value > 0.008856:
            value = value ** (1.0/3)
        else:
            value = (7.787 * value) + (16.0 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab


def calc_density(image, threshold=150):
    pixel = image.load()

    pixel_count = image.size[0] * image.size[1]
    color_count = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # transparent pixel don't count
            if pixel[i, j][3] < 125:
                continue
            # black pixel don't count
            if pixel[i, j][0] + pixel[i, j][1] + pixel[i, j][2] < 50:
                continue

            # using lab color space
            lab = rgb2lab(pixel[i, j])
            if lab[1] > 10:
                # red pixel
                color_count += 1
            # red pixel has a minium
            # if pixel[i, j][0] < threshold and pixel[i, j][0] > 50:
            #    color_count = color_count + 1
            # green pixel
            # if pixel[i, j][1] < threshold:
            #    color_count = color_count + 1
            # if pixel[i, j][2] < threshold:
            #    color_count = color_count + 1

    return color_count / float(pixel_count)


task_count = 0
task_sum = 0


def calc_task(folder, image_file):

    density = calc_density(Image.open(os.path.join(folder, image_file)))

    return (folder, image_file, density)


def task_callback(result):
    import re
    global task_count, task_sum, patients, start_time

    folder, image_file, density = result
    id_matcher = re.compile("TCGA-\w{2}-\w{4}-\w{3}-\w{2}-\w{3}")
    id = id_matcher.search(image_file).group()
    
    if id in patients:
        patients[id][image_file] = density
    else:
        patients[id] = {image_file: density}

    task_count = task_count + 1

    current_time = time.time()
    used_time = current_time - start_time
    time_each = used_time / task_count
    left_time = time_each * (task_sum - task_count)

    # used_time_str = ("%d:%d" % (int(used_time / 60), int(used_time % 60)))
    left_time_str = ("%02d:%02d:%02d" % (int(left_time / 3600),
                                         int((left_time % 3600) / 60),
                                         int(left_time % 60)))

    printProgressBar(task_count, task_sum,
                     prefix=("%s (%d/%d)" % (id, task_count, task_sum)),
                     suffix=("left: %s" % left_time_str),
                     length=30)


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
            # calc_task(os.path.join(folder, image_file))
            pool.apply_async(calc_task, (folder, image_file, ),
                             callback=task_callback)
        pool.close()
        pool.join()

        with open(tmpfilename, "wb") as output:
            pickle.dump(patients, output)
    else:
        print "using existing density file: %s" % tmpfilename
        patients = pickle.load(open(tmpfilename, "rb"))
        
    print "start copy file"

    copy_all_count = len(patients) * 20
    copy_count = 0
    for id in patients:
        if not os.path.exists(os.path.join(target_folder, id)):
            os.mkdir(os.path.join(target_folder, id))
        for key, value in sorted(patients[id].iteritems(),
                                 key=lambda (k, v): (v, k))[-20:]:
            shutil.copyfile(os.path.join(folder, key),
                            os.path.join(target_folder, id, key))
            copy_count = copy_count + 1
            printProgressBar(copy_count, copy_all_count, prefix=id,
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
