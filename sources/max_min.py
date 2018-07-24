# -*- coding: utf-8 -*-
def findMinAndMax(L):
    if len(L)==0:
        return(None,None)
    else:
        max = L[0]
        min = L[0]
        for a in L:
            if a > max:
                max=a
            elif a < min:
                min=a
        return (min,max)

if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
