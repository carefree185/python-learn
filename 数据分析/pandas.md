# pandas
安装: `pip install pandas`

## 一 pandas.Series

`Series`是pandas中的一个数据结构，类似与一维数组。由下面两个部分组成：
- `values`: 一组数据（`ndarray`类型）
- `index`：相关的数据索引标签
### 创建Series
```python
import pandas as pd
import numpy as np

s = pd.Series(data=[1,2,3,4,5])
print(s)

# s = pd.Series(data=np.arange(0,10).reshape((2,5)))  # Series只能保存一维数组
# print(s)
```
* `Series`只能保存一维数组

**自定义索引**
```python
import pandas as pd
import numpy as np

s = pd.Series(data=[1,2,3], index=["a", "b", "c"])
print(s)
```
* 显示索引可以增强程序可读性，在进行索引取值或切片时比较方便

### Series的索引取值和切片
```python
import pandas as pd
import numpy as np

s = pd.Series(data=[1,2,3,4,5], index=["a", "b", "c", "d", "e"])
print(s[1])  # 隐式索引取值
print(s.loc["a"])  #显示索引取值

print(s[0:3])
print(s['a':'d'])
```
* `Series`索引取值和切片与列表操作一致
* 当存在显示索引时，隐式索引仍然生效
* **切片时，显示索引包含索引最后一个元素**

### 显示前几条和后几条数据
* `s.head(n)`: 显示前几条数据
* `s.tail(n)`: 显示后几条数据

```python
import pandas as pd
import numpy as np

s = pd.Series(data=[1,2,3,4,5], index=["a", "b", "c", "d", "e"])

print(s.head(3))
print(s.tail(2))
```

### 去重`s.unique()`
```python
import pandas as pd
import numpy as np

s = pd.Series(data=[1,1,2,2,3,4,5,8, 8, 9,10,2])
s.unique()  # 去重
```

### Series相加
```python
import pandas as pd
import numpy as np

s1 = pd.Series(data=[1,2,3,4,5], index=["a", "b", "c", "d", "e"])
s2 = pd.Series(data=[1,2,3,4,5], index=["a", "b", "f", "d", "e"])

print(s1+s2)
```
* 将对应相同索引的值进行相加。
* 如果没有对应的索引则相加后值为`NaN`(缺失值)


### 缺失值检测
```python
import pandas as pd
import numpy as np

s1 = pd.Series(data=[1,2,3,4,5], index=["a", "b", "c", "d", "e"])
s2 = pd.Series(data=[1,2,3,4,5], index=["a", "b", "f", "d", "e"])

s = s1+s2
# series支持掩码取值，取出索引位置对应为True值
print(s[s.notna()])
```
* `s.isnull()`: 检测是否为空，为空返回`True`
* `s.notnull()`: 检测不为空, 不为空返回`True`


## 二 pandas.DataFrame
`DataFrame`是一个【表格型】的数据结构。`DataFrame`由按一定顺序排列的
多列数据组成。设计初衷是将`Series`的使用场景从一维拓展到多维。
`DataFrame`既有行索引，也有列索引。
- 行索引：`index`
- 列索引：`columns`
- 值：`values`

**DataFrame可以看作时一个表格**，可以视为关系型数据库中的表

### 创建DataFrame
最常用的方法是传递一个字典来创建。`DataFrame`以 *字典* 的键作为每一【列】的名称，
以字典的值（一个数组）作为每一列。

此外，`DataFrame`会自动加上每一行的索引。

使用字典创建的`DataFrame`后，则`columns`参数将不可被使用。

同`Series`一样，若传入的列与字典的键不匹配，则相应的值为`NaN`。

**通过numpy创建**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame(data=np.random.randint(0, 100, size=(3,4)), index=['a', 'b', 'c'], columns=['A','B','C','D'])
print(df)
```
**通过字典创建**
```python
import pandas as pd

dic = {"A": [1,2,3,4],
       "B": [2,3,4,5],
       "C": [3,4,5,6],
       "D": [4,5,6,7]
       }

df = pd.DataFrame(data=dic, index=['a', 'b', 'c', 'd'])
print(df)
```

### DataFrame的属性
DataFrame属性：
* `values`: df的值，一个ndarray对象
* `columns`: 列索引
* `index`: 行索引
* `shape`: 维度
* `size`: 元素个数

```python
import pandas as pd

dic = {"A": [1,2,3,4],
       "B": [2,3,4,5],
       "C": [3,4,5,6],
       "D": [4,5,6,7]
       }

df = pd.DataFrame(data=dic, index=['a', 'b', 'c', 'd'])
print(df.values)
print(df.columns)
print(df.index)
print(df.shape)
print(df.size)
```

### DataFrame的索引取值与切片
**索引取值**
```python
import pandas as pd

dic = {"A": [1,2,3,4],
       "B": [2,3,4,5],
       "C": [3,4,5,6],
       "D": [4,5,6,7]
       }

df = pd.DataFrame(data=dic, index=['a', 'b', 'c', 'd'])

print(df['A'])  # 取一列
print(df[['A', 'B']])  # 取两列

print(df.loc["a"]) # 取一行，只能指定显示索引
# print(df.loc[0]) # 不能指定显示索引
print(df.iloc[0])  # 取一行，只能指定隐式索引
print(df.iloc[[0, 1]])  # 取两行 

print(df['A']['a'])  # 取(a,A)对应的元素
print(df.loc['a','A'])  # 取(a,A)对应的元素
print(df.loc[['a','b'],'A'])  # 取(a,A),(b,A)对应的元素
```
**切片**
```python
import pandas as pd

dic = {"A": [1,2,3,4],
       "B": [2,3,4,5],
       "C": [3,4,5,6],
       "D": [4,5,6,7]
       }

df = pd.DataFrame(data=dic, index=['a', 'b', 'c', 'd'])
df[0:2]  # 切取前两行
df.iloc[:,0:1]  # 切取第一列，与ndarray相同
```
### DataFrame运算
同Series一样：

- 在运算中自动对齐不同索引的数据
- 如果索引不对应，则补`NaN`

## pandas案例 股票数据操作
- 使用tushare包获取某股票的历史行情数据。
- 输出该股票所有收盘比开盘上涨3%以上的日期。
- 输出该股票所有开盘比前日收盘跌幅超过2%的日期。
- 假如我从2010年1月1日开始，每月第一个交易日买入1手股票，每年最后一个交易日卖出所有股票，到今天为止，我的收益如何？

```jupyterpython

#%%
# 获取数据并保存
import tushare as ts
df = ts.get_k_data('600519',start='1900-01-01')
df.to_csv('./maotai.csv')
#%%
# 读取数据,将并date列转为行索引
df = pd.read_csv('./maotai.csv', index_col='date', parse_dates=['date'])
df.drop(labels='Unnamed: 0',axis=1,inplace=True)
#%%

# 输出该股票所有收盘比开盘上涨3%以上的日期。
is_true = (df['close'] - df['open'])/df['open'] > 0.03
df.loc[is_true].index  # 返回满足需求的数据

#%%

# 输出该股票所有开盘比前日收盘跌幅超过2%的日期
(df['open']-df['close'].shift(1))/df['close'].shift(1) < -0.02
df.loc[(df['open']-df['close'].shift(1))/df['close'].shift(1) < -0.02].index
# shift(n)数据整体移动

#%% md

- 假如我从2010年1月1日开始，每月第一个交易日买入1手股票，每年最后一个交易日卖出所有股票，到今天为止，我的收益如何？
- 分析：
    - 规则：基于开盘价股票的买卖
    - 买：一个完整的年需要买12次股票，一次买入100只，一个完整的年需要买入1200只（单价：当天开盘价）
    - 卖：一个完整的年需要卖一次股票，一次卖出1200只
    - 备注：19年不是一个完整的年，该年只可以买入900只，并且卖不出去

#%%

df_new = df['2010':'2021']  # 按年切片
#数据的重新取样的机制(resample):根据指定好的规则进行指定数据的提取
df_monthly = df_new.resample('M').first()
# 买股票
a = df_monthly['open'].sum()*100

# 卖股票
df_yearly = df_new.resample('A').last()
df_yearly = df_yearly[:-1]

b = df_yearly['open'].sum()*1200
# 剩余的计算到b中
b += df.iloc[-1]['close']*300
(b - a)/a  # 收益率
```



