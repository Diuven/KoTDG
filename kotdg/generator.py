from trdg.generators import *
import os
from pathlib import Path

# basedir of kotdg. ( i.e. basedir = 'kotdg/' )
basedir = Path(os.path.realpath(__file__)).parent
resourcedir = (basedir / '../resources/').resolve()

default_args = {
    'count': -1,
    'minimum_length': 1,
    'allow_variable': False,
    'use_letters': True,
    'use_numbers': True,
    'use_symbols': True,
    # Nanum Gothic as a default font
    'fonts': [ str(resourcedir / 'fonts/NanumGothic.ttf') ],
    'language': "ko",
    'size': 32,
    'skewing_angle': 0,
    'random_skew': False,
    'blur': 0,
    'random_blur': False,
    'background_type': 0,
    'distorsion_type': 0,
    'distorsion_orientation': 0,
    'is_handwritten': False,
    'width': -1,
    'alignment': 1,
    'text_color': "#282828",
    'orientation': 0,
    'space_width': 1.0,
    'character_spacing': 0,
    'margins': (5, 5, 5, 5),
    'fit': False,
    'output_mask': False,
    'word_split': False,
    'image_dir': str(basedir / "../images"),
}

args_list = {
    'common': (
        'count',
        'length',
        'fonts',
        'language',
        'size',
        'skewing_angle',
        'random_skew',
        'blur',
        'random_blur',
        'background_type',
        'distorsion_type',
        'distorsion_orientation',
        'is_handwritten',
        'width',
        'alignment',
        'text_color',
        'orientation',
        'space_width',
        'character_spacing',
        'margins',
        'fit',
        'output_mask',
        'word_split',
        'image_dir',
    ),
    'random': (
        'allow_variable',
        'use_letters',
        'use_numbers',
        'use_symbols',
    ),
    'string': ('strings',),
    'dict': ('allow_variable', 'dict',),
    'wiki': ('minimum_length',)
}

# TODO How to single character?
# TODO check if all works fine esp. dict

class KoreanTextGenerator():
    """ Wrapping class of trdg generators """

    def __init__(self, source = "random", **kargs):
        for key, val in default_args.items():
            if key not in kargs:
                kargs[key] = val
        self.args = dict(kargs)
        source = source.lower().strip()
        self.source = source

        toremove = []
        for key in self.args:
            if (key not in args_list['common']) and (key not in args_list[source]):
                toremove.append(key)
        for key in toremove:
            del self.args[key]

        if source == "random":
            self.generator = GeneratorFromRandom(**self.args)
        elif source == "string":
            self.generator = GeneratorFromStrings(**self.args)
        elif source == "dict":
            self.generator = GeneratorFromDict(**self.args)
        elif source == "wiki":
            self.generator = GeneratorFromWikipedia(**self.args)
        else:
            raise ValueError('Wrong source type! \nChoose among ("random", "string", "dict", "wiki").')
    
        pass

    def __iter__(self):
        return self.generator

    def __next__(self):
        return self.generator.next()
