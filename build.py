# Building dataset for Text Recognition

from kotdg.generator import KoreanTextGenerator
from kotdg.utils import ko_decompose
from pathlib import Path
from glob import glob
import os
import sys

out_base = Path("out")
all_fonts = glob("resources/fonts/*")
size = 224 # Same with Resnet / VGG


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


def main():
    make_ksx_clean()
    print("Done!")


if __name__ == "__main__":
    main()
