''' In this script, different data sources are compared with their patient id,
the patients without full data categories will be disgard. The output files
will have identical patients id list.
'''

import csv
import re
import os


id_matcher = re.compile("TCGA-\w{2}-\w{4}")


def instance_unified(histology_file_list, cbioportal_file_list, clinical_file):
    clinical_reader = csv.reader(open(clinical_file, 'r'), delimiter=',')
    clinical_data = []
    # bypass header
    header = clinical_reader.next()
    for line in clinical_reader:
        if line[1] == "None":
            pass
        else:
            clinical_data.append(line)

    clinical_writer = csv.writer(
        open('source/' + os.path.basename(clinical_file), 'w'),
        delimiter=',')
    clinical_writer.writerow(header)
    for line in clinical_data:
        clinical_writer.writerow(line)

    for file in histology_file_list:
        histology_dict = {}
        reader = csv.reader(open(file, 'r'), delimiter=',')
        
        writer = csv.writer(open('source/' + os.path.basename(file), 'w'),
                            delimiter=',')
        header = reader.next()

        for line in reader:
            id = id_matcher.search(line[0]).group()
            histology_dict[id] = line

        writer.writerow(header)
        emptyrow = [None] * len(header)
        for patient in clinical_data:
            if patient[0] in histology_dict:
                writer.writerow(histology_dict[patient[0]])
            else:
                emptyrow[0] = patient[0]
                writer.writerow(emptyrow)

    for file in cbioportal_file_list:
        cbioportal_dict = {}
        reader = csv.reader(open(file, 'r'), delimiter='\t')
        writer = csv.writer(open('source/' + os.path.basename(file), 'w'),
                            delimiter=',')
        ids = reader.next()[2:]
        ids = map(lambda x: id_matcher.search(x).group(), ids)
        header = ['id']
        for id in ids:
            cbioportal_dict[id] = []

        for line in reader:
            header.append(line[0])
            line = line[2:]
            for i in range(len(ids)):
                cbioportal_dict[ids[i]].append(line[i])

        writer.writerow(header)
        emptyrow = [None] * len(header)
        for patient in clinical_data:
            if patient[0] in cbioportal_dict:
                line = cbioportal_dict[patient[0]]
                line.insert(0, patient[0])
                writer.writerow(line)
            else:
                emptyrow[0] = patient[0]
                writer.writerow(emptyrow)


if __name__ == "__main__":
    instance_unified(['pipeline/cell.csv',
                      'pipeline/cytoplasm.csv',
                      'pipeline/nulei.csv'],
                     ['cbioportal/data_expression_Zscores.txt',
                      'cbioportal/data_linear_CNA.txt',
                      'cbioportal/data_mRNA_median_Zscores.txt'],
                     'TCGAMaxim/clinical.csv')
