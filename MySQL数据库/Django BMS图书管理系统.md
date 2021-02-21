# 一、首页搭建
**图书管理系统的首页** 
![](https://images.gitee.com/uploads/images/2020/1212/171544_07fac13c_7841459.png "屏幕截图.png")

## 1.1 前端模板
```html
{% load static %}  <!--导入静态文件标签-->
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}图书管理系统{% endblock %}</title>
    
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
    <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
    <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>   <!--bootstrap依赖jQuery-->
    
    {% block css %}
        {#  此处书写页面独有的css  #}
    {% endblock %}

</head>
<body>

<!--导航条-->
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
      <a class="navbar-brand" href="#">图书管理系统</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">图书 <span class="sr-only">(current)</span></a></li>
        <li><a href="#">作者</a></li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">更多 <span class="caret"></span></a>
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
        <li><a href="#">Jason</a></li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">更多操作 <span class="caret"></span></a>
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

        <!--侧边栏-->
        <div class="col-md-3">
            <div class="list-group">
              <a href="#" class="list-group-item active">
                首页
              </a>
              <a href="#" class="list-group-item">图书列表</a>
              <a href="#" class="list-group-item">出版社列表</a>
              <a href="#" class="list-group-item">作者列表</a>
              <a href="#" class="list-group-item">更多</a>
            </div>
        </div>

        <!--面板-->
        <div class="col-md-9">
            <div class="panel panel-primary">
              <div class="panel-heading">
                <h3 class="panel-title">图书管理系统</h3>
              </div>

              <div class="panel-body">
                {% block content %} 
                    {# 页面独有的内容 #}
                    <div class="jumbotron">
                  <h1>欢迎使用图书管理系统</h1>
                  <p>...</p>
                  <p><a class="btn btn-primary btn-lg" href="#" role="button">点击查看更多</a></p>
                </div>
                {% endblock %}
              </div>
            </div>
        </div>
    </div>
</div>
{% block js %}
{# 页面独有的js #}
{% endblock %}
</body>
</html>
```
> 1. 首页页面，将其作为基页面，用于搭建子夜

## 1.2 首页路由配置
在总路由层`urls.py`中的`urlpatterns`列表添加如下代码
```python
url(r"^$", views.home, name='home')
```
> 1. `name`: 用于反向解析
> 2. `views.home`: 视图函数

## 1.3 首页视图函数逻辑
```python
def home(request):
    return render(request, 'home.html')  # 返回首页
```

# 二、书籍信息展示页面
**书籍信息展示页面(图书列表页面)**
![](https://images.gitee.com/uploads/images/2020/1212/171708_a185c756_7841459.png "屏幕截图.png")

## 2.1 前端模板部分
```html
{% extends 'home.html' %}  <!--继承基模板-->

{% block content %}
    <a href="" class="btn btn-success">添加</a>
    <br>
    <br>
    <table class="table table-hover table-striped table-bordered">
        <thead>
            <tr>
                <th>id</th>
                <th>书名</th>
                <th>作者</th>
                <th>价格</th>
                <th>出版日期</th>
                <th>出版社</th>
                <th>操作</th>
            </tr>
        </thead>

        <tbody>
            {% for book_obj in book_list %}
                <tr>
                    <td>{{ book_obj.pk }}</td>
                    <td>{{ book_obj.title }}</td>
                    <td>
                        {% for author in book_obj.authors.all %}
                            {% if forloop.last %}
                                {{ author.name }}
                            {% else %}
                                {{ author.name }},
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>{{ book_obj.price }}</td>
                    <td>{{ book_obj.publish_date|date:'Y-m-d' }}</td>
                    <td>{{ book_obj.publish.name }}</td>
                    <td>
                        <a href="" class="btn btn-primary btn-xs">编辑</a>
                        <a href="" class="btn btn-danger btn-xs">删除</a>
                    </td>
                </tr>

            {% endfor %}

        </tbody>

    </table>
{% endblock %}
```
> 1. 继承首页模板: `{% extends 'home.html' %} `
> 2. 修该面板部分: `{% block content %} .... {% endblock %}`
> 3. 使用到了`for标签` `if标签`
> 4. 用到了一个过滤器: `date:'Y-m-d'`

## 2.2 后端路径配置
在总路由层`urls.py`中的`urlpatterns`列表添加如下代码
```python
url(r"^book/list/", views.book_list, name='book_list')
```
## 2.3 后端逻辑(视图函数)
```python
from .models import Book  # 导入book表对应的类
def book_list(request):
    """
    图书列表展示
    :param request:
    :return:
    """
    # 1. 查询出所有图书
    book_queryset = Book.objects.all()  # 查询出全部的书籍

    context = {'book_list': book_queryset}  # 传递到模板中

    return render(request, 'book_list.html', context)
```
> **模板中获取值**：传到前端的数据是`queryset`对象 通过`for`标签取值后的得到的是`book`数据对象。还要通过数据对象获取作者姓名，出版社，这些属于正向查询
> 1. ` book_obj.pk`: 获取书籍的主键值
> 2. `book_obj.title`: 获取书籍的名称
> 3. `book_obj.authors.all`: 获取书籍的所有作者，通过`for`标签取出作者姓名
> 4. `book_obj.publish.name`: 获取到出版社的名称(一对多)

# 三、添加书籍
**添加数据页面**
![](https://images.gitee.com/uploads/images/2020/1212/184036_409729f6_7841459.png "屏幕截图.png")

## 3.1 添加数据模板
```python
{% extends 'home.html' %}

{% block content %}
    <h1 class="text-center">书籍添加</h1>
    <form action="" method="post">
        <p>
            <label for="book_name">书名</label>
            <input type="text" id="book_name" name="title" class="form-control">
        </p>

        <p>
            <label for="book_price">价格</label>
            <input type="text" id="book_price" name="price" class="form-control">
        </p>

        <p>
            <label for="book_publish_date">出版日期</label>
            <input type="date" id="book_publish_date" name="publish_date" class="form-control">
        </p>

        <p>
            <label for="book_publish">出版社</label>
            <select name="publish" id="book_publish" class="form-control">
                {% for publish in publish_queryset %}
                    <option value="{{ publish.pk }}">{{ publish.name }}</option>
                {% endfor %}
            </select>
        </p>

        <p>
            <label for="book_author">作者</label>
            <select name="author" id="book_author" multiple class="form-control">
                {% for author in author_queryset %}
                    <option value="{{ author.pk }}">{{ author.name }}</option>
                {% endfor %}
            </select>
        </p>
        <input type="submit" class="btn btn-primary btn-block" value="提交">
    </form>
{% endblock %}
```
> 对于出版社和作者，需要我们从后端返回数据来进行展示，让用户选择该书出版社和作者
>
> 1. 向后端提交数据时，我们提交的时标识数据唯一的信息

## 3.2 添加书籍的路由配置
在总路由层`urls.py`中的`urlpatterns`列表添加如下代码
```python
url(r'^book/add/', views.book_add, name='book_add')
```

## 3.3 后端逻辑(视图函数)
```python
def book_add(request):
    """
    添加书籍
    :param request:
    :return:
    """
    if request.method == "POST":
        # 获取前端提交的数据
        title = request.POST.get("title")  # 书名
        price = request.POST.get("price")  # 价格
        publish_date = request.POST.get("publish_date")  # 出版日期
        publish_id = request.POST.get("publish")  # 出版社的主键值
        authors_list = request.POST.getlist("author")  # 获取作者

        # 操作数据库存储数据
        # 书籍表, 添加书籍
        book = Book.objects.create(title=title, price=price, publish_date=publish_date, publish_id=publish_id)
        # 书籍与作者关系表 添加对应关系
        book.authors.add(*authors_list)

        return redirect(reverse('book_list'))  # redirect("book_list") 可以直接写路由别名, 如果路由需要参数,使用reverse

    # 查询出出版社的数据
    publish_queryset = Publish.objects.all()
    # 查询出作者数据
    author_queryset = Author.objects.all()
    return render(request, "book_add.html", locals())
```
# 四、书籍信息修改
**前端页面**
![](https://images.gitee.com/uploads/images/2020/1212/204953_fd8c7e0c_7841459.png "屏幕截图.png")

## 4.1 书籍信息修改的前端模板
**与书籍信息添加的模板类似**
```python
{% extends 'home.html' %}

{% block content %}
<h1 class="text-center">书籍编辑</h1>
    <form action="" method="post">
        <p>
            <label for="book_name">书名</label>
            <input type="text" id="book_name" name="title" class="form-control" value="{{ edit.title }}">
        </p>

        <p>
            <label for="book_price">价格</label>
            <input type="text" id="book_price" name="price" class="form-control" value="{{ edit.price }}">
        </p>

        <p>
            <label for="book_publish_date">出版日期</label>
            <input type="date" id="book_publish_date" name="publish_date" class="form-control" value="{{ edit.publish_date|date:'Y-m-d' }}">
        </p>

        <p>
            <label for="book_publish">出版社</label>
            <select name="publish" id="book_publish" class="form-control">
                {% for publish in publish_queryset %}
                    {% if publish == edit.publish %}  <!--判断当前publish对象是否和edit.publish对象一样-->
                        <option value="{{ publish.pk }}" selected>{{ publish.name }}</option> <!--是.默认选择-->
                    {% else %}
                        <option value="{{ publish.pk }}">{{ publish.name }}</option>
                    {% endif %}
                {% endfor %}
            </select>
        </p>

        <p>
            <label for="book_author">作者</label>
            <select name="author" id="book_author" multiple class="form-control">
                {% for author in author_queryset %}
                    {% if author in edit.authors.all %}  <!--判断当前作者是否在被编辑书的作者里面-->
                        <option value="{{ author.pk }}" selected>{{ author.name }}</option> <!--在就默认选中-->
                    {% else %}
                        <option value="{{ author.pk }}">{{ author.name }}</option>
                    {% endif %}
                {% endfor %}
            </select>
        </p>
        <input type="submit" class="btn btn-primary btn-block" value="提交">
    </form>
{% endblock %}
```
> 1. 先展示被编辑对象的原始数据
> 2. 注意模板中的注释

## 4.2 书籍信息修改的路由配置
在总路由层`urls.py`中的`urlpatterns`列表添加如下代码
```python
url(r"^book/edit/(?P<book_id>\d+)", views.book_edit, name="book_edit")
```
> 1. 修改书籍信息需要知道被修改的书籍是那一本，书籍的主键字段可以唯一标识
> 2. 对正则进行分组匹配，将匹配出来的数据传递给视图函数
> 3. 要去数据展示页面(`book_list`)配置当前路由解析路径
>    ```django
>    <a href="{% url 'book_edit' book_obj.pk %}" class="btn btn-primary btn-xs">编辑</a>
>    ```

## 4.3 书籍信息修改的视图函数(后端逻辑)
```python
def book_edit(request, book_id):
    """
    书籍信息修改, 修改书籍信息需要确定的书籍
    :param book_id: 编辑的书籍的id
    :param request:
    :return:
    """
    # 获取当前用户想要编辑的书籍对象
    edit = Book.objects.filter(pk=book_id).first()
    if request.method == "POST":
        # 获取用户修改后的数据
        title = request.POST.get("title")  # 书名
        price = request.POST.get("price")  # 价格
        publish_date = request.POST.get("publish_date")  # 出版日期
        publish_id = request.POST.get("publish")  # 出版社的主键值
        authors_list = request.POST.getlist("author")  # 获取作者

        # 修改书籍表
        Book.objects.filter(pk=book_id).update(title=title,
                                               price=price,
                                               publish_date=publish_date,
                                               publish_id=publish_id)

        # 修改中间表
        edit.authors.set(authors_list)  # 不要打撒列表.
        return redirect(reverse('book_list'))  # 重定向到图书展示页面

    # 查询出出版社的数据
    publish_queryset = Publish.objects.all()
    # 查询出作者数据
    author_queryset = Author.objects.all()

    return render(request, 'book_edit.html', locals())
```

# 五、书籍信息的删除
这个删除无须前端页面，直接在后端删除，然后跳转到数据展示页面

## 5.1 书籍信息删除的路由信息配置
在总路由层`urls.py`中的`urlpatterns`列表添加如下代码
```python
url(r"^book/delete/(\d+)", views.book_delete, name="book_delete")
```
> 在数据展示页面(`book_list`)配置前端的路由解析
> ```django
> <a href="{% url 'book_delete' book_obj.pk %}" class="btn btn-danger btn-xs">删除</a>
> ```

## 5.2 书籍信息删除后端逻辑(视图函数)
> 1. 点击删除后，弹出弹窗确认，发送ajax请求
> 2. 在后端完成数据删除

### 5.2.1 sweetalter弹窗确认
```js
<script>
    $('.cancel').click(function () {
        var $aEle = $(this);    {#  this 指代当前点击对象  #}
        swal({
              title: "你确定要删嘛?",
              text: "你如果删了，你就要准备跑路了",
              type: "warning",
              showCancelButton: true,
              confirmButtonClass: "btn-danger",
              confirmButtonText: "是，老子就是要删!",
              cancelButtonText: "惹不起惹不起!",
              closeOnConfirm: false,
              closeOnCancel: false,
              showLoaderOnConfirm: true   // 确认延迟参数
        },
        function(isConfirm) {
          if (isConfirm) {
              // 发送ajax请求
            $.ajax({
                url:'/book/delete/',
                type:'post',
                data:{'delete_id':$aEle.attr('data_id')},
                success:function (data) {   // 回调函数会自动将二进制的json格式数据 解码并反序列成js中的数据类型
                    if (data.code === 1000){
                        swal("删了!", "你可以跑路了.", "success");
                        // 方式一 页面刷新
                        window.location.reload()
                        // 方式二 DOM操作动态修改
                        {#$aEle.parent().parent().remove()#}
                    }else{
                        swal('发生了未知的错误','error')    // 将标签直接移除
                    }
                }
            });
          } else {
            swal("怂逼", "你成功的刷新我对你的认知 :)", "error");
          }
        });
    })
</script>
```
### 5.2.2 后端逻辑
```python
def book_delete(request):
    """
    删除书籍信息
    :param request:
    :return:
    """
    if request.method == 'POST':
        time.sleep(0.5)  # 模拟延迟
        back_dic = {'code': 1000, 'msg': ''}
        delete_id = request.POST.get('delete_id')
        Book.objects.filter(pk=delete_id).delete()  # 删除
        back_dic['msg'] = '删除完成'
        return JsonResponse(back_dic, json_dumps_params={"ensure_ascii": False})

    return redirect(reverse('book_list'))
```

