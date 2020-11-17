# 一、连接服务端
> mysql的服务端程序: `mysqld`,客户端程序: `mysql`

* 完整命令
    ```sql
    mysql -h host -P port -uUserName -p password
    ```
* 通常在连接本地服务端时，省略 `-h` 和 `-P`选项
    ```sql
    mysql -uUsernName - pPassWorld
    ```
* 游客登录(直接在终端输入mysql)

# 二、查看库命令
```sql
show databases;  -- 查看所有的库 
```
> 1. 如果命令输入错误，可以在结尾添加`\c`取消命令执行

# 三、退出MySQL客户端与服务端的连接
```sql
exit  --
quit  --
\q    
```

# 四、设置MySQL用户密码
在`CMD`或在终端输入:

`mysqladmin -uUserName -pOldPassword password new_password`

