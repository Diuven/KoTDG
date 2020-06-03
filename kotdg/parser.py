# From trdg's run.py

import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def margins(margin):
    margins = margin.split(",")
    if len(margins) == 1:
        return [int(margins[0])] * 4
    return [int(m) for m in margins]


def argument_parser():
    """
        Parse the command line arguments of the program.
    """
    # Edits: added groups, ...
    # Honestly, the names of args are so awkward in original repo

    parser = argparse.ArgumentParser(
        description="Generate synthetic text data for text recognition."
    )

    """
        Output configuration (count, directory, extension, ...)
    """
    output_g = parser.add_argument_group("output", "Output Configurations")
    output_g.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",
        help="The number of images to be created.",
        required=True,
    )
    output_g.add_argument(
        "--output_dir",
        type=str,
        nargs="?",
        help="The output directory",
        default="out/"
    )
    output_g.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="The language to use, should be\
            ko (Korean), fr (French), en (English), es (Spanish), de (German), cn (Chinese), hi (Hindi)",
        default="ko",
    )
    output_g.add_argument(
        "-w",
        "--length",
        type=int,
        nargs="?",
        help="Define how many words should be included in each generated sample.\
            If the text source is Wikipedia, this is the MINIMUM length",
        default=1,
    )
    output_g.add_argument(
        "-e",
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension to save the image with",
        default="jpg",
    )
    output_g.add_argument(
        "-na",
        "--name_format",
        type=int,
        help="Define how the produced files will be named.\
            0: [TEXT]_[ID].[EXT],\
            1: [ID]_[TEXT].[EXT],\
            2: [ID].[EXT] + one file labels.txt containing id-to-label mappings",
        default=0,
    )

    """
        Text Sources (dict/random/string/wiki/file)
    """
    source_ex = parser.add_mutually_exclusive_group()
    source_ex.add_argument(
        "-i",
        "--input_file",
        type=str,
        nargs="?",
        help="When set, this argument uses a specified text file as source for the text\
            Each lines are separated  (by .splitlines()) and maximum 200 characters of each lines are used",
        default="",
    )
    source_ex.add_argument(
        "-wk",
        "--wikipedia",
        action="store_true",
        help="Use Wikipedia as the source text for the generation.",
        default=False,
    )
    source_ex.add_argument(
        "-dt",
        "--dict",
        "--dictionary",
        type=str,
        nargs="?",
        help="Specify the name of the dictionary to be used.\
            Each lines are separated by .splitlines(), and the orders of the lines are scrambled.",
        default="words.txt"
    )
    source_ex.add_argument(
        "-rs",
        "--random",
        action="store_true",
        help="Use random sequences as the source text for the generation.\
            Set '-let','-num','-sym' to use letters/numbers/symbols. If none specified, all three are used.",
        default=False,
    )
    string_g = parser.add_argument_group("string", "String construction options")
    string_g.add_argument(
        "--variable_length",
        action="store_true",
        help="Define if the produced string will have variable word count (with --length being the maximum)",
        default=False,
    )
    string_g.add_argument(
        "-let",
        "--include_letters",
        action="store_true",
        help="Define if random sequences should contain letters. Only works with -rs",
        default=False,
    )
    string_g.add_argument(
        "-num",
        "--include_numbers",
        action="store_true",
        help="Define if random sequences should contain numbers. Only works with -rs",
        default=False,
    )
    string_g.add_argument(
        "-sym",
        "--include_symbols",
        action="store_true",
        help="Define if random sequences should contain symbols. Only works with -rs",
        default=False,
    )

    """
        Text configuration (font, color, orientation, spacing, ...)
    """
    text_g = parser.add_argument_group("text", "Text configurations")
    text_g.add_argument(
        "-tc",
        "--text_color",
        type=str,
        nargs="?",
        help="Define the text's color, should be either a single hex color or a range in the ?,? format.",
        default="#282828",
    )
    text_g.add_argument(
        "-sw",
        "--space_width",
        type=float,
        nargs="?",
        help="Define the width of the spaces between words. 2.0 means twice the normal space width",
        default=1.0,
    )
    text_g.add_argument(
        "-cs",
        "--character_spacing",
        type=int,
        nargs="?",
        help="Define the width of the spaces between characters. 2 means two pixels",
        default=0,
    )
    text_g.add_argument(
        "-hw",
        "--handwritten",
        action="store_true",
        help='Define if the data will be "handwritten" by an RNN\
            Note: it will probably not work',
    )
    text_g.add_argument(
        "-ft",
        "--font",
        type=str,
        nargs="?",
        help="Define font to be used",
        default="NanumGothic.ttf"
    )
    text_g.add_argument(
        "-fd",
        "--font_dir",
        type=str,
        nargs="?",
        help="Define a font directory to be used",
    )
    text_g.add_argument(
        "-or",
        "--orientation",
        type=int,
        nargs="?",
        help="Define the orientation of the text. 0: Horizontal, 1: Vertical",
        default=0,
    )
    text_g.add_argument(
        "-ws",
        "--word_split",
        action="store_true",
        help="Split on words instead of on characters (preserves ligatures, no character spacing)",
        default=False,
    )
    text_g.add_argument(
        "-ca",
        "--case",
        type=str,
        nargs="?",
        help="Generate upper or lowercase only. arguments: upper or lower. Example: --case upper",
    )

    """
        # Image constructions (skewness, size, background, ...)
    """
    image_g = parser.add_argument_group("image", "Image construction details")
    image_g.add_argument(
        "-f",
        "--format",
        type=int,
        nargs="?",
        help="Define the height of the produced images if horizontal, else the width",
        default=32,
    )
    image_g.add_argument(
        "-wd",
        "--width",
        type=int,
        nargs="?",
        help="Define the width of the resulting image. If not set it will be the width of the text + 10. If the width of the generated text is bigger that number will be used",
        default=-1,
    )
    image_g.add_argument(
        "-k",
        "--skew_angle",
        type=int,
        nargs="?",
        help="Define skewing angle of the generated text. In positive degrees",
        default=0,
    )
    image_g.add_argument(
        "-rk",
        "--random_skew",
        action="store_true",
        help="When set, the skew angle will be randomized between the value set with -k and it's opposite",
        default=False,
    )
    image_g.add_argument(
        "-bl",
        "--blur",
        type=int,
        nargs="?",
        help="Apply gaussian blur to the resulting sample. Should be an integer defining the blur radius",
        default=0,
    )
    image_g.add_argument(
        "-rbl",
        "--random_blur",
        action="store_true",
        help="When set, the blur radius will be randomized between 0 and -bl.",
        default=False,
    )
    image_g.add_argument(
        "-b",
        "--background",
        type=int,
        nargs="?",
        help="Define what kind of background to use. 0: Gaussian Noise, 1: Plain white, 2: Quasicrystal, 3: Image",
        default=0,
    )
    image_g.add_argument(
        "-om",
        "--output_mask",
        type=int,
        help="Define if the generator will return masks for the text",
        default=0,
    )
    image_g.add_argument(
        "-d",
        "--distorsion",
        type=int,
        nargs="?",
        help="Define a distorsion applied to the resulting image. 0: None (Default), 1: Sine wave, 2: Cosine wave, 3: Random",
        default=0,
    )
    image_g.add_argument(
        "-do",
        "--distorsion_orientation",
        type=int,
        nargs="?",
        help="Define the distorsion's orientation. Only used if -d is specified. 0: Vertical (Up and down), 1: Horizontal (Left and Right), 2: Both",
        default=0,
    )
    image_g.add_argument(
        "-al",
        "--alignment",
        type=int,
        nargs="?",
        help="Define the alignment of the text in the image. Only used if the width parameter is set. 0: left, 1: center, 2: right",
        default=1,
    )
    image_g.add_argument(
        "-m",
        "--margins",
        type=margins,
        nargs="?",
        help="Define the margins around the text when rendered. In pixels",
        default=(5, 5, 5, 5),
    )
    image_g.add_argument(
        "-fi",
        "--fit",
        action="store_true",
        help="Apply a tight crop around the rendered text",
        default=False,
    )
    image_g.add_argument(
        "-id",
        "--image_dir",
        type=str,
        nargs="?",
        help="Define an image directory to use when background is set to image",
        default=os.path.join(os.path.split(os.path.realpath(__file__))[0], "images"),
    )

    """
        Others
    """
    others_g = parser.add_argument_group("others", "Other configurations")
    others_g.add_argument(
        "-t",
        "--thread_count",
        type=int,
        nargs="?",
        help="Define the number of thread to use for image generation",
        default=1,
    )

    return parser
