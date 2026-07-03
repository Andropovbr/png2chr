from image_tools import TILE_SIZE, normalize_color
from palette_tools import apply_replacement


REASON_COLOR_OUTSIDE_PALETTE = "reason_color_outside_palette"
REASON_TOO_MANY_COLORS = "reason_too_many_colors"


def get_pixel_color(image, x, y, replacements):
    color = normalize_color(image.getpixel((x, y)))
    return apply_replacement(color, replacements)


def collect_image_colors(image, replacements):
    colors = []
    counts = {}

    width, height = image.size

    for y in range(height):
        for x in range(width):
            color = get_pixel_color(image, x, y, replacements)

            if color not in colors:
                colors.append(color)
                counts[color] = 0

            counts[color] += 1

    return colors, counts


def collect_tile_colors(image, tile_x, tile_y, replacements):
    colors = []
    positions = {}

    for y in range(TILE_SIZE):
        for x in range(TILE_SIZE):
            color = get_pixel_color(image, tile_x + x, tile_y + y, replacements)

            if color not in colors:
                colors.append(color)
                positions[color] = []

            positions[color].append((x + 1, y + 1))

    return colors, positions


def analyze_tiles(image, replacements, palette=None):
    width, height = image.size
    problems = []

    for tile_y in range(0, height, TILE_SIZE):
        for tile_x in range(0, width, TILE_SIZE):
            colors, positions = collect_tile_colors(
                image,
                tile_x,
                tile_y,
                replacements
            )

            tile_col = tile_x // TILE_SIZE + 1
            tile_row = tile_y // TILE_SIZE + 1

            if palette:
                invalid_colors = [color for color in colors if color not in palette]

                if invalid_colors:
                    problems.append({
                        "tile_col": tile_col,
                        "tile_row": tile_row,
                        "tile_x": tile_x,
                        "tile_y": tile_y,
                        "colors": colors,
                        "positions": positions,
                        "reason": REASON_COLOR_OUTSIDE_PALETTE,
                        "invalid_colors": invalid_colors,
                    })
            else:
                if len(colors) > 4:
                    problems.append({
                        "tile_col": tile_col,
                        "tile_row": tile_row,
                        "tile_x": tile_x,
                        "tile_y": tile_y,
                        "colors": colors,
                        "positions": positions,
                        "reason": REASON_TOO_MANY_COLORS,
                        "invalid_colors": [],
                    })

    return problems


def suggest_palette(colors):
    transparent = (0, 0, 0, 0)

    ordered = []

    if transparent in colors:
        ordered.append(transparent)

    for color in colors:
        if color != transparent:
            ordered.append(color)

    return ordered[:4]