# 一、Django链接mysql
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # 数据库引擎
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 数据库的库名
    }
}
```
> Django默认使用sqlite3

## 1.1 第一步，配置文件的修改
在`settings.py`文件中修改`DATABASES`为如下内容
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 使用的数据库
        'NAME': 'djangodb',  # 库名称
        'USER': 'root',  # 用户名
        'PASSWORD': 'dyp1996',  # 用户密码
        'HOST': '127.0.0.1',  # 数据库服务器所在的地址
        'PORT': 3306,  # 数据库服务器运行的端口
        'CHARSET': 'UTF8'  # 服务器采用编码
    }
}
```
## 1.2 第二步，代码声明
Django默认使用`mysqldb`引擎链接`mysql`, 修改引擎为`pymysql`链接数据库.

**在`project_root`目录下的`project_name/__init__.py`文件或者是任意`app_name/__init__.py`文件声明如下代码**
```python
import pymysql
pymysql.install_as_MySQLdb()
```

# 二、`orm`简介
`ORM` 全称 `Object Relational Mapping`对象关系映射,
通过使用 `ORM` 可以不用关心后台是使用的哪种数据库，只需要按照 `ORM` 所提供的语法规则去书写相应的代码， `ORM` 就会自动的转换成对应对应数据库的 `SQL` 语句

但是，`orm`框架的封装层度高，导致`sql`执行效率会降低。

**映射关系如下表**
|语言|数据库|
|:---:|:---:|
|类|表|
|对象|记录|
|对象属性|字段的值|


# 三、创建模型(类，创建表)
在`app_name/models.py`文件下创建类，也即是见表
```python
from django.db import models  # 首先导入
class User(models.Model):  # 继承父类
    id = models.AutoField(primary_key=True)  # id int primary key auto_increment
    username = models.CharField(max_length=32)  # username varchar(32)
    password = models.IntegerField()  # password int


class Author(models.Model):
    """
    由于每张表必须包含一个主键字段，如果没有定义主键字段，orm就会自动添加一个名为 id 的主键字段
    """
    username = models.CharField(max_length=32)  # username varchar(32)
    password = models.IntegerField()  # password int
```
> 如果主键字段没有特殊的命名要求，可以不用定义主键字段

**注意点**
> 1. `CharField`必须指定`max_length`参数，如果不指定会报错
> 2. `verborse_name`: 所有字段都有，用于解释字段作用

# 四、数据库迁移命令(****)
1. `python manage.py makemigrations`: 创建记录
2. `python manage.py migrate`: 操作同步到数据库服务器上

同步完成后生成如下表:
![](https://images.gitee.com/uploads/images/2020/1208/170655_5f85f4f4_7841459.png "屏幕截图.png")
> 1. 一个Django项目可能会有多个应用，可能会有表冲突
> 2. **只要修改了`models.py`中代码就必须执行这两条命令。**


