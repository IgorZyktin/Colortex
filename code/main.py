"""

    Colortex - simple textual painter

    Based on:
        https://gist.github.com/BigglesZX/4016539
        https://gist.github.com/almost/d2832d0998ad9dfec2cacef934e7d247

"""
from code import ct_files, ct_images


def main():
    """
    Main flow
    """
    print('--- Colortex image conversion script ---')

    total_converted = 0
    local_files = ct_files.get_filenames()

    if not local_files:
        print('Nothing to convert')
        return

    for i, file_dict in enumerate(local_files, start=1):
        total_converted += ct_images.convert(file_dict, i, len(local_files))

    if total_converted:
        print(f'\nConversion complete, {total_converted} files converted.')
    else:
        print('\nComplete. No files converted.')


if __name__ == '__main__':
    main()
