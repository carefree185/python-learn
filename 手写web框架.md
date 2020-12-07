# 一、手写web框架
## 1.1 http协议
超文本传输协议，规定了浏览器与服务器之间数据交互的格式。传输数据不进行加密

**特性**
1. 基于请求和响应
2. 基于tcp/ip作用在应用层的协议
3. 无状态
4. 无连接

**数据格式**
* 请求数据格式
    1. 请求首行
    2. 请求头
    3. `\r\n`
    4. 请求体，提交的服务器的数据
* 响应数据格式
    1. 响应首行
    2. 响应头
    3. `\r\n`
    4. 响应数据，服务器返回的数据


## 1.2 https协议
加密的超文本传输协议，规定了浏览器与服务器之间数据交互的格式。传输数据进行加密

## 1.3 socket实现简单的web框架
```python
import socket

server = socket.socket()  # 创建服务端套接字
server.bind(("127.0.0.1", 8080))  # 绑定ip和端口
server.listen(5)  # 监听链接

"""
b'GET / HTTP/1.1\r\n  请求行，包含了 请求方法 请求路径 http版本 
Host: 127.0.0.1:8080\r\n
Connection: keep-alive\r\n
Cache-Control: max-age=0\r\n
Upgrade-Insecure-Requests: 1\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n
Sec-Fetch-Site: none\r\n
Sec-Fetch-Mode: navigate\r\n
Sec-Fetch-User: ?1\r\n
Sec-Fetch-Dest: document\r\n
Accept-Encoding: gzip, deflate, br\r\n
Accept-Language: zh-CN,zh;q=0.9\r\n
\r\n'

"""

while True:
    conn, addr = server.accept()  # 接受链接
    data = conn.recv(1024)  # 接受数据
    conn.send(b"HTTP/1.1 200 OK\r\n\r\n")  # 返回响应头
    request_header = data.decode().split(" ")

    with open("myhtml.html", 'rb') as f:
        html = f.read()
    conn.send(html)  # 返回html文件
    if len(request_header) >= 2:
        conn.send(request_header[1].encode())  # 获得访问路径，并返回

    conn.close()  # 关闭链接
```
> **不足** 
> 1. 代码重复
> 2. 处理http数据不完善，只能拿到url后缀，其他数据获取繁琐（数据格式一样，处理数据的逻辑将会是一致的）
> 3. 并发问题

## 1.4 `wsgiref`模块实现web框架
* `urls.py`: 用于存放路由与视图函数的对应关系
    ```python
    """
    路由与视图函数的的对应关系
    """
    
    from views import *
    
    # url与函数的对应
    urls = [
        ("/index", index),
        ("/login", login),
        ("/xxx", xxx)
    ]
    ```
* `views.py`: 存放视图函数
    ```python
    """
    存放视图函数
    """
    
    
    def index(env):
        return "index"
    
    
    def login(env):
        return "login"
    
    
    def xxx(env):
        return "xxx"
    
    
    def error(env):
        return "404 ERROR"
    ```
* `run.py`：框架运行启动文件
    ```python
    from wsgiref.simple_server import make_server
    from urls import urls
    from views import error
    
    
    def run(env, response):
        """
        :param env: 一个字典，请求相关的所有数据以及其他相关数据
        :param response: 响应相关的所有数据
        :return: 返回给浏览器的数据
        """
        response("200 OK", [])
        current_path = env.get("PATH_INFO")
        # if current_path == "/index":
        #     with open("login.html", "rb") as f:
        #         return [f.read()]
        # else:
        #     return [b"404 error"]
    
        func = None
        for url in urls:
            if current_path in url:
                func = url[1]
                break  # 匹配到一个url后结束循环
    
        if func is not None:  # 循环结束后，可能存在func==None
            res = func(env)
        else:
            res = error(env)
    
        return [res.encode()]
    
    
    if __name__ == '__main__':
        server = make_server("127.0.0.1", 8080, run)  # 实时监听指定地址，只要有客户链接就会出发run函数运行
        server.serve_forever()  # 启动服务的
    ```
# 二、动静态网页
* 静态网页
    > **页面上的数据不发生改变，数据在html上确定**

* 动态网页
    > **数据是实时从后端获取，数据会随时发生改变的网页**
    ```python
    def get_time(env):
        """
        获取时间返回给html
        :param env:
        :return:
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %X")
        with open("templates/time.html", 'r', encoding="utf-8") as f:
            data = f.read()
            data = data.replace("xxx", current_time)  # 处理html文件，然后返回给前端
    
        return data
    ```

# 三、jinja2模板初始

**模板语法**: 在后端处理好后返回给浏览器
```html
<h1>获取后端数据</h1>
{{user}}
username: {{user.get("username")}} 或 {{user["username"]}}
age: {{user.age}}
```
**后端代码**
```python
from jinja2 import Template
def get_dict(env):
    user_dict = {"username": "dyp", "age": 20}
    with open("templates/get_dict.html", "r", encoding="utf-8") as f:
        data = f.read()

    tmp = Template(data)
    res = tmp.render(user=user_dict)  # 给页面传值
    return res
```

# 四、后端获取数据库数据
**模板语法**
```html
{% for user_dict in user_list%}
    <tr>
        <td>{{user_dict.id}}</td>
        <td>{{user_dict.username}}</td>
        <td>{{user_dict.password}}</td>
    </tr>
{% endfor %}
```
**后端逻辑**
```python
from jinja2 import Template
def get_user(env):
    # 从数据库获取数据，通过模板语法处理后返回给html
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        charset="utf8",
        user="root",
        password="dyp1996",
        database="djangodb",
        autocommit=True
    )

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from user"
    cursor.execute(sql)
    res_list = cursor.fetchall()
    print(res_list)
    # 将获取好的数据传递给html文件
    with open("templates/get_user.html", "r", encoding="utf-8") as f:
        data = f.read()
    tmp = Template(data)
    res = tmp.render(user_list=res_list)
    return res
```

# 五、web框架请求流程

![](https://images.gitee.com/uploads/images/2020/1207/221459_94ae653c_7841459.png "web框架流程图.png")





