"""

    Common utils

"""
# builtin modules
from pathlib import Path
from common.defaults import IMAGE_TYPES

# third-party modules
import numpy as np
from PIL import Image


def open_image(path: str) -> Image:
    """
    Open supported image file
    """
    path = Path(path)
    suffix = path.suffix.lower()
    try:
        if suffix not in IMAGE_TYPES:
            raise TypeError
        img = Image.open(path)
        img.load()
        data = img
    except FileNotFoundError:
        print(f'Unable to find "{path}"!')
        data = None
    except TypeError:
        print(f'Unsupported file type: {suffix}')
        data = None

    return data


def save_image(image_data):
    im = Image.fromarray(image_data)
    im.convert("RGB").save("your_file.png")


def save_txt_file():
    pass
