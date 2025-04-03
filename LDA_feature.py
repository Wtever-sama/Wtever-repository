import os
from tqdm import tqdm
import pandas as pd
import jieba
indir_path = '/Users/wtsama/Documents/code/code2/python_assignment/week4/file_group/'

stop_words = set([
    "算是","吧","在","的","不是","和","也","什么","了","人","把","就","来","不","这次","一个","没","我"
    ,"在","过","嘛","还","九","开","而","去","也","但是","都","宝宝","们","啊","但","哈","只","然后","呀"
#    ,"因为","先","要","到","哈哈","同时","为了","个人感觉","上去","一边","例如"
#                                                ,"一粒","次次","带我去"
#                                                "哪里","其次","无法","有待","肯定","不会"
])
'''# 处理file_group中的所有文本文件，对于每个文件，将所有行中按照空格分割的词用停用词表过滤后整理成一个向量化的词频矩阵或者TF-IDF权重矩阵形式
def filter_file(dir_path):
    
    
    save_path = '/Users/wtsama/Documents/code/code2/python_assignment/week4/csv_filtered_group/'
    os.makedirs(save_path, exist_ok=True)
    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)
        try:
            with open(file_path, 'r', encoding='gbk') as file:  # 尝试 gbk 编码
                lines = file.readlines()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:  # 或忽略错误
                lines = file.readlines()
        
        # 初始化一个列表存储所有行的过滤后的词的列表
        doc_list =[]
        for line in lines:
            # 将每行（即每一年的所有评论词）转化为列表
            words_list = line.split()
            words_list = [word for word in words_list if word not in stop_words]
            words = ' '.join(words_list)
            doc_list.append(words)
        # 将doc_list转化为一个dataframe格式
        df = pd.DataFrame(doc_list)
        # print(df.dtypes)
        # 将其转化为一个csv文件保存到指定路径,要求名字包含原文件名
        df.to_csv(f'save_path f.csv',index =False, header = ['cus_comment'])
        
        print(f'file_name has been processed')

filter_file(indir_path)
'''
# jieba 分词
def chinese_word_cut(text):
    if not isinstance(text, str):
        return ""
    return " ".join(word for word in jieba.cut(text) if word not in stop_words)

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import numpy as np

# 打印高频词
def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword

csv_dir='/Users/wtsama/Documents/code/code2/python_assignment/week4/csv_filtered_group/'
for f in tqdm(os.listdir(csv_dir),desc="processing file"):
    
    # 文件名为去除后缀的f
    file_name = os.path.splitext(f)[0]
    print("Process "+file_name+':')
    file_path = os.path.join(csv_dir,f)
    data = pd.read_csv(file_path)
    
    # 处理缺失值和非字符串值
    data["cus_comment"] = data["cus_comment"].fillna("").astype(str)
    data["cus_comment"]=data["cus_comment"].apply(chinese_word_cut)
    print("after word cut",data["cus_comment"].head())
    
    n_features = 30 # 提取15个特征词语
    # 初始化 CountVectorizer
    tf_vectorizer = CountVectorizer(
                                    strip_accents = 'unicode',
                                    max_features=n_features,
                                    stop_words = None,
                                    max_df=0.8,# 调整为允许更高频率的词
                                    min_df=0.01 # 调整为较低的最小出现次数
                                    )
    # 拟合并转换文本数据为词频矩阵
    tf = tf_vectorizer.fit_transform(data["cus_comment"])
    if len(tf_vectorizer.get_feature_names_out()) == 0:
            print("警告：词汇表为空，请检查参数设置或数据内容！")
    else:
        print("词汇表：", tf_vectorizer.get_feature_names_out())
        print("词频矩阵：\n", tf.toarray())
    
    '''n_topics = 8
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,
                                    learning_method='batch',
                                    learning_offset=50,
    #                                 doc_topic_prior=0.1,
    #                                 topic_word_prior=0.01,
                                random_state=0)
    lda.fit(tf)
    
    ###########每个主题对应词语
    n_top_words = 25
    tf_feature_names = tf_vectorizer.get_feature_names_out()
    topic_word = print_top_words(lda, tf_feature_names, n_top_words)
    
    ###########输出每篇文章对应主题
    topics=lda.transform(tf)
    topic = []
    for t in topics:
        topic.append(list(t).index(np.max(t)))
    data['topic']=topic
    data.to_excel("data_topic.xlsx",index=False)
    topics[0]#0 1 2 
    
    ###########可视化

    import pyLDAvis

    pyLDAvis.enable_notebook()
    pic = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.display(pic)
    pyLDAvis.save_html(pic, f'{file_name}_lda_pass_with_'+str(n_topics)+'topics'+'.html')
    #去工作路径下找保存好的html文件
    #pyLDAvis.show(pic)

    ###########困惑度
    import matplotlib.pyplot as plt

    plexs = []
    n_max_topics = 16
    for i in range(1,n_max_topics):
        print(i)
        lda = LatentDirichletAllocation(n_components=i, max_iter=50,
                                        learning_method='batch',
                                        learning_offset=50,random_state=0)
        lda.fit(tf)
        plexs.append(lda.perplexity(tf))


    n_t=15#区间最右侧的值。注意：不能大于n_max_topics
    x=list(range(1,n_t))
    plt.plot(x,plexs[1:n_t])
    plt.xlabel("number of topics")
    plt.ylabel("perplexity")
    # 存储图片
    save_plex_pic_path = '/Users/wtsama/Documents/code/code2/python_assignment/week4/perplexity_pic/'
    os.makedirs(save_plex_pic_path, exist_ok=True)
    plt.savefig(f'{save_plex_pic_path}{file_name}_perplexity_with_'+str(n_topics)+'topics'+'.png')
    # plt.show()
print("all files saved")'''