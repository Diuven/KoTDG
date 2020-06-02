# Building dataset for Text Recognition

from kotdg.generator import KoreanTextGenerator
from pathlib import Path
from glob import glob
import os
import sys

out_base = Path("out")
all_fonts = glob("resources/fonts/*")


def make_2350_clean():
    """
        Simple single character images
        size: 32x32 (RGB)
        characters: common hangul 2350 (완성형 2350자)
        No background, no color, no distortion, no orientation, no blur, etc
        label: value, index(%08d), font
    """
    print("Building 2350_clean dataset!")

    out_path = out_base / "2350_clean"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    idx = 0
    label_path = out_path / "labels.csv"

    with open(label_path, "x") as label_file:
        for (pos, font) in enumerate(all_fonts):
            gen = KoreanTextGenerator("file", fonts=[font], dict='single.txt', count=2350, width=32)
            for dat in gen:
                name = out_path / ('%08d.jpg' % idx)
                dat[0].save(name)
                idx += 1
                label = "%s, %07d, %s\n" % (dat[1], idx, Path(font).stem)
                label_file.write(label)
            print("Finished font: %s (%d/%d)" % (font, pos+1, len(all_fonts)))
            sys.stdout.flush()

    print("Total number of images: %08d" % idx)
    print("Done!")


def main():
    make_2350_clean()


if __name__ == "__main__":
    main()
