"""

    Common utils

"""
# builtin modules
from pathlib import Path

# third-party modules
# import numpy as np
from PIL import Image


def open_image(path: str) -> Image:
    """
    Open supported image file
    """
    path = Path('input_files') / path
    suffix = path.suffix.lower()
    try:
        if suffix not in {'.png', '.jpg', '.gif', '.bmp'}:
            raise TypeError
        new_image = Image.open(path)
        new_image.load()
        image_data = new_image
    except FileNotFoundError:
        print(f'Unable to find "{path}"!')
        image_data = None
    except TypeError:
        print(f'Unsupported file type: {suffix}')
        image_data = None

    return image_data


def unique_name(filename: Path) -> str:
    """
    Ensure we're not overwriting anything
    """
    old_path = filename
    cur_path = old_path
    i = 0
    while cur_path.exists():
        filename = old_path.stem + f'_{i:02d}' + old_path.suffix
        cur_path = Path(filename)
        i += 1
    return filename


# def save_image(image_data):
#     im = Image.fromarray(image_data)
#     im.convert("RGB").save("your_file.png")


# noinspection PyBroadException
def save_text_file(filename: str, data: str):
    """
    Save text file
    """
    try:
        filename = Path('output_files') / filename
        with open(unique_name(filename), mode='w', encoding='utf-8') as file:
            file.write(data)
    except Exception as err:
        print(f'Unable to save text file: "{filename}"')
        print(f'                  Reason: {err.args[0]}')


# noinspection PyBroadException
def save_binary_file(filename: str, data: bytes):
    """
    Save binary object as a file
    """
    try:
        filename = Path('output_files') / filename
        with open(unique_name(filename), mode='wb') as file:
            file.write(data)
    except Exception as err:
        print(f'Unable to save binary file: "{filename}"')
        print(f'                    Reason: {err.args[0]}')
