# coding:utf-8

import sentencepiece as spm

#spm.SentencePieceTrainer.Train("--input=../data/tankaText.txt --model_prefix=../data/model/tanka_sp_model_4 vocab_size=4000")

sp = spm.SentencePieceProcessor()

sp.load("../data/model/tanka_sp_model_4.model")

print(sp.EncodeAsPieces("夏が過ぎ秋を迎えて冬は来る      春を呼び込むためのお誘い"))