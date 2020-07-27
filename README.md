# python-learn

#### 介绍
python学习笔记

# 一、python基础
## 1.1 数据类型
### 1.1.1 数字类型
* 整数: `int`
    > 整数, 也即是数学意义上的整数集合$Q$。对于整数的一切数学运算python都提供了支持。比如，算术运算，比较运算等
* 小数: `float`
    > 小数也即是浮点数, 对于浮点数的一切数学运算python都提供了支持。比如，算术运算，比较运算等。**基于C语言的double类型实现**
* 复数: `complex`
    > 也是数学意义上的复数, 在python中使用`j`或`J`表示虚数单位
* 布尔值: `bool`
    > 存在两个值(True --> 1, False --> 0), 在python解释器运行时，就会在内存中产生

### 1.1.2 变量
变量: 用于存放程序运行过程中的中间值。<br>
在python中变量是以引用方式保存变量值的. 也即是存放变量引用对象的内存地址。可以将python中的变量理解为C语言中的空指针(`void *`)。<br>
python提供内置函数`id()`可用于查看变量的标识, `Cpython`解释器则是返回变量引用对象的内存地址。

**变量的命名规范**<br>

1. 非数字开头
2. 字母、数字、下划线组成
3. 不能以python关键字和内置函数作为变量名
    ```python
    >>> import keyword
    >>> print(keyword.kwlist)  # python中的关键字
    ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

    >>> import builtins
    >>> print(dir(builtins))  # python内置函数等
    ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '_', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
    
    ```
**以上内容均不能用作变量名**

4. 尽量做到**见名知义**
5. 推荐使用以下划线分割多个单词方式命名变量

**小整数池**<br>
&emsp;&emsp;&emsp;&emsp;在交互模式下, 处于[-5, 256]范围内的整数，会在内存中提前生成，当对其进行使用时就不会在新建数据。对于在[-5, 256]范围外的整数，每次使用都会产生一个新的数据。<br>
&emsp;&emsp;&emsp;&emsp;在脚本方式则不会存在这一问题。

```python

```


## 1.2 控制流程

## 1.3 字符串

## 1.4 列表和元组

## 1.5 集合和字典



#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 码云特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5.  码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
