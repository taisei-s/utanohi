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
                tokens.append([mecab_nodes.surface] + features)
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
        if m_token[1] == '記号' or m_token[1] == '補助記号' or m_token[0] == '　':
            mora = 0
        else:
            mora = len(re.sub(r'[ゃゅょ]+?', '', m_token[0]))
    elif m_token[1] == '記号' or m_token[1] == '補助記号' or m_token[0] == '　':
        mora = 0
    else:
        mora = len(re.sub(r'[ャュョ]+?', '', yomi))

    return mora

def createGraph(n_tokens, u_tokens):
    graph = {}
    n_i = 0
    u_i = 0
    n_point = 0
    u_point = 0
    n_end = False
    u_end = False
    while not (n_end and u_end):
        try:
            if n_point == u_point:
                if n_point in graph:
                    print('error occurd!')
                    break
                graph[n_point] = {'n':n_tokens[n_i], 'u':u_tokens[u_i]}
                n_point += len(n_tokens[n_i][0])
                u_point += len(u_tokens[u_i][0])
                n_i += 1
                u_i += 1
            elif n_point < u_point:
                if n_point in graph:
                    print('error occurd!')
                    break
                graph[n_point] = {'n':n_tokens[n_i], 'u':None}
                n_point += len(n_tokens[n_i][0])
                n_i += 1
            elif n_point > u_point:
                if u_point in graph:
                    print('error occurd!')
                    break
                graph[u_point] = {'n':None, 'u':u_tokens[u_i]}
                u_point += len(u_tokens[u_i][0])
                u_i += 1
        except IndexError:
            if n_i == len(n_tokens):
                n_i = n_i - 1
                n_end = True
            elif u_i == len(u_tokens):
                u_i = u_i - 1
                u_end = True

    if n_point in graph:
        print('error occurd!')

    graph[n_point] = {'n':None, 'u':None}

    return graph

def merge(n_tokens, u_tokens):
    token_graph = createGraph(n_tokens, u_tokens)
    merge_tokens = []
    priority = 0
    p = 0
    while not (token_graph[p]['n'] == None and token_graph[p]['u'] == None):
        if priority > 1:
            priority = 0
        node = token_graph[p]

        if node['u'] == None:
            merge_tokens.append(node['n'])
            p += len(node['n'][0])
            priority = 0
        elif node['n'] == None:
            merge_tokens.append(node['u'])
            p += len(node['u'][0])
            priority += 1
        else:
            if countMora(node['n']) > countMora(node['u']):
                merge_tokens.append(node['n'])
                p += len(node['n'][0])
                priority = 0
            elif countMora(node['n']) < countMora(node['u']):
                merge_tokens.append(node['u'])
                p += len(node['u'][0])
                priority += 1
            else:
                if len(node['n'][0]) > len(node['u'][0]):
                    merge_tokens.append(node['n'])
                    p += len(node['n'][0])
                    priority = 0
                elif len(node['n'][0]) < len(node['u'][0]):
                    merge_tokens.append(node['u'])
                    p += len(node['u'][0])
                    priority += 1
                else:
                    if priority == 0:
                        merge_tokens.append(node['n'])
                        p += len(node['n'][0])
                    else:
                        merge_tokens.append(node['u'])
                        p += len(node['u'][0])

    return merge_tokens

def parseFixed2(tanka):
    #m_neologd = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    #m_unidic = init_mecab('/usr/lib/x86_64-linux-gnu/mecab/dic/UniDic-qkana_1603')
    m_neologd = init_mecab('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    m_unidic = init_mecab('/usr/local/lib/mecab/dic/UniDic-qkana_1603')

    tanka = re.sub(r'\s+?', r'　', tanka.rstrip('\r\n'))
    neologd_tokens = tokenize_mecab(tanka, m_neologd)
    unidic_tokens = tokenize_mecab(tanka, m_unidic, dic='uniDic')

    merge_tokens = merge(neologd_tokens, unidic_tokens)

    fixeds = [5, 7, 5, 7, 7, 0, 0]
    parsed = ""
    mora = 0
    p = 0
    fixed = fixeds[p]
    for i in range(len(merge_tokens)+1):
        try:
            mora += countMora(merge_tokens[i])
            parsed += merge_tokens[i][0]

            if mora == fixed:
                if not(countMora(merge_tokens[i+1]) <= 1):
                    p += 1
                    mora = 0
                    parsed += '　'
                    fixed = fixeds[p]
            elif mora == fixed-1:
                if countMora(merge_tokens[i+1]) >= 3:
                    p += 1
                    mora = 0
                    parsed += '　'
                    fixed = fixeds[p]
            elif mora == fixed+1:
                p += 1
                mora = 0
                parsed += '　'
                fixed = fixeds[p]
            elif mora > fixed:
                p += 1
                fixed += fixeds[p]
        except IndexError:
            break

        try:
            NONE = fixeds[p+1]
        except IndexError:
            p = p - 1

    return parsed

def main():
    csv_manager = CsvManager()
    themes = csv_manager.load_file('../data/test.csv')
    i = 0
    for tankas in themes:
        if i > 10:
            break
        output = [[tankas.pop(0)]]
        for tanka in tankas:
            parsed = parseFixed2(tanka)
            output.append([tanka, parsed])
        csv_manager.add_file(output, '../data/parsedTanka.csv')
        i += 1

if __name__ == "__main__":
    main()