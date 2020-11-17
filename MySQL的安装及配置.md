# 一、Linux下的MySQL安装

1. 安装
os：Ubuntu18.04
进入终端
```shell
# 命令1
sudo apt update
# 命令2
sudo apt install mysql-server
```
等待安装完成

2. 配置
```shel
# 命令3
sudo mysql_secure_installation
```
根据自己的需要选择配置。 参考：
```shell
#1
VALIDATE PASSWORD PLUGIN can be used to test passwords...
Press y|Y for Yes, any other key for No: N (我的选项)

#2
Please set the password for root here...
New password: (输入密码)
Re-enter new password: (重复输入)

#3
By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them...
Remove anonymous users? (Press y|Y for Yes, any other key for No) : N (我的选项)

#4
Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network...
Disallow root login remotely? (Press y|Y for Yes, any other key for No) : Y (我的选项)

#5
By default, MySQL comes with a database named 'test' that
anyone can access...
Remove test database and access to it? (Press y|Y for Yes, any other key for No) : N (我的选项)

#6
Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.
Reload privilege tables now? (Press y|Y for Yes, any other key for No) : Y (我的选项)
--------------------- 
作者：尘埃安然 
来源：CSDN 
原文：https://blog.csdn.net/weixx3/article/details/80782479 
版权声明：本文为博主原创文章，转载请附上博文链接！
此时配置基本完成
```
3. 增加用户及远程连接配置
3.1 用mysql的root用户登录mysql
```shell
# 命令 4
mysql -uroot -p

# 输入密码
# 如果报错使用 sudo mysql 进入mysql数据库。
# 使用以下命令
use mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
flush privileges;
让mysql通过密码登录
```
3.2 添加用户
```shell
# 切换到mysql
use mysql;  

# 查看已存在的用户
select user, host from user; 

# 创建用户
create user "username"@"localhost" identified by "passwd"; 

# 再次查看确保用户已经添加成功
select user, host from user; 
```
3.3 赋予权限
```shell
# 赋予远程连接权限
grant all on *.* to "username"@'%' with grant option;

# username是要用于远程连接的用户
# % 表示所用的ip可以连接
# passwd最好和建立用户时一样，方便记忆

# 刷新
flush privileges;
```
还没完 

4. 修改配置文件
```shell
# 进入 /etc/mysql
cd /etc/mysql

# 查看my.cnf
vim my.cnf

# 发现他只是引入一些文件，到这些文件中去寻找。最后在 /etc/mysql/mysql.conf.d这个目录下找到文件 mysqld.cnf里面找到bind-address=127.0.0.1将之注释掉

# 切换到 mysql.conf.d目录下
cd ./mysql.conf.d
# 打开mysqld.cnf
vim mysqld.cnf
# 注释掉 bind-address
在bind-address 前面加 （#）
```
到此完成远程连接配置

5. 修改默认编码
用于mysql默认不支持中文所以要修改默认编码 

之前打开了 mysql.cnf 找到[mysqld]在skip-external-locking下添加
```shell
character-set-server=utf8
```
这只是设置了服务的编码，下面去设置客户端编码

在设置远程连接是看到在my.cnf里面引用了两个文件，到另一个文件中，
```shell
cd ..  # 返回上一级目录

cd conf.d  # 进入conf.d目录

ls  # 查看文件

# 打开 mysql.cnf
sudo vim mysql.cnf 
在[mysql]下面插入一行:
default-character-set=utf8
保存的退出
```
最后重启mysql
```shell
service mysql restart
```
配置完成

# 二、Windows下MySQL的安装

## **下载`.msi`文件按照引导下一步安装发安装** 

## 下载编译好的二进制文件:https://dev.mysql.com/downloads/mysql/
1. 下载好文件
2. 解压到位置
3. 将`bin`目录添加到系统`Path`变量中
4. 将`mysql`服务端配置为系统服务
> 1. 在mysql的安装目录下新建`my.ini`文件
>    ```
>    [client]
>    # 设置mysql客户端默认字符集
>    default-character-set=utf8
>     
>    [mysqld]
>    # 设置3306端口
>    port = 3306
>    # 设置mysql的安装目录
>    basedir=C:\\mysql
>    # 设置data目录
>    datadir=C:\\mysql\\data
>    # 服务端使用的字符集默认为8比特编码的latin1字符集
>    character-set-server=utf8
>    ```
> 2. 打开管理员的cmd输入: `mysqld install`将MySQL配置为系统服务
> 3. 启动服务: `net start mysql`
> 4. 删除服务: `mysqld --remove`
> 5. 如果MySQL服务端被删除，删除服务执行: `sc delete 服务名称` 





