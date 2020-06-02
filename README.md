# Korean Text Data Generator

Korean Text Data Generator for OCR tasks. Heavily depends on [TRDG](https://github.com/Belval/TextRecognitionDataGenerator) by [Belval](https://github.com/Belval).

## Initialize

You should install `trdg` and `Pillow` package with pip, if not installed yet. You might want to use venv or conda.  
```pip install trdg Pillow```

## How to use

Refer to `demo.py` for general usage.

Run `python run.py` to build datasets.

## Structures

* `resources/`
  * fonts, dictionaries, and background images.
    * font file should be `.ttf` file
* `kotdg/`
  * core files.
  * `KoreanTextGeneator` in `generator.py` wraps TRDG generators
    * use with same parameters as TRDG generators, but with extra meta-parameter `source` 
    * `source` should have a value among `source_options = ("string", "random", "dict", "wiki", "file")`
* `demo.py`
  * testing scripts for development
  * refer to this when you want to call `kotdg` with code
* `out/`
  * default image saving directory
  * ignored by git by default
