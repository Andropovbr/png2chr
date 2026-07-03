from image_tools import normalize_color
from i18n import t


def parse_color(text):
    parts = text.split(",")

    if len(parts) not in (3, 4):
        raise ValueError(
            t(
                "error_invalid_color",
                color=text
            )
        )

    values = tuple(int(part.strip()) for part in parts)

    if len(values) == 3:
        values = values + (255,)

    for value in values:
        if value < 0 or value > 255:
            raise ValueError(
                t(
                    "error_color_component",
                    color=text
                )
            )

    return normalize_color(values)


def parse_palette(text):
    colors = [parse_color(part) for part in text.split(";") if part.strip()]

    if len(colors) != 4:
        raise ValueError(
            t("error_palette_size")
        )

    return colors


def parse_replace(text):
    if "=" not in text:
        raise ValueError(
            t(
                "error_invalid_replace",
                replace=text
            )
        )

    source_text, target_text = text.split("=", 1)

    source = parse_color(source_text)
    target = parse_color(target_text)

    return source, target


def build_replacements(items):
    replacements = {}

    for item in items:
        source, target = parse_replace(item)
        replacements[source] = target

    return replacements


def apply_replacement(color, replacements):
    return replacements.get(color, color)