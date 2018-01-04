import subprocess32 as sp
import os
from TCGAMaxim.utils import printProgressBar


def remove_dumpfile(source, folders):
    dir_list = []
    for dir in folders:
        print "finding files in folder %s" % dir
        _list = os.listdir(dir)
        _list = map(lambda(f): os.path.basename(f), _list)
        dir_list.append(_list)

    count = 0
    for file_list in dir_list:
        count += len(file_list)
    key = raw_input("delete %d files(y/N)? " % count)
    if key != 'y':
        print 'Cancled'
        return

    i = 0
    to_delete = ['rm']
    for file_list in dir_list:
        for file in file_list:
            if len(to_delete) > 100:
                i += len(to_delete) - 1
                sp.call(to_delete)
                to_delete = ['rm']
                printProgressBar(i, count)
            if file != '':
                to_delete.append(os.path.join(source, file))

    sp.call(to_delete)


if __name__ == "__main__":
    remove_dumpfile("data/svs-processed",
                    ['data/svs-processed-blanks',
                     'data/svs-processed-deleted']
                    )
