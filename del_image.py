#!/usr/bin/python

import sys
import os
import subprocess32 as sp
import re


def main(filepath, working_dir, target_dir,
         best_dir='data/svs-best',
         overlay_dir=None):
    file = os.path.basename(filepath)
    if 'threshold' in file:
        thstr = re.compile(r'threshold_.*\.(png|tiff)$')
        origin_file = thstr.sub('.png', file)
    else:
        origin_file = file

    if file.endswith('tiff'):
        best_file = file.replace('tiff', 'png')
    else:
        best_file = file

    print("del file %s in %s" % (origin_file, working_dir))
    if(not os.path.exists(os.path.join(best_dir, best_file))):
        print "error %s not exist in %s" % (best_file, best_dir)
    else:
        sp.call(['mv', os.path.join(working_dir, origin_file),
                 os.path.join(target_dir, origin_file)])
        sp.call(['rm', os.path.join(best_dir, best_file)])
        if overlay_dir is not None:
            sp.call(['rm', os.path.join(overlay_dir, file)])


if __name__ == "__main__":
    files = sys.argv[1:]
    working_dir = 'data/svs-processed'
    target_dir = 'data/svs-processed-deleted'
    best_dir = 'data/svs-best-new'
    overlay_dir = 'data/svs-best-overlay'

    if(not os.path.isdir(target_dir)):
        sp.call(['mkdir', target_dir])

    if len(sys.argv) == 2 and not ("png" in sys.argv[1]
                                   or "tiff" in sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
            for line in f.readlines():
                file = os.path.basename(line[:-1])
                main(file, working_dir, target_dir,
                     best_dir=best_dir,
                     overlay_dir=overlay_dir)
    else:
        for file in files:
            file = os.path.basename(file)
            main(file, working_dir, target_dir, best_dir=best_dir,
                 overlay_dir=overlay_dir)
