import sys
from skimage import io, color
import numpy as np


def calc_nuclei_threshold(image_file, threshold=150):
    rgb = io.imread(image_file)
    lab = color.rgb2lab(color.rgba2rgb(rgb))

    mean = np.mean(lab[:, :, 1]) / 100.0 * 1.5 + 0.125

    return mean


if __name__ == "__main__":
    print calc_nuclei_threshold(sys.argv[1])
