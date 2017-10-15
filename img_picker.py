from PIL import Image
import os
import shutil
from TCGAMaxim.utils import printProgressBar
import pickle
from multiprocessing import Pool
import time

def calc_density(image, threshold = 150):
    pixel = image.load();

    pixel_count = image.size[0] * image.size[1] * 3

    color_count = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pixel[i,j][0] < threshold:
                color_count = color_count + 1
            if pixel[i,j][1] < threshold:
                color_count = color_count + 1
            if pixel[i,j][2] < threshold:
                color_count = color_count + 1

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
    id_matcher = re.compile("TCGA-\w{2}-\w{4}")
    id = id_matcher.search(image_file).group()
    
    if id in patients:
        patients[id][image_file] =  density
    else:
        patients[id] = {image_file: density}

    task_count = task_count + 1

    current_time = time.time()
    used_time = current_time - start_time
    time_each = used_time / task_count
    left_time = time_each * (task_sum - task_count)

    used_time_str = ("%d:%d" % (int(used_time / 60), int(used_time % 60)))
    left_time_str = ("%02d:%02d:%02d" % (int(left_time / 3600),
                                         int((left_time % 3600) / 60),
                                         int(left_time % 60)))

    printProgressBar(task_count, task_sum,
                     prefix=("%s (%d/%d)" % (id, task_count, task_sum)),
                     suffix=("left: %s" % left_time_str),
                     length=30)


patients = {}
start_time = 0
def main(folder, target_folder, task_pool = 20):
    global task_count, task_sum, patients, start_time
    
    patients = {}

    task_sum = len(os.listdir(folder))

    task_count = 0
    pool = Pool(task_pool)
    #i = 0
    start_time = time.time()
    for image_file in os.listdir(folder):
        #i = i + 1
        #if i==10:
        #    break
        #calc_task(os.path.join(folder, image_file))
        pool.apply_async(calc_task, (folder, image_file, ),
                         callback=task_callback)
    pool.close()
    pool.join()
        

    with open("image_matas.pkl", "wb") as output:
        pickle.dump(patients, output)
    print "start copy file"

    for id in patients:
        if not os.path.exists(os.path.join(target_folder, id)):
            os.mkdir(os.path.join(target_folder, id))
        for key, value in sorted(patients[id].iteritems(),
                                 key=lambda (k,v): (v,k))[-10:]:
            shutil.copyfile(os.path.join(folder, key),
                            os.path.join(target_folder, id, key))

if __name__ == "__main__":
    main("/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/svs-processed",
         "/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/svs-selected")
