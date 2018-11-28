"""
    File processing module
"""
import os
import re
import psutil
PATH = os.path.abspath(os.path.curdir)
INPUT_PATH = os.path.join('input', '')
OUTPUT_PATH = os.path.join('output', '')
USED_PATH = os.path.join('used', '')


def memory_consumption():
    """
        Show memory consumption in megabytes
    """
    process = psutil.Process(os.getpid())
    used_memory = process.memory_info().rss
    return str(round(used_memory / 1024 / 1024, 2)) + ' mb.    '


def extract_scale(name: str) -> list:
    """
        Extract scale out of the filename
        "[10] some_file.png" --> 10
        "[5-8] some_file.png" --> 5, 6, 7, 8
    """
    pattern = r'(?<=\[).+?(?=\])'
    data = re.search(pattern, name)

    if data is not None:
        input_number = data.group()

        if '-' in input_number:
            start = input_number.split('-')[0]
            end = input_number.split('-')[-1]
            if start.isdigit() and end.isdigit():
                start = max([1, int(start)])
                end = min([50, int(end)])
                return list(range(start, end + 1))

        elif input_number.isdigit():
            return [int(input_number)]

    return [6]


def get_filenames() -> list:
    """
        Search for local files
    """
    if not os.path.isdir(INPUT_PATH):
        return []

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    filenames = os.listdir(INPUT_PATH)
    filenames = map(str.lower, filenames)

    verified_files = []

    for filename in filenames:
        full_path = os.path.join(INPUT_PATH, filename)

        if os.path.exists(full_path):

            name = filename.split('.')[0]
            ext = filename.split('.')[-1]

            if ext.lower() not in ['bmp', 'jpg', 'jpeg', 'png', 'gif']:
                continue

            scales_list = extract_scale(name)

            pos = name.find(']')
            name = name[pos + 2:]

            for subscale in scales_list:
                verified_files.append({
                    'scale': subscale,
                    'path': full_path,
                    'name': '[' + str(subscale).rjust(2, '0') + '] ' + name,
                    'ext': ext,
                    'filename': filename,
                    'last_image': '[' + str(max(scales_list)).rjust(2, '0') + '] ' + name
                })

    if verified_files:
        print(f'Images in queue: {len(verified_files)}')
        for i, image in enumerate(verified_files, start=1):
            num = str(i).rjust(len(str(len(verified_files))))
            print(f'{num}. {image["name"]}.{image["ext"]}')
        print()

    return verified_files


def unique_name(old_name: str, ext: str) -> str:
    """
        Avoid overwriting
    """
    var = 1
    path = OUTPUT_PATH
    new_name = old_name
    if os.path.isfile(os.path.join(path, new_name + '.' + ext)):
        while os.path.isfile(os.path.join(path, new_name + '.' + ext)):
            var += 1
            new_name = old_name + '_(' + str(var).rjust(2, '0') + ')'
    return new_name + '.' + ext


def move_file(file_dict: dict):
    """
        Move file from 'input' to 'used'
    """
    if file_dict['name'] != file_dict['last_image']:
        return
    source = os.path.join(PATH, INPUT_PATH, file_dict['filename'])
    resulting_name = unique_name(file_dict['name'], file_dict['ext'])
    destination = os.path.join(PATH, USED_PATH, resulting_name)

    if not os.path.exists(os.path.join(PATH, USED_PATH)):
        os.mkdir(os.path.join(PATH, USED_PATH))

    os.rename(source, destination)


def save_image(file_dict: dict, image, now: str, end: str) -> int:
    """
        Saving png
    """
    if not image:
        return 0

    new_name = unique_name(file_dict['name'], 'png')

    try:
        image.save(os.path.join(OUTPUT_PATH, new_name))
        size = os.path.getsize(os.path.join(OUTPUT_PATH, new_name))
        size = round(size / 1024 / 1024, 2)
        print(f'\rImage file saved ({now} of {end}): {new_name}, size: {size:.2f} mb.')
    except OSError:
        print(f'\r              Unable to save file:{new_name}')
        return 0
    return 1


def save_gif(file_dict: dict, frames: list, now: str, end: str) -> int:
    """
        Saving gif
    """
    if not frames:
        return 0

    new_name = unique_name(file_dict['name'], 'gif')
    full_name = os.path.join(OUTPUT_PATH, new_name)

    try:
        frames[0].save(full_name, save_all=True, append_images=frames[1:], duration=100, loop=0)
        size = os.path.getsize(os.path.join(OUTPUT_PATH, new_name))
        size = round(size / 1024 / 1024, 2)
        print(f'\r  GIF file saved ({now} of {end}): {new_name}, size: {size:.2f} mb.')
    except OSError:
        print(f'\r              Unable to save file:{new_name}')
        return 0
    return 1
