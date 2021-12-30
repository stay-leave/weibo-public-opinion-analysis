#coding='utf-8'
from gensim import corpora, models
from gensim.models import Word2Vec
import math
from sklearn.decomposition import PCA
import json



def work(list_1,list_2):
    #计算两个词集向量的余弦相似度
    #x值
    xs=[]
    #y值
    ys=[]
    for i in list_1:
        xs.append(i[0])
        ys.append(i[1])
    for i in list_2:
        xs.append(i[0])
        ys.append(i[1])
    #分子a,分母b,c
    a=0
    b=0
    c=0
    for x,y in zip(xs,ys):
        a=a+x*y
        b=b+x*x
        c=c+y*y
    #求值
    h=a/(math.sqrt(b)*math.sqrt(c))
    return h.real

def infile(fliepath):
    #输入主题词文件
    train = []
    fp = open(fliepath,'r',encoding='utf8')
    for line in fp:
        line = line.strip().split(' ')
        train.append(line)
    return train
sentences=infile('all.txt')#读取主题特征词

model=Word2Vec.load('w2v.model')#加载训练好的模型
# 基于2d PCA拟合数据
X = model.wv.vectors
pca = PCA(n_components=2)
result = pca.fit_transform(X)
words = list(model.wv.key_to_index)

'''
for i, word in enumerate(words):
    if word=='肺炎':
        print(word,result[i, 0], result[i, 1])#词和词向量



for sentence in sentences:#每一个主题
    print(sentence)
    for sen in sentence:#每一个词
        print(sen)
'''          


list_1=[]#二维向量词袋形式
for sentence in sentences:#每一个主题
    list_2=[]
    for sen in sentence:#每一个词
        for i, word in enumerate(words):
            if word==sen:
                #print(word,result[i, 0], result[i, 1])#词和词向量
                list_2.append((result[i, 0], result[i, 1]))
    list_1.append(list_2)

#print(len(list_1))
corpus=list_1
n_12=list(range(0,8))#12月的主题数
n_1=list(range(8,14))#1月的主题数
n_2=list(range(14,20))#2月的主题数
n_3=list(range(20,27))#3月的主题数
n_4=list(range(27,34))#4月的主题数
n_5=list(range(34,41))#5月的主题数
n_6=list(range(41,50))#6月的主题数
#计算相邻时间片主题的余弦相似度
hs={}
for i in n_12:#12月的主题
    for j in n_1:#1月的主题
        hs['12月的主题'+str(i)+str(sentences[i])+'与'+'1月的主题'+str(j-8)+str(sentences[j])+'的余弦相似度为']=work(corpus[i],corpus[j])
#print(hs)
for key,value in hs.items():#
    print(key,'\t',value,'\n')


with open('12-1.json', 'w') as f:
    f.write(json.dumps(hs, ensure_ascii=False, indent=4, separators=(',', ':')))
print('保存成功')






            