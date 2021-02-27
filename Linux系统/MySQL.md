# MariaDB
`mariadb` 是 `mysql` 的分支

可以直接在官方网站下载

# MySQL安装

### 下载

```SHELL
wget http://mirrors.sohu.com/mysql/MySQL-5.7/mysql-5.7.27-1.el7.x86_64.rpm-bundle.tar
```

### 解压

```SHELL
tar xf mysql-5.7.27-1.el7.x86_64.rpm-bundle.tar
```
### 安装

```shell
yum install -y *.rpm
```

默认安装位置：`/var/lib/mysql`

如果开启了selinux则会出现如下错误
```shell
2019-08-30T11:18:22.976635Z 0 [Warning] Can't create test file /mydata/mysql/localhost.lower-test
2019-08-30T11:18:22.976687Z 0 [Note] /usr/sbin/mysqld (mysqld 5.7.27) starting as process 2788 ...
2019-08-30T11:18:22.980289Z 0 [Warning] Can't create test file /mydata/mysql/localhost.lower-test
2019-08-30T11:18:22.980338Z 0 [Warning] Can't create test file /mydata/mysql/localhost.lower-test
```
只需要关闭selinux
```shell
setenforce 0
```

### 重置密码
```
# 查看默认密码
grep 'pass' /var/log/mysqld.log

# 重置密码
mysql_secure_installation
输入root密码
是否要修改密码
是否要修改root密码 大小写 数字 特殊字符 
是否要删除匿名用户
是否禁止root远程登录
是否要删除test数据库
是否要刷新表的权限
```
### 密码校验规则

```mysql
set global validate_password_policy=0;
-- 0 校验级别最低，只校验密码的长度，长度可以设定
-- 1 必须包括大写字母、小写字母、数字、特殊字符
-- 2 必须满足上面两条，并追加，对于密码中任意连续的4个（或者4个以上） 字符不能是字典中的单词
set global validate_password_length=3; -- 修改密码的最短长度
```

### 创建用户
```mysql
create user 'username'@'ip' identified by 'password';
-- 全部ip的话则是%
```

### 查看权限和授权用户
```mysql
show grants;  -- 查看权限

grant all on *.* to 'username'@'ip' identified by 'password';  -- 给权限给用户

flush privileges;  -- 刷新权限表
```

# MySQL主从配置

* 在业务复杂的系统中，有这么一个情景，有一句sql语句需要锁表，导致暂时不能使用读的服务，
  那么就很影响运行中的业务，使用主从复制，让主库负责写，从库负责读，这样，即使主库出现了锁表的情景，通过读从库也可以保证业务的正常运行。
* 做数据的热备，主库宕机后能够及时替换主库，保证业务可用性。
* 架构的扩展。业务量越来越大，I/O访问频率过高，单机无法满足，此时做多库的存储，
  降低磁盘I/O访问的频率，提高单个机器的I/O性能。

## MySQL主从复制原理
![](./.img/mysql主从复制原理图.jfif)

* 主服务器角色的数据库服务器必须开启二进制日志
* 主服务器上面的任何修改都会通过自己的` I/O tread(I/O 线程)`保存在二进制日志 `Binary log` 里面。
* 从服务器上面也启动一个 `I/O thread`，通过配置好的用户名和密码, 连接到主服务器上面请求读取二进制日志，然后把读取到的二进制日志写到本地的一个`Realy log（中继日志）`里面
* 从服务器上面同时开启一个 `SQL thread` 定时检查 `Realy log`(这个文件也是二进制的)，如果发现有更新立即把更新的内容在本机的数据库上面执行一遍。

## MySQL主服务器配置
```
server-id=1
log-bin = /var/log/mysql/master-bin
sync_binlog = 1  # 保证主从复制的事务安全(原子操作)
```
在主服务器执行命令
```mysql
grant replication slave on *.* to 'slave'@'192.168.174.132' identified by 'slave1234';  # 创建用户并指定权限

flush privileges;  # 刷新权限
```

## MySQL从服务器每组
```
server-id = 2
relay_log = /var/log/mysql/slave-log
sync_binlog = 1
read-only = ON
```
在从服务器执行命令
```mysql
CHANGE MASTER TO
  MASTER_HOST='master2.example.com',
  MASTER_USER='replication',
  MASTER_PASSWORD='password',
  MASTER_PORT=3306,
  MASTER_LOG_FILE='master2-bin.001',
  MASTER_LOG_POS=4,
  MASTER_CONNECT_RETRY=10; #监控主服务器的时间
  
# 执行如下命令
## 链接主库
change master to master_host='192.168.174.129',master_user='slave',master_password='slave1234';
## 启动进程
start slave;

## 查看状态
show slave status\G;
```
如果查看状态时出现错误
```
Last_IO_Error: Fatal error: The slave I/O thread stops because master and slave have equal MySQL server UUIDs; these UUIDs must be different for replication to work.
```
需要删除从服务器中的`data`目录下的`auto.cnf`，然后从前数据库

# MySQL

