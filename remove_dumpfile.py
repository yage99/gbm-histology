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

    i = 0
    for file_list in dir_list:
        for file in file_list:
            sp.call(['rm', os.path.join(source, file)])
            i += 1
            printProgressBar(i, count)


if __name__ == "__main__":
    main("data/svs-processed",
         ['data/svs-processed-blanks',
          'data/svs-processed-deleted']
         )
