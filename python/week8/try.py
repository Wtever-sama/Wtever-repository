'''def d(f):
    def n(*args):
        return '$'+str(f(*args))
    return n
@d
def p(a,t):
    return a+a*t
print(p(100,0))'''
#max=lambda a,b:a if(a>b)
#print(max(1,2))
#python 关键字；关键字是具有特殊意义和用途的保留字，不能用作变量名、函数名或其他标识符。以下是 Python 的关键字列表
#['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 
#'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 
#'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 
#'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 
#'with', 'yield']

def foo(*args,**kwargs):
    print(f"args={args},kwargs={kwargs}")
foo(oine =1, twp=2)#args=(),kwargs={'oine': 1, 'twp': 2}
foo([1,2,3])#args=([1, 2, 3],),kwargs={}