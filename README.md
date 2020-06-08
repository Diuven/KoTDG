# Korean Text Data Generator (KoTDG)

Korean Text Data Generator for OCR tasks. Heavily depends on [TRDG](https://github.com/Belval/TextRecognitionDataGenerator) by [Belval](https://github.com/Belval).

## Initialize

You should install `trdg` and `Pillow` package with pip, if not installed yet. You might want to use venv or conda.  
```pip install trdg Pillow```

All resources including dictionaries, fonts, and background images are located in respective folders at `resources/`.  
You may add more resources in the corresponding folders.

## How to use

Run `python build.py` to build preconfigured datasets. You can refer to the `build.py` to write your own datasets.

### CLI

You can run `./run.py` to run kotdg. `./run.py --help` will show (shockingly long) list of options.

#### List of commonly used arguments

Behaviors of the options are generally same as the original [TRDG](https://github.com/Belval/TextRecognitionDataGenerator)

* `-c` or `--count` is the only required option. It specifies the number of the images to be generated.
* `-l` or `--language` specifies the languages to be used. You can refer to the [ISO standard](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
  * FYI: Korean is `ko`, and English is `en`.
* `-o` or `--output_dir <dir>` specifies the location where the generated images and labels will be saved.
  * Default to `out`
* Specifying text source
  * `--dict <name>` will load dictionary named `<name>` from `resources/dicts/`
    * If none of the source-specifying options are set, this option (with `<name>` as `words.txt`) is used by default.
    * Each line of the file is separated, and at most 200 characters (from the beginning) are used.
    * Lines are randomly picked.
    * e.g. `./run.py --dict anthem.txt -c 5`
  * `--input_file <path>` will load a file from the given path.
    * Note that `<path>` is not related to `resources/`, unlike other cases.
    * Lines are sequentially used.
    * e.g. `./run.py --input_file resources/dicts/ksx1001.txt -c 5`
  * `--random` will load randomly picked letters in the corresponding pool
    * 한글은 유니코드 0xAC00부터 0xD7A3 영역에서 임의 추출합니다. 이는 가능한 모든 조합형 글자의 영역입니다.
    * `--include_**` options will configure what letters can be included in the pool
    * `ko` and `cn` each have their own pool, and other latin languages will use ASCII pool
  * `--wikipedia` will load random words from random [Wikipedia](https://www.wikipedia.org/),page, corresponding to the given language code.
* Text options
  * `--font <name>` specifies which font to be used
    * Font will be loaded from `resources/fonts`
    * The default value (even if this options is not set) is `'NanumGothic.ttf'`.
    * Note: all fonts should be `.ttf` or `.otf` format.
      * TRDG uses `PIL.Imagefont.truetype` function. Check corresponding documents for compatibility.
    * e.g. `./run.py -c 5 --font "Maplestory Bold.ttf"`
  * `--font_dir <dir>` specifies the directory where fonts are located
    * All fonts in the directory will be tried to be used.
    * Note that, of course, the total number of generated images is equal to the number passed to the `--count`.
    * e.g. `./run.py -c 5 --font_dir resources/fonts`
* Image options
  * `--format` specifies the 'height' of each image
    * If the text orientation is vertical, this specifies the width.
    * Default to 32.
  * `--width` specifies the width of each image.
    * If not set, the width will be 10 + `<width of text>`
    * Not yet tested with vertical texts
  * `-b <mode>` or `--background <mode>` specify which backgrounds will be used.
    * options for `<mode>`: 0 (gaussian noise), 1 (plain white), 2 (quasi-crystal), 3 (custom image)
    * Note that `<mode>=3` needs `--image_dir` to locate the custom background images
  * `--image_dir` specifies the location of background images.
    * Only used when `--background 3`.
    * Ideally, this should be `resources/images`. Planning to make that as a default.
    * e.g. `./run.py --background 3 --image_dir resources/images -c 5`
  * `--text_color "color_code"` specifies the color of the text.
    * Color code should be in hex type (e.g. `#00FFFF`), and it must be enclosed by double quotes. ("")
    * e.g. `./run.py -c 5 --text_color "#00FFFF"`
* Output options
  * `--name_format` specifies the format of the generated file names.
    * `<text>`: text written on the image, `<idx>`: integer index of the image, `<ext>`: extension of the image
    * 0: `<text>_<idx>.<ext>`
    * 1: `<idx>_<text>.<ext>`
    * 2: `<idx>.<ext>`, and `labels.txt` containing `<idx>`-`<text>` mapping 

### `kotdg` module

Import `KoreanTextGenerator` with `from kotdg.generator import KoreanTextGenerator`.

Refer to `demo.py` for general usage.

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

## Acknowledgment

Based on [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator)

Some files are from:  
[딥러닝을 활용한 한글문서 OCR 연구](https://github.com/parksunwoo/ocr_kor),  
[Jeongeun So](https://github.com/sojjeong)

Note that I do not have rights of most resources in this repository.
