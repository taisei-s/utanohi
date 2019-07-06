# coding:utf-8

import re
import MeCab
from manager import CsvManager

def init_mecab(dic_path=''):
    arg = ''
    if dic_path:
        arg = '-d ' + dic_path
    m = MeCab.Tagger(arg)
    m.parseToNode('')  # バグ対策で空打ちする
    return m

#文を単語にトークナイズし、単語の読みをカタカナで返す
def tokenize_mecab(text, m):
    mecab_nodes = m.parseToNode(text)
    kana = []
    while mecab_nodes:
        if mecab_nodes.surface is not '':
            if re.fullmatch(r'[a-zA-Z]+', mecab_nodes.surface):
                kana.append(mecab_nodes.surface)
            else:
                kana.append(mecab_nodes.feature.split(',')[-2])  # surfaceで表層形、featureで形態素情報
        mecab_nodes = mecab_nodes.next  # nextを忘れない
    return kana

def countMora(word):
    pass

def parseFixed(tanka):
    m = init_mecab('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tanka = tokenize_mecab(tanka, m)

    return tanka


def main():
    csv_manager = CsvManager()
    lines = csv_manager.load_file('../data/test.txt')
    fixed_tankas = []
    for line in lines:
        fixed_tankas.append(line.pop(0))
        for tanka in line:
            fixed_tankas.append(parseFixed(tanka))

    for tanka in fixed_tankas:
        print(tanka)

if __name__ == "__main__":
    #main()
    m = init_mecab('/usr/local/lib/mecab/dic/mecab-ipadic-neologd`')
    text = 'めつきりとGigaの減つてる月末に飢餓をかんじてすこしひもじい'
    mecab_nodes = m.parseToNode(text)
    while mecab_nodes:
        print(mecab_nodes.feature.split(',')[-2])
        mecab_nodes = mecab_nodes.next
