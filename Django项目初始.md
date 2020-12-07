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






