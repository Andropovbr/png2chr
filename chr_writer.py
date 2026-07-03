from image_tools import TILE_SIZE
from analyzer import get_pixel_color, collect_tile_colors


def convert_tile_to_chr(image, tile_x, tile_y, replacements, palette=None):
    if palette:
        color_map = {color: index for index, color in enumerate(palette)}
    else:
        colors, _ = collect_tile_colors(image, tile_x, tile_y, replacements)
        color_map = {color: index for index, color in enumerate(colors)}

    plane0 = []
    plane1 = []

    for y in range(TILE_SIZE):
        byte_plane0 = 0
        byte_plane1 = 0

        for x in range(TILE_SIZE):
            color = get_pixel_color(image, tile_x + x, tile_y + y, replacements)
            color_index = color_map[color]

            bit0 = color_index & 1
            bit1 = (color_index >> 1) & 1

            shift = 7 - x

            byte_plane0 |= bit0 << shift
            byte_plane1 |= bit1 << shift

        plane0.append(byte_plane0)
        plane1.append(byte_plane1)

    return bytes(plane0 + plane1)


def convert_image_to_chr(image, replacements, palette=None):
    width, height = image.size
    chr_data = bytearray()

    for tile_y in range(0, height, TILE_SIZE):
        for tile_x in range(0, width, TILE_SIZE):
            chr_data.extend(
                convert_tile_to_chr(
                    image,
                    tile_x,
                    tile_y,
                    replacements,
                    palette
                )
            )

    return chr_data


def parse_pad_size(value):
    value = value.lower().strip()

    aliases = {
        "4k": 4096,
        "8k": 8192,
        "16k": 16384,
    }

    if value in aliases:
        return aliases[value]

    size = int(value)

    if size <= 0:
        raise ValueError("Pad size must be greater than zero.")

    return size


def pad_chr_data(chr_data, target_size):
    current_size = len(chr_data)

    if current_size > target_size:
        raise ValueError(
            f"CHR data has {current_size} bytes, larger than pad size {target_size}."
        )

    padding = target_size - current_size
    chr_data.extend(b"\x00" * padding)

    return padding


def save_chr(path, chr_data):
    with open(path, "wb") as file:
        file.write(chr_data)