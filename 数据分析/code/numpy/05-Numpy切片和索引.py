# -*- coding:utf-8 -*-
import numpy as np

'''
    ndarray 对象的内容可以通过索引或者切片来访问和修改，就像python的内置容器对象一样
    ndarray对象中的元素遵循基于零的索引。有三种行可用的索引方法类型：
        字段访问
        基本切片
        高级索引
'''
# arr = np.arange(10)
# arr2 = arr[2:7:2]
# print(arr2)

# arr=np.array([
#         [
#             [1,2,3,4],
#             [2,3,4,5],
#             [3,4,5,6]
#         ],
#         [
#             [10,20,30,40],
#             [20,30,40,50],
#             [30,40,50,60]
#         ]
#     ])
# print(arr[1])
# print(arr[1][1])
# print(arr[1][1][2])

#取40 50
# print(arr[1][1][2:])
# print(arr[1,1,2:])

# print(arr[1][:][0:2])  #获取第二维所有的数据加第三维的第一第二个数据失败
# print(arr[1,:,0:2])    #获取成功



'''
    NumPy - 高级索引  花式索引
    如果一个ndarray是非元组序列，数据类型为整数或布尔值的ndarray，或者至少一个元素为序列对象的元组，
    我们就能够用它来索引ndarray。高级索引始终返回数据的副本。 与此相反，切片只提供了一个视图。
    整数索引
    这种机制有助于基于 N 维索引来获取数组中任意元素。 每个整数数组表示该维度的下标值。 
    当索引的元素个数就是目标ndarray的维度时，会变得相当直接。
'''
a = np.arange(9).reshape(3,3)
print(a)
# a[[0,1,2],[0,1,2]] = 9
# num = a[[0,1,2],[0,1,2]]
#使用索引器 np.ix_()
num = a[np.ix_([0,1,2],[0,1])]
print(num)
# print(a)
# num2 = a[[[0,0],[2,2]],[[0,2],[0,2]]]
# print(num2)


# arr = np.arange(18).reshape(2,3,3)
# print(arr)
# arr[...,[0,1,2],[0,1,2]] = 9
#num = arr[[0,1],[0,1,2],[0,1,2]]
# num = arr[...,[0,1,2],[0,1,2]]

#使用索引器
# num = arr[[0,1],[0,1,2],[0,1]]
# num = arr[np.ix_([0,1],[0,1,2],[0,1])]
# num[:,[0]] = 99
# print(num)
# print(arr)

'''
    布尔索引
    当结果对象是布尔运算的结果是，将使用此类型的高级索引
'''
# arr = np.arange(12).reshape(4,3)
# print(arr)
# print('大于五的元素是：')
# print(arr[arr>5])

names = np.array(['joe','susan','tom'])
scores = np.array([
    [98,86,88,90],
    [70,86,90,99],
    [82,88,89,86]
])
classic = np.array(['语文','数学','英语','科学'])
print('susan的成绩是:')
# print(names=='susan')
print(scores[names=='susan'])

print('susan的数学成绩:')
# print(scores[names=='susan',classic=='数学'])
print(scores[names=='susan'].reshape(-1,)[classic=='数学'])

print('joe和susan的成绩是：')
print(scores[(names=='joe')|(names=='susan')])

print('非joe和susan的成绩')
print(scores[(names!='joe')&(names!='susan')])

'''
    数组转置与轴对换
'''
arr = np.arange(24).reshape(2,3,4)
print(arr.shape)
# print(np.transpose(arr))
#print(arr.transpose())
print(arr.T)


