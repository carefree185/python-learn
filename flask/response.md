# flask response
flask返回数据的方式有如下几种

## 一 返回字符串
返回字符串直接使用`return 字符串`即可完成数据返回
```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"  # 返回字符串数据


if __name__ == '__main__':
    app.run()
```
## 二 返回模板页面
flask使用的Jinja2模板字符串来处理和渲染页面。要返回html页面时需要使用到
函数`render_template(template_name_or_list, *context)`. 

* flask处理模板保存的**默认目录为`templates`**

```python
from flask import Flask  # Flask类
from flask import render_template  # 用于返回模板的函数

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
```

## 三 路由跳转
需要调整路由时，需要使用`redirect()`函数进行路由跳转
```python
from flask import Flask  # Flask类
from flask import render_template  # 用于返回模板的函数
from flask import redirect

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/to_home")
def to_home():
    return redirect("/home")    # 跳转路由到/home


if __name__ == '__main__':
    app.run(debug=True)
```

## 四 返回文件
flask可以直接返回文件，需要调用`send_file(文件路径)`即可。调用该函数返回
时，flask会在ResponseHeader中添加content-type建指定文件类型，交给客户端
进行识别。如果客户端能够识别直接展示出来，不能识别可以采用其他方法进行处理
```python
from flask import Flask, send_file 
app = Flask(__name__)

@app.route("/get_file")
def get_file():
    return send_file("first_flask.py")  
    # 1. 打开文件，并返回文件的内容。
    # 2. 修改Response Header中conten-type为文件的类型

if __name__ == '__main__':
    app.run(debug=True)
```

## 五 返回json格式字符串
flask返回json格式字符串需要使用`jsonify()`函数即可
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/get_json")
def get_json():

    d = {
        "name": "杜宇鹏",
        "age": 25
    }
    return jsonify(d)  # return d 这样也可返回json格式字符串


if __name__ == '__main__':
    app.run(debug=True)
```



