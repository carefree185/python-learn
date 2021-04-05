# -*- coding:utf-8 -*-
import numpy as np

'''
    常用一元函数
'''
print('**************常用一元函数************************')

print()
print('abs绝对值函数：')
#abs fabs计算整数、浮点数或者复数的绝对值，对于非复数，可以使用更快的fabs
num = np.random.randn(6).reshape(2,3)
print(num)
print(np.abs(num))
print(np.fabs(num))

'''
    sqrt()计算各个元素的平方根，相当于arr ** 0.5， 要求arr的每个元素必须是非负数
'''
print()
print('sqrt计算各个元素的平方根：')
num = np.random.randint(1,7,size = (2,3))
print(num)
print(np.sqrt(num))
print()

'''
   square()计算各个元素的平方，相当于arr ** 2
'''
print()
print('sqrt计算各个元素的平方根：')
num = np.random.randint(1,7,size = (2,3))
print(num)
print(np.square(num))

'''
   exp()计算各个元素的指数e的x次方
'''
print()
print('exp计算各个元素的指数e的x次方：')
'''
    自然底数e： e ≈ 2.71828 。。。
'''
num = np.random.randint(1,7,size = (2,3))
print(num)
print(np.exp(num))



'''
   log()分别计算自然对数、底数为10的log、底数为2的log以及log(1+x)；
   要求arr中的每个元素必须为正数
'''
print()
print('log()计算自然对数：')

num = np.random.randint(1,7,size = (2,3))
print(num)
print(np.log(num))  #以e为底数 根据数组的元素 来求得e指数



'''
   sign()计算各个元素的正负号: 1 正数，0：零，-1：负数

'''
print()
print('sign()计算各个元素的正负号：')

num = np.random.randint(1,7,size = (2,3))
print(num)
print(np.sign(num))

'''
    四舍五入函数
    这个函数返回四舍五入的所需精度的值，
    numpy.around(a,decimals)
    a:输入的数组
    decimals:要舍入的小数位，默认值位0，负数讲四舍五入到小数点左侧位置
'''
print()
print('******************* 四舍五入函数*******************')
aro = np.array([1.0,5.56,11,0.567,35.543])
print('原数组：')
print(aro)
print(np.around(aro))
print(np.around(aro,1))
print(np.around(aro,-1))
print('**************************************')
print()

print()
print('**************************************')
#向下取整
print('向下取整')
afl = np.array([-1.7,  1.5,  -0.2,  0.6,  10])
print(np.floor(afl))
print('**************************************')
print()

print()
print('**************************************')
#向下取整
print('向上取整')
afl = np.array([-1.7,  1.5,  -0.2,  0.6,  10])
print(np.ceil(afl))
print('**************************************')
print()


'''
   modf()将数组中元素的小数位和整数位以两部分独立数组的形式返回
'''
print()
print('modf函数：')
#将将数组中元素的小数位和整数位以两部分独立数组的形式返回
num = np.random.random(6).reshape(2,3)
print(num)
print(np.modf(num))


'''
   isnan()返回一个表示“那些值是NaN(不是一个数字)”的布尔类型数组
'''
print()
print('isnan函数：')
num = np.random.random(6).reshape(2,3)
print(num)
print(np.isnan(num))


'''
   isfinite()、isinf()
   分别一个表示”那些元素是有穷的(非inf、非NaN)”或者“那些元素是无穷的”的布尔型数组
'''
print()
print('isfinite函数：')
#将将数组中元素的小数位和整数位以两部分独立数组的形式返回
num = np.random.random(6).reshape(2,3)
print(num)
print(np.isfinite(num))
print(np.isinf(num))

'''
    numpy包含大量的各种数学运算功能。NumPy日工标准的三角函数。算数运算的函数，附属处理函数等
'''
print('****************三角函数**********************')
#三角函数
#Numpy拥有标准的三角函数，它为弧度制单位的给定角度返回三角函数比值
a = np.array([0,30,45,60,90])
print('不同角度的正弦值：')
#通过pi/180 转化为弧度
print(np.sin(a*np.pi/180))
print('不同角度的余弦值：')
print(np.cos(a*np.pi/180))
print('不同角度的正切值：')
print(np.tan(a*np.pi/180))
print('**************************************')

a = np.array([0,20,45,60,90])
print('不同角度的正弦值：')
#通过pi/180 转化为弧度
sin = np.sin(a*np.pi/180)
print(sin)
print('不同角度的反正弦值：')
print(np.arcsin(sin))

print('不同角度的余弦值：')
cos = np.cos(a*np.pi/180)
print(cos)
print('不同角度的反余弦值：')
print(np.arccos(cos))

print('不同角度的正切值：')
tan = np.tan(a*np.pi/180)
print(tan)
print('不同角度的反正切值：')
print(np.arctan(tan))

print(np.degrees(np.arctan(tan)))  #degrees获取角度
print()


print('****************二元函数**********************')
print()
'''
   mod()元素级的取模
'''
print()
print('mod函数：')
#将将数组中元素的小数位和整数位以两部分独立数组的形式返回
num1 = np.random.randint(15,22,size = (2,3))
num2 = np.random.randint(1,7,size = (2,3))
print(num1)
print(num2)
print(np.mod(num1,num2))
print()



'''
   dot()求两个数组的点积
'''
print()
print('dot函数：')
a = np.array([[1,2],[3,4]])
b = np.array([[11,12],[13,14]])
print(np.dot(a,b))
#点积的计算方式
#[[1*11+2*13,1*12+2*14],[3*11+4*13,3*12+4*14]]

num1 = np.random.randint(15,22,size = (2,3))
num2 = np.random.randint(1,7,size = (3,2))
print(num1)
print(num2)
print(np.dot(num1,num2))
print()


'''
   greater() 大于
   less()    小于
   equal()   等于
   执行元素级别的比较运算，最终返回一个布尔型数组
'''
print()
print('比较函数：')
num1 = np.random.randint(1,7,size = (2,3))
num2 = np.random.randint(1,7,size = (2,3))
print(num1)
print(num2)
print('大于，大于等于')
print(np.greater(num1,num2))
print(np.greater_equal(num1,num2))
print('小于，小于等于')
print(np.greater(num1,num2))
print(np.greater_equal(num1,num2))
print('等于，不等于')
print(np.equal(num1,num2))
print(np.not_equal(num1,num2))
print()


'''
   logical_and() 
   logical_or()    
   logical_xor()   
   执行元素级别的布尔逻辑运算，相当于中缀运算符&、|、^
'''
print()
print('逻辑函数：')
num1 = np.random.randint(1,7,size = (2,3))
num2 = np.array([[1,0,0],[1,0,1]])
print(num1)
print(num2)
print('and:') #两者皆为 Ture
print(np.logical_and(num1,num2))
print('or:')  #两者有一个为True 返回Ture
print(np.logical_or(num1,num2))
print('xor:') #两者不同返回 Ture 否则返回false
print(np.logical_xor(num1,num2))
print()

'''
   power()对数组中的每个元素进行给定次数的指数值，类似于: arr ** 3
'''
print()
print('power函数：')
num1 = np.random.randint(1,7,size = (2,3))
print(num1)
print(np.power(num1,2))
print()

