

# 一、创建Django项目
## 1.1 创建Django项目的虚拟环境
```shell
mkvirtualenv django_env -p python3
workon django_env  # 进入虚拟环境
```
## 1.2 安装Django
推荐使用`1.x`版本的`Django`
```shell
pip install django==1.11.11   # 安装Django
```
## 1.3 创建项目
```shell
django-admin startproject 项目名称
```
```
项目文件夹
    项目文件夹同名的文件夹
        __init__.py
        settings.py
        urls.py  # 存放路由与视图函数的对应关系
        wsgi.py
    manage.py
```
## 1.3 启动项目
```shell
cd 项目文件夹
python manage.py runserver  # 启动项目
```
## 1.4 创建应用(功能)
应用: Django是用来开发`app`(功能)的`web`框架

不同的`app`对应不同的功能: 一个`app`就是一个独立的功能模块

```shell
python manage.py startapp app_name  # app_name注意见名知义
```
> 会在项目目录下新建一个文件夹，命名为`app_name`, `app_name`下的文件结构如下
![输入图片说明](https://images.gitee.com/uploads/images/2020/1207/231749_56b17718_7841459.png "屏幕截图.png")


## 1.5 主要文件及文件夹介绍
```
-- DjangoLearn 项目文件夹
    -- DjangoLearn 文件夹
        -- settings.py 配置文件
        -- urls.py  路由与视图函数对应的关系(路由层)
        -- wsgi.py
    -- manage.py  Django的启动文件
    -- db.sqlite3  Django自带的sqlite3数据库
    -- app_name 文件夹
        -- admin.py  Django后台管理
        -- apps.py  注册使用
        -- migrations 文件夹  所有的数据库迁移记录
        -- models.py 数据库相关的模型类(orm)
        -- tests.py 测试文件
        -- views.py 视图函数(视图层)
```

## 1.6 使用pycharm启动
直接使用python打开创建的已经创建好的项目。pycharm会自动添加好启动参数。

* **第一步**
![](https://images.gitee.com/uploads/images/2020/1207/233949_5c0a279f_7841459.png "屏幕截图.png")
* **第二步**
![](https://images.gitee.com/uploads/images/2020/1207/234214_ec42a00e_7841459.png "屏幕截图.png")
* **第三步**
![](https://images.gitee.com/uploads/images/2020/1207/234249_b8871761_7841459.png "屏幕截图.png")


# 二、使用pycharm自动创建Django项目
![](https://images.gitee.com/uploads/images/2020/1207/234422_56bef2d6_7841459.png "屏幕截图.png")
> 1. 会自动创建`templates`文件夹, 且在配置文件中添加对应的`templates`路径






