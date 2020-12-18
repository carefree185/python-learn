# 一、项目开发流程
1. 需求分析
    * 架构师+产品经理+开发者组长 和客户谈需求。
    * 先大致了解客户的需求，然后事先设计一套方案。
    * 和客户沟通，引导客户走向我们的方案设计
    * 形成一个初步方案
2. 项目设计(架构师做项目设计)
    * 选择技术
        * 编程语言
        * 框架
        * 数据库的选择
            * 主数据库
            * 缓存数据库

    * 划分功能

    * 给开发者分配任务
    
    * 项目报价
        * 技术：人 时间
        * 公司：售后 客服
        * 签字确认
        * 和客户沟通价格

3. 分组开发
    * 开发组组长找组员，安排功能开发
    * 功能开发过程中，需要先测试是否存在`bug`
    * 工资组成(为了避税)
        * 底薪
        * 绩效
        * 岗位津贴
        * 生活补贴

4. 测试
    * 测试部门测试代码
    * 压力测试
    ...

5. 交付上线
    * 交给客户的运维人员
    * 自己上线，维护，收取维护费用


# 二、`BBS`项目(模仿博客园)
模仿博客园页面，`Django`全栈项目。

## 2.1 表设计
**表设计是项目的核心，只有表设计的合理，才能更好的属性功能代码**

1. 用户表
    * 继承`AbstratcUser`
       * 扩展字段
            1. `phone`: 手机号
            2. `avatar`: 用户头像
            3. `create_time`: 注册时间
    * 外键字符段
        * 个人站点表: 一对一

2. 个人站点表
    * 普通字段
        * `site_name`: 站点名称
        * `site_title`: 站点标题
        * `site_theme`: 站点样式
    

3. 文章标签表
    * 普通字段
        * `name`: 标签名
    * 外键字段
        * 一对多个人站点    

4. 文章分类表
    * 普通字段
        * `name`: 分类名
    * 外键字段
        * 一对多个人站点 

5. 文章表
    * 普通字段
        * `title`: 文章标题
        * `desc`: 文章摘要
        * `content`: 文章内容
        * `create_time`: 文章发布时间
    
        * 数据库字段设计优化，虽然下面的数据可以跨表查询计算出来，但是效率极低。同步操作提高查询效率
            * `up_num`: 点赞
            * `down_num`: 点踩
            * `comment_num`: 评论
    * 外键字段
        * 一对多个人站点
        * 多对多文章标签表
        * 一对多文章分类表


6. 文章点赞点踩表(记录用户给文章是点赞还点踩)
    * 外键字段
        * `user`：用户主键 `ForeignKey(to='User')`
        * `article`：文章主键 `ForeignKey(to='Ariticle')`
    * 普通字段
        * `is_up`：点赞
        * `is_down`：点踩

7. 文章评论表(记录用户给文章写的评论)
    * 外键字段
        * `user`：用户主键 `ForeignKey(to='User')`
        * `article`：文章主键 `ForeignKey(to='Ariticle')`
        * `parent`: `ForeignKey(to='Comment', null=True)`(自关联) 子评论与根评论是一对多关系。(`ORM`提供的自关联`ForeignKey(to='self', null=True)`)
    * 普通字段
        * `content`: 评论内容 
        * `comment_time`: 评论时间
    
**图解**
![](https://images.gitee.com/uploads/images/2020/1215/195413_7f0a596d_7841459.png "BBS项目表关系图解.png")

## 2.2 表创建
```python
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
"""
先写普通字段
再写外键字段
"""


# 用户表
class UserInfo(AbstractUser):
    phone = models.BigIntegerField(null=True,  # 手机号可以为空
                                   verbose_name='手机号'
                                   )

    # 头像
    avatar = models.FileField(upload_to='avatar/',
                              default='avatar/default.png',
                              verbose_name='头像'
                              )
    """
    给avatar字段传文件对象，该文件会自动存放在avatar文件夹下，字段保存文件路径, 用户不修改这使用默认头像
    """
    create_time = models.DateField(auto_now_add=True)

    blog = models.OneToOneField(to='Blog', null=True)


# 个人站点
class Blog(models.Model):
    site_name = models.CharField(verbose_name='站点名称',
                                 max_length=32
                                 )

    site_title = models.CharField(verbose_name='站点标题',
                                  max_length=32
                                  )

    # 模拟样式内部操作
    site_theme = models.CharField(verbose_name='站点样式',
                                  max_length=64
                                  )  # 保存css/js的文件路径


# 分类
class Category(models.Model):
    name = models.CharField(verbose_name='文章分类', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)


# 标签
class Tag(models.Model):
    name = models.CharField(verbose_name='文章标签', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)


# 文章
class Article(models.Model):
    title = models.CharField(verbose_name='文章标题', max_length=64)
    desc = models.CharField(verbose_name='文章简介', max_length=255)
    # 文章内容很多
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 数据库字段设计优化
    up_num = models.BigIntegerField(default=0, verbose_name='点赞数')
    down_num = models.BigIntegerField(default=0, verbose_name='点踩数')
    comment_num = models.BigIntegerField(default=0, verbose_name='评论数')

    # 外键字段
    blog = models.ForeignKey(to='Blog', null=True)
    category = models.ForeignKey(to='Category', null=True)
    tags = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'))


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')


# 点赞点踩表
class UpAndDown(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')

    is_up = models.BooleanField()  # 传bool存0或1
    is_down = models.BooleanField()


# 评论
class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    # 自关联
    parent = models.ForeignKey(to='self', verbose_name='根评论', null=True)  # 有些评论只是根评论
```

## 2.3 注册功能
* forms组件
* 用户头像前端实时展示
* Ajax
### 2.3.1 注册功能的`forms`组件

1. 组件代码
    ```python
    # 正对用户的forms组件
    from django import forms
    from userapp import models
    
    class RegForm(forms.Form):
        """
        用于注册的forms组件
        username: 用户名
        password: 密码
        confirm_password: 确认密码
        email: 邮箱
        """
        username = forms.CharField(label='用户名',  # 标签名
                                   min_length=1,  # 用户名长度限制
                                   max_length=8,
                                   error_messages={  # 错误信息
                                       'required': '用户名不能为空',
                                       'min_length': '用户名最少1位字符',
                                       'max_length': '用户名最多8位字符',
                                   },
                                   widget=forms.widgets.TextInput(attrs={'class': 'form-control'})  # type='text' 并添加class属性
                                   )  # 用户名
        
        password = forms.CharField(label='密码',
                                   min_length=8,
                                   max_length=18,
                                   error_messages={
                                       'required': '密码不能为空',
                                       'min_length': '密码最少8位字符',
                                       'max_length': '密码最多18位字符',
                                   },
                                   widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                   )  # 用户密码
        confirm_password = forms.CharField(label='确认密码',
                                           min_length=8,
                                           max_length=18,
                                           error_messages={
                                               'required': '密码不能为空',
                                               'min_length': '密码最少8位字符',
                                               'max_length': '密码最多18位字符',
                                           },
                                           widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                          )  # 确认密码
    
        email = forms.EmailField(label='邮箱',
                                 error_messages={
                                     'required': '邮箱不能为空',
                                     'invalid': '邮箱格式不正确'
                                 },
                                 widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
                                 )  # 邮箱
    
        # 钩子函数
        # 局部钩子，校验用户名是否已存在
        def clean_username(self):  
            """
            校验用户名是否存在，存在这不允许注册
            :return: 将勾出来的数据返回
            """
            username = self.cleaned_data.get('username')
            is_exist = models.UserInfo.objects.first(username=username)
            if is_exist:
                # 添加提示信息
                self.add_error("username", '用户名已存在')
            return username
    
        # 全局钩子，校验两次密码是否一致
        def clean(self):  
            """
            校验两次输入的密码是否一致，不一致提示
            :return: 全局钩子会将所有的数据拿出来，记得返回
            """
            password = self.cleaned_data.get('password')
            confirm_password = self.cleaned_data.get("confirm_password")
            if not (password == confirm_password):
                self.add_error("confirm_password", '两次密码不一致')
            return self.cleaned_data
    ```
2. 页面渲染
    * 视图函数
        ```python
        from . import form
        
        
        def register(request):
            reg_form = form.RegForm()  # 生成一个空对象，并传递到前端页面
        
            return render(request, 'register.html', locals())
        ```
    * 前端页面的渲染
        ```django
        {% load static %}
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
            <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
            <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
            <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>   <!--bootstrap依赖jQuery-->
            <link rel="stylesheet" href="{% static 'font-awesome/css/font-awesome.css' %}">
            <link rel="stylesheet" href="{% static 'bootstrap-sweetalert/dist/sweetalert.css' %}">
            <script src="'{% static 'bootstrap-sweetalert/dist/sweetalert.js' %}"></script>
        </head>
        <body>
        <div class="container">
            <div class="row">
                <div class="col-md-8 col-md-offset-2">
                    <h1 class="text-center">注册</h1>
                    <form id="myform">
                        {% csrf_token %}  <!--跨域请求校验-->
        
                        {% for form_obj in reg_form %}
                            <div class="form-group">
                                <label for="">{{ form_obj.label }}</label>
                                {{ form_obj }}
                                <span style="color: red">{{ form_obj.errors.0 }}</span>
                            </div>
                        {% endfor %}  <!--渲染输入控件-->
                        <div class="form-group">
                            <label for="">头像</label>
                            <input type="file" id="myfile" name="avatar">
                        </div> <!--头像-->
        
                        <input type="button" class="btn btn-primary pull-right" value="注册" id="id_commit"> <!--提交数据-->
                    </form>
                </div>
        
            </div>
        
        </div>
        </body>
        </html>
        ```
3. 通过以上代码渲染出来的页面
![](https://images.gitee.com/uploads/images/2020/1215/222312_65115c04_7841459.png "屏幕截图.png")

### 2.3.2 头像实时展示
用户选择头像后，就实时展示出来，
* 优化一些之前的模板
    ```django
    <div class="form-group">
        <label for="myfile">
            头像 <img src="{% static 'image/default.png' %}" alt="头像" width="40px" height="40px" style="margin-left: 10px">
        </label>
        <input type="file" id="myfile" name="avatar" style="display: none">
    </div>
    ```

    * 优化后的页面![](https://images.gitee.com/uploads/images/2020/1215/223325_8b0d2ba9_7841459.png "屏幕截图.png")

    * 点击头像就可以上传文件了

* **实现选择图片后实时展示出来** 
    1. 给输入头像的标签`id="myfile""`绑定文本域变化事件
        ```html
        <script>
            // 绑定文本域变化事件
            $("#myfile").change(function () {
                // 文件阅读器对象
                // 1. 先生成一个文件阅读器对象
                let myFileReader = new FileReader();  // 生成文件阅读器对象
                // 2. 获取用户上传的头像文件
                let fileObj = $(this)[0].files[0];  // 获取文件对象
                // 3. 将文件对象交给文件阅读读取
                myFileReader.readAsDataURL(fileObj);  // 异步的io操作
                // 4. 利用文件阅读器，将文件展示到前端页面, 修改img标签的src属性
                // 等待fileReader文件读取完毕
                myFileReader.onload = function () {
                    $("#my_img").attr('src', myFileReader.result)
                }
            })
        </script>
        ```
    2. 优化后，选择图片后的效果
    ![](https://images.gitee.com/uploads/images/2020/1215/225334_8ea91536_7841459.png "屏幕截图.png")

### 2.3.3 `Ajax`发送`post`请求进行注册
* 给按钮标签`id="id_commit"`绑定点击事件，发送`post`请求
    ```js
     //绑定点击事件
        $("input:button").click(function () {
        // 发送Ajax请求，发送的数据包含普通键值对和文件对象
        // 1. 生成FormData对象
        let formDataObj = new FormData()
        // 2. 添加数据普通键值对数据  $("#myform").serializeArray()
        $.each($("#myform").serializeArray(), function (index, obj) {
            {#console.log(index, obj)#} // obj 自定义对象
            formDataObj.append(obj.name, obj.value)
        })
        // 3. 添加文件数据
        formDataObj.append('avatar', $("#myfile")[0].files[0])
    
        // 4. 发送ajax请求
        $.ajax({
            url:'',
            type:'post',
            data: formDataObj,
            // 两个关键参数
            contentType: false,
            processData: false,
            success: function (args) {
                if (args.code === 1000) {
                    // 跳转到登录页面
                    window.location.href = args.url
                } else {
                    // 如何将对于的错误提示展示到input框下面
                    // forms主键渲染的id值都是 id_字段名
                    $.each(args.msg, function (index, obj) {
                        // index: 字段名 obj: 报错信息数组
                        let targetId = "#id_" + index;  // 拼接id值
                        $(targetId).next().text(obj[0]).parent().addClass('has-error')
                    })
                }
            }
        })
    })
    ```
* 后端数据校验(视图函数)
    ```python
    def register(request):
        """
        注册视图函数
        :param request:
        :return:
        """
        reg_form_obj = form.RegForm()
        back_dic = {"code": 1000, 'msg': ''}
        if request.method == 'POST':  # 如果访问的是post请求执行如下代码
            # 校验数据是否合法
            reg_form_obj = form.RegForm(request.POST)
            # 判断数据是否合法
            if reg_form_obj.is_valid():
                cleaned_data = reg_form_obj.cleaned_data  # 将校验通过的字典，赋值给变量，
                # 将字典中的confirm_password删除
                cleaned_data.pop('confirm_password')
                # 获取用户头像
                file = request.FILES.get('avatar')  # 判断用户头像是否传值，不能直接添加到字典中
                if file:
                    cleaned_data['avatar'] = file
                # 操作数据库保存数据
                models.UserInfo.objects.create_user(**cleaned_data)  # 创建用户，并刷新刷新到数据库
                back_dic['url'] = reverse('userapp:login')  # 注册成功后默认跳转到登录
            else:
                back_dic['code'] = 2000  # 登录失败后的校验数据
                back_dic['msg'] = reg_form_obj.errors
    
            return JsonResponse(back_dic, json_dumps_params={"ensure_ascii": False})
    
        return render(request, 'register.html', locals())
    ```
* 前端代码的继续优化；目前，展示错误信息后，再次点击输入框，依旧会展示错误信息。现在，使输入框获取焦点后，清除提示信息. 给所有的input标签绑定获取焦点事件。
    ```js
    // 给input标签添加后去焦点事件焦点
    $("input").focus(function () {
        // 将获取焦点的input框
        $(this).next().text("").parent().removeClass('has-error')
    })
    ```

### 2.3.4 注册功能的完整代码
1. forms主键
    ```python
    from django import forms
    from userapp import models
    
    
    # 注册
    class RegForm(forms.Form):
        """
        用于注册的forms组件
        username: 用户名
        password: 密码
        confirm_password: 确认密码
        email: 邮箱
        """
        username = forms.CharField(label='用户名',  # 标签名
                                   min_length=1,  # 用户名长度限制
                                   max_length=8,
                                   error_messages={  # 错误信息
                                       'required': '用户名不能为空',
                                       'min_length': '用户名最少1位字符',
                                       'max_length': '用户名最多8位字符',
                                   },
                                   widget=forms.widgets.TextInput(attrs={'class': 'form-control'})  # type='text' 并添加class属性
                                   )  # 用户名
    
        password = forms.CharField(label='密码',
                                   min_length=8,
                                   max_length=18,
                                   error_messages={
                                       'required': '密码不能为空',
                                       'min_length': '密码最少8位字符',
                                       'max_length': '密码最多18位字符',
                                   },
                                   widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                   )  # 用户密码
        confirm_password = forms.CharField(label='确认密码',
                                           min_length=8,
                                           max_length=18,
                                           error_messages={
                                               'required': '密码不能为空',
                                               'min_length': '密码最少8位字符',
                                               'max_length': '密码最多18位字符',
                                           },
                                           widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                          )  # 确认密码
    
        email = forms.EmailField(label='邮箱',
                                 error_messages={
                                     'required': '邮箱不能为空',
                                     'invalid': '邮箱格式不正确'
                                 },
                                 widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
                                 )  # 邮箱
    
        # 钩子函数
        # 局部钩子，校验用户名是否已存在
        def clean_username(self):
            """
            校验用户名是否存在，存在这不允许注册
            :return: 将勾出来的数据返回
            """
            username = self.cleaned_data.get('username')
            is_exist = models.UserInfo.objects.filter(username=username)
            if is_exist:
                # 添加提示信息
                self.add_error("username", '用户名已存在')
            return username
    
        # 全局钩子，校验两次密码是否一致
        def clean(self):
            """
            校验两次输入的密码是否一致，不一致提示
            :return: 全局钩子会将所有的数据拿出来，记得返回
            """
            password = self.cleaned_data.get('password')
            confirm_password = self.cleaned_data.get("confirm_password")
            if not (password == confirm_password):
                self.add_error("confirm_password", '两次密码不一致')
            return self.cleaned_data
    
    ```
2. 视图函数
    ```python
    from django.shortcuts import render, reverse
    from django.http import JsonResponse
    from . import form, models
    
    
    # Create your views here.
    def register(request):
        """
        注册视图函数
        :param request:
        :return:
        """
        reg_form_obj = form.RegForm()
        back_dic = {"code": 1000, 'msg': ''}
        if request.method == 'POST':  # 如果访问的是post请求执行如下代码
            # 校验数据是否合法
            reg_form_obj = form.RegForm(request.POST)
            # 判断数据是否合法
            if reg_form_obj.is_valid():
                cleaned_data = reg_form_obj.cleaned_data  # 将校验通过的字典，赋值给变量，
                # 将字典中的confirm_password删除
                cleaned_data.pop('confirm_password')
                # 获取用户头像
                file = request.FILES.get('avatar')  # 判断用户头像是否传值，不能直接添加到字典中
                if file:
                    cleaned_data['avatar'] = file
                # 操作数据库保存数据
                models.UserInfo.objects.create_user(**cleaned_data)  # 创建用户，并刷新刷新到数据库
                back_dic['url'] = reverse('userapp:login')  # 注册成功后默认跳转到登录
            else:
                back_dic['code'] = 2000  # 登录失败后的校验数据
                back_dic['msg'] = reg_form_obj.errors
    
            return JsonResponse(back_dic, json_dumps_params={"ensure_ascii": False})
    
        return render(request, 'register.html', locals())
    
    ```
3. 前端模板
    ```django
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
        <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
        <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>   <!--bootstrap依赖jQuery-->
        <link rel="stylesheet" href="{% static 'font-awesome/css/font-awesome.css' %}">
        <link rel="stylesheet" href="{% static 'bootstrap-sweetalert/dist/sweetalert.css' %}">
        <script src="'{% static 'bootstrap-sweetalert/dist/sweetalert.js' %}"></script>
    </head>
    <body>
    <div class="container">
        <div class="row">
            <div class="col-md-8 col-md-offset-2">
                <h1 class="text-center">注册</h1>
                <form id="myform">
                    {% csrf_token %}
    
                    {% for form_obj in reg_form_obj %}
                        <div class="form-group">
                            <label for="{{ form_obj.auto_id }}">{{ form_obj.label }}</label>
                            {{ form_obj }}
                            <span style="color: red" class="pull-right">{{ form_obj.errors.0 }}</span>
                        </div>
                    {% endfor %}
                    <div class="form-group">
                        <label for="myfile">
                            头像 <img src="{% static 'image/default.png' %}" alt="" id="my_img" width="50px" height="50px" style="margin-left: 10px">
                        </label>
                        <input type="file" id="myfile" name="avatar" style="display: none">
                    </div>
                    <input type="button" class="btn btn-primary pull-right" value="注册" id="id_commit">
                </form>
            </div>
    
        </div>
    </div>
    <script>
        // 绑定文本域变化事件
        $("#myfile").change(function () {
            // 文件阅读器对象
            // 1. 先生成一个文件阅读器对象
            let myFileReader = new FileReader();  // 生成文件阅读器对象
            // 2. 获取用户上传的头像文件
            let fileObj = $(this)[0].files[0];  // 获取文件对象
            // 3. 将文件对象交给文件阅读读取
            myFileReader.readAsDataURL(fileObj);  // 异步的io操作
            // 4. 利用文件阅读器，将文件展示到前端页面, 修改img标签的src属性
            // 等待fileReader文件读取完毕
            myFileReader.onload = function () {
                $("#my_img").attr('src', myFileReader.result)
            }
        })
    
        //绑定点击事件
        $("input:button").click(function () {
            // 发送Ajax请求，发送的数据包含普通键值对和文件对象
            // 1. 生成FormData对象
            let formDataObj = new FormData()
            // 2. 添加数据普通键值对数据  $("#myform").serializeArray()
            $.each($("#myform").serializeArray(), function (index, obj) {
                {#console.log(index, obj)#} // obj 自定义对象
                formDataObj.append(obj.name, obj.value)
            })
            // 3. 添加文件数据
            formDataObj.append('avatar', $("#myfile")[0].files[0])
    
            // 4. 发送ajax请求
            $.ajax({
                url:'',
                type:'post',
                data: formDataObj,
                // 两个关键参数
                contentType: false,
                processData: false,
                success: function (args) {
                    if (args.code === 1000) {
                        // 跳转到登录页面
                        window.location.href = args.url
                    } else {
                        // 如何将对于的错误提示展示到input框下面
                        // forms主键渲染的id值都是 id_字段名
                        $.each(args.msg, function (index, obj) {
                            // index: 字段名 obj: 报错信息数组
                            let targetId = "#id_" + index;  // 拼接id值
                            $(targetId).next().text(obj[0]).parent().addClass('has-error')
                        })
                    }
                }
            })
        })
    
        // 给input标签添加后去焦点事件焦点
        $("input").focus(function () {
            // 将获取焦点的input框
            $(this).next().text("").parent().removeClass('has-error')
        })
    
    </script>
    
    </body>
    </html>
    ```

## 2.4 登录功能
* 图片验证码(自定义)
* Ajax
### 2.4.1 前端模板的搭建，效果如下图
![](https://images.gitee.com/uploads/images/2020/1216/002223_612d9f4b_7841459.png "屏幕截图.png")
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
    <script src="{% static 'js/JQuery-3.5.1.js' %}"></script>
    <script src="{% static 'bootstrap/js/bootstrap.js' %}"></script>   <!--bootstrap依赖jQuery-->
    <link rel="stylesheet" href="{% static 'font-awesome/css/font-awesome.css' %}">
    <link rel="stylesheet" href="{% static 'bootstrap-sweetalert/dist/sweetalert.css' %}">
    <script src="'{% static 'bootstrap-sweetalert/dist/sweetalert.js' %}"></script>
</head>
<body>
<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
            <h1 class="text-center">登录</h1>
            <div class="form-group">
                <label for="id_username">用户名</label>
                <input type="text" id="id_username" name="username" class="form-control">
            </div>
            <div class="form-group">
                <label for="id_password">密&emsp;码</label>
                <input type="password" id="id_password" name="password" class="form-control">
            </div>
            <div class="form-group">
                <label for="id_code">验证码</label>
                <div class="row">
                    <div class="col-md-6">
                        <input type="text" name="code" id="id_code" class="form-control">
                    </div>
                    <div class="col-md-6">
                        <img src="{% static 'image/default.png' %}" alt="" width="380px" height="34px" style="border-radius: 4px">
                    </div>
                </div>

            </div>
            <input type="button" class="btn btn-success" value="登录">

        </div>
    </div>
</div>
</body>
</html>
```
### 2.4.2 图片验证码
1. 每次访问都需要展示不同的验证码，所以要在后端生成这个验证码。兴建一个生成验证码的`url`，对应的视图函数如下。
    ```python
    from PIL import Image, ImageDraw, ImageFont
    """
    Image: 生成图片片
    ImageDraw：绘画图片
    ImageFont：控制字体样式
    """
    import random
    from io import BytesIO, StringIO
    """
    BytesIOL: 临时在内存中存放数据， 二进制io
    StringIO: 字符串io
    """
    def get_rgb():
        """
        生成颜色，三基色
        :return:
        """
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    
    def get_code(request):
        # 方式一、直接获取现成的图片数据
        # with open(r'C:\Users\23219\Desktop\BBS\static\image\111.jpg', 'rb') as f:
        #     data = f.read()
    
        # # 方式二、利用pillow模块产生图片(模式, 尺寸, 三基色)
        # img_obj = Image.new('RGB', (380, 34), get_rgb())
        # # 先将图片对象保存起来，在读取出来，
        # with open('xxx.png', 'wb') as f1:
        #     img_obj.save(f1, 'png')
        #
        # with open('xxx.png', 'rb') as f2:
        #     data = f2.read()
    
        # 方式三、方式二的io操作太多，使用io模块
        # img_obj = Image.new('RGB', (380, 34), get_rgb())
        # io_obj = BytesIO()  # 看出一个文件句柄
        # img_obj.save(io_obj, 'png')
        # data = io_obj.getvalue()
    
        # 给图片写字
        img_obj = Image.new('RGB', (380, 34), get_rgb())
        img_draw = ImageDraw.Draw(img_obj)  # 产生画笔对象
        img_font = ImageFont.truetype(r'C:\Users\23219\Desktop\BBS\static\fonts\杨任东竹石体-Extralight.ttf', 30)  # 字体样式，大小
    
        # 随机验证码(包含数字 大小写字母)
        code = ''  # 随机验证码，登录视图函数，需要使用，其他地方也要获取到（session）
        for i in range(5):
            random_upper = chr(random.randint(65, 90))
            random_lower = chr(random.randint(97, 122))
            random_int = str(random.randint(0, 9))
            # 从上面随机选择一个
            tem = random.choice([random_upper, random_lower, random_int])
            # 将产生的随机字符串写入图片, 生成好了之后无法控制间隙
            img_draw.text((i*60+60, -1), tem, get_rgb(), img_font)
            # 凭借随机字符串
            code += tem
        request.session['code'] = code  # 生成的验证码要在登录的视图函数中能获取，将它保存到session中
        io_obj = BytesIO()  # 为了降低io操作，是同io模块让图片在内存进行生成
        img_obj.save(io_obj, 'png')
        data = io_obj.getvalue()   # 获取图片数据
        return HttpResponse(data)
    ```
2. 修改登录页面的前端代码, 就是在`img`标签的`src`属性中使用反向解析得到产生图片的`url`
    ```django
    <div class="form-group">
                    <label for="id_code">验证码</label>
                    <div class="row">
                        <div class="col-md-6">
                            <input type="text" name="code" id="id_code" class="form-control">
                        </div>
                        <div class="col-md-6">
                            <img src="{% url 'userapp:get_code' %}" id="id_image" alt="" width="380px" height="34px" style="border-radius: 4px">
                        </div>
                    </div>
                </div>
    ```
3. 如果验证码看不清除，就需要重写获取图片验证码。由于页面上的`url`发送变化使，浏览器会自动发送请求。可以给`img`标签绑定点击事件，修改`url`后缀
    ```html
    <script>
        // 给标签绑定点击事件, 每次点击都获取一个图片
        $('#id_image').click(function () {
            let oldVal = $(this).attr('src')
            let reg = /.*\?$/  // 生成一个正则对象，匹配默认是否含有?
            if (reg.test(oldVal)) {
                reg.lastIndex = 0
                $(this).attr('src', oldVal.replace(/\?$/, ''))  // 如果有，将?替换为""
            } else {
                $(this).attr('src', oldVal+='?') // 没有，拼接一个?
            }
        })
    </script>
    ```
* 给登录按钮绑定点击事件，向后端发送Ajax请求
    ```js
    // 点击发送ajax请求
    $("#id_commit").click(function () {
        $.ajax({
            url:'',
            type: 'post',
            data:{
                'username': $("#id_username").val(),
                'password': $("#id_password").val(),
                'code': $("#id_code").val(),
                {#'csrfmiddlewaretoken':'{{ csrf_token }}', // 选择第三种方式#}
            },
            success: function (args) {
                if(args.code === 1000) {
                    // 跳转到后端返回的路由
                    window.location.href = args.url
                } else {
                    $('#error').text(args.msg)
                }
    
            }
        })
    })
    ```

### 2.4.3 后端数据校验
```python
def login(request):
    """
    登录功能
    :param request:
    :return:
    """
    back_dic = {'code': 1000, 'msg': ''}
    if request.method == 'POST':  # post请求校验数据
        username = request.POST.get("username")
        password = request.POST.get('password')
        coed = request.POST.get('code')  # 验证码
        # 校验验证码是否正确 忽略大小写
        if request.session.get('code', '').lower() == coed.lower():  # 将验证码转为小写进行比较
            # 校验用户名密码是否正确
            user = auth.authenticate(request, username=username, password=password)
            if user:
                # 保存用户状态
                auth.login(request, user)
                back_dic['url'] = '/'   # 登录成功跳转到首页
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)  # 给ajax返回响应数据

    return render(request, 'login.html')  # get请求返回登录页面
```

## 2.5 首页搭建
首页整体样式
![](https://images.gitee.com/uploads/images/2020/1216/173455_952437e8_7841459.png "屏幕截图.png")
> 中间展示文章，两边展示其他内容或是广告等


### 2.5.1 导航栏
* 导航条根据用户是否登录展示不同的内容
![](https://images.gitee.com/uploads/images/2020/1216/110947_f3e62174_7841459.png "屏幕截图.png")
    * 当用户登录了，显示用户名和更多操作
    * 用户没有登录，显示注册和登录
    ```django
    <ul class="nav navbar-nav navbar-right">
        {% if request.user.is_authenticated %}
              <li><a href="#">{{ request.user.username }}</a></li>
              <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">更多操作 <span class="caret"></span></a>
              <ul class="dropdown-menu">
                  <li><a href="#">修改密码</a></li>
                  <li><a href="#">修改头像</a></li>
                  <li><a href="#">后台管理</a></li>
                  <li role="separator" class="divider"></li>
                  <li><a href="#">注销</a></li>
              </ul>
            </li>
        {% else %}
            <li><a href="{% url 'userapp:register' %}">注册</a></li>
            <li><a href="{% url 'userapp:login' %}">登录</a></li>
        {% endif %}
    </ul>
    ```
* 用户登录后修改密码和注销登录
    * 前端使用模态框展示
        ```html
        <!-- Large modal -->
        <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
           <div class="modal-dialog modal-lg" role="document">
               <div class="modal-content">
                   <h1 class="text-center">修改密码</h1>
                   <div class="row">
                       <div class="col-md-8 col-md-offset-2">
                           <div class="form-group">
                               <label for="">用户名</label>
                               <input type="text" disabled value="{{ request.user.username }}" class="form-control">
                           </div>
                           <div class="form-group">
                               <label for="id_old_password">原密码</label>
                               <input type="password" id="id_old_password" name="old_password" class="form-control">
                           </div>
                           <div class="form-group">
                               <label for="id_new_password">新密码</label>
                               <input type="password" id="id_new_password" name="new_password" class="form-control">
                           </div>
                           <div class="form-group">
                               <label for="id_confirm_password">确认密码</label>
                               <input type="password" id="id_confirm_password" name="confirm_password" class="form-control">
                           </div>
                           <div class="modal-footer">
                               <button type="button" class="btn btn-danger pull-left" data-dismiss="modal">取消</button>
                               <button type="button" class="btn btn-primary" id="id_edit">修改</button>
                               <span id="set_error" style="color: red"></span>
                           </div>
                       </div>
                   </div>
               </div>
           </div>
        </div>
        ```
    * 后端修改密码和注销登录逻辑
        ```python
        @login_required
        def set_password(request):
            """
            修改密码
            :param request:
            :return:
            """
            if request.is_ajax():
                back_dic = {'code': 1000, 'msg': ''}
                if request.method == 'POST':
                    old_password = request.POST.get("old_password")
                    new_password = request.POST.get("new_password")
                    confirm_password = request.POST.get('confirm_password')
                    is_right = request.user.check_password(old_password)  # 校验原密码是否正确
                    if is_right:
                        if new_password == confirm_password:
                            request.user.set_password(new_password)
                            request.user.save()
                            back_dic['msg'] = '修改成功'
                            back_dic['url'] = reverse('userapp:login')  # 修改成功跳转到登录页面
                        else:
                            back_dic['code'] = 2000
                            back_dic['msg'] = '两次密码不一致'
                    else:
                        back_dic['code'] = 3000
                        back_dic['msg'] = '原密码不正确'
        
                return JsonResponse(back_dic)
        
            return HttpResponse('ok')
        
        
        @login_required
        def logout(request):
            """
            退出登录
            :param request:
            :return:
            """
            auth.logout(request)
            return redirect('/')  # 退出登录后定向到首页
        ```
    * 通过Ajax发送修改密码的请求
        ```js
        $('#id_edit').click(function () {
            $.ajax({
                url:'{% url "userapp:set_password" %}',
                type: 'post',
                data: {
                    'old_password': $("#id_old_password").val(),
                    "new_password": $("#id_new_password").val(),
                    'confirm_password': $("#id_confirm_password").val(),
                },
                success: function (args) {
                    if(args.code === 1000) {
                        window.location.href = args.url
                    }else {
                        $("#set_error").text(args.msg)
                    }
        
                }
            })
        })
        ```
### 2.5.2 侧边栏搭建
```html
<div class="container-fluid">
    <div class="row">
        <div class="col-md-2">
            <div class="panel panel-primary">
              <div class="panel-heading">
                  <h3 class="panel-title">广告</h3>
              </div>
              <div class="panel-body">
                  。。。。。
              </div>
            </div>
            <div class="panel panel-primary">
              <div class="panel-heading">
                  <h3 class="panel-title">广告</h3>
              </div>
              <div class="panel-body">
                  。。。。。
              </div>
            </div>
            <div class="panel panel-primary">
              <div class="panel-heading">
                  <h3 class="panel-title">广告</h3>
              </div>
              <div class="panel-body">
                  。。。。。
              </div>
            </div>

        </div>

        <div class="col-md-8">文章</div>

        <div class="col-md-2">
            <div class="panel panel-primary">
              <div class="panel-heading">
                  <h3 class="panel-title">广告</h3>
              </div>
              <div class="panel-body">
                  。。。。。
              </div>
            </div>
            <div class="panel panel-primary">
              <div class="panel-heading">
                  <h3 class="panel-title">广告</h3>
              </div>
              <div class="panel-body">
                  。。。。。
              </div>
            </div>
            <div class="panel panel-primary">
              <div class="panel-heading">
                  <h3 class="panel-title">广告</h3>
              </div>
              <div class="panel-body">
                  。。。。。
              </div>
            </div>

        </div>

    </div>

</div>
```
### 2.5.2 文章区域搭建
**文章区域样式** 
![](https://images.gitee.com/uploads/images/2020/1216/201226_5bf93ce3_7841459.png "屏幕截图.png")
* 在搭建文章区域时，要使用数据，需要提前准备。
* 使用`admin`后台管理系统可以方便的操作我们的数据表
* 使用`admin`后台管理系统操作表，先到`app/admin.py`种绑定表
    ```python
    from django.contrib import admin
    from . import models
    
    
    # Register your models here.
    
    admin.site.register(models.UserInfo)
    admin.site.register(models.Blog)
    admin.site.register(models.Tag)
    admin.site.register(models.Category)
    admin.site.register(models.Article)
    admin.site.register(models.Article2Tag)
    admin.site.register(models.UpAndDown)
    admin.site.register(models.Comment)
    ```
* `admin`后台展示的表名可以在模型类种定义如下类进行控制
    ```python
    class Meta:
        verbose_name_plural = '用户表'  # 修改admin后台管理的表名
    ```
* 如何展示用户头像(开放更多的后台接口)
    1. 配置`MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`
    2. 开放接口
        ```python
        from django.views.static import serve
        # 开设后端自定文件夹资源
        url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
        ```
        1. `serve`: 用于开放文件的访问
        2. `{'document_root': MEDIA_ROOT}`: 指定开发文件的路径

* 展示文章
    1. 先查询出全部的文章（分页）返回到前端
        ```python
        article_queryset = models.Article.objects.all()
        ```
    2. 前端    
        ```django
        <ul class="media-list">
            {% for article in article_queryset %}  <!--循环遍历获取文章数据对象-->
                <li class="media">
                    <h4 class="media-heading"><a href="#"><h4 class="media-heading">{{ article.title }}<!--文章标题--> </h4></a></h4>
                    <div class="media-left">
                      <a href="#">
                        <img class="media-object" src="/media/{{ article.blog.userinfo.avatar }}" width="50px" height="50px" style="margin-left: 10px"><!--展示头像-->
                      </a>
                    </div>
                    <div class="media-body">
                      {{ article.desc }} <!--文章简介-->
                    </div>
                    <br>
                    <div>
                        <span><a href="#">{{ article.blog.userinfo.username }}</a><!--文章作者--></span>&nbsp;&nbsp;
                        <span>发布于</span>&nbsp;&nbsp;
                        <span>{{ article.create_time|date:'Y-m-d' }}<!--文章发布事件--></span>&nbsp;&nbsp;
                        <span><span class="glyphicon glyphicon-thumbs-up"> </span> 点赞 {{ article.up_num }}</span>&nbsp;&nbsp;
                        <span><span class="glyphicon glyphicon-comment"> </span> 评论 {{ article.comment_num }}</span>&nbsp;&nbsp;
        
                    </div>
                  </li>
                <hr>
            {% endfor %}
        </ul>
        ```
## 2.6 个人站点搭建
**个人站点页面** 在首页(其他页面)上点击用户名，直接跳转到站点首页
![](https://images.gitee.com/uploads/images/2020/1216/214120_be8f02f3_7841459.png "屏幕截图.png")

```python
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
      <a class="navbar-brand" href="#">{{ blog.site_title }}</a> <!--站点标题-->
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">博客 <span class="sr-only">(current)</span></a></li>
        <li><a href="#">文章</a></li>
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
          {% if request.user.is_authenticated %}
              <li><a href="#">{{ request.user.username }}</a></li>
               <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">更多操作 <span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li><a href="#"  data-toggle="modal" data-target=".bs-example-modal-lg">修改密码</a></li>
            <li><a href="#">修改头像</a></li>
            <li><a href="#">后台管理</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="{% url 'userapp:logout' %}">注销</a></li>


          </ul>
           <!-- Large modal -->
           <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
               <div class="modal-dialog modal-lg" role="document">
                   <div class="modal-content">
                       <h1 class="text-center">修改密码</h1>
                       <div class="row">
                           <div class="col-md-8 col-md-offset-2">
                               <div class="form-group">
                                   <label for="">用户名</label>
                                   <input type="text" disabled value="{{ request.user.username }}" class="form-control">
                               </div>
                               <div class="form-group">
                                   <label for="id_old_password">原密码</label>
                                   <input type="password" id="id_old_password" name="old_password" class="form-control">
                               </div>
                               <div class="form-group">
                                   <label for="id_new_password">新密码</label>
                                   <input type="password" id="id_new_password" name="new_password" class="form-control">
                               </div>
                               <div class="form-group">
                                   <label for="id_confirm_password">确认密码</label>
                                   <input type="password" id="id_confirm_password" name="confirm_password" class="form-control">
                               </div>
                               <div class="modal-footer">
                                   <button type="button" class="btn btn-danger pull-left" data-dismiss="modal">取消</button>
                                   <button type="button" class="btn btn-primary" id="id_edit">修改</button>
                                   <span id="set_error" style="color: red"></span>
                               </div>
                           </div>
                       </div>
                   </div>
               </div>
           </div>

        </li>
          {% else %}
              <li><a href="{% url 'userapp:register' %}">注册</a></li>
              <li><a href="{% url 'userapp:login' %}">登录</a></li>
          {% endif %}
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>  <!--导航条-->

<div class="container-fluid">
    <div class="row">
        <div class="col-md-3">
            <div class="panel panel-primary">
                  <div class="panel-heading">
                      <h3 class="panel-title">广告</h3>
                  </div>
                  <div class="panel-body">
                      。。。。。
                  </div>
                </div>
                <div class="panel panel-primary">
                  <div class="panel-heading">
                      <h3 class="panel-title">广告</h3>
                  </div>
                  <div class="panel-body">
                      。。。。。
                  </div>
                </div>
                <div class="panel panel-primary">
                  <div class="panel-heading">
                      <h3 class="panel-title">广告</h3>
                  </div>
                  <div class="panel-body">
                      。。。。。
                  </div>
                </div>

        </div>  <!--侧边栏-->
        <div class="col-md-9">
            <ul class="media-list">
                {% for article in article_list %}  <!--站点文章-->
                    <li class="media">
                        <h4 class="media-heading"><a href="#"><h4 class="media-heading">{{ article.title }}</h4></a></h4>
                        <div class="media-left">
                          <a href="#">
                            <img class="media-object" src="/media/{{ article.blog.userinfo.avatar }}" width="50px" height="50px" style="margin-left: 10px">
                          </a>
                        </div>
                        <div class="media-body">
                          {{ article.desc }}
                        </div>
                        <div class="pull-right">
                            <span>posted</span>&nbsp;&nbsp;
                            <span>&copy;</span>
                            <span>{{ article.create_time|date:'Y-m-d' }}</span>&nbsp;&nbsp;
                            <span>{{ article.blog.userinfo.username }}</span>&nbsp;&nbsp;
                            <span>发布于</span>&nbsp;&nbsp;
                            <span><span class="glyphicon glyphicon-thumbs-up"> </span> 点赞 {{ article.up_num }}</span>&nbsp;&nbsp;
                            <span><span class="glyphicon glyphicon-comment"> </span> 评论 {{ article.comment_num }}</span>&nbsp;&nbsp;
                            <span><a href="#">编辑</a></span>
                        </div>
                      </li>
                    <hr>
                {% endfor %}

            </ul>  <!--个人站点中的文章-->
        </div>
    </div>
</div>
```

**后端逻辑搭建**
```python
def site(request, username):
    # 获取用户名，匹配站点，匹配成功，返回站点页面
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        # 用户不能存在，返回404页面
        return render(request, 'error.html')

    blog = user.blog  # 获取站点
    article_list = models.Article.objects.filter(blog=blog)  # 筛选出当前用户站点的文章
    return render(request, 'site.html', locals())
```

**图片防盗链**
* 避免其他网站，通过`url`访问本网站资源
    * 检查当前请求是否为本网站发起的请求(请求头中`refer`参数记录请求来自哪里)
    * 可以通过修改请求头，或使用爬虫程序将资源下载到本地，用于解决无法访问的问题

## 2.7 个人站点的侧边栏跳转搭建

对于侧边栏，是对文章的进一步筛选，不用在开始页面，直接使用`site`站点进行。可以在视图函数中，对文章进行更加严格的条件筛选。
* `url`的搭建
    ```python
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)/', views.site),  # 侧边栏分类筛选功能
    ```
   ```django
    "/{{ username }}/category/{{ category.2 }}"    <!--分类筛选-->
    "/{{ username }}/tag/{{ tag.2 }}"              <!--标签筛选-->
    "/{{ username }}/archive/{{ d.0|date:'Y-m' }}" <!--日期赛选-->
   ```
* 数据进一步分类
    ```python
    if kwargs:
        # print(kwargs)  # {'condition': 'tag', 'param': '1'}
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'category':
            article_list = article_list.filter(category_id=param)
        elif condition == 'tag':
            article_list = article_list.filter(tags__pk=param)  # 跨表查询
        else:
            year, month = param.split('-')
            article_list = article_list.filter(create_time__year=year, create_time__month=month)
    ```
## 2.8 文章详情
* `url`设计
    ```python
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/', views.article_detail),
    ```
* 后端逻辑
    ```python
    def article_detail(request, username, article_id):
        """
        需要校验username和article_id是否存在
        :param request:
        :param username:
        :param article_id:
        :return:
        """
        blog = models.UserInfo.objects.filter(username=username).first().blog
        # 先获取文章对象
        article = models.Article.objects.filter(pk=article_id, blog__userinfo__username=username).first()
        if not article:
            return render(request, 'error.html')
    
        return render(request, 'article_detail.html', locals())
    ```
* 页面，文章详情页和站点首页一致，可以使用模板继承
* 侧边栏渲染需要传入参数，可以使用`inclusion_tag`，让他渲染好后填入到需要的位置
    ```python
    from django import template
    from userapp import models
    from django.db.models import Count
    
    register = template.Library()
    
    
    # 自定义inclusion_tag
    @register.inclusion_tag('left_menu.html')
    def left_menu(username):
        # 钩爪侧边栏需要的数据
        user = models.UserInfo.objects.filter(username=username).first()
        blog = user.blog
        # 查询出当前用户所以的分类及分类下的文章数
        category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list(
            'name', 'count_num', 'pk')  # 筛选站点下的分类
        print(category_list)
        # 查询出当前用户所有的标签及标签下的文章数
        tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list('name',
                                                                                                             'count_num',
                                                                                                             'pk')
        print(tag_list)
        # 将文章以年月进行分组
        from django.db.models.functions import TruncMonth
        date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
            'month').annotate(count_num=Count('pk')).values_list("month", 'count_num', 'pk')
        print(date_list)
        return locals()
    ```
* 使用`inclusion_tag`
    ```django
    {% load my_tags %}
    {% left_menu username %}
    ```

## 2.9 文章点赞点踩
* 前端，及点赞点踩的判断
    ```js
    {# 点赞点踩 #}
    <div id="div_digg">
        <div class="diggit action">
            <span class="diggnum" id="digg_count">1</span>
        </div>
        <div class="buryit action">
            <span class="burynum" id="bury_count">0</span>
        </div>
        <div class="clear"></div>
        <div class="diggword" id="digg_tips">
        </div>
    </div>
    ```
    * `$(this).hasClass('diggit')`：返回`true`表示点赞，返回`false`表示点踩
* ajax请求
    ```js
    <script src="{% static 'js/ajax_csrf_verify.js' %}"></script>
    <script>
    // 给所有的.action绑定事件
    $(".action").click(function () {
        {#alert($(this).hasClass('diggit'))#}
        let is_upper = $(this).hasClass('diggit');
        let $btn = $(this);
        // 向后端发送请求
        $.ajax({
            url: '/up_and_down/',
            type: 'post',
            data: {
                'article_id': '{{ article.pk }}',
                "is_upper": is_upper,
            },
            success: function (args) {
                if(args.code === 1000){
                    $("#digg_tips").text(args.msg)
                    // 展示数字+1
                    let oldNum = $btn.children().text();
                    $btn.children().text(Number(oldNum)+1);
                } else {
                    $("#digg_tips").html(args.msg)
                }
            }
    
        })
    
    })
    
    </script>
    ```
    * 修改点赞点踩数是，前端页面需要注意获取到的数字是子字符串。需要修改类型

* 后端，点赞点踩逻辑较多，所有单独开设一个`url`
    ```python
    def up_and_down(request):
        """
        处理点赞点踩
        1. 登录校验
        2. 文章是否为当前用户写的
        3. 当前用户是否已经对此文章点过了
        4. 操作数据库
        :param request:
        :return:
        """
        import json
        from django.db.models import F
        if request.is_ajax():
            back_dic = {'code': 1000, "msg": ''}
            # 判断当前用户是否登录
            if request.user.is_authenticated():
                article_id = request.POST.get("article_id")
                is_upper = request.POST.get("is_upper")  # 获取字符串
                is_upper = json.loads(is_upper)
                # 2. 判断当前文章是否是当前用户写的
                article = models.Article.objects.filter(pk=article_id).first()
                if not (article.blog.userinfo == request.user):
                    # 3. 校验当前用户是否点赞点踩了
                    is_click = models.UpAndDown.objects.filter(user=request.user, article=article)
                    if not is_click:
    
                        # 4. 操作数据库记录数据, 同步操作文章表的普通字段
                        # 判断当前用户是点踩还是点赞
                        if is_upper:
                            # 给点赞数+1
                            models.Article.objects.filter(pk=article_id).update(up_num=F('up_num')+1)
                            back_dic['msg'] = '点赞成功'
                        else:
                            # 给点踩数+1
                            models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                            back_dic['msg'] = '点踩成功'
                        # 操作点赞点踩表
                        models.UpAndDown.objects.create(user=request.user, article=article, is_up=is_upper)
                    else:
                        back_dic['code'] = 1001
                        back_dic['msg'] = '已经点过了，不能在点击'
                else:
                    back_dic['code'] = 1002
                    back_dic['msg'] = '不能给自己文章点'
            else:
                back_dic['code'] = 1003
                back_dic['msg'] = '请先<a href="/userapp/login/">登录</a>'
    
            return JsonResponse(back_dic)
    ```

## 2.10 评论
**先写根评论，在写子评论，后端逻辑统一**
* 后端逻辑
    ```python
    from django.db import transaction
    def comment(request):
        """
        评论
        :param request:
        :return:
        """
        if request.is_ajax():
            back_dic = {'code': 1000, "msg": ''}
            if request.method == 'POST':
                if request.user.is_authenticated():
                    article_id = request.POST.get("article_id")
                    content = request.POST.get("content")
                    parent_id = request.POST.get('parent_id')
    
                    with transaction.atomic():  # 开启事务
                        models.Article.objects.filter(pk=article_id).update(comment_num=F("comment_num") + 1)
                        models.Comment.objects.create(user=request.user, article_id=article_id, content=content,
                                                      parent_id=parent_id)
                    back_dic['msg'] = '评论成功'
                else:
                    back_dic['code'] = 1001
                    back_dic['msg'] = '请<a href=/userapp/login/>登录</a>'
    
                return JsonResponse(back_dic)
    ```

* 前端页面
    ```django
    {# 评论楼 #}
    <ul class="list-group">
    <li class="list-group-item">
    {% for comment in comment_list %}
        <span>#{{ forloop.counter }}</span>
        <span>{{ comment.comment_time|date:'Y-m-d h:M:S' }}</span>
        <span>{{ comment.user.username }}</span>
        <span class="pull-right"><a class="reply" username="{{ comment.user.username }}" comment_id="{{ comment.pk }}">回复</a></span>
        <div>
        <!--判断当前评论是否是子评论-->
            {% if comment.parent_id %}
                <p>@{{ comment.parent.user.username }}</p>
            {% endif %}
                <p>{{ comment.content }}</p>
        </div>
    {% endfor %}
    </li>
    </ul>
    ```
* 前端事件
    ```js
    // 用户点击提交评论（根评论）
    var parentPk = null;  // 用于表示该评论是子评论
    $("#id_submit").click(function () {
        let content = $("#id_comment").val()
        // 判断，如果是子评论，去掉@username
        if (parentPk) {
            let indexNo = content.indexOf('\n')+1
            content = content.slice(indexNo)  // 将indexNo将之前的数据切除，保留后面的内容
        }
    
    
        $.ajax({
            url: '/comment/',
            type: 'post',
            data: {
                'article_id': '{{ article.pk }}',
                'content': content,
                'parent_id': parentPk,  // 如果没有值，也不会影响后端
            },
            success: function (args) {
                if (args.code === 1000) {
                    $("#error_comment").text(args.msg);
                    // 清空评论框内容
                    $("#id_comment").val('');
                    // 临时渲染评论
                    let userName = '{{ request.user.username }}';
                    let tmp = `
                    <li class="list-group-item">
                    <span>${userName}</span>
                    <span class="pull-right"><a href="#">回复</a></span>
                    <div>
                    ${content}
                    </div>
                    </li>
                    `;
                    $(".list-group").append(tmp);
                    parentPk=null;
                }
            }
    
        })
    
    })
    
    // 给回复按钮绑定点击事件（子评论）
    $(".reply").click(function () {
        // 获取评论的评论人的姓名。评论的主键值（给回复按钮添加评论姓名，评论主键值属性）
        let commentUsername = $(this).attr('username')
        parentPk = $(this).attr('comment_id')  // 设置为全局的parentPK
        // 拼接 @ + commentUsername
        $("#id_comment").val("@"+commentUsername + '\n').focus()
    
    })
    ```

## 2.11 后台管理
* 使用`kindeditor`作为文章的编辑器
* 对于文章简介，需要去除标签，在进行简介截取
    1. 正则匹配文本内容

* `XSS`攻击:针对用户可以直接书写的`script`标签，通常需要处理。
    * 解决方式（使用`bs4`模块处理）
        1. 注释`script标签内的内容
        2. 删除`script标签
    












