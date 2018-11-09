import os
import ct_files
from ct_palette import palette
from PIL import Image, ImageDraw, ImageFont
# Based on https://gist.github.com/BigglesZX/4016539
# Based on https://gist.github.com/almost/d2832d0998ad9dfec2cacef934e7d247

TILE_HEIGHT = 16
TILE_WIDTH = 16
FONT_SIZE = 20


def generate_symbol(density, color):
    image = Image.new(mode="RGBA", size=(TILE_WIDTH, TILE_HEIGHT), color=(0, 0, 0, 255))
    font = ImageFont.truetype('Anonymous.ttf', FONT_SIZE)
    textdraw = ImageDraw.ImageDraw(image, "RGBA")
    textdraw.text((2, 0), text=palette[density], font=font, fill=color)
    return image


def base_conversion(source, size):
    width, height = size
    source = source.resize((int(size[0]/5), int(size[1]/5)), 0)
    width = int(size[0]/5)
    height = int(size[1]/5)
    image_data = source.getdata()
    color_space = len(image_data[0])

    black = (0, 0, 0, 255)
    image = Image.new(mode='RGBA', size=(width * TILE_WIDTH, height * TILE_HEIGHT), color=black)
    position = 0
    symbols = {}

    for y in range(height):
        for x in range(width):
            rgb_color = image_data[position]
            density = int(sum(rgb_color) / color_space / 255 * 100)

            if density in symbols:
                symbol = symbols[density]
            else:
                symbol = generate_symbol(density, rgb_color)
                symbols[density] = symbol

            image.paste(symbol, (x * TILE_WIDTH, y * TILE_HEIGHT))
            position += 1

    return image


def analyse_image(image):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Need to know the mode before processing all frames.
    """
    results = {'size': image.size, 'mode': 'full'}
    print(image.n_frames)
    print(dir(image))
    try:
        while True:
            if image.tile:
                tile = image.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != image.size:
                    results['mode'] = 'partial'
                    break
            image.seek(image.tell() + 1)
    except EOFError:
        pass
    return results


def make_frames(filename):
    """
    Iterate the GIF, extracting each frame.
    """
    image = Image.open(os.path.join(ct_files.INPUT_PATH, filename))
    frames = [filename]
    size = image.size
    #mode = analyse_image(image)['mode']
    gif_palette = image.getpalette()
    last_frame = image.convert('RGBA')

    for x in range(image.n_frames + 1):
        try:
            image.seek(x)

            empty_frame = Image.new('RGBA', (int(size[0]/200), int(size[1]/200)))
            smaller = image.resize((int(size[0]/200), int(size[1]/200)), 0)
            empty_frame.paste(smaller, (0, 0), smaller.convert('RGBA'))
            new_frame = base_conversion(empty_frame, empty_frame.size)
            #new_frame.show()
            frames.append(new_frame)
        except EOFError:
            break
            pass
    return frames

    try:
        while True:
            if not image.getpalette():
                image.putpalette(gif_palette)

            empty_frame = Image.new('RGBA', image.size)
            if mode == 'partial':
                empty_frame.paste(last_frame)

            empty_frame.paste(image, (0, 0), image.convert('RGBA'))
            new_frame = base_conversion(empty_frame, empty_frame.size)
            frames.append(new_frame)
            last_frame = new_frame
            image.seek(image.tell() + 1)

    except EOFError:
        pass

    return frames


def convert_image(filename):
    new_image = Image.open(os.path.join(ct_files.INPUT_PATH, filename))
    converted_image = base_conversion(source=new_image, size=new_image.size)
    ct_files.save_image(filename, converted_image)


def convert_gif(filename):
    temp_files = make_frames(filename)
    ct_files.save_gif(temp_files)


