# Demo of generating korean text images

import trdg.generators
from pathlib import Path
from glob import glob
import os
import random
from kotdg.generator import KoreanTextGenerator

demo_text = r"모든 사람은 자유로운 존재로 태어났고, 똑같은 존엄과 권리를 가진다. 사람은 이성과 양심을 타고 났으므로 서로를 형제애의 정신으로 대해야 한다." 

outpath = Path("out")
all_fonts = glob("resources/fonts/*")

def vanila_demo():
    print("Testing the original trdg generators!")

    fonts = random.sample(all_fonts, 5)
    # fonts = glob("resources/fonts/NanumGothic.ttf")

    string_input = [[x] for x in demo_text.split(" ")]
    random.shuffle((string_input))

    print("Generating 5 samples with %s font!" % fonts)
    print("Demo text: %s" % demo_text)
    gen = trdg.generators.GeneratorFromStrings(
        strings = string_input,
        count = 10,
        fonts = fonts
    )

    print("Successfully generated generator")

    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    for a in gen:
        print(a)
        a[0].save(outpath / (a[1][0] + '.jpg'))
        a[0].show()
    
    print("Done!")


def kotdg_gen():
    print("Testing kotdg generators!")

    fonts = random.sample(all_fonts, 5)

    string_input = [[x] for x in demo_text.split(" ")]
    random.shuffle((string_input))

    gen = KoreanTextGenerator("string", strings = string_input, fonts = fonts, count = 5)

    for a in gen:
        print(a)
        a[0].save(outpath / (a[1][0] + '.jpg'))
        a[0].show()
    
    print("Done!")

if __name__ == "__main__":
    # vanila_demo()
    kotdg_gen()