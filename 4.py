'''
有n个歌单。每个歌单的第一行是一个数字count，表示歌单里的曲 目；接下来count行，每行一个字符串和一个数字title和comments，表
示小明在歌曲下方留言的次数和歌曲的名字
'''
'''
1 对于输入的后面几行，既有数字也有元组（包含字符串和整数），创建一个列表，字典的key是歌曲名字，value是留言次数
2 如果输入的字符串是数字，就忽略；如果是一个str和一个数字并且用空格分割，就添加到列表
3 将列表按照留言次数降序排列，然后每行输出字典一个元素的key和value，用空格分割
'''
'''
对于输入的每一个第二行开始的数字，就将歌单数减少一
'''
#读入一个正整数，表示歌单数量
n = int(input())
# 代表歌曲总数
nums = 0
# 用字典存储歌曲名字和留言次数
list = {}
for i in range(n):
    count = int(input())
    nums += count
    for _ in range(count):
        line = input().split()
        title = line[0]
        comments =line[1]
        list[title] = int(comments)
        

# 给列表按照第二个值降序排序
# 使用 items() 方法获取键值对，并按留言次数降序排序
sorted_list = sorted(list.items(), key = lambda x: x[1], reverse = True)
# 按行输出列表每个元组，用空格分割元组中的不同元素
for title, comments in list.items():
    print(title, comments)
    
'''
3
2
Don_t_Fight_The_Music 13
Marble_Blue 11
4
Sasoribi 10
Invisible_Frenzy 8
TiamaT_F_Minor 7
Disrupter_Array 6
2
Tsunagite 9
Pandora_Paradoxxx 1
'''

        
        
    