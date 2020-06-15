from kotdg.generator import KoreanTextGenerator
from kotdg.utils import *
from glob import glob
from random import getrandbits, random, sample


def get_color():
    if random() < 0.5:
        r, g, b = getrandbits(5), getrandbits(5), getrandbits(5)
    else:
        val = getrandbits(24)
        r, g, b = val // (2**16), (val // (2**8)) % (2**8), val % (2**8)
        if r+g+b > 128*3:
            r, g, b = 255 - r, 255 - g, 255 - b
    return "#%02X%02X%02X" % (r, g, b)


if __name__ == "__main__":
    strings = ko_load_dict('ksx1001.txt')
    fonts = glob("resources/fonts/*.[o,t]tf")
    fonts = sample(fonts, 50)
    gen = KoreanTextGenerator(
        'out/test', 100, (224, 224), strings, fonts,
        features={'get_color': get_color, 'blur': 2})
    labels = gen.generate()
