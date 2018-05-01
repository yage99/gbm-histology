from PIL import Image
import sys
from TCGAMaxim.meta import meta
import openslide
import os
import re
from TCGAMaxim.utils import printProgressBar
import time
from multiprocessing import Pool, Value
import subprocess32 as sp


ID_MATCHER = re.compile('(TCGA-\w{2}-\w{4}-\w{3}-\w{2}-\w{3})(_([0-9]*))?')
count = Value('d', 0)
length = 0
time_start = 0


def read_mag(file):
    slide = openslide.OpenSlide(file)
    return int(slide.properties['aperio.AppMag'])


def read_meta_list(meta_file):
    svsSlides = meta(meta_file)
    location = os.path.dirname(os.path.abspath(meta_file))

    meta_list = {}

    for id, file in svsSlides.files():
        file_id = ID_MATCHER.search(file).group(1)
        meta_list[file_id] = read_mag(os.path.join(location, file))

    return meta_list


def split_file(mag, file, working_dir, target_dir, type=2):
    match_result = ID_MATCHER.search(file)
    id = match_result.group(1)
    sequence = match_result.group(3)

    if type == 1:
        if mag == 20:
            # split to four pics
            image = Image.open(os.path.join(working_dir, file))
            a = image.crop((0, 0, 512, 512))
            a.load()
            a.save(os.path.join(target_dir, '%s_%s0.png' % (id, sequence)))
            b = image.crop((512, 0, 1024, 512))
            b.load()
            b.save(os.path.join(target_dir, '%s_%s1.png' % (id, sequence)))
            c = image.crop((0, 512, 512, 1024))
            c.load()
            c.save(os.path.join(target_dir, '%s_%s2.png' % (id, sequence)))
            d = image.crop((512, 512, 1024, 1024))
            d.load()
            d.save(os.path.join(target_dir, '%s_%s3.png' % (id, sequence)))
        elif mag == 40:
            # just resize the image
            image = Image.open(os.path.join(working_dir, file))
            image.resize((512, 512), Image.LANCZOS)
            image.save(os.path.join(target_dir, '%s_%s.png' % (id, sequence)))
    elif type == 2:
        if mag == 20:
            sp.call(['cp', os.path.join(working_dir, file),
                     os.path.join(target_dir, file)])

    with count.get_lock:
        count.value += 1


def main(meta_file, working_dir, target_dir):
    file_meta = read_meta_list(meta_file)

    file_list = os.listdir(working_dir)
    length = len(file_list)

    time_start = time.time()
    pool = Pool(20)
    for file in file_list:
        id = ID_MATCHER.search(file).group(1)
        mag = file_meta[id]
        if mag != 20 and mag != 40:
            continue
        pool.apply_async(split_file, (mag, file, working_dir, target_dir))

    while count.value < length - 1:
        printProgressBar(count.value, length, time_start=time_start)
        time.sleep(0.5)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
