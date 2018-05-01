from run import calc_threshold_task
import os
import sys
import time

sys.path.append('../')
from TCGAMaxim.utils import printProgressBar  # noqa: E402


def calc_threshold(file_list):
    length = len(file_list)
    count = 0
    time_start = time.time()
    for file in file_list:
        count += 1
        calc_threshold_task(file)
        printProgressBar(count, length, time_start=time_start)


if __name__ == "__main__":
    file_list = os.listdir(sys.argv[1])
    file_list = map(lambda x: os.path.join(sys.argv[1], x), file_list)
    calc_threshold(file_list)
