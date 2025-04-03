# 输入，一个列表有多个tuple
students = eval(input("please put in the list of tuples: "))

# 按照降序排列学生成绩
sorted_students = sorted(students, key = lambda x: x[2], reverse = True )

for i in sorted_students:
    # 按照学号 奖项 分数 输出
    print(i[0], i[1], i[2])
