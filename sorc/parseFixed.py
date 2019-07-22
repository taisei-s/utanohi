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

#文を単語にトークナイズして返す
def tokenize_mecab(text, m, dic='ipadic'):
    text = text.lower()
    mecab_nodes = m.parseToNode(text)

    tokens = []
    if dic == 'ipadic':
        while mecab_nodes:
            if mecab_nodes.surface == '':
                mecab_nodes = mecab_nodes.next
                continue
            tokens.append([mecab_nodes.surface] + mecab_nodes.feature.split(','))  # surfaceで表層形、featureで形態素情報
            mecab_nodes = mecab_nodes.next  # nextを忘れない
    elif dic == 'uniDic':
        while mecab_nodes:
            if mecab_nodes.surface == '':
                mecab_nodes = mecab_nodes.next
                continue
            features = mecab_nodes.feature.split(',')
            try:
                tokens.append([mecab_nodes.surface] + features[0:6] + [features[7]] + [features[10]] + [features[9]])
            except IndexError:
                tokens.append(features)
            mecab_nodes = mecab_nodes.next  # nextを忘れない

    return tokens

def countMora(m_token):
    mora = 0
    yomi = ''
    if m_token[-1] == '*':
        if alkana.get_kana(m_token[0]):
            yomi = alkana.get_kana(m_token[0])
    else:
        yomi = m_token[-1]

    if yomi == '':
        if m_token[1] == '記号' or m_token[1] == '補助記号':
            mora = 0
        else:
            mora = len(re.sub(r'[ゃゅょ]+?', '', m_token[0]))
    elif m_token[1] == '記号' or m_token[1] == '補助記号':
        mora = 0
    else:
        mora = len(re.sub(r'[ャュョ]+?', '', yomi))

    return mora

def parseFixed(tanka):
    fixed = [5, 13, 19, 27, 35, '<eos>']
    parsed = ""
    m_neologd = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    m_unidic = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/UniDic-qkana_1603')
    neologd_tokens = tokenize_mecab(text, m_neologd)
    unidic_tokens = tokenize_mecab(text, m_unidic, dic='uniDic')

    i = 0
    while fixed[i] != '<eos>':
        
        if len(parsed) >= fixed[i]:
            i += 1

def main():
    #text = 'めつきりとGigaの減つてる月末に飢餓をかんじてすこしひもじい'
    text = '僕の無能な妄想日記。 8月13日晴れ。 あなたの目になって僕を見つめるあなたを創った。 こころはからだに置いていったので、僕はちゃんと確かめました。 こころはそこにないってことを。(三重苦歌)'

    for token in neologd_tokens:
        print(countMora(token), token)
    print()
    for token in unidic_tokens:
        print(countMora(token), token)


if __name__ == "__main__":
    main()