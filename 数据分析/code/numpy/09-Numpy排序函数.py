# -*- coding:utf-8 -*-
import numpy as np
'''
    NumPy中提供了各种排序相关功能。 这些排序函数实现不同的排序算法，
    每个排序算法的特征在于执行速度，最坏情况性能，所需的工作空间和算法的稳定性。 
    下表显示了三种排序算法的比较：
    种类	                速度  	最坏情况	    工作空间	    稳定性
    'quicksort'(快速排序)	 1	    O(n^2)	       0	      否
    'mergesort'(归并排序)	 2	    O(n*log(n))    ~n/2	      是
    'heapsort'(堆排序)	 3	    O(n*log(n))	   0	      否
'''

'''
    numpy.sort()
    函数返回输入数组的排序副本
    numpy.sort(a,axis,kind,order)
    a :要排序的函数
    axis：压着它排序数组的轴，如果没有数组会被展开，沿着最后的轴排序
    kind:默认为’quicksort’快速排序
    order：如果数组包含字段，则是要排序的字段
'''

arr = np.array([[3,7],[9,1]])
print('我们的数组是:')
print(arr)
print('调用sort排序:')
print(np.sort(arr))
print('沿轴0排序')
print(np.sort(arr,axis = 0)) #按列排序
print(' sort 函数中排序字段')
# 在 sort 函数中排序字段
dt = np.dtype([('name',  'S10'),('age',  int)])
a = np.array([("raju",21),("anil",25),("ravi",  17), ("amar",27)], dtype = dt)
print('我们的数组是:')
print(a)
print(a['name'])
print('调用sort 按 name字段排序:')
print(np.sort(a,order = 'name'))
print('调用sort 按 age字段排序:')
print(np.sort(a,order = 'age'))








