# urllib与urllib3的介绍
`urllib`是`Python`中请求`url`连接的官方标准库，在`Python2`中主要为`urllib`
和`urllib2`，在`Python3`中整合成了`urllib`。

官方文档链接为：https://docs.python.org/3/library/urllib.html

而`urllib3`则是增加了连接池等功能，两者互相都有补充的部分。

## urllib库详细

它是 `Python` 内置的 `HTTP` 请求库，也就是说我们不需要额外安装即可使用，基本上涵盖了基础的网络请求功能，它包含四个模块：

* `urllib.request` 用于打开和读取`url`
* `urllib.error` 用于处理前面`request`引起的异常
* `urllib.parse` 用于解析`url`
* `urllib.robotparser` 用于解析`robots.txt`文件



### urllib.request
`urllib`中，`request`这个模块主要负责构造和发起网络请求，
并在其中加入`Headers`、`Proxy`等。

利用它可以模拟浏览器的一个请求发起过程

#### 发起GET请求
主要使用`urlopen()`方法来发起请求
```python
from urllib import request

resp = request.urlopen('http://www.baidu.com')
print(resp.read().decode())
```
在`urlopen()`方法中传入字符串格式的`url`地址，则此方法会访问目标网址，然后返回访问的结果。

访问的结果会是一个`http.client.HTTPResponse`对象，使用此对象的`read()`方法，
则可以获取访问网页获得的数据。但是要注意的是，获得的数据会是`bytes`的二进制格式，
所以需要`decode()`一下，转换成字符串格式。
> * `urlopen`方法返回的是一个`http.client.HTTPResponse`对象
> * 需要使用该对象的`read`方法来获取**二进制数据**

#### 发起POST请求
`urlopen()`方法默认发起的是`get`请求，当在`urlopen()`方法中传入`data`参数时，则会发起`POST`请求

```python
from urllib import request

resp = request.urlopen('http://httpbin.org/post', data=b'word=hello')
print(resp.read().decode())
```
**data参数传递时必须是bytes格式**的数据

#### 请求操作
发起请求时，可以设置超时时间，避免程序一直卡在等待响应位置。

设置超时时间(给`urlopen`指定参数`timeout`即可)，单位为秒，如果请求时间超出还没有得到响应，那么就会抛出`URLError`异常

```python
from urllib import request

response = request.urlopen('http://httpbin.org/get', timeout=0.1)
```

### Request对象构造
`urlopen()`方法可以实现最基本请求，但这几个简单的参数并不足以构建一个完整的请求，
如果请求中需要加入 `Headers` 等信息，我们就可以利用更强大的`Request`对象来扩展功能，
`Request`对象如下所示
```
class urllib.request.Request(url, data=None, headers={},
						   origin_req_host=None,
						   unverifiable=False, method=None)
```
构造`Request`对象**必须传入**`url`参数，`data`数据和`headers`都是可选的。

最后，`Request`方法可以使用`method`参数来自由选择请求的方法，
如`PUT`，`DELETE`等等，默认为`GET`。


#### 添加Headers信息
通过`urllib`发起的请求会有默认的一个`Headers："User-Agent":"Python-urllib/3.6"`，
指明请求是由`urllib`发起的。

所以遇到一些验证`User-Agent`的网站时，数据将不能够获得，所以我们需要自定义`Headers`，
而这需要借助于`urllib.request`中的`Request`类
```python
from urllib import request

url = 'http://httpbin.org/get'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

# 需要使用url和headers生成一个Request对象，然后将其传入urlopen方法中
req = request.Request(url, headers=headers)
resp = request.urlopen(req)
print(resp.read().decode())
```

#### 添加Cookies

为了在请求时能带上`Cookie`信息，我们需要重新构造一个`opener`。

使用`request.build_opener`方法来进行构造`opener`，
将我们想要传递的`cookie`配置到`opener`中，然后使用这个`opener`的`open`方法来发起请求。

需要先行构造一个`CookieJar`对象
```python
from http import cookiejar
from urllib import request

url = 'http://httpbin.org/cookies'
# 创建一个cookiejar对象
cookie = cookiejar.CookieJar()
# 使用HTTPCookieProcessor创建cookie处理器
cookies = request.HTTPCookieProcessor(cookie)
# 并以它为参数创建Opener对象
opener = request.build_opener(cookies)
# 使用这个opener来发起请求
resp = opener.open(url)
print(resp.read().decode())
```

或者也可以把这个生成的`opener`使用`install_opener`方法来设置为全局的。
则之后使用`urlopen`方法发起请求时，都会带上这个`cookie`。
```
# 将这个opener设置为全局的opener
request.install_opener(opener)
resp = request.urlopen(url)
```

#### 设置Proxy代理
使用爬虫来爬取数据的时候，常常需要使用代理来隐藏我们的真实`IP`。或者防止被网站的频率给限制

```python
from urllib import request

url = 'http://httpbin.org/ip'
proxy = {'http':'50.233.137.33:80','https':'50.233.137.33:80'}
# 创建代理处理器
proxies = request.ProxyHandler(proxy)
# 创建opener对象
opener = request.build_opener(proxies)

resp = opener.open(url)
print(resp.read().decode())
```
* 先创建`ProxyHandler`对象
* 再构造`opener`对象


### 下载数据到本地
在我们进行网络请求时常常需要保存图片或音频等数据到本地，一种方法是使用python的文件操作，
将`read()`获取的数据保存到文件中。

而`urllib`提供了一个`urlretrieve()`方法，可以简单的直接将请求获取的数据保存成文件。
```python
from urllib import request

url = 'http://python.org/'
request.urlretrieve(url, 'python.html')
```
`urlretrieve()`方法传入的第二个参数为文件保存的位置，以及文件名。

注：**`urlretrieve()`方法是python2直接移植过来的方法，以后有可能在某个版本中弃用**。

### urllib.response

在使用`urlopen()`方法或者`opener`的`open()`方法发起请求后，
获得的结果是一个`response`对象。

这个对象有一些方法和属性，可以让我们对请求返回的结果进行一些处理。

* read()

    获取响应返回的数据，只能使用一次。

* getcode()

    获取服务器返回的状态码。

* getheaders()

    获取返回响应的响应报头。

* geturl()

    获取访问的url。

### urllib.parse

#### urllib.parse.quote
在url中，是只能使用ASCII中包含的字符的，也就是说，ASCII不包含的特殊字符，以及中文等字符都是不可以在url中使用的。而我们有时候又有将中文字符加入到url中的需求，例如百度的搜索地址：
```
https://www.baidu.com/s?wd=南北
```
`?`之后的`wd`参数，则是我们搜索的关键词。那么我们实现的方法就是将特殊字符进行`url`编码，
转换成可以`url`可以传输的格式，`urllib`中可以使用`quote()`方法来实现这个功能。
```python
from urllib import parse
keyword = '南北'
parse.quote(keyword)  # '%E5%8D%97%E5%8C%97'
```
如果需要将编码后的数据转换回来，可以使用`unquote()`方法
```python
from urllib import parse
parse.unquote('%E5%8D%97%E5%8C%97')  # '南北'
```

#### urllib.parse.urlencode
在访问`url`时，我们常常需要传递很多的`url`参数，而如果用字符串的方法去拼接`url`的话，
会比较麻烦，所以`urllib`中提供了`urlencode`这个方法来拼接`url`参数。
```ipython
>>> from urllib import parse
>>> params = {'wd': '南北', 'code': '1', 'height': '188'}
>>> parse.urlencode(params)
'wd=%E5%8D%97%E5%8C%97&code=1&height=188'
```

### urllib.error
在`urllib`中主要设置了两个异常，一个是`URLError`，一个是`HTTPError`，
`HTTPError`是`URLError`的子类。

`HTTPError`还包含了三个属性：
* `code`：请求的状态码
* `reason`：错误的原因
* `headers`：响应的报头

## urllib3

Urllib3是一个功能强大，条理清晰，用于HTTP客户端的Python库。许多Python的原生系统已经开始使用urllib3。Urllib3提供了很多python标准库urllib里所没有的重要特性：

1. 线程安全
2. 连接池
3. 客户端SSL/TLS验证
4. 文件分部编码上传
5. 协助处理重复请求和HTTP重定位
6. 支持压缩编码
7. 支持HTTP和SOCKS代理



### 安装

urllib3是一个第三方库，安装非常简单，pip安装即可：

```shell
pip install urllib3
```



### 使用

`urllib3`主要使用连接池进行网络请求的访问，所以访问之前我们需要创建一个连接池对象，如下所示：

```shell
>>> import urllib3
>>> http = urllib3.PoolManager()
>>> r = http.request('GET', 'http://httpbin.org/robots.txt')
>>> r.status
200
>>> r.data
'User-agent: *\nDisallow: /deny\n'
```

#### 2.2.1 设置headers

```shell
headers={'X-Something': 'value'}
resp = http.request('GET', 'http://httpbin.org/headers', headers=headers)
```

#### 2.2.2 设置url参数

对于GET等没有请求正文的请求方法，可以简单的通过设置`fields`参数来设置url参数。

```shell
fields = {'arg': 'value'}
resp = http.request('GET', 'http://httpbin.org/get', fields=fields)
```

如果使用的是POST等方法，则会将fields作为请求的请求正文发送。

所以，如果你的POST请求是需要url参数的话，那么需要自己对url进行拼接。

```shell
fields = {'arg': 'value'}
resp = http.request('POST', 'http://httpbin.org/get', fields=fields)
```

#### 2.2.3 设置代理

```shell
>>> import urllib3
>>> proxy = urllib3.ProxyManager('http://50.233.137.33:80', headers={'connection': 'keep-alive'})
>>> resp = proxy.request('get', 'http://httpbin.org/ip')
>>> resp.status
200
>>> resp.data
b'{"origin":"50.233.136.254"}\n'
```

**注：`urllib3`中没有直接设置cookies的方法和参数，只能将cookies设置到headers中**

