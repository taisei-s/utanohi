# coding:utf-8

import re
import MeCab
from manager import CsvManager
import alkana

def init_mecab(dic_path=''):
    arg = ''
    if dic_path:
        arg = '-d ' + dic_path
    m = MeCab.Tagger(arg)
    m.parseToNode('')  # バグ対策で空打ちする
    return m

#文を単語にトークナイズし、単語の読みをカタカナで返す
def tokenize_mecab(text, m, num):
    text = text.lower()
    mecab_nodes = m.parseToNode(text)

    kana = []
    while mecab_nodes:
        if mecab_nodes.surface == '':
            mecab_nodes = mecab_nodes.next
            continue
        surface = mecab_nodes.surface
        yomi = mecab_nodes.feature.split(',')[num]  # surfaceで表層形、featureで形態素情報
        kana.append((surface, yomi))
        mecab_nodes = mecab_nodes.next  # nextを忘れない
    return kana

def countMora(word):
    pass

def parseFixed(tanka):
    pass

def main():
    m_neologd = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    m_unidic = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/UniDic-qkana_1603')
    text = 'めつきりとGigaの減つてる月末に飢餓をかんじてすこしひもじい'

    print(tokenize_mecab(text, m_neologd, -2))
    print(tokenize_mecab(text, m_unidic, 9))

if __name__ == "__main__":
    main()