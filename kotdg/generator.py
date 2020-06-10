import os
from pathlib import Path

from trdg.generators import *
from trdg.string_generator \
    import create_strings_from_wikipedia, create_strings_from_dict

from .utils import ko_load_dict, ko_create_strings_randomly
import random

# basedir of kotdg. ( i.e. basedir = 'kotdg/' )
basedir = Path(os.path.realpath(__file__)).parent
resourcedir = (basedir / '../resources/').resolve()

default_args = {
    'count': -1,
    'length': 1,
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
    'image_dir': str(resourcedir / "images"),
    'shuffle': False
}

args_list = {
    'common': (
        'count',
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
        'length',
        'allow_variable',
        'use_letters',
        'use_numbers',
        'use_symbols',
    ),
    'string': ('strings',),
    'dict': ('length', 'allow_variable', 'dict',),
    'wiki': ('minimum_length',)
}

source_options = ("string", "random", "dict", "wiki", "file")


class KoreanTextGenerator:
    """ Wrapping class of trdg generators """

    def __init__(self, source="random", **kwargs):
        # Feed default arguments
        self.args = dict(kwargs)
        for key, val in default_args.items():
            if key not in self.args:
                self.args[key] = val
        source = source.lower().strip()
        self.source = source

        # Separate distinct arguments
        self.sargs = {}
        for key in self.args:
            if (key not in args_list['common']) and (key not in args_list['string']):
                self.sargs[key] = self.args[key]
        for key in self.sargs:
            del self.args[key]

        if source not in source_options:
            raise ValueError('Wrong source type! \nChoose among ("string", "random", "dict", "wiki").')

        if source == "dict" or source == "file":
            # Load dict to self.dict
            self.dict = ko_load_dict(self.sargs['dict'])

        self.args['strings'] = self.generate_strings()

        # Generate generator
        self.generator = GeneratorFromStrings(**self.args)

    def generate_strings(self):
        # Generate strings from respective source
        if self.source == 'string':
            res = self.args['strings']

        elif self.source == 'random':
            res = ko_create_strings_randomly(
                self.sargs['length'],
                self.sargs['allow_variable'],
                1000,
                self.sargs['use_letters'],
                self.sargs['use_numbers'],
                self.sargs['use_symbols'],
                self.args['language']
            )

        elif self.source == 'dict':
            res = create_strings_from_dict(
                self.sargs['length'], self.sargs['allow_variable'], 1000, self.dict
            )

        elif self.source == 'wiki':
            res = create_strings_from_wikipedia(
                self.sargs['minimum_length'], 1000, self.args['language']
            )

        elif self.source == 'file':
            # 1000??
            res = self.dict

        else:
            raise RuntimeError
            
        if self.sargs['shuffle']:
            random.shuffle(res)

        return res

    def next(self):
        if self.generator.generated_count % 1000 == 999:
            self.generator.strings = self.generate_strings()
        return self.generator.next()

    def __iter__(self):
        return self.generator

    def __next__(self):
        return self.next()
