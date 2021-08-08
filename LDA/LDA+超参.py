#coding='utf-8'
import os
import heapq
from importlib import reload
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from gensim import corpora,similarities,models
from gensim.models import LdaModel
from gensim.corpora import Dictionary
#from ldamattle import LdaMallet#导入mallet
import pyLDAvis.gensim
import math
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
from LDA import infile,deal,run,save_visual

#超参搜索的形式探索最佳主题数,对于暴力搜索可以一开始设置区间较大，步伐较大，目的是锁定大致区间范围，而后在小区间范围内精细化搜索。
def compute_coherence_values(dictionary, corpus, texts,start, limit, step):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    perplexs=[]
    model_list = []
    for num_topic in range(start, limit, step):
        #模型
        lda_model,coherence_lda,perplex=run(corpus,dictionary,num_topic,texts)
        #lda_model = LdaModel(corpus=corpus,num_topics=num_topic,id2word=dictionary,passes=50)
        model_list.append(lda_model)
        perplexs.append(perplex)#困惑度
        #一致性
        #coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        #coherence_lda = coherence_model_lda.get_coherence()
        coherence_values.append(coherence_lda)

    return model_list, coherence_values,perplexs

def show_1(dictionary,corpus,texts,start,limit,step):
    #从 5 个主题到 30 个主题，步长为 5 逐次计算一致性，识别最佳主题数
    model_list, coherence_values,perplexs = compute_coherence_values(dictionary, corpus,texts, start, limit, step)
    #输出一致性结果
    n=0
    for m, cv in zip(perplexs, coherence_values):
        print("主题模型序号数",n,"主题数目",(n+4),"困惑度", round(m, 4), " 主题一致性", round(cv, 4))
        n=n+1
    #打印折线图
    x = list(range(start, limit, step))
    #困惑度
    plt.plot(x, perplexs)
    plt.xlabel("Num Topics")
    plt.ylabel("perplex  score")
    plt.legend(("perplexs"), loc='best')
    plt.show()
    #一致性
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
    
    return model_list

def choose(model_list,n):
    # 选择最佳主题并输出，一致性最高的
    optimal_model = model_list[n]
    model_topics = optimal_model.show_topics(formatted=False)
    #print(model_topics)
    return optimal_model

#反过来给每个博文打上主题标签
def format_topics_sentences(optimal_model, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()
    # Get main topic in each document
    for i, row in enumerate(optimal_model[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = optimal_model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)

    return sent_topics_df

def show_2(optimal_model, corpus, texts,name):
    #输出每个博文的主题标签，以便计算热度
    df_topic_sents_keywords = format_topics_sentences(optimal_model, corpus, texts)
    # 格式化
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    #打印
    df_dominant_topic.head(10)
    #保存
    df_dominant_topic.to_excel('推文话题标签\\'+name+'.xlsx')

    return df_topic_sents_keywords

def show_3(df_topic_sents_keywords,name):
    #展示各个主题的关键词列表以及每个主题的代表性新闻内容
    sent_topics_sorteddf_mallet = pd.DataFrame()
    sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')
    for i, grp in sent_topics_outdf_grpd:
        sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet, 
                                             grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], 
                                            axis=0)
    # Reset Index    
    sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)
    # Format
    sent_topics_sorteddf_mallet.columns = ['Topic_Num', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    # Show
    sent_topics_sorteddf_mallet.to_excel('主题关键词\\'+name+'.xlsx')

def show_4(df_topic_sents_keywords,name):
    #LDA 给出的标签下，各个主题的新闻数以及占比情况,利于计算热度
    # Number of Documents for Each Topic
    topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()
    # Percentage of Documents for Each Topic
    topic_contribution = round(topic_counts/topic_counts.sum(), 4)
    # Topic Number and Keywords
    topic_num_keywords = df_topic_sents_keywords[['Dominant_Topic', 'Topic_Keywords']].drop_duplicates().reset_index(drop=True)
    # Concatenate Column wise
    df_dominant_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1)
    # Change Column names
    df_dominant_topics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']
    df_dominant_topics.sort_values(by="Dominant_Topic", ascending=True, inplace=True)
    # Show
    print(df_dominant_topics)
    #保存
    df_dominant_topics.to_excel('主题新闻数\\'+name+'.xlsx')
    return df_dominant_topics

if __name__ == '__main__':
    filenames=os.listdir(r'F:\A数据比赛\正式流程及文件\2.数据处理\正文信息\正文分词分月_关键词')
    for i in filenames:
        print(i)
        train=infile(r'F:\A数据比赛\正式流程及文件\2.数据处理\正文信息\正文分词分月_关键词\\'+i)
        name=i.replace('.txt','')#后续结果文件名
        id2word,texts,corpus=deal(train)
        model_list=show_1(id2word,corpus,texts,4,16,1)#找出困惑度和主题一致性最佳的，最好是不超过20个主题数,10个为宜
        n=input('输入指定模型序号，以0为第一个: ')#还是需要手动，权衡比较
        optimal_model=choose(model_list,int(n))
        #主题列表
        topic_list = optimal_model.print_topics()
        #保存主题
        f=open('主题txt\\'+name+'.txt','w',encoding='utf-8')
        for t in topic_list:
            f.write(' '.join(str(s) for s in t) + '\n')
        f.close()
        df_topic_sents_keywords=show_2(optimal_model,corpus,texts,name)
        show_3(df_topic_sents_keywords,name)
        df_dominant_topics=show_4(df_topic_sents_keywords,name)
        save_visual(optimal_model,corpus,id2word,'主题可视化\\'+name)#可视化
    







