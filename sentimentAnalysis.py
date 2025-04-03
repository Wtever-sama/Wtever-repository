import pandas as pd
import os

           

def emotion_analyse(file_path, row_index, anaylse_cmd = 0):# 默认为混合情绪分析
    '''
    函数一：混合情绪分析：认为文本的情绪是混合的，即统计文本中所有情绪词的出现次数，并计算每种情绪的比例。
    例如，如果joy出现n1次，总情绪词数为n，则joy的比例为n1/n。
    五类情绪词汇：
    anger、disgust、fear、sadness和joy
    
    结构：闭包，mix_analyse(analyse_cmd)
    
    参数1：文件路径，是一个csv，包含列名为cus_comment的列，对其中某一行进行文本分析
    参数2：row_index，表示要分析的行号
    参数3：anaylse_cmd，表示要分析的命令，可选值有mix_analyse和single_analyse，类型为整数
    
    返回：一个字典，键为每种情绪类型的词汇，值为每个情绪类型的词汇的出现的比例
    '''
    
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
        # 查看这个字典中的键值对看是否成功
        # print(dict_emotion['anger'][4],dict_emotion['disgust'][3])'''
        
    df = pd.read_csv(file_path)

    column = df['cus_comment'] # 返回一个series
    comment = column[row_index] # 以第一个单元格为例子
    # print(comment)
    
    # 将comment中的所有按照空格分割的词汇存入一个列表
    comment_list = comment.split()   

    emotion_lexicon = read_emotion_lexicon() 
    
    def mix_analyse(analyse_cmd):
        # 创建一个统计频率的字典
        emotion_frequency_dict = {'anger':0, 'disgust':0, 'fear':0, 'sadness':0, 'joy':0}
        # 根据comment_list中的每个词，在emotion_lexicon中查询  
        for word in comment_list:
            for emotion_type in emotion_lexicon:
                if word in emotion_lexicon[emotion_type]:
                    emotion_frequency_dict[emotion_type] +=1
                    
        ### 第二问继续修改代码计算情绪比例，不论情绪词出现次数相同，还是值相同
        sum_frequency = sum(emotion_frequency_dict.values())
        if sum_frequency == 0:
            print('The comment is empty.')
        else :
            anger_proportion = emotion_frequency_dict['anger']/sum_frequency
            disgust_proportion = emotion_frequency_dict['disgust']/sum_frequency
            fear_proportion = emotion_frequency_dict['fear']/sum_frequency
            sadness_proportion = emotion_frequency_dict['sadness']/sum_frequency
            joy_proportion = emotion_frequency_dict['joy']/sum_frequency
            
            emotion_proportion_dict = {'anger':anger_proportion,
                                    'disgust':disgust_proportion,
                                    'fear':fear_proportion,
                                    'sadness':sadness_proportion,
                                    'joy':joy_proportion}
        
        if (analyse_cmd == 0):# 情绪分析模式
            ###（1）函数一：混合情绪分析
            sum_frequency = sum(emotion_frequency_dict.values())
            anger_proportion = emotion_frequency_dict['anger']/sum_frequency
            disgust_proportion = emotion_frequency_dict['disgust']/sum_frequency
            fear_proportion = emotion_frequency_dict['fear']/sum_frequency
            sadness_proportion = emotion_frequency_dict['sadness']/sum_frequency
            joy_proportion = emotion_frequency_dict['joy']/sum_frequency
            print(f"The proportions of each emotion type are:\n anger: {anger_proportion}, disgust: {disgust_proportion}, fear: {fear_proportion}, sadness: {sadness_proportion}, joy: {joy_proportion}")
             
        else:
            ### (2)函数二：单一情绪分析
            
            # 判断最大值有相同的情况，或者值同
            sorted_emotion_frequency_dict = sorted(emotion_frequency_dict.items(), key = lambda x: x[1],reverse = True)
            
            if sorted_emotion_frequency_dict[0] == sorted_emotion_frequency_dict[1]== sorted_emotion_frequency_dict[2] == sorted_emotion_frequency_dict[3]== sorted_emotion_frequency_dict[4]:
                print('The emotional tendency is ambiguous.')
            else:
                # 找出值最大的键然后打印
                max_key = max(emotion_frequency_dict, key=emotion_frequency_dict.get)
                print(f'The emotional tendency is {max_key}') # 正确的格式化插入       
                 
        return emotion_frequency_dict 
        
    
    return mix_analyse
   
                
comment_file = r"python_assignment\week3\week3.csv"
# print("To use the second comment as an example:")
emo_ana_fun = emotion_analyse(comment_file, 16, 0)
print("16:",emo_ana_fun(0)) 

