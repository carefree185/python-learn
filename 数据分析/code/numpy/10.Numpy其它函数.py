# -*- coding:utf-8 -*-
import numpy as np

'''
    numpy.where
    是三元表达式 x if condition else y 的矢量化版本
'''

# print(help(np.where))
# a = np.where([[True, False], [True, True]],[[1, 2], [3, 4]],[[9, 8], [7, 6]])
# print(a)

xarr = np.array([1,2,3,4,5])
yarr = np.array([6,7,8,9,10])
condition = xarr < yarr
#传统的三元表达式
# zip 函数接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个tuple（元组），
# 然后返回由这些tuples组成的list（列表）
result1 = [x if c else y for (x,y,c) in zip(xarr,yarr,condition)]
print(result1)
result2 = np.where(condition,xarr,yarr)
print(result2)

'''
    案例：将数组中的所有异常数字替换为0，比如将NaN替换为0
'''
arr = np.array([
    [1,2,np.NaN,4],
    [4,5,6,np.NaN],
    [np.inf,7,8,9],
    [np.inf,np.e,np.pi,4]
])

print('原数组：')
print(arr)
#设置条件
condition = np.isnan(arr) | np.isinf(arr)
print('结果：')
print(np.where(condition,0,arr))



'''
    np.uunique函数
    主要的作用是将数组中的元素进行去重操作（也就是只保存不重复的数据）
'''
arr = np.array(['图书','数码','小吃','数码','男装','小吃','美食','数码','女装'])
print('原始数组：')
for a in arr:
    print(a,end = ' ')
print()

print('去重数据：')
arr2 = np.unique(arr)
for a in arr2:
    print(a,end = ' ')
print()

