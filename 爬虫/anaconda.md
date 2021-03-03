# conda
## 安装
### linux
```shell
bash Anaconda3-2020.11-Linux-x86_64.sh
```

### windows

双击`Anaconda3-2020.11-Windows-x86_64.exe`。将`conda`添加到环境变量

## 升级
```shell
conda update conda          #基本升级
conda update anaconda       #大的升级
conda update anaconda-navigator    //update最新版本的anaconda-navigator 
```

## conda环境使用基本命令
* `conda update -n base conda`: 更新最新版本的conda

* `conda create -n env_name python=version`: 指定python版本创建虚拟环境

* `conda activate env_name`: 激活虚拟环境

* `conda deactivate`: 退出虚拟环境

* `conda env list`: 查看所有的虚拟环境

* `conda info --envs`: 显示所有的虚拟环境

## 查看指定包可安装版本信息命令

* `anaconda search -t conda package`: 查看`package`各个版本

* `anaconda show <USER/PACKAGE>`: 查看指定包可安装版本信息，输出结果会提供一个下载地址url

* `conda install --channel url package=version`: 下载包

## 更新，卸载安装包
* `conda list`: 查看已经安装的文件包
* `conda list  -n env_name`: 指定查看env_name虚拟环境下安装的package
* `conda update package`: 更新package文件包
* `conda uninstall package`: 卸载package文件包

## 删除虚拟环境

* `conda remove -n env_name --all`

## 清理（conda瘦身）
* `conda clean -p`: 删除没有用的包
* `conda clean -t`: 删除tar包
* `conda clean -y --all`: 删除所有的安装包及cache

## 复制/重命名/删除env环境
Conda是没有重命名环境的功能的, 要实现这个基本需求, 只能通过愚蠢的克隆-删除的过程。
切记不要直接mv移动环境的文件夹来重命名, 会导致一系列无法想象的错误的发生
```shell
# 克隆oldname环境为newname环境
conda create --name newEnvName --clone oldEnvName 
# 彻底删除旧环境
conda remove --name oldEnvName --all
```

## conda自动开启/关闭激活

* `conda activate`: 默认激活base环境
* `conda activate env_name`: 激活env_name环境
* `conda deactivate`: 关闭当前环境
* `conda config --set auto_activate_base false`: 关闭自动激活状态
* `conda config --set auto_activate_base true`: 开启自动激活状态

## conda安装本地包
```shell
#pip 安装本地包
pip install ~/Downloads/a.whl
#conda 安装本地包
conda install --use-local  ~/Downloads/a.tar.bz2
```

## 解决conda/pip install 下载速度慢

### conda数据源管理

* Windows
	```shell
	#显示目前conda的数据源有哪些
	conda config --show channels
	#添加数据源：例如, 添加清华anaconda镜像：
	conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
	conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
	conda config --set show_channel_urls yes
	#删除数据源
	conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
	```
* linux, 修改`~/.condarc`
	```yaml
	auto_activate_base: false
	channels:
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
	show_channel_urls: true
	```

### pip数据源管理
```shell
#显示目前pip的数据源有哪些
pip config list
pip config list --[user|global] # 列出用户|全局的设置
pip config get global.index-url # 得到这key对应的value 如：https://mirrors.aliyun.com/pypi/simple/

# 添加
pip config set key value
#添加数据源：例如, 添加USTC中科大的源：
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
#添加全局使用该数据源
pip config set global.trusted-host https://mirrors.ustc.edu.cn/pypi/web/simple

# 删除
pip config unset key
# 例如
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

#搜索
pip search flask  #搜素flask安装包

# 升级pip
pip install pip -U
```

**常用源**
```shell
阿里云                    http://mirrors.aliyun.com/pypi/simple/
中国科技大学         https://pypi.mirrors.ustc.edu.cn/simple/ 
豆瓣(douban)         http://pypi.douban.com/simple/ 
清华大学                https://pypi.tuna.tsinghua.edu.cn/simple/
中国科学技术大学  http://pypi.mirrors.ustc.edu.cn/simple/
```

**pip常用命令**

```shell
pip list # 列出当前缓存的包
pip purge # 清除缓存
pip remove # 删除对应的缓存
pip help # 帮助
pip install package # 安装package包
pip uninstall package # 删除package包
pip show package # 展示指定的已安装的package包
pip check package # 检查package包的依赖是否合适
```

## pip和conda批量导出、安装组件(requirements.txt)

### pip
* 导出依赖包到requirements.txt
	```shell
	pip freeze > requirements.txt
	```
* 安装requirements.txt文件中包含的组件依赖
	```shell
	pip install -r requirements.txt
	```

### conda

* 导出依赖包到requirements.txt
	```shell
	conda list -e > requirements.txt
	```
* 安装requirements.txt文件中包含的组件依赖
	```shell
	conda install --yes --file requirements.txt
	```

## jupyter notebook默认工作目录设置
* `jupyter notebook --generate-config`: 创建jupyter的配置文件`jupyter_notebook_config.py`

* 修改, 打开`jupyter_notebook_config.py`修改
	```shell
	c.NotebookApp.notebook_dir = 'E:\\tf_models'     //修改到自定义文件夹
	```


