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


