# 虚拟环境

## 安装
```shell
pip3 install virtualenv -i https://pypi.douban.com/simple
```

## 创建虚拟环境
```shell
virtualenv --no-site-packages django11 
--no-site-packages 创建一个全新的python环境
--python 指定以哪个python来创建虚拟环境
```

## 激活虚拟环境
```shell
source envdir/bin/activate 
```

## 退出虚拟环境
```shell
deactivate
```

## 确保环境一致
```shell
在windows上执行如下命令
将windows上安装的包做快照
pip freeze > requirement.txt
将requirement.txt发送到linux上
切换虚拟机
pip install -r requirement.txt -i https://pypi.douban.com/simple
```

## virtualenvwrapper

1. 安装
	```shell
	pip3 install virtualenvwrapper -i https://pypi.douban.com/simple
	```
2.修改文件
	```shell
	vim ~/.bashrc
	export WORKON_HOME=/envdir  
	export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'   
	export VIRTUALENVWRAPPER_PYTHON=/opt/python36/bin/python3      
	source /opt/python36/bin/virtualenvwrapper.sh
	``` 
3. 加载`~/.bashrc`

	```shell
	source ~/.bashrc
	```

4.创建环境
	```shell
	mkvirtualenv django11 创建并切换
	```
5.进入虚拟环境
	```shell
	workon name
	```

6.切换到当前虚拟环境的文件夹
	```shell
	cdvirtualenv
	```

7.切换到当前虚拟环境的第三方包的文件夹
	```shell
	cdsitepackages
	```

8.退出
	```shell
	deactivate
	```

9.列出当前管理的虚拟环境
	```shell
	lsvirtualenv
	```

10.列出当前虚拟环境的第三方包
	```shell
	lssitepackages
	```

11.删除虚拟环境
	```shell
	rmvirtualenv 必须要退出才能删除
	```

