# 一、路由匹配
```python
url(r"test", views.test),
url(r"testadd", views.testadd)
```
1. url(reg, views_function): 第一个参数是正则表达式，只要第一个参数能够匹配到内容，就会立刻停止匹配，直接执行视图函数。在正则后面添加一个斜杠(`/`)作为后缀，用于区别不同的路由。
    ```python
    url(r"route/", views_function)
    ```

2. 如果所有的路由均匹配完成后，没有匹配到路由，`Django`就会自动给路由添加后缀(`/`)，让浏览器在发送一次请求
    * 取消自动添加后缀(`/`)，在`settings.py`文件中添加`APPEND_SLASH=False`; 这个参数默认为`True`

3. 此时只要`url`的后缀能够在末尾匹配到路由就能访问(`aaa_route/`也可以访问)，需要在路由前面添加`^`限制为以`r`开头
    ```python
    url(r"^route/", views_function)
    ```
4. 现在，`url`能够在前面匹配到`route/`就能访问(`test/aaaaffff`也可以访问)，需要在路由末尾添加`$`限制以`/`结尾
    ```python
    url(r"^route/$", views_function)
    ```
    * 此时只能以`route/`访问才能访问成功

**路由匹配的语法为: `^route/$`**

> * 首页匹配: `r"^$"`, 
> * 错误匹配: `r""`, 会匹配所有的`url`，用于`url`错误处理时要放在最后

# 二、正则分组
> 1. 某一段正则表达式被小括号括起来的就是一个分组
## 2.1 无名分组
将正则表达式匹配到的内容，当作位置参数传递给路由绑定的视图函数。
```python
url(r"^test/(\d+)/$", views.test)  # 路由匹配

def test(request, number):  # 视图函数
    return HttpResponse("test/%s" % number)
```

## 2.2 有名分组
对于每个分组可以取一个别名，将匹配到的数据，以别名来指代。然后将其当作关键参数传递到视图函数中
```python
url(r"^testadd/(?P<year>\d+)/$", views.testadd)

def testadd(request, year):
    return HttpResponse("testadd/%s" % year)
```

## 2.3 分组注意
* **无名分组和有名分组是不能混用**
* 一个路由中可以有多个分组，这个路由绑定的视图函数也需要有相应的多个参数
* 对于有名分组，路由绑定的视图函数的参数也要使用分组名来进行命名。

# 三、反向解析路由
当我们确定了一个路由后，并且要在模板中使用。之后如果路由发生变化，页面上的`url`将会集体失效。如果发生变化的路由使用量比较，维护的难度将会很大。需要提供一个方法来动态的获取到路由。

## 3.1 无分组情况下进行反向解析路由
1. 给路由取别名
    ```python
    url(r'^route/$', views_function, name='route_as_name')  # 给路由route取别名为route_as_name
    ```
2. 在模板中动态获取路由信息, 使用模板语法
    ```html
    {% url 'route_as_name' %}
    ```
3. 后端动态获取路由信息
    ```python
    from django.shortcuts import reverse
    reverse('route_as_name')
    ```
## 3.2 有分组情况下的反向解析


