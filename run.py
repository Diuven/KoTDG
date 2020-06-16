#! /usr/bin/python3
import os
import errno

import random as rnd
import sys
from pathlib import Path
from glob import glob

from tqdm import tqdm
from trdg.string_generator import (
    create_strings_from_dict,
    create_strings_from_file,
    create_strings_from_wikipedia,
)
from trdg.utils import load_dict, load_fonts
from trdg.data_generator import FakeTextDataGenerator
from multiprocessing import Pool

from kotdg.parser import argument_parser
from kotdg.utils import ko_create_strings_randomly

base_dir = Path(os.path.realpath(__file__)).parent
resource_dir = base_dir / "resources/"


def main():
    """
        Description: Main function
    """

    # Argument parsing
    args = argument_parser().parse_args()

    # Create the directory if it does not exist.
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Create font (path) list
    if args.font_dir:
        fonts = list(glob( str(Path(args.font_dir) / "*.ttf") ))
        if len(fonts) == 0:
            raise ValueError("No fonts found from the given directory %s" % args.font_dir)
    elif args.font:
        font_path = resource_dir / 'fonts' / args.font
        if os.path.isfile(str(font_path)):
            fonts = [str(font_path)]
        else:
            sys.exit("Cannot open font")
    else:
        fonts = load_fonts(args.language)

    # Creating synthetic sentences (or word)
    strings = []

    if args.wikipedia:
        strings = create_strings_from_wikipedia(args.length, args.count, args.language)
    elif args.input_file != "":
        strings = create_strings_from_file(args.input_file, args.count)
    elif args.random:
        strings = ko_create_strings_randomly(
            args.length,
            args.variable_length,
            args.count,
            args.include_letters,
            args.include_numbers,
            args.include_symbols,
            args.language,
        )
        # Set a name format compatible with special characters automatically if they are used
        if args.include_symbols or True not in (
                args.include_letters,
                args.include_numbers,
                args.include_symbols,
        ):
            args.name_format = 2
    elif args.dict:
        # Creating word list
        lang_dict = []
        dict_path = resource_dir / "dicts" / args.dict
        if os.path.isfile(dict_path):
            with open(dict_path, "r", encoding="utf8", errors="ignore") as d:
                lang_dict = [l for l in d.read().splitlines() if len(l) > 0]
        else:
            sys.exit("Cannot open dict")

        strings = create_strings_from_dict(
            args.length, args.variable_length, args.count, lang_dict
        )
    else:
        raise RuntimeError("Source option broke... somehow")

    if args.case == "upper":
        strings = [x.upper() for x in strings]
    if args.case == "lower":
        strings = [x.lower() for x in strings]

    if args.rand_color:
        def get_color():
            if rnd.random() < 0.5:
                r, g, b = rnd.getrandbits(5), rnd.getrandbits(5), rnd.getrandbits(5)
            else:
                val = rnd.getrandbits(24)
                r, g, b = val // (2**16), (val // (2**8)) % (2**8), val % (2**8)
                if r+g+b > 128*3:
                    r, g, b = 255 - r, 255 - g, 255 - b
            return "#%02X%02X%02X" % (r, g, b)
    else:
        def get_color():
            return args.text_color

    if args.rand_back:
        def get_back():
            # img_cnt = len(glob(str(resource_dir / 'images/*.jpg')))
            val = rnd.randrange(0, 10)
            return min(3, val)
    else:
        def get_back():
            return args.background

    string_count = len(strings)

    with Pool(args.thread_count) as pool:
        def gen_tuple():
            for idx, text in enumerate(strings):
                yield (
                    idx + args.start,
                    text,
                    fonts[rnd.randrange(0, len(fonts))],
                    args.output_dir,
                    args.format,
                    args.extension,
                    args.skew_angle,
                    args.random_skew,
                    args.blur,
                    args.random_blur,
                    get_back(),
                    args.distorsion,
                    args.distorsion_orientation,
                    args.handwritten,
                    args.name_format,
                    args.width,
                    args.alignment,
                    get_color(),
                    args.orientation,
                    args.space_width,
                    args.character_spacing,
                    args.margins,
                    args.fit,
                    args.output_mask,
                    args.word_split,
                    args.image_dir
                )
        res = list(tqdm(
            pool.imap_unordered(FakeTextDataGenerator.generate_from_tuple, gen_tuple()),
            total=args.count))

        # for _ in tqdm(
        #         pool.imap_unordered(
        #             FakeTextDataGenerator.generate_from_tuple,
        #             zip(
        #                 [i for i in range(0, string_count)],
        #                 strings,
        #                 [fonts[rnd.randrange(0, len(fonts))] for _ in range(0, string_count)],
        #                 [args.output_dir] * string_count,
        #                 [args.format] * string_count,
        #                 [args.extension] * string_count,
        #                 [args.skew_angle] * string_count,
        #                 [args.random_skew] * string_count,
        #                 [args.blur] * string_count,
        #                 [args.random_blur] * string_count,
        #                 [args.background] * string_count,
        #                 [args.distorsion] * string_count,
        #                 [args.distorsion_orientation] * string_count,
        #                 [args.handwritten] * string_count,
        #                 [args.name_format] * string_count,
        #                 [args.width] * string_count,
        #                 [args.alignment] * string_count,
        #                 [args.text_color] * string_count,
        #                 [args.orientation] * string_count,
        #                 [args.space_width] * string_count,
        #                 [args.character_spacing] * string_count,
        #                 [args.margins] * string_count,
        #                 [args.fit] * string_count,
        #                 [args.output_mask] * string_count,
        #                 [args.word_split] * string_count,
        #                 [args.image_dir] * string_count,
        #             ),
        #         ),
        #         total=args.count,
        # ):
        #     pass

    if args.name_format == 2:
        # Create file with filename-to-label connections
        with open(
                os.path.join(args.output_dir, "labels.txt"), "w", encoding="utf8"
        ) as f:
            for i in range(string_count):
                file_name = str(i) + "." + args.extension
                f.write("{} {}\n".format(file_name, strings[i]))


if __name__ == "__main__":
    main()
