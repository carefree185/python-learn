# -*- coding:utf-8 -*-
import numpy as np
'''
    numpy.empty
    创建指定形状和dtype的未初始化数组
    numpy.empty(shape, dtype = float, order = 'C')
    构造器接受下列参数：
    
    序号	参数及描述
    1.	Shape 空数组的形状，整数或整数元组
    2.	Dtype 所需的输出数组类型，可选
    3.	Order 'C'为按行的 C 风格数组，'F'为按列的 Fortran 风格数组
'''
#例: 数组元素为随机值
arr = np.empty((3,3),dtype = 'i1')
print(arr)

'''
    numpy.zeros
    返回特定大小，以0填充
'''
#例
# arr = np.zeros((3,3))
# print(arr)

# 自定义类型
# arr = np.zeros((3,3), dtype =  [('x',  'i4'),  ('y',  'i4')])
# print(arr)

'''
    numpy.ones
    返回特定大小，以1填充
'''
# arr = np.ones((2,3,4))
# print(arr)
# arr = np.ones((3,3), dtype =  [('x',  'i4'),  ('y',  'i4')])
# print(arr)


'''
    ---------------------------------------
    -       Numpy 来自现有数据的数组        -
    ---------------------------------------
'''

'''
    numpy.asarray
    类似 numpy.array 可以将Python序列转换为ndarray
'''
#来自列表
# arr = [1,2,3,4]
# arr2 = np.asarray(arr)
# print(arr2)
# print(type(arr))
# print(type(arr2))

#来自元组
# arr = (1,2,3,4)
# arr2 = np.asarray(arr)
# print(arr2)
# print(type(arr))
# print(type(arr2))

#来自元组列表
# arr = [(1,2,3,4),(5,6,7,8)]
# arr2 = np.asarray(arr)
# print(arr2)
# print(type(arr))
# print(type(arr2))


'''
    ---------------------------------------
    -       Numpy 来自数值范围的数组        -
    ---------------------------------------
'''

'''
    numpy.arange
    这个函数返回ndarray对象，包含给定范围内的等间隔值
    numpy.arange(start,stop,step,dtype)
'''

# arr = np.arange(5,dtype = float)
# print(arr)


'''
    numpy.linspace
    与arange函数类似  等差数列
    numpy.linspace(start,stop,num,endpoint,retstep,dtype)
    start 起始值
    stop  结束值
    num   生成等间隔样例的数量，默认为50
    endpoint 序列中是否包含stop 值 默认为 True
'''
# arr = np.linspace(10,20,9)
# print(arr)

# arr = np.linspace(10,20,5,endpoint=False)
# print(arr)

# arr = np.linspace(10,20,5,retstep=True)
# print(arr) #返回步长

'''
    numpy.logspace 
    等比数列
    numpy.logscale(start, stop, num, endpoint, base, dtype)
    1.	start 起始值是base ** start
    2.	stop 终止值是base ** stop
    3.	num 范围内的数值数量，默认为50
    4.	endpoint 如果为true，终止值包含在输出数组当中
    5.	base 对数空间的底数，默认为10
    6.	dtype 输出数组的数据类型，如果没有提供，则取决于其它参数
'''
# arr = np.logspace(1,10,10,base = 2)
# print(arr)


'''
    其他创建方式
    random模块
    rand  返回 0 - 1 随机值
    randn 返回一个样本具有标准正态分布
    randint 返回随机的整数，位于半开区间[low,hight)size = 10  (3,3)
    random_integers(low[, high, size])  返回随机的整数，位于闭区间
    random 返回随机浮点数
'''
# arr = np.random.rand(9).reshape(3,3)
# print(arr)

# arr = np.random.rand(3,2,3)
# print(arr)

# arr = np.random.randn(9).reshape(3,3)
# print(arr)

# arr = np.random.randn(3,2,3)
# print(arr)

# arr = np.random.randint(1,9,size = (2,4))
# print(arr)

# arr = np.random.random_integers(1,9,size =(2,4))
# print(arr)

# arr = np.random.random((3,2,3))
# print(arr)

# arr = np.random.randn(3,2,3)
# print(arr)

