"""

    Renders image into a TXT file

"""
# builtin modules
from common.utils import open_image, save_image

# third-party modules
import numpy as np
from PIL import Image

# project modules
from common.defaults import TEXT_WIDTH_RATIO
from ct_palette import DENSITY_LIST, PALETTE

density_list = np.array(DENSITY_LIST)


def get_closest_multiplier(input_multiplier: int):
    """

    """
    return input_multiplier


# noinspection SpellCheckingInspection
def fix_text_ratio(image: Image):
    """
    Make image a bit wider, so it still looks proportional in text mode.
    Distortion happens because usually text characters are not square.

    Original image:
        44444444
        4WWWWWW4
        4WWooWW4
        4WooooW4
        4WooooW4
        4WWooWW4
        4WWWWWW4
        44444444

    With fixed ratio:
        44444444444444444
        44WWWWWWWWWWWWW44
        44WWWWoooooWWWW44
        44WWoooooooooWW44
        44WWoooooooooWW44
        44WWWWoooooWWWW44
        44WWWWWWWWWWWWW44
        44444444444444444
    """
    new_width = int(image.width * TEXT_WIDTH_RATIO)
    new_height = image.height
    return image.resize((new_width, new_height))


def to_grayscale(image: np.array) -> np.array:
    """
    Turn image into grayscale using mean of the RGB values
    """
    weights = np.array([0.2989, 0.5870, 0.1140, 0])
    tile = np.tile(weights, reps=(image.shape[0], image.shape[1], 1))
    return np.sum(tile * image, axis=2, dtype="uint8")


def apply_threshold(image: np.array, threshold: int = 128) -> np.array:
    """
    Simple threshold function, anything below threshold will be 0, anything above will be 255
    """
    return ((image > threshold) * 255).astype("uint8")


def calc_density(image: np.array) -> np.array:
    """
    Turn color value into density value
    """
    print(image)
    print((image / 2.55).astype("uint8"))
    return (image / 2.55).astype("uint8")


def turn_into_text(image: np.array, palette: dict) -> np.array:
    """
    Turn density numbers into actual characters
    """
    # keys = np.array(list(palette.keys()))
    # print(keys)
    # values = np.array(list(palette.values()))
    # print(values)
    #
    # indexes = keys.argsort()
    # print(indexes)
    # print(image)
    f = np.vectorize(palette.get)(image)
    # print(f)
    return f
    # array([[23, 34, 36],
    #        [36, 34, 45]])

    # return vs[np.searchsorted(ks, image)]


def into_text(image: np.array) -> str:
    """
    Turn array into regular string
    """
    lines = [''.join(item) for item in image.astype(str)]
    return '\n'.join(lines)

def downscale(image, ratio):
    new_width = int(image.width / ratio)
    new_height = int(image.height / ratio)
    return image.resize((new_width, new_height))


def render_txt(image_path: str, width: int):
    """
    Render media file into TXT document
    """
    image = open_image(image_path)
    image = fix_text_ratio(image)
    image = downscale(image, 10)

    image_data = np.asarray(image, dtype="int32")
    x = to_grayscale(image_data)
    # print(x)
    # x =
    x = calc_density(x)
    x = turn_into_text(x, PALETTE)
    # save_image(x)
    f = into_text(x)
    with open('zzz.txt', mode='w', encoding='utf-8') as file:
        file.write(f)

    print(f)

import time
start = time.perf_counter()
render_txt('1.png', width=16)
end = time.perf_counter()
print(end - start)

