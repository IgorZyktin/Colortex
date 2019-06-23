"""

    Colortex - simple textual painter

    Based on:
        https://gist.github.com/BigglesZX/4016539
        https://gist.github.com/almost/d2832d0998ad9dfec2cacef934e7d247

"""
# builtin modules
import argparse
from pathlib import Path

# project modules
from utils import save_binary_file, save_text_file
from text_renderer import image_to_txt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rendering settings.')
    parser.add_argument('-kind', type=str, help='Kind of rendering (text or image).')
    parser.add_argument('-path', type=str, help='Path to an image file.')
    parser.add_argument('-width', type=int, help='Width of the output document (pixels/characters)')
    parser.add_argument('-threshold', type=int, default=255,
                        help='Cut brightness below this in text mode).')
    parser.add_argument('-invert', type=int, default=0, help='Invert colors before processing.')
    arguments = parser.parse_args()

    if arguments.kind == 'text':
        path = arguments.path
        data = image_to_txt(path, width=arguments.width, threshold=arguments.threshold,
                            invert=bool(arguments.invert))

        save_text_file(Path(path).with_suffix('.txt'), data)
    else:
        pass
        # total_converted = 0
        # local_files = ct_files.get_filenames()
        #
        # if not local_files:
        #     print('Nothing to convert')
        #     return
        #
        # for i, file_dict in enumerate(local_files, start=1):
        #     total_converted += ct_images.convert(file_dict, i, len(local_files))
        #
        # if total_converted:
        #     print(f'\nConversion complete, {total_converted} files converted.')
        # else:
        #     print('\nComplete. No files converted.')
