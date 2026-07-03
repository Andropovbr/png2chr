from PIL import Image, ImageDraw
from image_tools import TILE_SIZE
from analyzer import get_pixel_color

DEBUG_SCALE = 32


def save_debug_tile(image, problem, replacements, palette=None):
    tile_col = problem["tile_col"]
    tile_row = problem["tile_row"]
    tile_x = problem["tile_x"]
    tile_y = problem["tile_y"]
    colors = problem["colors"]

    output_name = f"debug_tile_col{tile_col}_row{tile_row}.png"

    debug_image = Image.new(
        "RGBA",
        (TILE_SIZE * DEBUG_SCALE, TILE_SIZE * DEBUG_SCALE),
        (255, 255, 255, 255)
    )

    draw = ImageDraw.Draw(debug_image)

    if palette:
        color_to_index = {color: index for index, color in enumerate(palette)}
    else:
        color_to_index = {color: index for index, color in enumerate(colors)}

    for y in range(TILE_SIZE):
        for x in range(TILE_SIZE):
            color = get_pixel_color(image, tile_x + x, tile_y + y, replacements)
            index = color_to_index.get(color, "?")

            fill_color = (220, 220, 220, 255) if color[3] == 0 else color

            left = x * DEBUG_SCALE
            top = y * DEBUG_SCALE
            right = left + DEBUG_SCALE
            bottom = top + DEBUG_SCALE

            draw.rectangle(
                [left, top, right, bottom],
                fill=fill_color,
                outline=(0, 0, 0, 255)
            )

            draw.text(
                (left + 10, top + 8),
                str(index),
                fill=(0, 0, 0, 255)
            )

    debug_image.save(output_name)
    return output_name


def save_debug_map(image, problems):
    width, height = image.size

    debug_image = image.copy().convert("RGBA")
    draw = ImageDraw.Draw(debug_image)

    for problem in problems:
        tile_x = problem["tile_x"]
        tile_y = problem["tile_y"]

        draw.rectangle(
            [tile_x, tile_y, tile_x + TILE_SIZE - 1, tile_y + TILE_SIZE - 1],
            outline=(255, 0, 0, 255),
            width=1
        )

    output_name = "debug_problem_tiles.png"
    debug_image.save(output_name)

    return output_name