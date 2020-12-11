# 一、测试脚本准备
在`app_name/test.py`文件下添加如下代码
```python
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoLearn.settings")
    import django
    django.setup()
```

# 二、单表数据的增删改查
表准备
```python
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    register_time = models.DateTimeField()
    # auto_now: 每次操作数据的时候，会自动更新当前时间
    # auto_now_add: 创建数据时，会自动将当前时间记录，如果不修改数据，就不会发生改变

    def __str__(self):
        """
        当对象被输出时，改为正常输出
        :return:
        """
        return "User(id={}, name={}, age={}, register_time={})".format(self.id, self.name, self.age, self.register_time)
```
> 对于时间日期字段(`DateField`，`DateTimeField`), 用两个非常总要的参数
> 1. auto_now: 记录每次操作数据的时间
> 2. auto_now_add: 记录数据创建或修改的时间

## 2.1 增加数据的两种方式
1. 调用`objects`的`create`方法增加数据，该方法会直接将数据写入数据库，并返回创建的数据对象.
    ````python
    res = models.User.objects.create(name="dyp", age=22, register_time="2020-01-21")
    ```
2. 创建空数据对象，然后调用数据对象的`save`方法保存到数据库
    ```python
    user = models.User()
    user.name = 'dyy'
    user.age = 12
    user.register_time = datetime.now()  # 可以传入日期格式字符串或日期对象
    user.save()  # 保存到数据库
    ```

## 2.2 查询数据
1. 查询全部数据，调用`objects`的`all`方法返回表中的全部数据
    ```python
    res = models.User.objects.all()
    res[index]  # 通过索引获取数据对象
    ```
    * 返回值是这些数据封装成的`QuerySet`对象，这个对象类似与列表，可以进行索引取值
    * 索引取值 **不支持负数索引** 
2. 条件查询，调用`objects`的`filter`方法，在`filter`方法中添加条件就可以查询出满足条件的数据，也是返回`queryset`对象
    ```python
    res = models.User.objects.filter(条件)
    ```
3. 获取数据对象，调用`objects`的`get`方法，在`get`方法中指定条件，可以直接获取到满足条件的数据对象
    ```python
    user = models.User.objects.get(pk=4)
    ```
    * `pk`: 指代表的主键

## 2.3 修改数据
1. 调用`queryset`对象的`update`方法修改数据
    ```python
    models.User.objects.filter(条件).update(field_1=value, field_2=value, ...)
    ```
    * 数据修改是批量修改的，而且只修改指定的字段数据
    
2. 获取数据对象然后修改属性值在调用其`save`方法修改数据
    ```python
    user = models.User.objects.get(id=4)
    user.age = 20
    user.save()
    ```
## 2.4 删除数据
1. 调用`queryset`对象的`delete`方法删除数据
    ```python
    res = models.User.objects.filter(pk=2)
    line = res.delete()  # 删除, 返回删除数据的行数
    ```
    * `queryset`对象`delete`方法会批量删除数据

## 2.5 常用的查询方法
> **model_name: 模型类名**

1. all()
    * `model_name.objects.all()`， 返回所用数据构成的`queryset`对象

2. filter(条件)
    * `model_name.objects.filter(条件)`，返回满足条件的数据构成的`queryset`对象
    * 多条件默认以`and`链接

3. get(条件)
    * `model_name.objects.get(key=value)`，返回满足条件的数据对象
    * 条件不满足报错

4. exclude(条件)
    * 排除满足条件的数据

5. first()
    * `queryset.first()`, 返回queryset对象中第一条数据

6. last()
    * `queryset.last()`, 返回queryset对象中最后一条数据

7. values(*fields)
    * `model_name.objects.values(*fields)`, 自定字段获取值
    * 返回`queryset`对象，元素视为字典

8. values_list()
    * `model_name.objects.values_list(*fields)
    * 返回`queryset`对象，元素视为元组

9. distinct()
    * 去重，不要忽略主键的影响，有主键的数据不能进行去重

10. order_by(field)
    * 指定字段排序
    * 默认升序，降序需要在字段前添加负号`"-age"`

11. reverse()
    * 反转，前提是数据已经排序过
    * 没有排序过的数据不支持反转

12. count()
    * 统计数据条目

13. exists()
    * 判断是否存在，返回bool值

## 2.6 条件查询
1. `filter(field=value)`: 字段`field`等于`value`

2. `filter(field__gt=value)`: 字段`field`大于`value`, 注意是双下划线(`__`)

3. `filter(field__gte=value)`: 字段`field`大于或等于`value`

4. `filter(field__lt=value)`: 字段`field`小于`value`

5. `filter(field__lte=value)`: 字段`field`小于或等于`value`

6. `filter(field__in=value)`: value是可迭代对象，指定值查询

7. `filter(field__range=(value1, value2))`: 返回查询，在value1和value2之间的数据. 首尾都要

8. `filter(field__contains=value)`: 字段值包含`value`的数据(模糊查询)
    * 区分大小写
    * 忽略大小写`field_icontains`

9. `filter(field_startswith=value)`: 字段以`value`开头
    * `field_endswith`: 字段以`value`结尾

10. `filter(field__month=value)`: 月份为`value`的数据
    * `field__year=value`: 年份为`value`的数据

```python
# 单表的数据操作
    from app01 import models
    res = models.User.objects.create(name="小兰", age=20, register_time='2002-03-22')  # 增加数据
    print(res)  # User(id=6, name=小兰, age=20, register_time=2002-03-22)

    res = models.User.objects.all()  # 查询出所有数据
    print(res)
    res = models.User.objects.first()  # 查询出表中的第一条数据，返回数据对象
    print(res)
    res = models.User.objects.last()  # 查询出表中的最后一条数据
    print(res)
    res = models.User.objects.filter(pk=5)  # 查询出主键值等于5的数据
    print(res)
    res = models.User.objects.get(pk=6)  # 获取主键值为6的数据
    print(res)
    res = models.User.objects.exclude(pk=6)  # 排除主键值为6的数据
    print(res)
    res = models.User.objects.filter(id=4).values("name", "age")  # 获取id=4的name和age值
    print(res)
    res = models.User.objects.values('name', 'age', 'register_time').distinct()  # 去重
    print(res)
    res = models.User.objects.values('name', 'age').order_by('age')  # 排序
    print(res)
    res = models.User.objects.filter(age__lt=22)  # 小于
    print(res)
    res = models.User.objects.filter(age__gt=22)  # 大于
    print(res)
    res = models.User.objects.filter(age__in=(18, 19))  # 指定值查询
    print(res)
    res = models.User.objects.filter(age__range=(18, 22))  # 查询18--22之间的数据
    print(res)
    res = models.User.objects.filter(name__contains='d')
    print(res)
    res = models.User.objects.filter(register_time__month='03')
    print(res)
```

# 三、多表操作
表准备
```python
# 图书管理系统表
class Book(models.Model):
    """
    图书表
    """
    title = models.CharField(max_length=32, verbose_name='书名')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="价格")  # 总共8位，小数占2位
    publish_date = models.DateField(auto_now_add=True)

    # 一部图书只能由一个出版社出版，但是出版社可以出版多部图书，出版社与图书是一对多关系
    publish = models.ForeignKey(to="Publish")  # 外键约束，一对多
    # 一部图书可以由多个作者编著，一个作者也可以编著多半图书，图书与作者是多对多关系
    authors = models.ManyToManyField(to="Author")  # 虚拟字段，主要是用来使orm自动创建第三张关系表


class Publish(models.Model):
    """
    出版社表
    """
    name = models.CharField(max_length=32, verbose_name='出版社名')
    addr = models.CharField(max_length=108, verbose_name='出版社地址')
    email = models.EmailField()  # 限制为邮箱格式


class Author(models.Model):
    """
    作者表
    """
    name = models.CharField(max_length=20, verbose_name='作者名')
    age = models.IntegerField(verbose_name='年龄')
    # 作者与作者详情是一对一关系
    author_detail = models.OneToOneField(to="AuthorDetail")  # 建立一对一外键关系


class AuthorDetail(models.Model):
    """
    作者详情表
    """
    phone = models.CharField(max_length=12, verbose_name='电话号码')
    addr = models.CharField(max_length=108, verbose_name='地址')
```

## 3.1 一对多关系的增删改查
### 3.1.1 增加数据的两种方式
1. 使用表(`Book`)中的真实外键字段(`publish_id`)，直接存放其被关联表(`Publish`)中的被关联字段(`id`)的值，创建数据
    ```python
    models.Book.objects.create(title='三国演义', price=123.2, publish_id=1)
    ```
    * `publish_id`: 表中的真实外键字段
2. 使用模型(`Book`)中的外键属性字段(`publish`)，存放被关联表(`Publish`)的数据对象
    ```python
    publish_obj = models.Publish.objects.filter(pk=2).first()
    models.Book.objects.create(title='水浒传', price=125.4, publish=publish_obj)
    ```
    * `publish`: 创建时指定的外键属性字段

### 3.1.2 删除数据
如果删除被关联表(`Publish`)中的数据，关联表(`Book`)中的数据也会一并删除. (`Django 1.x`  **默认为级联删除的** )
```python
models.Publish.objects.filter(pk=1).delete()
```

### 3.1.3 更新数据的两种方式
1. 使用表(`book`)中的真实外键字段(`publish_id`), 直接存放其被关联表(`Publish`)中的被关联字段(`id`)的值, 更新数据
    ```python
    models.Book.objects.filter(pk=1).update(publish_id=2)
    ```
2. 使用模型(`Book`)中的外键属性字段(`publish`)，存放被关联表(`Publish`)的数据对象
    ```python
    publish_obj = models.Publish.objects.filter(pk=1).first()
    models.Book.objects.filter(pk=1).update(publish=publish_obj)    
    ```

## 3.2 多对多关系的增删改查
&emsp;&emsp;&emsp;&emsp;多对多关系数据的操作实际是操作中间表，但是我们是采用的自动生成中间表，所以不能直接使用模型进行操作。<br>
&emsp;&emsp;&emsp;&emsp;要先查找出创建多对多关系的数据对象，然后获取其虚拟字段，这样就获得了中间表。就可以向中间表添加删除修改数据

### 3.2.1 增加数据(`add`方法)
* 第一步、查询数据关联表(`Book`)的数据对象
    ```python
    book = models.Book.objects.filter(pk=1).first()
    ```
    * 查询出主键值为1的书籍

* 第二步、中间表插入数据
    * 方式一，直接添加被关联表(`Author`)的被关联字段(`id`)
        ```python
        book.authors.add(1)  # 给主键值为1的书籍添加主键为1的作者
        book.authors.add(2, 3)  # 给主键值为1的书籍添加主键为2和3的作者
        ```
    * 方式二、添加被关联表(`Author`)的数据对象
        ```python
        book = models.Book.objects.filter(pk=2).first()
        author_1 = models.Author.objects.filter(pk=1).first()
        book.authors.add(author_1)
        ```

### 3.2.2 删除数据(`remove`)
* 第一步、查询数据关联表(`Book`)的数据对象
    ```python
    book = models.Book.objects.filter(pk=1).first()
    ```
    * 查询出主键值为1的书籍
* 第二步、删除中间表的数据
    * 方式一
        ```python
        book = models.Book.objects.filter(pk=1).first()
        book.authors.remove(2)  # 删除中间表(主键值为1的书籍，主键值为2的作者)
        book.authors.remove(1, 3)
        ```
    * 方式二
        ```python
        author_1 = models.Author.objects.filter(pk=1).first()
        book = models.Book.objects.filter(pk=2).first()
        book.authors.remove(author_1)
        ```

### 3.2.3 修改数据(`set`)
* 第一步、查询数据关联表(`Book`)的数据对象
    ```python
    book = models.Book.objects.filter(pk=1).first()
    ```
    * 查询出主键值为1的书籍
* 第二步、修改数据，先删除，在添加；修改的数据已经存在则忽略，不操作
    ```python
    # 修改数据
    # 方式一
    book = models.Book.objects.filter(pk=1).first()
    book.authors.set([1, 2])  # 将book.id=1的作者修改author.id=1,2; 流程是先删除在添加. 如果已经存在则不发生变化
    # 方式二
    author = models.Author.objects.filter(pk=3).first()
    book.authors.set([author])
    ```
### 3.2.4 清空中间表中某个绑定关系(`clear`)
```python
book = models.Book.objects.filter(pk=1).first()
book.authors.clear()
```
> 清空主键为1书籍的所用作者绑定关系



# 四、多表查询
## 4.1 正向与反向查询概念
正向查询: 从外键字段所在的表，查询其外键字段关联表中的数据称为正向查询

反向查询: 从被关联表，查询与外键字段所在表的数据称为反向查询

## 4.2 子查询(基于对象的跨表查询)
1. 查询书籍主键为1的出版社名称(一对多)
    * 通过书籍表查询出版社表，外键字段在书籍表中，是正向查询
    * 正向查询通过字段，查询数据
    ```python
    book = models.Book.objects.filter(pk=1).first()
    res = book.publish
    print(res.name)
    print(res.addr)
    ```

2. 查询书籍主键为1的作者(多对多)
    * 通过书籍表查询作者表，外键字段在书籍表中，正向查询
    ```python
    book = models.Book.objects.filter(pk=1).first()
    res = book.authors
    print(res.all())
    ```
    * 当查询结果有多个值时，使用`all`方法将书籍查询出来

3. 查询作者dyp的电话号码和地址(一对一)
    * 通过作者表查询作者详情表，外键字段在作者表中，正向查询
    ```python
    author = models.Author.objects.filter(name='dyp').first()
    res = author.author_detail
    print(res.phone)
    print(res.addr)
    ```

4. 查询出版社是东方出版社出版的书籍(一对多)
    * 通过出版社表查询书籍表，外键字段在书籍表中，反向查询
    * 反向查询通过 **`表名小写_set` 或`表名小写`** 查询数据
    ```python
    publish = models.Publish.objects.filter(name="东方出版社").first()
    res = publish.book_set
    print(res.all())
    ```

5. 查询作者是`dyy`写的书籍(多对多)
    * 通过作者查询书籍，外键在书籍表中， 反向查询
    ```python
    author = models.Author.objects.filter(name="dyy").first()
    res = author.book_set
    print(res.all())
    ```

6. 查询手机号码为122的作者姓名(一对一)
    * 通过作者详情表查询作者，外键在作者表中，反向查询
    ```python
    author_detail = models.AuthorDetail.objects.filter(phone="122").first()
    res = author_detail.author
    print(res)
    ```

**正向查询与反向查询注意**
1. 正向查询时，通过 _数据对象.属性名_ 查询被关联表中的数据
    * 如果数据有多条时，使用all()方法才能获得数据
    * 如果数据只有一条，直接获得数据对象

2. 反向查询，通过 `数据对象.表名小写`或`数据对象.表名小写_set` 查外键所在表的数据
    * 如果数据有多条，使用 `数据对象.表名小写_set.all()`查询外键所在表的数据，获取到`queryset`对象
    * 如果数据只有一条，使用`数据对象.表名小写`查询外键所咋的数据，直接获取到数据对象    

3. 正向查询基于属性，反向查询基于表名小写

## 4.3 基于双下划线跨表查询(连接查询)
1. 查询姓名`dyy`的手机号码
    ```python
    res = models.Author.objects.filter(name="dyy").values("author_detail__phone")
    print(res.first())
    
    # 反向查询
    # res = models.AuthorDetail.objects.filter(author__name="dyy")  # 获取姓名为dyy的作者详情
    res = models.AuthorDetail.objects.filter(author__name="dyy").values("phone", 'author__name')
    print(res)
    ```

2. 查询书籍主键为1的出版社名称,书名和作者名
    ```python
    res = models.Book.objects.filter(pk=1).values("title", 'publish__name', "authors__name")
    print(res) 

    # 反向查询
    # res = models.Publish.objects.filter(book__pk=1)  # 获取出版过书籍主键为1的出版社
    res = models.Publish.objects.filter(book__pk=1).values("name", "book__title", "book__authors__name")
    print(res)   
    ```

3. 查询书籍主键为1的作者姓名
    ```python
    res = models.Book.objects.filter(pk=1).values("authors__name")
    print(res)

    # 反向查询
    # res = models.Author.objects.filter(book__pk=1)  # 获取写过书籍主键为1的作者
    res = models.Author.objects.filter(book__pk=1).values("name", "book__title")
    print(res)
    ```

4. 查询书籍主键为1的作者的姓名和手机号码
    ```python
    res = models.Book.objects.filter(pk=1).values("authors__name", "authors__author_detail__phone")
    print(res)
    ```



