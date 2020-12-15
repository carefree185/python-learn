# 一、Django中间件简介
Django默认自带了七个中间件，每个中间件都有对应的功能，用于处理全局的请求和响应。并且支持自定义中间件，暴露了5个方法自定义中间件。在Django项目中，涉及全局相关的功能可以使用中间件实现。例如：
1. 全局用户身份校验
2. 全局用户权限校验
3. 全局访问频率校验

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 操作session时的中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

# 二、自定义中间件
* 第一步、在项目根目录或app目录下创建一个文件夹用于保存自定义的中间件，可以任意命名但是要做到标识性。

* 第二步、在该文件夹下创建一个`py`文件用于编写自定义中间件，可以任意命名。

* 第三步、在该文件中以类的形式书写中间件，这个类需要继承`MiddlewareMixin`类

* 第四步、在类中自定义如下五个方法
    1. `process_request`: 请求到来时触发
    2. `process_response`: 响应时触发
    3. `process_view`:
    4. `process_template_response`:
    5. `process_exception`:

* 第五步，在`setting.py`的`MIDDLEWARE`列表中注册自定义中间件

**自定义中间件模板** 
```python
from django.utils.deprecation import MiddlewareMixin
# 自定义中间件类
class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        request: 请求相关的数据
        return: 校验不通过时，返回数据，否则不要由返回值
        """
        pass

    def process_response(self, request, response):
        """
        request: 请求相关的数据
        response: Django返回的数据，后端给前端的内容，被捕获到此方法中
        return response: 必须返回response，否则返回数据将被丢弃
        """
        return response

    def process_view(self, request, view_func, *args, **kwargs):
        """
        路由匹配成功之后，视图函数执行之前调用此方法
        :param request: 是HttpRequest对象, 请求数据
        :param view_func: Django即将使用的视图函数。 （它是实际的函数对象，而不是函数的名称作为字符串。）
        :param args: 将传递给视图的位置参数的列表.
        :param kwargs: 将传递给视图的关键字参数的字典
        :return None: 保持返回None， 如果返回HttpResponse的对象将，将不在执行视图函数，而是直接返回响应给浏览器
        """

    def process_template_response(self, request, response):
        """
        在视图函数之后，且返回的HttpResponse对象有render属性才会触发
        :param request: 请求数据
        :param response: 响应数据
        :return: 默认要返回响应数据
        """
        return response


    def process_exception(self, request, exception):
        """
        视图函数中出现异常了才执行
        :param request: 请求携带的数据
        :param exception: 异常信息
        :return:
        """
```

## 2.1 `process_request(self, requests)`方法
请求来的时候，每个请求都会经过每个中间件的`process_request`方法。
1. 触发顺序为`settings.py`文件中`MIDDLEWARE`列表中间件注册顺序执行。
2. 如果没有定义该方法，该中间件将被跳过。
3. 如果该方法返回了`HttpResponse`对象，请求将被返回，不在往下执行。(不允许访问)

## 2.2 `process_response(self, request, response)`方法
* `request`: 请求相关的数据
* `response`: Django响应的数据，必须返回的数据

响应返回时，每个响应都会经过`process_response`方法。
1. 触发顺序与`settings.py`文件中`MIDDLEWARE`列表 **中间件注册顺序相反** 
2. 如果没有该方法，该中间将被跳过
3. 该方法必须要有一个`HttpResponse`对象进行返回
    * **可以对返回内容进行替换** 


**如果请求在中间件的process_request方法中返回，那么将直接执行同级别的process_response方法进行数据返回**

## 2.3 `process_view(self, request, view_func, *args, **kwargs)`方法
```python
def process_view(self, request, view_func, *args, **kwargs):
    """
    路由匹配成功之后，视图函数执行之前调用此方法
    :param request: 是HttpRequest对象, 请求数据
    :param view_func: Django即将使用的视图函数。 （它是实际的函数对象，而不是函数的名称作为字符串。）
    :param args: 将传递给视图的位置参数的列表.
    :param kwargs: 将传递给视图的关键字参数的字典
    :return None: 保持返回None， 如果返回HttpResponse的对象将，将不在执行视图函数，而是直接返回响应给浏览器
    """
```

## 2.4 `process_template_response(self, request, response)`方法
```python
def process_template_response(self, request, response):
    """
    在视图函数之后，且返回的HttpResponse对象有render属性才会触发
    :param request: 请求数据
    :param response: 响应数据
    :return: 默认要返回响应数据
    """
    return response
```

## 2.5 `process_exception(self, request, exception)`方法
```python
def process_exception(self, request, exception):
    """
    视图函数中出现异常了才执行
    :param request: 请求携带的数据
    :param exception: 异常信息
    :return:
    """
```

# 三、跨域请求伪造(`csrf`)
钓鱼网站就是应用跨域请求伪造来实现的。例如，中国银行钓鱼网站
1. 搭建一个与正规网站页面相同的网站，然后诱导用户登录该网站
2. 当用户在该网站进行正规网站上转账交易时，用户提交的数据是到了中国银行的网站，但是转账的账户被修改了。

**早期`web csrf`的本质** 
1. 提供用户输入转账账户的标签是没有`name`属性的，提交数据后端将不能获取到这个信息。
2. 提前在页面中隐藏一个已经具备了`name`属性和`value`属性的隐藏标签。当用户提交数据时，提交的转账账户就是其他的账户了，而非真正的转账账户。

这个漏洞会造成用户的财产损失，我们需要杜绝这些现象。
1. 网站在给用户返回一个具有提交数据功能页面时，需要给该页面添加一个随机的唯一标识，将其与访问的`ip:port`绑定，存放在服务器。
2. 当页面向后端发送`post`请求时，需要先校验唯一标识。校验不通过，就拒绝访问；校验通过则继续进行

## 3.1 `csrf`校验
在前端模板的`form`标签内部，添加模板语法`{% csrf_token %}`, 就可以将唯一校验数据,返回个前端页面。

在`ajax`提交的post数据中，通过`csrf`校验
```js
// 方式一
"csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val() // 获取前端的值
// 方式二
"csrfmiddlewaretoken": '{{ csrf_token }}'  // 模板语法
// 方式三，直接引入文件ajax_csrf_verify.js即可
```
**ajax_csrf_verify.js**
```js
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
```

## 3.2 `csrf`相关装饰器
网站可能会有下一列需求
1. 整个网站总体上都不进行`CSRF`，但是某几个视图函数需要进行`CSRF`校验
2. 整个网站都要进行`CSRF`，但是某几个视图函数需要不进行`CSRF`校验

Django已经提供了相关的装饰器
```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# csrf_exempt: 忽视校验
# csrf_protect: 需要校验
```
### 3.2.1 校验`CSRF`的装饰器(`csrf_protect`)
整个网站总体上都不进行`CSRF`，但是某几个视图函数需要进行`CSRF`校验
```python
@csrf_protect  # 需要进行校验
def transform(request):
    if request.method == "POST":
        username = request.POST.get("username")
        target_user= request.POST.get("target_user")
        money = request.POST.get("money")
        print(f"{username}给{target_user}转{money}元")
    return render(request, "transform.html")
```
**任意方式给`CBV`内部方法添加装饰器，都可以生效**
```python
# @method_decorator(csrf_protect, name='post')  # 可行
@method_decorator(csrf_protect, name='dispatch') 
class Csrf(View):

    @method_decorator(csrf_protect)  # 可行
    def dispatch(self, request, *args, **kwargs):
        return super(Csrf, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("get")

    # @method_decorator(csrf_protect)  # 可行
    def post(self, request):
        return HttpResponse("post")
```


### 3.2.2 不校验`CSRF`的装饰器(`csrf_exemp`)
整个网站都要进行`CSRF`，但是某几个视图函数需要不进行`CSRF`校验
```python
@csrf_exempt  # 不进行csrf校验
def transform(request):
    if request.method == "POST":
        username = request.POST.get("username")
        target_user= request.POST.get("target_user")
        money = request.POST.get("money")
        print(f"{username}给{target_user}转{money}元")
    return render(request, "transform.html")
```
**只能添加给`CBV`内部的`dispatch`方法才能生效**

```python
# @method_decorator(csrf_exempt, name='post')  # 不可行
# @method_decorator(csrf_exempt, name="dispatch")  # 可行
class Csrf(View):

    @method_decorator(csrf_exempt)  # 可行
    def dispatch(self, request, *args, **kwargs):
        return super(Csrf, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("get")

    # @method_decorator(csrf_exempt)  # 不可行
    def post(self, request):
        return HttpResponse("post")
```

