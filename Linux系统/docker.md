如何保持环境一致？

`pip3 freeze > requerment.txt`

`pip install -r requerment.txt`

1. 环境不一致

2. 配置文件不一致

3. 技术水平不一致，导致部署环境快慢不一致

# Docker容器
Docker是一个虚拟环境容器，可以将你的开发环境、代码、配置文件等一并打包到这个容器中，
并发布和应用到任意平台中。比如，你在本地用Python开发网站后台，开发测试完成后，
就可以将Python3及其依赖包、Flask及其各种插件、Mysql、Nginx等打包到一个容器中，
然后部署到任意你想部署到的环境。

- 一处编译，到处运行
- 对系统的消耗不是特别的多
- 可以快速启动
- 维护简单
- 扩展容易
- 基于`namespace`和`cgroup`技术实现

## 镜像(Image)
类似于虚拟机中的镜像，是一个包含有文件系统的面向`Docker`引擎的只读模板。
任何应用程序运行都需要环境，而镜像就是用来提供这种运行环境的。
例如一个`Ubuntu`镜像就是一个包含`Ubuntu`操作系统环境的模板，
同理在该镜像上装上`Apache`软件，就可以称为`Apache`镜像。

**可以理解为操作系统地iso镜像**

## 容器(Container)
类似于一个**轻量级的沙盒**，可以将其看作一个极简的`Linux`系统环境（包括root权限、进程空间、用户空间和网络空间等），
以及运行在其中的应用程序。`Docker`引擎利用容器来**运行、隔离**各个应用。**容器是镜像创建的应用实例**，可以**创建、启动、停止、删除**容器，
各个容器之间是是 **相互隔离** 的，互不影响。

注意：**镜像本身是只读的，容器从镜像启动时，Docker在镜像的上层创建一个可写层，镜像本身不变**。

## 仓库(Repository)
类似于**代码仓库**，这里是**镜像仓库**，是Docker用来**集中存放镜像文件**的地方。
注意与注册服务器（Registry）的区别：**注册服务器是存放仓库的地方，一般会有多个仓库**；
而**仓库是存放镜像的地方**，一般每个仓库存放一类镜像，每个镜像利用`tag`进行区分，
比如Ubuntu仓库存放有多个版本（12.04、14.04等）的Ubuntu镜像

**私有的仓库**

**公共的仓库**：[docker hub](https://hub.docker.com/)


## 安装docker
`docker-ce`: 社区版

`docker-ee`: 商业版

使用阿里源，参考地址: https://developer.aliyun.com/mirror/docker-ce?spm=a2c6h.13651102.0.0.3e221b11feIrMf

### ubuntu安装
```shell
# step 1: 安装必要的一些系统工具
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: 安装GPG证书
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: 写入软件源信息
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
# Step 4: 更新并安装Docker-CE
sudo apt-get -y update
sudo apt-get -y install docker-ce

# 安装指定版本的Docker-CE:
# Step 1: 查找Docker-CE的版本:
# apt-cache madison docker-ce
#   docker-ce | 17.03.1~ce-0~ubuntu-xenial | https://mirrors.aliyun.com/docker-ce/linux/ubuntu xenial/stable amd64 Packages
#   docker-ce | 17.03.0~ce-0~ubuntu-xenial | https://mirrors.aliyun.com/docker-ce/linux/ubuntu xenial/stable amd64 Packages
# Step 2: 安装指定版本的Docker-CE: (VERSION例如上面的17.03.1~ce-0~ubuntu-xenial)
# sudo apt-get -y install docker-ce=[VERSION]
```

### centos安装
```shell
# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
# Step 2: 添加软件源信息
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# Step 3
sudo sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
# Step 4: 更新并安装Docker-CE
sudo yum makecache fast
sudo yum -y install docker-ce
# Step 4: 开启Docker服务
sudo service docker start

# 注意：
# 官方软件源默认启用了最新的软件，您可以通过编辑软件源的方式获取各个版本的软件包。例如官方并没有将测试版本的软件源置为可用，您可以通过以下方式开启。同理可以开启各种测试版本等。
# vim /etc/yum.repos.d/docker-ce.repo
#   将[docker-ce-test]下方的enabled=0修改为enabled=1
#
# 安装指定版本的Docker-CE:
# Step 1: 查找Docker-CE的版本:
# yum list docker-ce.x86_64 --showduplicates | sort -r
#   Loading mirror speeds from cached hostfile
#   Loaded plugins: branch, fastestmirror, langpacks
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            docker-ce-stable
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            @docker-ce-stable
#   docker-ce.x86_64            17.03.0.ce-1.el7.centos            docker-ce-stable
#   Available Packages
# Step2: 安装指定版本的Docker-CE: (VERSION例如上面的17.03.0.ce.1-1.el7.centos)
# sudo yum -y install docker-ce-[VERSION]
```

### 配置docker加速

在`/etc/docker/daemon.json`文件中写入如下内容
```shell
{
    "registry-mirrors": [
        "https://1nj0zren.mirror.aliyuncs.com",
        "https://docker.mirrors.ustc.edu.cn",
        "http://f1361db2.m.daocloud.io",
        "https://registry.docker-cn.com"
    ]
}
```
保存退出后，执行如下命令
```shell
systemctl daemon-reload 
systemctl restart docker
```

## docker命令

* `docker run hello-world`: 运行镜像

* `docker search image-name`: 搜索镜像

* `docker images [image-name]`: 查看本地镜像
	* `docker` 镜像是分层的。
	
* `docker image ls`: 查看本地镜像

* `docker image ls --format "table {{.ID}}:{{.Tag}}"`: 查看镜像部分信息

* `docker rmi name|id`: 删除镜像

* `docker rmi `docker images` -q`: 删除全部镜像

* `docker run 镜像名称`: 启动镜像
	* 先查找本地是否存在镜像
	* 如果不存在则去下载镜像
	* 下载以后再启动
	* 容器启动以后**在原来的镜像基础上在新建一层**

* 查看容器
	```shell
	docker ps  #默认查询是运行中的容器
	-a 查看所有的
	-q 只查看容器的id
	```

* 容器执行命令
	```shell
	docker run centos /bin/echo 'hongxu'
	```

* 启动并进入镜像
	```shell
	docker run -ti centos /bin/bash
	```
    先查找本地，如果本地存在则启动；如果本地不存在，则下载，完成后在启动。
 
	* `-t` 创建一个虚拟终端
	* `-i` 将容器的标准输入保持打开
	* `--name` 指定名字
	* `-d` 后台运行
	* `—P` 将容器的端口暴露在宿主机的随机端口上
	* `-p` 宿主机端口:容器端口
	* `-v` 宿主机目录:容器指定目录（可以实现将宿主机目录挂载到容器中）

* 退出镜像
	```shell
	exit
	ctrl + d 
	```

* 制作镜像
	```shell
	docker commit -m "信息" 名字:tag
	```

* 导出镜像
	```shell
	docker save -o mycentos.tar.gz mycentos
	docker save mycentos > mycentos.tar.gz 
	```

* 删除容器
	```shell
	docker rm  id# 默认只能删除未运行的容器
	```
	* `-f` 强制删除

* 导入镜像
	```shell
	docker load -i mycentos.tar.gz
	docker load < mycentos.tar.gz 
	```

**补充linux命令**: `scp`: `linux`之间互相传递文件

* `docker port name|id`: 查看docker容器端口与宿主机端口的映射关系
	
* `docker stop 容器id或者容器名称`: 关闭容器

* `docker start  容器id或者容器名称`: 启动容器

* `docker stats  容器id或者容器名称`: 获取容器的运行状态(监控容器)

* 查看日志
	```shell
	docker logs  容器id或者容器名称
	-f 实时输出
	```

* `docker exec -ti  容器id或者容器名称 /bin/bash`: 进入容器

* `docker container prune`: 移除所有停止状态的容器


## Dockerfile文件
```shell
FROM 镜像名称
RUN 命令
```


