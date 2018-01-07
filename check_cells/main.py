import run
import retrive_best_images
import os
import subprocess32 as sp


def main():
    selected_dir = '/home/zhangya/GBM/data/svs-selected'
    best_dir = '/home/zhangya/GBM/data/svs-best'
    best_overlay_dir = '/home/zhangya/GBM/data/svs-best-overlay'
    print 'counting cell numbers'
    run.main(selected_dir)

    if(os.path.isdir(best_dir)):
        sp.call(['rm', os.path.join(best_dir, '*')])

    sp.call(['mkdir', best_dir])
    sp.call(['mkdir', best_overlay_dir])
    sp.call(['mv', 'outputs*/*.tiff', '.'])

    print 'copying images'
    retrive_best_images.main(selected_dir, best_dir, best_overlay_dir)
    sp.call(['rm', '*.tiff'])


if __name__ == "__main__":
    main()
