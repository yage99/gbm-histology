import run
import retrive_best_images
import os
import subprocess32 as sp


def main():
    selected_dir = '/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-selected'
    best_dir = '/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-best'
    print 'counting cell numbers'
    run.main(selected_dir)

    if(not os.path.isdir(best_dir)):
        sp.call(['mkdir', best_dir])
    else:
        sp.call(['rm', os.path.join(best_dir, '*')])

    print 'copying images'
    retrive_best_images.main(selected_dir, best_dir)


if __name__ == "__main__":
    main()
