import os
import csv
import re
import subprocess32 as sp
import sys


FILE_MATCHER = re.compile(r'threshold_.*\.(png|tiff)$')


def main(csv_file):
    reader = csv.reader(open(csv_file, 'r'))
    for line in reader:
        print line
        realname = FILE_MATCHER.sub(".png", line[0])

        sp.call(['ln', '-s',
                 os.path.abspath(os.path.join('data/svs-processed', realname)),
                 os.path.join('data/svs-selected-by-hand',
                              line[0].replace('tiff', 'png')),
                 ])


if __name__ == "__main__":
    main(sys.argv[1])
