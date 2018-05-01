'''
This script is used to gather outputs of cellprofiler pipeline
of GBM histology images.
'''


import csv
import numpy
import os
import re
import sys
import time
from multiprocessing import Pool, Value

sys.path.append("../")
from TCGAMaxim.utils import printProgressBar  # noqa: E402


thread_count = Value('d', 0)
thread_total = Value('d', 0)
thread_finished = Value('d', 0)

id_matcher = re.compile("TCGA-\w{2}-\w{4}")


def main(dirname, outputname, task_pool=20):

    for gathername, sourcename in [("cell.csv",
                                    ["MyExpt_cell.csv", "MyExpt_Cells.csv"]),
                                   ("cytoplasm.csv", ["MyExpt_Cytoplasm.csv"]),
                                   ("nulei.csv",
                                    ["MyExpt_nulei.csv",
                                     "MyExpt_Nuclei.csv"])]:

        print("processing %s files" % sourcename)
        cellfiles = []

        pool = Pool(task_pool)

        recurse_find(dirname, cellfiles, sourcename)

        all_data_matrix = {}

        thread_count.value = 0
        thread_total.value = 1
        thread_finished.value = 0

        def task_callback(local_all_data):
            title = local_all_data['title']
            del local_all_data['title']

            if "title" not in all_data_matrix:
                all_data_matrix['title'] = title

            for id in local_all_data:
                if id in all_data_matrix:
                    print "warn: id gathered before, this may be fatal error"
                    # all_data_matrix[id] = numpy.append(
                    #     all_data_matrix[id],
                    #     local_all_data[id],
                    #     axis=0
                    # )
                else:
                    all_data_matrix[id] = local_all_data[id]

            with thread_finished.get_lock():
                thread_finished.value += 1
                # print(matrix)

        for filename in cellfiles:
            # task_callback(file_processor(filename))
            pool.apply_async(file_processor, (filename, ),
                             callback=task_callback)

        time_start = time.time()
        while(thread_finished.value < len(cellfiles)):
            printProgressBar(thread_count.value,
                             thread_total.value,
                             prefix=("%d/%d"
                                     % (thread_finished.value,
                                        len(cellfiles))),
                             time_start=time_start,
                             length=50)
            time.sleep(0.1)

        pool.close()
        pool.join()

        with open(gathername, "w") as f:
            print "start writing file %s" % gathername
            writer = csv.writer(f)

            title = all_data_matrix['title']
            mean_title = map(lambda x: "mean_" + x, title)
            std_title = map(lambda x: "std_" + x, title)
            title = mean_title
            title.extend(std_title)
            title.insert(0, 'id')
            writer.writerow(title)
            del all_data_matrix['title']

            all = len(all_data_matrix)
            time_start = time.time()
            i = 0
            for id in all_data_matrix:
                i = i + 1
                printProgressBar(i, all,
                                 time_start=time_start,
                                 length=40)
                # matrix = all_data_matrix[id]
                # if(len(matrix) < 10):
                #     print("warn: %s not enough lines(%d)"
                #           % (id, len(matrix)))
                #     continue

                # numpy_matrix = matrix
                # # numpy.array(matrix).astype(numpy.float)
                # mean = []
                # std = []
                # # iterate each column to remove nan value of each column
                # for column_idx in range(numpy_matrix.shape[1]):
                #     column = numpy_matrix[:, column_idx]
                #     column = column[~numpy.isnan(column)]
                #     mean.append(numpy.mean(column))
                #     std.append(numpy.std(column))

                mean, max, min, median, std = all_data_matrix[id]
                # append std to the end of means
                mean.extend(max)
                mean.extend(min)
                mean.extend(median)
                mean.extend(std)
                mean.insert(0, id)
                writer.writerow(mean)


def file_processor(filename):
    line_count = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        reader.next()

        for line in reader:
            line_count += 1

        with thread_total.get_lock():
            thread_total.value += line_count

    f = open(filename, 'r')
    reader = csv.reader(f, delimiter=',')

    local_all_data = {}
    title = reader.next()
    title = title[8:]
    local_all_data['title'] = title

    last_id = ""
    this_id_data = None
    for line in reader:

        id = id_matcher.search(line[2]).group()

        numpy_line = numpy.array([line[8:]]).astype(numpy.float)

        if last_id == id:
            # just append data if id not changed
            this_id_data = numpy.append(this_id_data, numpy_line, axis=0)
            # local_all_data[id] = numpy.append(
            #     local_all_data[id],
            #     numpy_line,
            #     axis=0)

            # this will reduce memory use
            '''if all_data_matrix[row[0]].shape[0] == 10:
            matrix = all_data_matrix[row[0]]
            mean = numpy.mean(matrix, axis=0).tolist()
            std = numpy.std(matrix, axis=0).tolist()
            mean.extend(std)
            mean.insert(0, row[0])
            writer.writerow(mean)
            del all_data_matrix[row[0]]
            '''

        else:
            if this_id_data is not None:
                mean_std = calc_mean_std(this_id_data)
                local_all_data[id] = mean_std

            this_id_data = numpy_line
            last_id = id

        with thread_count.get_lock():
            thread_count.value += 1

    return local_all_data


def calc_mean_std(numpy_matrix):
    mean = []
    max = []
    min = []
    median = []
    std = []
    # iterate each column to remove nan value of each column
    for column_idx in range(numpy_matrix.shape[1]):
        column = numpy_matrix[:, column_idx]
        column = column[~numpy.isnan(column)]
        if len(column) == 0:
            print "warn: column length is 0, fill by 0"
            column = [0]
        mean.append(numpy.mean(column))
        max.append(numpy.max(column))
        min.append(numpy.min(column))
        median.append(numpy.median(column))
        std.append(numpy.std(column))
    return (mean, max, min, median, std)


def recurse_find(dirname, results, contains):
    if os.path.isdir(dirname):
        for subdir in os.listdir(dirname):
            recurse_find(os.path.join(dirname, subdir), results, contains)
    else:
        is_valid_file = False
        for item in contains:
            if (item.upper().lower()
                    == os.path.basename(dirname).upper().lower()):
                is_valid_file = True

        if is_valid_file:
            results.append(dirname)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1], "cell.csv")
    else:
        print('enter the pipline output dir')
