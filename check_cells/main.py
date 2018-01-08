import run
import retrive_best_images
import os
import subprocess32 as sp


def main():
    selected_dir = '../data/svs-selected'
    best_dir = '../data/svs-best'
    best_overlay_dir = '../data/svs-best-overlay'
    print 'counting cell numbers'
    run.main(selected_dir)

    if(os.path.isdir(best_dir)):
        sp.call(['rm', '-r', best_dir])
    sp.call(['mkdir', best_dir])

    if os.path.isdir(best_overlay_dir):
        sp.call(['rm', '-r', best_overlay_dir])
    sp.call(['mkdir', best_overlay_dir])
    sp.call(['mv', 'outputs*/*.tiff', '.'])

    print 'copying images'
    retrive_best_images.main(selected_dir, best_dir, best_overlay_dir)
    sp.call(['rm', '*.tiff'])


if __name__ == "__main__":
    main()
