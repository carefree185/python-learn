# 一、视图
视图就是通过查询得到的一张虚拟表，然后保存下来，下次可以直接使用.

如果频繁的操作一张虚拟表，可以将其制作为视图。

**创建视图** 
```sql
create view 表名 as 虚拟表的查询sql语句

create view teacher2course as 
select teacher.tno, teacher.tname, teacher.tsex, teacher.tbirthday, teacher.prof, course.cno, course.cname from teacher INNER JOIN course 
on teacher.tno = course.tno;
```

**注意**
> 1. 创建视图只会在硬盘上保存表结构, 不会保存数据
> 2. 视图通常只用于查询; 不建议修改视图表中的数据, 可能会影响到真正的数据
> 3. 当创建视图过于多时, 导致表混乱，造成表的维护困难

# 二、触发器
在满足对表数据进行增、删、改的情况下，自动触发的功能

通常用于监控、日志...

**语法结构** 
```sql
create trigger 触发器的名字 before/after insert/update/delete 
on 表名

for each row

begin
    sql语句
end
```
> 1. 触发器自动触发的情形: 增加前后，删除前后、修改前后
> 2. 触发器的名字需要做到见名知义

**示例**
```sql
create trigger tri_before_insert_t1 before insert on t1 for each row
begin
    sql语句
end
```

> 补充:
>
> 1. 修改MySQL默认的语句结束符: `delimiter 结束符`; **只作用当前窗口**

**示例**
存在两张表`cmd`和`errlog`, 当`cmd`出现错误就在`errlog`添加数据
```sql
create table cmd 
(
    user char(32),
    priv char(32),
    cmd char(64),
    sub_time datetime,
    success enum("yes", "no")
);

create table errlog
(
    id int primary key auto_increment,
    err_cmd char(64),
    err_time datetime
);

-- 触发器
delimiter $$
create trigger tri_after_insert_cmd after insert on cmd
for each row
begin 
    if NEW.success = "no" then
        insert into errlog(err_cmd, err_time) values(NEW.cmd, NEW.sub_time);
    end if;
end$$
delimiter ;

-- 插入数据
insert into cmd
(user, priv, cmd, sub_time, success) 
values
("jason", "0755", "ls -l /etc", NOW(), "yes"),
("jason", "0755", "cat /etc/passwd", NOW(), "no"),
("jason", "0755", "useradd xxx", NOW(), "no"),
("jason", "0755", "ps aux", NOW(), "yes");
```
**删除触发器**
```
drop trigger 触发器的名字;
```

# 三、事务
开启一个事务，可以包含多条`sql`语句,  **要么同时成功，要么都不成功** , 事务 **原子性** 

保证对数据操作的安全性.


**事务特性(ACID)**
> A: 原子性, 一个事务时一个不可分隔的单位，事务中包含的操作 **要么同时成功要么同时失败** <br>
> C: 一致性, 事务必须是时数据库 _从一个一致性变到另一个一致性状态_ <br> 
> I: 隔离性, 一个事务的执行，不能被其他事务干扰 <br>
> D: 持久性, 一个事务一旦提交执行成功, 对数据库中的数据修改是永久的。之后的操作或故障不应该对其有影响 <br>

**事务语法** 
```sql
start transaction;  -- 开启事务
rollback;  -- 回滚(回退到事务执行之前的状态)
commit;  -- 提交事务(提交事务后不能在回滚)

-- 模拟转账

create table user
(
    id int primary key auto_increment,
    name char(16),
    balance int
);

insert into user(name, balance) values
("jason", 1000),
("egon", 1000),
("tank", 1000);

-- tank向jason借钱，egon充当中间商抽取10%
start transaction;  -- 开启事务
update user set balance = 900 where name="jason";  -- jason账户扣除100块
update user set balance = 1010 where name="egon";  -- egon账户增加10块
update user set balance = 1090 where name="tank";  -- tank账户增加90块
```
![](https://images.gitee.com/uploads/images/2020/1126/204734_c42265fe_7841459.png "屏幕截图.png")
```sql
commit;  - 提交事务
```
![输入图片说明](https://images.gitee.com/uploads/images/2020/1126/204945_6258f68b_7841459.png "屏幕截图.png")


# 四、存储过程
包含了一系列的可执行sql语句，存储过程存放在MySQL服务端，可以直接调用存储过程触发内部的sql语句执行(**类似于函数**)

**基本使用**
```sql
delimiter &&
-- 创建存储过程
create procedure 存储过程名字(形参列表)
begin
    sql代码;
end$$
delimiter ;

call 存储过程名字(实参列表);  -- 调用存储过程
```
**示例**
```sql
delimiter $$
-- 创建存储过程
create procedure p1(
    in m varchar(20),  -- m只能接收int类型, in限制m不能返回
    out res int -- out指明res可以返回, 表明存储过程已执行
)
begin
    select tname from teacher where tno=m;
    set res=0;
end $$
delimiter ;

-- 针对可以返回的形参，必须传入变量名
set @ret = 10; -- 定义变量
select @ret;  -- 查看变量的值
-- 调用存储过程
call p1("804", @ret);  -- 调用传参
```

**pymysql中调用存储过程**
```python
import pymysql


conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="dyp1996",
    charset="utf8",
    db="db_seacher"
)  # 连接数据库

cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 生成游标对象, 将查询结果以字典形式返回

# 调用存储过程
cursor.callproc("p1", ("804", 10))  # 自动变形参数
"""
arg参数变形为
@_存储过程名字_index
"""
cursor.execute("select @_p1_1;")
print(cursor.fetchall())
```

**三种开发模式**

1. 应用程序+存储过程: 首先写好存储过程，由应用程序调用
    * 优点: 开发和执行效率高
    * 缺点: 存储过程的扩展性较差
2. 应用程序和数据库部分由同一部门人完成
    * 优点: 扩展性高
    * 确定: 开发效率低下，`sql`语句较为繁琐，后期优化难度较大
3. 使用第三方框架操作数据库
    * 优点: 开发效率高
    * 缺点: 语句扩展性差，可能会出现效率低下问题

# 五、内置函数
**存储过程相当于自定义函数**
|函数|说明|
|:---:|:---:|
|`NOW()`|获取当前时间|
|`date_format(时间日期字段, 格式符)`|格式化时间日期|

**更多内置函数**
[mysql函数--菜鸟教程](https://www.runoob.com/mysql/mysql-functions.html)

# 六、流程控制
* if判断
    ```sql
    if 条件1 then
        条件1成立执行的sql语句
    elseif 条件2 then
        条件2成立执行
    else
        条件1, 2均不成立执行
    end if;
    ```
* while循环
    ```sql
    while 循环条件 do
        循环执行的sql语句
    end while;
    ```
# 七、索引理论
**数据存在硬盘之上的，查询数据不可避免进行io操作**

索引是一种数据结构，类似于书的目录。是存储引擎用于快速查找数据的数据结构

**索引键**
* `primary key`
* `unique key`
* `index key`

以上三个`key`都可以做为索引. 加速查询速度

**本质** 

不断的缩小筛选范围选出想要查询的结果

> 1. 一张表中可以有多个索引
> 2. 使用索引查询数据才能加速
> 
> 3. 表中存在大量数据时, 创建索引速度很慢
> 4. 索引创建完毕之后，查询数据的效率就很高；插入数据性能将会很低
>
> **索引不要随意创建**

<br>

**b+树索引**

![b+树](https://images.gitee.com/uploads/images/2020/1126/231503_b49fa64b_7841459.png "屏幕截图.png")
叶子节点存放数据, 其他节点存放虚拟数据，用于划分数据在磁盘中的位置。为了提高查询的效率，就必须使磁盘块中存放的数据最多。这条可以使b+树的层级小，查询效率就越高


**聚集索引(primary key)**
> `innodb`规定必须要有一个主键，innodb引擎将索引存放在了数据表

**辅助索引(unique key, index key)**
> 查询数据的时候，不可能都使用到主键，也可能使用其他字段
> 此时没有办法利用聚集索引加速查询。
> 
> 可以设置辅助索引加速查询。辅助索引也是b+树；但是叶子节点存放的是数据的主键值。

**覆盖索引**
> 在辅助索引的叶子节点，就已经获取到了数据，这些索引就称为覆盖索引
