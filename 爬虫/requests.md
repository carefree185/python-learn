# requests

## 简介
`Requests` 唯一的一个非转基因的 `Python HTTP` 库，人类可以安全享用。

`Requests` 是以 PEP 20 的箴言为中心开发的

## 安装

1. pip方式安装
    ```shell
    pip install requests
    ```
2. 源码安装
    ```shell
    # 1. 下载源码
    git clone git://github.com/kennethreitz/requests.git

    # 2. 安装
    cd requests
    pip install .
    ```

## 快速上手

### 发送请求
`requests`模块发送请求的`api`十分简单。

#### 请求方法
每个请求方式就对应一个请求方法，例如：发送`get`请求只需要调用`requests`
的`get`方法即可。具体调用形式
```python
import requests
response = requests.get('url', 'params')
```

发送`post`请求只需要调用`rquests`的`post`方法即可
```python
import requests
requests.post('http://httpbin.org/post', data = {'key':'value'})
```

而其他的请求类型，都有各自对应的方法
```python
import requests
resp1 = requests.put('http://httpbin.org/put', data = {'key':'value'})
resp2 = requests.delete('http://httpbin.org/delete')
resp3 = requests.head('http://httpbin.org/get')
resp4 = requests.options('http://httpbin.org/get')
```

### 传递参数
请求不可免除的是参数的携带，`http`携带参数有下面两种形式
#### 在`url`中携带参数
以`?key1=value1&key2=value2...`的形式携带参数，在requests模块
中只需要将这些参数组织为一个字典，传递给`params`参数即可。`requests`
中不建议拼接`url`

**例如**
```python
import requests
params = {'key1': 'value1', 'key2': 'value2'}
response = requests.get("http://httpbin.org/get", params=params)
```
`params`: 就是需要`url`携带的参数

当遇到一个键有多个值的参数，只需要将值放在一个列表中
```python
import requests
params = {'key1': 'value1', 'key2': ['value2', 'value3']}
response = requests.get('http://httpbin.org/get', params=params)
```

#### 在`body`中携带参数
对于`post`、`put`等需要在请求体中携带参数的请求方式，也只需要将参数构造成字典
传递给`data`参数即可

```python
import requests
resp = requests.post('http://httpbin.org/post', data = {'key':'value'})
```

### response对象

发送请求后返回的数据被`requests`模块封装到了response对象中。
操作`response`对象,就可以获取到相关数据。

#### 获取响应文本数据
请求响应的数据可以通过`response.text`属性来获得。
```python
import requests
resp = requests.get('https://api.github.com/events')
print(resp.text)  # u'[{"repository":{"open_issues":0,"url":"https://github.com/...'
```
#### 响应数据的编码
`Requests` 会根据会自动的根据响应的报头来猜测网页的编码是什么，
然后根据猜测的编码来解码网页内容，基本上大部分的网页都能够正确的被解码。
而如果发现`text`解码不正确的时候，就需要我们自己手动的去指定解码的编码格式

可以通过`response.encoding`来查看或指定编码。指定编码后，再次调用`response.text`
就会根据新指定的`encoding`来解码响应内容
```python
import requests

resp = requests.get('https://api.github.com/events')
resp.encoding = 'utf-8'
print(resp.text)  # u'[{"repository":{"open_issues":0,"url":"https://github.com/...'
```

在你需要的情况下，`Requests` 也可以使用定制的编码。
如果你创建了自己的编码，并使用 `codecs` 模块进行注册，
你就可以轻松地使用这个解码器名称作为 `r.encoding 的值`，
然后由 `Requests` 来为你处理编码。

#### 获取响应二进制数据
`response`对象中还保存了响应数据的二进制信息，可以通过`response.content`
来获取

```python
import requests

resp = requests.get('https://api.github.com/events')
print(resp.content)  # b'[{"repository":{"open_issues":0,"url":"https://github.com/...'
```

#### JSON响应内容
`Requests`请求的响应对象`response`内置带有一个`json`解析器，只需要调用
`response.json()`方法就可以获得`json`格式的响应数据。
```python
import requests

r = requests.get('https://api.github.com/events')
print(r.json())  # [{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...'
```
如果 `JSON` 解码失败， `r.json()` 就会抛出一个异常。然而，并不是解码成功
就意味着响应成功。有的服务器会在失败的响应中包含一个 `JSON` 对象（比如 `HTTP 500` 的错误细节）。
这种 `JSON` 会被解码返回。要检查请求是否成功，
请使用 `r.raise_for_status()` 或者检查 `r.status_code` 是否和你的期望相同

#### 原始响应内容
`requests`请求的响应对象`response`中包含了来自服务器的原始套接字响应
被封装到了`response.raw`对象中。想要获取原始响应内容，则需要在发送请求时指定
`stream=True`, 调用`response.raw.read()`来读取内容

```python
import requests
r = requests.get('https://api.github.com/events', stream=True)
print(r.raw)  # <requests.packages.urllib3.response.HTTPResponse object at 0x101194810>
print(r.raw.read(10))  # '\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'
```

如果响应数据两过大，可以使用`response.iter_content`获取
```python
import requests
r = requests.get('https://api.github.com/events', stream=True)
with open('filename', 'wb') as fd:
    for chunk in r.iter_content('size'):
        fd.write(chunk)
```

### 常见反爬策略解决方式

#### 请求载体标识 `User-Agent`
目标网站一般都会检查发起请求的载体是由什么软件发起的。根本依据就是请求
头`headers`中`User-Agent`参数。只需要在请求头中指定该参数就可以越过服务器的检测
```python
import requests
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}  # 定制请求头信息
r = requests.get(url, headers=headers)
```
> **注意**: 定制 header 的优先级低于某些特定的信息源
> * 如果在 `.netrc` 中设置了用户认证信息，使用 `headers=` 设置的授权就不会生效。
> 而如果设置了 `auth= 参数`，`.netrc` 的设置就无效了。
> * 如果被重定向到别的主机，授权 header 就会被删除
> * 代理授权 `header` 会被 `URL` 中提供的代理身份覆盖掉
> * 在我们能判断内容长度的情况下，`header` 的 `Content-Length` 会被改写

**`Requests` 不会基于定制 `header` 的具体情况改变自己的行为**
只不过在最后的请求中，所有的 `header` 信息都会被传递进去

> 所有的 `header` 值必须是 `string`、`bytestring` 或者 `unicode`。
> 尽管传递 `unicode header` 也是允许的，但不建议这样做

#### ip频率检测
对于检测访问`ip`频率的接口，需要设置`ip`代理，来规避网站的检测，只需要将`ip`
代理组织成一个字典，传递到`proxies`参数中即可
```python
import requests

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}

requests.get('http://example.org', proxies=proxies)
```

#### 登录检测
对于需要登录才能访问的数据而言，可以指定`cookies`来模拟登录，解决登录
限制问题；也可使用`session`来实现长会话，也即是持久登录。

##### cookies
在`requests`中，`cookies`的使用只需要将`cookies`的字典传递给参数
`cookies`即可
```python
import requests
url = 'http://httpbin.org/cookies'
cookies = {'cookies_are': 'working'}
resp = requests.get(url, cookies=cookies)
print(resp.text)  # '{"cookies": {"cookies_are": "working"}}'
```

#### session
在`Requests`中，实现了`Session()`会话功能，当我们使用`Session`时，
能够像浏览器一样，在没有关闭关闭浏览器时，能够保持住访问的状态。

这个功能常常被我们用于登陆之后的数据获取，使我们不用再一次又一次的传递`cookies`。
```python
import requests

session = requests.Session()

session.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
resp = session.get('http://httpbin.org/cookies')

print(resp.text)  # '{"cookies": {"sessioncookie": "123456789"}}'
```
首先我们需要去生成一个`Session`对象，然后用这个`Session`对象来发起访问，
发起访问的方法与正常的请求是一摸一样的。

同时，需要注意的是，如果是我们在`get()`方法中传入`headers`和`cookies`等数据，
那么这些数据只在当前这一次请求中有效。
如果你想要让一个`headers`在`Session`的整个生命周期内都有效的话，
需要用以下的方式来进行设置：
```python
import requests

session = requests.Session()
# 设置整个headers
session.headers = {
    'user-agent': 'my-app/0.0.1'
}
# 增加一条headers
session.headers.update({'x-test': 'true'})
```

### post请求详细

#### data参数编码

##### urlencoded
对于`urlencoded`编码的`data`参数只需要将数据组织成一个字典或者一个嵌套元组
的形式就可以完成。
```
>>> import request
>>> payload = {'key1': 'value1', 'key2': 'value2'}

>>> r = requests.post("http://httpbin.org/post", data=payload)
>>> print(r.text)
{
  ...
  "form": {
    "key2": "value2",
    "key1": "value1"
  },
  ...
}
```
或者
```
>>> import request
>>> payload = (('key1', 'value1'), ('key1', 'value2'))
>>> r = requests.post('http://httpbin.org/post', data=payload)
>>> print(r.text)
{
  ...
  "form": {
    "key1": [
      "value1",
      "value2"
    ]
  },
  ...
}
```
##### json

有的网站需要提供的参数并非是`urlencoded`编码的参数，而是需要`json`编码
格式的参数，子需要将`data`使用`json`模块编码后传递给`data`参数即可
```
>>> import json

>>> url = 'https://api.github.com/some/endpoint'
>>> payload = {'some': 'data'}

>>> r = requests.post(url, data=json.dumps(payload))
```

此处除了可以自行对 `dict` 进行编码，你还可以使用 `json` 参数直接传递，
然后它就会被自动编码。这是 `2.4.2` 版的新加功能
```
>>> url = 'https://api.github.com/some/endpoint'
>>> payload = {'some': 'data'}

>>> r = requests.post(url, json=payload)
```

#### POST一个多部分编码(Multipart-Encoded)的文件
`requests`提交文件, 只需组织这样`{'file': open('report.xls', 'rb')}`的
参数，将参数传递给`files`即可
```python
import requests
url = 'http://httpbin.org/post'
files = {'file': open('report.xls', 'rb')}

r = requests.post(url, files=files)
print(r.text)
"""
{
  ...
  "files": {
    "file": "<censored...binary...data>"
  },
  ...
}
"""
```

## 响应对象的其他属性
### 响应头`response headers`
响应头是一个以 `Python` 字典形式展示的数据，可以调用`response.headers`属性访问
响应头。

```python
import requests
url = 'http://httpbin.org/post'
files = {'file': open('report.xls', 'rb')}

r = requests.post(url, files=files)
print(r.headers)
"""
{
    'content-encoding': 'gzip',
    'transfer-encoding': 'chunked',
    'connection': 'close',
    'server': 'nginx/1.0.4',
    'x-runtime': '148ms',
    'etag': '"e1ca502697e5c9317743dc078f67693f"',
    'content-type': 'application/json'
}
"""

```

### 响应状态码`response status_code`

可以检测响应状态码, 以判断响应是否符合我们的需求
```
>>> r = requests.get('http://httpbin.org/get')
>>> r.status_code
200
```
为方便引用，`Requests`还附带了一个内置的状态码查询对象
```
>>> r.status_code == requests.codes.ok
True
```

如果发送了一个错误请求(一个 `4XX` 客户端错误，或者 `5XX` 服务器错误响应)，
我们可以通过 `Response.raise_for_status()` 来抛出异常
```
>>> bad_r = requests.get('http://httpbin.org/status/404')
>>> bad_r.status_code
404

>>> bad_r.raise_for_status()
Traceback (most recent call last):
  File "requests/models.py", line 832, in raise_for_status
    raise http_error
requests.exceptions.HTTPError: 404 Client Error
```
但是，由于我们的例子中 `r` 的 `status_code` 是 `200` ，
当我们调用 `raise_for_status()` 时，得到的是：
```
>>> r.raise_for_status()
None
```
但是这个字典比较特殊：它是仅为 `HTTP` 头部而生的。
根据 `RFC 2616`， `HTTP` 头部是大小写不敏感的。

因此，我们可以使用任意大写形式来访问这些响应头字段
```
>>> r.headers['Content-Type']
'application/json'

>>> r.headers.get('content-type')
'application/json'
```

### Cookie
响应数据一般包含了`cookie`信息, 可以使用`response.cookies`快速访问

```
>>> url = 'http://example.com/some/cookie/setting/url'
>>> r = requests.get(url)

>>> r.cookies['example_cookie_name']
'example_cookie_value'
```

`Cookie` 的返回对象为 `RequestsCookieJar`，它的行为和字典类似，
但接口更为完整，适合跨域名跨路径使用。你还可以把 `Cookie Jar` 传到 `Requests` 中
```
>>> jar = requests.cookies.RequestsCookieJar()
>>> jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
>>> jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
>>> url = 'http://httpbin.org/cookies'
>>> r = requests.get(url, cookies=jar)
>>> r.text
'{"cookies": {"tasty_cookie": "yum"}}'
```

## 请求重定向与请求历史

默认情况下，除了 `HEAD`, `Requests` 会自动处理所有重定向。在`response`对象的
`history`属性可以来最终重定向。它是保存请求历史的一个列表。`Response.history` 是一个 `Response` 对象的列表，
为了完成请求而创建了这些对象。这个对象列表按照**从最老到最近**的请求进行排序。

如果你使用的是`GET`、`OPTIONS`、`POST`、`PUT`、`PATCH` 或者 `DELETE`，
那么你可以通过 `allow_redirects` 参数禁用重定向处理：
```
>>> r = requests.get('http://github.com', allow_redirects=False)
>>> r.status_code
301
>>> r.history
[]
```
如果你使用了 HEAD，你也可以启用重定向
```
>>> r = requests.head('http://github.com', allow_redirects=True)
>>> r.url
'https://github.com/'
>>> r.history
[<Response [301]>]
```


## 超时
你可以告诉 `requests` 在经过以 `timeout` 参数设定的秒数时间之后停止等待响应。
基本上所有的生产代码都应该使用这一参数。如果不使用，你的程序可能会永远失去响应
```
>>> requests.get('http://github.com', timeout=0.001)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
requests.exceptions.Timeout: HTTPConnectionPool(host='github.com', port=80): Request timed out. (timeout=0.001)
```

> `timeout` 仅对连接过程有效，与响应体的下载无关。 
> `timeout` 并不是整个下载响应的时间限制，而是如果服务器在 `timeout` 秒内没有应答，
> 将会引发一个异常（更精确地说，是在 `timeout` 秒内没有从基础套接字上接收到任何字节的数据时）
> If no timeout is specified explicitly, requests do not time out.

## 错误与异常

遇到网络问题（如：`DNS` 查询失败、拒绝连接等）时，`Requests` 会抛出一个 `ConnectionError` 异常。

如果 `HTTP` 请求返回了不成功的状态码，`Response.raise_for_status()` 会抛出一个 `HTTPError` 异常。

若请求超时，则抛出一个 `Timeout` 异常。

若请求超过了设定的最大重定向次数，则会抛出一个`TooManyRedirects` 异常。

所有`Requests`显式抛出的异常都继承自 `requests.exceptions.RequestException`。


## 判断数据是否为Ajax请求获取
- 如何检测页面中是否存在动态加载的数据？
    - 基于抓包工具实现
        - 先捕获网站请求后所有的数据包
        - 在数据包中定位到地址栏所对应请求的数据包，在response选项卡对应的数据中进行局部搜索（页面中的某一组内容）
            - 可以搜索到：爬取的数据不是动态加载的
            - 没有搜索到：爬取的数据是动态加载的
        - 如何定位动态加载的数据在哪个数据包中呢？
            - 进行全局搜索


