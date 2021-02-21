# 一、`Auth`模块简介
创建一个Django项目后，执行数据库迁移命令后，会生成多张表其中有一张表`auth_user`表用于保存用户认证信息的表。访问`admin`路由登录就是基于这张表进行。登录的用户必须是超级用户

* 创建超级用户
    ```python
    python manage.py createsuperuser
    ```


# 二、`auth`模块的使用
* 第一步、导入`auth`模块
    ```python
    from django.contrib import auth
    ```

* 第二步、校验用户名和密码是否一致(`auth.authenticate(request, username=username, password=password)`)
    ```python
    user = auth.authenticate(request, username=username, password=password)
    ```
    * 返回值为当前登录用户的数据对象

* 第三步、保存用户登录状态 (`auth.login(request, user)`)
    ```python
    auth.login(request, user)
    ```
    * `request`: 请求相关数据
    * `user`: 登录用户的数据对象
    * 此方法一旦执行，网页全局就可以使用`request.user`获得当前登录的用户数据对象

* 第四步、判断当前用户是否登录,验证通过(`request.user.is_authenticated()`)
    ```python
    request.user.is_authenticated()
    ```

* 第五步、登录认证装饰器(现在某些路由为登录后才能访问)
    ```python
    from django.contrib.auth.decorators import login_required
    
    @login_required(login_url='/login/')
    def home(request):
        print(request.user)
        print(request.user.is_authenticated())
        return HttpResponse('OK')
    ```
    * `login_url='/login/'`: 登录认证失败时跳转的路由，局部配置
    * 可以全局配置(在`settings.py`文件中): `LOGIN_URL='/login/'`

* 第六步、修改用户密码
    1. 6.1，校验旧密码(`request.user.check_password(old_password)`)
        ```python
        is_right = request.user.check_password(old_password)
        ```
    2. 6.2步，修改密码(`request.user.set_password(new_password)`)
        ```python
        request.user.set_password(new_password)
        ```
        * 并未影响到数据库，只是在内存中修改了对象的属性值
    3. 6.3，保存修改后的密码(`request.user.save()`)
        ```python
        request.user.save()  # 刷新数据库，真正修改密码
        ```
* 第七步、注销登录用户(`auth.logout(request)`)
    ```python
    auth.logout(request)  # 注销登录用户
    ```

* 第八步、注册用户，需要导入`auth_user`对应的模型类型
    ```python
    from django.contrib.auth.models import User
    user = User.objects.create_user(username=username, password=password)  # 创建普通用户
    
    superuser = User.objects.create_superuser(username=username, password=password, email='111@qq.com') # 创建超级用户(了解)，邮箱必填
    ```
    * 创建用户会返回当前创建用户的数据对象

****
**完整的流程**
```python
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth

def login(request):
    """
    登录
    """
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 如何获取表
        # 密码如何比对
        user = auth.authenticate(request, username=username, password=password)  # 自动查找auth_user表，自动给密码加密在比对
        """
        用户名和密码需要同时传入，同时完成校验, 校验通过，返回用户对象; 如果用户名和密码校验不正确，返回None
        """
        # 判断当前用户是否存在
        if user:
            # 保存用户状态
            auth.login(request, user)  # 类似与request.session[key]=user_obj
            """
            只要执行了该方法，就可以在任何地方使用 request.user获取到当前登录的用户对象
            """
            return redirect('/home/')

    return render(request, 'login.html')


from django.contrib.auth.decorators import login_required  # 登录认证装饰器

"""
局部和全局都有登录url, 局部的有限被使用

全局：无需重复写代码
局部: 在用户没有登录的情况下可以跳转到各种各样的页面
"""

@login_required  # 登录认证装饰器，登录才能访问
def home(request):
    """根视图"""
    print(request.user)  # 用户登录了，获取到的是登录用户对象，否则获取到的是AnonymousUser
    print(request.user.is_authenticated())  # 判断当前用户是否验证过(是否登录)
    return HttpResponse('OK')


@login_required
def set_password(request):
    """
   修改密码
    """
    if request.method == 'POST':
        old_password = request.POST.get("old_password")   # 旧密码
        new_password = request.POST.get("new_password")  # 新密码
        confirm_password = request.POST.get("confirm_password")  # 二次确认密码

        if new_password == confirm_password:  # 两次密码是否一致
            # 在校验老密码是否输入正确
            is_right = request.user.check_password(old_password)
            """
            自动加密比对密码，正确返回True, 错误返回False
            """
            if is_right:
                request.user.set_password(new_password)  # 修改密码， 此时并未影响数据库
                request.user.save()  # 刷新数据库，真正修改密码
    return render(request, 'set_password.html', locals())

@login_required
def logout(request):
    """
    注销登录
    """
    auth.logout(request)  # 注销登录用户
    return redirect('/login/')  # 跳转到登陆页面


from django.contrib.auth.models import User
def register(request):
    """
    注册
    """
    if request.method == 'POST':
        username = request.POST.get("username")  # 用户名
        password = request.POST.get("password")  # 用户密码
        confirm_password = request.POST.get("confirm_password")  # 二次确认密码
        if password == confirm_password:
            # 操作auth_user表，添加数据
            # User.objects.create(username=username, password=password)  # 密码不会被加密
            user = User.objects.create_user(username=username, password=password)  # 创建用户，密码会被加密
            # User.objects.create_superuser(username=username, password=password, email='111@qq.com')
            # print(user)
            auth.login(request, user)  # 保存登录信息
            return redirect('/home/')  # 跳转到指定页面

    return render(request, 'register.html')
```

# 三、扩展`auth_user`字段
1. 第一种方式，使用一对一外键关联表
    ```python
    from django.contrib.auth.models import User
    
    class UserDetail(models.Model):
        phone = models.CharField(max_length=12, verbose_name='电话号码')
        user = models.OneToOneField(to='User', to_field='id')
    ```
    * 该方式对于`auth`模块操作不适用
2. 第二种方式，利用面向对象的继承`AbstractUser`类
    * 如果继承了 `AbstractUser`类 在执行数据看迁移命名后，`auth_user`表就不会在创建，而`user_info`表中会出现`auth_user`表中的所有字段和自己扩展的字段
    * 前提
        1. 在继承之前没有执行过数据库迁移命名(`auth_user` 表没有被创建才能使用)
        2. 继承的类里面不能覆盖`AbstractUser`中的字段
        3. 需要在配置文件中声明使用`userinfo`替换`auth_user`表 : `AUTH_USER_MODEL = 'app_name.UserInfo'`

    ```python
    from django.contrib.auth.models import User, AbstractUser
    class UserInfo(AbstractUser):
        """
        如果继承了 `AbstractUser` 在执行数据看迁移命名后，`auth_user`表就不会在创建，
        而`userinfo`表中会出现`auth_user`表中的所有字段和自己扩展的字段
    
        前提:
            1. 在继承之前没有执行过数据库迁移命名 ( auth_user 表没有被创建才能使用)
            2. 继承的类里面不能覆盖AbstractUser中的字段
            3. 需要在配置文件中声明使用user_info替换auth_user表 : AUTH_USER_MODEL = 'app_name.UserInfo'
        """
    ```
    * **如果自己写表替换了原来的表，`auth`模块功能不受影响** 