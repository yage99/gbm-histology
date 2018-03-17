# -*- coding: utf-8 -*-

# from TCGAMaxim.svs import svs
import openslide
from TCGAMaxim.meta import meta
import os
import sys
import multiprocessing as mp
from TCGAMaxim.utils import printProgressBar
import PIL
import re

allFilesCount = 0
currentFileProcessed = 0
ID_REGEXP = re.compile("TCGA-\w{2}-\w{4}-\w{3}-\w{2}-\w{3}")


def log_callback(result):
    global currentFileProcessed, allFilesCount
    currentFileProcessed = currentFileProcessed + 1
    print("Overall Progressing: %d/%d" % (currentFileProcessed, allFilesCount))
    printProgressBar(currentFileProcessed, allFilesCount)


def process(location, svsFile):
    slide = openslide.OpenSlide(os.path.join(location, svsFile))
    # get magnification of the slide
    appmag = int(slide.properties['aperio.AppMag'])
    id = ID_REGEXP.search(svsFile).group()
    unit = 512

    piece_start = [0, 0]
    width, height = slide.dimensions
    slide_count = 0
    if appmag == 20:
        # when it's 20x, get pic directlywhile piece_start[1] < height:
        while piece_start[1] < height:
            while piece_start[0] < width:
                img = slide.read_region(piece_start, 0, (unit, unit))
                img.save(os.path.join('data/svs-processed-20X',
                                      ('%s_%04d.png' % (id, slide_count))))
                slide_count += 1
                piece_start[0] += unit

            piece_start[0] = 0
            piece_start[1] += unit

    elif appmag == 40:
        # when 40x, read larger image and downsample
        while piece_start[1] < height:
            while piece_start[0] < width:
                img = slide.read_region(piece_start, 0, (unit*2, unit*2))
                img = img.resize((unit, unit), PIL.Image.LANCZOS)
                slide_count += 1
                piece_start[0] += unit*2

            piece_start[0] = 0
            piece_start[1] += unit*2
    else:
        return

    # slide = svs(os.path.join(location, svsFile))
    # thread = Thread(target = slide.slideWholeSlide,
    #         args = (slide.location, 1024,))
    # pool.apply_async(slide.slideWholeSlide,
    #                 args = (slide.location, 1024, ),
    #                 callback = log_callback)
    # slide.slideWholeSlide("data/svs-processed", 1024)


def main(metaFile):
    global allFilesCount
    svsSlides = meta(metaFile)
    location, filename = os.path.split(metaFile)
    print location

    pool = mp.Pool(20)

    for id, svsFile in svsSlides.files():
        pool.apply_async(process, (location, svsFile, ),
                         callback=log_callback)

        allFilesCount = allFilesCount + 1

        # thread.start()
        # thread.join()
        # threads.append(thread)

    pool.close()
    pool.join()

    # for thread in threads:
    #    thread.join()


if __name__ == '__main__':
    # print sys.argv
    main(sys.argv[1])
