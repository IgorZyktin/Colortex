"""
    File processing module
"""
import os
from PIL import Image
PATH = os.path.abspath(os.path.curdir)
INPUT_PATH = os.path.join('input', '')
OUTPUT_PATH = os.path.join('output', '')


def get_files():
    """ Retirve local files"""
    filenames = os.listdir(INPUT_PATH)

    gifs = []
    imgs = []

    for filename in filenames:
        full_path = os.path.join(INPUT_PATH, filename)

        if os.path.exists(full_path):
            if full_path.lower().endswith('gif'):
                gifs.append(filename)
            else:
                imgs.append(filename)

    if imgs:
        print(f'Images found: {len(imgs)}')
        for i, image in enumerate(imgs, start=1):
            num = str(i).rjust(len(str(len(imgs))))
            print(f'{num}. {image}')
        print()

    if gifs:
        print(f'Gif images found: {len(gifs)}')
        for i, gif in enumerate(gifs, start=1):
            num = str(i).rjust(len(str(len(gifs))))
            print(f'{num}. {gif}')
        print()

    return imgs, gifs


def unique_name(old_name, ext):
    """ Avoid overwriting """
    var = 1
    filepath = OUTPUT_PATH
    new_name = old_name
    if os.path.isfile(os.path.join(filepath, new_name + '.' + ext)):
        while os.path.isfile(os.path.join(filepath, new_name + '.' + ext)):
            var += 1
            new_name = old_name + '_(' + str(var) + ')'
    return new_name + '.' + ext


def save_image(filename, image):
    if not image:
        return 0

    name = filename.split('.')[0]
    ext = filename.split('.')[-1]
    new_name = unique_name(name, ext)
    image.save(os.path.join(OUTPUT_PATH, new_name), ext)
    print(f'Saved: {new_name}')


def save_gif(frames):
    if not frames:
        return 0
    print(frames)
    frames[1].show()
    old_name = frames[0].split('.')[0]
    del frames[0]
    new_name = unique_name(old_name, 'gif')
    full_name = os.path.join(OUTPUT_PATH, new_name + '.gif')
    frames[0].save(full_name, save_all=True, append_images=frames[1:], duration=100, loop=0)
    print(f'Saved: {new_name}')
