# 第1行，两个正整数n，m用空格分隔
# n,m表示所有学生的数量和所有精品好课的数量
n, m = map(int, input().split())

# 第2行，n个字符串，表示学院所有同学的姓名（没有重复）
names = input().split()

# 输入第3行至第m+2行（共m行），每行表示一门精品好课，有k个字符串，表示选修该课所有人的姓名。一个人可以同时学习多门精品好课
courses = []
for i in range(m):
    courses.append(input().split())

# input()读取一行输入。
# .split()将这一行按空格分割成多个字符串，形成一个表示选修该课程的学生姓名的列表。


# 标记是否有没有没有出勤的人
flag = False
# 没有上课的人数
nums = 0
for student in names:
    # 检查是否出勤
    if all(student not in course for course in courses):
        nums += 1

print(nums)
'''
6 3
gorilla ape chimpanzee monkey baboon macaque
ape monkey
gorilla monkey ape
baboon ape

7 4
a b c d e f g h
a b c
a b c
g e f 
c e f
'''