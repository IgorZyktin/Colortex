"""

    Renders image into a TXT file

    Base parameters:
        image_path - full path to the image file.

        width - target width of the output image, in characters.
                Height will be calculated proportionally.

        threshold - the value of the threshold brightness (applied on black and white image).

        invert - flag to invert colors (applied on black and white image)
"""
# built-in modules
import argparse
from pathlib import Path

# third-party modules
import numpy as np
from PIL import Image

# project modules
from palette import PALETTE
from utils import open_image, save_text_file


def image_to_txt(image_path: str, width: int, threshold: int = 255, invert: bool = False) -> str:
    """
    Render media file into TXT document
    """
    image = open_image(image_path)
    image = scale(image, width)
    image = image_to_array(image)
    image = colored_to_grayscale(image)

    if threshold < 255:
        image = apply_threshold(image, threshold)

    if invert:
        image = apply_invert(image)

    image = brightness_to_density(image)
    image = density_to_characters(image, PALETTE)

    result = array_to_string(image)
    return result


# noinspection SpellCheckingInspection
def scale(image: Image, new_width: int) -> Image:
    """
    Downscale image to a more handy size.
    Note that we're additionally upscaling the width, making image a bit wider,
    so it still looks proportional in text mode. Distortion happens because usually
    text characters are not square.

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
    text_width_ratio: float = 2.125

    cur_width = image.width
    cur_height = image.height

    base_ratio = new_width / cur_width

    # maximum values are just in case
    width = min(int(cur_width * base_ratio * text_width_ratio), 10_000)
    height = min(int(cur_height * base_ratio), 10_000)

    result = image.resize((width, height))
    return result


def image_to_array(image: Image) -> np.array:
    """
    Turn PIL Image into numpy array
    """
    result = np.asarray(image, dtype="int32")
    return result


def colored_to_grayscale(image: np.array) -> np.array:
    """
    Turn image into grayscale using mean of the RGB values
    """
    if image.shape[2] == 3:
        weights = np.array([0.2989, 0.5870, 0.1140])
    else:
        weights = np.array([0.2989, 0.5870, 0.1140, 1])

    tile = np.tile(weights, reps=(image.shape[0], image.shape[1], 1))
    result = np.sum(tile * image, axis=2, dtype="uint8")
    return result


def apply_threshold(image: np.array, threshold: int = 128) -> np.array:
    """
    Simple threshold function, anything below threshold will be 0, anything above will be 255
    """
    result = ((image > threshold) * 255).astype("uint8")
    return result


def apply_invert(image: np.array) -> np.array:
    """
    Invert colors from black to white and vice versa.
    """
    result = np.invert(image)
    return result


def brightness_to_density(image: np.array) -> np.array:
    """
    Turn color value into density value
    """
    result = (image / 2.55).astype("uint8")
    return result


def density_to_characters(image: np.array, palette: dict) -> np.array:
    """
    Turn density numbers into actual characters
    """
    result = np.vectorize(palette.get)(image)
    return result


# noinspection SpellCheckingInspection
def array_to_string(image: np.array) -> str:
    """
    Turn numpy array into regular string

    Input:
        [['r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r']
         ['r' 'r' 'w' 'w' 'w' 'w' 't' 't' 't' 't' 't' 'w' 'w' 'w' 'w' 'r' 'r']
         ['r' 'r' 'w' 'w' 'w' 'w' 't' 't' 't' 't' 't' 'w' 'w' 'w' 'w' 'r' 'r']
         ['r' 'r' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 'r' 'r']
         ['r' 'r' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 't' 'r' 'r']
         ['r' 'r' 'w' 'w' 'w' 'w' 't' 't' 't' 't' 't' 'w' 'w' 'w' 'w' 'r' 'r']
         ['r' 'r' 'w' 'w' 'w' 'w' 't' 't' 't' 't' 't' 'w' 'w' 'w' 'w' 'r' 'r']
         ['r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r' 'r']]

    Output:
        rrrrrrrrrrrrrrrrr
        rrwwwwtttttwwwwrr
        rrwwwwtttttwwwwrr
        rrtttttttttttttrr
        rrtttttttttttttrr
        rrwwwwtttttwwwwrr
        rrwwwwtttttwwwwrr
        rrrrrrrrrrrrrrrrr
    """
    lines = [''.join(item) for item in image.astype(str)]
    result = '\n'.join(lines)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rendering settings.')
    parser.add_argument('-path', type=str, help='Path to an image file.')
    parser.add_argument('-width', type=int, help='Width of the output document (characters)')
    parser.add_argument('-threshold', type=int, default=255, help='Cut brightness below this.')
    parser.add_argument('-invert', type=int, default=0, help='Invert colors before processing.')
    parser.add_argument('-overwrite', type=int, default=0,
                        help='Preserve existing files with the same name.')
    arguments = parser.parse_args()

    path = arguments.path
    data = image_to_txt(
        image_path=path,
        width=arguments.width,
        threshold=arguments.threshold,
        invert=bool(arguments.invert)
    )

    save_text_file(Path(path).with_suffix('.txt'), data, bool(arguments.overwrite))
