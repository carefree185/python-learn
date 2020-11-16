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



