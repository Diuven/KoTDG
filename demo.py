# Demo of generating korean text images

import trdg.generators
from pathlib import Path
from glob import glob
import random

if __name__ == "__main__":
    outpath = Path("out")
    # fonts = glob("resources/fonts/*")
    # sampled_fonts = random.sample(fonts, 5)
    font = glob("resources/fonts/NanumGothic.ttf")

    demo_text = r"모든 사람은 자유로운 존재로 태어났고, 똑같은 존엄과 권리를 가진다. 사람은 이성과 양심을 타고 났으므로 서로를 형제애의 정신으로 대해야 한다." 
    string_input = [[x] for x in demo_text.split(" ")]

    print("Generating 5 samples with %s font!" % font)
    print("Demo text: %s" % demo_text)
    gen = trdg.generators.GeneratorFromStrings(
        strings = string_input,
        count = 5,
        fonts = font,
        language="ko",
        image_dir=outpath,
    )

    print("Successfully generated generator")

    for a in gen:
        print(a)
        # print(outpath / a[1][0] / 'jpg')
        # Assuming the string is singleton
        # a[0].save(outpath / raw(a[1][0]) / 'jpg')
        a[0].show()
    
    print("Done!")
    exit(0)