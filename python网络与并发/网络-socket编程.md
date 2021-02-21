# 五十、socket
`Socket`是应用层与`TCP/IP`协议族通信的中间软件抽象层，它是一组接口。在设计模式中，`Socket`其实就是一个**门面模式**，它把复杂的`TCP/IP`协议族隐藏在`Socket`接口后面，对用户来说，一组简单的接口就是全部，让`Socket`去组织数据，以符合指定的协议.
## 50.1 `socket`发展史及分类
套接字起源于 20 世纪 70 年代加利福尼亚大学伯克利分校版本的 `Unix`,即人们所说的 `BSD Unix`。 因此,有时人们也把套接字称为“伯克利套接字”或“BSD 套接字”。一开始,套接字被设计用在同 *一台主机上多个应用程序* 之间的通讯。这也被称进程间通讯,或 `IPC`。套接字有两种（或者称为有两个种族）,分别是基于文件型的和基于网络型的。

* **基于文件类型的套接字家族(AF_UNIX)**
unix一切皆文件，基于文件的套接字调用的就是底层的文件系统来取数据，两个套接字进程运行在同一机器，可以通过访问同一个文件系统间接完成通信

* **基于网络类型的套接字家族(AF_INET)**
(还有`AF_INET6`被用于`ipv6`，还有一些其他的地址家族，不过，他们要么是只用于某个平台，要么就是已经被废弃，或者是很少被使用，或者是根本没有实现，所有地址家族中，`AF_INET`是使用最广泛的一个，python支持很多种地址家族，但是由于我们只关心网络编程，所以大部分时候我么只使用`AF_INET`)

## 50.2 socket工作流程
![输入图片说明](https://images.gitee.com/uploads/images/2020/0919/201506_dbd0ecfc_7841459.jpeg "socket工作流程.jpg")

## 50.3 基于`tcp\ip`的`socket`编程
|                  socket常用的方法                   |                             描述                             |
| :-------------------------------------------------: | :----------------------------------------------------------: |
| `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` |                  创建`tcp`服务端socket对象                   |
|            `socket对象.bind((ip,port))`             |                        绑定`ip`和端口                        |
|                `socket对象.listen()`                |                   监听客户端发起的连接请求                   |
|                `socket对象.accept()`                | 接受客户端连接请求，返回用于与客户端通信的**对等socket对象**，和**客户端的`ip`和端口** |
|             `对等socket对象.recv(int)`              |                     接受客户端发来的消息                     |
|             `对等socket对象.send(data)`             |                       向客户端发送消息                       |
|                `socket对象.close()`                 |                           关闭连接                           |
|`对等socket对象.getpeername()`|获取客户端的ip地址和端口|

* 简单服务端
    ```python
    import socket
    
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_STREAM  --> tcp
    sock_server.bind(("192.168.194.105", 8080))  # 绑定服务端程序运行的ip和端口
    sock_server.listen(__backlog=5)  # 监听客户端的链接请求, backlog设置半连接池大小
    connect, address = sock_server.accept()  # 接受链接，返回与客户端链接的socket对象和客户端的ip和端口
    print(connect)
    print(address)
    data = connect.recv(1024)  # 接受客户端发送来的数据, 参数表示每次接收的数据大小(单位为Bytes)
    print(data.decode())
    connect.close()  # 关闭连接
    sock_server.close()
    ```
    > 1. `socket.AF_INET`: `ipv4`协议族
    > 2. `socket.SOCK_STREAM`: `tcp`协议
    > 3. `socket.socket()`: 创建`socket`对象
* 简单客户端
```python
import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建tcp/ip客户端socket对象
connection.connect(("192.168.56.1", 8080))  # 链接客户端
connection.send("hello world".encode())  # 向服务端发送数据
connection.close()  # 关闭连接
```

**存在bug**
> 1. 当发送空数据时客户端卡死
> 2. 只能服务端只能服务一个客户，且服务完成后服务端就结束
> 3. 客户端非正常退出时，导致服务端错误
> 4. 客户端只能发送一次数据

**解决bug完成后的代码**
* 服务端
    ```python
    import socket
    
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_STREAM  --> tcp
    sock_server.bind(("192.168.56.1", 8080))  # 绑定服务端程序运行的ip和端口
    print(f"服务端运行于: {('192.168.56.1', 8080)}")
    sock_server.listen(5)  # 监听客户端的链接请求, backlog设置半连接池大小
    while True:
        connect, address = sock_server.accept()  # 接受链接，返回与客户端链接的socket对象和客户端的ip和端口
        print(f"客户端{address}与服务端{('192.168.56.1', 8080)}建立链接")
        while True:
            try:  # 解决Windows下服务端，客户端强制关闭链接导致服务端异常问题
                recv_data = connect.recv(1024)  # 接受客户端发送来的数据, 参数表示每次接收的数据大小(单位为Bytes)
                if recv_data:  # 解决unix/linux服务端，客户端强制关闭链接导致服务端异常问题
                    print(f"客户端{address}发送的消息 ", recv_data.decode())
                    connect.send(recv_data.upper())  # 向客户端响应数据
                else:
                    connect.close()  # 关闭与客户端的连接
                    break
            except ConnectionResetError as e:
                print(e)
                break
    ```
* 客户端
    ```python
    import socket
    
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("192.168.56.1", 8080))
    while True:
        msg = input("输入要发送的数据:").strip()
        if not msg:
            continue
    
        if msg == "quit":  # 退出客户端
            break
        connection.send(msg.encode())  # 向服务端发送消息
        recv_data = connection.recv(1024)  # 接服务端返回的消息
        print(f"服务端{('192.168.56.1', 8080)}返回的信息", recv_data.decode())
    
    connection.close()  # 关闭客户端与服务端的链接
    ```

**基于`tcp`协议实现远程命令执行**
* 客户端
    ```python
    import socket
    import struct
    
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("192.168.56.1", 8080))
    while True:
        msg = input("输入要执行的命令:").strip()
        if not msg:
            continue
    
        if msg == "quit":  # 退出客户端
            break
    
        connection.send(msg.encode())  # 向服务端发送消息
    
        ### 粘包问题客户端解决
        total_size = struct.unpack('i', connection.recv(4))[0]
        recv_size = 0
        while recv_size < total_size:
            recv_data = connection.recv(1024)  # 接服务端返回的消息
            recv_size += len(recv_data)
            print(f"服务端{connection.getpeername()}命令执行结果: ", recv_data.decode("GBK"))
        ###
    
    connection.close()  # 关闭客户端与服务端的链接
    ```
* 服务端
    ```python
    import socket
    import subprocess
    import struct
    
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_STREAM  --> tcp
    sock_server.bind(("192.168.56.1", 8080))  # 绑定服务端程序运行的ip和端口
    print(f"服务端运行于: {('192.168.56.1', 8080)}")
    sock_server.listen(5)  # 监听客户端的链接请求, backlog设置半连接池大小
    while True:
        connect, address = sock_server.accept()  # 接受链接请求，返回与客户端链接的socket对象和客户端的ip和端口
        print(f"客户端{address}与服务端{('192.168.56.1', 8080)}建立链接")
        while True:
            try:  # 解决Windows下服务端，客户端强制关闭链接导致服务端异常问题
                recv_data = connect.recv(1024)  # 接受客户端发送来的数据, 参数表示每次接收的数据大小(单位为Bytes)
                if recv_data:  # 解决unix/linux服务端，客户端强制关闭链接导致服务端异常问题
                    print(f"客户端{address}要执行的命令: ", recv_data.decode())
                    obj = subprocess.Popen(
                        recv_data.decode(),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    
                    stdout_res = obj.stdout.read()
                    stderr_res = obj.stderr.read()
                    #### 解决粘包问题  先发送数据头
                    total_size = len(stdout_res) + len(stderr_res)  # 数据的描述，数据的总长度
                    connect.send(struct.pack('i', total_size))  # 将数据总大小传回客户端
                    ####
    
                    connect.send(stdout_res)  # 向客户端响应数据
                    connect.send(stderr_res)  # 向客户端响应数据
                else:
                    connect.close()  # 关闭与客户端的连接
                    break
            except ConnectionResetError as e:
                print(e)
                break
    
    ```

> **粘包问题**
> 1. `tcp`协议的数据传输会像水流一样，每次传送的数据都会拼接在一起
> 2. 由于数据接收者在接收数据时，可能会接收的不完全。下一次传送过来的数据就会和本次数据结合，造成数据粘包
> 
> **解决方案**: *循环的接收数据* 
> 1. 获取数据的总大小并将其转为固定字节长度(使用struct模块)，先发送数据包的头，其中包括了数据的总大小
> 2. 分批次接收数据，根据

**基于`tcp`的文件上传下载服务**
```python

```


















