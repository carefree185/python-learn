# 一、字段的操作
修改`app_name/models.py`文件中的类属性，就可以对字段进行操作。然后执行数据库迁移命令
> 1. 如果表中有数据，增加字段需要提供默认值，或允许为空。
> 2. 删除字段时，字段对应的数据也会被删除

# 二、数据的增删查改
在查询数据时，使用表对应的类(创建表时创建的类(`User`类))进行数据的查询
1. 基本查询语句，查询语句，返回的是数据对象列表(`QuerySet`对象)，支持索引取值(负数不行)、切片
    ```python
    data = models.User.objects.filter(username=username) # 查询出符合条件的数据
    # 查询出所有数据
    data = models.User.objects.all()  
    ```
    * QuerySet对象的操作:
        * 从数据对象列表取值: `QuerySet.first()`, 获取第一个数据
    * `filter()`相当于关键字`where`，里面放条件，多个条件默认以`and`连接起来    

2. 添加数据
    * 创建数据，并添加到数据库，返回当前数据对象
        ```python
        models.User.objects.create(username=username, password=password)
        ```
    * 创建数据对象，然后调用保存方法
        ```python
        user_obj = models.User(username=username, password=password)  # 创建数据
        user_obj.save()  # 保存到数据库       
        ```
3. 修改数据
    ```python
    # 方式1 将查询出来的QuerySet对象中的数据对象全部更新
    models.User.objects.filter(id=edit_id).update(username=username, password=password)
    
    # 方式2 对象.属性=属性值，对象.save()进行更新
    ```
    > 方式2，将字段都会修改一遍，无论字段属性是否发生变化
4. 删除数据
    ```python
    models.User.objects.filter(id=delete_id).delete()  # 批量删除
    ```
    > 在删除数据的时候，不会真正意义上的删除，只会开设一个标记数据是否删除的字段。如果数据被删除，则将其设置为`True`或`False`

# 三、数据展示编辑删除
## 3.1 数据展示
**前端页面** 
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>数据展示</title>
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
    <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
    <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>   <!--bootstrap依赖jQuery-->
</head>
<body>
<h1 class="text-center">数据展示</h1>
<div class="container">
    <div class="row1">

        <div class="col-md-8 col-md-offset-2">
            <table class="table table-bordered table-hover table-striped">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>username</th>
                        <th>password</th>
                        <th>action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in user_list %}
                        <tr>
                            <td>{{ user.id }}</td>
                            <td>{{ user.username }}</td>
                            <td>{{ user.password }}</td>
                            <td>
                                <a href="" class="btn btn-primary btn-xs">编辑</a>
                                <a href="" class="btn bg-danger btn-xs">删除</a>
                            </td>
                        </tr>
                    {% endfor %}

                </tbody>
            </table>
        </div>
    </div>

</div>
</body>
</html>
```
**后端代码**
```python
def user_list(request):
    """
    展示数据
    :param request:
    :return:
    """
    # 查询出用户表的数据
    user_query_set = models.User.objects.all()  # 查询出所有数据
    return render(request, 'user_list.html', {"user_list": user_query_set})
```

## 3.2 数据编辑
* 第一步，点击编辑，发生数据对应的主键值到后端。`/edit_user/?user_id={{ user.id }}`, 在a标签的`href="/edit_user/?user_id={{ user.id }}"`,就可以将数据对应的id发送给服务端
* 第二步，获取到主键值查询出用户想要编辑的数据对象，展示到前端页面，让用户编辑

**前端页面**
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>编辑数据</title>
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
    <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
    <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>   <!--bootstrap依赖jQuery-->
</head>
<body>
<h1 class="text-center">编辑数据</h1>
<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
            <form action="" method="post">
                <p>
                    <label for="user">修 改 用 户 名:</label>
                    <input type="text" name="username" id="user" class="form-control" value="{{ edit_obj.username }}">
                </p>
                <p>
                    <label for="pwd">修 改 密 码:</label>
                    <input type="text" name="password" id="pwd" class="form-control" value="{{ edit_obj.password }}">
                </p>

                <input type="submit" class="btn btn-danger btn-block">
            </form>
        </div>
    </div>
</div>
</body>
</html>
```
**后端代码**
```python
def edit_user(request):
    """
    编辑用户
    :param request:
    :return:
    """
    edit_id = request.GET.get("user_id")  # 获取要编辑的数据的主键值
    edit_obj = models.User.objects.filter(id=edit_id).first()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 去数据库中修改数据
        # 方式1 将查询出来的QuerySet对象中的数据对象全部更新
        models.User.objects.filter(id=edit_id).update(username=username, password=password)
        # 方式2 对象修改属性的方式然后使用 对象.save()更新
        # 跳转到数据展示页面
        return redirect("/userlist/")

    return render(request, "edit_user.html", {"edit_obj": edit_obj})
```
## 3.3 删除数据
删除数据与编辑数据的逻辑类似。
**后端代码**
```python
def delete_user(request):
    """
    删除用户
    :param request:
    :return:
    """
    # 获取要删除的id
    delete_id = request.GET.get("user_id")
    # 二次确认
    # 删除数据
    models.User.objects.filter(id=delete_id).delete()  # 批量删除
    return redirect('/userlist/')
```
# 四、Django表关系创建
**以图书管理系统为例**，我们要使用到如下几张数据表
1. 图书表：存放图书的信息，包括书名、书架
2. 出版社表：存放出版社名及出版社地址
3. 作者表：作者姓名年龄
4. 作者详情表：作者联系方式和联系地址等详细数据

**表关系的确定**：对于以上4张表，分析得出下列关系 
> 1. 图书只能在一个出版社里面出版，但是出版社可以出版许多图书。**出版社与图书是一对多关系** 
> 2. 一个作者可以编著多部图书，一部图书也可以由多个作者编著。**图书与作者是多对多关系**
> 3. 作者和作者详情只能是一对一关系

**Django orm创建表关系**：在`Django1.x`外键都是级联更新级联删除
* 一对多
    ```python
    from django.db import models
    foreign_field = models.ForeignKey(to="一对多外键关联的表类", to_field="关联的字段") # to_field默认关联的是id字段。id字段orm会自动创建
    ```
    * `ForeignKey`： 自动给字段添加`_id`后缀

* 一对一
    ```python
    from django.db import models
    foreign_field = models.OneToOneField(to="一对一关联的表类", to_field="关联的字段")
    ```
    * `OneToOneField`: 自动给字段添加`_id`后缀

* 多对多，创建多对多关系有很多。
    * 在经常被查询的表中添加如下字段，这个字段是一个虚拟字段，用于标识使的`orm`自动创建第三张多对多关系表
    ```python
    virtual_field = models.ManyToManyField(to="多对多关联的表类", to_field="关联的字段")
    ```



**图书管理系统数据创建表的代码**
```python
# 图书管理系统表
class Book(models.Model):
    """
    图书表
    """
    title = models.CharField(max_length=32, verbose_name='书名')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="价格")  # 总共8位，小数占2位
    # 一部图书只能由一个出版社出版，但是出版社可以出版多部图书，出版社与图书是一对多关系
    publish_id = models.ForeignKey(to="Publish")  # 外键约束，一对多
    # 一部图书可以由多个作者编著，一个作者也可以编著多半图书，图书与作者是多对多关系
    authors = models.ManyToManyField(to="Author")  # 虚拟字段，主要是用来使orm自动创建第三张关系表


class Publish(models.Model):
    """
    出版社表
    """
    name = models.CharField(max_length=32, verbose_name='出版社名')
    addr = models.CharField(max_length=108, verbose_name='出版社地址')
    
    
class Author(models.Model):
    """
    作者表
    """
    name = models.CharField(max_length=20, verbose_name='作者名')
    age = models.IntegerField(verbose_name='年龄')
    # 作者与作者详情是一对一关系
    detail = models.OneToOneField(to="AuthorDetail")  # 建立一对一外键关系


class AuthorDetail(models.Model):
    """
    作者详情表
    """
    phone = models.CharField(max_length=12, verbose_name='电话号码')
    addr = models.CharField(max_length=108, verbose_name='地址')
```

