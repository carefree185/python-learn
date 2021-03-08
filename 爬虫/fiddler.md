
移动端数据的爬取
- fiddler是一款抓包工具：代理服务器
    - 青花瓷，miteproxy

    - 配置：让其可以抓取https协议的请求
    - tools-》options-》https-》安装证书
- http：客户端和服务器端进行数据交互的某种形式
- https：安全的http协议
- https的加密方式采用的是证书密钥加密。

- 1.配置下fiddler的端口
- 2.将手机和fiddler所在的电脑处在同一个网段下（pc开启wifi，手机连接）
- 3.在手机中访问fiddler的ip+port：192.168.14.110:50816,在当前页面中点击对应的连接下载证书
- 4.在手机中安装且信任证书
- 5.设置手机网络的代理：开启代理==》fiddler对应pc端的ip地址和fiddler自己端口号

