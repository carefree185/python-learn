# 十二、for循环
for循环又称迭代循环，可以遍历任何一个可迭代你对象
> 1. 可迭代对象，指可以变为迭代器对象的对象，也即是定义了`__iter__`方法的对象

```python
for var_name in iterable:
    # 循环体代码
else:
    # 未被break跳过执行此块语句
```
> 1. for循环会在底层调用可迭代对象`__iter__`方法，产生一个迭代器
> 2. 每次循环都会取出迭代器的一个值，赋值给变量`var_name`
> 3. `else`为可选子句

## **range对象**
`range([start], end, [step])`
> 1. `range`会产一根据参数产生一个可迭代对象
> 2. start: 产的对象数据的开始数据
> 3. end: 结束数据，不包括
> 4. step: 每隔`step`产生一个数据(`data[index+1] - data[index] = step`)
> 5. `range(3)`: 最终数据`0 1 2`
> 6. `range(1, 5)`: 最终数据`1 2 3 4`
> 7. `range(1, 5, 3)`: 最终数据`1, 4`

**九九乘法表**
![输入图片说明](https://images.gitee.com/uploads/images/2020/1114/004023_efd923d6_7841459.png "屏幕截图.png")
```python
for i in range(1, 10):
    for j in range(1, i+1):
        print("%d * %d = %d" % (j, i, i * j), end='\t')
    print()
print()
for i in range(9, 0, -1):
    for j in range(1, i+1):
        print("%d * %d = %d" % (j, i, i * j), end='\t')
    print()
```