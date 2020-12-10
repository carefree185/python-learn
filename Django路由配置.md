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
当我们访问一个`url`后，返回的页面往往还有很多其他的`url`提供给我们访问，这些`url`是如何确定的？？
> 如果直接在模板中写死，那么路由发生变化后将会使这些待访问的`url`失效
`Django`提供了反向解析这些路由的方法。
1. 第一步，给路由取别名
2. 第二步，在模板中使用模板语法通过路由别名获取路由
3. 第三步，在我们访问的路由中，使用Django提供的反向解析方法获取到下一次要访问的路由

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
### 3.2.1 无名分组的反向解析
**要被解析的路由**
```python
url(r'^route/(\d+)/', views_function, name="route_as_name")
```

* 前端，获取要访问的路由及其分组
    ```html
    {% url 'route_as_name' 能够被分组匹配的内容 %}
    ```
* 后端
    ```python
    reverse('route_as_name', args=(能够被分组匹配的数据, ))
    ```
### 3.2.2 有名分组的反向解析
```python
url(r"^route/(?P<year>\d+)/", views_function, name='route_as_name')
```
* 前端，获取要访问的路由及其分组
    ```html
    {% url 'route_as_name' 能够被分组匹配的内容(key=value) %}
    ```
* 后端
    ```python
    reverse('route_as_name', args=(能够被分组匹配的数据, )) 或者
    reverse('route_as_name', kwargs={key: value})
    ```

# 四、路由分发
Django的每一个应用都可以有自己的`url.py`、`template文件夹`、`static文件夹`（应用于分组分组开发）

当项目功能越来越多时，总路由将会有巨大的压力。可以使用路由分发来完成，来减轻总路由的压力。

利用路由分发后，不在做路由与视图函数的绑定关系；而是识别当前访问的url是属于哪个app的，然后直接分发给对应app进行处理


* 总路由
    ```python
    from django.conf.urls import url, include
    from django.contrib import admin
    from app_name import urls as app_name_urls
    
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        # 路由分发
        url(r'^app_name/', include(app_name_urls)),
    
        # 终极写法
        url(r'^app_name/', include('app_name_urls')),
    ]
    ```
    > **总路由里面的url不能使用`$`结尾** 

* 子路由(`app`目录下的`urls.py`)
    ```python
    from django.conf.urls import url
    from app_name import views
    
    urlpatterns = [
        url(r"^reg/", views.reg)
    ]
    ```

# 五、名称空间
不同`app`下的 **路由别名** 出现相同时，反向解析是 **不能** 解析出 **路由别名** 所在的`app`。为了解决该问题，Django在总路由中配置路由分发时需要指定一个`namespace`参数，然后在给子路由取别名。

* 子路由取别名
    ```python
    from django.conf.urls import url
    from app_name import views
    
    urlpatterns = [
        url(r"^route/", views.reg, name='route_as_name')
    ]
    ```
* 总路由指定名称空间
    ```python
    from django.conf.urls import url, include
    from django.contrib import admin
    from app_name import urls as app_name_urls
    
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
    
        # 路由分发
        url(r'^app_name/', include(app_name_urls, namespace="name")),
        # 终极写法
        url(r'^app_name/', include('app_name_urls.urls', namespace="name")),
    ]
    ```
* 后端反向解析路由
    ```python
    reverse('namespace:route_as_name')
    ```
* 前端反向解析路由
    ```python
    {% url 'namespace:route_as_name' %}
    ```

**一般情况下，在给子路由取别名时，添加`app_name`前缀；这样就可以不使用名称空间**



# 六、伪静态
将动态网页伪装成静态网页，目的在于增大网站的`seo`查询力度，增加搜索引擎收藏网站的概率。

# 七、虚拟环境
在开发流程中，会给每个项目配备该项目独占的解释器环境，在这个给环境中只安装了该项目需要的模块。这个解释器环境称为虚拟环境，当我创建虚拟环境时，就相当于重新安装一个纯净的python。

在实际开发中，要配置`requirement.txt`文件，里面包含了项目需要的模块和版本。

### ubuntu下python3安装与配置
==注意:== 
最新版ubuntu默认删除python2

安装python2及python3:
在命令行输入：
```bash
sudo apt-get install python2  python3
sudo apt-get install python-pip python3-pip
```
等待安装完成

### python虚拟环境
第一步：安装virtualenv
```bash
# 在python2下安装
sudo pip install virtualenv
sudo pip install virtualenvwrapper
# 在python3下安装
sudo pip3 install virtualenv
sudo pip3 install virtualenvwrapper
```
等待安装完成
完成后在文件 ~/.bashrc 末尾添加义项内容

```sheel
vim ~/.bashrc
# 输入以下内容
export WORKON_HOME=~/.virtualenv
source /usr/local/bin/virtualenvwrapper.sh
```
保存文件
在命令行输入
```sheel
source ~/.bashrc  # 读入配置文件，立即生效
```
### virtualenvwrapper的基本使用
1： 创建虚拟环境
mkvirtuelwnv --python=指定要使用的python 虚拟环境名称

2：基本命令 
查看当前的虚拟环境： workon

进入虚拟环境：
workon 虚拟环境名称 

退出虚拟环境：deactivate

3: 删除虚拟环境
rmvirtualenv 虚拟环境名称



# 八、Django版本区别
1. Django 1.x 路由层使用`url`方法, 在Django 2.x之后的版本使用的是`path`和`re_path`方法
    * `url`和`re_path`的第一个参数支持正则, `path`第一个参数不支持正则,
2. Django 2.x 提供数据类型转换器
    ```python
    path('/route/<数据类型转换器: 变量名>', views_function)  # 将匹配出的数据转换成对应的类型，传递到视图函数中. 
    ```
    * **默认转换器**

        |符号|作用|
        |---|---|
        |str|匹配非空字符串 (/除外)|
        |int|匹配整数|
        |slug|匹配字母、数值及横杠、下划线注册的字符串|
        |uuid|匹配uuid格式|
        |path|匹配任何空字符串，包含路径分割符|
    * 除了默认的转换器，还可以自定义转换器
        1. 在`app_name`下新建文件`path_converters.py`, 文件名可以随意取
        ```python
        class MonthConverter:
            regex = "\d{2}"  # 属性名必须为regex
        
            def to_python(self, value):
                return int(value)
        
            def to_url(self, value):
                return value
        ```
        2. 在要使用自定义转换器的`urls.py`使用`register_converter`方法注册到`url`配置中
        ```python
        from django.urls import path, register_converter
        from app_name.path_converters import MonthConverter
        # 注册转换器
        register_converter(MonthConverter, "mon")  # 第二个参数是转换器的名称
        
        urlpatterns = [
            path('route/<mon: month>', views_function)
        ]
        ```
3. 模型层中，Django 2.x及以上的外键需要配置级联更新级联删除









