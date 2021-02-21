# 十三、`while`循环
`while`循环语法如下:
```python
while 循环条件:
    loop_body
else:
    """循环没有被break跳出时执行此语句"""
```
> 1. `while`循环又称条件循环, 每次循环都会先检查循环条件是否成立. 当条件成立时, 进入循环。当条件不成立时, 结束循环.
> 2. `while`循环存在一个可选`else`子句. 当且仅当循环不被`break`跳出时，执行`else`子句

**示例1**
```python
a, b = 0, 1
while a < 10:
    print(a, end=" ")
    a, b = b, a + b
print()
```
**示例2**
```python
i = 0
while i < 10:
    if i % 2 != 0:
        print(i, end=" ")
    i += 1  # 控制条件发生变化, 条件不发生变化的while循环是一个死循环.
```
