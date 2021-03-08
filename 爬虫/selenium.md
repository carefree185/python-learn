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
    

## selenium基本使用

### 示例: 打开百度，搜索python
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


