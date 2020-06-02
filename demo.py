# Demo of generating korean text images

import trdg.generators
from pathlib import Path
from glob import glob
import os
import random
from kotdg.generator import KoreanTextGenerator

demo_text = r"모든 사람은 자유로운 존재로 태어났고, 똑같은 존엄과 권리를 가진다. 사람은 이성과 양심을 타고 났으므로 서로를 형제애의 정신으로 대해야 한다." 

out_path = Path("out")
all_fonts = glob("resources/fonts/*")


def vanilla_demo():
    print("Testing the original trdg generators!")

    fonts = random.sample(all_fonts, 5)
    # fonts = glob("resources/fonts/NanumGothic.ttf")

    string_input = [[x] for x in demo_text.split(" ")]
    random.shuffle(string_input)

    print("Generating 5 samples with %s font!" % fonts)
    print("Demo text: %s" % demo_text)
    gen = trdg.generators.GeneratorFromStrings(
        strings=string_input,
        count=10,
        fonts=fonts
    )

    print("Successfully generated generator")

    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    for a in gen:
        print(a)
        a[0].save(out_path / (a[1][0] + '.jpg'))
        a[0].show()
    
    print("Done!")


def kotdg_gen():
    print("Testing kotdg generators!")

    fonts = random.sample(all_fonts, 5)

    string_input = [[x] for x in demo_text.split(" ")]
    random.shuffle(string_input)

    gen4 = KoreanTextGenerator("wiki", fonts=fonts, count=3)

    for d in gen4:
        print(d)
        d[0].show()

    gen3 = KoreanTextGenerator("dict", fonts=fonts, count=3, dict='ko.txt')

    for c in gen3:
        print(c)
        c[0].show()

    gen2 = KoreanTextGenerator("random", fonts=fonts, count=3, length=3)

    for b in gen2:
        print(b)
        b[0].show()

    gen1 = KoreanTextGenerator("string", strings=string_input, fonts=fonts, count=3)

    for a in gen1:
        print(a)
        a[0].save(out_path / (a[1][0] + '.jpg'))
        a[0].show()

    print("Done!")


if __name__ == "__main__":
    # vanilla_demo()
    kotdg_gen()
