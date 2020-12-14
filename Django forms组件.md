# 一、Forms组件介绍
## 1.1 实现一个注册功能
要求:
1. 获取用户名和密码，利用form表单提交数据
2. 在后端判断用户名和密码是否符合一下条件
    * 用户名中不能含有敏感字符
    * 密码不能少于6位
3. 在前端展示提示信息

开发网站过程中，不可避免的会涉及到数据格式校验，现在初窥校验流程。

* 后端校验逻辑
    ```python
    def register(request):
        back_dic = {"username": '', "password": ""}
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if 'jpm' in username:
                back_dic["username"] = "不符合要求"
            if len(password) < 6:
                back_dic["password"] = "长度不足"
    
        return render(request, 'register.html', locals())
    ```
    * 将所有的校验逻辑放在后端完成。
    * 将校验完成后的信息传递到前端页面进行渲染
* 前端展示
    ```django
    <form action="" method="post">
            <p>
                <label for="username">username</label>
                <input type="text" id="username" name="username" class="form-control">
                <span style="color: red">{{ back_dic.username }}</span>
            </p>
            <p>
                <label for="password">password</label>
                <input type="password" id="password" name="password" class="form-control">
                <span style="color: red">{{ back_dic.password }}</span>
            </p>
            <input type="submit" class="btn btn-block btn-primary" value="注册">
        </form>
    ```
    * 如果数据不符合要求，在前端展示提示信息

这些逻辑自己实现要求的代码复杂，Django提供了`form`组件用于完成以上所有操作：
1. 校验数据是否符合要求
2. 渲染html文件
3. 展示提示信息

**为什么后端必须要有数据校验** ？
1. 前端的js校验数据是不安全的，可以直接修改前端校验代码和校验后的数据
2. 也可以通过爬虫程序发送请求绕过前端的数据校验


# 二、Django forms组件简单使用
在使用`form`组件时必须要定义一个类，并继承`Form`类
```python
from django import forms  # 导入这个组件

class MyForm(forms.Form):
    pass
```

## 2.1  forms组件校验数据
也是以注册为例
1. 首先要写一个类，里面写上每个数据的校验规则
    ```python
    class RegForm(forms.Form):
        """
        校验用户注册时的信息
        """
        username = forms.CharField(min_length=4, max_length=8)  # username最多8位最低4位
        password = forms.CharField(min_length=6, max_length=18)  # password最低6位最高18位
    ```
2. 使用自定义form类实例化一个对象, 实例化时，传入一个字段，里面保存待校验数据的键值对
    ```python
    form_obj = views.RegForm({"username": 'dyp', "password": '123456'})
    ```
3. **校验数据的常用方法**
    * 判断数据是否合法
        ```python
        form_obj.is_valid()  # False 判断数据是否符合数据要求，只有说有的数据完全合法才会返回True
        ```
    * 查看校验通过数据
        ```python
        form_obj.cleaned_data  # 保存所有校验通过的数据
        {'password': '123456'}
        ```
    * 查看校验失败的数据的失败原因
        ```python
        form_obj.errors  # 校验失败的字段，与失败原因组成的键值对
        {'username': ['Ensure this value has at least 4 characters (it has 3).']}
        ``` 
        * 可能触犯多个规则

4. 校验规则
    * 第一步、获取类中规则的字段名
    * 第二步、在传入的字典中获取对应字段的数据
    * 第三步、判断数据是否符合规则
        * 如果符合规则，将数据放回到`cleaned_data`字典中
        * 如果不符合规则，将字段和错误信息组织成键值对放到`error`字典中
    * 第四步、如果类中的字段属性完全校验完成后，无论传入的字典中是否还有其他数据，都不会在进行校验
    * **默认情况下，所有字段必须要传值** 

**默认条件下，校验数据，数据可以多传，不能少传**


## 2.2 forms组件渲染模板
* 第一步、将自定义的`form`类实例化一个空对象
* 第二步、将实例化的空对象传递给前端模板
* **`forms`渲染模板只会渲染一些输入控件** 
```python
def register(request):
    # 先生成一个空对象
    reg_form = RegForm()
    # 直接将空对象传递给html页面
    return render(request, 'register.html', locals())
```

### 2.2.1 第一种渲染方式，完整渲染
```django
<form action="" method="post">
    <h1>第一种渲染方法</h1>
    {{ reg_form.as_p }}
    {{ reg_form.as_ul }}
    {{ reg_form.as_table }}
</form>
```
> 1. `as_p`: 以`p`标签包裹
![](https://images.gitee.com/uploads/images/2020/1214/132037_4d2c6c3a_7841459.png "屏幕截图.png")
> 2. `as_ul`: 以`ul li`标签包裹
![](https://images.gitee.com/uploads/images/2020/1214/132106_ad78bb67_7841459.png "屏幕截图.png")
> 3. `as_table`: 没有任何标签包裹 
![](https://images.gitee.com/uploads/images/2020/1214/132127_892e6cf7_7841459.png "屏幕截图.png")

* 直接渲染出完整的输入空间，及相关信息
* 封装程度太高，不便于后期扩展，一般只在本地测试时使用

### 2.2.2 第二种渲染方式，分开渲染
为了解决第一种方式耦合性太高的问题，可以将标签分开渲染
```django
<form action="" method="post">
    <h1>第二种渲染方式</h1>
    <p>
        <label for="">
        {{ reg_form.username.label }} {# 渲染提示信息 #}
        {{ reg_form.username }}  {# 渲染输入控件 #}
        </label>
    </p>
    <p>
        <label for="">
        {{ reg_form.password.label|safe }} {# 渲染提示信息 #}
        {{ reg_form.password }}  {# 渲染输入控件 #}
        </label>
    </p>
</form>
```
>  **这个方法解决了耦合性高的问题，但是，当字段太多时，需要书写过多的代码。一般情况不适用** 

### 2.2.3 第三种渲染方式，for循环
`form`对象支持循环遍历，遍历出来的时对象的字段，可以直接渲染成输入控件
```django
<form action="" method="post">
    <h1>第三种渲染方式</h1>
    {% for form in reg_form %}
        <p>
            <label for="">
                {{ form.label|safe }}: {{ form }}
            </label>
        </p>
    {% endfor %}
</form>
```
> 1. 解决字段多时，书写代码较多的问题，也有很强的扩展性
> 2. `label`书写默认展示的时字段名首字母的大写形式，可以使用字段修改`label`属性
>     ```python
>      password = forms.CharField(min_length=6, max_length=18, label='密&emsp;码')
>     ```

## 2.3 展示提示信息
标签渲染好后，默认在前端有一次校验。可以修改代码让其不做校验(在form标签添加`novalidate`属性)

**后端**
```python
def register(request):
    # 先生成一个空对象
    reg_form = RegForm()
    # 直接将空对象传递给html页面
    if request.method == 'POST':
        # 获取用户数据并校验
        """
        1. 字段较多的情况，数据获取繁琐
        2. 校验数据需要构造字典
        3. 但是request.POST可以看成字典
        """
        reg_form = RegForm(request.POST)  # 校验数据
        # 判断数据是否合法
        if reg_form.is_valid():
            # 合法，操作数据库，存储数据
            return HttpResponse('OK')
    return render(request, 'register.html', locals())
```
> 当有请求触发注册视图函数时，视图函数的逻辑
> * 先生成一个空`forms`组件对象，判断请求方式是否为`POST`请求
>     1. 如果不是，直接将空的`forms`对象传递给模板渲染出，注册页面
>     2. 如果是，获取用户的输入数据。（**request.POST保存用户通过POST请求提交的数据，可以看作是字典**。）新建一个`forms`对象，用于校验数据是否正确，然后将这个对象保存到空`forms`对象的变量名中
> * 判断校验数据是否合法
>     1. 合法，操作数据库保存数据
>     2. 不合法，在前端展示错误信息。（错误信息是以列表信息保存）

**在前端**
```django
<span style="color: red">{{ form.errors.0 }}</span>
```
> 1. 针对错误信息，可以使用字段参数`error_messages={'min_length': 'message',...}`指定不满足规则时的报错信息

# 三、`forms`组件的`hook`函数
`hook`(钩子)函数：在特点的节点触发完成响应操作

`forms`组件提供了 _局部钩子_ 和 _全局钩子_ 函数
1. 局部钩子，给单个字段增加校验规则。（自定义校验规则）
2. 全局钩子，给多个字段增加校验规则。

**案例**: 校验用户名中不能含有666, 和 校验密码与确认密码是否一致
```python
class RegForm(forms.Form):
    """
    校验用户注册时的信息
    """
    username = forms.CharField(min_length=4,
                               max_length=8,
                               label='用户名',
                               error_messages={
                                   'min_length': '用户名最少四位',
                                   'max_length': '用户名最多8位',
                                   'required': '用户名不能为空'
                               })  # username最多8位最低4位
    password = forms.CharField(min_length=6,
                               max_length=18,
                               label='密&emsp;码',
                               error_messages={
                                   'min_length': '密码最少6位',
                                   'max_length': '密码最多18位',
                                   'required': '密码不能为空'
                               }
                               )  # password最低6位最高18位
    confirm_password = forms.CharField(min_length=6,
                                       max_length=18,
                                       label='确认密码',
                                       error_messages={
                                           'min_length': '密码最少6位',
                                           'max_length': '密码最多18位',
                                           'required': '密码不能为空'
                                       }
                                       )

    # 局部钩子函数
    def clean_username(self):
        """
        通过第一次校验，后触发
        :return:
        """
        username = self.cleaned_data.get('username')  # 通过校验后的数据放在在cleaned_data里面
        if '666' in username:
            # 添加错误信息
            self.add_error('username', '数据包含敏感信息')  # 添加错误信息
        # 将钩子函数获取的数据放回去
        return username

    # 全局钩子函数
    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if not password == confirm_password:
            # 添加错误信息
            self.add_error('confirm_password', '两次密码不一致')
        # 将钩子函数获取的数据放回去, 全局钩子将所有的数据全都获取了
        return self.cleaned_data
```
> 1. 在自定义的`forms`类中，定义钩子函数。
> 2. **钩子函数将数据拿出来，原来的位置就没有数据了** 。校验完成后，要将数据返回回去

# 四、forms组件字段常见参数

1. `label`: 字段名字

2. `error_messages`: 自定义报错信息

3. `initial`: 默认值，默认在输入控件中展示的内容

4. `required`: 默认为`True`：必传，控制字段在校验时是否必须传入。`False`: 非必传

5. `widget`: 控制`input`的属性
    * `type=text`: `widget=forms.widgets.TextInput(attrs={'class': 'form-control'})`
        * `attrs`: 控制标签的属性，`属性名:属性值` 键值对的字典,多个属性值，空格隔开
    * `type=password`: `widget=forms.widgets.PasswordInput(attrs={attr={'class': 'form-control'}})`
        * `attrs`: 控制标签的属性，`属性名:属性值` 键值对的字典

6. `validators`: 额外校验器
    * 先导正则校验器
        ```python
        from django.core.validators import RegexValidator
        ```
    * 指定校验正则规则
        ```python
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^159[0-9]+$', '数字必须以159开头')]
        ```
    * `validators`是一个列表，保存正则校验器对象

# 五、其他字段类型渲染
## 5.1 选择字段`ChoiceField`
1. 单选按钮`radioSelect`
    ```python
    gender = forms.fields.ChoiceField(
            choices=((1, "男"), (2, "女"), (3, "保密")),
            label="性别",
            initial=3,
            widget=forms.widgets.RadioSelect()
        )
    ```
2. 单选下拉框`Select`
    ```python
    hobby = forms.ChoiceField(
            choices=((1, "篮球"), (2, "足球"), (3, "双色球"), ),
            label="爱好",
            initial=3,
            widget=forms.widgets.Select()
        )
    ```
3. 多选下拉框`Select`
    ```python
    hobby = forms.MultipleChoiceField(
            choices=((1, "篮球"), (2, "足球"), (3, "双色球"), ),
            label="爱好",
            initial=[1, 3],
            widget=forms.widgets.SelectMultiple()
        )
    ```
4. 单选`Checkbox`
    ```python
    keep = forms.ChoiceField(
            label="是否记住密码",
            initial="checked",
            widget=forms.widgets.CheckboxInput()
        )
    ```
5. 多选`checkbox`
    ```python
    hobby = forms.MultipleChoiceField(
            choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
            label="爱好",
            initial=[1, 3],
            widget=forms.widgets.CheckboxSelectMultiple()
        )
    ```

## 5.2 Django forms组件内置字段
1. `Field`：所有字段的基类, 参数解释
   
    |参数|含义|
    |:---:|:---:|
    |`required=True`|是否允许为空|
    |`widget=None`|HTML插件|
    |`label=None`|用于生成Label标签或显示内容|
    |`initial=None`|初始值|
    |`help_text=''`|帮助信息(在标签旁边显示)|
    |`error_messages=None`|错误信息`{'required': '不能为空','invalid': '格式错误'}`|
    |`validators=[]`|自定义验证规则|
    |`localize=False`|是否支持本地化|
    |`disabled=False`|是否可以编辑|
    |`label_suffix=None`| Label内容后缀|

2. `CharField(Field)`: 字符串
    
    |参数|含义|
    |:---:|:---:|
    |`max_length=None`|最大长度|    
    |`min_length=None`|最小长度|
    |`strip=True`|是否移除用户输入空白|

3. `IntegerField(Field)`: 整数

    |参数|含义|
    |:---:|:---:|
    |`max_value=None`|最大值|
    |`min_value=None`|最小值|

4. `FloatField(IntegerField)`: 小数

5. `DecimalField(IntegerField)`: 小数

    |参数|含义|
    |:---:|:---:|
    |`max_value=None`|最大值|
    |`min_value=None`|最小值|
    |`max_digits=None`|总长度|
    |`decimal_places=None`|小数位长度|

6. `BaseTemporalField(Field)`: 时间类型的基类

    |参数|含义|    
    |`input_formats=None`|时间格式|
    
7. `DateField(BaseTemporalField)`: 格式：2015-09-01
8. `TimeField(BaseTemporalField)`: 格式：11:12
9. `DateTimeField(BaseTemporalField)`: 格式：2015-09-01 11:12

10. `DurationField(Field)`: 时间间隔：%d %H:%M:%S.%f

11. `RegexField(CharField)`: 正则字符串

    |参数|含义|
    |:---:|:---:|
    |regex|自定制正则表达式|
    |max_length=None|最大长度|
    |min_length=None|最小长度|

12. `EmailField(CharField)`: 邮箱格式

13. `FileField(Field)`: 文件字段
    
    |参数|含义|
    |:---:|:---:|
    |allow_empty_file=False|是否允许空文件|

14. `ImageField(FileField)`: 图片处理字段
    * 注：需要PIL模块，`pip3 install Pillow`
    * 以上两个字典使用时，需要注意两点：
        * `form`表单中 `enctype="multipart/form-data"`
        * `view`函数中 `obj = MyForm(request.POST, request.FILES)`

15. `URLField(Field)`：url校验


16. `BooleanField(Field)` 
 
17. `NullBooleanField(BooleanField)`
 
18. `ChoiceField(Field)`
    * choices=(),                选项，如：choices = ((0,'上海'),(1,'北京'),)
    * required=True,             是否必填
    * widget=None,               插件，默认select插件
    * label=None,                Label内容
    * initial=None,              初始值
    * help_text='',              帮助提示
 
 
19. `ModelChoiceField(ChoiceField)`
    * `django.forms.models.ModelChoiceField`
    * `queryset`                 查询数据库中的数据
    * `empty_label="---------"`  默认空显示内容
    * `to_field_name=None`       HTML中value的值对应的字段
    * `limit_choices_to=None`    ModelForm中对queryset二次筛选
     
20 `ModelMultipleChoiceField(ModelChoiceField)`
    * django.forms.models.ModelMultipleChoiceField
 
 
21. `TypedChoiceField(ChoiceField)`
    * `coerce = lambda val: val`   对选中的值进行一次转换
    * `empty_value= ''`            空值的默认值
 
22. `MultipleChoiceField(ChoiceField)`

23. `TypedMultipleChoiceField(MultipleChoiceField)`
    * `coerce = lambda val: val `  对选中的每一个值进行一次转换
    * `empty_value= ''`            空值的默认值
 
24. `ComboField(Field)`
    * `fields=()`使用多个验证
    * 如下：即验证最大长度20，又验证邮箱格式
        * `fields.ComboField(fields=[fields.CharField(max_length=20), fields.EmailField(),])`
 
25. `MultiValueField(Field)`
    * PS: 抽象类，子类中可以实现聚合多个字典去匹配一个值，要配合MultiWidget使用
 
26. `SplitDateTimeField(MultiValueField)`
    * `input_date_formats=None`  格式列表：['%Y--%m--%d', '%m%d/%Y', '%m/%d/%y']
    * `input_time_formats=None`  格式列表：['%H:%M:%S', '%H:%M:%S.%f', '%H:%M']
 
27. `FilePathField(ChoiceField)`: 文件选项，目录下文件显示在页面中
    * `path`                   文件夹路径
    * `match=None`             正则匹配
    * `recursive=False`        递归下面的文件夹
    * `allow_files=True`       允许文件
    * `allow_folders=False     允许文件夹
 
28. `GenericIPAddressField`
    * `protocol='both'`      both,ipv4,ipv6支持的IP格式
    * `unpack_ipv4=False `   解析ipv4地址，如果是::ffff:192.0.2.1时候，可解析为192.0.2.1， 
    * PS：protocol必须为both才能启用
 
29. `SlugField(CharField)`: 数字，字母，下划线，减号（连字符）
 
30. `UUIDField(CharField)`: uuid类型


