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
s = [s_1, s_2,\cdots, s_n] \\
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
s = [s_1, s_2, \cdots, s_n] \\
w = [w_1, w_2, \cdots, w_n] \\
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

```
