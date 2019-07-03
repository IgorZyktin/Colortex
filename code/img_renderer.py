"""

    Renders image into a PNG or GIF file

    Base parameters:
        image_path - full path to the image file.

        width - target width of the output image, in pixels.
                Height will be calculated proportionally.

        invert - flag to invert colors (applied on black and white image)
"""
# built-in modules
import argparse
from pathlib import Path

# third-party modules
from PIL import Image, ImageDraw, ImageFont

# project modules
import numpy as np
from palette import PALETTE
from utils import open_image, save_binary_file

TILE_HEIGHT = 16
TILE_WIDTH = 16
FONT_SIZE = 20

alphabet = {}


def image_to_png(image_path: str, width: int, invert: bool = False):
    """
    Render media file into cute PNG document
    """
    image = open_image(image_path)
    image = scale(image, width)
    font = ImageFont.truetype('Anonymous.ttf', FONT_SIZE)

    text_tile = Image.new(mode="L", size=(TILE_WIDTH, TILE_HEIGHT), color=(255,))
    draw = ImageDraw.Draw(text_tile)
    draw.text((2, 0), "X", (0,), font=font)
    x = np.array(text_tile)
    print(x)

    rows = 10
    columns = 10

    result_x_size = TILE_WIDTH * columns
    result_y_size = TILE_HEIGHT * rows

    # img_stitched = np.zeros((result_y_size, result_x_size), dtype=np.uint8)
    img_stitched = np.random.randint(0, 255) * np.ones((result_x_size, result_y_size), dtype=np.uint8)

    # for i in range(columns):
    #     for j in range(rows):
    #         x = TILE_WIDTH * i
    #         y = TILE_HEIGHT * j
    #         img_stitched[x:x+TILE_WIDTH, y:y+TILE_HEIGHT] = x

    print(img_stitched)
    img = Image.fromarray(img_stitched).convert('RGB')

    # def add_img(mxi, myi, nxi, nyi, img):
    #     assert img.shape == (img_ysize, img_xsize)
    #     xi = nxi * (mx * img_xsize + wgap) + mxi * img_xsize
    #     yi = nyi * (my * img_ysize + wgap) + myi * img_ysize
    #     img_stitched[yi:yi + img_ysize, xi:xi + img_xsize] = img
    #
    # for nxi, nyi, mxi, myi in product(range(nx), range(ny), range(mx), range(my)):
    #     # ... get image data
    #     img = np.random.randint(0, 255) * np.ones((img_ysize, img_xsize), dtype=np.uint8)
    #     add_img(mxi, myi, nxi, nyi, img)


    # plt.imshow(img_stitched)
    # plt.colorbar()
    # plt.show(block=False)
    # raw_input("Enter")

    img.save("a_test.png")

    # print(dir(x))
    return bytes(image)


def image_to_gif(image_path: str, width: int, invert: bool = False):
    """
    Render media file into cute GIF document
    """
    image = open_image(image_path)
    image = scale(image, width)
    return b''


def process_gif():
    pass


def process_image():
    pass


def scale(image: Image, new_width: int) -> Image:
    """
    Downscale image to a more handy size.
    """
    cur_width = image.width
    cur_height = image.height

    base_ratio = new_width / cur_width

    # maximum values are just in case
    width = min(int(cur_width * base_ratio), 10_000)
    height = min(int(cur_height * base_ratio), 10_000)

    # make sure that the tiles are fitting
    width = int(width / TILE_WIDTH) * TILE_WIDTH
    height = int(height / TILE_HEIGHT) * TILE_HEIGHT

    result = image.resize((width, height))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rendering settings.')
    parser.add_argument('-path', type=str, help='Path to an image file.')
    parser.add_argument('-width', type=int, help='Width of the output document (pixels)')
    parser.add_argument('-invert', type=int, default=0, help='Invert colors before processing.')
    parser.add_argument('-overwrite', type=int, default=0,
                        help='Preserve existing files with the same name.')
    arguments = parser.parse_args()

    path = Path(arguments.path)

    if path.suffix == '.gif':
        data = image_to_gif(
            image_path=path,
            width=arguments.width,
            invert=bool(arguments.invert)
        )
        save_binary_file(Path(path).with_suffix('.gif'), data, bool(arguments.overwrite))

    else:
        data = image_to_png(
            image_path=path,
            width=arguments.width,
            invert=bool(arguments.invert)
        )
        save_binary_file(Path(path).with_suffix('.png'), data, bool(arguments.overwrite))
