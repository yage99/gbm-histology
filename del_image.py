import sys
import os
import subprocess32 as sp


def main(file, working_dir, target_dir):
    print("del file %s in %s" % (file, working_dir))
    if(not os.path.exists(os.path.join('/media/af214dbe-b6fa-4f5e-932a\
-14b133ba4766/zhangya/svs-best', file))):
        print "error %s not exist" % file
    else:
        sp.call(['mv', os.path.join(working_dir, file),
                 os.path.join(target_dir, file)])
        sp.call(['rm', os.path.join('/media/af214dbe-b6fa-4f5e-932a\
-14b133ba4766/zhangya/svs-best', file)])


if __name__ == "__main__":
    file = sys.argv[1]
    working_dir = '/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-processed'
    target_dir = '/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-processed-deleted'

    if(not os.path.isdir(target_dir)):
        sp.call(['mkdir', target_dir])

    main(file, working_dir, target_dir)
