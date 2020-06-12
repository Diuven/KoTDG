from pathlib import Path
# loading files

from trdg.data_generator import FakeTextDataGenerator
from trdg.computer_text_generator import _generate_horizontal_text as synthetic_generate


class KoreanTextGenerator:
    def __init__(self, count, out_dir, size, threads,  strings, fonts, features=None):
        """
        인자:
            전체 pool을 주는 인자들. e.g. fonts, strings ... 길이, ...?
            그 pool의 각 원소에 대해 랜덤하게 얹을 특성들. e.g. color, background, distortion ... (or

            모든 원소들이 가져야 하는 특성들. e.g. 사이즈, 위치,
            스레드 개수

            복원 추출 / 비복원 추출.
            개수
            count (새로운 generator를 주는 식으로 할까? 아니면 그냥 field를 바꾸는 식으로 할까?

            반환값
                이미지, metadata (font, value, index?)
        """
        """
            KoreanTextGenerator class only takes care of 'generating' according to the given parameters.
            Note that the caller should take care of the split, strings (and its shuffling), or possible random features
            
        Returns:
            an iterator yielding (image, meta={'font': str, 'value': str, 'decomposed': str})
            iterates in order. i.e. for font in fonts: for string in strings: yield (data)

        Parameters:
            count: number of images to generate. if -1 makes full set of images (all possible (string, font) pairs)
            out_dir: directory to place generated images & labels
            size: a tuple representing size of the images. (H, W). In case of W = -1, it should be automatically set... but not now
            threads: number of threads to use when generating images

            strings: an iterable for strings.

            As you might know, strings can be a generator, instead of an explicit list of strings

        """
        if 0 <= count:
            raise NotImplementedError("Count should be -1 for now")
        if size[0] < 0 or size[1] < 0:
            raise ValueError("Not a proper size: %s" % size )
        if threads != 1:
            raise NotImplementedError("Threads should be 1 for now")

        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=False)

        color = "#282828"

        for font in fonts:
            for string in strings:
                # We're not using save for FTDG here, so there's some placeholder parameters
                # img = synthetic_generate(string, font, color)
                
        pass

    def __iter__(self):
        return self

    def __next__(self):
        pass