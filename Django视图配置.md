# 一、`render, HttpResponse, redirect` 
`render()`, `HttpResponse`, `redirect()`都会返回一个HttpResponse对象

**render内部实现原理**
```python
from django.template import Template Context

res = Template("<h1>{{ user }}</h1>")
con = Contest({"user":{key:value, ...}})
ret = res.render(con)  # 渲染好的模板
return HttpResponse(ret)
```

# 二、JsonResponse对象
`json`格式的数据是用来实现跨语言传输数据的格式。

Django返回json字符串
```python
def json_str(request):
    user_dic = {"user": "dyy东湖与", "password": "111"}
    # import json
    # s = json.dumps(user_dic, ensure_ascii=False)  # ensure_ascii: 不自动转码
    # return HttpResponse(s)
    return JsonResponse(user_dic, json_dumps_params={"ensure_ascii": False}, safe=False)  # 默认只能序列号字典，序列号其他数据类型需要添加safe=False参数
```

# 三、文件上传
```html
<form action="" method="post" enctype="multipart/form-data">
    <p>username: <input type="text" name="username"></p>
    <p>file: <input type="file" name="file"></p>
    <input type="submit">
</form>
```

```python
def upload_file(request):
    if request.method == 'POST':
        print(request.POST)  # 只能获取普通文本数据
        print(request.FILES)  # 获取文件数据
        file = request.FILES.get('file')  # 获取文件对象
        print(file.name)
        with open(file.name, 'wb') as f:  # 保存文件
            for line in file.chunks():
                f.write(line)

    return render(request, "upload file.html")
```


# 四、request对象的补充方法
```python
request.body  # 浏览器发过来的原生数据 
request.path  # 获取用户访问的url后缀
request.get_full_path()  # 获取url后缀及其携带的参数
```

# 五、FBV与CBV
针对视图层
> * `FBV`: 基于函数的视图
> * `CBV`: 基于类的视图，基于类的视图会自动识别请求方式，然后调用其对应的方法

* **视图层中类的定义**
    ```python
    from django.views import View
    class Login(View):
        def get(self, request):
            return render(request, 'login.html')
    
        def post(self, request):
            return HttpResponse("POST")
    ```
* **CBV路由配置**
    ```python
    url(r"^login/", views.Login.as_view())
    ```

## 5.1 CBV内部源码
```python
url(r"^login/", views.Login.as_view())  # 第一步，Django启动时就会执行，查看as_view方法。 执行结果变为url(r"^login/", views.view)
##############################################
class View(object):
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    @classonlymethod
    def as_view(cls, **initkwargs):  # 第一步执行
        """
        Main entry point for a request-response process.
        """
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs): # 第二步执行
            self = cls(**initkwargs)  # Login(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)  # 调用了一个函数，返回
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view  # 第一步执行结果，返回内部函数名

    def dispatch(self, request, *args, **kwargs): # self=Login(**initkwargs)
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:  # 获取到请求方式，判断方式是否合法。合法执行下面代码
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)  # 反射操作, 获取到与请求方式同名的方法名
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)  # 执行方法

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            'Method Not Allowed (%s): %s', request.method, request.path,
            extra={'status_code': 405, 'request': request}
        )
        return http.HttpResponseNotAllowed(self._allowed_methods())

    def options(self, request, *args, **kwargs):
        """
        Handles responding to requests for the OPTIONS HTTP verb.
        """
        response = http.HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
```





