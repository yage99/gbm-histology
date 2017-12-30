import subprocess32 as sp
import os
from TCGAMaxim.utils import printProgressBar


def main(source, folders):
    source_list = sorted(
            sp.check_output(['find', source, '-name', '*.png']).split('\n'))
    source_list = map(lambda(f): os.path.basename(f), source_list)
    dir_list = []
    for dir in folders:
        _list = sorted(
            sp.check_output(['find', dir, '-name', '*.png']).split('\n'))
        _list = map(lambda(f): os.path.basename(f), _list)
        dir_list.append(_list)

    to_delete = []
    for file_name in source_list:
        for file_list in dir_list:
            if file_name in file_list:
                to_delete.append[file_name]
                file_list.remove(file_name)
                break

    count = len(to_delete)
    i = 0
    for file in to_delete:
        sp.call(['rm', os.path.join(source, file)])
        i += 1
        printProgressBar(i, count)


if __name__ == "__main__":
    main("data/svs-processed",
         ['data/svs-processed-blanks',
          'data/svs-processed-deleted']
         )
