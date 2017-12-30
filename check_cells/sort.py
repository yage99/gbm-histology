'''
This file can sort any csv file
'''


import csv


def main(inputfile, outputfile):
    '''
    this is the main func
    '''
    with open(inputfile, 'r') as inputhandle, open(outputfile, 'w') as output:
        reader = csv.reader(inputhandle)

        for line in sorted(reader, key=lambda(k): (int(k[1]), k[0])):
            output.write("%s,%s\n" % (line[0], line[1]))


if __name__ == "__main__":
    main("cell_counts.csv", "cell_count_sorted.csv")
