# 一、简介

### 什么是数据分析? 
数据分析是指用适当的**统计分析方法**对收集来的大量数据进行分析，
**提取有用信息和形成结论**而**对数据加以详细研究和概括总结**的过程。

### 使用python做数据分析的常用库
1. `numpy`基础数值算法
2. `scipy`科学计算
3. `matplotlib`数据可视化
4. `pandas`序列高级函数

### numpy简介
1. `Numerical Python`，数值的`Python`，补充了`Python`语言所欠缺的数值计算能力。
2. `Numpy`是其它数据分析及机器学习库的底层库。
3. `Numpy`完全标准`C`语言实现，运行效率充分优化。
4. `Numpy`开源免费。

### numpy的核心: 多维数组
1. 代码简洁：减少`Python`代码中的循环。
2. 底层实现：厚内核(`C`)+薄接口(`Python`)，保证性能。

# 二、numpy基础

`numpy`提供了一个多维数组对象`ndarray`，使用`np.array()`进行构造

```python
import numpy as np

ary = np.array([1, 2, 3, 4, 5, 6])
print(ary, type(ary))  # [1 2 3 4 5 6] <class 'numpy.ndarray'>
```
### 内存中的`ndarray`对象

`ndarry`对象创建出来后，在内存中保存了两部分数据信息，**元数据**和**实际数据**

* 元数据(`metadata`): 存储对目标数组的**描述信息**，如：
  * `dim`: 维数
  * `shape`: 数据形状
  * `size`: 数据量
  * `dimensions`: 规模
  * `dtype`: 数据类型
  * `data`: 实际数据所在地址

* 实际数据: 完整的数组数据

将实际数据与元数据分开存放，**一方面提高了内存空间的使用效率，
另一方面减少对实际数据的访问频率，提高性能**

### 特点
1. `Numpy`数组是同质数组，即**所有元素的数据类型必须相同**

## 2.1 ndarray数组初体验

数组与一个数进行**四则运算**时，**运算规则是作用在数组的每个元素之上**。
```python
import numpy as np

ary = np.array([1, 2, 3, 4, 5, 6])
# 原始数据
print("原始数据    ", ary)      # 原始数据     [1 2 3 4 5 6]
# 加法
print("原始数据 + 2", ary + 2)  # 原始数据 + 2 [3 4 5 6 7 8]
# 减法
print("原始数据 - 2", ary - 2)  # 原始数据 - 2 [-1  0  1  2  3  4]
# 乘法
print("原始数据 * 2", ary * 2)  # 原始数据 * 2 [ 2  4  6  8 10 12]
# 除法
print("原始数据 / 2", ary / 2)  # 原始数据 / 2 [0.5 1.  1.5 2.  2.5 3. ]
# 幂运算
print("原始数据 ** 2", ary ** 2)# 原始数据 ** 2 [ 1  4  9 16 25 36]
# 取模
print("原始数据 % 2", ary % 2)  # 原始数据 % 2 [1 0 1 0 1 0]
```

数组与一个数做**比较运算**，**运算规则作用在每个元素之上**
```python
import numpy as np

ary = np.array([1, 2, 3, 4, 5, 6])
# 比较
print("原始数据 > 3", ary > 3)
print("原始数据 < 3", ary < 3)
print("原始数据 == 3", ary == 3)
print("原始数据 != 3", ary != 3)
```
输出结果为:
```
原始数据 > 3 [False False False  True  True  True]
原始数据 < 3 [ True  True False False False False]
原始数据 == 3 [False False  True False False False]
原始数据 != 3 [ True  True False  True  True  True]
```

数组与数组**运算**时，**运算规则作用在相同索引位置的元素之上**, **两个数组的维度必须一致**
```python
import numpy as np

ary = np.array([1, 2, 3, 4, 5, 6])

# 数组与数组进行运算
ary1 = ary
ary2 = np.array([7, 8, 9, 10, 11, 12])

print("ary1 + ary2", ary1 + ary2)
print("ary1 - ary2", ary1 - ary2)
print("ary1 * ary2", ary1 * ary2)
print("ary1 / ary2", ary1 / ary2)
print("ary1 % ary2", ary1 % ary2)
print("ary1 ** ary2", ary1 ** ary2)
print("ary1 > ary2", ary1 > ary2)
print("ary1 < ary2", ary1 < ary2)
```

## 2.2 创建`ndarray`对象
### 2.2.1 np.array(args: Any)
通过传入的参数构造一个数组，该参数可以时python的`list`，`tuple`等其他的数据类型
```python
import numpy as np

ary = np.array([1, 2, 3, 4, 5, 6])
print(ary)
```

### 2.2.2 np.arange(start, end, step)
生成一个有规律的元素数组
* `start`, 起始值，默认为0
* `end`, 终止值，生成的值不包含该值
* `step`, 步长，默认为1

```python
import numpy as np
ary = np.arange(0, 10, 2)
print(ary)
```

### 2.2.3 np.zeros(number, dtype)
生成一个元素全为`0`数组
* `number`, 元素个数, 或`shape`
* `dtype`, 数据类型

```python
import numpy as np

np.zeros(10, dtype=np.int8)
np.zeros(10, dtype=np.float16)
```

### 2.2.4 np.ones(number, dtype)
生成一个元素全为`1`的数组
* `number`, 元素个数, 或`shape`
* `dtype`, 数据类型

```python
import numpy as np

np.ones(10, dtype=np.int8)
np.ones(10, dtype=np.float16)
```

### 2.2.5 np.zeros_link(a:[ndarry, iterable, int, float], dtype)
生成一个形状像`a`数据元素全为`0`的数组
* `a`: ndarry对象，可迭代对象，int或float数据值
* `dtype`: 数据类型
  
```python
import numpy as np
np.zeros_like([1,2,3,4])
```

### 2.2.6 np.ones_like(a:[ndarray, iterable, int, float], dtype)
生成一个形状像`a`数据元素全为`1`的数组
* `a`: ndarry对象，可迭代对象，int或float数据值
* `dtype`: 数据类型

```python
import numpy as np
np.ones_like([1,2,3,4])
```

## 2.3 `ndarray`对象的属性基础访问
* 维度
* 形状
* 数据类型
* 数据元素个数
* 索引

### 2.3.1 `np.ndarray.ndim`维数
```python
import numpy as np

ary = np.arange(1, 11)
print(ary.ndim)  # 1

ary = np.array([
  [1,2,3],
  [4,5,6]
])
print(ary.ndim)  # 2
```
* `np.ndarray.ndim`: 返回`array`的维数

### 2.3.2 `np.ndarray.shape`维度
返回的数据维度，也即是**数据的行列数**
```python
import numpy as np
ary = np.arange(1, 11)
print(ary, ary.shape)  # [ 1  2  3  4  5  6  7  8  9 10] (10,)

ary = np.array([
  [1,2,3],
  [4,5,6]
])
print(ary, ary.shape)  # ary，(2, 3)
```
* `np.ndarray.shape`: 是一个元组, 表示数组的形状，可以进行修改

### 2.3.3 `np.ndarray.size`数据元素个数
该属性存放的是**数组数据元素的个数**，等于`shape`元组元素的乘积
```python
import numpy as np
ary = np.array([
    [1,2,3,4],
    [5,6,7,8]
])
# 观察维度，size，len的区别
print(ary.shape, ary.size, len(ary))  # (2, 4) 8 2
```
* `array.size`: 返回的数组元素个数
* `len(array)`: 返回的是最外层元素个数

### 2.3.4 `np.ndarray.dtype`数据类型
该属性存放的是**数组元素的数据类型**
```python
import numpy as np
ary = np.array([1, 2, 3, 4, 5, 6])
print(type(ary), ary, ary.dtype)
# 转换ary元素的类型
b = ary.astype(float)
print(type(b), b, b.dtype)
#转换ary元素的类型
c = ary.astype(str)
print(type(c), c, c.dtype)
```
* **不能对该属性进行直接修改**, 不同类型的数据在底层处理是不一样的。 修改数据类型需要调用
  `array.astype(dtype)`方法转换数据类型。
  
* `array.astype(dtype)`: 将数组元素的数据类型转为`dtype`指定的类型；
  **不会改变原有数组，只会生成一个新的数组**

### 2.3.5 索引

`array[..., 页号, 行号, 列号]`, 从最外层像最里层寻找。

每层索引从0开始到每层数组的长度`len-1`

```python
import numpy as np
a = np.array([[[1, 2],
               [3, 4]],
              [[5, 6],
               [7, 8]]])
print(a, a.shape)

print(a[0])

print(a[0][0])
print(a[0, 0])

print(a[0][0][0])
print(a[0,0,0])
```

## 2.4 `ndarray`对象的数据类型

### 2.4.1 numpy内部的基本数据类型
| 类型名       | 类型表示符                           | 说明|
| :---------: | :-------------------------------:  |:---:|
| 布尔型       | `bool_`                            ||
| 有符号整数型  | `int8(-128~127)` `int16` `int32` `int64`  |后面的数字表示占用的二进制位|
| 无符号整数型  | `uint8(0~255)` `uint16` `uint32` `uint64` |后面的数字表示占用的二进制位|
| 浮点型       | `float16` `float32` `float64 `          |后面的数字表示占用的二进制位|
| 复数型       | `complex64` `complex128`              |后面的数字表示占用的二进制位，实部虚部各占一半|
| 字串型       | `str_` |每个字符用`32`位`Unicode`编码表示|

### 2.4.2 自定义符合类型
将复杂的数据结构存放到`ndarray`中

#### 第一种方式设置`dtype`
```python
import numpy as np

data=[
	('zs', [90, 80, 85], 15),
	('ls', [92, 81, 83], 16),
	('ww', [95, 85, 95], 15)
]

a = np.array(data, dtype='U3, 3int32, int32')
print(a)
```
#### 第二种方式设置`dtype`
额外设置每一列数据的别名。给`dtype`指定一个列表，元素为一个个三元组
`<别名, 数据类型, 元素个数>`

```python
import numpy as np

data=[
	('zs', [90, 80, 85], 15),
	('ls', [92, 81, 83], 16),
	('ww', [95, 85, 95], 15)
]

b = np.array(data, dtype=[('name', 'str_', 2),
                    ('scores', 'int32', 3),
                    ('ages', 'int32', 1)])
print(b[0]['name'], ":", b[0]['scores'])
```

#### 第三种方式设置`dtype`
以字典的形式设置`dtype`
```python
dtype = {'names': ['name', 'scores', 'ages'],
        'formats': ['U3', '3int32', 'int32']}
```
* `names`: 设置每一列别名
* `formats`: 每一列的数据类型

**这两个字段不能改变的**

```python
import numpy as np

data=[
	('zs', [90, 80, 85], 15),
	('ls', [92, 81, 83], 16),
	('ww', [95, 85, 95], 15)
]

c = np.array(data, dtype={'names': ['name', 'scores', 'ages'],
                    'formats': ['U3', '3int32', 'int32']})
print(c[0]['name'], ":", c[0]['scores'], ":", c.itemsize)
```

#### 第四种方式设置`dtype`
以字典的形式设置`dtype`
```python
dtype = {'name': ('U3', 0),
         'scores': ('3i4', 16),
         'age': ('i4', 28)}
```
* 以列的别名为键
* 以一个二元组`<数据类型, 偏移字节数>`为值
  * `偏移字节`，从该位置开始输出数据
  
```python
import numpy as np

data=[
	('zs', [90, 80, 85], 15),
	('ls', [92, 81, 83], 16),
	('ww', [95, 85, 95], 15)
]

d = np.array(data, dtype={'name': ('U3', 0),
                    'scores': ('3i4', 16),
                    'age': ('i4', 28)})
print(d[0]['name'], d[0]['scores'], d.itemsize)
```

#### 第五种方式设置`dtype`

```python
dtype = ('u2', {'lowc': ('u1', 0),
                'hignc': ('u1', 1)})
```

```python
import numpy as np

e = np.array([0x1234, 0x5667],
             dtype=('u2', {'lowc': ('u1', 0),
                           'hignc': ('u1', 1)}))
print('%x' % e[0])
print('%x %x' % (e['lowc'][0], e['hignc'][0]))
```


#### 日期类型
```python
import numpy as np

f = np.array(['2011', '2012-01-01', '2013-01-01 01:01:01',
              '2011-02-01'])
f = f.astype('M8[D]')  # M8：datetime64, [D]：精确到天

print(f[3]-f[0])  # 时间日期的计算
```

### 2.4.3 类型字符码
对于`numpy`的数据类型, 可以有简写的形式如下表

| 类型                 | 字符码                                 |
| :---------------:   | :----------------------------------:  |
| `np.bool_`          | `?`                                   |
| `np.int8/16/32/64`  | `i1/i2/i4/i8`                         |
| `np.uint8/16/32/64` | `u1/u2/u4/u8`                         |
| `np.float/16/32/64` | `f2/f4/f8`                            |
| `np.complex64/128`  | `c8/c16`                              |
| `np.str_`           | `U<字符数>`                            |
| `np.datetime64`     | `M8[Y] M8[M] M8[D] M8[h] M8[m] M8[s]` |

**字节序前缀，用于多字节整数和字符串**

`< >  =` 分别表示小端 大端 硬件字节序

**类型字符码格式**

`<字节序前缀><维度><类型><字节数或字符数>`

|类型字符码格式| 释义                                                         |
| :-------: | :---------------------------------------------------------: |
| `3i4`      | 大端字节序，`3`个元素的一维数组，每个元素都是整型，每个整型元素占`4`个字节。    |
| `<(2,3)u8` | 小端字节序，`6`个元素`2`行`3`列的二维数组，每个元素都是无符号整型，每个无符号整型元素占`8`个字节。 |
| `U7`       | 包含7个字符的`Unicode`字符串，每个字符占`4`个字节，采用默认字节序。 |

## 2.5 `ndarray`对象的维度
`ndarray.shape`表示数据的视图，也即是数据的组织形状。可以直接修改该属性值
达到变维目的。

`ndarray.resize(shape)`可以达到变维目的，同修改`ndarray.shape`一致

### 2.5.1 视图变维
特点，**数据共享**
> 也即是，当变维后的数组数据发生修改，变维前的数组数据也相应的发生修改

#### ndarray.reshape(shape)
将原数组的维度变维合理的任何维度
> 返回的是一个新的数组，原数组不会发生变化

```python
import numpy as np
a = np.arange(1, 9)
print(a)		# [1 2 3 4 5 6 7 8]

b = a.reshape(2, 4)	#视图变维  : 变为2行4列的二维数组
print(b)
b[0, 0]=10
print("修改b", b)
print("修改b后的a", a)
```

#### ndarray.ravel()
将原数组变成一维数组
> 撑平数组，返回一个新数组，原数组不会发生变化

```python
import numpy as np
a = np.arange(1, 9)
print(a)		# [1 2 3 4 5 6 7 8]

b = a.reshape(2, 4)	#视图变维  : 变为2行4列的二维数组

c = b.ravel()	#视图变维	变为1维数组
print(c)
```

### 2.5.2 复制变维
特点，**数据独立**
> 也即是，当变维后的数组数据发生修改，变维前的数组数据不会发生相应的修改

#### ndarray.flatten()
```python
import numpy as np
a = np.arange(1, 9)		# [1 2 3 4 5 6 7 8]

b = a.reshape(2, 4)	#视图变维  : 变为2行4列的二维数组

e = b.flatten()  # 复制变维
print("e", e)
a += 10   # a中的每个元素加10
print("a", a,"\n","b", b, "\n","e", e)  # a发生变化，b同时发生变化，e不发生变化
```

## 2.6 `ndarray`数组切片
* 数组对象切片的参数设置与列表切面参数类似
  * `步长+`：默认切从首到尾
  * `步长-`：默认切从尾到首
  
* `ndarray[start:end:step, ...]`
  * 对给个维度指定`start:end:step`就可以达到切片目的
* 默认位置步长：`1`

### 2.6.1 一维数组切片
**一位数组切片和列表切片操作一致**。
```python
import numpy as np
a = np.arange(1, 10)
print("{:15}".format("a:"), a) # 1,2,...,9
print("{:15}".format('a[:3]:'), a[:3]) # 1,2,3
print("{:15}".format('a[3:6]:'), a[3:6]) # 4,5,6
print("{:15}".format('a[6:]:'), a[6:]) # 7, 8, 9
print("{:15}".format('a[::-1]:'), a[::-1]) # 反序
print("{:15}".format('a[:-4:-1]:'), a[:-4:-1]) # 9, 8, 7
print("{:15}".format('a[-4:-7:-1]:'), a[-4:-7:-1]) # 6, 5, 4
print("{:15}".format('a[-7::-1]:'), a[-7::-1]) # 3 2 1
print("{:15}".format('a[::]:'), a[::]) # 1 2 3 4 5 6 7 8 9
print("{:15}".format('a[:]:'), a[:]) # 1 2 3 4 5 6 7 8 9
```
### 2.6.2 多为数组切片

```python
import numpy as np
a = np.arange(1, 10)
a.resize((3,3))
print(a)

print(a[:2,:2])  # 获取3*3二维数组的前两行和前两列
print(a[::2,:])  # 获取3*3二维数组的一三两行
print(a[::2,::2])  # 获取3*3二维数组的一三两行和一三两列
```

### 2.6.3 `ndarray`掩码操作
基于bool类型的掩码，**获取数组的对应掩码为`True`的子数组**
```python
import numpy as np

a = np.arange(1, 101)
mask = (a % 3 == 0) & (a % 7 == 0)
print(a[mask])
```
基于索引的掩码，**按照索引的排序输出数组中的元素**
```python
import numpy as np

names = np.array(['Apple', 'MI', 'Vivo', 'Oppo', 'HuaWei'])
rank = [1,4,0,3,2]
print(names[rank])
```

## 2.7 多维数组的组合与拆分
**组合**: 指将两个或多个数组在一定方向拼接成一个数组

**拆分**: 指将一个数组拆成多个**结构相同的数组**

### 2.7.1 垂直方向组合与拆分
* 垂直方向组合(`np.vstack((ndarray, ndarray, ...))`): 使得数组行增加，**两个组合的数组要求列必须相同** 
  * 参数是一个元组
* 垂直方向拆分(`np.vsplit(ndarray, num)`): 是的数组行减少，**将行平均才分为`n`份**
  * `ndarray`数组
  * `num`: 拆分成`num`个数组
```python
import numpy as np
a = np.arange(1, 7).reshape(2, 3)
b = np.arange(7, 13).reshape(2, 3)
print(a)
print(b)

# 垂直方向完成组合操作，生成新数组
c = np.vstack((a, b))
print(c)

# 垂直方向完成拆分操作，生成两个数组
d, e = np.vsplit(c, 2)
print(d)
print(e)
```

### 2.7.2 水平方向组合与拆分
* 水平方向组合(`np.hstack((ndarray, ndarray, ...))`): 使得数组列增加，**两个组合的数组要求行必须相同** 

* 水平方向拆分(`np.hsplit(ndarray, num)`): 是的数组列减少，**将列平均分为`n`份**

```python
import numpy as np
a = np.arange(1, 7).reshape(2, 3)
b = np.arange(7, 13).reshape(2, 3)
# 水平方向完成组合操作，生成新数组 
c = np.hstack((a, b))
# 水平方向完成拆分操作，生成两个数组
d, e = np.hsplit(c, 2)
```

### 2.7.3 深度方向组合与拆分

* 深度方向组合(`np.dstack((ndarray, ndarray, ...))`): 使得数组维数增加，**两个组合的数组要求行和列必须相同** 

* 深度方向拆分(`np.dsplit(ndarray, num)`)

```python
import numpy as np
a = np.arange(1, 7).reshape(2, 3)
b = np.arange(7, 13).reshape(2, 3)
# 深度方向（3维）完成组合操作，生成新数组
i = np.dstack((a, b))
# 深度方向（3维）完成拆分操作，生成两个数组
k, l = np.dsplit(i, 2)
```

### 2.7.4 高级组合与拆分

* 组合(`np.concatenate((ndarray, ndarray, ...), axis=0)`)
  * `(ndarray, ndarray, ...)`: 待组合的数组
  * `axis`: 组合方向
    * `0`: 垂直方向组合
    * `1`: 水平方向组合
    * `2`: 深度方向组合(要求，**待组合数组都必须为三维数组**)
  
* 拆分(`np.split(ndarray, num, axis=0)`)
  * `ndarray`: 带拆分的数组
  * `num`: 拆分为`num`个数组
  * `axis`: 才分方向
    * `0`: 垂直方向组合
    * `1`: 水平方向组合
    * `2`: 深度方向组合(要求，**待拆分数组都必须为三维数组**)

### 2.7.5 长度不等的数组组合
* 首先将数组填充到一致的长度
  * `np.pad(ndarray, pad_with, mode, mode_values)`
    * `ndarray`: 带填充数组
    * `pad_with`: 如何填充
    * `mode`: 填充模式
    * `values`: 填充值
* 然后在进行组合或是其他运算

```python
import numpy as np
a = np.array([1,2,3,4,5])
b = np.array([1,2,3,4])
# 填充b数组使其长度与a相同,头部添加0个元素，尾部添加1个元素
b = np.pad(b, pad_width=(0, 1), mode='constant', constant_values=-1)
print(b)
# 垂直方向完成组合操作，生成新数组
c = np.vstack((a, b))
print(c)
```

### 2.7.6 简单的一维数组组合
把两个数组摞在一起成两行: `np.row_stack((a, b))`

把两个数组组合在一起成两列: `np.column_stack((a, b))`

```python
import numpy as np
a = np.arange(1,9)		#[1, 2, 3, 4, 5, 6, 7, 8]
b = np.arange(9,17)		#[9,10,11,12,13,14,15,16]
# 把两个数组摞在一起成两行
c = np.row_stack((a, b))
print(c)
# 把两个数组组合在一起成两列
d = np.column_stack((a, b))
print(d)
```

## 2.8 `ndarray`其他属性

- `shape`: 维度
- `dtype`: 元素类型
- `size`: 元素数量
- `ndim`: 维数，`len(shape)`
- `itemsize`: 元素字节数
- `nbytes`: 总字节数 = `size x itemsize`
- `real`: 复数数组的实部数组
- `imag`: 复数数组的虚部数组
- `T`: 数组对象的转置视图
- `flat`: 扁平迭代器

```python
import numpy as np
a = np.array([[1 + 1j, 2 + 4j, 3 + 7j],
              [4 + 2j, 5 + 5j, 6 + 8j],
              [7 + 3j, 8 + 6j, 9 + 9j]])
print(a.shape)
print(a.dtype)
print(a.ndim)
print(a.size)
print(a.itemsize)
print(a.nbytes)
print(a.real, a.imag, sep='\n')
print(a.T)
print([elem for elem in a.flat])
b = a.tolist()
print(b)
```

