# 输入一个小数的序列，用逗号隔开，请用list存储并排序，从大到小输出。'
nums = eval(input())
sorted_nums = sorted(nums, reverse=True) #排序整个列表，列表每个“组”只有一个元素的时候，不能用lambda函数

for i in sorted_nums:
    print(i)
    print("\n")