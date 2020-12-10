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







