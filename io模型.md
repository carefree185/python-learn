# 六十四、io模型
**是针对网络io的模型**

**常见io模型**
* blocking IO
* nonblocking IO
* IO multiplexing
* signal driven IO
* asynchronous IO


## 64.1 `Blocking IO`阻塞IO模型

![](https://images.gitee.com/uploads/images/2020/1116/204208_456d55cd_7841459.gif "阻塞IO模型.gif")
****
![](https://images.gitee.com/uploads/images/2020/1116/210157_ec4d8eaf_7841459.png "屏幕截图.png")
> 1. 阻塞`IO`模型在向  _操作系统/内核_  获取数据时，如果数据没有到达操作系统将一直等待，当数据到达操作系统才会向下继续执行.
> 2. 当数据到达操作系统后，操作系统就会将数据拷贝到用户进程，让用户进程继续处理数据
> 3. **blocking IO的特点就是在IO执行的两个阶段（等待数据和拷贝数据两个阶段）都被block了**
> 4. **之前使用的都是阻塞IO模型( _协程除外_ )**

## 64.2 `NonBlocking IO` 非阻塞`IO`模型

![输入图片说明](https://images.gitee.com/uploads/images/2020/1116/210012_8fbc51a5_7841459.gif "非阻塞IO模型.gif")
> 1. 获取数据时，操作系统每次都会返回数据
> 2. 如果没有数据，则返回error；如果有数据，返回数据
****
![输入图片说明](https://images.gitee.com/uploads/images/2020/1116/210102_a2efccc1_7841459.png "屏幕截图.png")
* 用户进行向操作系统请求数据，如果数据没有到达，用户进程就会继续处理其他事务。
* 然后每隔一段时间来询问操作系统数据是否到达
* 当数据到达操作系统后，操作系统将数据拷贝到用户进程，让用户进程继续处理数据。

**非阻塞`IO`实现TCP服务端并发**

**server.setblocking(False)  设置为非阻塞`IO` 默认为True，阻塞IO**
```python
import socket

server = socket.socket()

server.bind(("127.0.0.1", 8080))
server.listen(10)
server.setblocking(False)  # 设置为非阻塞`IO` 默认为True，阻塞IO

connection_list = []  # 保存连接生成的套接字
del_con_list = []  # 记录需要删除的连接
while True:
    try:
        connection, address = server.accept()  # 如果没有连接将会触发异常 BlockingIOError
        print(f"客户端{address}建立连接")
        connection_list.append(connection)  # 保存连接对象
    except BlockingIOError as e:
        # 没有连接，执行其他事情
        con_handler = connection_list.copy()  # 复制一份套接字列表
        for conn in con_handler:
            try:
                data = conn.recv(1024)  # 此时conn也是一个非阻塞IO，没有消息也会触发异常 BlockingIOError
                if not data:
                    conn.close()  # 关闭连接
                    del_con_list.append(conn)  # 记录删除
                    continue  # 检测下一个套接字
                else:
                    print(f"客户端{conn.getpeername()}发送过来的消息: {data.decode()}")
                    conn.send(data.upper())  # 将客户端发来的消息返回
            except BlockingIOError as e:
                # 没有数据发送过来，检测下一个客户端是否发送消息过来
                continue
            except ConnectionResetError:  # 遍历到套接字时，可能已经被关闭引发的异常
                conn.close()  # 套接字被提前关闭
                del_con_list.append(conn)  # 记录删除

        for del_conn in del_con_list:  # 遍历将要删除的连接
            connection_list.remove(del_conn)  # 删除原列表中无用的套接字

        del_con_list.clear()  # 清空无用连接的列表
```
> 1. 非阻塞`IO`对系统资源消耗非常严重。
> 2. 长时间占用`CPU`资源，但是有大部分时间却无事可做
> 3. 实际应用中通常不考虑使用

## 64.3 `IO`多路复用模型
`IO`多路复用也称为`IO`方式为事件驱动`IO(event driven IO)`

**基本原理** 
> 1. 将有`IO`操作的事件交由操作系统提供的`select`等机制监管，操作系统会轮询的查询这些事件
> 2. 当检测到`IO`操作完成, `select`等机制就会已经完成的事件返回
> 3. 由用户进程(应用程序)来处理

![输入图片说明](https://images.gitee.com/uploads/images/2020/1116/225232_982b574c_7841459.gif "IO多路复用模型.gif")

![输入图片说明](https://images.gitee.com/uploads/images/2020/1117/011126_b31b2097_7841459.png "屏幕截图.png")

### 64.3.1 **`select`机制** 
python内置`select`模块提供

**select机制监听 _文件描述符_， 当 _文件描述_ 符满足某个状态后返回**
1. `select.select(rlist, wlist, xlist, timeout=None)`: 提交监管对象
>  * `rlist`: 等待 **读的对象** ，监听需要获取数据的对象列表
>  * `wlist`: 等待 **写的对象** ，监听需要写入数据的对象列表，一般不用，传递一个空列表`[]`
>  * `xlist`: 等待 **异常的对象** , 一般情况传入空列表`[]`
>  * `timeout`: 当超时时间为空，则`select`会一直阻塞，直到监听的句柄发生变化
>  * 返回值: 元组`(read_list, write_list, error_list)`
>    * `read_list`: 序列中的`fd`满足 **可读** 条件时，则获取发生变化的`fd`并添加到`read_list`中
>    * `write_list`: 序列中含有`fd`时，则将该序列中所有的`fd`添加到`write_list`
>    * `error_list`: 序列中的`fd`发生错误时，则将该发生错误的`fd`添加到 `error_list`

**select机制实现TCP服务端并发**
```python
import socket
import select

server = socket.socket()

server.bind(("127.0.0.1", 8080))
server.listen(10)
server.setblocking(False)
r_list = [server]  # 需要检测的对象


while True:
    read_list, write_list, error_list = select.select(r_list, [], [])  # 监测server 返回[<socket.socket fd=348, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8080)>], [], [])

    for i in read_list:
        if i is server:  # 判断对象类型，如果为server对象，执行以下操作
            conn, addr = i.accept()  # 接受客户端的连接
            r_list.append(conn)  # 建立连接，客户端发送消息可能还未到
        else:  # 对象为连接对象
            try:
                data = i.recv(1024)  # 接受客户端发送过来的消息
                if not data:  # 没有数据，也就是客户端断开连接
                    i.close()  # 关闭无用连接
                    r_list.remove(i)  # 从移除检测对象列表
                    continue  # 监测下一个对象是否有数据
                print(f"客户端{i.getpeername()}发送的消息: {data.decode()}")
                i.send(data.upper())  # 将数据返回
            except ConnectionResetError:
                i.close()  # 关闭被强制关闭的连接
                r_list.remove(i)  # 移除无用的连接对象
                continue  # 监测下一个对象
```
> 存在缺陷, 当监测对象的量过大时，会造成较大的延时

**补充**

`io`多路复用的机制由以下几个

1. `select`机制：存在与windows和linux系统
2. `poll`机制：只在linux系统上有效
3. `epoll`机制：只在linux系统上有效
    ![epoll工作机制](https://images.gitee.com/uploads/images/2020/1117/011201_ed8a12dd_7841459.png "屏幕截图.png")
> 1. `select/poll`机制存在缺陷，当监测对象的量过大时，会造成较大的延时
> 2. `epoll`机制是较为完美的机制, 基于 **惰性** 的 **事件回调机制**； **惰性的事件回调** 是由用户自己调用的，操作系统只起到通知的作用

### 64.3.2 selectors模块
由于`io`多路复用机制多，且各个不同的平台存在一定兼容性问题。python内置`selectors`模块提供了根据平台选择`IO`多路复用机制，同一的编程规范。基本使用
|方法|描述|
|:---:|:---:|
|`selector = selectors.DefaultSelector()`|根据平台选择io多路复用机制|
|`selector.register(要监控的对象, 事件编号, 回调函数)`|注册回调事件|
|`selector.unregister(被监控的对象)`|取消注册的事件|

> 事件编号:
> 1. `EVENT_READ = (1 << 0)`: 读事件, 常用
> 2. `EVENT_WRITE = (1 << 1)`: 写事件，一半情况下不用

**基于selectors实现tcp并发服务端**
```python
import socket
import selectors

server = socket.socket()

server.bind(('127.0.0.1', 8080))

server.listen()

epoll_selector = selectors.DefaultSelector()  # 根据平台选择io多路复用机制


def read(connection):
    recv_data = connection.recv(1024)
    if recv_data:
        print(f"客户端{connection.getpeername()}发来消息:{recv_data.decode()}")
        connection.send(recv_data)
    else:
        epoll_selector.unregister(connection)  # 客户端断开连接，取消注册的事件
        connection.close()


def accept(sev):  # 接受连接监测
    connection, address = sev.accept()
    print(f'{address}建立连接')
    epoll_selector.register(connection, selectors.EVENT_READ, read)  # 连接成功后注册read为回调函数，将来有消息发来就会调用read函数


epoll_selector.register(server, selectors.EVENT_READ, accept)  # 将建立连接注册为事件,只要有链接就调用接受连接这个函数

while True:
    event = epoll_selector.select()  # 查询准备好的事件, 返回一个列表，存放的是一个元组(SelectorKey对象, _EventMask)
    for key, mask in event:
        print(key, mask)
        # key: SelectorKey(fileobj=<socket.socket fd=448, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8080), raddr=('127.0.0.1', 60536)>, fd=448, events=1, data=<function read at 0x0000011982A47310>)
            # fileobj: 连接对象
            # data: 回调函数
        # mask: 1
        callback = key.data  # 获取回调函数
        sock = key.fileobj  # 文件句柄，连接在操作系统中是以文件形式存在
        callback(sock)  # 将连接传入回调函数，调用函数
```

## 64.4 `Asynchronous IO`异步`IO`模型

![输入图片说明](https://images.gitee.com/uploads/images/2020/1117/084247_6f8acf46_7841459.png "屏幕截图.png")

当应用程序调用`aio_read`时，内核一方面去 **取数据报内容** 返回，另一方面进程将 **程序控制权还给应用** ，应用进程继续处理其他事情，是一种非阻塞的状态。

当内核中有数据报就绪时，由内核将数据报拷贝到应用程序中，返回`aio_read`中定义好的函数处理程序。
> 1. 异步IO模型是效率最高的模型
> 2. 原生python代码是无法实现异步IO模型的，需要内置模块`asyncio`和异步框架(`sanic`, `tornado`, `twisted`)提供支持


### 64.4.1 `asyncio`模块
```python
import asyncio


@asyncio.coroutine  # 将要被删除 使用async/await代替
def hello():
    print("hello world")
    yield from asyncio.sleep(1)
    print("hello again")


loop = asyncio.get_event_loop()  # 监测事件
tasks = [hello(), hello()]  # 任务列表
loop.run_until_complete(asyncio.wait(tasks))  # asyncio.wait(tasks)等待任务
loop.close()
``` 

* **`async/await`**原生协程实现异步`IO`
```python
import asyncio

async def hello():  # 此处将@asyncio.coroutine 修改为async
    print("hello world")
    await asyncio.sleep(1)   # 将yield from修改为await
    print("hello again")


loop = asyncio.get_event_loop()  # 监测事件
tasks = [hello(), hello()]  # 任务列表
loop.run_until_complete(asyncio.wait(tasks))  # asyncio.wait(tasks)等待任务
loop.close()

```







