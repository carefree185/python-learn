# -*- coding:utf-8 -*-
import numpy as np
'''
    NumPy - 统计函数
    NumPy 有很多有用的统计函数，用于从数组中给定的元素中查找最小，最大，百分标准差和方差等
'''

'''
    Nump.main  numpy.amax
    这些函数从给定数组中的元素沿指定轴返回最小值和最大值。
    
'''
# a = np.random.randint(1,15,size = (3,3))
a = np.array([[1,2,3,4],[7,8,9,10]])
'''
    random模块
    rand  返回 0 - 1 随机值
    randn 返回一个样本具有标准正态分布
    randint 返回随机的整数，位于半开区间[low,hight)size = 10  (3,3)
    random_integers(low[, high, size])  返回随机的整数，位于闭区间
    random 返回随机浮点数
'''
print(a)
#amin返回最小值
print('------------amin 返回最小值-------------')
print(np.amin(a,1)) #参数1 表示同行数据
print(np.amin(a,0)) #参数0 表示同列数据
#amax返回最大值
print('------------amax 返回最大值-------------')
print(np.amax(a,1))
print(np.amax(a,0))

#mean 平均值
print('------------mean 平均值-------------')
print(np.mean(a))
print(np.mean(a,0)) #求列平均值
print(np.mean(a,axis = 1)) #求行平均值

'''
    标准差  是与平均值的偏差的平方的平均值的平方根
    std = sqrt(mean((x-x.mean())**2))
    如果数组是[1,2,3,4] 则平均值是 2.5 因此偏差是[1.5,0.5,0.5,1.5],
    偏差的平方是[2.25,0.25,0.25,2.25]
    并且其平均值的平方根，即sqrt(5/4)
'''
arr2 = np.array([[1,2,3,4],[7,8,9,10]])
print(arr2)
# print(arr2-arr2.mean()) #平均值的偏差
print(((arr2-arr2.mean())**2).sum()/arr2.size)#平均值的偏差的平方的平均值
print(np.mean(((arr2-arr2.mean())**2)))#平均值的偏差的平方的平均值
print(np.sqrt(((arr2-arr2.mean())**2).sum()/arr2.size))
print(np.sqrt(np.mean(((arr2-arr2.mean())**2))))
print(np.std(arr2,0))
print('************************')
'''
    方差
    方差是偏差的平方的平均值即mean(x-x.mean()**2)
'''
arr3 = np.array([[1,2,3,4],[7,8,9,10]])
# print(np.var(arr3))
# print(arr3-arr3.mean())
print(((arr3-arr3.mean())**2).sum()/arr3.size)
print(np.mean((arr3-arr3.mean())**2))
print(np.var(arr3))




