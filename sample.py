import os
import subprocess32 as sp
import random


def pick_images(source, target):
    if os.path.exists(target):
        sp.call(['rm', '-r', target])
    sp.call(['mkdir', '-p', target])

    files = os.listdir(source)
    sample = random.sample(files, 500)
    for file in sample:
        sp.call(['ln', '-s', os.path.abspath(os.path.join(source, file)),
                 os.path.join(target, file)])


if __name__ == "__main__":
    pick_images("data/svs-selected-by-hand", "data/tmp/smallData")
