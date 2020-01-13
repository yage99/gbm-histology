#!/usr/bin/python

import img_picker
from check_cells.main import select_best_imgs
import run_pipeline

if __name__ == '__main__':
    img_picker.main("data/svs-processed",
                    "data/svs-selected")
    select_best_imgs()

    run_pipeline.batch_num = 100
    run_pipeline.batch_mode = 'fix batch'
    run_pipeline.run_pipeline(
            folder='data/svs-best', working_dir='data/pipeline',
            project_file='pipeline.cpproj', thread_num=20)
