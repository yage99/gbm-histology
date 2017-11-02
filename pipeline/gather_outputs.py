'''
This script is used to gather outputs of cellprofiler pipeline 
of GBM histology images.
'''


import csv
import re
import os
import sys
import numpy
sys.path.append("../")
from TCGAMaxim.utils import printProgressBar

id_matcher = re.compile("TCGA-\w{2}-\w{4}")
def main(dirname, outputname):
    for gathername, sourcename in [("cell.csv", "MyExpt_cell.csv"),
                                   ("cytoplasm.csv", "MyExpt_Cytoplasm.csv"),
                                   ("nulei.csv", "MyExpt_nulei.csv")]:
        print("processing %s files" % sourcename)
        cellfiles = []

        recurse_find(dirname, cellfiles, sourcename)
        all_data_matrix = {}
        with open(gathername, "w") as f:
            writer = csv.writer(f)

            i = 0
            all = len(cellfiles)
            for filename in cellfiles:
                i=i+1
                printProgressBar(i, all, prefix=filename, length=50)
                features = file_processor(filename)

                for row in features:
                    if row[0] in all_data_matrix:
                        all_data_matrix[row[0]] = numpy.append(
                            all_data_matrix[row[0]],
                            numpy.array([row[1:]]).astype(numpy.float),
                            axis=0)

                        # this will reduce memory use
                        if all_data_matrix[row[0]].shape[0] == 10:
                            matrix = all_data_matrix[row[0]]
                            mean = numpy.mean(matrix, axis=0).tolist()
                            std = numpy.std(matrix, axis=0).tolist()
                            mean.extend(std)
                            mean.insert(0, row[0])
                            writer.writerow(mean)
                            del all_data_matrix[row[0]]

                    else:
                        all_data_matrix[row[0]] = numpy.array(
                            [row[1:]]).astype(numpy.float)
                        #print(matrix)

            all = len(all_data_matrix)
            i = 0
            for id in all_data_matrix:
                i = i + 1
                printProgressBar(i, all,
                                 prefix=("%s(%d/%d)" % (id, i, all)),
                                 length=40)
                matrix = all_data_matrix[id]
                if(len(matrix) < 10 ):
                    print("warn: %s not enough lines(%d)" % (id, len(matrix)))
                        
                numpy_matrix = matrix#numpy.array(matrix).astype(numpy.float)
                mean = numpy.mean(numpy_matrix, axis=0)
                std = numpy.std(numpy_matrix, axis=0)
                mean_list = mean.tolist()
                std_list = std.tolist()
                mean_list.extend(std_list)
                mean_list.insert(0, id)
                writer.writerow(mean_list)



def file_processor(filename):
    global id_matcher
    
    all_features = []
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",")

        reader.next()   # skip the first meta line
        for line in reader:
            id = id_matcher.search(line[2]).group()

            features = line[8:]
            features.insert(0, id)

            all_features.append(features)

    return all_features


def recurse_find(dirname, results, contains):
    if os.path.isdir(dirname):
        for subdir in os.listdir(dirname):
            recurse_find(os.path.join(dirname, subdir), results, contains)
        
    else:
        if contains in dirname:
            results.append(dirname)


if __name__ == "__main__":
    main(".", "cell.csv")
    
