import sys
import os
import subprocess32 as sp


def main(filepath, working_dir, target_dir):
    file = os.path.basename(filepath)

    print("del file %s in %s" % (file, working_dir))
    if(not os.path.exists(os.path.join('data/svs-best', file))):
        print "error %s not exist" % file
    else:
        sp.call(['mv', os.path.join(working_dir, file),
                 os.path.join(target_dir, file)])
        sp.call(['rm', os.path.join('data/svs-best', file)])


if __name__ == "__main__":
    files = sys.argv[1:]
    working_dir = 'data/svs-processed'
    target_dir = 'data/svs-processed-deleted'

    if(not os.path.isdir(target_dir)):
        sp.call(['mkdir', target_dir])

    if len(sys.argv) == 2 and "png" not in sys.argv[1]:
        with open(sys.argv[1], 'r') as f:
            for line in f.readlines():
                file = os.path.basename(line[:-1])
                main(file, working_dir, target_dir)
    else:
        for file in files:
            file = os.path.basename(file)
            main(file, working_dir, target_dir)
