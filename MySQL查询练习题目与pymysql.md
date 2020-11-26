# 一、mysql查询练习题
## 1.1 表准备
```sql
-- 创建班级表
create table class
(
    cid varchar(20) primary key,
    cname varchar(20) not null
);

-- 建学生信息表student
create table student
(
    sno varchar(20) not null primary key,
    sname varchar(20) not null,
    ssex varchar(20) not null,
    sbirthday datetime,
    class_id varchar(20),
    foreign key(class_id) references class(cid)
    on update cascade
    on delete cascade
);

-- 建立教师表
create table teacher
(
    tno varchar(20) not null primary key,
    tname varchar(20) not null,
    tsex varchar(20) not null,
    tbirthday datetime,
    prof varchar(20),
    depart varchar(20) not null
);

-- 建立课程表course
create table course
(
    cno varchar(20) not null primary key,
    cname varchar(20) not null,
    tno varchar(20) not null,
    foreign key(tno) references teacher(tno)
    on update cascade
    on delete cascade
);

-- 建立成绩表
create table score
(
    id int auto_increment primary key,
    sno varchar(20) not null,
    foreign key(sno) references student(sno),
    cno varchar(20) not null,
    foreign key(cno) references course(cno)
    on update cascade
    on delete cascade,
    degree decimal
);

-- 添加班级表
insert into class values('95031', "电子一班");
insert into class values('95033', "计算机一班");

-- 添加学生信息
insert into student values('108','曾华','男','1977-09-01','95033');
insert into student values('105','匡明','男','1975-10-02','95031');
insert into student values('107','王丽','女','1976-01-23','95033');
insert into student values('101','李军','男','1976-02-20','95033');
insert into student values('109','王芳','女','1975-02-10','95031');
insert into student values('103','陆君','男','1974-06-03','95031');

-- 添加教师表
insert into teacher values('804','李诚','男','1958-12-02','副教授','计算机系');
insert into teacher values('856','张旭','男','1969-03-12','讲师','电子工程系');
insert into teacher values('825','王萍','女','1972-05-05','助教','计算机系');
insert into teacher values('831','刘冰','女','1977-08-14','助教','电子工程系');

-- 添加课程表
insert into course values('3-105','计算机导论','825');
insert into course values('3-245','操作系统','804');
insert into course values('6-166','数字电路','856');
insert into course values('9-888','高等数学','831');

-- 添加成绩表
insert into score values(1,'103','3-245','86');
insert into score values(2,'105','3-245','75');
insert into score values(3,'109','3-245','68');
insert into score values(4,'103','3-105','92');
insert into score values(5,'105','3-105','88');
insert into score values(6,'109','3-105','76');
insert into score values(7,'103','3-105','64');
insert into score values(8,'105','3-105','91');
insert into score values(9,'109','3-105','78');
insert into score values(10,'103','6-166','85');
insert into score values(11,'105','6-166','79');
insert into score values(12,'109','6-166','81');
```

1. 查询所有课程的名称和任课老师姓名
    ```sql
    SELECT
    	course.cname,
    	teacher.tname 
    FROM
    	course
    	INNER JOIN teacher ON course.tno = teacher.tno;
    ```
2. 查询平均成绩大于80分的同学的姓名和平均成绩
    ```sql
    SELECT
    	student.sno,
    	t1.avg_degree 
    FROM
    	student
    	INNER JOIN (
    	SELECT
    		score.sno,
    		avg( score.degree ) AS avg_degree 
    	FROM
    		score
    		INNER JOIN student ON score.sno = student.sno 
    	GROUP BY
    		score.sno 
    	HAVING
    		avg_degree > 80 
    	) AS t1 ON student.sno = t1.sno;
    ```
3. 查询没有报 *王萍* 老师课的学生姓名
    ```sql
    -- 一步、先找到王萍老师教授的课程no
    -- SELECT course.cno FROM teacher INNER JOIN course on teacher.tno = course.tno 
    -- WHERE teacher.tname="王萍"; 
    -- 二步、找到报了王萍老师课程学生的学生no
    -- SELECT DISTINCT score.sno FROM score where score.cno in (SELECT course.cno FROM teacher INNER JOIN course on teacher.tno = course.tno 
    -- WHERE teacher.tname="王萍");
    -- 三步、到学生表中查询出不在查询出学生no的学生姓名
    SELECT
    	student.sname 
    FROM
    	student 
    WHERE
    	student.sno NOT IN (
    	SELECT DISTINCT
    		score.sno 
    	FROM
    		score 
    	WHERE
    		score.cno IN (
    		SELECT
    			course.cno 
    		FROM
    			teacher
    			INNER JOIN course ON teacher.tno = course.tno 
    		WHERE
    			teacher.tname = "王萍" 
    		));
    ```
4. 查询没有同时选修计算机导论和数字电路的学生姓名
    ```sql
    -- 4. 查询没有同时选修计算机导论和数字电路的学生姓名
    -- 第一步、先查询出计算机导论和数字电路课程id号
    SELECT course.cno FROM course WHERE course.cname in ("计算机导论", "数字电路");
    -- 第二步、获取选了计算机导论和数字电路学生的数据
    SELECT * FROM score WHERE score.cno in (SELECT course.cno FROM course WHERE course.cname in ("计算机导论", "数字电路"));
    -- 第三步、按照学生分组 筛选出之选了一门可的学生id，获取学生姓名
    SELECT student.sname from student where student.sno in (SELECT score.sno FROM score WHERE score.cno in (SELECT course.cno FROM course WHERE course.cname in ("计算机导论", "数字电路")) GROUP BY score.sno HAVING count(score.cno) = 1);
    ```
5. 查询出分数低于70分的学生姓名和班级
```sql
-- 5. 查询出超过两门分数分数低于80分的学生姓名和班级
-- 第一步、查询出分数低于80分的数据
select * from score WHERE score.degree < 80;
-- 第二步、按学生分组，获取
select * from score WHERE score.degree < 80 GROUP BY score.sno HAVING COUNT(score.cno) >= 2;
-- 第三步、查询出班级
select class.cname, student.sname from class INNER JOIN student on class.cid = student.class_id WHERE student.sno in (select score.sno from score WHERE score.degree < 80 GROUP BY score.sno HAVING COUNT(score.cno) >= 2);
```

# 二、PyMySQL操作数据库

* 下载数据库接口

  ```shell
  pip install pymysql
  ```

* 链接数据库
    ```python
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="dyp1996",
        charset="utf8",
        db="db_seacher"
    )  # 连接数据库，生成连接对象
    ```

* 建立游标
  > 游标是用于操作数据、光标和执行sql语句
  ```python
  cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)  # 建立游标,将查询结果以字典形式返回
  ```

* 执行`sql`语句

  ```python
  excutes = cursor.execute(sql)  # 不会返回结果，但是会返回影响数据的条数
  ```

* 查询`sql`语句执行结果

  ```python
  value = cursor.fetchone()  # 获取一条数据
  value = cursor.fetchmany(size)  # 获取size条数据
  value = cursor.fetchall()  # 获取所有数据
  ```

* 光标移动
    ```python
    cursor.scroll(-1, "relative")  # 相对于光标所在位置向前移动
    cursor.scroll(1, "absolute")  # 相对于数据的开头向后移动
    ```
    
* 事务

  `pymysql`会主动开启一个事务，执行与修改数据相关的`sql`语句不会主动提交

  * 提交事务

    ```python
    connection.commit()  # 用连接生成的对象调用
    ```

  当发生错误时，有必要对事务进行回滚

  * 回滚

    ```python
    connection.rollback()  # 用连接生成的对象调用
    ```

* 关闭游标

  ```python
  cursor.close() 
  ```

* 关闭连接

  ```python
  connection.close()
  ```


**pymysql补充**
* 在数据库操作中，增加数据、删除数据、修改数据的操作在pymysql中需要二次确认
    ```sql
    connection.commit()
    ```

* 添加多条数据
    ```sql
    sql = "insert into class values (%s, %s)"

    cursor.executemany(sql, [(.., ..),(.., ..),(.., ..),...,(.., ..)])
    ```

# 三、sql注入问题
利用编程语言拼接sql语句，使执行sql语句时出现条件 **恒为真** 或者 **条件丢失**导致数据库被入侵.

**常见的sql注入方法** 
1. 恒为真条件(`or 1 = 1`恒真条件)
    ```sql
    select * from user where useid="xxx" or 1=1;
    ```
2. 条件缺少(`--`sql注释语法)
    ```sql
    select * from user where user="xxx" -- and password="yyy";
    ``` 


**问题解决**
1. 尽量不使用编程语句进行sql语句拼接
2. 使用SQL参数














