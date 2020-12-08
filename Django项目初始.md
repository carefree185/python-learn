# 一、路由配置

在`项目文件夹/view.py`文件下添加如下
```python
from django.conf.urls import url
from django.contrib import admin
from app01 import views  # 导入视图函数文件

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),  # 添加的路由与视图函数绑定关系
]
```
# 二、模板文件夹路径配置
在`项目文件夹/settings.py`文件找到`TEMPLATES`进行如下修改
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 添加模板路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

# 三、视图函数
在`app_name/views.py`文件中编写路由绑定的函数
```python
def index(request):
    """
    与index路由绑定的函数
    :param request: 请求相关的所有数据
    :return:
    """
    # return HttpResponse("你好 我是Django")  # 用来返回字符串
    # return render(request, "first.html")  # 配置templates文件路径，会自动查找html文件
    # return redirect('https://www.baidu.com')  # 重定向到指定路由或url
    return redirect('/admin/')
```
> 1. `HttpResponse(字符串)`: 返回字符串
> 2. `render(request, template)`: 返回html文件
> 3. `redirect(to)`: 重定向 

**模板渲染的过程**
```python
def template_render(request):
    """
    模板渲染过程
    :param request:
    :return:
    """
    temp = get_template('first.html')
    html = temp.render()
    return HttpResponse(html)
```

## render函数向模板传值方式
1. `render(request, template, {key: value})`: 在模板中获取到`key`对应的`value`值
2. `render(request, template, locals())`: 将当前作用域中的变量全部传入到模板中，适用于模板使用后端数据较多的情况

# 四、登录功能实现
## 4.1 静态文件路径配置
1. 我们的web后端将html文件存放在`template`文件夹中
2. 对于静态文件存放在`static`目录下
    * **静态文件** : 已经写好的样式(`css`), 动画(`js`), 图片(`img`)等不用经常修改的文件称为静态文件.  **通常会在static目录下在创建这上目录** 
    * 创建`static`目录，将使用的样式动画图片等存放在`static`目录下
3. 我们在访问url时，能够拿到资源是后台开放了该资源的访问接口。在没有配置静态路径的情况下，静态资源是不能被访问获得的。如下图报错
![输入图片说明](https://images.gitee.com/uploads/images/2020/1208/145959_206804d8_7841459.png "屏幕截图.png")

**配置静态文件路径**
1. 在`settings.py`中配置
    ```python
    STATIC_URL = '/static/'  # 访问静态文件的开头
    # 静态文件配置
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),  # 拼接静态文件的路径
    ]
    ```
    > 访问路径为`/static/`开头的路径，`Django`将允许在静态文件路径中查找文件.
    > * `STATIC_URL`其实就是访问静态文件的校验头。
    > * 凡是以`STATIC_URL`开头都将被允许访问静态文件中的文件

2. 在`html`页面上配置
> 1. 使用模板语法导入`STATIC_URL`: `{% load static %}`
    ```html
    {% load static %}
    ```
> 2. 在要使用静态文件的位置使用模板语法拼接静态文件路径: `{% static "文件所在的路径" %}`
>    * 文件路径为 **去除静态文件夹后的路径** 
>
>    ```html
>    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
>    <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
>    <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>
>    ```

## 4.2 登录功能的实现
1. `form`表单默认为`get`方式提交数据
    * `action`参数描述
        * `action = ""`: 默认项当前url`提交数据 
        * `action = "url"`: 向指定位置提交数据
        * `action = "url后缀"`: 自动补全当前后端的`ip:port`
    * `get`方式提交数据, 数据直接在`url`中提交的
        * `http://ip:port/action/?name=value&name=value`
    * `post`方式提交数据，数据在请求体中存放。

**在提交post请求出现403页面需要在配置文件中修该以下代码**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**登录页面**
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
    <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
    <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>
</head>
<body>
<h1 class="text-center">登录</h1>
<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
            <form action="" method="post">
                <p>
                    <label for="user">用户名:</label>
                    <input type="text" name="username" id="user" class="form-control">
                </p>
                <p>
                    <label for="pwd">密&emsp;码:</label>
                    <input type="password" name="password" id="pwd" class="form-control">
                </p>
                <input type="submit" class="btn btn-success btn-block">
            </form>
        </div>
    </div>
</div>
</body>
</html>
```

**后端代码** : 写在`app_name/views.py`文件下
```python
def login(request):
    """
    登录功能
    :param request:
    :return:
    """
    print("欢迎")
    return render(request, "login.html")
```

**此时post请求和get请求触发的是同一个视图函数。不符合开发要求**，下面实现分离`get`和`post`请求出发不同的逻辑

## 4.3 `request`对象初体验(获取用户输入的数据)
封装的请求数据对象，里面有很多属性和方法。

1. 获取请求的请求方式: `request.method`, 返回的是字符串，全大写
2. 获取`post`请求方式提交的数据: `request.POST`, 返回的是一个字典
    * `request.POST.get("key")`: 获取key对应列表的最后一个值
    * `request.POST.getlist("key")`: 获取key对应的列表元素
    * `post`请求提交的数据没有大小限制
    ```python
    username = request.POST.get("username")  # 只获取username对应列表的最后一个值
    hobby = request.POST.getlist("hobby")  # 获取hobby对应的列表
    print(username, hobby)
    ```
3. 获取`get`请求方式提交的数据：`request.GET`, 返回一个字典
    * 获取用户提交的数据与`post`方式一模一样
    * `get`请求提交的数据是有大小限制的

```python
def login(request):
    """
    登录功能
    :param request:
    :return:
    """
    print(request.method)  # 获取请求方式，返回的是字符串，全大写
    if request.method == "POST":
        # 获取post方式提交数据
        print(request.POST)  # 获取post提交的数据，不包含文件，返回的是一个字典<QueryDict: {'username': ['dyp'], 'password': ['111']}>
        username = request.POST.get("username")  # 只获取username对应列表的最后一个值
        hobby = request.POST.getlist("hobby")  # 获取hobby对应的列表
        print(username, hobby)
        return HttpResponse("等待数据校验")

    print(request.GET)  # <QueryDict: {'username': ['dyp'], 'password': ['111'], 'hobby': ['111', '222', '333']}>
    print(request.GET.get("hobby"))
    print(request.GET.getlist("hobby"))

    return render(request, "login.html")
```

## 4.4 借助`pymysql`实现用户登录
```python
def login(request):
    """
    登录功能
    :param request:
    :return:
    """
    print(request.method)  # 获取请求方式，返回的是字符串，全大写
    if request.method == "POST":
        # 获取post方式提交数据
        print(request.POST)  # 获取post提交的数据，不包含文件，返回的是一个字典<QueryDict: {'username': ['dyp'], 'password': ['111']}>
        username = request.POST.get("username")  # 只获取username对应列表的最后一个值
        password = request.POST.get("password")  # 获取password对应列表的最后一个值
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
        sql = "select * from user where username=%s and password=%s"
        cursor.execute(sql, (username, password))
        res_list = cursor.fetchall()
        if res_list:
            return HttpResponse("登录成功")
        return HttpResponse("用户名或密码错误")
    return render(request, "login.html")
```






