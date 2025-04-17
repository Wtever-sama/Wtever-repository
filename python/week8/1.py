from functools import wraps
def log_decorator(func):
    @wraps(func)# 保留函数的元信息
    def wrapper(*args,**kwargs):
        print(f"开始执行函数:{func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数{func.__name__}执行结束")
        return result  
    return wrapper

def validate_and_standardize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        numbers = args[0]
        stand_numbers = []
        for i in numbers:
            if len(i) < 11:
                print(f'无效号码:{i}')
                continue
            
            #取出字符串的前缀，包括+91, 91, 0
            if i[0]=='+':
                appendix = i[3:]
            elif i[0]=='9':
                appendix = i[2:]
            elif i[0]=='0':
                appendix = i[1:]
            else:
                appendix = i
            #判断appendix是否是11位的数字
            if appendix.isdigit() and len(appendix) == 11:
                stand_numbers.append(f'+91 {appendix[0:3]} {appendix[3:7]} {appendix[7:11]}')
            else:
                print(f'无效号码:{i}')
            
        return func(stand_numbers, **kwargs)
    return wrapper

@log_decorator
@validate_and_standardize
def sort_phone_number(numbers):
    #numbers is a list of phone numbers
    sorted_numbers = sorted(numbers)#默认进行升序排列，sorted(numbers, reverse=True)是降序
    for i in sorted_numbers:
        print(i)
        
n = int(input())
phone_numbers = []
for _ in range(n):
    phone_numbers.append(input())#每个元素有可能是一个字符串，也可能numbers,甚至是特殊符号加numbers

sort_phone_number(phone_numbers)