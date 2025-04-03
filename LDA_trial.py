import os
from tqdm import tqdm
import pandas as pd
import jieba
indir_path = '/Users/wtsama/Documents/code/code2/python_assignment/week4/file_group/'

stop_words = set([
    "算是","吧","在","的","不是","和","也","什么","了","人","把","就","来","不","这次","一个","没","我"
    ,"在","过","嘛","还","九","开","而","去","也","但是","都","宝宝","们","啊","但","哈","只","然后","呀"
    ,"因为","先","要","到","哈哈","同时","为了","个人感觉","上去","一边","例如"
                                                ,"一粒","次次","带我去"
                                                "哪里","其次","无法","有待","肯定","不会"
])
### 以店铺520356为例
file_path='/Users/wtsama/Documents/code/code2/python_assignment/week4/csv_filtered_group/shop_520356.txt.csv'
# jieba 分词
def chinese_word_cut(text):
    if not isinstance(text, str):
        return ""
    return " ".join(word for word in jieba.cut(text) if word not in stop_words)

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import numpy as np

data = pd.read_csv(file_path, encoding='utf-8')
# 处理缺失值和非字符串值
data["cus_comment"] = data["cus_comment"].fillna("").astype(str)
data["cus_comment"]=data["cus_comment"].apply(chinese_word_cut)
print("after word cut",data["cus_comment"].head())

n_features = 30 # 提取30个特征词语
# 初始化 CountVectorizer
tf_vectorizer = CountVectorizer(
                                strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words = None,
                                max_df=0.6,# 调整为允许更高频率的词
                                min_df=5 # 调整为较低的最小出现次数
                                )
# 拟合并转换文本数据为词频矩阵
tf = tf_vectorizer.fit_transform(data["cus_comment"])
if len(tf_vectorizer.get_feature_names_out()) == 0:
        print("警告：词汇表为空，请检查参数设置或数据内容！")
else:
    print("词汇表：", tf_vectorizer.get_feature_names_out())
    print("词频矩阵：\n", tf.toarray())
    
    
n_topics = 8
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,# 最大迭代次数
                                learning_method='batch',
                                learning_offset=50, # 学习偏移量
#                                 doc_topic_prior=0.1,
#                                 topic_word_prior=0.01,
                            random_state=0 # 随机种子，默认为0。确保每次运行结果一致
                            )
lda.fit(tf) # 将转换后的词频矩阵进行拟合提取潜在主题

# 打印高频词
def print_top_words(model, feature_names, n_top_words):
    # 返回列表top_words
    tword = []
    for topic_idx, topic in enumerate(model.components_):# model.components_包含每个主题对应的词分布向量，topic_idx 表示当前主题的索引
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword

###########每个主题对应词语
n_top_words = n_features
tf_feature_names = tf_vectorizer.get_feature_names_out() # 长度为n_features，这里是30
topic_word = print_top_words(lda, tf_feature_names, n_top_words)

###########输出每篇文章对应主题
topics=lda.transform(tf) # 返回每个文档在各个主题上的概率分布
topic = []
for t in topics:
    topic.append(list(t).index(np.max(t))) # 遍历每个文档的主题分布，找到最大值对应的索引（即最相关的主题编号）
data['topic']=topic # 添加主题列并保存数据
data.to_csv("/Users/wtsama/Documents/code/code2/python_assignment/week4/shop_520356_topic.csv",index=False)
topics[0]#0 1 2 查看第一个文档的主题编号

'''###########可视化
import matplotlib.pyplot as plt
import seaborn as sns
# 处理中文乱码问题
# from matplotlib import rcParams
# import matplotlib.font_manager as fm

# 文档-主题分布可视化
def plot_document_topic_distribution(topics, n_topics):
    # 设置中文字体（支持中文且系统自带）
    #font_path ='/System/Library/AssetsV2/com_apple_MobileAsset_Font7/c3a843d226791256d897018e02e6c09b1ef283a9.asset/AssetData/Kavivanar-regular.ttf'
    #font = fm.FontProperties(fname=font_path)
    #plt.rcParams['font.family'] = font.get_name()
    #plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号
    #plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'SimHei']
    #plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(12, 8))
    sns.heatmap(topics, cmap="YlGnBu", xticklabels=[f'Topic{i}' for i in range(n_topics)])
    plt.title("Document-Topic Distribution")
    plt.xlabel("Topic")
    plt.ylabel("Document")
    plt.show()

# 调用函数绘制文档-主题分布
plot_document_topic_distribution(topics, n_topics)

# 利用pickle或json对所得到的lda模型、对应的词频矩阵、以及特征表示等进行序列化保存
import pickle
# 保存前将所有对象存入字典
save_data = {
    'lda_model': lda,
    'tf_matrix': tf,
    'vectorizer': tf_vectorizer,
    'topic_words': topic_word,
    'topic_list': topic
}
# 一次性保存，并修改保存路径
file_name = 'lda_model'
save_path = '/Users/wtsama/Documents/code/code2/python_assignment/week4/'
with open(save_path + file_name + '.pkl', 'wb') as f:
    pickle.dump(save_data, f)
print('保存成功')
'''   

'''import pyLDAvis
import pyLDAvis.sklearn
# pyLDAvis.enable_notebook()
pic = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
# pyLDAvis.display(pic)
pyLDAvis.save_html(pic, f'shop_520356_lda_pass_with_'+str(n_topics)+'topics'+'.html')
print(f"可视化结果已保存为 shop_520356_lda_pass_with_{n_topics}topics.html")
#去工作路径下找保存好的html文件
#pyLDAvis.show(pic)'''

###########困惑度
import matplotlib.pyplot as plt

plexs = []
n_max_topics = 100
for i in range(1,n_max_topics):
    # print(i)
    lda = LatentDirichletAllocation(n_components=i, max_iter=50,
                                    learning_method='batch',
                                    learning_offset=50,random_state=0)
    lda.fit(tf)
    plexs.append(lda.perplexity(tf))


n_t=99#区间最右侧的值。注意：不能大于n_max_topics
x=list(range(1,n_t))
plt.plot(x,plexs[1:n_t])
plt.xlabel("number of topics")
plt.ylabel("perplexity")
# 存储图片
save_plex_pic_path = '/Users/wtsama/Documents/code/code2/python_assignment/week4/pic/'
file_name = 'plex_pic.png'
# os.makedirs(save_plex_pic_path, exist_ok=True)
plt.savefig(f'{save_plex_pic_path}{file_name}_with_'+str(n_max_topics)+'topics'+'.png')
print('save plex pic successfully')
# plt.show()
