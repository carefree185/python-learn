# 一、初始介绍

## 1.1 用户介绍

- root用户: 系统安装自带的默认用户
	- 是一个特殊的管理账号，也可以成为超级管理员
	- root用户对系统有完全控制的权限
	- 对系统的损害会无限大
	- 在工作中，如果没有特殊的必要，尽量不要使用root
- 普通用户：系统安装后创建的用户
	- 权限有限
	- 对系统的损害会小

## 1.2 终端

- 设备终端
- 物理终端
- 虚拟终端 `ctrl + alt + F1-F6` /dev/tty#
- 图形终端  `/dev/tty7`
- 串行终端
- 伪终端 通过ssh远程连接的 `/dev/pts/#`
	- 查看终端的命令 `tty`
	- 查看ip地址的命令 `ip addr`

## 1.3 交互式接口

启动终端以后，在终端设备上附加的一个应用程序

- GUI（桌面）
- CLI `command line`: 命令行终端
	- powershell(Windows上的命令行终端)
	- sh
	- bash（linux，mac默认的程序）
	- zsh
	- csh
	- tcsh

### 1.3.1 bash

bash是linux系统的用户界面，提供了用户和操作系统之间的交互， 它接收用户的输入，让它送给操作系统执行

- 目前bash是是linux和mac上默认的shell
- centos默认使用
- 显示系统当前使用的shell  `echo $SHELL`
- 查看系统内可以使用的shell `cat /etc/shells`
- `ctrl + d` 快速终止当前的连接
- 切换shell `chsh -s shell`

### 1.3.2 远程链接终端缓慢解决方式

```shell
echo "UseDNS no" >> /etc/ssh/sshd_config
systemctl restart sshd
```

### 1.3.3 命令提示符

```shell
root@VM-0-11-ubuntu:~#  #  root用户的命令提示符
ubuntu@VM-0-11-ubuntu:~$  # 普通用户的命令提示符
```

管理员是`#` 普通用户时`$`

* 修改命令提示符显示格式
  ```shell
  root@VM-0-11-ubuntu:~# echo $PS1
  \[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w\$
  # \u 代表当前登录的用户
  # \h 代表当前主机的主机名
  # \W 代表当前的目录
  # 0表示默认字体，1表示加粗，4在字体下方加下划线 5 闪烁 7 代表突出显示
  # 31-37 字体颜色
  # 40-47 表示背景颜色
  echo 'PS1="\[\e[1;35mm\][\u@\h \W]\\$\[\e[0m\]"' >> /etc/profile.d/ps.sh #永久生效
  ```

## 1.4 命令

执行命令: 输入命令回车

内部命令: shell 自带的命令

- `help` 显示所有的内部命令

外部命令: 第三方提供的命令

查看命令的类型: `type`

```shell
root@VM-0-11-ubuntu:~# type echo
echo is a shell builtin
root@VM-0-11-ubuntu:~# type top
top is /usr/bin/top
```

### 1.4.1 命令别名(alias)

命令: `alias 别名='命令'`，给命令设置别名, 只对当前终端有效

查看别名: `alias`

取消别名: `unalias 别名`

执行本身命令(不执行别名指定的命令，执行命令本身):

* `\command`
* `"command"`
* `'command'`
* `path` 命令所在的目录

### 1.4.2 命令格式

`command [options.....] [args...]`

* `command`: 命令

* `options`: 启动或者关闭命令里面的某些功能
	- 长选项：`--help` `--color`
	- 短选项： `-i` `-l`(短选项可以合并)

* `args`: 命令的作用体，一般情况下是目录或者文件，用户名等等

* 注意：
	- 短选项是可以合并
	- 空格隔开
	- `ctrl+c` 结束命令的执行
	- 在同一行执行多个命令用`;`隔开
	- 一个命令可以在多行显示用`\`连接

### 1.4.3 命令的帮助信息

**内部命令**: 获取命令帮助信息

* `help command`
* `man command`

**外部命令**：获取命令帮助信息

* `command -h`
* `command --help`
* `man command`
* `官方文档`

### 1.4.4 man手册

man手册分了如下章节

```
1   Executable programs or shell commands  (命令章节)
2   System calls (functions provided by the kernel) (系统调用)
3   Library calls (functions within program libraries) (库调用)
4   Special files (usually found in /dev) (设备文件和特殊文件)
5   File formats and conventions, e.g. /etc/passwd (配置文件的格式)
6   Games  (游戏)
7   Miscellaneous  (including  macro  packages  and  conventions),   e.g.
   man(7), groff(7)  (杂项)
8   System administration commands (usually only for root) (系统管理命令)
9   Kernel routines [Non standard]  (系统内核api)
```

**空格翻页，回车换行**

查看命令所属章节: `whatis 命令`

指定章节打开命令的man手册: `man 章节 命令`

### 1.4.5 常用bash快捷键

- `ctrl+l` 清屏 相当于`clear`
- `ctrl+o` 执行当前的命令，并换行显示当前的命令
- `ctrl+s` 锁屏
- `ctrl+q` 解锁
- `ctrl+c` 终止命令
- `ctrl+z` 挂起命令
- `ctrl+a` 光标移动到行首，相当于Home
- `ctrl+e` 光标移动到行尾，相当于End
- `ctrl+xx` 在开头和当前光标所在位置跳转
- `ctrl+k` 删除光标后的文字
- `ctrl+u` 删除光标前的文字
- `alt+r` 删除正行

### 1.4.6 Tab命令自动补全

- 命令补全
	- 内部命令
	- 外部命令：根据环境变量定义的路径，从前往后依次查找，自动匹配第一个查找到的内容
	- 如果用户给的命令只有唯一一个匹配，则直接补全
	- 如果有多个匹配，则需要在按tab键(双击)将所有匹配到的结果展示出来
- 目录补全
	- 把用户给定的字符作为文件的开头，如果有唯一一个匹配则直接补全
	- 如果有多个匹配，则需要再次按tab键(双击)把所有的匹配到的结果展示出来

### 1.4.7 字符串中执行命令
```shell
ubuntu@VM-0-11-ubuntu:~$ name=dyp  # 设置变量
ubuntu@VM-0-11-ubuntu:~$ echo $name  # 使用变量
dyp
ubuntu@VM-0-11-ubuntu:~$ echo '$name'
$name
ubuntu@VM-0-11-ubuntu:~$ echo "$name"
dyp
ubuntu@VM-0-11-ubuntu:~$ echo "`ls -la`"  # 字符串中的命令执行
total 80
drwx------ 8 ubuntu ubuntu 4096 Feb 22 15:18 .
drwxr-xr-x 3 root   root   4096 Aug  6  2020 ..
-rw-r--r-- 1 ubuntu ubuntu 6290 Feb 22 16:34 .bash_history
-rw-rw-r-- 1 ubuntu ubuntu  104 Feb 21 22:04 .bash_profile
drwx------ 4 ubuntu ubuntu 4096 Feb 21 00:51 .cache
-rw-r--r-- 1 root   root      0 Aug 12  2020 .cloud-warnings.skip
-rw------- 1 ubuntu ubuntu  297 Feb 21 00:42 .dbshell
drwxrwxr-x 3 ubuntu ubuntu 4096 Feb 21 00:50 .local
-rw------- 1 ubuntu ubuntu    0 Feb 20 22:50 .mongorc.js
-rw------- 1 ubuntu ubuntu  292 Feb 21 01:09 .mysql_history
drwxr-xr-x 2 root   root   4096 Feb 20 22:06 .pip
-rw-r--r-- 1 root   root     73 Feb 20 22:06 .pydistutils.cfg
-rw------- 1 ubuntu ubuntu    7 Feb 21 00:47 .python_history
-rw------- 1 ubuntu ubuntu   17 Feb 20 23:19 .rediscli_history
drwx------ 2 ubuntu ubuntu 4096 Feb 21 01:02 .ssh
-rw-r--r-- 1 ubuntu ubuntu    0 Aug 12  2020 .sudo_as_admin_successful
drwxr-xr-x 2 ubuntu ubuntu 4096 Feb 21 01:03 .vim
-rw------- 1 ubuntu ubuntu 9233 Feb 21 01:03 .viminfo
drwxrwxr-x 4 ubuntu ubuntu 4096 Feb 21 00:51 .virtualenvs
-rw------- 1 ubuntu ubuntu  180 Feb 22 15:18 .Xauthority
ubuntu@VM-0-11-ubuntu:~$ echo "$(ls -la)"
total 80
drwx------ 8 ubuntu ubuntu 4096 Feb 22 15:18 .
drwxr-xr-x 3 root   root   4096 Aug  6  2020 ..
-rw-r--r-- 1 ubuntu ubuntu 6318 Feb 22 16:34 .bash_history
-rw-rw-r-- 1 ubuntu ubuntu  104 Feb 21 22:04 .bash_profile
drwx------ 4 ubuntu ubuntu 4096 Feb 21 00:51 .cache
-rw-r--r-- 1 root   root      0 Aug 12  2020 .cloud-warnings.skip
-rw------- 1 ubuntu ubuntu  297 Feb 21 00:42 .dbshell
drwxrwxr-x 3 ubuntu ubuntu 4096 Feb 21 00:50 .local
-rw------- 1 ubuntu ubuntu    0 Feb 20 22:50 .mongorc.js
-rw------- 1 ubuntu ubuntu  292 Feb 21 01:09 .mysql_history
drwxr-xr-x 2 root   root   4096 Feb 20 22:06 .pip
-rw-r--r-- 1 root   root     73 Feb 20 22:06 .pydistutils.cfg
-rw------- 1 ubuntu ubuntu    7 Feb 21 00:47 .python_history
-rw------- 1 ubuntu ubuntu   17 Feb 20 23:19 .rediscli_history
drwx------ 2 ubuntu ubuntu 4096 Feb 21 01:02 .ssh
-rw-r--r-- 1 ubuntu ubuntu    0 Aug 12  2020 .sudo_as_admin_successful
drwxr-xr-x 2 ubuntu ubuntu 4096 Feb 21 01:03 .vim
-rw------- 1 ubuntu ubuntu 9233 Feb 21 01:03 .viminfo
drwxrwxr-x 4 ubuntu ubuntu 4096 Feb 21 00:51 .virtualenvs
-rw------- 1 ubuntu ubuntu  180 Feb 22 15:18 .Xauthority
```

### 1.4.8 历史命令
- 可以使用上下箭头来查找之前执行过的命令
- 存放文件是`~/.bash_history`
- 执行的命令是`history`
- 执行上一条命令
  - `上箭头`
  - `!!`
  - `！-1`
  - `ctrl+p` 回车
- 调用上一条命令的最后一个值 `esc .`
- `!#` 指定第`#`条命令
- `!-#` 指定倒数第`#`条命令
- `!string` 用来最近一次匹配到的命令（从下往上）
- `ctrl+r` 搜索命令
- `ctrl+g` 取消搜索
- `\#` 显示最后 `#`条命令

### 1.4.9 命令展开
```shell
touch file{1..10}  # 批量创建文件
seq 0 2 10  # 产生序列
echo file{1..20..2}
```

### 1.4.10 echo回显
```shell
echo -e 'dadasda\ndasdasd'
echo -e '\a' #播放声音
```

# 二、基本命令

## 2.1 查看用户登录信息
1. `whoami` : 当前登录用户的用户名
2. `who am i`: 当前登录用户的详细信息
3. `w`: 查看所有用户和用户执行的命令

```shell
ubuntu@VM-0-11-ubuntu:~$ whoami
ubuntu
ubuntu@VM-0-11-ubuntu:~$ who am i
ubuntu   pts/1        2021-02-22 15:18 (112.18.193.155)
ubuntu@VM-0-11-ubuntu:~$ w
 17:04:04 up 1 day, 18:31,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
ubuntu   pts/1    112.18.193.155   15:18    4.00s  0.04s  0.00s w
```

## 2.2 date时间命令
```shell
Usage: date [OPTION]... [+FORMAT]
  or:  date [-u|--utc|--universal] [MM(月份)DD(日期)hh(时)mm(分钟)[[CC]YY][.ss]]
```
实例
```shell
ubuntu@VM-0-11-ubuntu:~$ date  # 显示当前时间
Mon 22 Feb 2021 05:06:22 PM CST
ubuntu@VM-0-11-ubuntu:~$ date 100923212019  # 设置时间为2019-10-09 23:21
ubuntu@VM-0-11-ubuntu:~$ ntpdate time.windows.com  # 同步网络时间
```
时间格式化
```shell
date +%a  # 显示星期，简写
date +%A  # 显示星期，全写
date +%F  # 显示年-月-日
date +%H  # 显示24小时制的时间
date +%I  # 显示12小时制的时间
date +%m  # 显示月份
date +%d  # 显示日期
date +%M  # 显示分钟
date +%h  # 显示月份(英语)
date +%c  # 
date +%T  # 24小时完整时间
date +%y  # 年
date +%Y  # 年
date +%Y/%m/%d  # 显示年/月/日
date +%s  # 时间戳
date +%W  # 周数
```

## 2.3 时区
```shell
ubuntu@VM-0-11-ubuntu:~$ timedatectl  # 显示时区
               Local time: Mon 2021-02-22 17:27:44 CST
           Universal time: Mon 2021-02-22 09:27:44 UTC
                 RTC time: Mon 2021-02-22 09:27:45    
                Time zone: Asia/Shanghai (CST, +0800) 
System clock synchronized: yes                        
              NTP service: n/a                        
          RTC in local TZ: no 
timedatectl set-timezone Asia/Tokyo  # 设置时区
```
## 2.4 日历
`cal`

`cal -y` 一年的日历

`cal #` 显示`#`年的日历


## 2.5 关机和重启

### 2.5.1 关机
```shell
shutdown  # 默认60秒后关机
shutdown -c  # 取消
shutdown -r  # 重启
shutdown now  # 立即关键
shutdown +n  # n分钟后关键
shutdown hh:mm  # hh:mm点后关键

poweroff  # 关机
```
### 2.5.2 重启
```shell
reboot     # 重启
reboot -f  # 强制重启
reboot -p  # 关机
```

# 三、文件系统与目录结构

## 3.1 文件目录结构
- 文件和目录被组织成一颗倒置的**树状结构**
- 文件系统从根开始，`/`
- 文件名称 **严格区分大小写** 
- 隐藏文件以 `.` 开头
- 路径的分隔符为`/`

## 3.2 文件命名规范

- 文件字符最长为255个字符
- 包括路径在内文件名称最长为4095个
- 颜色表示
  - 蓝色 ---> 文件夹
  - 绿色 --> 可执行文件
  - 红色 --> 压缩文件
  - 蓝绿色 --> 链接文件
  - 灰色-->其他文件
  - 白色 --> 文件
- 除了斜杠和NULL，其他所有字符都可以使用
- 对大小写敏感

## 3.3 文件系统结构
- `/boot` 引导文件的存放位置，内核文件、引导加载器都在此目录
- `/bin` 所有的用户都可以使用的命令
- `/sbin` 管理类的命令
- `/lib` 启动时程序使用的基本库文件 `.so`结尾
- `/lib64` 专门存放`X86_64`系统上得辅助库文件
- `/etc` 存放配置文件
- `/home/USERNAM`E 普通用户的家目录
- `/root` 管理员的家目录
- `/media` 便携式移动设备的挂载点
- `/mnt` 临时文件的挂载点
- `/dev` 设备文件和特殊文件的存放位置
- `/opt` 第三方的应用的安装位置
- `/tmp` 临时文件的存放位置
- `/usr` 存放安装程序
- `/var` 存放经常变化的文件，比如日志
- `/proc` 存放内核启动和进程相关的虚拟文件
- `/sys` 输出当前系统上的硬件相关的文件
- `/srv` 系统上允许的服务用到的数据


## 3.4 linux应用程序的组成
- 二进制文件
  - `/bin`
  - `/sbin`
  - `/usr/bin`
  - `/usr/sbin`
  - `/usr/local/bin`
  - `/usr/local/sbin`
- 库文件
  - `/lib`
  - `/lib64`
  - `/usr/lib`
  - `/usr/lib64`
  - `/usr/local/lib`
  - `/usr/local/lib64`
- 配置文件
  - `/etc`
  - `/etc/name`
  - `/usr/local/etc`
- 帮助文件
  - `/usr/share/man`
  - `/usr/share/doc`
  - `/usr/local/share/man`
  - `/usr/local/share/doc`

## 3.5 绝对路径与相对路径

- 绝对路径
  - 以根开始
  - 完整的文件的存放位置
  - 可以读取到任何一个文件或者文件夹
- 相对路径
  - 不以根开始
  - 相对当前的位置来决定
  - 可以简短的表示一个文件或者文件夹
  - `.` 当前目录
  - `..` 父级目录
## 3.6 命令

### 3.6.1 basename和dirname
* `basename`: 基名
* `dirname`: 目录名

```shell
ubuntu@VM-0-11-ubuntu:~$ basename /etc/mysql
mysql
ubuntu@VM-0-11-ubuntu:~$ dirname /etc/mysql
/etc
```

### 3.6.2 cd(切换目录) 
* `cd 路径`: 路径可以使用绝对路径和相对路径 

	* `cd`: 回到家目录
	* `cd -`: 切换到上一次所在目录
### 3.6.3 pwd(显示当前的工作目录)

```shell
ubuntu@VM-0-11-ubuntu:/etc/mysql$ pwd
/etc/mysql

ubuntu@VM-0-11-ubuntu:/$ cd lib
ubuntu@VM-0-11-ubuntu:/lib$ pwd -P  # 查看链接文件的真实路径
/usr/lib
```
### 3.6.4 ls(列车目录或文件)
```shell
ls -a  # 显示所有文件
ls -l  # 以长格式显示文件列表
total 21104
-rw-r--r--. 1 root root        0 Aug 22 17:21 10
权限        硬盘的引用次数  属主 属组  大小  访问时间  文件名称
ls -R  # 递归显示目录
ls -d  # 显示目录本身
ls -1  # (数字1) 文件分行显示
ls -S  # 按文件大小排序
ls -r  # 倒序显示
ls -t  # 按照时间来排序
ls -lh # 显示人类易读的方式
ls -d */ # 显示当前目录下的文件夹
l.       # 只显示隐藏文件
```

### 3.6.5 目录类型
- `-` 用来表示文件
- `d` 用来表示目录
- `b` 块设备 
- `c` 字符设备
- `l` 表示符号链接文件
- `s` socket套接字

### 3.6.6 stat(查看文件状态)
```shell
ubuntu@VM-0-11-ubuntu:~$ stat .bash_profile 
  File: .bash_profile
  Size: 104       	Blocks: 8          IO Block: 4096   regular file
Device: fc02h/64514d	Inode: 146330      Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/  ubuntu)   Gid: ( 1000/  ubuntu)
Access: 2021-02-21 22:04:21.929185212 +0800  # 访问时间 查看文件内容时发生变化
Modify: 2021-02-21 22:04:21.101189519 +0800  # 修改时间 改变内容发送变化
Change: 2021-02-21 22:04:21.101189519 +0800  # 改动时间 元数据发送变化
 Birth: -
```
* atime 访问时间  查看文件内容就会改变
* mtime 修改时间  改变内容发生变化
* ctime 改动时间  元数据发生变化

### 3.6.7 touch(创建文件和刷新时间)
创建空文件和刷新时间，如果文件存在，则刷新时间，
如果文件不存在，则创建文件

`touch -a 文件`: 只修改文件的`atime`和`ctime`

`touch -m 文件`: 只修改文件的`mtime`和`ctime`

### 3.6.8 文件通配符
- `*` 所有
- `?` 匹配的是任意单个字符
- `~` 表示用户的家目录
- `[123]` 其中一个
- `[^123]` 取反
- `[0-9]` 表示数字
- `[a-z]` 字母（有坑）缺少Z
- `[A-Z]` 字母（有坑）缺少a
- `[:lower:]` 小写字母
- `[:upper:]` 大写字母
- `[:alpha:]` 所有字母 a-zA-Z
- `[:alnum:]` 表示字母和数字
- `[:digit:]` 表示数字

### 3.6.9 创建目录、显示目录树、删除目录
* `mkdir 目录` 创建目录
	- `-p` 递归创建
	- `-v` 显示详细过程
* `tree` 显示目录树
	- `-d` 只显示文件夹

	- `-L #` 只显示#层
* `rmdir` 删除空目录 	  
	- `-p` 递归删除空父目录
	
	- `-v` 显示删除过程
	
### 3.6.10 cp(复制)
`cp` copy 默认情况下是别名，原来本身命令是不提示覆盖的
```shell
Usage: cp [OPTION]... [-T] SOURCE DEST
  or:  cp [OPTION]... SOURCE... DIRECTORY
  or:  cp [OPTION]... -t DIRECTORY SOURCE... 
  -i 显示提示信息
  -n 不覆盖
  -r -R 递归复制
  -d 只复制链接文件，不复制源文件
  -a 归档
  -v 显示过程
  -b 备份原来的文件
  --backup=number 备份文件加上数字
  -p 保留原来的属性
```
- 如果源文件是文件的话
  - 目标是文件
    - 目标文件如果不存在的话，则新建目标文件，并把内容写到目标文件中
    - 如果目标文件存在的话，本来的命令是直接覆盖，建议使用-i来提示用户
  - 目标是文件夹
    - 在文件夹中新建一个同名的文件，并把文件内容写到新文件中
- 如果源文件为多个文件的话
  - 目标必须是文件夹，文件夹必须存在，其他情况都会报错
- 如果源文件是文件夹的话
  - 目标文件是文件： 不可以
  - 目标文件必须是文件夹，必须使用-r选项
  - 如果目标文件不存在：则直接创建目标文件夹，并把源文件夹的数据都复制到目标文件夹
  - 如果目标文件存在：
    - 如果是文件的话，则报错
    - 如果是文件夹：则在目标文件夹中创建同名文件夹，并把所有数据都复制到新文件夹

### 3.6.11 mv 移动文件(重命名)
```shell
Usage: mv [OPTION]... [-T] SOURCE DEST
  or:  mv [OPTION]... SOURCE... DIRECTORY
  or:  mv [OPTION]... -t DIRECTORY SOURCE...
-i 提示
-f 强制
-b 备份
--backup=number 备份后面加数字
-v 显示过程
```

### 3.6.12 rm 删除文件
```shell
Usage: rm [OPTION]... FILE...
-i 提示
-r -R 递归删除
-f 强制删除

rm -rf 慎用
rm -rf /*
cd /
rm -rf *
```

### 3.6.13 ln链接
#### 软链接
- 相当于windows的快捷方式
- 创建命令 `ln -s 源文件 目标文件`
- 可以对目录做软链接
- 指向另外的一个文件或者目录的路径，大小是路径的长度的字符
- 对磁盘引用次数没有影响
- 可以跨分区
- 源文件发生改变，软链接会跟着发生变化
- 源文件删除，软链接不能访问

#### 硬链接
- 磁盘引用次数会发生变化
- 指向的是硬盘上的同一块区域
- 磁盘的引用数会随着硬链接次数来增加
- 不能对目录做硬链接
- 不能跨越分区
- 源文件发生改变，硬链接也会跟着变化
- 源文件删除以后，硬链接可以访问

### 3.6.14 查看文件类型 file

### 3.6.15 输入输出
-  标准输入 **默认是来自键盘的输入** `stdin` 0
-  标准输出 **默认输出到终端窗口** `stdout` 1
-  标准错误输出  **默认输出到终端窗口** `stderr` 2

### 3.6.16 I/O重定向

#### 输出重定向 > 
* `>` 覆盖
	- `>` 将标准输出重定向到文件中
	- `2>` 将错误输出重定向到文件中
	- `&>` 将所有的输出都重定向到文件中

	**禁止、允许覆盖**
	
	- 禁止覆盖 `set -C`
	- 允许覆盖 `set +C`

* `>>` 追加

	- `>>` 将**标准输出**追加到文件中

	- `2>>` 将**错误输出**追加到文件中

	- `&>>` 将**所有输出**追加到文件中

* 标准输出与错误输出分开
	- `command >保存标准输出文件 2>保存错误输出文件 &>所用输出文件 `
	
#### 合并所有的输出
- `&>` 覆盖重定向
- `&>>` 追加重定向
- `command > file 2>&1`
- `command >> file 2>&1`
- `(命令1, ..., 命令n)`：合并多个命令的输出
- `/dev/null` 黑洞

#### 输入重定向 <

* 字符替换 `tr 源字符 目标字符` 将源字符用目标字符替换
	* `tr 'a-z' 'A-Z'`: 用大写字母替换小写字母
	* `tr -t 源字符 目标字符`: 截断
	* `tr -d 源字符 目标字符`: 将目标字符中的源字符删除
	* `tr -s 字符`: 去重，自定字符保留一个
	* `tr -sc 字符`: 取反，非指定字符保留一个

#### 多行发送到stdin
```shell
# 方式一
ubuntu@VM-0-11-ubuntu:~$ cat > f1
hjkdiskjjf
chxska
^C

# 方式二
ubuntu@VM-0-11-ubuntu:~$ cat > f1 <<EOF
> ksjjjfis
> cvjhsxja
> EOF
EOF 不是必须得只要两个相同就可以
```

### 3.6.17 管道 |
`命令1|命令2|命令3`

- 把命令1的输出结果当做命令2的输入结果，把命令2的输出结果当成命令3的输入结果
- 默认情况下，**管道只能传送标准输出**
- 如果需要把错误输出也传递，则需要 `|&`
- 一般用来组合多个命令
- 有一些命令是不接受管道的


## 3.7 文本处理工具

### 3.7.1 cat查看文件内容
```shell
-E 显示结尾的$符
-n 对显示的每一行进行编号
-b 对非空行进行编号
-s 对连续的空行进行压缩
```
### 3.7.2 tac 倒叙显示
### 3.7.3 less 分屏显示
* 向下翻一屏 空格

* 向下翻一行 回车

* q 退出

* `/ 文本`  搜索文本

* `n` 向下查找 `N` 向上查找

* `less` 是man命令的默认分页器

### 3.7.4 more 分页显示文件
* 默认情况下显示读取的百分比
* 读取完成自动退出
* `q` 退出
* `-d` 显示翻屏和退出的提示

### 3.7.5 head 显示文件的前面的内容
* 默认显示前10行
* `-#` 显示前`#`行
* `-n #` 显示前`#`行
* `-c #` 显示前`#`个字符

### 3.7.6 tail 显示文件的后面的内容
* 默认显示后10行
* `-#` 显示后`#`行 
* `-n #` 显示后`#`行
* `-c #` 显示后`#`个字符，换行符也是一个字符

### 3.7.7 cut 切割
`cut OPTION... [FILE]...`

* `-c` 按照字符切割
	* `tail passwd |cut -c2-5`
* `-d` 指定切割符，默认是`tab`
* `-f #` 显示第`#`个字段
* `#，#，#` 显示离散的多个
* `#-#` 表示连续的
	* `1-5,7` 可以结合使用
	
	- `tail passwd |cut -d: -f1-5,7`
	- `tail passwd |cut -d: -f1-5`
	- `tail passwd |cut -d: -f1,3,5`

### 3.7.8 paste 合并
默认是**相同行合并到一起**，默认是`tab`键分隔

* `-d :` 指定间隔符

* `-s` 将所有的行按照列来显示

`paste  a.txt b.txt`

`paste  -d: a.txt b.txt`

`paste  -s a.txt b.txt` 

### 3.7.9 wc 用来对文本进行统计
`wc 选项 文件`

```shell
 4     5     20  b.txt
行数  单词数 字节数 文件名
```

* `-l` 只显示行数
* `-w` 只显示单词数
* `-c` 只显示字节数
* `-m` 只显示字符数
* `-L` 显示文件中最长行的长度

### 3.7.10 sort 排序
```shell
Usage: sort [OPTION]... [FILE]...
  or:  sort [OPTION]... --files0-from=F
```
默认按字母排序

* `-r` 倒序 
* `-R` 随机排序
* `-n` 按照数字排序
* `-f` 忽略大小写
* `-t` 指定分隔符
* `-k #` 指定按照第`#`个字段进行排序

`sort -t: -k3 passwd`

`sort -nt: -k3 passwd `


### 3.7.11 uniq 合并相同的行

合并前提:
- 相邻
- 完全一样

选项: 

* `-c` 显示相同的行出现的次数
* `-d` 只显示重复的行
* `-u` 显示从没有重复过的行

`cut -d" " -f4 d | sort | uniq -c`: Django日志统计

`pv` page: 页面访问量

`uv` user: 页面访问量

### 3.7.12 diff 对比文件
```shell
ubuntu@VM-0-11-ubuntu:~$ diff f1 f2
3d2
< aaaa
ubuntu@VM-0-11-ubuntu:~$ echo "bbbb" >> f2
ubuntu@VM-0-11-ubuntu:~$ diff f1 f2
3c3
< aaaa
---
> bbbb
```

## 3.8 文件权限

### 3.8.1 chown 修改文件的所有者和组

```shell
Usage: chown [OPTION]... [OWNER][:[GROUP]] FILE...
  or:  chown [OPTION]... --reference=RFILE FILE...
```
* `-R`: 递归修改
* `--reference=RFILE`: 使用`RFILE`属主和属组修改

**实例**
```shell
chown wu c  修改属主
chown wu:wu c 修改属主和属组
chown root.root c
chown :wu c 直接属组
chown -R wu test 递归修改
chown --reference=c d
```

**修改属组的命令**
```shell
Usage: chgrp [OPTION]... GROUP FILE...
  or:  chgrp [OPTION]... --reference=RFILE FILE...
```

### 3.8.2 权限表示
权限由9位二进制表示，每3位表示一组。格式如下

`--- --- ---`

分别代表, `属主权限 属组权限 其他权限`

* `u`表示文件的`属主`
* `g`表示文件`属组`
* `o`表示`其他`用户
* `a`表示所有用户

****

* `r`表示读权限(`100` = `4`)
  * 文件，就是可以查看文件内的内容
  * 目录，可以使用`ls`等文件查看命令查看
* `w`表示写权限(`010` = `2`)
  * 文件，修改文别内容
  * 目录，创建和删除
* `x`表示执行权限(`100` = `1`)
  * 文件，执行文件
  * 目录，可以`cd`进入目录

****

* `rw` = `110` = `4 + 2` = `6`
* `r-x` = `101` = `4 + 1` = `5`
* `rwx` = `111` = `4 + 2 + 1` = `7`
* `-wx` = `011` = `2 + 1` = `3`

### 3.8.3 chmod 修改文件

```shell
chmod u+x c 增加
chmod u-x c 删除
chmod u=r c 直接赋值
```

### 3.8.4 设定特殊权限
* `chattr +i`: 不能删除、不能修改、不能变更
* `lsattr`: 查看属性
* `chattr +a`: 只能追加数据


## 3.9 vi/vim文本编辑工具

`vim [option]...file...`

### 3.9.1 打开文件
`vim 选项 文件名`: 可以打开不存在的文件

**选项**
* `+n`: 直接定位到第`n`行
* `+/pattern`: 匹配到第一个`pattern`
* `-b`: 以二进制方式打开文件
* `-d file1 file2`: 对比打开多个文件
* `-m file` 只读方式打开文件
* `-e` 直接以末行模式打开

### 3.9.2 模式

* 命令模式：复制文本，默认打开在命令模式
* 插入模式: 修改文本
* 末行模式: 保存文件，退出

****
* 命令模式 --> 插入模式
	* `i`: 光标处插入
	* `I`: 光标所在的行首插入
	* `a`: 光标所在的后边插入
	* `A`: 光标所在的行尾插入
	* `o`: 在当前光标所在的行的下一行（新开）插入
	* `O`: 在当前光标所在的行的上一行（新开一行）插入
* 插入模式 --> 命令模式
	* `esc`退出插入模式
	
* 命令模式 --> 末行模式
	* `:`
	
* 末行模式 --> 命令模式

	* `esc esc`
	* `esc enter`

### 3.9.3 关闭文件

* 末行模式
	* `:w` 保存
	* `:q` 退出
	* `:x` 保存并退出
	* `:wq` 保存并退出
	* `:q!` 强制退出
	* `:wq!` 强制保存退出
	
* 命令模式
	* `ZZ` 保存并退出
	* `ZQ` 不保存退出

### 3.9.4 末行模式命令
- 按`:` 来进入
- `w` 写入
- `q` 退出
- `wq` 保存并退出
- `q!` 强制退出
- `x` 保存并退出
- `r file` 读入文件
- `w file` 另存为
- `!command` 直接执行命令
- `r!command` 直接把命令的结果写到文件中

### 3.9.5 命令模式跳转
* 字符间跳转(光标移动)
	* `I` 向右
    * `H` 向左
	* `J` 向下
	* `K` 向上
	
* 单词间跳转
	* `w` 下一次的单词的词首
	* `e` 当前词的词尾或下一词的词尾
	* `b` 当前词的词首或者上一词的词首
	* `#command` 直接跳转到`#`单词

* 页面间跳转
	- `H` 页首
	- `L` 页尾
	- `M` 页中
	- `zt` 将光标所在行移动到屏幕的顶端
	- `zb` 将光标所在行移动到屏幕的底部
	- `zz` 将光标所在行移动到屏幕的中间

* 行首行尾之间跳转
	* `^` 跳转到当前光标所在行的第一个非空字符
	* `0（数字）` 跳转到行首
	* `$` 跳转到行尾

* 行间移动
	- `#G` 跳转到第`#`行
	- 在命令扩展模式下，直接：`#` 跳转到对应的行
	- `G` 直接到最后一行
	- `gg` 跳转到第一行
	- `1G` 跳转到第一行

* 段落之间跳转（空行）
	- `{` 上一段
	- `}` 下一段

* 翻屏
	- `ctrl+f` 向文件尾部翻一屏
	- `ctrl+b` 向文件首部翻一屏
	- `ctrl+d` 向文件尾部翻半屏
	- `ctrl+u` 向文件首部翻半屏

### 3.9.6 命令模式编辑

* 字符编辑
	- `x` 删除光标所在处的字符
	- `#x` 删除#个字符
	- `xp` 将光标所在处的字符和后面的字符互换位置
	- `~` 将光标所在的位置大小写互换
	- `J` 删除当前行的换行符
	
* 替换
	* `r` 替换光标所在的字符
	* `R` 进入替换模式
	
* 删除
	* `d` 删除，与字符跳转配合使用
	* `d$` 删除到行尾
	* `d0` 删除到行首，当前位置不删除
	* `d^` 删除到非空字符
	* `dw` 删除一个单词
	* `de` 向后删除一个单词
	* `db` 向前删除一个单词
	* `dd` 删除整行
	* `#dd` 删除`#`行
	* `dG` 删除到结尾
	* `dgg` 删除到开头
	* `D = d$`: 删除到行尾
	
* 复制

	* `y` 复制, 与字符跳转配合使用
	* `y$`
	* `y0`
	* `y^`
	* `yw`
	* `ye`
	* `yb`
	* `yy` 复制一整行
	* `#yy` 复制`#`行
	* `yG` 复制到结尾
	* `ygg` 复制到开头
	* `Y` 复制整行

* 粘贴
	* `p` 如果是整行的话，则粘贴到当前光标所在行的下一行，
	  否则粘贴到光标的后面
	* `P` 如果是整行的话，则粘贴到当前光标所在行的上一行，
	  否则粘贴到光标的前面

* 改变, 删除以后并将模式切换成插入模式
	- `c` 可以跟光标的跳转做结合
	- `c$`
	- `c0`
	- `c^`
	- `cw`
	- `ce`
	- `cb`
	- `#command`
	- `cc` 删除正行并插入
	- `C` 相当于`c$`
		
* `#[i|I|a|A|o|O]string esc` 将string粘贴`#`次

* 搜索
	- `/pattern` 从当前光标往下搜索`pattern`
	- `?pattern` 从当前光标往上搜索`pattern`
	- `n` 同命令相同的方向
	- `N` 同命令相反的方向

* 撤销
	- `u` 撤销最近的修改
	- `# u` 撤销最近的`#`次修改
	- `ctrl + r` 撤销之前的动作
	- `.`  重复最后一次操作 
	- `#.` 最后一次操作重复执行`#`次

### 3.9.7 末行模式
* 地址定界
	* `:start,end`
	* `#`, 定位到`#`行
	* `#,#` 第`#`行到第`#`行
	* `#,+n` 第`#`开始，到`#+n`结束
	* `.` 当前光标所在行
	* `$` 最后一行
	* `$-n` 倒数`n+1`行
	* `%` 全文
	* `/part1/, /part2/` 从第一个`part1`匹配到第一个`part2`
	* `#, /part/` 从第`#`开始，到第一次`part`匹配到的地方
	* `/part/, $` 第一次匹配`part`到结尾
	
	* 配合使用的的命令
		* `d` 删除匹配内容
		* `y` 复制匹配内容
		* `w file`匹配内容另存为一个文件
		* `r file` 将文件内容写入匹配位置的下一行
	
* 查找并替换
	* 使用地址定界来查找
	* `s` 在扩展命令模式下使用为替换
		* `:s/npt/123` 将`npt`替换为`123`
	* 格式: `:地址定界s/查找内容/替换内容/装饰器`
		* 查找内容可以使用正则
		* 替换内容不能为正则
			* 可以为正则分组内容
	* 装饰器
		* `i` 忽略大小写
		* `g` 全部替换
		* `gc` 每次替换都询问
	* 分隔符
		* `#`: `:地址定界s#查找内容#替换内容#装饰器` 
		* `@`

### 3.9.8 可视化
* `v`: 面向字符
* `V`: 面向行
* `ctrl + v`: 面向块
* 可以结合跳转键使用
* 对突出显示部分可以使用删除、复制、变更、过滤、替换、另存为等等

### 3.9.9 多文件编辑

`vim file1 file2 file3 ...` 打开多个文件

* `:next` 下一个
* `:prev` 上一个
* `:first` 第一个
* `:last` 最后一个
* `qall` 退出全部
* `wall` 保存全部
* `wqall` 保存并退出全部
* `:xall` 保存并退出全部

### 3.9.10 使用多窗口
* `vim -o` 水平分隔
* `vim -O` 垂直分隔
* `ctrl + w + 上下左右箭头` 切换

#### 单文件
`ctrl+w,s` 水平切割

`ctrl+w,v` 垂直切割

`ctrl+w，q` 取消相邻的窗口

`ctrl+w，o` 取消全部窗口

## 3.10 vim工作特性
配置文件
- 全局有效：`/etc/vimrc`
- 对当前用户有效： `~/.vimrc`
- 行号：`set nu`  取消 `set nonu`
- 忽略大小写（搜索） `set ic` 取消`set noic`
- 自动缩进（同上一行） `set ai` 取消`set noai`
- 设置高亮显示（搜索到的内容） `set hls`  取消`set nohls`
- 语法高亮 `syntax on`  取消 `syntax off`
- 文件格式
  - `windows`格式: `set fileformat=dos`
  - `unix`: `set fileformat=unix`
- 添加标识线： `set cul` 取消标识线 `set nocul`
- 获取帮助： `set all`
- 获取帮助信息：
  - `:help`
  - `:help topic`
  - `vimtutor`



## 3.11 find命令，查找

是linux里面的一个实时查找工具，通过制定路径完成文件查找

`find [options] ..... [查找路径] [查找条件] [处理动作]`

* 查找路径: 查找的位置，默认是当前文件夹

* 查找条件：制定查找的标准，文件名、大小、类型、日期等等

* 处理动作：对符合条件的文件做什么操作，默认是输出到屏幕上

### 3.11.1 查找条件
- 根据文件名查找
	- `-name`  指定名称，可以使用正则
	  * `find /etc -name *.conf`
	- `-iname` 忽略大小写
	- `-links n` 引用次数为n的文件
	- `-regex` 后面跟完整路径，而不是文件名， 必须整个路径完全匹配

- 制定搜索的层级
	- `-maxdepth  level` 最大的搜索深度，指定的目录为第`1`层
	- `-mindepth level` 最小的搜索深度，包括`level`层

- 根据属主、属组来查找
	- `-user username` 查找属主为`username`的文件
	- `-group groupname` 查找属组为`groupname`的文件
	- `-uid id` 查找属主为`id`的文件
	- `-gid id` 查找属组为`id`的文件
	- `-nouser` 查找没有属主的文件
	- `-nogroup` 查找没有属组的文件

- 根据文件类型 `-type`
	- `d` 目录
	- `f` 文件
	- `l` 符号链接
	- `s` 套接字
	- `b` 块设备
	- `c` 字符设备
	- `p` 管道文件


- 空文件或者空目录
	- `-empty`
	
- 条件
    - 与 `-a`
	- 或 `-o`
	- 非 `-not`

- 排除目录
	- `-path #` 寻找`#`指定的目录，指定特殊操作`-prune`不打印
	- `find /etc -path /etc/ssh -prune -o -name *_config`
	- `find /etc -path /etc/sane.d -prune -o -name *_config`

- 按照大小来查找
	- `-size #` 表示`(#-1，#]` 不包括`#-1`，包括`#`
	- `-size -#` 表示`[0,#-1]` 包括`#-1`
	- `-size +#` 表示`(#,...)`

- 按照时间来查找
	- `-atime #` 表示`[#,#+1)` 
	- `-atime -#` 表示`(0，#)`
	- `-atime +#` 表示`[#+1,...]`
	- 查找7天以后的文件 `find -atime +7`
	- `-mtime`
	- `-ctime` 
	- 以分钟为单位
		- `-amin`
		- `-mmin`
		- `-cmin`

### 3.11.2 处理动作
- `-print` 默认的处理动作，显示在屏幕上
- `-ls` 类似于`ls -l`显示长格式
- `-delete` 删除查找到的文件
- `-fls file` 将查找的结果以长格式保存到文件中
- `-ok command {} \;` 对每一个查找到的文件执行`command`命令，在执行命令之前要先提示用户是否要执行
- `-exec command {} \;` 对查到的每一个文件执行`command`命令，不需要确认，一次性交给后面命令处理

### 3.11.3 xargs
- 有的命令不支持管道
- 命令参数过长
- `xargs` 将管道前面的内容一条一条的交给后面命令处理
- 一般会跟find使用

* `echo file{1..100000000} |xargs touch`

## 3.12 grep awk sed

### 3.12.1 grep过滤
`grep [option] "模式" file`

**option**
```
--color=auto 对匹配到的行添加颜色
-v 取反
-i 不区分大小写
-n 查找的内容增加行号
-c 打印匹配到的行数
-o 只显示匹配到的文字
-q 静默模式
-A # after 向下显示#行
-B # before 向上显示#行
—C # context 上下分别显示#行
-e 或者 grep -e 'user' -e 'root' passwd
-E 扩展正则表达式
-F 不使用正则表达式
-r 递归
-w 匹配整个单词
```

### 3.12.2 正则

- 字符匹配
	- `.` 任意单个字符
	- `[]` 匹配指定范围内的任意单个字符 `[0-9] [a-z] [A-Z]`
	- `[^]` 取反
	- `[:upper:]` 大写字母
	- `[:lower:]` 小写字母
	- `[:alnum:]` 字母和数字
	- `[:alpha:]` 大小写字母
	- `[:digit:]` 数字
	- `[:black:]` 空白
	- `[:punct:]` 标点符号

- 匹配次数

	- `*` 表示任意次数
	- `.*` 任意字符任意次数
	- `?` 表示0或者1次
	- `+` 至少一次
	- `{n}` 表示n次
	- `{m,n}` 最少m次，最多n次
	- `{n,}` 至少n次
	- `{,n}` 至多n次

- 位置锚定
	- `^` 开头
	- `$` 结尾
	- `^$` 空行
	```SHELL
	grep -v "^#" /etc/ssh/sshd_config |grep -v "^$" 显示不以#开头并且不是空行
	```

- 分组

	```SHELL
	grep "\(c\|C\)at" a
	```

- 向后引用

	- `\1` 前面第一个括号出现的内容**匹配完成**之后再后面在出现一次
	- `\2` 前面第二个括号出现的内容**匹配完成**之后再后面在出现一次
	- `\i` 前面第`i`个括号出现的内容**匹配完成**之后再后面在出现一次

- 扩展正则表达式
	- 与正则表达式的区别是不需要转义

## 3.13 压缩、解压、归档

### 3.13.1 gzip
* `gzip [option]... file` 压缩，压缩后删除源文件

	* **option**
		* `-c` 将压缩结果输出到屏幕，保留原来的文件
		    * `gzip -c passwd > passwd.gz`
		* `-1-9` 指定压缩比，默认9
	    * `-d` 解压
	
* `gunzip file` 解压

* `zcat file.gz` 不解压的情况下查看压缩比内的内容

### 3.13.2 bzip2
* `bzip [option] file` 压缩, 压缩后删除源文件
	* **option**
		* `-k` 保留原来的文件
		* `-d` 解压
		* `-1-9` 指定压缩比
	
* `bzcat file.bz2` 不解压的情况下查看压缩包的内容

### 3.13.3 xz
* `xz [option] file` 压缩文件，压缩后删除源文件
	* **option**
		* `-k` 保留原来的文件
		* `-d` 解压
		* `-1-9` 指定压缩比

* `xzcat file.xz`  不解压直接查看

### 3.13.4 zip
* `zip [option] zipfile` 压缩文件，解压到到当前路径
	* `-r` 递归压缩
	
* `unzip file.zip` 解压文件，解压到当前路径

### 3.13.5 tar 归档

* `tar [option] 归档文件名.tar 待归档的文件或目录`

	* `-c` 创建归档
	* `-v` 显示过程
	* `-f` 指定归档文件名
	* `-p` 带入原有属性
	* `-r` 追加
	*` -t` 查看归档文件内容
	* `-x` 解除归档
	  
	* 调用压缩工具进行压缩或解压
		* `-z` 使用`gzip`压缩
		* `-j` 使用`bzip2`压缩
		* `-J` 使用`xz`压缩
		
	* -`-exclude` 排除文件	

**实例**
```shell
tar -cpvf file.tar 目录或文件 #将文件或目录归档
tar -zvxf file.tar.gz -C 目录   # 解压file.tar.gz文件到指定目录
tar -jvxf file.tar.bz2 -C 目录  # 解压file.tar.bz2文件到指定目录
```

### 3.13.6 切割文件
```
split -b 指定大小 文件(只能为文件) 切割以后的名字
	
	-d 指定后缀为数字
	-a 指定后缀几位
	
cat 切割后的文件 > 新文件
```
```shell
split -b 2M file -d -a 3 file
```


