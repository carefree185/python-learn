# -*- coding:utf-8 -*-
import numpy as np


'''
    在执行函数时，其中一些返回输入数组的副本，而另一些返回视图。当物理存储在
    另一位置时，称为副本，另一方面，如果提供了相同内存内容的我们将其称为视图
'''

'''
    无复制
    简单的赋值不会创建对象的副本。相反，它使用原始数组的相同id()来访问它。
    id()返回python对象的同用标识符，类似于C中的指针
'''

arr = np.arange(6)
print('原数组：')
print(arr)
print('查看原数组的ID:')
print(id(arr))
print('将原数组赋值给brr')
brr = arr
print('brr的id与arr的相同:')
print(id(brr))
print('修改brr的形状arr的也会随之改变：')
brr.shape = (2,3)
print('brr:')
print(brr)
print('arr:')
print(arr)
print()
'''
    视图或浅复制
    NUmpy拥有ndarray.view()方法它是一个新的数组对象，并课查看原始数据的相同数据。与前一种
    情况不同，新数组的位数更改不会影响原始数据的维数
    数组的切片也会创建视图
'''
print('------------------视图或浅复制--------------------')
arr = np.arange(6).reshape(2,3)
print('原数组：')
print(arr)
print('查看原数组的ID:')
print(id(arr))
print('创建arr的视图brr，brr = arr.view()')
brr = arr.view()
print('brr的id与arr的不相同:')
print(brr)
print(id(brr))
print('修改brr的形状arr的不会改变，但是更改brr里面的值arr的也会改变：')
brr.shape = (3,2)
brr[0,0] = 10
print('brr:')
print(brr)
print('arr:')
print(arr)
print()

'''
    副本深复制
    ndarray.copy()函数创建一个深层副本。 它是数组及其数据的完整副本，不与原始数组共享。   
'''
print('------------------副本深复制--------------------')
arr = np.array([[4,5],[6,7],[8,9]])
print('原数组：')
print(arr)
print('查看原数组的ID:')
print(id(arr))
print('创建arr的副本，brr = arr.copy()')
brr = arr.copy()
print('brr的id与arr的不相同:')
print(brr)
print(id(brr))
print('修改brr的值arr的不会改变：')
brr[0,0] = 10
print('brr:')
print(brr)
print('arr:')
print(arr)
print()





