# coding:utf-8

import MeCab
from collections import Counter
from manager import CsvManager, JsonManager

def init_mecab(dic_path=''):
    arg = ''
    if dic_path:
        arg = '-d ' + dic_path
    m = MeCab.Tagger(arg)
    m.parseToNode('')  # バグ対策で空打ちする
    return m

def tokenize_mecab(text, m):
    mecab_nodes = m.parseToNode(text)
    surfaces = []
    while mecab_nodes:
        if mecab_nodes.surface is not '':
            surfaces.append(mecab_nodes.surface)  # surfaceで表層形、featureで形態素情報
        mecab_nodes = mecab_nodes.next  # nextを忘れない
    return surfaces

def wordCount2json():
    m = init_mecab('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    csv_manager = CsvManager()
    data_list = csv_manager.load_file('../data/theme_tanka.csv')

    words = []
    for theme_tanka in data_list:
        tankas = theme_tanka[1:]
        for tanka in tankas:
            words += tokenize_mecab(tanka, m)

    word_dict = Counter(words)
    json_manager = JsonManager()
    json_manager.make_file(dict(word_dict), '../data/wordCont.json')

def analyseTanka():
    json_manager = JsonManager()
    word_count = json_manager.load_file('../data/wordCont.json')

    value_line = 10
    keys = []
    for key, value in word_count.items():
        if value_line > value:
            keys.append(key)

    print(len(word_count))
    print(len(keys))
    #print(keys)


if __name__ == "__main__":
    analyseTanka()