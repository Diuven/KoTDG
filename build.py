# Building dataset for Text Recognition

from kotdg.generator import KoreanTextGenerator
from kotdg.utils import ko_decompose
from pathlib import Path
from glob import glob
import os
import sys
import argparse
import random



all_fonts = glob("resources/fonts/*")
split_ratio = (7, 2, 1)


parser = argparse.ArgumentParser(description='Build preconfigured datasets')
parser.add_argument('dataset', type=str, choices=['ksx'], default='ksx')
parser.add_argument('--size', type=int, default=224, help='Size of generated images (square)')
parser.add_argument('--fonts', type=int, default=-1, help="Number of fonts to use. If less than one, it will use all available fonts")
# parser.add_argument('--color', action='store_true', help="Generate colorized texts")
parser.add_argument('--train-only', action='store_true', help="Generate training dataset only. It generates train/valid/tests dataset as a default")
# parser.add_argument('--backg', action='store_true', help="Generate images with various backgrounds")
parser.add_argument('--outdir', type=str, default='out', help="Root directory for saving generated files")
parser.add_argument('--name', type=str, help="Name of the dataset (folder named after this will be generated in outdir)")


def make_ksx_clean():
    """
        Simple single character images
        size: sizexsize (RGB)
        characters: common hangul 2350 (KSX 1001 완성형 2350자)
        No background, no color, no distortion, no orientation, no blur, etc
        label: decomposed value, original value, index(%08d), font
        small label: decomposed value
        ex:
            label: (ㅆ,ㅓ,ㄻ), 썲, 0036541, NanumGothic
            small: ㅆ,ㅓ,ㄻ
    """
    print("Building ksx_clean dataset!")

    out_path = out_base / "ksx_clean"
    out_path.mkdir(parents=True, exist_ok=False)

    idx = 0
    label_path = out_path / "labels.csv"
    small_path = out_path / "small_labels.csv"

    with open(label_path, "x") as label_file:
        with open(small_path, "x") as small_file:

            for (pos, font) in enumerate(all_fonts):
                gen = KoreanTextGenerator("file", fonts=[font], dict='ksx1001.txt', count=2350, width=size, size=size)

                for dat in gen:
                    name = out_path / ('%08d.jpg' % idx)
                    dat[0].save(name)
                    idx += 1

                    dec = ko_decompose(dat[1])
                    dec = ', '.join(dec)
                    label = "%s, (%s), %08d, %s\n" % (dat[1], dec, idx, Path(font).stem)

                    label_file.write(label)
                    small_file.write(dat[1] + '\n')

                print("Finished font: %s (%d/%d)" % (font, pos+1, len(all_fonts)))

    print("Total number of images: %08d" % idx)
    print("")


def generate(getgen, out_path, fonts):
    print("Generating to %s" % out_path)
    out_path.mkdir(parents=True, exist_ok=False)

    label_path = out_path / 'labels.csv'
    info_path = out_path / 'info.csv'
    idx = 0

    with open(label_path, "x") as label_file, open(info_path, "x") as info_file:
        for pos, font in enumerate(fonts):
            gen = getgen(font)
        
            for dat in gen:
                name = out_path / ('%08d.jpg' % idx)
                dat[0].save(name)
                idx += 1

                dec = ko_decompose(dat[1])
                dec = ', '.join(dec)
                info = "%s, (%s), %08d, %s\n" % (dat[1], dec, idx, Path(font).stem)

                info_file.write(info)
                label_file.write(dat[1] + '\n')

            print("Finished font: %s (%d/%d)" % (font, pos+1, len(fonts)))
    
    return idx




def main(args):
    print("Generating images!")

    dsname = args.name if args.name is not None else args.dataset

    out_path = Path(args.outdir) / dsname

    if args.fonts <= 0:
        args.fonts = len(all_fonts)
    fonts = random.sample(all_fonts, args.fonts)
    random.shuffle(fonts)

    if args.train_only:
        raise NotImplementedError("sorry hehe")
    
    # split along fonts

    getgen = lambda font: KoreanTextGenerator("file", fonts=[font], dict='ksx1001.txt', count=2350, width=args.size, size=args.size)


    train_len = args.fonts * split_ratio[0] // sum(split_ratio)
    valid_len = (args.fonts - train_len) * split_ratio[1] // sum(split_ratio[1:])
    tests_len = args.fonts - train_len - valid_len

    if train_len < 1 or valid_len < 1 or tests_len < 1:
        raise ValueError("Wrong split numbers: %d, %d, %d" % (train_len, valid_len, tests_len))

    train_fonts = random.sample(fonts, train_len)
    tests_fonts = list(fonts)
    for x in train_fonts: tests_fonts.remove(x)
    valid_fonts = random.sample(tests_fonts, valid_len)
    for y in valid_fonts: tests_fonts.remove(y)

    if len(train_fonts) < 1 or len(valid_fonts) < 1 or len(tests_fonts) < 1:
        raise RuntimeError("Somehow at least one of the fonts list is empty. %s %s %s" % (train_fonts, valid_fonts, tests_fonts))

    count = 0
    count += generate(getgen, out_path / 'train', train_fonts)
    count += generate(getgen, out_path / 'valid', valid_fonts)
    count += generate(getgen, out_path / 'tests', tests_fonts)

    print("Total number of images: %08d" % count)

    print("Done!")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
