'''
This script picks images by the number of nuleis recognized in
cellprofiler.
'''


import csv
import os
# import shutil
import re
import sys
import time
import subprocess32 as sp

ID_MATCHER = re.compile(r"TCGA-\w{2}-\w{4}-\w{3}-\w{2}-\w{3}")

sys.path.append('../')
from TCGAMaxim.utils import printProgressBar  # noqa: E402


def read_info(filename, all_infos):
    ''' reads info from a file'''
    with open(filename, "r") as inputfile:
        reader = csv.reader(inputfile, delimiter=',')

        for metas in reader:

            # if this line is header, skip
            if metas[0] == "Count_nulei":
                continue

            number_of_nuclei = float(metas[0])
            image_name = metas[1]
            patient_id = ID_MATCHER.search(metas[1]).group()

            if patient_id not in all_infos:
                all_infos[patient_id] = {}
            all_infos[patient_id][image_name] = number_of_nuclei

        return all_infos


def main(source_dir, output_dir):
    ''' main process '''
    all_infos = {}
    for i in range(20):
        filename = "outputs%d/MyExpt_Image.csv" % i
        print 'reading filename %s' % filename
        read_info(filename, all_infos)

    print "writing list file"
    with open('cell_counts.csv', 'w') as inputfile:
        for patient_id in all_infos:
            images = all_infos[patient_id]
            for name in images:
                inputfile.write("%s,%d\n" % (name, images[name]))

    print "copying files"

    all_line_count = len(all_infos)
    i = 0

    print "clean output dir"
    sp.call(['rm', '-r', output_dir])
    sp.call(['mkdir', output_dir])

    copied_files = {}
    time_start = time.time()
    for patient_id in all_infos:
        i += 1
        printProgressBar(i, all_line_count, time_start=time_start)
        for key, value in sorted(all_infos[patient_id].iteritems(),
                                 key=lambda (k, v): (v, k))[-20:]:
            parent_dir = ID_MATCHER.search(key).group()
            source = os.path.join(source_dir, parent_dir, key)
            target = os.path.join(output_dir, key)
            sp.call(['cp', source, target])
            # shutil.copy(source, target)
            copied_files[key] = value

    with open("copied_files.csv", 'w') as copied_record:
        for key, value in sorted(copied_files.iteritems(),
                                 key=lambda(k, v): (v, k)):
            copied_record.write("%s,%d\n" % (key, value))


if __name__ == "__main__":
    main('/home/zhangya/GBM/data/svs-selected',
         '/home/zhangya/GBM/data/svs-best')
