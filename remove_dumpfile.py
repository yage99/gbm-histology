import subprocess32 as sp
import os
from TCGAMaxim.utils import printProgressBar


def main(source, folders):
    dir_list = []
    for dir in folders:
        _list = sp.check_output(['find', dir, '-name', '*.png']).split('\n')
        _list = map(lambda(f): os.path.basename(f), _list)
        dir_list.append(_list)

    count = 0
    for file_list in dir_list:
        count += len(file_list)
    key = raw_input("delete %d files(y/N)?" % count)
    if key != 'y':
        print 'Cancled'
        return

    i = 0
    to_delete = ['rm']
    for file_list in dir_list:
        for file in file_list:
            if len(to_delete) >= 100:
                i += len(to_delete)
                sp.call(to_delete)
                to_delete = ['rm']
                printProgressBar(i, count)
            to_delete.append(os.path.join(source, file))


if __name__ == "__main__":
    main("data/svs-processed",
         ['data/svs-processed-blanks',
          'data/svs-processed-deleted']
         )