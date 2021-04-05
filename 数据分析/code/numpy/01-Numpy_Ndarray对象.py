# -*- coding:utf-8 -*-
'''
    Numpy中定义的最终要的对象是称为ndarray的N维数组类型。它描述相同类型的元素集合。可以使用基于零的索引访问
    集合中的项目。
    numpy.array(object, dtype = None, copy = True, order = None, subok = False, ndmin = 0)
    上面的构造器接受以下参数：

    序号	参数及描述
    1.	object 任何暴露数组接口方法的对象都会返回一个数组或任何(嵌套)序列。
    2.	dtype 数组的所需数据类型，可选。
    3.	copy 可选，默认为true，对象是否被复制。
    4.	order C(按行)、F(按列)或A(任意，默认)。
    5.	subok 默认情况下，返回的数组被强制为基类数组。 如果为true，则返回子类。
    6.	ndimin 指定返回数组的最小维数。
'''
import numpy as np
# 例子01
# a = np.array([1,2,3])
# print(a)
# print(type(a))

# 多于一个维度
# a2 = np.array([[1,2],[3,4]])
# print(a2)

# 最小维度
# a3 = np.array([1,2,3,4,5],ndmin = 2)
# print(a3)
