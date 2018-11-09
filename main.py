"""

    Colortex - simple textual painter

"""
import ct_images
import ct_files


def main():
    """
    Main flow
    """
    print('[Colortex image conversion script]')
    total_converted = 0
    local_imgs, local_gifs = ct_files.get_files()

    if not local_imgs and not local_gifs:
        print('Nothing to convert')
        return

    for filename in local_imgs:
        ct_images.convert_image(filename)
        total_converted += 1

    for filename in local_gifs:
        ct_images.convert_gif(filename)
        total_converted += 1

    print(f'Conversion complete, {total_converted} files converted.')


if __name__ == '__main__':
    main()
