import matplotlib.pyplot as plt  
import os    
import pandas as pd
from tqdm import tqdm  # 导入进度条库

comment_file = r"python_assignment\week3\week3.csv"
# 创建情绪字典
def read_emotion_lexicon():
    '''
    创建情绪字典
    返回：一个字典，键为情绪种类，值为情绪词语的列表
    '''
    input_folder = r"python_assignment\week3\emotion_lexicon"
    dict_emotion = {}
    for file_name in os.listdir(input_folder):
        # 由于open函数需要完整的文件路径，必须使用os.path.join函数
        file = os.path.join(input_folder, file_name)
        with open(file, "r", encoding = 'utf-8') as file:
            # 将每个text文档中的每个按照行分割的词汇存储在一个字典中，键为文档的名称，去除后缀'.txt'，值为所有词汇的列表
            lines = file.readlines() # 按行读取，返回一个列表
            lines = [line.strip() for line in lines] # 去除换行符，strip去除字符串首尾的空白字符（包括换行符\n、制表符\t和空格）
                # 对文档名进行切片操作，去除最后四个字符；按照换行符分割成列表
        dict_emotion[file_name[:-4]] = lines
            
        # 将dict_emotion这个字典挨个连接起来
    return dict_emotion    

emotion_lexicon = read_emotion_lexicon()  
def time_scale_analyse(file_path, shop_id, time_scale, emotion_type):
    '''
    2.时间模式分析函数实现。

    利用数据集中的评论时间信息，分析不同时间段的情绪比例变化趋势。
    实现一个函数，可以通过参数控制来返回指定店铺、指定情绪的时间模式，并可视化呈现这些模式。
    例如，可以展示shopID为518986的店铺积极情绪的小时模式，或shopID为520004店铺消极情绪的周模式等。
    
    :param 1: shop ID
    :param 2: time scale
    :param 3: emotion type
    
    :return: time scale analysis result, a picture, none
    '''
    '''
    以小时为例子：
    先按照shopID进行筛选，time_scale筛选，对其时间进行升序排列
    然后对每个dataframe中的变量为cus_comment的单元格进行情绪词频统计，根据指定情绪类型计算出每小时或者每个时刻的该类型情绪比列，
    以小时为横轴，横坐标为0-23，纵坐标为该时间段该情绪比例，画出一张折线图
    
    ***对于general的time_scale情况而言，就按照传入的time_scale进行判断，
    是hour就按照hour列为自变量，其他变量忽略，hour 相同的作为一个数据集求出所有评论的情绪比例然后取平均，
    如果比例分母为0就删除子数据，得出的平均值对应这个hour下的因变量，所有的数据集处理好后形成一个hour为自变量，
    proportion 为因变量的dataframe然后做出折线图***
    是week就按照weekday列，以此类推
    '''
    # 读入csv表格
    df = pd.read_csv(file_path)
    shop = shop_id
    row_id_filter = df[df['shopID']==shop] # 返回一个series
    # comments = row_id_filter['cus_comment']
    
    # 获取time_scale 列的所有值，将重复的值忽略，按照升序排列成一个列表
    time_scale_list = row_id_filter[f'{time_scale}'].unique()
    # 将所有time_scale 列等于time_scale_list中的值的row_index提取出来
    # 初始化一个字典用来存储每个时间段对应的指定情绪比例
    time_scale_list = sorted(map(int, time_scale_list), key=lambda x: x, reverse=False)
    draw_dict = {time: 0 for time in time_scale_list} # 将np整型转化为普通的
    # 存储所有时间段评论中的词语频率，包含所有词汇的词频
    all_types = {time: 0 for time in time_scale_list}
    
    for time in tqdm(time_scale_list, desc="Processing time scale", unit="time"):
        all_words = []
        try:
            time_row_id_filter = row_id_filter[row_id_filter[f'{time_scale}']==time]
            comments = time_row_id_filter['cus_comment']
            comments = comments.dropna()
            # 将comments的所有行的值提取出来，得到一个列表
            for comment in comments:
                # 将评论中的所有词语提取出来，得到一个列表
                if not isinstance(comment, str):
                    continue
                words = comment.split()
                # 将所有评论中的词语汇总到一个列表中
                all_words += words
        
            for word in all_words:
                if word in emotion_lexicon[emotion_type]:
                    # 将该词出现的次数加1
                    draw_dict[time] += 1
                if word in emotion_lexicon['anger'] or word in emotion_lexicon['disgust'] or word in emotion_lexicon['fear'] or word in emotion_lexicon['sadness'] or word in emotion_lexicon['joy']:
                    all_types[time] += 1
            
        except Exception as e:
            print(f"Error processing time scale {time}: {e}")
            
    draw_dict1 = {time: draw_dict[time]/all_types[time] for time in time_scale_list}
    # print(draw_dict1)
    
 
    # 将这个字典转化为一个可以用来画图的series
    draw_df = pd.Series(draw_dict1, index=time_scale_list) 
    # 可视化
    plt.figure(figsize=(10, 6))
    plt.plot(draw_df, color = 'blue', marker = 'o', linestyle = '-')
    # plt.scatter(draw_df.index, draw_df.values[0], color = '#red')
    plt.title(f'{emotion_type} proportion of shopID {shop_id} in {time_scale}',fontsize = 16)
    plt.xlabel(f'{time_scale}',fontsize = 12)
    plt.ylabel(f'{emotion_type} proportion',fontsize = 12)
    plt.xticks(time_scale_list)
    plt.grid(True)
    plt.ylim(0.0,0.05)
    plt.show()          
    
    
time_scale_analyse(comment_file, 1893229, 'month', 'disgust')

    