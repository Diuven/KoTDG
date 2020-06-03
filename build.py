# Building dataset for Text Recognition

from kotdg.generator import KoreanTextGenerator
from kotdg.utils import ko_decompose
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
        label: decomposed value, original value, index(%08d), font
        small label: decomposed value
        ex:
            label: (ㅆ,ㅓ,ㄻ), 썲, 0036541, NanumGothic
            small: ㅆ,ㅓ,ㄻ
    """
    print("Building 2350_clean dataset!")

    out_path = out_base / "2350_clean"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    idx = 0
    label_path = out_path / "labels.csv"
    small_path = out_path / "small_labels.csv"

    with open(label_path, "x") as label_file:
        with open(small_path, "x") as small_file:

            for (pos, font) in enumerate(all_fonts):
                gen = KoreanTextGenerator("file", fonts=[font], dict='single.txt', count=2350, width=32)

                for dat in gen:
                    name = out_path / ('%08d.jpg' % idx)
                    dat[0].save(name)
                    idx += 1

                    ans = ko_decompose(dat[1])
                    ans = ', '.join(ans)
                    label = "(%s), %s, %08d, %s\n" % (ans, dat[1], idx, Path(font).stem)

                    label_file.write(label)
                    small_file.write(ans + '\n')

                print("Finished font: %s (%d/%d)" % (font, pos+1, len(all_fonts)))

    print("Total number of images: %08d" % idx)
    print("")


def main():
    make_2350_clean()
    print("Done!")


if __name__ == "__main__":
    main()
