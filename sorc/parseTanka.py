# coding:utf-8

import CaboCha
from manager import CsvManager, TxtManager

cabocha = CaboCha.Parser('')
csv = CsvManager()
text = TxtManager()
lines = csv.load_file('../data/data.csv')

data = []
for line in lines:
    for i, tanka in enumerate(line):
        if i == 0:
            theme = tanka + '\n'
            data.extend([theme])
            continue
        data.extend([tanka])
        data.extend([cabocha.parseToString(tanka)])
        tree = cabocha.parse(tanka)
        data.extend([tree.toString(CaboCha.FORMAT_LATTICE)])

text.make_file(data, '../data/parsedData.txt')