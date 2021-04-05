# -*- coding:utf-8 -*-
import numpy as np
'''
    ndarray.shape
    这个数组属性返回一个包含数组维度的元组，它也可以用于调整数组大小
'''
# a = np.array([[1,2,3],[4,5,6]])
# print(a)
# print(a.shape)

#调整数组大小
# a = np.array([[1,2,3],[4,5,6]])
# a.shape=(3,2)
# print(a)

'''
    reshape 调整数组大小
'''
# a = np.array([[1,2,3],[4,5,6]])
# b = a.reshape(3,2)
# print(b)


'''
    ndarray.ndim 返回数组的维数
'''
# a = np.arange(24)
# print(a)
# print(a.ndim)
# b = a.reshape(2,4,3)
# print(b)
# print(b.ndim)
# print(b.shape)

'''
    numpy.itemsize
    返回数组中每个元素的字节单位长度
'''
#数组的int8 一个字节
# x = np.array([1,2,3,4,5], dtype = np.int8)
# print(x.itemsize)
#数组的float32 4个字节
# x = np.array([1,2,3,4,5], dtype = np.float32)
# print(x.itemsize)

'''
    ndarray.size
    返回数组的大小，即shape中的乘积
'''
arr = np.arange(18).reshape(2,3,3)
print(type(str(arr)))
print(arr.shape)
print(arr.size)

