import run
import glob
import sys
import retrive_best_images
import os
import subprocess32 as sp


def select_best_imgs(recalc_threshold=False):
    # in my machine, 30 threads use too much memory
    THREAD_NUM = 25

    selected_dir = '../data/svs-selected'
    best_dir = '../data/svs-best-new'
    best_overlay_dir = '../data/svs-best-overlay'
    print 'counting cell numbers'
    run.main(selected_dir, recalc_threshold=recalc_threshold,
             thread_num=THREAD_NUM)

    if(os.path.isdir(best_dir)):
        sp.call(['rm', '-r', best_dir])
    sp.call(['mkdir', best_dir])

    if os.path.isdir(best_overlay_dir):
        sp.call(['rm', '-r', best_overlay_dir])
    sp.call(['mkdir', best_overlay_dir])
    # if copy once will cause list too long error
    for i in range(THREAD_NUM):
        # sp.call(['mv', 'outputs%d/*.tiff' % i, '.'])
        files = glob.glob('outputs%d/*.tiff' % i)
        for file in files:
            sp.call(['mv', file, '.'])

    print 'copying images'
    retrive_best_images.main(selected_dir, best_dir,
                             overlay_dir=best_overlay_dir,
                             thread_num=THREAD_NUM,
                             num_to_retrive=20)
    to_remove = glob.glob('*.tiff')
    to_remove.insert(0, 'rm')
    sp.call(to_remove)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 't':
            select_best_imgs(True)
    else:
        select_best_imgs()
