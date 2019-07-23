# coding:utf-8

import re
import MeCab
from manager import CsvManager,TxtManager
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
    #m_neologd = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    #m_unidic = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/UniDic-qkana_1603')
    m_neologd = init_mecab('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    m_unidic = init_mecab('/usr/local/lib/mecab/dic/UniDic-qkana_1603')
    neologd_tokens = tokenize_mecab(tanka, m_neologd)
    unidic_tokens = tokenize_mecab(tanka, m_unidic, dic='uniDic')

    fixeds = [5, 7, 5, 7, 7, 0, 0]
    parsed = ""
    i = 0
    n_num = 0
    u_num = 0
    mora = 0
    fixed = fixeds[0]
    while n_num+1 <= len(neologd_tokens) and u_num+1 <= len(unidic_tokens):

        n_token = neologd_tokens[n_num]
        u_token = unidic_tokens[u_num]

        #定型を利用してneologdかunidicかどっちの形態素がいいか判断し、追加する
        if countMora(n_token) == countMora(u_token):
            if len(n_token[0]) >= len(u_token[0]):
                parsed += n_token[0]
                mora += countMora(n_token)
            else:
                parsed += u_token[0]
                mora += countMora(u_token)
        elif countMora(n_token) > countMora(u_token):
            parsed += n_token[0]
            mora += countMora(n_token)
            u_len = len(u_token[0])
            while len(n_token[0]) > u_len:
                u_num += 1
                u_token = unidic_tokens[u_num]
                u_len += len(u_token[0])
        elif countMora(n_token) < countMora(u_token):
            parsed += u_token[0]
            mora += countMora(u_token)
            n_len = len(n_token[0])
            while len(u_token[0]) > n_len:
                n_num += 1
                n_token = neologd_tokens[n_num]
                n_len += len(n_token[0])

        #定型にはまっているなら全角の空白を入れて、はまっていないならいれない
        try:
            if mora == fixed:
                if not(countMora(neologd_tokens[n_num+1]) <= 1 and countMora(unidic_tokens[u_num+1]) <= 1):
                    i += 1
                    mora = 0
                    parsed += '　'
                    fixed = fixeds[i]
            elif mora == fixed-1:
                if countMora(neologd_tokens[n_num+1]) >= 3 or countMora(unidic_tokens[u_num+1]) >= 3:
                    i += 1
                    mora = 0
                    parsed += '　'
                    fixed = fixeds[i]
            elif mora == fixed+1:
                if not(countMora(neologd_tokens[n_num+1]) <= 1 and countMora(unidic_tokens[u_num+1]) <= 1):
                    i += 1
                    mora = 0
                    parsed += '　'
                    fixed = fixeds[i]
            elif mora > fixed:
                i += 1
                fixed += fixeds[i]
        except IndexError:
            print('kokoda!')
            break

        n_num += 1
        u_num += 1
        try:
            NONE = fixeds[i+1]
        except IndexError:
            i = i - 1

    return parsed

def main():
    txt_manager = TxtManager()
    tankas = txt_manager.load_file('../data/test.txt')

    for tanka in tankas:
        p = parseFixed(tanka)
        print(p)

if __name__ == "__main__":
    main()