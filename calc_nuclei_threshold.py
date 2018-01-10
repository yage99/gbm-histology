import sys
from skimage import io, color
import numpy as np


def calc_nuclei_threshold(image_file, threshold=150):
    rgba = io.imread(image_file)
    rgb = color.rgba2rgb(rgba)

    # lab = color.rgb2lab(rgb)
    # threshold = 0.5 + np.mean(lab[:, :, 1]) / 100 * 0.3

    unmixed = unmix_color(rgb)
    mean = np.mean(unmixed)
    threshold = mean + 0.1

    return threshold


def html_color(rgb):
    '''Return an HTML color for a given stain'''
    rgb = np.exp(-np.array(rgb)) * 255
    rgb = rgb.astype(int)
    color = hex((rgb[0] * 256 + rgb[1]) * 256 + rgb[2])
    if color.endswith("L"):
        color = color[:-1]
    return "#" + color[2:]


CHOICE_HEMATOXYLIN = "Hematoxylin"
ST_HEMATOXYLIN = (0.644, 0.717, 0.267)
COLOR_HEMATOXYLIN = html_color(ST_HEMATOXYLIN)

CHOICE_EOSIN = "Eosin"
ST_EOSIN = (0.093, 0.954, 0.283)
COLOR_EOSIN = html_color(ST_EOSIN)

STAIN_DICTIONARY = {
    CHOICE_EOSIN: ST_EOSIN,
    CHOICE_HEMATOXYLIN: ST_HEMATOXYLIN,
    }

STAINS_BY_POPULARITY = (
    CHOICE_HEMATOXYLIN, CHOICE_EOSIN,
    )

FIXED_SETTING_COUNT = 2
VARIABLE_SETTING_COUNT = 5


def unmix_color(input_pixels):
    '''Produce one image - storing it in the image set'''
    inverse_absorbances = get_inverse_absorbances(CHOICE_HEMATOXYLIN)
    #########################################
    #
    # Renormalize to control for the other stains
    #
    # Log transform the image data
    #
    # First, rescale it a little to offset it from zero
    #
    eps = 1.0 / 256.0 / 2.0
    image = input_pixels + eps
    log_image = np.log(image)
    #
    # Now multiply the log-transformed image
    #
    scaled_image = (log_image
                    * inverse_absorbances[np.newaxis, np.newaxis, :])
    #
    # Exponentiate to get the image without the dye effect
    #
    image = np.exp(np.sum(scaled_image, 2))
    #
    # and subtract out the epsilon we originally introduced
    #
    image -= eps
    image[image < 0] = 0
    image[image > 1] = 1
    image = 1 - image

    return image


def get_inverse_absorbances(choice):
    '''Given one of the outputs, return the red, green and blue
    absorbance'''

    result = STAIN_DICTIONARY[choice]
    result = np.array(result)
    result = result / np.sqrt(np.sum(result ** 2))
    return result


if __name__ == "__main__":
    print calc_nuclei_threshold(sys.argv[1])
