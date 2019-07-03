"""

    Common utils

"""
# builtin modules
from typing import Union
from pathlib import Path

# third-party modules
# import numpy as np
from PIL import Image


# def save_image(image_data):
#     im = Image.fromarray(image_data)
#     im.convert("RGB").save("your_file.png")


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
    i = 0
    name = filename.stem
    while filename.exists():
        suffix = filename.suffix
        filename = filename.with_name(f'{name}_{i:02d}{suffix}')
        i += 1
    return filename


def save_text_file(filename: str, data: str, overwrite: bool = False) -> None:
    """
    Save text file
    """
    save_file(filename, data, {'mode': 'w', 'encoding': 'utf-8'}, 'text', overwrite)


def save_binary_file(filename: str, data: bytes, overwrite: bool = False) -> None:
    """
    Save binary object as a file
    """
    save_file(filename, data, {'mode': 'wb'}, 'binary', overwrite)


# noinspection PyBroadException
def save_file(filename: str, data: Union[str, bytes],
              settings: dict, kind: str, overwrite: bool) -> None:
    """
    Generic file saving function
    """
    if not Path('output_files').exists():
        Path('output_files').mkdir()

    filename = Path('output_files') / filename
    if not overwrite:
        filename = unique_name(filename)

    try:
        with open(filename, **settings) as file:
            file.write(data)
            print(f'{filename} has been saved.')
    except Exception as err:
        spacer = '  ' if kind == 'text' else ''
        print(f'Unable to save {kind} file: "{filename}"')
        print(f'                   {spacer}Reason: {err.args[0]}')
