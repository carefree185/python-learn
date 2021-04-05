# -*- coding:utf-8 -*-

'''
    NumPy 数字类型是dtype(数据类型)对象的实例，
    每个对象具有唯一的特征。 这些类型可以是np.bool_，np.float32等。

'''
import numpy as np
#使用数组标量类型
# dt = np.dtype(np.int32)
# print(dt)

#int8，int16，int32，int64 可替换为等价的字符串 'i1'，'i2'，'i4'，以及其他。
# dt = np.dtype('i4')
# print(dt)


'''
    结构化数据类型
'''
dt = np.dtype([('age',np.int8)])
print(dt)

#将结构化数据应用于ndarray对象
# dt = np.dtype([('age',np.int8)])
# a = np.array([(10,),(20,),(30,)],dtype = dt)
# print(a)


#访问age列内容
# dt = np.dtype([('age','i1')])
# a = np.array([(10,),(20,),(30,)],dtype = dt)
# print(a['age'])


#结构化数据包含多个字段
student = np.dtype([('name','S20'),('age','i1'),('marks','f4')])
a = np.array([('joe',20,80),('susan',22,85),('tom',23,90),('fank',23,33)],dtype=student)
print(a)
print(a['name'])

'''
每个内建类型都有一个唯一定义它的字符代码：

'b'：布尔值

'i'：符号整数

'u'：无符号整数

'f'：浮点

'c'：复数浮点

'm'：时间间隔

'M'：日期时间

'O'：Python 对象

'S', 'a'：字节串

'U'：Unicode

'V'：原始数据(void)

'''