"""

    Colortex - simple textual painter

    Based on:
        https://gist.github.com/BigglesZX/4016539
        https://gist.github.com/almost/d2832d0998ad9dfec2cacef934e7d247

"""
import ct_images
import ct_files


def main():
    """
    Main flow
    """
    print('[Colortex image conversion script]')
    print()

    total_converted = 0
    local_files = ct_files.get_filenames()

    if not local_files:
        print('Nothing to convert')
        return

    for file_dict in local_files:
        total_converted += ct_images.convert(file_dict)

    if total_converted:
        print(f'Conversion complete, {total_converted} files converted.')
    else:
        print('Complete. No files converted.')


if __name__ == '__main__':
    main()
