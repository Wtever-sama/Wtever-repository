comment_file = '/Users/wtsama/Documents/code/code2/python_assignment/week3/week3.csv'

import pandas as pd
from tqdm import tqdm
def filter_file(file_path):
    df = pd.read_csv(file_path)
    save_path = '/Users/wtsama/Documents/code/code2/python_assignment/week4/file_group/'
    # 获取shopID列的所有值，将重复的值忽略，按照升序排列成一个列表
    shop_id_list = df['shopID'].unique() #返回一个list
    year_list = df['year'].unique()
    # 将numpy.int64 object转化为普通的int类型
    shop_id_list = [int(id) for id in shop_id_list]
    year_list = [int(year) for year in year_list]
    
    for shop_id in tqdm(shop_id_list, desc = 'Processing', unit = 'shop_id'):
        # shop_all_year_dict每个键为年份，就是year_list 中的元素,值是一个列表，包含这个年份所有的评论
        shop_all_year_dict = {}
        for year in tqdm(year_list, desc = 'Processing', unit = 'year'):
            # 初始化shop_all_year_dict
            shop_all_year_dict[year] = []
            
            id_filter = df[(df['shopID']==shop_id) & (df['year']== year)]
            comments = id_filter['cus_comment']
            comments = comments.dropna()
            # 得到一个列表，是该年的所有评论行的合集
            # comments.to_csv(f'{save_path}shop_{shop_id}_time_{year}.csv', index = False)
            # 如果comments为空，则将该年的评论行设置none，继续读取下一个年份
            for comment in comments:
                if not isinstance(comment, str):
                    continue
                # 得到一个列表，是该评论行的所有词
                words = comment.split()
                shop_all_year_dict[year]+=words
                
        #将shop_all_year_dict写入文本txt,要求每个元素单独占据一行
        with open(f'{save_path}shop_{shop_id}.txt','w',encoding = 'utf-8')as file:
            # 对字典shop_all_year_dict中的每个值进行遍历
            
            for year_id,year_comment in shop_all_year_dict.items():
                # 将列表转化为字符串
                year_comment = ' '.join(year_comment)
                file.write(year_comment)
                file.write('\n')
            file.close() 

              
filter_file(comment_file)
        