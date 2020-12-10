# 一、模板语法
1. `{{ }}`: 取变量的值时使用

2. `{% %}`: 设计到逻辑相关时使用

3. `{# #}`: 单行注释

4. `{%comment%} 被注释的内容 {%endcoomment%}`: 多行注释

# 二、可以传递的数据类型
1. python基本数据类型均可以传递到html模板之中
2. 传递函数名会自动调用，但是不能给函数传递参数，如果函数需要参数，则不执行
3. 传递类名时，也会自动实例化产生对象。

**模板会自动判断传递到`html`模板对象是否为可以调用对象，如果是可调用对象，则自动调用**
> 针对函数名和类名

# 三、获取后端传给模板的值`{{ 传递过来的变量名 }}`
```html
<p>整形: {{ n }}</p>
<p>浮点型: {{ f }}</p>
<p>布尔性: {{ b }}</p>
<p>字符串: {{ s }}</p>
<p>列表: {{ l }}</p>
<p>元组: {{ t }}</p>
<p>字典: {{ d }}</p>
<p>集合: {{ se }}</p>
<p>函数: {{ func }}</p>
<p>类: {{ MyClass }}</p>
<p>对象: {{ obj }}</p>
<p>调用类方法: {{ MyClass.get_cls }}</p>
<p>调用对象方法: {{ obj.get }}</p>
<p>调用对象的静态方法: {{ obj.get_func }}</p>
```
**注意**
* 对于可调用对象，模板会自动调用，获得其返回值

## 3.1 获取后端传递对象的值`{{ 变量名.key(变量名.index)}}`
```html
<h2>获取非值对象中的值</h2>
<p>列表/元组取值(list.索引): {{ l.0 }}</p>
<p>字典取值(dict.key): {{ d.username }}</p>
```

# 四、过滤器
过滤器类似是模板语法的方法。

## 4.1 内置过滤器`{{数据|过滤器:参数}}`
> 一共有60几个过滤器

* 统计长度`{{ 可迭代对象|lenght }}`

* 默认值`{{ 对象|default: "默认值" }}`, 如果对象为`True`返回对象的值, `False`返回默认值

* 文件大小`{{ file_size| filesizeformat }}`，自动计算出文件的大小

* 时间日期格式化`{{ current_time|date:'Y-m-d H:i:s' }}`

* 切片操作`{{ 可迭代对象|slice:"start:end:step" }}`

* 截取字符`{{ 字符串|truncatechars:size }}`，`size`指定长度，末尾三个点(`...`)也计算到`size`中

* 截取单词`{{ 字符串|truncatewords:size }}`，`size`截取单词个数，按空格截取

* 移出特点字符`{{ 字符串|cut:'指定字符' }}`

* 拼接`{{ 可迭代对象|join:"拼接使用的字符" }}`, 使用指定字符，将可迭代对象中的数据拼接成字符串

* 取消转义`{{ 标签|safe }}`, 标签，默认是不被解析的，
    * 在后端取消转义
        ```python
        from django.utils.safestring import mark_safe
        h2 = mark_safe("<h2>我是安全的</h2>")
        ```
## 4.2 自定义过滤器
* 第一步, 必须要在`app_name`下创建名为`templatetags`文件夹
* 第二步, 在`templatetages`文件夹下创建任意名称的`py`文件(推荐创建`customer_filters.py`)
* 第三步, 在`customer_filters.py`文件内必须下如下内容
    ```python
    from django import template

    register = template.Library()
    ```
* 第四步，自定义过滤器，并注册过滤器
    ```python
    @register.filter(name="filter_name")  # 注册过滤器
    def filter_function(value, arg2):
        return value + arg2
    ```
* 第五步，在模板页面引入过滤器文件
    ```django
    {% load customer_filters %}  {# 导入自定义过滤器文件 #}
    ```
* 第六步，使用注册时给过滤器取的名字，使用过滤器
    ```django
    {{ value|filter_name:arg2 }}
    ```
> **过滤器最少一个参数，最多两个参数**


# 五、标签

## 5.1 for循环标签

```django
{% for var_name in iterable %}
    ...
{% empty %} {# iterable 为空 #}
    ...    
{% endfor %}
```
> 1. 循环标签有一个自带的变量`forloop`对象，包含如下几个属性
![输入图片说明](https://images.gitee.com/uploads/images/2020/1210/195641_8c466098_7841459.png "屏幕截图.png")

## 5.2 if判断标签
```django
{% if 条件1 %}
    <p>条件1成立执行此处</p>
{% elif 条件2 %}
    <p>条件1不成立且条件2成立执行此处</p>
{% else %}
    <p>条件1和条件2均不成立执行此处</p>
{% endif %}
```

## 5.3 自定义标签
* 第一步，在`templatetags`文件夹下面创建任意命名的`py`文件(推荐`customer_tags.py`）
* 第二步，在创建的文件(`customer_tags.py`)内必须下如下内容
    ```python
    from django import template

    register = template.Library()
    ```
* 第三步，自定义标签，并注册
    ```python
    @register.simple_tag(name="tag_name")  # 注册标签
    def tag_function(arg1, arg2):
        return "%s-%s" % (arg1, arg2)
    ```
* 第四步，在模板中导入标签
    ```django
    {% load custormer_tags %}
    ```
* 第五步，使用标签
    ```django
    {% tag_function arg1 arg2 %}
    ```

## 5.4 自定义inclusion_tag
 **通过渲染另一个模板来展示数据** 
1. 先定义一个方法，注册为inclusion_tag
    ```python
    # 自定义inclusion_tag
    @register.inclusion_tag("left.html")
    def left(n):
        data = ["{}".format(i) for i in range(n)]
        # return locals()
        return {"data": data}  # 给被渲染页面传值
    ```
2. 在页面上使用该标签，会触发方法的运行
    ```django
    <h2>自定义inclusion_tag</h2>
    {% left 5 %}
    ```
3. 该方法会取渲染一个模板
4. 将渲染好的模板返回到该标签的位置

**当某个页面的某一段html代码需要传递一些参数才能渲染出来时，且在多个页面也需要渲染这个端html代码，使用自定义inclusion_tag**




# 六、别名
```django
{% with 对象 as 别名 %}
    {# 这里面可以使用别名来指代数据 #}
{% endwith %}
```

# 七、模板继承`{% extends '被继承的模板' %}`与模板扩展`{% block name %} {% endbloack %}`
* **base.html**
    ```django
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
        <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
        <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>   <!--bootstrap依赖jQuery-->
    </head>
    <body>
    <nav class="navbar navbar-inverse">
      <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Brand</a>
        </div>
    
        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Link <span class="sr-only">(current)</span></a></li>
            <li><a href="#">Link</a></li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="#">Action</a></li>
                <li><a href="#">Another action</a></li>
                <li><a href="#">Something else here</a></li>
                <li role="separator" class="divider"></li>
                <li><a href="#">Separated link</a></li>
                <li role="separator" class="divider"></li>
                <li><a href="#">One more separated link</a></li>
              </ul>
            </li>
          </ul>
          <form class="navbar-form navbar-left">
            <div class="form-group">
              <input type="text" class="form-control" placeholder="Search">
            </div>
            <button type="submit" class="btn btn-default">Submit</button>
          </form>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">Link</a></li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="#">Action</a></li>
                <li><a href="#">Another action</a></li>
                <li><a href="#">Something else here</a></li>
                <li role="separator" class="divider"></li>
                <li><a href="#">Separated link</a></li>
              </ul>
            </li>
          </ul>
        </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="list-group">
                  <a href="{% url 'app01:home' %}" class="list-group-item active">
                    首页
                  </a>
                  <a href="{% url 'app01:login' %}" class="list-group-item">登录</a>
                  <a href="{% url 'app01:reg' %}" class="list-group-item">注册</a>
                </div>
            </div>
            <div class="col-md-9">
                <div class="panel panel-primary">
                  <div class="panel-heading">Panel heading without title</div>
                  <div class="panel-body">
                    Panel content
                  </div>
                </div>
    
                <div class="panel panel-primary">
                  <div class="panel-heading">
                    <h3 class="panel-title">Panel title</h3>
                  </div>
                  <div class="panel-body">
    
                    <div class="jumbotron">
                      {% block content %} {# 划定修改位置 #}
                          <h1>Hello, world!</h1>
                          <p>...</p>
                          <p><a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a></p>
                      {% endblock %}
                    </div>
    
                  </div>
                </div>
            </div>
    
        </div>
    
    </div>
    
    </body>
    </html>
    ```
    
* **继承模板base.html**
    ```django
    {% extends "base.html" %}
    ```
* **修改继承的模板**
    ```django
    {% block content %}  {# 修改划定的位置 #}
        <h1 class="text-center">注册页面</h1>
        <form action="" method="post">
            <p>
                <label for="user">输 入 用 户 名:</label>
                <input type="text" name="username" id="user" class="form-control">
            </p>
            <p>
                <label for="pwd">输 入 密 码:</label>
                <input type="password" name="password" id="pwd" class="form-control">
            </p>
    
            <input type="submit" class="btn btn-danger btn-block">
        </form>
    {% endblock %}
    ```
    * 可以被修改的位置一般要有三个可以被修改的区域，这样每一个页面可以单独定制样式和动画
        * 1. `CSS`区域
        * 2. `JS`区域
        * 3. `HTML`区域

# 八、模板导入`{% include '被引入的模板'%}`

将页面的某个局部`html`当成模块，哪里要使用就在那里导入。导入后，会将被导入的html代码直接插入到导入的页面
    ```django
    {% include "要被导入的模板" %}
    ```