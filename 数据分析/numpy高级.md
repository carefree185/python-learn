# numpy常用函数

## 一 加载文件

numpy提供了函数用于加载逻辑上可被解释为二维数组的文本文件，格式如下:
```
数据项1 <分隔符> 数据项2 <分隔符> ... <分隔符> 数据项n
例如：
AA,AA,AA,AA,AA
BB,BB,BB,BB,BB
...
或：
AA:AA:AA:AA:AA
BB:BB:BB:BB:BB
...
```

**`np.loadtxt()`接口用于读取文本数据**具体接口如下
```python
import numpy as np
# 直接读取该文件并且获取ndarray数组对象 
# 返回值：
#     unpack=False：返回一个二维数组
#     unpack=True： 多个一维数组
np.loadtxt(
    '../aapl.csv',			# 文件路径
    delimiter=',',			# 分隔符
    usecols=(1, 3),			# 读取1、3两列 （下标从0开始）
    unpack=False,			# 是否按列拆包
    dtype='U10, f8',		# 制定返回每一列数组中元素的类型
    converters={1:'func'}		# 转换器函数字典
)   
```

**案例，读取`aapl.csv`文件内容**
```python
import numpy as np
from datetime import datetime
# 日期转换函数
def dmy2ymd(dmy):
    # 将日-月-年 转为 年-月-日
	dmy = str(dmy, encoding='utf-8')
	time = datetime.strptime(dmy, '%d-%m-%Y').date()
	t = time.strftime('%Y-%m-%d')
	return t

data = np.loadtxt('./data/aapl.csv',  # 读取文件
                  delimiter=',',  # 分隔符
                  usecols=(1, 3, 4, 5, 6),  # 要读取的列
                  dtype='M8[D], f8, f8, f8, f8',  # 每个维度的数据类型
                  unpack=True,  # 拆包
                  converters={1: dmy2ymd}  # 自定第几列使用的转换函数
                  )
print(data)
```

**案例，绘制苹果股票收盘价的折线图**
```python
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
# 日期转换函数
def dmy2ymd(dmy):
    # 将日-月-年 转为 年-月-日
	dmy = str(dmy, encoding='utf-8')
	time = datetime.strptime(dmy, '%d-%m-%Y').date()
	t = time.strftime('%Y-%m-%d')
	return t

dates, opening_prices,highest_prices, \
	lowest_prices, closeing_prices  = np.loadtxt('./data/aapl.csv',  # 读取文件
                  delimiter=',',  # 分隔符
                  usecols=(1, 3, 4, 5, 6),  # 要读取的列
                  dtype='M8[D], f8, f8, f8, f8',  # 每个维度的数据类型
                  unpack=True,  # 拆包
                  converters={1: dmy2ymd}  # 自定第几列使用的转换函数
                  )
# print(data)
plt.figure('APPL K', facecolor='lightgray')
plt.title('APPL K')
plt.xlabel('Day', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.grid(linestyle=':')

#拿到坐标轴
ax = plt.gca()
#设置主刻度定位器为周定位器（每周一显示主刻度文本）
ax.xaxis.set_major_locator( md.WeekdayLocator(byweekday=md.MO) )
ax.xaxis.set_major_formatter(md.DateFormatter('%d-%b-%Y'))
#设置次刻度定位器为日定位器
ax.xaxis.set_minor_locator(md.DayLocator())
plt.tick_params(labelsize=8)
dates = dates.astype(md.datetime.datetime)  # numpy数据类型转换

plt.plot(dates, closeing_prices, color='blue', linestyle='-.')
plt.gcf().autofmt_xdate()  # 自动格式话x轴日期
plt.show()
```

**案例，绘制苹果股票的k线图**
```python
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
# 日期转换函数
def dmy2ymd(dmy):
    # 将日-月-年 转为 年-月-日
	dmy = str(dmy, encoding='utf-8')
	time = datetime.strptime(dmy, '%d-%m-%Y').date()
	t = time.strftime('%Y-%m-%d')
	return t

dates, opening_prices,highest_prices, \
	lowest_prices, closeing_prices  = np.loadtxt('./data/aapl.csv',  # 读取文件
                  delimiter=',',  # 分隔符
                  usecols=(1, 3, 4, 5, 6),  # 要读取的列
                  dtype='M8[D], f8, f8, f8, f8',  # 每个维度的数据类型
                  unpack=True,  # 拆包
                  converters={1: dmy2ymd}  # 自定第几列使用的转换函数
                  )
# print(data)
plt.figure('APPL K', facecolor='lightgray')
plt.title('APPL K')
plt.xlabel('Day', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.grid(linestyle=':')

#拿到坐标轴
ax = plt.gca()
#设置主刻度定位器为周定位器（每周一显示主刻度文本）
ax.xaxis.set_major_locator( md.WeekdayLocator(byweekday=md.MO) )
ax.xaxis.set_major_formatter(md.DateFormatter('%d-%b-%Y'))
#设置次刻度定位器为日定位器
ax.xaxis.set_minor_locator(md.DayLocator())
plt.tick_params(labelsize=8)
dates = dates.astype(md.datetime.datetime)  # numpy数据类型转换

plt.gcf().autofmt_xdate()  # 自动格式话x轴日期

#绘制每一天的蜡烛图
#填充色：涨为白色，跌为绿色
rise = closeing_prices > opening_prices
color = np.array([('white' if x else 'limegreen') for x in rise])
#边框色：涨为红色，跌为绿色
edgecolor = np.array([('red' if x else 'limegreen') for x in rise])

#绘制线条
plt.bar(dates, highest_prices - lowest_prices, 0.1,
	lowest_prices, color=edgecolor)
#绘制方块
plt.bar(dates, closeing_prices - opening_prices, 0.8,
	opening_prices, color=color, edgecolor=edgecolor)

plt.show()
```

## 二 平均值

### 2.1 算术平均
算术平均值是对真实值的一种无偏估计

$$
s = [s_1, s_2,\cdots, s_n]\\ 
m = \frac{\sum_i^n s_i}{n}
$$
* `s`: 样本
* `m`: 样本的算术平均值

**`numpy`计算算术平均值api**
```python
import numpy as np
array = np.random.normal(10, 2, 100)
np.mean(array)  # 计算array的均值
array.mean()  # 计算array的算术平均值
```

**案例，计算aapl股票收盘价的算术平均值**
```python
import numpy as np
from datetime import datetime


# 日期转换函数
def dmy2ymd(dmy):
    # 将日-月-年 转为 年-月-日
    dmy = str(dmy, encoding='utf-8')
    time = datetime.strptime(dmy, '%d-%m-%Y').date()
    t = time.strftime('%Y-%m-%d')
    return t


closeing_prices = np.loadtxt('./data/aapl.csv',  # 读取文件
                             delimiter=',',  # 分隔符
                             usecols=(6,),  # 要读取的列
                             dtype='f8',
                             # 每个维度的数据类型
                             unpack=True,  # 拆包
                             # converters={1: dmy2ymd}
                             # 自定第几列使用的转换函数
                             )

mean = 0
for closing_price in closeing_prices:
    mean += closing_price
mean /= closeing_prices.size
print(mean)
mean = np.mean(closeing_prices)
print(mean)
```

### 2.2 加权平均

$$
s = [s_1, s_2, \cdots, s_n]\\ 
w = [w_1, w_2, \cdots, w_n]\\ 
a = \frac{\sum_i^n s_iw_i}{\sum_i^n w_i}
$$

* `s`: 样本
* `w`: 权重
* `a`: 加权平均值

**numpy计算加权平均值**
```python
import numpy as np
array = np.random.normal(10, 2, 100)
weights = np.random.random(100)
np.average(array, weights=weights)  # 计算加权平均值
```

**案例，计算股票的成交量加权平均价格**
* 成交量加权平均价格: 体现了市场对当前交易价格的认可度，更加的接近真实价格

```python
import numpy as np
closing_prices, volumes = np.loadtxt(
    './data/aapl.csv', delimiter=',',
    usecols=(6, 7), unpack=True)
vwap, wsum = 0, 0
for closing_price, volume in zip(
        closing_prices, volumes):
    vwap += closing_price * volume
    wsum += volume
vwap /= wsum
print(vwap)
vwap = np.average(closing_prices, weights=volumes)
print(vwap)
```

## 三 最值 中位数 标准差

### 3.1 最值

样本中的最大值和最小值

**`np.max() np.min() np.ptp()`** 返回一个数组中最大值/最小值/极差

```python
import numpy as np
# 产生9个介于[10, 100)区间的随机数
a = np.random.randint(10, 100, 9)
print(a)
print(np.max(a), np.min(a), np.ptp(a))
```

**`np.argmax() np.argmin()`** 返回一个数组中最大/最小元素的下标
```python
import numpy as np
# 产生9个介于[10, 100)区间的随机数
a = np.random.randint(10, 100, 9)
print(np.argmax(a), np.argmin(a))
```

**`np.maximum() np.minimum()`** 将两个同维数组中对应元素中最大/最小元素构成一个新的数组
```python
import numpy as np
# 产生9个介于[10, 100)区间的随机数
a = np.random.randint(10, 100, 9)
b = np.random.randint(100, 1000, 9)
print(np.maximum(a, b), np.minimum(a, b), sep='\n')
```
* 保留对于位置较大或者较小的元素，构成新的数组

**案例，股票波动性**
```python
import numpy as np
highest_prices, lowest_prices = np.loadtxt(
    './data/aapl.csv', delimiter=',',
    usecols=(4, 5), dtype='f8, f8', unpack=True)
max_price = np.max(highest_prices)
min_price = np.min(lowest_prices)
print(min_price, '~', max_price)
```

**案例，查看AAPL股票最大最小值的日期**，分析为什么这一天出现最大最小值
```python
import numpy as np
dates, highest_prices, lowest_prices = np.loadtxt(
    './data/aapl.csv', delimiter=',',
    usecols=(1, 4, 5), dtype='U10, f8, f8',
    unpack=True)
max_index = np.argmax(highest_prices)
min_index = np.argmin(lowest_prices)
print(dates[min_index], dates[max_index])
```
**案例，观察最高价与最低价的波动范围**，分析这支股票底部是否坚挺
```python
import numpy as np
dates, highest_prices, lowest_prices = np.loadtxt(
    './data/aapl.csv', delimiter=',',
    usecols=(1, 4, 5), dtype='U10, f8, f8',
    unpack=True)
highest_ptp = np.ptp(highest_prices)
lowest_ptp = np.ptp(lowest_prices)
print(lowest_ptp, highest_ptp)
```

### 3.2 中位数

将多个样本按照大小排序，取中间位置的元素。

**若样本数量为奇数，中位数为最中间的元素**

$[1, 2000, 3000, 4000, 10000000]$

**若样本数量为偶数，中位数为最中间的两个元素的平均值**

$[1,2000,3000,4000,5000,10000000]$

**numpy提供的中位数API**
```python
import numpy as np
array = np.arange(10, 20, 10)
size = array.size
sorted_array = np.msort(array)  # 排序

median = np.median(array)  # 计算中位数api
# 自己算
median = (sorted_array[int((size - 1) / 2)] + sorted_array[int(size / 2)]) / 2  # 计算中位数
```

**案例：分析中位数的算法**
```python
import numpy as np
closing_prices = np.loadtxt( './data/aapl.csv', 
	delimiter=',', usecols=(6, ), unpack=True)
size = closing_prices.size
sorted_prices = np.msort(closing_prices)
median = (sorted_prices[int((size - 1) / 2)] + sorted_prices[int(size / 2)]) / 2
print(median)
median = np.median(closing_prices)
print(median)
```

### 3.3 方差 标准差
现在获得样本数据$s=\[s_1, s_2, s_3,\cdots, s_n\]$，为了计算其标准差则要先计算其方差。


方差计算公式: $\sigma^2=\frac{(s_1 - \overline{s})^2 +...+(s_n - \overline{s})^2}{n}$
* $\overline{s}$: 表示`s`的平均值(期望)
    * 期望计算公式: $\overline{s}=\sum_i^n {s_ip_i}$, 其中$p_i$表示$s_i$出现的概率

标准差: $\sigma = \sqrt{\sigma^2}$

离差: $s_i - \overline{s}$: 离差和等于0

**标准差用于衡量数据的离散程度，标准差越小，数据离散程度越小，否则越大。**

**方差，标准差的相关计算**
```python
import numpy as np
closing_prices = np.loadtxt(
    './data/aapl.csv', delimiter=',', usecols=(6,), unpack=True)
# 自己计算
mean = np.mean(closing_prices)         # 算数平均值
devs = closing_prices - mean           # 离差
dsqs = devs ** 2                       # 离差方
pvar = np.sum(dsqs) / dsqs.size        # 总体方差
pstd = np.sqrt(pvar)                   # 总体标准差
svar = np.sum(dsqs) / (dsqs.size - 1)  # 样本方差
sstd = np.sqrt(svar)                   # 样本标准差
print(pstd, sstd)
# api
pstd = np.std(closing_prices)          # 总体标准差
sstd = np.std(closing_prices, ddof=1)  # 样本标准差
print(pstd, sstd)
```

## 四 时间数据处理和数据轴向汇总

**时间数据处理**
```python
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


# 日期转换函数
def dmy2wday(dmy):
    # 将日-月-年 转为 年-月-日
    dmy = str(dmy, encoding='utf-8')
    time = datetime.strptime(dmy, '%d-%m-%Y').date()
    wday = time.weekday()
    return wday


wdays, closing_prices = np.loadtxt('./data/aapl.csv',  # 读取文件
                                   delimiter=',',  # 分隔符
                                   usecols=(1, 6),  # 要读取的列
                                   unpack=True,  # 拆包
                                   converters={1: dmy2wday}  # 自定第几列使用的转换函数
                                   )

ave = np.zeros(5)
for i in range(ave.size):
    ave[i] = np.mean(closing_prices[wdays == i])

plt.plot(ave)
```

**数据的轴向汇总**
```python
import numpy as np
def func(data):
    pass

# func 	处理函数
# axis 	轴向 [0,1] 0:列  1:行
# array 	数组
np.apply_along_axis(func, axis, array)
```
**沿着数组中所指定的轴向，调用处理函数，并将每次调用的返回值重新组织成数组返回**

```python
import numpy as np

ary = np.arange(1,37).reshape((6, 6))

def apply(data):
    return np.mean(data)

print(np.mean(ary, axis=0))
print(np.apply_along_axis(apply, axis=0, arr=ary))
```
**轴向汇总时，可以使用api**

|Function Name|	NaN-safe|Description
|:---:|:---:|:---:|
|`np.sum`|`np.nansum`|元素求和|
|`np.prod`|`np.nanprod`|元素乘积|
|`np.mean`|`np.nanmean`|计算元素均值|
|`np.std`|`np.nanstd`|计算标准差|
|`np.var`|`np.nanvar`|计算方差|
|`np.min`|`np.nanmin`|寻找最小值|
|`np.max`|`np.nanmax`|寻找最大值|
|`np.argmin`|`np.nanargmin`|求最小值的索引|
|`np.argmax`|`np.nanargmax`|求最大值的索引|
|`np.median`|`np.nanmedian`|计算元素的中位数|
|`np.percentile`|`np.nanpercentile`|计算元素的基于排名的统计|
|`np.any`|`N/A`|是否有任何元素为真|
|`np.all`|`N/A`|是否所有元素都为真|
|`np.power`|`N/A`|幂运算|

* 可以通过指定`axis`参数实现轴向汇总

## 4.1 移动平均线
$N日移动平均线=\frac{N日收盘价之和}{N}$

**案例，绘制5日均线**
```python
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md

def dmy2ymd(dmy):
    dmy = str(dmy, encoding='utf-8')
    date = dt.datetime.strptime(dmy, '%d-%m-%Y').date()
    ymd = date.strftime('%Y-%m-%d')
    return ymd

dates, closing_prices = np.loadtxt('./data/aapl.csv', delimiter=',',
    usecols=(1, 6), unpack=True, dtype='M8[D], f8', converters={1: dmy2ymd})
sma51 = np.zeros(closing_prices.size - 4)
for i in range(sma51.size):
    sma51[i] = closing_prices[i:i + 5].mean()
# 开始绘制5日均线
plt.figure('Sipltle Moving Average', facecolor='lightgray')
plt.title('Sipltle Moving Average', fontsize=20)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Price', fontsize=14)
ax = plt.gca()
# 设置水平坐标每个星期一为主刻度
ax.xaxis.set_major_locator(md.WeekdayLocator( byweekday=md.MO))
# 设置水平坐标每一天为次刻度
ax.xaxis.set_minor_locator(md.DayLocator())
# 设置水平坐标主刻度标签格式
ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %Y'))
plt.tick_params(labelsize=10)
plt.grid(linestyle=':')
dates = dates.astype(md.datetime.datetime)
plt.plot(dates, closing_prices, c='lightgray', label='Closing Price')
plt.plot(dates[4:], sma51, c='orangered', label='SMA-5(1)')
plt.legend()
plt.gcf().autofmt_xdate()
plt.show()
```

# 五 卷积

设函数$f(\vec x) g(\vec x)$，$\vec x$为$n$维向量，则$f(\vec x)$与$g(\vec x)$卷积定义如下
做卷积运算的结果为:

$$
\begin{aligned}
    C(\vec x)=f(\vec x)\ast g(\vec x)=\int_{-\infty}^{+\infty}f(\vec y)g(\vec x -\vec y)d^{n}\vec y
\end{aligned}
$$

**一维的情况**
$$
\begin{aligned}
   f(x)\ast g( x)=\int_{-\infty}^{+\infty}f( y)g(x - y)d y
\end{aligned}
$$

**二维情况**
$$
\begin{aligned}
f(x,y)\ast g(x,y)=\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}f(\alpha,\beta)g(x - \alpha,y-\beta)d \alpha d\beta
\end{aligned}
$$

**三维情况**
$$
\begin{aligned}
f(x,y,z)\ast g(x,y,z)=\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}f(\alpha,\beta,\gamma)g(x - \alpha,y-\beta,z-\gamma)d \alpha d\beta d\gamma
\end{aligned}
$$

**离散情况**
$$
\begin{equation}y[n]=\sum_{k=-\infty}^{\infty} x[k] h[n-k]\end{equation}
$$

**卷积计算过程**
```
a = [1, 2, 3, 4, 5]   源数组
b = [8, 7, 6]		  卷积核  kernel
使用b作为卷积核，对a数组执行卷积运算的过程如下：

			   44  65  86           有效卷积 (valid)
           23  44  65  86  59       同维卷积 (same)
        8  23  44  65  86  59  30   完全卷积 (full)
        
0   0   1   2   3   4   5   0   0
6   7   8   反转，对应乘积求和，移动卷积核，知道卷积核变量完成源数组
	6   7   8
    	6   7   8
        	6   7   8
            	6   7   8
                	6   7   8
                    	6   7   8

c = numpy.convolve(a, b, 卷积类型)
```

**案例，卷积计算移动均线**
```python
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

def dmy2ymd(dmy):
    dmy = str(dmy, encoding='utf-8')
    date = dt.datetime.strptime(dmy, '%d-%m-%Y').date()
    ymd = date.strftime('%Y-%m-%d')
    return ymd

dates, closing_prices = np.loadtxt('./data/aapl.csv', delimiter=',',
    usecols=(1, 6), unpack=True, dtype='M8[D], f8', converters={1: dmy2ymd})

# 5日移动均线
sma52 = np.convolve( closing_prices, np.ones(5) / 5, 'valid')
plt.plot(dates[4:], sma52, c='limegreen', alpha=0.5,
        linewidth=1, label='SMA-5(2)')
# 10日移动均线
sma10 = np.convolve(closing_prices, np.ones(10) / 10, 'valid')
plt.plot(dates[9:], sma10, c='dodgerblue',linewidth=1,label='SMA-10')

plt.legend()
plt.show()
```

## 加权卷积

**案例，基于成交量加权的移动均线**
```python
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

def dmy2ymd(dmy):
    dmy = str(dmy, encoding='utf-8')
    date = dt.datetime.strptime(dmy, '%d-%m-%Y').date()
    ymd = date.strftime('%Y-%m-%d')
    return ymd

dates, closing_prices = np.loadtxt('./data/aapl.csv', delimiter=',',
    usecols=(1, 6), unpack=True, dtype='M8[D], f8', converters={1: dmy2ymd})

weights = np.exp(np.linspace(-1, 0, 5))
weights /= weights.sum()
sma5 = np.convolve(closing_prices, weights[::-1], 'valid')
plt.plot(dates[4:], sma5, c='limegreen', alpha=0.5,
        linewidth=6, label='SMA-5')
```
