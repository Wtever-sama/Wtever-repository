####第一题################################################################################
# 1. 定义一个类TextAnalyzer，其属性包括待分析的文本文件路径，等加载的预训练模型文件路径，       #
# 训练word2vec的一些简单参数（如向量长度，窗口大小）等，初始化的时候需要对这些属性进行定义。     #
##########################################################################################
import pandas as pd
import numpy as np
import jieba
from gensim.models import Word2Vec
from tqdm import tqdm
class TextAnalyzer:
    def __init__(self,file_path,model_path,len_vec,size_window):
        self.file_path = file_path
        self.model_path = model_path
        self.len_vec = len_vec
        self.size_window = size_window
        
        self.processed_words = None # 增加缓存
    def _pre_process(self):
        if self.processed_words:
            return self.processed_words
        
        # 使用jieba多线程模式
        # jieba.enable_parallel(4) 
        stopset = ([
            '，','【','】','#','s','1','2','3','4','5','6','7','8','9','MIUI','@','_','(',')','￣','！','[',']','-',
            '“','”','p','ID',':','：','~','td','t','d','//','/','？','。','%','>>','>','《','》','、','+','ing','TNND','〜',
            '🎂','⊙','o','(⊙o⊙)','⊙o⊙','.','..','..........','℃','H','……','^','*','$','￥','↗','↖','ω','↖(^ω^)↗','😃','…','""','"','Y',
        ])
        chunk_size = 10000
        chunks = pd.read_csv(# csv更快
            self.file_path,
            sep = '\t',
            header=0,# 第一行是列名（location/text/user_id/weibo_created_at）
            names=['text'],         # 指定列名（覆盖原有列名）
            chunksize=chunk_size,
            usecols=[1],# 只读取内容列
            dtype={'text':str},
            engine='c',
            on_bad_lines='skip'     # 跳过格式错误行
            )
        
        words = []
        #jieba.enable_parallel(4)  # 开启4个线程提高速度
        for chunk in tqdm(chunks, desc="Processing text chunks",dynamic_ncols=True):
            texts = chunk['text'].dropna().unique()
            words.extend([[w for w in jieba.lcut(text)if w not in stopset]
                         for text in texts])
            
        self.processed_words = words
        return words
    def _get_word2vec_model(self):
        words = self._pre_process()
        model = Word2Vec(words,
                        vector_size = self.len_vec,
                        window = self.size_window,
                        min_count = 2,
                        workers=4,
                        sg=1,             # 使用 Skip-gram 算法
                        alpha=0.01,       # 初始学习率
 #                       min_alpha=0.0001, # 最小学习率
#                        seed=42,          # 随机种子
                        sample=1e-5,      # 高频词下采样阈值
                        hs=0,             # 使用负采样
                        negative=10,      # 负采样数量
                        epochs=20         # 迭代次数
                        
                        )
        model.save(self.model_path)
        print("model saved")
        return model
    def get_similar_words(self, string):
        model = self._get_word2vec_model()
        most_similar = model.wv.most_similar(string,topn = 10)
        #least_similar = model.wv.most_similar(negative = str(string), topn = 10)
        return most_similar
        
if __name__ == "__main__":
    text_ana = TextAnalyzer(
        file_path='/Users/wtsama/Documents/code/code2/python_assignment/week5/weibo.txt',
        model_path='/Users/wtsama/Documents/code/code2/python_assignment/week5/word2vec.model',
        len_vec=300,
        size_window=10
    )
    print(text_ana.get_similar_words("回忆"))
####第二题##########################################################################################
# 在上述类加入一个预处理方法_pre_process，如将待分析的weibo.txt加载到内存（请先解压提供的weibo.txt.zip)，#
# 进行基本的文本预处理，如对所有微博内容进行去重，进行分词、去除停用词、标点等，                          #
# 最终建立一个以微博为单位进行分词的二维列表。注意，weibo.txt一行为一条微博的属性，                       #
# 用\t分隔后，第二个元素为微博内容。（提供的weibo.txt包含大量重复和标点等，需要仔细预处理，                #
# 否则会影响后面的嵌入模型训练。）                                                                     #
#####################################################################################################
