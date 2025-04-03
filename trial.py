import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging
import time

# 配置日志
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def train_word2vec(input_file, output_model_file, output_vector_file):
    """
    训练Word2Vec模型并保存
    
    参数:
        input_file: 输入文本文件路径(每行是分词后的微博内容)
        output_model_file: 模型输出文件路径(.model)
        output_vector_file: 词向量输出文件路径(.vec)
    """
    start_time = time.time()
    
    print("开始训练Word2Vec模型...")
    
    # 使用LineSentence读取大型文本文件(逐行读取，避免内存不足)
    sentences = LineSentence(input_file)
    
    # 配置Word2Vec参数
    model = Word2Vec(
        sentences=sentences,
        vector_size=200,      # 词向量维度
        window=5,             # 上下文窗口大小
        min_count=5,          # 忽略出现次数低于此值的词
        workers=8,            # 使用多线程
        epochs=10,            # 迭代次数
        sg=1,                 # 使用skip-gram模型(1), 0表示CBOW
        hs=0,                 # 使用负采样
        negative=5,           # 负采样数量
        sample=1e-3           # 高频词下采样阈值
    )
    
    # 保存模型(可以重新加载继续训练)
    model.save(output_model_file)
    
    # 保存词向量(纯文本格式，可用于其他工具)
    model.wv.save_word2vec_format(output_vector_file, binary=False)
    
    end_time = time.time()
    print(f"训练完成! 耗时: {end_time-start_time:.2f}秒")
    print(f"模型已保存至: {output_model_file}")
    print(f"词向量已保存至: {output_vector_file}")

# 使用示例
if __name__ == "__main__":
    input_file = "/Users/wtsama/Documents/code/code2/python_assignment/week5/processed_words.txt"  # 你的400MB分词文本文件
    output_model = "/Users/wtsama/Documents/code/code2/python_assignment/week5/weibo_word2vec.model"
    output_vector = "/Users/wtsama/Documents/code/code2/python_assignment/week5/weibo_word2vec.vec"
    
    train_word2vec(input_file, output_model, output_vector)