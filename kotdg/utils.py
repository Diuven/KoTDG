# From trdg/string_generator.py and trdg/utils.py

import random as rnd
import os
import string
from pathlib import Path

# basedir of kotdg. ( i.e. basedir = 'kotdg/' )
basedir = Path(os.path.realpath(__file__)).parent
resourcedir = (basedir / '../resources/').resolve()


def ko_decompose(character):
    assert type(character) is str and len(character) == 1
    # assert ord(u'가') <= chr(character) and chr(character) <= ord(u'힣')

    fir = [x for x in "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"]
    snd = [x for x in "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"]
    thr = [chr(0x3130)] + [x for x in "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"]
    
    val = ord(character) - ord(u'가')

    res = []
    l1, l2, l3 = len(fir), len(snd), len(thr)

    res.append(thr[val%l3]); val = val // l3
    res.append(snd[val%l2]); val = val // l2
    res.append(fir[val])

    res.reverse()

    return res


def ko_load_dict(dict_path):
    """ Read the dictionary file and returns all words in it. """
    lang_dict = []
    with open(
       resourcedir/ 'dicts' / dict_path,
        "r",
        encoding="utf8",
        errors="ignore",
    ) as d:
        lang_dict = [token for token in d.read().splitlines() if len(token) > 0]
    return lang_dict


def ko_create_strings_from_dict(length, allow_variable, lang_dict):
    """
        Create all strings from the dictionary sequentially
    """

    dict_len = len(lang_dict)
    strings = []
    for idx in range(0, dict_len):
        current_string = lang_dict[idx]
        strings.append(current_string)
    return strings


def ko_create_strings_randomly(length, allow_variable, count, let, num, sym, lang):
    """
        Create all strings by randomly sampling from a pool of characters.
    """

    # If none specified, use all three
    if True not in (let, num, sym):
        let, num, sym = True, True, True

    pool = ""
    if let:
        if lang == "ko":
            pool += "".join(
                [chr(i) for i in range(0xAC00, 0xD7A4)]
            )  # Unicode range of KOR characters
        elif lang == "cn":
            pool += "".join(
                [chr(i) for i in range(19968, 40908)]
            )  # Unicode range of CHK characters
        else:
            pool += string.ascii_letters
    if num:
        pool += "0123456789"
    if sym:
        pool += "!\"#$%&'()*+,-./:;?@[\\]^_`{|}~"

    if lang == "cn":
        min_seq_len = 1
        max_seq_len = 2
    else:
        min_seq_len = 2
        max_seq_len = 10

    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length) if allow_variable else length):
            seq_len = rnd.randint(min_seq_len, max_seq_len)
            current_string += "".join([rnd.choice(pool) for _ in range(seq_len)])
            current_string += " "
        strings.append(current_string[:-1])
    return strings
