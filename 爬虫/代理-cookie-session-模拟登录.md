# 代理

当我们对一个网站短时间内发起大量的请求时，可能会出现下列错误。

- `HttpsConnectionPool`异常:
    - 原因：
        - 1.短时间内发起了高频的请求导致ip被禁
        - 2.`http`连接池中的连接资源被耗尽
    - 解决：
        - 1.代理
        - 2.`headers`中加入`Connection："close"`

**代理简介**

- 代理：代理服务器，可以接受请求然后将其转发。

- 匿名度
    - 高匿：啥也不知道
    - 匿名：知道你使用了代理，但是不知道你的真实ip
    - 透明：知道你使用了代理并且知道你的真实ip

- 类型：
    - `http`
    - `https`
    - `sockes5`

- 免费代理：
    - `www.goubanjia.com`
    - `快代理`
    - `西祠代理`
    - `http://http.zhiliandaili.cn/`

## urllib对代理的使用

```python
from urllib import request
from urllib.request import Request

url = 'https://www.baidu.com/s?wd=ip'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"
}
request_handler = Request(url=url, headers=headers)

proxy = {'http': '121.233.206.212:9999'}
# 创建代理处理器
proxies = request.ProxyHandler(proxy)
# 创建opener对象
opener = request.build_opener(proxies)
# 注册为全局opener
request.install_opener(opener)
resp = request.urlopen(request_handler)
print(resp.getcode())
```

## requests对代理的使用

```python
import requests

url = 'https://www.baidu.com/s?wd=ip'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"
}
proxy = {'http': '121.233.206.212:9999'}

response = requests.get(url, headers=headers, proxies=proxy)
print(response.status_code)
```

## 代理池构建

1. 爬取免费的代理ip
2. 检测代理ip是否可用
    * 使用代理随便发起一个请求，如果返回响应状态码为200，则代理是可用的。
3. 将可用代理加入到代理池中

```python
# 获取免费ip保存在文件中
# 代理池构建 以快代理提供的免费高匿名代理ip构建 https://www.kuaidaili.com/free/inha/1/
import requests
import random
import json
from lxml import etree

format_url = "http://www.kuaidaili.com/free/inha/%d/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
    "Connection": 'close'
}
# current_proxy = {'http':'110.243.24.22:9999'}

proxies_http_list = []

proxies_https_list = []

for page in range(1, 101):
    url = format_url % page
    # print(url)
    try:
        page_response = requests.get(url, headers=headers)
        if page_response.status_code == 200:
            page_html = page_response.text
        else:
            page_html = None
    except Exception as e:
        print(e)
        page_html = None
        if proxies_http_list:
            current_proxy = random.choice(proxies_http_list)

    if page_html is not None:
        tree = etree.HTML(page_html)
        ip_list = tree.xpath('//table//tr[position()>1]')
        # print(ip_list)
        for item in ip_list:
            ip = item.xpath('./td[1]/text()')[0]
            port = item.xpath('./td[2]/text()')[0]
            protocol = item.xpath('./td[4]/text()')[0]
            proxy = {
                protocol: ip + ":" + port
            }
            if protocol == "HTTP":
                proxies_http_list.append(proxy)
            else:
                proxies_https_list.append(proxy)
    else:
        continue
    print(proxies_http_list, proxies_https_list)
    with open('ip.json', 'w', encoding='utf8') as f:
        json.dump(proxies_http_list, f, ensure_ascii=False)
        json.dump(proxies_https_list, f, ensure_ascii=False)

# 读取文件中ip，检测是否有效，有效则保存，无效则剔除
import json
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
    "Connection": 'close'
}
fp = open("ip.json", 'r', encoding='utf-8')

ip_list = json.load(fp)

validity_proxies = []

while len(ip_list):
    proxy = ip_list.pop()
    response = requests.get(url='http://www.baidu.com', headers=headers, proxies=proxy)
    if response.status_code == 200:
        validity_proxies.append(proxy)

    print(validity_proxies)


```

# cookie

以获取雪球财经信息为例，https://xueqiu.com/

通过分析网站，我们知道信息是通过Ajax请求动态加载的。Ajax发送的请求地址为: https://xueqiu.com/statuses/hot/listV2.json
参数为:`since_id max_id size`, 其中变化的只有`max_id`变化规律为`max_id+=size`

```python
import requests

url = "https://xueqiu.com/statuses/hot/listV2.json"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"
}
params = {
    'since_id': '-1',
    'max_id': '0',
    'size': '15'
}

response = requests.get(url, params=params, headers=headers)
print(response.json())
```

执行代码发现，返回数据不正确。再次分析网站，发现在请求头中带有`cookie`信息、我们也在 headers中添加cookie信息，进行测试

```python
import requests

url = "https://xueqiu.com/statuses/hot/listV2.json"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
    "Cookie": "acw_tc=2760820816150988790958552e33fa6486c31b7b52d2d111c8b93d86b2a4e6; xq_a_token=62effc1d6e7ddef281d52c4ea32f6800ce2c7473; xqat=62effc1d6e7ddef281d52c4ea32f6800ce2c7473; xq_r_token=53a0f79d5bae795fb7abc6814dc0fc0410413016; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxNTYwMzIxNSwiY3RtIjoxNjE1MDk4ODUyNTE1LCJjaWQiOiJkOWQwbjRBWnVwIn0.hN9tL2NQvBNbtXK87kGiXkT46rgpJVKkMPvvwK9LTOEWfL4Ul49iOso97N7FdQ4FucyuJIfAaL9DAsUVLU-YHYvAIrcDjdmYAPY7PpRp4pCSd2964u43A2sWqDv10Zdj9sSpPdujSA0nF3ja2UpbqPVAVZxBcKgvH7aSSLyf1YjQ7ygYzhmZCJVVjb3bUlo9KSYhxmmKEw8zDlzyYBFSO7qLdBozl9KrwRevWo4CZRoyl1Wcnxk3fgTSSpSwac8N9K_SeVzBbob7jRs5WO4VZbwMiBrV3y9ZWNXTLs8TZ83VGXVjKQlN8lx8t-FFy1LyGfuCzgVkoDbT3-PwbkHDCw; u=421615098879100; Hm_lvt_1db88642e346389874251b5a1eded6e3=1615098886; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1615098886; device_id=24700f9f1986800ab4fcc880530dd0ed"
}
params = {
    'since_id': '-1',
    'max_id': '0',
    'size': '15'
}

response = requests.get(url, params=params, headers=headers)
print(response.json())
```

现在，发现数据就已经返回了。

当我们第一次请求该网站时，浏览器中也是不会带有cookie信息的。 那么这些cookie信息就是在我们第一次访问网址的时候产生的。 所以，可以先发起一次请求访问，生成cookie保存，再发起获取数据的请求

```python
import requests

cookie_url = "https://xueqiu.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
}

response = requests.get(cookie_url, headers=headers)
cookies = response.cookies  # 获取cookies

json_url = "https://xueqiu.com/statuses/hot/listV2.json"
params = {
    'since_id': '-1',
    'max_id': '0',
    'size': '15'
}
response = requests.get(json_url, params=params, headers=headers, cookies=cookies)
response.encoding = 'utf-8'
print(response.json())
```

# session

如果每次请求都要先获取cookies在发送请求，未免有点麻烦，可以使用会话`session`对像来 自动处理cookie。可以模拟浏览器

```python
import requests

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
}

session.get(url="https://xueqiu.com")
params = {
    'since_id': '-1',
    'max_id': '0',
    'size': '15'
}
r = session.get("https://xueqiu.com/statuses/hot/listV2.json", params=params)

print(r.json())
```

# 模拟登录

对于要进行登录验证后才能获取数据的接口，不等不进行登录操作。

在登录过程中，需要对验证进行处理，常见的验证有

* **字符型验证码验证**
* **滑动验证码验证**
* **点触验证码验证**
* **鼠标点击检测验证**

这些验证的处理，将决定你能否模拟登录成功的关键。最为**简单且高效**的方式就是**花钱**
购买打码平台的服务，常见的打码平台有

- 超级鹰：http://www.chaojiying.com/
- 打码兔
- 云打码
- ...

## 字符验证码

对于字符验证码，我们可以自行处理，使用图像识别工具进行识别。 下面将介绍`Tesseract-OCR`的使用

对于`Windows`下载`tesseract-ocr-w64-setup-v5.0.0.20190623.exe`一路下一步安装 即可

下载语言库`tessdata_best-4.1.0.tar.gz`解压后复制到`Tesseract-OCR`目录下 的`tessdata`目录下。

配置环境变量 在`Path`添加`Tesseract-OCR`目录的绝对路径，并添加`TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata`
环境变量中。

使用`pip`安装`tesserocr-2.4.0-cp36-cp36m-win_amd64.whl`
之后再使用`pip`安装`pytesser3 pytesseract tesseract`这三个模块。

定位到`pytesser3`源代码将`__init__.py`中的`tesseract_exe_name`改为自己安装目录下的`tesseract`即可

定位到`pytesseract`源码将`tesseract_cmd`修改为自己安装目录下载的`tesseract`即可

**测试识别示例1**
![](./test.png)

```python
import pytesser3
from PIL import Image

im = Image.open('test.png')
print(pytesser3.image_to_string(im))
```

识别成功

**测试识别示例2**
![](./test.png)

```python
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
im = Image.open('test.png')
print(pytesseract.image_to_string(im))
```

识别成功

### 图像处理Pillow

为了提高识别效率，需要对图像进行处理，以提高识别效率

这类验证码大多是数字、字母的组合，国内也有使用汉字的。 在这个基础上增加**噪点、干扰线、变形、重叠、不同字体颜色**等方法来增加识别难度。

相应的，验证码识别大体可以分为下面几个步骤

1. 灰度处理
2. 增加对比度(可选)
3. 二值化
4. 降噪
5. 倾斜校正分割字符
6. 建立训练库
7. 识别

#### 灰度化

像素点是最小的图像单元，一张图片由好多的像素点构成， 一个像素点的颜色是由`RGB`三个值 来表现的，所以一个像素点矩阵对应三个颜色向量矩阵，我们对图像的处理就是对这个像素点矩阵的操作，
想要改变某个像素点的颜色，只要在这个像素点矩阵中找到这个像素点的位置`(x, y)`, 因为一个像素点的颜色由红、绿、蓝三个颜色变量表示，所以我们通过给这三个变量赋值， 来改变这个像素点的颜色.

图片的灰度化,就是让像素点矩阵中的每一个像素点都满足下面的关系：`R=G=B`, 此时的这个值叫做**灰度值**.

灰度化的转化公式一般为：

`R = G = B` = `处理前的 R*0.3 + G*0.59 + B*0.11`

```
img = img.convert('L')  #转为灰度图
```

#### 二值化

二值化就是让图像的像素点矩阵中的每个像素点的灰度值为**0（黑）**或者**255（白）** ， 从而实现二值化，让整个图像呈现**只有黑和白**的效果。

原理是利用设定的一个**阈值**来判断图像像素为 0 还是 255，
**小于** 阈值的 **变为0（黑色）**， **大于** 的 **变为255（白色）**。

这个临界灰度值就被称为阈值，阈值的设置很重要。阈值过大或过小都会对图片造成损坏。

选择阈值的原则是：**既要尽可能保存图像信息，又要尽可能减少背景和噪声的干扰**，

**常用二值化方法**

- 取阈值为127（0~255的中数，（0+255）/2=127 ）

  好处是计算量小速度快，

  缺点也是很明显的 ，对于图片中内容色彩分布较大的图片，很容易造成内容的缺失。

- 平均值法

  计算像素点矩阵中的所有像素点的灰度值的平均值**avg**

  `（像素点1灰度值+...+像素点n灰度值）/ n = 像素点平均值avg `

  这样做比方法1好一些。 但可能导致部分对象像素或者背景像素丢失。

```python
def averageThreshold(img):
    """
    计算平均值
    """
    pixdata = img.load()
    width,height = img.size
    
    threshold = sum(img.getdata())/(width*height)   # 计算图片的平均阈值

    # 遍历所有像素，大于阈值的为白色
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x,y] = 255

    return img
```

- 双峰法

  图像由**前景和背景**组成，在灰度直方图上，前后二景都形成高峰， 在双峰之间的最低谷处就是图像的阈值所在。 当**前后景的对比较为强烈**时， 分割效果较好；否则基本无效。

- 迭代法

  首先选择一个**近似阈值**作为估计值的初始值，然后进行分割，产生子图像， 并根据子图像的特性来选取新的阈值，再利用新的阈值分割图像，经过几次循环， 使错误分割的图像像素点降到最少。这样做的效果好于用初始阈值直接分割图像的效果。

    1. 求出图象的最大灰度值和最小灰度值，分别记为`Pmax`和`Pmin`， 令初始阈值`T0=(Pmax+Pmin)/2`
    2. 根据阈值`Tk`将图象分割为**前景和背景**， （小于 `T0` 的像素部分，大于`T0`的背景部分）， 并分别求其均值 `avgPix`, `avgBac`
    3. 求出新阈值`Tk = ( avgPix+avgBac) / 2`；
    4. 若`T0=Tk`，则所得即为阈值；否则转`2`，迭代计算 。

```python
from PIL import Image


def iterGetThreshold(img, pixdata, width, height):
    """
    迭代法，求阈值
    """
    pixPrs = pixBac = []  # 用于统计前景和背景平均阈值
    threshold = 0
    pixel_min, pixel_max = img.getextrema()  # 获得图片中最大和最小灰度值
    newThreshold = int((pixel_min + pixel_max) / 2)  # 初始阈值

    while True:
        if abs(threshold - newThreshold) < 5:  # 差值小于5,退出
            break
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] >= newThreshold:
                    pixBac.append(pixdata[x, y])  # 大于阈值 为背景
                else:
                    pixPrs.append(pixdata[x, y])  # 小于， 前景

        avgPrs = sum(pixPrs) / len(pixPrs)
        avgBac = sum(pixBac) / len(pixBac)
        threshold = newThreshold
        newThreshold = int((avgPrs + avgBac) / 2)

    return newThreshold


def binary(img, threshold=None):
    """
    二值化
    """
    img = img.convert('L')  # 转为灰度图
    pixdata = img.load()
    width, height = img.size

    if not threshold:
        threshold = iterGetThreshold(img, pixdata, width, height)
    # 遍历所有像素，大于阈值的为白色
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255

    return img


img = Image.open('test-1.jpg')
img.show()
new_img = binary(img)
new_img.show()
```

#### 降噪

从前面经过二值化处理，如果一个像素点是图片或者干扰因素的一部分，那么它的灰度值一定是**0， 即黑色**； 如果一个点是背景，则其灰度值应该是**255，白色**。

因此对于孤立的噪点，其周围应该都是白色，或者大多数点都是白色`pixel`

如果图片分辨率够高，一个噪点实际上可能是有很多个点组成 ，所以此时的判断条件应该放宽， 即一个点是黑色的并且相邻的8个点为白色点的个数大于一个固定值，那么这个点就是噪点 。

常见的**4邻域、8邻域算法**。所谓的**X邻域算法**，可以参考手机九宫格输入法， 按键5为要判断的像素点，**4邻域**就是判断上下左右，**8邻域**就是判断周围8个像素点。 如果这**4或8个点**中`255`
的个数大于某个阈值则判断这个点为噪音，阈值可以根据实际情况修改。

这个方法对小噪点比较好，如果阀值设的比较大，很多验证码字符也会受到很大影响， 因为验证码可能就是一些断断续续的点连出来的，阀值设太大，尽管噪点没了，验证码也会没了。

```python
def depoint(img, N=2):
    """
    降噪
    """
    pixdata = img.load()
    width, height = img.size
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            count = 0
            if pixdata[x, y - 1] == 255:  # 上
                count = count + 1
            if pixdata[x, y + 1] == 255:  # 下
                count = count + 1
            if pixdata[x - 1, y] == 255:  # 左
                count = count + 1
            if pixdata[x + 1, y] == 255:  # 右
                count = count + 1

            # if pixdata[x-1, y-1] == 255:  #左上
            #     count = count + 1
            # if pixdata[x+1, y-1] == 255:  #右上
            #     count = count + 1
            # if pixdata[x-1, y+1] == 255:  #左下
            #     count = count + 1
            # if pixdata[x+1, y+1] == 255:  #右下
            #     count = count + 1

            if count > N:
                pixdata[x, y] = 255  # 设置为白色
    return img
```


#### 图片识别的完整流程
```python
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

im=Image.open('test.jpg')
# print(pytesseract.image_to_string(im))

# 第一步 转为灰度图
im = im.convert('L')  # 转为灰度图

# 第二步 二值化
def iterGetThreshold(img, pixdata, width, height):
    """
    迭代法，求阈值
    """
    pixPrs = pixBac = []  # 用于统计前景和背景平均阈值
    threshold = 0
    pixel_min, pixel_max = img.getextrema()  # 获得图片中最大和最小灰度值
    newThreshold = int((pixel_min + pixel_max) / 2)  # 初始阈值

    while True:
        if abs(threshold - newThreshold) < 5:  # 差值小于5,退出
            break
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] >= newThreshold:
                    pixBac.append(pixdata[x, y])  # 大于阈值 为背景
                else:
                    pixPrs.append(pixdata[x, y])  # 小于， 前景

        avgPrs = sum(pixPrs) / len(pixPrs)
        avgBac = sum(pixBac) / len(pixBac)
        threshold = newThreshold
        newThreshold = int((avgPrs + avgBac) / 2)

    return newThreshold


def binary(img, threshold=None):
    """
    二值化
    """
    img = img.convert('L')  # 转为灰度图
    pixdata = img.load()
    width, height = img.size

    if not threshold:
        threshold = iterGetThreshold(img, pixdata, width, height)
    # 遍历所有像素，大于阈值的为白色
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255

    return img

new_img = binary(im)



# 第三步 降噪
def depoint(img, N=2):
    """
    降噪
    """
    pixdata = img.load()
    width, height = img.size
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            count = 0
            if pixdata[x, y - 1] == 255:  # 上
                count = count + 1
            if pixdata[x, y + 1] == 255:  # 下
                count = count + 1
            if pixdata[x - 1, y] == 255:  # 左
                count = count + 1
            if pixdata[x + 1, y] == 255:  # 右
                count = count + 1
            if pixdata[x-1, y-1] == 255:  #左上
                count = count + 1
            if pixdata[x+1, y-1] == 255:  #右上
                count = count + 1
            if pixdata[x-1, y+1] == 255:  #左下
                count = count + 1
            if pixdata[x+1, y+1] == 255:  #右下
                count = count + 1

            if count > N:
                pixdata[x, y] = 255  # 设置为白色
    return img

img = depoint(new_img, 4)

# 第四步 识别
print(pytesseract.image_to_string(img))
```





### 接入打码平台--超级鹰
注册`--`登录`--`购买提分`--`下载开发示例

**案例5**[古诗文网模拟登录](./案例5，字符验证码识别.ipynb)

```python
from chaojiying import Chaojiying_Client

chaojiying = Chaojiying_Client('dyp1996', 'DYP-abcd-1996', '913681')


import requests
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from lxml import etree
from io import BytesIO
from PIL import Image

session = requests.Session()

url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
}
response = session.get(url, headers=headers)

tree = etree.HTML(response.text)
img_src = "https://so.gushiwen.cn/" + tree.xpath('//*[@id="imgCode"]/@src')[0]

__VIEWSTATE = tree.xpath("//input[@id='__VIEWSTATE']/@value")[0]

__VIEWSTATEGENERATOR = tree.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value")[0]
print(__VIEWSTATEGENERATOR, __VIEWSTATE)

img_data = session.get(img_src, headers=headers).content
img_io = BytesIO(img_data)

result = chaojiying.PostPic(img_io, 1902)

code = result.get("pic_str")

print(code)
Image.open(img_io).show()

login_url = "https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx"

data = {
    "__VIEWSTATE": __VIEWSTATE,
    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
    "from": "http://so.gushiwen.cn/user/collect.aspx",
    "email": "2321936402@qq.com",
    "pwd": "abcd1996",
    "code": code,
    "denglu": "登录"
}

resp = session.post(login_url, headers=headers, data=data)
with open('login.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)
```

该网站的登录，需要**验证字符验证码、动态变化的数据、cookie验证**
* **字符验证码**: 该验证码可以接入超级鹰打码平台进行获取
* **动态变化的数据**: 对于动态变化的数据，基本上都是在**登录的前一个页面源码中携带**
* **cookie验证**: 登录验证的`cookie`可能在登录之前的过程中的任何一个请求中生成，
  将所有请求都以`session`会话的方式进行请求发送以便于自动保存`cookie`





