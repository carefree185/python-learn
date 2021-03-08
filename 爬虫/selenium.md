# selenium
- selenium模块在爬虫中的使用
    - 概念：是一个基于浏览器自动化的模块。
    - 爬虫之间的关联：
        - 便捷的捕获到动态加载到的数据。（可见即可得）
        - 实现模拟登陆
    - 环境安装：`pip install selenium`
    - 基本使用：
        - 准备好某一款浏览器的驱动程序：http://chromedriver.storage.googleapis.com/index.html
            - 版本的映射关系：https://blog.csdn.net/huilan_same/article/details/51896672
        - 实例化某一款浏览器对象
    - 动作链：
        - 一系列连续的动作
        - 在实现标签定位时，如果发现定位的标签是存在于iframe标签之中的，则在定位时必须执行一个
        固定的操作：bro.switch_to.frame('id')
    - 无头浏览器的操作：无可视化界面的浏览器
        - PhantomJs:停止更新
        - 谷歌无头浏览器
    - 让selenium规避检测
    

## selenium的使用

### 1.1 示例: 打开百度，搜索python
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 打开一个Chrome浏览器
browser = webdriver.Chrome()
# 请求百度首页
browser.get('https://www.baidu.com')
# 找到输入框位置
input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="kw"]'))
            )
# 在输入框中输入Python
input.send_keys('Python')
# 找到输入按钮
button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="su"]'))
            )
# 点击一次输入按钮
button.click()
browser.quit()
```


### 1.2 浏览器对象及相关操作(Webdriver对象)
```python
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome(executable_path='/webdriver/chromedriver')  # 创建浏览器对象
# 支持常见的chrome firefox edge等浏览器

# 发起请求, 向指定url发起请求
driver.get('url') 
# 获取页面源代码
html = driver.page_source
```
selenium打开浏览器是以全新状态打开的，不会包含任何的设置、缓存、cookie等信息

#### 1.2.1 获取页面元素
浏览器对象有很多支持我们获取定位页面元素的方法，例如

|定位器|描述|
|:---:|:---:|
|`class name`|定位`class`属性与搜索值匹配的元素（不允许使用复合类名）|
|`css selector`|定位 `CSS` 选择器匹配的元素|
|`id`|定位 `id` 属性与搜索值匹配的元素|
|`name`|定位 `name` 属性与搜索值匹配的元素|
|`link text`|定位`link text`可视文本与搜索值完全匹配的锚元素|
|`partial link text`|定位`link text`可视文本部分与搜索值部分匹配的锚点元素。如果匹配多个元素，则只选择第一个元素。|
|`tag name`|定位标签名称与搜索值匹配的元素|
|`xpath`|定位与 `XPath` 表达式匹配的元素|

##### 1.2.1.1 常见页面元素定位的方法

**查找单个元素的方法**

| 方法                                  | 作用                         |
| ------------------------------------- | ---------------------------- |
| `find_element_by_xpath`()             | 通过`Xpath`查找              |
| `find_element_by_class_name`()        | 通过`class属性`查找          |
| `find_element_by_css_selector`()      | 通过`css选择器`查找          |
| `find_element_by_id`()                | 通过`id`查找                 |
| `find_element_by_link_text`()         | 通过`链接文本`查找           |
| `find_element_by_name`()              | 通过`name属性`进行查找       |
| `find_element_by_partial_link_text`() | 通过`链接文本的部分匹配`查找 |
| `find_element_by_tag_name`()          | 通过`标签名`查找             |

查找后返回的是一个`Webelement`对象。

**查找多元素的方法**

上面的方法都是将第一个找到的元素进行返回，而将所有匹配的元素进行返回使用的是
`find_elements_by_*`方法

**注意：将其中的`element`加上一个`s`，则是对应的多个查找方法，
对于页面只能出现一次的元素没有查找多个的方法，例如`id`**

此方法返回的是一个`Webelement`对象组成的**列表**。

##### 1.2.1.2 通过私有方法进行查找
除了以上的多种查找方式，还有两种私有方法`find_element()`和`find_elements()`可以使用：

例子：

```python
from selenium.webdriver.common.by import By
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome(executable_path='/webdriver/chromedriver')  # 创建浏览器对象
# 支持常见的chrome firefox edge等浏览器

# 发起请求, 向指定url发起请求
driver.get('url') 
# 查找元素
driver.find_element(By.XPATH, '//button[text()="Some text"]')
driver.find_elements(By.XPATH, '//button')
```

`By`这个类是专门用来查找元素时传入的参数，这个类中有以下属性：

```python
ID = "id"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
NAME = "name"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"
```

#### 1.2.2 浏览器操作

```python
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome(executable_path='/webdriver/chromedriver')  # 创建浏览器对象
# 支持常见的chrome firefox edge等浏览器

# 发起请求, 向指定url发起请求
driver.get('url') 

# 获取页面源代码
html = driver.page_source

# 关闭浏览器当前窗口
driver.close()

# 退出webdriver并关闭所有窗口。
driver.quit()

# 刷新当前页面
driver.refresh()

# 获取当前页面标题
title = driver.title

# 获取当前页面的url
url = driver.current_url

# 获取当前会话中所有窗口的句柄
handler = driver.window_handles
```

#### 1.2.3 cookie操作

```python
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome(executable_path='/webdriver/chromedriver')  # 创建浏览器对象

# 添加cookie
driver.add_cookie({'name' : 'foo', 'value' : 'bar'})
# cookie_dict: 一个字典对象，必须要有"name"和"value"两个键，可选的键有：“path”, “domain”, “secure”, “expiry”

# 获取名称为name的cookie
driver.get_cookie('name')  # 没有则返回None

# 获取所有cookie
driver.get_cookies()  # 返回一个字典

# 删除名称为name的cookie
driver.delete_cookie('name')

# 删除所以cookie
driver.delete_all_cookies()
```

#### 1.2.4 获取截屏
- `get_screenshot_as_base64()`

  获取当前窗口的截图保存为一个`base64`编码的字符串。

- `get_screenshot_as_file(filename)`

  获取当前窗口的截图保存为一个`png`格式的图片，`filename`参数为图片的保存地址，
  最后应该以`.png`结尾。如果出现`IO`错误，则返回`False`。

- `get_screenshot_as_png()`

  获取当前窗口的截图保存为一个`png`格式的**二进制字符串**。

#### 1.2.5 获取窗口信息

- `get_window_position(windowHandle='current')`

  获取当前窗口的`x,y`坐标。

- `get_window_rect()` 

  获取当前窗口的`x,y`坐标和当前窗口的高度和宽度。

- `get_window_size(windowHandle='current') `

  获取当前窗口的高度和宽度。

#### 1.2.6 窗口切换

- `switch_to.frame(frame_reference)`

  将焦点切换到指定的子框架中

- `switch_to.window(window_name)`
  
  切换窗口

#### 1.2.7 JS注入
- `execute_async_script(script, *args)` 

  在当前的`window/frame`中`异步`执行JS代码。

  `script`：是你要执行的JS代码。

  `*args`：是你的JS代码执行要传入的参数。
  
- `execute_script(script, *args)` 

  在当前的`window/frame`中`同步`执行`JS`代码。

  `script`：是你要执行的`JS`代码。

  `*args`：是你的`JS`代码执行要传入的参数。

### 1.3 WebElement对象
元素定位(通过`find_*`)时获取到的元素对象。该元素对象常用方法如下

|方法/属性|作用|
|:---:|:---:|
|`click()`|点击元素|
|`send_keys(key)`|输入文本|
|`clear()`|清空文本|
|`submit()`|提交表单|
|`get_attribute(name)`|获取元素的`attribute/property`, 优先返回完全匹配属性名的值，如果不存在，则返回属性名中包含`name`的值|
|`screenshot(filename)`|获取截图|
|||
|`text`|获取当前元素的文本内容|
|`tag_name`|获取当前元素的标签名|
|`size`|获取当前元素的大小|
|`screenshot_as_png`|将当前元素截屏并保存为png格式的二进制数据|
|`screenshot_as_base64`|将当前元素截屏并保存为base64编码的字符串|
|`rect`|获取一个包含当前元素大小和位置的字典|
|`parent`|获取当前元素的父节点|
|`location`|当前元素的位置|
|`id`|当前元素的`id`值，主要用来`selenium`内部使用，可以用来判断两个元素是否是同一个元素|

```python
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome(executable_path='/webdriver/chromedriver')  # 创建浏览器对象
# 支持常见的chrome firefox edge等浏览器

# 发起请求, 向指定url发起请求
driver.get('url') 

id_element = driver.find_element_by_id('id_value')

id_element.send_keys('hhe')  # 模拟输入值
id_element.clear()  # 清空
id_element.click()  # 点击
id_element.submit()  # 提交表单
id_element.screenshot('filepath')  # 截图元素
id_element.get_attribute('name')  # 获取属性
id_element.get_property("name")
```


#### 1.3.1 Keys
我们经常需要模拟键盘的输入，当输入普通的值时，在`send_keys()`方法中传入要输入的字符串就好了。

但是我们有时候会用到一些特殊的按键，这时候就需要用到我们的`Keys`类
```python
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome(executable_path='/webdriver/chromedriver')  # 创建浏览器对象
# 支持常见的chrome firefox edge等浏览器

# 发起请求, 向指定url发起请求
driver.get('url') 

id_element = driver.find_element_by_id('id_value')
id_element.send_keys(Keys.CONTROL, 'C')  # 输入control+c
```
这个`Keys`类有很多属性，每个属性对应一个按键。所有的属性如下所示
```python
ADD = u'\ue025'
ALT = u'\ue00a'
ARROW_DOWN = u'\ue015'
ARROW_LEFT = u'\ue012'
ARROW_RIGHT = u'\ue014'
ARROW_UP = u'\ue013'
BACKSPACE = u'\ue003'
BACK_SPACE = u'\ue003'
CANCEL = u'\ue001'
CLEAR = u'\ue005'
COMMAND = u'\ue03d'
CONTROL = u'\ue009'
DECIMAL = u'\ue028'
DELETE = u'\ue017'
DIVIDE = u'\ue029'
DOWN = u'\ue015'
END = u'\ue010'
ENTER = u'\ue007'
EQUALS = u'\ue019'
ESCAPE = u'\ue00c'
F1 = u'\ue031'
F10 = u'\ue03a'
F11 = u'\ue03b'
F12 = u'\ue03c'
F2 = u'\ue032'
F3 = u'\ue033'
F4 = u'\ue034'
F5 = u'\ue035'
F6 = u'\ue036'
F7 = u'\ue037'
F8 = u'\ue038'
F9 = u'\ue039'
HELP = u'\ue002'
HOME = u'\ue011'
INSERT = u'\ue016'
LEFT = u'\ue012'
LEFT_ALT = u'\ue00a'
LEFT_CONTROL = u'\ue009'
LEFT_SHIFT = u'\ue008'
META = u'\ue03d'
MULTIPLY = u'\ue024'
NULL = u'\ue000'
NUMPAD0 = u'\ue01a'
NUMPAD1 = u'\ue01b'
NUMPAD2 = u'\ue01c'
NUMPAD3 = u'\ue01d'
NUMPAD4 = u'\ue01e'
NUMPAD5 = u'\ue01f'
NUMPAD6 = u'\ue020'
NUMPAD7 = u'\ue021'
NUMPAD8 = u'\ue022'
NUMPAD9 = u'\ue023'
PAGE_DOWN = u'\ue00f'
PAGE_UP = u'\ue00e'
PAUSE = u'\ue00b'
RETURN = u'\ue006'
RIGHT = u'\ue014'
SEMICOLON = u'\ue018'
SEPARATOR = u'\ue026'
SHIFT = u'\ue008'
SPACE = u'\ue00d'
SUBTRACT = u'\ue027'
TAB = u'\ue004'
UP = u'\ue013'
```

### 1.4 动作链

一般来说我们与页面的交互可以使用Webelement的方法来进行点击等操作。但是，有时候我们需要一些更复杂的动作，类似于拖动，双击，长按等等。

这时候就需要用到我们的`Action Chains（动作链）`完成动作连操作

#### 1.4.1 示例
```python
from selenium.webdriver import ActionChains
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome(executable_path='/webdriver/chromedriver')  # 创建浏览器对象
# 支持常见的chrome firefox edge等浏览器

# 发起请求, 向指定url发起请求
driver.get('url') 

element = driver.find_element_by_name("source")
target = driver.find_element_by_name("target")

actions = ActionChains(driver)
actions.drag_and_drop(element, target)
actions.perform()
```

在导入动作链模块以后，需要声明一个动作链对象，在声明时将`webdriver`当作参数传入，
并将对象赋值给一个`actions`变量。

然后我们通过这个`actions`变量，调用其内部附带的各种动作方法进行操作。

**注：在调用各种动作方法后，这些方法并不会马上执行，而是会按你代码的顺序存储在`ActionChains`对象的队列中。当你调用`perform()`时，这些动作才会依次开始执行。**

#### 1.4.2 常见动作
|动作|作用|
|:---:|:---:|
`click(on_element=None)`|单击鼠标左键
`click_and_hold(on_element=None)`|点击鼠标左键，不松开
`context_click(on_element=None)`|点击鼠标右键
`double_click(on_element=None)`|双击鼠标左键
`drag_and_drop(source, target)`|拖拽到某个元素然后松开
`drag_and_drop_by_offset(source, xoffset, yoffset)`|拖拽到某个坐标然后松开
`key_down(value, element=None)`|按下某个键盘上的键
`key_up(value, element=None)`|松开某个键
`move_by_offset(xoffset, yoffset)`|鼠标从当前位置移动到某个坐标
`move_to_element(to_element)`|鼠标移动到某个元素
`move_to_element_with_offset(to_element, xoffset, yoffset)`|移动到距某个元素（左上角坐标）多少距离的位置
`perform()`|执行链中的所有动作
`release(on_element=None)`|在某个元素位置松开鼠标左键
`send_keys(*keys_to_send)`|发送某个键到当前焦点的元素
`send_keys_to_element(element, *keys_to_send)`|发送某个键到指定元素

### 1.5 selenium其他操作

- `PhantomJS`: 暂停更新，不推荐使用
#### chrome无界面运行
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 实例化一个启动参数对象
chrome_options = Options()
# 设置浏览器以无界面方式运行
chrome_options.add_argument('--headless')
# 官方文档表示这一句在之后的版本会消失，但目前版本需要加上此参数
chrome_options.add_argument('--disable-gpu')
# 设置浏览器参数时最好固定好窗口大小，窗口大小不同会在解析网页时出现不同的结果
chrome_options.add_argument('--window-size=1366,768')
# 启动浏览器
browser = webdriver.Chrome(chrome_options=chrome_options)
```


#### 浏览器动选项


|        启动参数        |                 作用                 |
| :--------------------: | :----------------------------------: |
|    `--user-agent="" `    |        设置请求头的User-Agent        |
| `--window-size=1366,768` |           设置浏览器分辨率           |
|       `--headless`       |              无界面运行              |
|   `--start-maximized`    |              最大化运行              |
|      `--incognito`       |               隐身模式               |
|  `--disable-javascript`  |            禁用javascript            |
|   `--disable-infobars`   | 禁用浏览器正在被自动化程序控制的提示 |

完整启动参数可以到此页面查看：

https://peter.sh/experiments/chromium-command-line-switches/

#### selenium规避监测

网站对请求发起者进行监控，当浏览器打开网站时执行js代码`window.navigator.webdriver`
的返回值为`undefined`，如果浏览器被`selenium`打开则返回`true`，网站就是通过改
方法进行监控。

规避方法是，给浏览添加启动参数`'excludeSwitches', ['enable-automation']`

```python
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(r'chromedriver.exe',options=option)
driver.get('https://www.taobao.com/')
```

#### 等待
在selenium操作浏览器的过程中，每一次请求url，selenium都会等待页面加载完毕以后，才会将操作权限再次交给我们的程序。

但是，由于ajax和各种JS代码的异步加载问题，所以我们在使用selenium的时候常常会遇到操作的元素还没有加载出来，就会引发报错。为了解决这个问题，`Selenium`提供了几种等待的方法，让我们可以等待元素加载完毕后，再进行操作。



##### 显式等待

###### 例子

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()
```

在这个例子中，我们在查找一个元素的时候，不再使用`find_element_by_*`这样的方式来查找元素，而是使用了`WebDriverWait`。

try代码块中的代码的意思是：在抛出元素不存在异常之前，最多等待10秒。在这10秒中，`WebDriverWait`会默认每500ms运行一次until之中的内容，而until中的`EC.presence_of_element_located`则是检查元素是否已经被加载，检查的元素则通过`By.ID`这样的方式来进行查找。

就是说，在10秒内，默认每0.5秒检查一次元素是否存在，存在则将元素赋值给element这个变量。如果超过10秒这个元素仍不存在，则抛出超时异常。

###### **Expected Conditions** 

`Expected Conditions`这个类提供了很多种常见的检查条件可以供我们使用。

- title_is
- title_contains
- presence_of_element_located
- visibility_of_element_located
- visibility_of
- presence_of_all_elements_located
- text_to_be_present_in_element
- text_to_be_present_in_element_value
- frame_to_be_available_and_switch_to_it
- invisibility_of_element_located
- element_to_be_clickable
- staleness_of
- element_to_be_selected
- element_located_to_be_selected
- element_selection_state_to_be
- element_located_selection_state_to_be
- alert_is_present 

例子：

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
# 等待直到元素可以被点击
element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
```



##### 隐式等待

隐式等待指的是，在`webdriver`中进行`find_element`这一类查找操作时，如果找不到元素，则会默认的轮询等待一段时间。

这个值默认是0，可以通过以下方式进行设置：

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10) # 单位是秒
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")
```


