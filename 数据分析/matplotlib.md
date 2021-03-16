# 一、简介
`matplotlib`是`python`的一个绘图库。使用它可以很方便的绘制出版质量级别的图形

### matplotlib基本功能

1. 基本绘图 （在二维平面坐标系中绘制连续的线）
   1. 设置线型、线宽和颜色  
   2. 设置坐标轴范围
   3. 设置坐标刻度
   4. 设置坐标轴
   5. 图例
   6. 特殊点
   7. 备注
2. 图形对象(图形窗口)
   1. 子图
   2. 刻度定位器
   3. 刻度网格线
   4. 半对数坐标
   5. 散点图
   6. 填充
   7. 条形图
   8. 饼图
   9. 等高线图
   10. 热成像图
   11. 三维曲面
   12. 简单动画

# 二、基本绘图

## 2.1 核心绘图接口plot
核心绘图接口，`matplotlib.pyplot.plot(xarray, yarray)`

* `xarray`: `x`轴的数组
* `yarray`: `y`轴的数组

**案例，绘制一条余弦曲线**
```python
import numpy as np
import matplotlib.pyplot as plt

# x = np.arange(-np.pi/2, np.pi/2, 0.001)
x = np.linspace(-np.pi/2, np.pi/2, 10000)
y = np.cos(x)
plt.plot(x, y)
plt.show()
```


## 2.2 绘制水平线和垂直线
水平线: `plt.hlines(yvals, xmins, xmaxs)`
* `yvals`:可以是一个数组，也可以是单独的一个数。表示水平线的高度
* `xmins, xmaxs`: 可以是一个数组，也可以是单独的一个数，
   * `xmaxs-xmins`: 表示水平线的长度
   * **注意**: 如果是数组，维度必须和`yvalues`一致

垂直线: `plt.vlines(xvals, ymins, ymaxs)`
* `xvals`:可以是一个数组，也可以是单独的一个数。表示垂直线的水平位置
* `ymins, ymaxs`: 可以是一个数组，也可以是单独的一个数，
   * `ymaxs-ymins`: 表示垂直线的的长度
   * **注意**: 如果是数组，维度必须和`xvals`一致

```python
import matplotlib.pyplot as plt

# 绘制一条
plt.hlines(5, 1, 10)  # 水平
plt.vlines(5, 1, 10)  # 水平
# 绘制多条
plt.hlines([1,2,3,4,5], 1, 5)
plt.vlines([1,2,3,4,5], 1, 5)

plt.hlines([1,2,3,4,5], [1,2,3,4,5], [2,3,4,5,6])
plt.vlines([1,2,3,4,5], [1,2,3,4,5], [2,3,4,5,6])
plt.show()
```

## 2.3 线型、线宽和颜色
要设置绘制线的线型、线宽和颜色，可以指定绘图接口的参数。
* `linestyle`: 线型, 取值为 : `'-'  '--'  '-.'  ':'`
* `linewidth`: 线宽, 取值为数字
* `color`: 颜色，取值如下图
  ![](.img/matplotlib-color.png)
* `alpha`: 透明度，取值为`0~1`之间的数

其中参数的取值如下

|参数|取值|说明|
|:---:|:---:|:---:|
|`linestyle`|`'-'  '--'  '-.'  ':'`|`'-'`: 直线, `'--'`: 虚线, `'-.'`: 点虚线, `':'`点线|
|`linewidth`|数字`num`|代表默认宽度的`num`倍|
|`color`|色彩单词, 十六进制, `(R, G, B)`, `(R, G, B, A)`||
|`alpha`|`0~1`之间|表示透明度|

```python
import numpy as np
import matplotlib.pyplot as plt

# x = np.arange(-np.pi/2, np.pi/2, 0.001)
x = np.linspace(-np.pi/2, np.pi/2, 10000)
cosx = np.cos(x)
sinx = np.sin(x)

plt.plot(x, cosx, linestyle='--', linewidth=2, color='black')
plt.plot(x, sinx, linestyle='-.', linewidth=3, color='r', alpha=0.5)
plt.show()
```

## 2.4 设置坐标范围
**`x`轴**: `plt.xlim(x_min, x_max)`
* `x_min`: `x`轴最小取值
* `x_max`: `x`轴最大取值

**`y`轴**: `plt.ylim(y_min, y_max)`
* `y_min`: `y`轴最小取值
* `y_max`: `y`轴最大取值

```python
import numpy as np
import matplotlib.pyplot as plt

# x = np.arange(-np.pi/2, np.pi/2, 0.001)
x = np.linspace(-np.pi, np.pi, 10000)
cosx = np.cos(x)
sinx = np.sin(x)
# 设置线型、线宽、颜色和透明度
plt.plot(x, cosx, linestyle='--', linewidth=2, color='black')
plt.plot(x, sinx, linestyle='-.', linewidth=3, color='r', alpha=0.5)
# 设置坐标轴范围为0~pi(设置图像可视化区间)
plt.xlim(0, np.pi+0.1)
plt.ylim(0, 1.1)
plt.show()
```

## 2.5 设置坐标轴刻度
设置`x`轴坐标刻度: `plt.xticks(x_val_list , x_text_list )`
* `x_val_list`: `x`轴刻度值序列
* `x_text_list`:`x`轴刻度标签文本序列`[可选]`

设置`y`轴坐标刻度: `mp.yticks(y_val_list , y_text_list )`
* `y_val_list`: `y`轴刻度值序列
* `y_text_list`:`y`轴刻度标签文本序列`[可选]`

**matplotlib支持使用`latex`语法**

```python
import numpy as np
import matplotlib.pyplot as plt

# x = np.arange(-np.pi/2, np.pi/2, 0.001)
x = np.linspace(-np.pi, np.pi, 10000)
cosx = np.cos(x)
sinx = np.sin(x)
# 设置线型、线宽、颜色和透明度
plt.plot(x, cosx, linestyle='--', linewidth=2, color='black')
plt.plot(x, sinx, linestyle='-.', linewidth=3, color='r', alpha=0.5)
# 设置坐标刻度
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [r"$-\pi$", r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$'])
plt.show()
```

## 2.6 设置坐标轴位置
matplotlib坐标轴分为四部分分别是:`left / right / bottom / top`是个坐标轴
* 获取当前坐标轴字典: `ax = mp.gca()`, `getCurrentaxis`
* 获取坐标轴: `axis = ax.spines['坐标轴名']`
* 设置坐标轴的位置: `axis.set_position((type, val))`
   * `type`: 类型，一般为`'data'`
   * `val`: 参照值
* 设置坐标轴的颜色: `axis.set_color(color)`
   * `color`: 表示颜色字符串

```python
import numpy as np
import matplotlib.pyplot as plt

# x = np.arange(-np.pi/2, np.pi/2, 0.001)
x = np.linspace(-np.pi, np.pi, 10000)
cosx = np.cos(x)
sinx = np.sin(x)
# 设置线型、线宽、颜色和透明度
plt.plot(x, cosx, linestyle='--', linewidth=2, color='black')
plt.plot(x, sinx, linestyle='-.', linewidth=3, color='r', alpha=0.5)
# 设置坐标刻度
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [r"$-\pi$", r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$'])

ax = plt.gca()
axis_b = ax.spines['bottom']  # 获取底部坐标
axis_b.set_position(('data', 0))   # 移动到y=00位置
axis_l = ax.spines['left']  # 获取左边坐标对象
axis_l.set_position(('data', 0))  # 移动到x=0位置
ax.spines['top'].set_color('none')  # 顶部坐标设置为空
ax.spines['right'].set_color('none')  # 右边坐标设置为空

plt.show()
```

## 2.7 图例
备注每个图形代表的意义

* `plt.legend(loc='')`: 显示图例，默认为最佳位置
   * `loc`取值如下
  
      |位置|值|
      |:---:|:---:|
      |`'best'`        |`0`|
      |`'upper right'` |`1`|
      |`'upper left'`  |`2`|
      |`'lower left'`  |`3`|
      |`'lower right'` |`4`|
      |`'right'`       |`5`|
      |`'center left'` |`6`|
      |`'center right'`|`7`|
      |`'lower center'`|`8`|
      |`'upper center'`|`9`|
      |`'center'`      |`10`|
   * **需要在绘图接口中指定`label`参数**，可以使用`latex`语法


```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-np.pi, np.pi, 10000)
cosx = np.cos(x)
sinx = np.sin(x)
# 设置线型、线宽、颜色和透明度,label
plt.plot(x, cosx, linestyle='--', linewidth=2, color='black', label=r'$y=\cos(x)$')
plt.plot(x, sinx, linestyle='-.', linewidth=3, color='r', alpha=0.5, label=r'$y=\sin(x)$')
plt.legend()
```

## 2.8 特殊点

绘制特殊点接口如下
```python
# xarray: <序列> 所有需要标注点的水平坐标组成的序列
# yarray: <序列> 所有需要标注点的垂直坐标组成的序列

import matplotlib.pyplot as plt

plt.scatter(xarray,  # 特殊点的x轴数组
            yarray,  # 特殊的的y轴数值
            marker='',  # 点型 ~ matplotlib.markers
            s=70,  # 大小
            edgecolor='',  # 边缘色
            facecolor='',  # 填充色
            zorder=3  # 绘制图层编号 （编号越大，图层越靠上）
            )
```
点样式可以在`help(matplotlib.markers)`中查看

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-np.pi, np.pi, 10000)
cosx = np.cos(x)
sinx = np.sin(x)
# 设置线型、线宽、颜色和透明度,label
plt.plot(x, cosx, linestyle='--', linewidth=2, color='black', label=r'$y=\cos(x)$')
plt.plot(x, sinx, linestyle='-.', linewidth=3, color='r', alpha=0.5, label=r'$y=\sin(x)$')
# 绘制特殊点
plt.scatter([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [-1, 0, 1, 0, -1], marker='.', s=140, color='red')
plt.scatter([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [0, -1, 0, 1, 0], marker='.', s=140, color='green')
plt.show()
```

## 2.9 备注
绘图后，难免会要在图像上添加一些文本信息，可以使用如下`api`进行备注
```python
# 在图表中为某个点添加备注。包含备注文本，备注箭头等图像的设置。
import matplotlib.pyplot as plt
plt.annotate(
    r'$\frac{\pi}{2}$',			# 备注中显示的文本内容
    xycoords='data',			# 备注目标点所使用的坐标系（data表示数据坐标系）
    xy=(x, y),	 				# 备注目标点的坐标
    textcoords='offset points',	# 备注文本所使用的坐标系（offset points表示参照点的偏移坐标系）
    xytext=(x, y),				# 备注文本的坐标
    fontsize=14,				# 备注文本的字体大小
    arrowprops=dict()			# 使用字典定义文本指向目标点的箭头样式
)
```
**箭头和连接线样式设置**
```python
#arrowprops字典参数的常用key
arrowprops=dict(
	arrowstyle='',		#定义箭头样式
    connectionstyle=''	#定义连接线的样式
)
```
`arrowstyle`样式字符串如下
```
=============================================
Name           Attrs
=============================================
  '-'          None
  '->'         head_length=0.4,head_width=0.2
  '-['         widthB=1.0,lengthB=0.2,angleB=None
  '|-|'        widthA=1.0,widthB=1.0
  '-|>'        head_length=0.4,head_width=0.2
  '<-'         head_length=0.4,head_width=0.2
  '<->'        head_length=0.4,head_width=0.2
  '<|-'        head_length=0.4,head_width=0.2
  '<|-|>'      head_length=0.4,head_width=0.2
  'fancy'      head_length=0.4,head_width=0.4,tail_width=0.4
  'simple'     head_length=0.5,head_width=0.5,tail_width=0.2
  'wedge'      tail_width=0.3,shrink_factor=0.5
=============================================
```
`connectionstyle`样式字符串如下
```
=============================================
Name           Attrs
=============================================
  'angle' 		angleA=90,angleB=0,rad=0.0
  'angle3' 		angleA=90,angleB=0`   
  'arc'			angleA=0,angleB=0,armA=None,armB=None,rad=0.0
  'arc3' 		rad=0.0
  'bar' 		armA=0.0,armB=0.0,fraction=0.3,angle=None
=============================================
```


**示例**
```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-np.pi, np.pi, 10000)
cosx = np.cos(x)
sinx = np.sin(x)
# 设置线型、线宽、颜色和透明度,label
plt.plot(x, cosx, linestyle='--', linewidth=2, color='black', label=r'$y=\cos(x)$')
plt.plot(x, sinx, linestyle='-.', linewidth=3, color='r', alpha=0.5, label=r'$y=\sin(x)$')

plt.scatter([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [-1, 0, 1, 0, -1], marker='.', s=140, color='red')
plt.scatter([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [0, -1, 0, 1, 0], marker='.', s=140, color='green')

plt.annotate(
    r'$[\frac{\pi}{2}, 1]$',			# 备注中显示的文本内容
    xycoords='data',			# 备注目标点所使用的坐标系（data表示数据坐标系）
    xy=(np.pi/2, 1),	 				# 备注目标点的坐标
    textcoords='offset points',	# 备注文本所使用的坐标系（offset points表示参照点的偏移坐标系）
    xytext=(40, -10),				# 备注文本的坐标
    fontsize=14,				# 备注文本的字体大小
    arrowprops=dict(
        arrowstyle='->',
        connectionstyle='angle3'
    )			# 使用字典定义文本指向目标点的箭头样式
)

plt.legend()
plt.show()
```

# 三 图像对象

## 3.1 图像窗口figure

创建窗口
```python
import matplotlib.pyplot as plt
plt.figure(
    'title1',					#窗口标题栏文本 
    figsize=(4, 3),		#窗口大小 <元组>
    dpi=120,			#像素密度
	facecolor=''		#图表背景色
)
```
* **如果指定标题的窗口已经创建，则将窗口置为当前窗口**

`plt.figure`方法不仅可以构建一个新窗口，如果已经构建过`title='AAA'`
的窗口，又使用`figure`方法构建了`title='AAA'` 的窗口的话，
`plt`将不会创建新的窗口，而是把`title='AAA'`的窗口置为当前操作窗口。

**窗口的相关属性**
```python
import matplotlib.pyplot as plt
# 设置图表标题 显示在图表上方
plt.title("title", fontsize=12)

# 设置水平轴的文本
plt.xlabel("x_label_str", fontsize=12)
# 设置垂直轴的文本
plt.ylabel("y_label_str", fontsize=12)

# 设置刻度参数   labelsize设置刻度字体大小
plt.tick_params(..., labelsize=8)
# 设置图表网格线  linestyle设置网格线的样式
	#	-  or solid 粗线
	#   -- or dashed 虚线
	#   -. or dashdot 点虚线
	#   :  or dotted 点线
plt.grid(linestyle='')
# 设置紧凑布局，把图表相关参数都显示在窗口中
plt.tight_layout() 
```

## 3.2 子图
### 3.2.1 矩阵式布局
矩阵式布局接口
```python
import matplotlib.pyplot as plt
plt.figure('Subplot Layout', facecolor='lightgray')
# 拆分矩阵
	# rows:	行数
    # cols:	列数
    # num:	编号
plt.subplot(rows, cols, num)
	#	1 2 3
	#	4 5 6
	#	7 8 9 
plt.subplot(3, 3, 5)		# 操作3*3的矩阵中编号为5的子图
plt.subplot(335)			# 简写
```
**案例**
```python
import matplotlib.pyplot as plt
plt.figure('Subplot Layout', facecolor='lightgray')

for i in range(9):
    plt.subplot(3, 3, i+1)
    plt.text(0.5, 0.5, i+1,ha='center',va='center',size=36,alpha=0.7,color='red')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
plt.show()
```

### 3.2.2 网格式布局
网格式布局区别于局长式布局的优点是可以进行**单元格合并**

绘制网格式子图布局相关API
```python
import matplotlib.gridspec as mg
import matplotlib.pyplot as plt
plt.figure('Grid Layout', facecolor='lightgray')
# 调用GridSpec方法拆分网格式布局
# rows:	行数
# cols:	列数
# gs = mg.GridSpec(rows, cols)	拆分成3行3列
gs = mg.GridSpec(3, 3)	
# 合并0行与0、1列为一个子图表
plt.subplot(gs[0, :2])
plt.text(0.5, 0.5, '1', ha='center', va='center', size=36)
plt.show()
```
**案例**
```python
import matplotlib.gridspec as mg
import matplotlib.pyplot as plt
plt.figure('Grid Layout', facecolor='lightgray')

gs = mg.GridSpec(3, 3)

plt.subplot(gs[0, :2])
plt.text(0.5, 0.5, '1', ha='center', va='center', size=36)
plt.xticks([])
plt.yticks([])
plt.tight_layout()

plt.subplot(gs[:2, 2])
plt.text(0.5, 0.5, '2', ha='center', va='center', size=36)
plt.xticks([])
plt.yticks([])
plt.tight_layout()

plt.subplot(gs[1:, 0])
plt.text(0.5, 0.5, '3', ha='center', va='center', size=36)
plt.xticks([])
plt.yticks([])
plt.tight_layout()

plt.subplot(gs[2, 1:])
plt.text(0.5, 0.5, '4', ha='center', va='center', size=36)
plt.xticks([])
plt.yticks([])
plt.tight_layout()

plt.subplot(gs[1:2, 1:2])
plt.text(0.5, 0.5, '5', ha='center', va='center', size=36)
plt.xticks([])
plt.yticks([])
plt.tight_layout()

plt.show()
```

### 3.2.3 自由式布局

```python
import matplotlib.pyplot as plt
plt.figure('Flow Layout', facecolor='lightgray')
# 设置图标的位置，给出左下角点坐标与宽高即可
# left_bottom_x: 左下角点x坐标
# left_bottom_x: 左下角点y坐标
# width:		 宽度
# height:		 高度
# mp.axes([left_bottom_x, left_bottom_y, width, height])
plt.axes([0.03, 0.03, 0.94, 0.94])
plt.text(0.5, 0.5, '1', ha='center', va='center', size=36)
plt.show()
```

## 3.3 刻度定位器
自动在坐标上设置主刻度

刻度定位器的API
```python
import matplotlib.pyplot as plt
# 获取当前坐标轴
ax = plt.gca()
# 设置水平坐标轴的主刻度定位器
ax.xaxis.set_major_locator(plt.NullLocator())
# 设置水平坐标轴的次刻度定位器为多点定位器，间隔0.1
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
```

**常用刻度定位器**
```python
import matplotlib.pyplot as plt
# 空定位器：不绘制刻度
plt.NullLocator()
# 最大值定位器：
# 最多绘制nbins+1个刻度
plt.MaxNLocator(nbins=3)
# 定点定位器：根据locs参数中的位置绘制刻度
plt.FixedLocator(locs=[0, 2.5, 5, 7.5, 10])
# 自动定位器：由系统自动选择刻度的绘制位置
plt.AutoLocator()
# 索引定位器：由offset确定起始刻度，由base确定相邻刻度的间隔
plt.IndexLocator(offset=0.5, base=1.5)
# 多点定位器：从0开始，按照参数指定的间隔(缺省1)绘制刻度
plt.MultipleLocator()
# 线性定位器：等分numticks-1份，绘制numticks个刻度
plt.LinearLocator(numticks=21)
# 对数定位器：以base为底，绘制刻度
plt.LogLocator(base=2)
```

**案例，绘制坐标轴**
```python
import matplotlib.pyplot as plt
plt.xlim(-10, 10)
plt.ylim(-1, 1)


ax = plt.gca()
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
# 设置水平坐标轴的主刻度定位器
ax.xaxis.set_major_locator(plt.MultipleLocator(1))
# 设置水平坐标轴的次刻度定位器为多点定位器，间隔0.1
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

plt.yticks([])
plt.show()
```

## 3.4 刻度网格线

```python
import matplotlib.pyplot as plt
ax = plt.gca()
#绘制刻度网格线
ax.grid(
    which='',		# 'major'/'minor' <-> '主刻度'/'次刻度' 
    axis='',		# 'x'/'y'/'both' <-> 绘制x或y轴
    linewidth=1, 	# 线宽
    linestyle='', 	# 线型
    color='',		# 颜色
	alpha=0.5		# 透明度
)
```

**案例**
```python
import matplotlib.pyplot as mp
import numpy as np
y = np.array([1, 10, 100, 1000, 100, 10, 1])

mp.figure('Normal & Log', facecolor='lightgray')
ax = mp.gca()
# 设置刻度定位器
ax.xaxis.set_major_locator(mp.MultipleLocator(1.0))
ax.xaxis.set_minor_locator(mp.MultipleLocator(0.1))
ax.yaxis.set_major_locator(mp.MultipleLocator(250))
ax.yaxis.set_minor_locator(mp.MultipleLocator(50))
# 绘制网格线
ax.grid(which='major', axis='both', linewidth=0.5,
        linestyle='--', color='orange')
ax.grid(which='minor', axis='both', linewidth=0.25,
        linestyle='-', color='orange')
# 窗口属性设置
mp.title('Normal', fontsize=20)
mp.ylabel('y', fontsize=14)
mp.tick_params(labelsize=10)
# 绘图
mp.plot(y, 'o-', c='dodgerblue', label='plot')
mp.legend()
mp.show()
```
## 3.5 半对数坐标
更好展示底部数据的细节
```python
import matplotlib.pyplot as mp
mp.figure('Grid', facecolor='lightgray')
y = [1, 10, 100, 1000, 100, 10, 1]
mp.semilogy(y)
mp.show()
```

# 四 统计图绘制

## 4.1 散点图

可以通过每个点的坐标、颜色、大小和形状**表示不同的特征值**

```python
import matplotlib.pyplot as mp

mp.scatter(
    'x', 					# x轴坐标数组
    'y',					# y轴坐标数组
    marker='', 			# 点型
    s=10,				# 大小
    color='',			# 颜色
    edgecolor='', 		# 边缘颜色
    facecolor='',		# 填充色
    zorder=''			# 图层序号
)
```

**numpy.random**提供生成一组正态分布的api:`np.random.normal(e, s, n)`
* `e= "期望"`
* `s = "标准差"`
* `n = "个数"`

```python
import numpy as np
e = "期望"
s = "标准差"
n = "个数"
np.random.normal(e, s, n)
```

**颜色映射**
```python

import numpy as np
import matplotlib.pyplot as mp

n = 100
x = np.random.normal(172, 10, n)
y = np.random.normal(60, 7, n)

d = (x-172)**2 + (y-60)**2
mp.scatter(x, y, c=d, cmap='jet')	# 以c作为参数，取cmap颜色映射表中的颜色值
```
* 以`c`作为参数，取`cmap`颜色映射表中的颜色值

颜色映射表可以通过如下代码进行查询
```python
import numpy as np
import matplotlib.pyplot as plt

# Have colormaps separated into categories:
# http://matplotlib.org/examples/color/colormaps_reference.html

cmaps = [('Perceptually Uniform Sequential',
                            ['viridis', 'inferno', 'plasma', 'magma']),
         ('Sequential',     ['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
         ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool',
                             'copper', 'gist_heat', 'gray', 'hot',
                             'pink', 'spring', 'summer', 'winter']),
         ('Diverging',      ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                             'seismic']),
         ('Qualitative',    ['Accent', 'Dark2', 'Paired', 'Pastel1',
                             'Pastel2', 'Set1', 'Set2', 'Set3']),
         ('Miscellaneous',  ['gist_earth', 'terrain', 'ocean', 'gist_stern',
                             'brg', 'CMRmap', 'cubehelix',
                             'gnuplot', 'gnuplot2', 'gist_ncar',
                             'nipy_spectral', 'jet', 'rainbow',
                             'gist_rainbow', 'hsv', 'flag', 'prism'])]


nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps)
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(cmap_category, cmap_list):
    fig, axes = plt.subplots(nrows=nrows)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

    for ax, name in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()

for cmap_category, cmap_list in cmaps:
    plot_color_gradients(cmap_category, cmap_list)

plt.show() 
```

## 4.2 

