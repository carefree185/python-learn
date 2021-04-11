# flask request

**登录页面**
```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
```
* `methods=['GET', 'POST'`: 指定请求方式
* 该搭建了一个登录页面，下面开flask请求对象学习

## 一 请求对象
flask的视图函数不接收请求对象，请求对象在flask中进行接收的。使用请求对象时，
需要进行导入
```python
from flask import request
```

1. 获取当前请求的请求方式: `request.method`
   
2. 获取`post`请求提交的数据信息: `request.form`
    * 返回的是一个类似于字典的对象，可以调用字典的方法获取值
    * 可以调用`.to_dict()`方法转为字典。

3. `request.values`: 接收`get`和`post`两种方式提交的数据
    * 可以调用`.to_dict()`方法转为字典。
    
4. `request.args`: 接收`get`方式提交的参数
    * 返回的是一个类似于字典的对象，可以调用字典的方法获取值
    * 可以调用`.to_dict()`方法转为字典。

5. `request.files`: 保存提交过来的文件数据
    * 返回的是一个类似于字典的对象，可以调用字典的方法获取
    * 可以从字典中取出一个`FileStorage`对象，该对象是`flask`提供的文件处理对象
    * `fileStorage.save(文件名)`: 保存文件
    * `fileStorage.filename`: 文件名，包含扩展名

**使用示例**
```python
import os

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        print(request.url)  # 完整的url
        print(request.url_root)  # 请求地址，host
        print(request.url_rule)  # 路由
        print(request.url_charset)  # url的编码
        print(request.values)  # 包含了get和post两种请求方式提交的数据
        print(request.args)
        print(request.args.to_dict())
        return render_template("login.html")
    else:
        print(request.form)  # form表单提交的参数，FormData数据。post提交的数据
        print(request.form.to_dict())  # 转为字典
        print(request.files.to_dict())
        # 上传并保存文件
        file = request.files.get("file")
        path = os.path.join("xht", file.filename)
        file.save(path)

        return "200 ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
```
****

**其他数据获取**
1. `request.headers`: 请求头
2. `request.cookies`: cookie信息
3. `request.path`: 路由
4. `request.host`: `ip:port`
5. `request.host_url`: `http://ip:port/`

**特殊的content-type**
1. 当content-type为`application/json`，数据保存在`request.json`和`request.data`中

2. 当content-type不能被识别，或者与Form不相关时，数据保存在`request.data`


