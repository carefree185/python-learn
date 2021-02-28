# nginx web服务

web服务 `apache` `iis`(Windows 提供web服务) `nginx`等

web框架应用框架 `django` `tornado` `flask`等

负载均衡 `lvs`章文嵩博士. 

`Tengine`(淘宝重写封装的nginx)

## 安装nginx

```shell
wget http://nginx.org/download/nginx-1.16.1.tar.gz  # 下载
tar xf nginx-1.16.1.tar.gz   # 解压

cd nginx-1.16.1

yum install gcc zlib2-devel pcre-devel openssl-devel  # 安装gcc工具

./configure --prefix=/opt/nginx --with-http_ssl_module --with-http_stub_status_module  # 配置
# --prefix(安装目录)  --with-http_ssl_module(支持443端口，支持https协议) --with-http_stub_status_module(查看nginx状态)
make && make install
```

## 目录结构
```
.
├── conf  配置文件
│   ├── fastcgi.conf
│   ├── fastcgi.conf.default
│   ├── fastcgi_params
│   ├── fastcgi_params.default
│   ├── koi-utf
│   ├── koi-win
│   ├── mime.types
│   ├── mime.types.default
│   ├── nginx.conf
│   ├── nginx.conf.default
│   ├── scgi_params
│   ├── scgi_params.default
│   ├── uwsgi_params
│   ├── uwsgi_params.default
│   └── win-utf
├── html  存放静态文件 index.html 是默认的欢迎页面
│   ├── 50x.html
│   └── index.html
├── logs  日志目录
└── sbin  二进制文件
    └── nginx
```

## 命令格式

```shell
./sbin/nginx -h
nginx version: nginx/1.16.1
Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

Options:
  -?,-h         : this help
  -v            : show version and exit 显示版本号
  -V            : show version and configure options then exit 显示版本+编译时选项
  -t            : test configuration and exit  测试配置文件
  -T            : test configuration, dump it and exit
  -q            : suppress non-error messages during configuration testing
  -s signal     : send signal to a master process: stop, quit, reopen, reload 信号
  -p prefix     : set prefix path (default: /opt/nginx/)
  -c filename   : set configuration file (default: conf/nginx.conf)  配置文件
  -g directives : set global directives out of configuration file
```

## 配置文件
```shell
#user  nobody;  # 使用那个用户启动子进程
worker_processes  1;  # 工作进程的个数 一般配置为cpu的核心数-1
# cpu亲缘性绑定，让nginx的子进程工作在哪个核心上
# 错误日志
#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;  # 启动时生成的pid文件


events {
  	# user [epoll|poll|select]
    worker_connections  1024;  # 每一个子进程可以处理的最大链接个数
}


http {
    include       mime.types;   # 导入
    default_type  application/octet-stream; # 默认的请求方式
	
	# 定义日志格式
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
	
	# 定义日志并定义日志格式
    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;  # 长连接的超时时间

    #gzip  on;

    server {
        listen       80;  # 监听的端口
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;  # 指定静态文件指定
            index  index.html index.htm;  # 指定默认的index页面
        }

        #error_page  404              /404.html;  # 找不到的资源，错误页面

        # redirect server error pages to the static page /50x.html
        #
        
        # 服务端错误页面
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}
}
```

启动以后会生成一个主进程，根据配置文件的选项来生成子进程（工作进程），
主进程不负责处理用户的请求，用来转发用户的请求，真正负责处理用户请求的是子进程

## 404页面
```
error_page  404              /404.html;
```

## root与alias
```shell
location /img {
  root /data/img;
}
# root /data/img 里面必须有/img目录

location /img {
  alias /data/img;
}
# alias /data/img 里面不需要有 /img目录
```

## 域名
```shell
server_name ms.s22.com  # 设置域名
```

## 多域名
```shell
server  {
    listen 80;
    server_name www.taobao.com taobao.com;
    location / {
        root /data/taobao;
        index index.html;
    }
}

server  {
    listen 80;
    server_name www.jd.com jd.com;
    location / {
        root /data/jd;
        index index.html;
    }
}
```

## 默认server
以ip地址访问默认的server
```shell
listen 80 default_server;
```

