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

# 五、跳过授权表并从新设置密码
MySQL登录是将mysql客户端发送到服务端的用户名和密码在某个位置进行比对。
> 校验密码的本质就可以看成一个登录认证装饰器

**跳过验证**
1. 关闭MySQL服务
2. 在命令行启动(跳过认证): `mysqld --skip-grant-tables`
3. 此时客户端连接就不用在输入密码
4. 修改当前用户密码: 
   > ```sql
   > update mysql.user set password=password(new_password) where user='root'and host='localhost'
   > flush privileges;
   > ```
5. 关闭当前服务端，然后重新启动(通过校验)






