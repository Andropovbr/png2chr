from PIL import Image

from i18n import t

TILE_SIZE = 8


def load_image(path):
    return Image.open(path).convert("RGBA")


def normalize_color(color):
    r, g, b, a = color

    if a == 0:
        return (0, 0, 0, 0)

    return (r, g, b, 255)


def validate_image_size(image):
    width, height = image.size

    if width % TILE_SIZE != 0 or height % TILE_SIZE != 0:
        raise ValueError(
            t(
                "error_image_size",
                width=width,
                height=height
            )
        )


def get_tile_count(image):
    width, height = image.size
    return (width // TILE_SIZE) * (height // TILE_SIZE)