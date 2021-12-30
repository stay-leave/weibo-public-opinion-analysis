from gensim import corpora, models
from gensim.models import Word2Vec
from gensim.similarities import Similarity
import logging
import cmath
from sklearn.decomposition import PCA
from matplotlib import pyplot
import numpy as np


def infile(fliepath):
    #输入主题词文件
    train = []
    fp = open(fliepath,'r',encoding='utf8')
    for line in fp:
        line = line.strip().split(' ')
        train.append(line)
    return train
sentences=infile('训练.txt')#文本

model=models.Word2Vec(sentences,min_count=0)
print(model)
model.save('w2v.model')

