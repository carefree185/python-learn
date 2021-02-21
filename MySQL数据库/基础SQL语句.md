# 一、库的增删改查
**创建数据库** 
```sql
CREATE DATABASE [IF NOT EXISTS] db_name [CHARSET="编码"];  -- 
```
**查询数据库**
```sql
show databases;  -- 查询所有数据库
SHOW CREATE DATABASE db_name; -- 查询db_name数据库的创建详细信息
```
**修改数据库**
```sql
ALTER DATABASE db_name CHARSET="编码"; -- 修改db_name的编码
```
**删除数据库**
```sql
DROP DATABASE db_name;  -- 删除db_name数据库
```

# 二、表的增删改查
**操作表(文件)时，要指定表存放的数据库** 
```sql
SELECT DATABASE(); -- 查看当前所在的库
USE db_name;  -- 切换到db_name数据库
```
**创建表**
```sql
CREATE TABLE tb_name(filed_name datatype, filed_name datatype, ..., filed_name datatype); -- filed_name: 字段名 datatype: 字段数据类型
```
**查看表**
```sql
SHOW TABLES;  -- 查看当前库中的所有表
SHOW CREATE TABLE tb_name; 查看tb_name表的创建信息
DESCRIBE tb_name == DESC tb_name; -- 查看tb_name表的信息
```
**修改表**
```sql
-- 修改表名 将表面修改为new_tb_name
alter table tb_name rename to new_tb_name; 
-- 修改字段名 将字段名修改为 new_name
alter table tb_name change name new_name data_type; 
-- 修改字段类型
alter table tb_name modify field_name data_type;
-- 添加字段
alter table tb_name add [column] field_name data_type;
-- 删除字段
ALTER TABLE tb_name DROP [column] field_name;
```
**删除表**
```sql
DROP TABLE tb_name; 删除tb_name表
```

> 操作表可以指定数据库进行操作(绝对路径形式)

# 三、数据的增删改查
**一定要先创建库，再创建表，最后在操作数据**

**添加数据**
```sql
-- 指定字段插入
INSERT [INTO] tb_name(field_name_1, field_name_2, ...) VALUE(value_1, value_2, ...); -- 只能插入一行数据
-- 多行插入
INSERT [INTO] tb_name(field_name_1, field_name_2, ...) VALUES(value_1, value_2, ...), (value_1, value_2, ...), ...; -- 指定字段多行插入
-- 全字段插入
INSERT [INTO] tb_name VALUES(value_1, value_2, ...), (value_1, value_2, ...), ...; -- 可以插入多行数据
```

**查询数据**
```sql
-- 全字段查询
SELECT * FROM tb_name;  -- 从tb_name表中查询出全部字段的数据
-- 指定字段查询
SELECT field_name_1, field_name_2, ... FROM tb_name; --从tb_name表中查询出指定字段的数据
```

**修改表中数据**
```sql
-- 全文档修改
update tb_name set field_name_1=field_value_1,field_name_2=field_value_2; -- 可以修改多个
-- 满足条件修改
update tb_name set field_name=field_value where conditions;
```

**删除表中数据**
```sql
delete from tb_name;  -- 删除tb_name表中的所有数据
delete from tb_name where conditions;  -- 满足条件删除数据
```

**使用**
```sql
mysql> show databases;   -- 查看存在的数据库
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test               |
+--------------------+
4 rows in set (0.00 sec)

mysql> create database learndb charset=utf8;  -- 创建数据库
Query OK, 1 row affected (0.02 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| learndb            |
| mysql              |
| performance_schema |
| test               |
+--------------------+
5 rows in set (0.00 sec)

mysql> use learndb  -- 进入数据库
Database changed
mysql> create table t1(id int, name varchar(20));  -- 创建表
Query OK, 0 rows affected (0.07 sec)

mysql> insert into t1 values(0, "小芳"),(1, "小南");  -- 插入数据到表
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> select * from t1;  -- 全字段查询
+------+--------+
| id   | name   |
+------+--------+
|    0 | 小芳   |
|    1 | 小南   |
+------+--------+
2 rows in set (0.01 sec)

mysql> delete from t1 where id = 0;  -- 删除表中的数据
Query OK, 1 row affected (0.01 sec)

mysql> select * from t1;
+------+--------+
| id   | name   |
+------+--------+
|    1 | 小南   |
+------+--------+
1 row in set (0.00 sec)

mysql> desc t1;  -- 查看表的结构
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(11)     | YES  |     | NULL    |       |
| name  | varchar(20) | YES  |     | NULL    |       |
+-------+-------------+------+-----+---------+-------+
2 rows in set (0.03 sec)

mysql> show create table t1;  -- 查看创建表的sql语句
+-------+-------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                            |
+-------+-------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 |
+-------+-------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```


