# coding:utf-8

import CaboCha
from manager import CsvManager, TxtManager

cabocha = CaboCha.Parser('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
csv = CsvManager()
text = TxtManager()
lines = csv.load_file('../data/theme_tanka.csv')

data = []
for line in lines:
    for i, tanka in enumerate(line):
        if i == 0:
            data.extend([tanka + '\n'])
            continue
        data.extend([tanka + '\n'])
        data.extend([cabocha.parseToString(tanka)])
        tree = cabocha.parse(tanka)
        data.extend([tree.toString(CaboCha.FORMAT_LATTICE)])

text.make_file(data, '../data/parsedData.txt')