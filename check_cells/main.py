import run
import sys
import retrive_best_images
import os
import subprocess32 as sp


def select_best_imgs(recalc_threshold=False):
    selected_dir = '../data/svs-selected'
    best_dir = '../data/svs-best'
    best_overlay_dir = '../data/svs-best-overlay'
    print 'counting cell numbers'
    run.main(selected_dir, recalc_threshold=recalc_threshold)

    if(os.path.isdir(best_dir)):
        sp.call(['rm', '-r', best_dir])
    sp.call(['mkdir', best_dir])

    if os.path.isdir(best_overlay_dir):
        sp.call(['rm', '-r', best_overlay_dir])
    sp.call(['mkdir', best_overlay_dir])
    # if copy once will cause list too long error
    for i in range(20):
        sp.call(['mv', 'outputs%d/*.tiff' % i, '.'])

    print 'copying images'
    retrive_best_images.main(selected_dir, best_dir, best_overlay_dir)
    sp.call(['rm', '*.tiff'])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 't':
            select_best_imgs(True)
    else:
        select_best_imgs()
