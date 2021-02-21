# 一、cookie和session简介
发展简史：由于`http`协议是无状态无连接的协议。
1. 最初，网站都没有保存用户功能的需求，所有用户访问响应的结果都是一样的
2. 随着web技术的发展，出现了一些需要保存用户功能的需求，例如：淘宝、京东等网站。如果不保存用户的登录功能，每次用户访问都需要登录。这样会导致用户使用繁琐。
    * 初代解决方案，当用户登录成功后，将用户的用户名和密码保存在用户本地浏览器中，每次请求，让浏览器带着这些数据访问。(`cookie`)
    * 这个方案有较大的安全隐患，对其进行了一些优化。当用户登录成功后，服务端将产生一个随机字符串，并将 **其与用户的敏感信息** 组织成键值对的形式保存在服务端。随机字符串返回给浏览器，让浏览器保存。然后每次访问都将这个随机字符串发送给服务器进行校验。如果这个随机字符串可能被窃取。(`session`)


## 1.1 cookie
由服务端返回给浏览器的一些信息，并且浏览保存在本地，然后每次访问都需要将这些信息一并发送给服务端。
* 服务端保存在浏览器上的数据都可以称为`cookie`
* 一般以 _键值对_ 的形式保存在浏览器中

## 1.2 session
用户的敏感信息不在返回给浏览器，而是产生一个随机字符串，将它与用户敏感信息构造成`k:v`键值对的信息保存在服务端中。然后将这个随机字符串返回给浏览器。
* 数据保存在服务端中
* 一般以 _键值对_ 的形式保存在浏览器中

# 二、Django cookie操作
实现一个较为完整的登录功能，来学习cookie操作
1. **阶段一** ，登陆后跳转到指定网页
    * 登录功能， **设置cookie**使用`httpresponse.set_cookie(key, value)`
        ```python
        def login(request):
            if request.method == 'POST':  # 第一步、判断是否为post请求
                # post请求执行如下操作
                username = request.POST.get('username')  # 第二步，获取前端发送过来的数据
                password = request.POST.get('password')
                if username == 'dyp' and password == '111':  # 第三步 校验数据是否正确
                    target = '/'  # 默认跳转到首页
                    obj = redirect(target)  # target 要跳转的目标网站，创建HttpResponse对象
                    obj.set_cookie('username', 'dyp')  # 设置cookie, 浏览器保存用cookie, 每次访问也会将其发送到服务器
                    return obj  # 跳转到需要用户登录才能访问的页面
        
            return render(request, 'login.html')  # 不是post请求，返回登录页面
        ```
    * 校验用户是否登录，**获取cookie**使用`request.COOKIES.get(key)`

        ```python
        def buy(request):
            # 获取cookie信息， 判断是否登录
            if request.COOKIES.get('username') == 'dyp':  # 第一步、获取cookie信息
                # 登录成功后，返回当前登录用户能够访问的页面
                return HttpResponse("我是登录后才能访问的页面")
            # 没有则，跳转到登录页面
            return redirect('/login/')  # 没有登录，转到登录页面
        ```
2. **阶段二**， **封装登录认证装饰器**，当页面太多时，如果每个页面都去写一个验证代码，会造成代码重复。使用装饰器来解决这一个问题。下面先复习一些装饰器.
    * 装饰器 `function=decorator(function), function(*args, **kwargs)`
        ```python
        def decorator(fun):
            def inner(*args, **kwargs):
                res = fun(*args, **kwargs)
                return res
            return inner
        
        @decorator
        def function(*args, **kwargs):
            pass
        ```
        * 被装饰函数的执行流程:
            1. 第一步、被装饰函数被调用时，将被装饰函数传递到装饰器中
            2. 第二步、对函数进行功能添加后，将被装饰函数封装到装饰器的返回值中。
            3. 第三步、调用装饰器函数的返回值，将被装饰的函数参数传递给装饰器函数的返回值
    * 自定义一个登录认证装饰器, 及使用
        ```python
        def login_auth(func):
            def inner(*args, **kwargs):
                if request.COOKIES.get('username') == 'dyp':  # 判断是否登录
                    # 登录，触发需要登录的视图函数，返回页面
                    res = func(*args, **kwargs)
                    return res
                return redirect('/login/')  # 没有登录，跳转到需要登录页面
            return inner

        @login_auth
        def function(request):  # 需要认证的页面
            pass
        ```
3. **阶段三**，现在登录认证已经基本完成，但是存在一个小的逻辑问题，当用户在没有登录的情况下，直接访问的是需要登录的页面。此时用户登录成功后，将只能跳转到固定的页面。对于用户的使用体验是一个巨大的打击。正常逻辑应该为，登陆后，依旧跳转到访问上一次访问的需要登录的页面。实现这三点需要明白下列几件事情。
    1. 后端可以获得当前访问的`url`地址: `request.get_full_path()`
    2. `get`请求可以携带参数
    3. 访问页面的方式通常是`get`请求进行访问的<br>
    现在实现实现登录后跳转到上一次访问页面
    * 第一步、修改登录认证装饰器
        ```python
        def login_auth(func):
            def inner(request, *args, **kwargs):
                target = request.get_full_path()  # 第一步，获取本次访问的url
                if request.COOKIES.get('username') == 'dyp': # 第二步、判断是否登录成功
                    # 登录成功，执行被访问页面的视图函数
                    res = func(request, *args, **kwargs)
                    return res
                return redirect('/login/?next=%s' % target)  # 没有登录，拼接当前访问的url，然后跳转到登录页面
            return inner
        ```
    * 第二步、修改登录逻辑
        ```python
        def login(request):
            # 第一步、判断请求方式是否为post请求
            if request.method == 'POST':
                # 请求为post请求，执行第二步
                username = request.POST.get('username')  # 获取用户输入的数据
                password = request.POST.get('password')
                # 第三步、校验数据是否正确
                if username == 'dyp' and password == '111':  # 校验数据是否正确
                    # 用户输入的数据都正确，执行第四步
        
                    # 第四步、获取用户上一次访问的需要登录url
                    target = request.GET.get('next')  # 可能为空，用户直接访问的登录页面，则上一次的请求url为空
                    # 第五步，设置cookie，跳转页面
                    if target:
                        # 不是直接访问的登录页面
                        obj = redirect(target)  # 生成跳转到目标url的HttpResponse对象
                    else:
                        # 直接访问的登录页面，默认跳转到首页
                        obj = redirect('/')  # 生成跳转到首页的HttpResponse对象
                    obj.set_cookie('username', 'dyp')  # 设置cookie, 浏览器保存用cookie, 每次访问也会将其发送到服务器
                    return obj 
        
            # 请求为get请求，返回登录页面
            return render(request, 'login.html')
        ```
4. **阶段四**，为了保护用户的信息安全，通常要给cookie设置有效期，有效期一过cookie将失效
    ```python
    obj.set_cookie('username', 'dyp', max_age=3, expires=3) 
    ```
    * `max_age`: 设置cookie有效期，以秒为单位
    * `expires`: 设置cookie有效期，以秒为单位，针对IE浏览器

5. **阶段五**，主动删除`cookie`,`httpresponse.delete_cookie("key")` (注销登录)
    ```python
    @login_auth
    def logout(request):
        obj = redirect('/')
        obj.delete_cookie('username')
        return obj
    ```
    * 只有登录的用户才能使用注销功能
    * 注销后，默认跳转到网站首页

# 三、Django session操作
在默认情况下，操作session需要Django的默认一张`django_session`表，用于保存随机字符串，校验数据，session有效时间(**默认情况下，有限时间为14天**)

1. **阶段一**，设置`session`
    ```python
    request.session['key'] = 'value'
    ```
    * `Django`内部会自动生成一个随机字符串
    * `Django`内部会自动将随机字符串和数据存放到`django_session`表
        1. 先在内存中产生操作数据的缓存
        2. 响应经过中间件时才开始操作数据库
    * 将产生的随机字符串返回给浏览器保存
    * `session`表中的数据条数取决于浏览器, 同一个计算机上的同一个浏览器只会由一条数据。为了节省服务端数据库资源。
    * 当`session`过期后，可能会出现一个浏览器对应多条`session`。 Django会自动清理，也可以在代码中清理数据

2. **阶段二**，获取`session`
    ```python
    request.session.get("key")
    ```
    1. 自动从请求中获取`sessionid`对应的随机字符串
    2. 使用随机字符串在`django_session`表中匹配出数据，以字典的形式封装到`request.session`中
    3. 如果没有匹配出数据，`request.session.get`返回`None`

3. **阶段三**，设置`session`过期时间
    ```python
    request.session.set_expiry(3)     # 3秒后过期
    request.session.set_expiry(date)  # 到指定的日期失效
    request.session.set_expiry(0)     # 浏览器窗口关闭，session失效
    ```
    * `date`: 日期对象

4. **阶段四**，清除`session`
    ```python
    request.session.delete()  # 删除当前会话的所有session，只删除服务端
    request.session.flush()  # 删除浏览和服务端的session, 常用这个
    ```

5. **阶段五**，session配置，在`setting`目录下
    ```
    1. 数据库Session
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # 引擎（默认）
    
    2. 缓存Session
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 引擎
    SESSION_CACHE_ALIAS = 'default'                            # 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置
    
    3. 文件Session
    SESSION_ENGINE = 'django.contrib.sessions.backends.file'    # 引擎
    SESSION_FILE_PATH = None                                    # 缓存文件路径，如果为None，则使用tempfile模块获取一个临时地址tempfile.gettempdir() 
    
    4. 缓存+数据库
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'        # 引擎
    
    5. 加密Cookie Session
    SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'   # 引擎
    
    其他公用设置项：
    SESSION_COOKIE_NAME ＝ "sessionid"                       # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
    SESSION_COOKIE_PATH ＝ "/"                               # Session的cookie保存的路径（默认）
    SESSION_COOKIE_DOMAIN = None                             # Session的cookie保存的域名（默认）
    SESSION_COOKIE_SECURE = False                            # 是否Https传输cookie（默认）
    SESSION_COOKIE_HTTPONLY = True                           # 是否Session的cookie只支持http传输（默认）
    SESSION_COOKIE_AGE = 1209600                             # Session的cookie失效日期（2周）（默认）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False                  # 是否关闭浏览器使得Session过期（默认）
    SESSION_SAVE_EVERY_REQUEST = False                       # 是否每次请求都保存Session，默认修改之后才保存（默认）
    ```

**基于`session`的登录认证**
```python
# 基于session的登录认证
def login_auth_session(func):
    def inner(request, *args, **kwargs):
        target = request.get_full_path()
        if request.session.get("username") == 'dyp':
            return func(request, *args, **kwargs)
        return redirect('/session_login/?next=%s' % target)
    return inner


# 基于session的登录
def session_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'dyp' and password == '111':  # 校验数据是否正确
            # 获取用户上一次想要访问的url
            target = request.GET.get('next')  # 可能为空
            if target:
                # 保存用户登录状态
                obj = redirect(target)
            else:
                # 跳转到主页
                obj = redirect('/')  # 跳转到首页
            request.session['username'] = username
            request.session['password'] = password
            # 跳转到需要用户登录才能访问的页面
            return obj

    return render(request, 'login.html')


@login_auth_session
def session_buy(request):
    return HttpResponse('session_buy 登录后访问的内容')


@login_auth_session
def session_back(request):
    return HttpResponse('session_back 登录后访问的内容')
```

# 四、`CBV`添加装饰器
在`CBV`下，步允许直接添加装饰器，需要导入模块来支持`CBV`中的方法添加装饰器
```python
from django.utils.decorators import method_decorator
```

**添加装饰器** 
* **方式一**  
    ```python
    class LoginView(View):
        @method_decorator(login_auth)
        def get(self, request):
            return HttpResponse("get请求")
    
        def post(self, request):
            return HttpResponse("post请求")
    ```
* **方式二** 
    ```python
    @method_decorator(login_auth, name='get')
    @method_decorator(login_auth, name='post')
    class LoginView(View):
    
        def get(self, request):
            return HttpResponse("get请求")
    
        def post(self, request):
            return HttpResponse("post请求")
    ```
* **方式三** 
    ```python
    class LoginView(View):
        
        @method_decorator(login_auth)
        def dispatch(self, request, *args, **kwargs):
            super(LoginView, self).dispatch(request, *args, **kwargs)
        
        def get(self, request):
            return HttpResponse("get请求")
    
        def post(self, request):
            return HttpResponse("post请求")
    ```
    * 作用于当前类里面的所有的方法


