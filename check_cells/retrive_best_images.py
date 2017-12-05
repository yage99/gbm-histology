'''
This script picks images by the number of nuleis recognized in
cellprofiler.
'''


import csv
import os
import shutil
import re
import sys
import subprocess32 as sp
import time

id_matcher = re.compile("TCGA-\w{2}-\w{4}-\w{3}-\w{2}-\w{3}")

sys.path.append('../')
from TCGAMaxim.utils import printProgressBar  # noqa: E402


def read_info(filename, all_infos):
    global id_matcher
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=',')

        for metas in reader:

            # if this line is header, skip
            if(metas[0] == "Count_nulei"):
                continue

            number_of_nuclei = float(metas[0])
            image_name = metas[1]
            id = id_matcher.search(metas[1]).group()

            if id not in all_infos:
                all_infos[id] = {}
            all_infos[id][image_name] = number_of_nuclei
            
        return all_infos


def main(source_dir, output_dir):
    all_infos = {}
    for i in range(20):
        file = "outputs%d/MyExpt_Image.csv" % i
        print 'reading file %s' % file
        read_info(file, all_infos)

    print "copying files"

    all = len(all_infos)
    i = 0

    print "clean output folder"
    output_folder = output_dir
    sp.call(['rm', '-r', output_folder])
    sp.call(['mkdir', output_folder])

    time_start = time.time()
    for id in all_infos:
        i += 1
        printProgressBar(i, all, time_start=time_start)
        for key, value in sorted(all_infos[id].iteritems(),
                                 key=lambda (k, v): (v, k))[-10:]:
            parent_folder = id_matcher.search(key).group()
            source = os.path.join(source_dir, parent_folder, key)
            target = os.path.join(output_folder, key)
            shutil.copy(source, target)


if __name__ == "__main__":
    main('/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-selected',
         '/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/\
svs-best')
