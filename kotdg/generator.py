from pathlib import Path
from random import shuffle, random
from tqdm import tqdm
from glob import glob
import os

from trdg.data_generator import FakeTextDataGenerator

base_dir = Path(os.path.realpath(__file__)).parent
# directory for background images
images_dir = (base_dir / 'resources/images').resolve()


def get_image(text, font, height, width, background_type, color, blur):
    return FakeTextDataGenerator.generate(
        index=-1,
        text=text,
        font=font,
        out_dir=None,
        size=height,
        extension=None,
        skewing_angle=0,
        random_skew=False,
        blur=blur,
        random_blur=True,
        background_type=background_type,
        distorsion_type=0,
        distorsion_orientation=0,
        is_handwritten=False,
        name_format=0,
        width=width,
        alignment=1,
        text_color=color,
        orientation=0,
        space_width=1.0,
        character_spacing=0,
        margins=(5, 5, 5, 5),
        fit=False,
        output_mask=False,
        word_split=False,
        image_dir=images_dir,
    )


class KoreanTextGeneratorIterator:
    def __init__(self, count, size, strings, fonts, features=None):
        if 0 <= count:
            raise NotImplementedError("Count should be -1 for now")
        if size[0] < 0 or size[1] < 0:
            raise ValueError("Not a proper size: %s" % size)

        self.count = count
        self.made = 0
        self.size = tuple(size)

        self.color = "#282828"
        if 'color' in features:
            self.color = features['color']
        if 'get_color' in features:
            self.get_color = features['get_color']

        self.bg_num = len(glob(str(images_dir / '*')))
        self.get_background = lambda: min(3, int(random() * (2 + self.bg_num)))

        if 'blur' in features:
            self.blur = features['blur']
        else:
            self.blur = 0

        self.pairs = []
        for font in fonts:
            for string in strings:
                self.pairs.append((string, font))
        shuffle(self.pairs)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.pairs) <= self.made:
            raise StopIteration

        text, font = self.pairs[self.made]
        background = self.get_background()

        if self.get_color is not None:
            color = self.get_color()
        else:
            color = self.color

        img = get_image(text, font, self.size[0], self.size[1], background, color, self.blur)
        self.made += 1

        return img, {"font": Path(font).stem, "text": text}

    def __len__(self):
        return len(self.pairs)


class KoreanTextGenerator:
    def __init__(self, out_dir, threads, size, strings, fonts, features=None):
        self.gen = KoreanTextGeneratorIterator(-1, size, strings, fonts, features)
        self.out_dir = Path(out_dir)
        self.labels = [None] * len(self.gen)

        if threads != 1:
            raise NotImplementedError("Threads should be 1 for now")

    def save(self, index, img, meta):
        name = self.out_dir / ("%08d.jpg" % index)
        self.labels[index] = meta
        img.save(name)

    def generate(self):
        print("Generating!")
        self.out_dir.mkdir(parents=True, exist_ok=False)

        for index, (img, meta) in tqdm(enumerate(self.gen), total=len(self.gen)):
            self.save(index, img, meta)

        with open(self.out_dir / "labels.txt", "wt") as label_file:
            for idx in range(len(self.labels)):
                meta = self.labels[idx]
                label_file.write(meta["text"] + '\n')

        print("Done!")

        return self.labels

