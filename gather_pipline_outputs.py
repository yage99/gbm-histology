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

    for gathername, sourcename in [("cell.csv", "MyExpt_cell.csv"),
                                   ("cytoplasm.csv", "MyExpt_Cytoplasm.csv"),
                                   ("nulei.csv", "MyExpt_nulei.csv")]:

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
                    all_data_matrix[id] = numpy.append(
                        all_data_matrix[id],
                        local_all_data[id],
                        axis=0
                    )
                else:
                    all_data_matrix[id] = local_all_data[id]

            with thread_finished.get_lock():
                thread_finished.value += 1
                # print(matrix)

        for filename in cellfiles:
            # file_process_callback(file_processor(filename))
            pool.apply_async(file_processor, (filename, ),
                             callback=task_callback)

        while(thread_finished.value < len(cellfiles)):
            printProgressBar(thread_count.value,
                             thread_total.value,
                             prefix=("%d/%d (%d/%d)"
                                     % (thread_finished.value,
                                        len(cellfiles),
                                        thread_count.value,
                                        thread_total.value)),
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
                                 time_start=time_start
                                 length=40)
                matrix = all_data_matrix[id]
                if(len(matrix) < 10):
                    print("warn: %s not enough lines(%d)" % (id, len(matrix)))
                    continue

                numpy_matrix = matrix
                # numpy.array(matrix).astype(numpy.float)
                mean = []
                std = []
                for column_idx in range(numpy_matrix.shape[1]):
                    column = numpy_matrix[:, column_idx]
                    column = column[~numpy.isnan(column)]
                    mean.append(numpy.mean(column))
                    std.append(numpy.std(column))

                # append std to the end of means
                mean.extend(std)
                mean.insert(0, id)
                writer.writerow(mean)


def file_processor(filename):
    global id_matcher

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
    
    for line in reader:

        id = id_matcher.search(line[2]).group()

        numpy_line = numpy.array([line[8:]]).astype(numpy.float)
        # numpy_line[numpy.isnan(numpy_line)] = 0

        if id in local_all_data:
            local_all_data[id] = numpy.append(
                local_all_data[id],
                numpy_line,
                axis=0)

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
            local_all_data[id] = numpy_line

        with thread_count.get_lock():
            thread_count.value += 1

    return local_all_data


def recurse_find(dirname, results, contains):
    if os.path.isdir(dirname):
        for subdir in os.listdir(dirname):
            recurse_find(os.path.join(dirname, subdir), results, contains)

    else:
        if contains in dirname:
            results.append(dirname)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1], "cell.csv")
    else:
        print('enter the pipline output dir')
