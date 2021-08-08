#coding='utf-8'
import os
from importlib import reload
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from gensim import corpora,similarities,models
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from ldamattle import LdaMallet#导入mallet
import pyLDAvis.gensim
import math
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel

def infile(fliepath):
    #输入分词好的TXT，返回train
    '''
    all=[]
    with open(fliepath,'r',encoding='utf-8')as f:
        all_1=list(f.readlines())#列表
        for i in all_1:#一句
            i=i.strip()#去除占位符
            if i:
                all=all+i.split(' ')

    #字典统计词频
    dic={}
    for key in all:
        dic[key]=dic.get(key,0)+1
    #print(dic)
    #清除词频低的词
    all_2=[]#低词频列表
    for key,value in dic.items():
        if value<=5:
            all_2.append(key)
    '''
    train = []
    fp = open(fliepath,'r',encoding='utf8')
    for line in fp:
        new_line=[]
        if len(line)>1:
            line = line.strip().split(' ')
            for w in line:
                w.encode(encoding='utf-8')
                new_line.append(w)
        if len(new_line)>1:
            train.append(new_line)
    return train

def deal(train):
    #输入train，输出词典,texts和向量
    id2word = corpora.Dictionary(train)     # Create Dictionary
    texts = train                           # Create Corpus
    corpus = [id2word.doc2bow(text) for text in texts]   # Term Document Frequency

    #使用tfidf
    tfidf = models.TfidfModel(corpus)
    corpus = tfidf[corpus]

    id2word.save('tmp/deerwester.dict') #保存词典
    corpora.MmCorpus.serialize('tmp/deerwester.mm', corpus)#保存corpus

    return id2word,texts,corpus

'''
# Build LDA model
lda_model = LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=10, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
# Print the Keyword in the 10 topics
print(lda_model.print_topics())
doc_lda = lda_model[corpus]
'''

def run(corpus_1,id2word_1,num,texts):
    #标准LDA算法
    lda_model = LdaModel(corpus=corpus_1, 
                         id2word=id2word_1,
                        num_topics=num,
                       passes=60,
                       alpha=(50/num),
                       eta=0.01,
                       random_state=42)
    # num_topics：主题数目
    # passes：训练伦次
    # num：每个主题下输出的term的数目
    #输出主题
    #topic_list = lda_model.print_topics()
    #for topic in topic_list:
        #print(topic)
    # 困惑度
    perplex=lda_model.log_perplexity(corpus_1)  # a measure of how good the model is. lower the better.
    # 一致性
    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=id2word_1, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    #print('\n一致性指数: ', coherence_lda)   # 越高越好
    return lda_model,coherence_lda,perplex

def save_visual(lda,corpus,id2word,name):
    #保存为HTML
    d=pyLDAvis.gensim.prepare(lda, corpus, id2word)
    pyLDAvis.save_html(d, name+'.html')#可视化

def mallet(corpus_1,id2word_1,num,texts_1):
    #Mallet 版本的 LDA 算法
    os.environ.update({'MALLET_HOME':r'E:/mallet/mallet-2.0.8/'})
    mallet_path = 'E:\\mallet\\mallet-2.0.8\\bin\\mallet.bat' #路径
    ldamallet = LdaMallet(mallet_path, corpus=corpus_1, num_topics=num, id2word=id2word_1)
    # Show Topics
    #print(ldamallet.show_topics(formatted=False))

    # Compute Coherence Score
    coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=texts_1, dictionary=id2word_1, coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    #print('\nCoherence Score: ', coherence_ldamallet)
    return ldamallet,coherence_ldamallet


if __name__ == '__main__':
    train=infile('12月.txt')
    id2word,texts,corpus=deal(train)
    lda=run(corpus,id2word,6,texts)
    topic_list = lda.print_topics()
    f=open('12月.txt','w',encoding='utf-8')
    for t in topic_list:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()
    save_visual(lda,corpus,id2word,'12月')