'''
This script picks images by the number of nuleis recognized in
cellprofiler.
'''


import csv
import os
import shutil
import re

id_matcher = re.compile("TCGA-\w{2}-\w{4}-\w{3}-\w{2}-\w{3}")


def read_info(filename):
    global id_matcher
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=',')

        all_infos = {}
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


def main():
    all_infos = {}
    for i in range(20):
        file = "outputs%d/.csv" % i
        print 'reading file %s' % file
        all_infos.extend(read_info(file))

    print "copying files"

    for id in all_infos:
        for key, value in sorted(all_infos[id].iteritems(),
                                 key=lambda (k, v): (v, k))[-10:]:
            parent_folder = id_matcher.search(key).group()
            source = os.path.join("/media/af214dbe-b6fa-4f5e\
-932a-14b133ba4766/zhangya/svs-selected", parent_folder, key)
            target = os.path.join("/media/af214dbe-b6fa-4f5e\
-932a-14b133ba4766/zhangya/svs-best", key)
            shutil.copy(source, target)


if __name__ == "__main__":
    main()
