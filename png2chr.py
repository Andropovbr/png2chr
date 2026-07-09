#!/usr/bin/env python3

import argparse
import textwrap

from i18n import load_language, t
from image_tools import load_image, validate_image_size, get_tile_count
from palette_tools import parse_palette, build_replacements
from version import __version__

from analyzer import (
    collect_image_colors,
    analyze_tiles,
    suggest_palette,
)
from debug_tools import save_debug_tile, save_debug_map

from chr_writer import (
    convert_image_to_chr,
    save_chr,
    parse_pad_size,
    pad_chr_data,
    dedupe_chr_data,
    save_tile_map,
    concat_chr_files,
)


def print_colors(colors, counts=None):
    for index, color in enumerate(colors):
        if counts:
            print(t("color_line_with_count", index=index, color=color, count=counts[color]))
        else:
            print(t("color_line", index=index, color=color))


def print_problem(problem, show_color_count=False):
    reason = t(problem["reason"])

    if show_color_count:
        print(
            t(
                "tile_problem_with_color_count",
                col=problem["tile_col"],
                row=problem["tile_row"],
                reason=reason,
                count=len(problem["colors"]),
            )
        )
    else:
        print(
            t(
                "tile_problem",
                col=problem["tile_col"],
                row=problem["tile_row"],
                reason=reason,
            )
        )


def command_analyze(args):
    image = load_image(args.input)
    validate_image_size(image)

    replacements = build_replacements(args.replace)

    colors, counts = collect_image_colors(image, replacements)
    problems = analyze_tiles(image, replacements)

    width, height = image.size

    print(t("analysis_title"))
    print("-----------------")
    print(f"{t('file')}: {args.input}")
    print(f"{t('size')}: {width}x{height}")
    print(f"{t('tiles')}: {get_tile_count(image)}")
    print()

    print(f"{t('colors_found')}:")
    print_colors(colors, counts)
    print()

    suggested = suggest_palette(colors)

    print(f"{t('suggested_palette')}:")
    print_colors(suggested)
    print()

    if problems:
        print(f"{t('problem_tiles')}:")
        for problem in problems:
            print_problem(problem, show_color_count=True)

        debug_map = save_debug_map(image, problems)
        print()
        print(t("debug_map_saved", filename=debug_map))

        if args.debug:
            first = problems[0]
            debug_tile = save_debug_tile(image, first, replacements)
            print(t("debug_tile_saved", filename=debug_tile))
    else:
        print(t("no_problems"))


def command_convert(args):
    image = load_image(args.input)
    validate_image_size(image)

    replacements = build_replacements(args.replace)

    if args.palette:
        palette = parse_palette(args.palette)
    else:
        colors, _ = collect_image_colors(image, replacements)

        if len(colors) > 4:
            raise ValueError(
                t(
                    "error_too_many_global_colors",
                    count=len(colors)
                )
            )

        palette = colors

    problems = analyze_tiles(image, replacements, palette)

    if problems:
        print(t("error_problem_tiles"))
        print()

        for problem in problems[:10]:
            print_problem(problem)

        debug_map = save_debug_map(image, problems)
        print()
        print(t("debug_map_saved", filename=debug_map))

        if args.debug:
            first = problems[0]
            debug_tile = save_debug_tile(image, first, replacements, palette)
            print(t("debug_tile_saved", filename=debug_tile))

        raise SystemExit(1)

    chr_data = convert_image_to_chr(image, replacements, palette)

    removed_tiles = 0
    tile_map = None

    if args.dedupe:
        chr_data, tile_map, removed_tiles = dedupe_chr_data(chr_data)

        if args.tile_map:
            save_tile_map(args.tile_map, tile_map)

    padding_added = 0

    if args.pad:
        pad_size = parse_pad_size(args.pad)
        padding_added = pad_chr_data(chr_data, pad_size)

    save_chr(args.output, chr_data)

    width, height = image.size

    print(t("conversion_completed"))
    print(t("image_size", width=width, height=height))
    print(t("tiles_generated", count=get_tile_count(image)))
    print(t("chr_size", size=len(chr_data)))

    if args.dedupe:
        print(t("dedupe_removed", count=removed_tiles))

    if args.tile_map:
        print(t("tile_map_saved", filename=args.tile_map))

    if args.pad:
        print(t("padding_added", size=padding_added))

    print()
    print(f"{t('global_palette_used')}:")
    print_colors(palette)


def build_parser():
    description = t("arg_description")

    epilog = textwrap.dedent(
        f"""
        {t("help_examples_title")}:

          {t("help_example_analyze")}:
            python3 png2chr.py analyze player.png

          {t("help_example_analyze_debug")}:
            python3 png2chr.py analyze player.png --debug

          {t("help_example_convert")}:
            python3 png2chr.py convert player.png player.chr

          {t("help_example_convert_pad")}:
            python3 png2chr.py convert player.png player.chr --pad 8k

          {t("help_example_palette")}:
            python3 png2chr.py convert player.png player.chr \\
              --palette "0,0,0,0;0,0,0,255;248,56,0,255;252,224,168,255"

          {t("help_example_replace")}:
            python3 png2chr.py convert player.png player.chr \\
              --replace "63,63,116,255=0,0,0,255"

          {t("help_example_dedupe")}:
            python3 png2chr.py convert player.png player.chr \\
              --dedupe --tile-map player_tile_map.txt

          {t("help_example_lang")}:
            python3 png2chr.py --lang en analyze player.png
        """
    )

    parser = argparse.ArgumentParser(
        description=f"{t('arg_description')} ({__version__})",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--lang",
        help=t("arg_lang_help")
    )

    parser.add_argument(
        "--version",
        action="version",
        version=(
            f"%(prog)s {__version__}\n"
            "Copyright (c) 2026 André Santos\n"
            "Licensed under the MIT License."
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        title=t("help_commands_title"),
        description=t("help_commands_description")
    )

    analyze = subparsers.add_parser(
        "analyze",
        help=t("arg_analyze_help"),
        description=t("arg_analyze_description"),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    analyze.add_argument("input", help=t("arg_input_help"))
    analyze.add_argument(
        "--replace",
        action="append",
        default=[],
        help=t("arg_replace_help")
    )
    analyze.add_argument(
        "--debug",
        action="store_true",
        help=t("arg_debug_help")
    )

    convert = subparsers.add_parser(
        "convert",
        help=t("arg_convert_help"),
        description=t("arg_convert_description"),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    convert.add_argument("input", help=t("arg_input_help"))
    convert.add_argument("output", help=t("arg_output_help"))
    convert.add_argument(
        "--palette",
        help=t("arg_palette_help")
    )
    convert.add_argument(
        "--replace",
        action="append",
        default=[],
        help=t("arg_replace_help")
    )
    convert.add_argument(
        "--debug",
        action="store_true",
        help=t("arg_debug_help")
    )
    convert.add_argument(
        "--pad",
        help=t("arg_pad_help")
    )
    convert.add_argument(
        "--dedupe",
        action="store_true",
        help=t("arg_dedupe_help")
    )
    convert.add_argument(
        "--tile-map",
        help=t("arg_tile_map_help")
    )

    concat = subparsers.add_parser(
        "concat",
        help=t("arg_concat_help"),
        description=t("arg_concat_description"),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    concat.add_argument(
        "files",
        nargs="+",
        help=t("arg_concat_files_help")
    )

    concat.add_argument(
        "--pad",
        help=t("arg_pad_help")
    )

    concat.add_argument(
        "--dedupe",
        action="store_true",
        help=t("arg_dedupe_help")
    )

    concat.add_argument(
        "--tile-map",
        help=t("arg_tile_map_help")
    )

    return parser


def command_concat(args):
    if len(args.files) < 2:
        raise ValueError(t("error_concat_min_files"))

    input_files = args.files[:-1]
    output_file = args.files[-1]

    chr_data = concat_chr_files(input_files)

    original_tile_count = len(chr_data) // 16

    removed_tiles = 0
    tile_map = None

    if args.dedupe:
        chr_data, tile_map, removed_tiles = dedupe_chr_data(chr_data)

        if args.tile_map:
            save_tile_map(args.tile_map, tile_map)

    padding_added = 0

    if args.pad:
        pad_size = parse_pad_size(args.pad)
        padding_added = pad_chr_data(chr_data, pad_size)

    save_chr(output_file, chr_data)

    print(t("concat_completed"))
    print(t("input_files_count", count=len(input_files)))
    print(t("tiles_input", count=original_tile_count))
    print(t("chr_size", size=len(chr_data)))

    if args.dedupe:
        print(t("dedupe_removed", count=removed_tiles))

        if args.tile_map:
            print(t("tile_map_saved", filename=args.tile_map))

    if args.pad:
        print(t("padding_added", size=padding_added))

    print(t("output_file", filename=output_file))

def main():
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--lang")

    pre_args, _ = pre_parser.parse_known_args()

    load_language(pre_args.lang)

    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "analyze":
            command_analyze(args)
        elif args.command == "convert":
            command_convert(args)
        elif args.command == "concat":
            command_concat(args)

    except Exception as error:
        print(f"{t('error')}: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()