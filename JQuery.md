# 一、JQuery简介
* jQuery是一个JavaScript函数库。
* jQuery是一个轻量级的"写的少，做的多"的JavaScript库。
* jQuery库包含以下功能：
    * HTML 元素选取
    * HTML 元素操作
    * CSS 操作
    * HTML 事件函数
    * JavaScript 特效和动画
    * HTML DOM 遍历和修改
    * AJAX
    * Utilities

**目前jQuery兼容于所有主流浏览器**

* [JQuery官网](https://jquery.com/)
* [JQuery中文手册](https://jquery.cuishifeng.cn/index.html)


# 二、JQuery的导入
```html
<script src="../JavaScript/JQuery-3.5.1.js"></script> <!--通过文件引入JQuery-->
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.js"></script> <!--通过bootcdn引入Jquery，必须联网使用-->
```

# 三、基本使用
1. 语法结构
    ```js
    JQuery(selector).action()
    $(selector).action()
     /*选择器      操作*/
    ```
    **jQuery选择器使用`CSS`中的选择器** 
2. Jquery与原生js对比
    ```js
    <script>
        // 原生js
        let pEle = document.getElementById("d1");
        pEle.style.color = "red";
    
        // jquery
        $("#d1").css("color", "blue");
    </script>
    ```

## 3.1 基本选择器
1. id选择器: `$("#id值")`
2. class选择器: `$(".class值")`
3. 标签选择器: `$("标签名")`
4. `$("#id值")[index]`: 获取index处的标签对象
5. `$(标签对象)`: 将标签对象转为jQuery对象

![](https://images.gitee.com/uploads/images/2020/1204/185553_5845bb6d_7841459.png "屏幕截图.png")

## 3.2 高级选择器
1. `$("div[class='c1']"): `属性选择器
2. `$("#d1, .c1, p")`: 并集选择器
3. `$("div span")`: 后代选择器
4. `$("div>span")`: 子代选择器
5. `$("div+span")`: 相邻兄弟选择器
6. `$("div~span")`: 兄弟选择器

```js
$("#d1, .c1, p")

$("div span") // 选择div下的所有span标签

$("div>span") // 选择div的子代span标签

$("div+span") // 选择div相邻的兄弟span标签

$("div~span") // 选择div兄弟span标签

```
![](https://images.gitee.com/uploads/images/2020/1204/190456_2803b76b_7841459.png "屏幕截图.png")

## 3.3 筛选器
1. `$("选择器:first")`: 获取第一个元素
2. `$("选择器:last")`: 获取最后一个元素
3. `$("选择器:eq(index)")`: 获取索引为index的元素
4. `$("选择器:gt(index)")`: 获取索引大于index的元素
5. `$("选择器:lt(index)")`: 获取索引小于index的元素
6. `$("选择器:even")`: 获取索引为奇数的元素
7. `$("选择器:odd")`: 获取索引为偶数的元素
8. `$("选择器:not(_选择器)")`： 排除`_选择器`元素
9. `$("选择器:has(_选择器)")`: 获取含有`_选择器`的元素 

```js
$("ul li:first");  // 获取ul下的li标签，过滤出第一个
$("ul li:last");  // 获取ul下的li标签，过滤出最后一个
$("ul li:eq(2)"); // 获取索引为2个标签
$("ul li:even");  // 获取索引为偶数的标签
$("ul li:odd");  // 获取索引为奇数的标签
```
## 3.4 属性选择器
1. `$("[key]")`: 选择具有某种属性(key)的标签
2. `$("[key=value]")`：选择具有`属性名(key)=属性值(value)`的标签
3. `$("[key$=value]")`: 选择属性名的属性值以`value`结尾的标签
4. `$("[key^=value]")`: 选择属性名的属性值以`value`开头的标签
5. `$("[key*=value]")`：选择属性名的属性值包含`value`的标签

## 3.5 表单筛选器
```js
$("selectors:text");  // 匹配所有的单行文本框
$(":password");  // 匹配所有密码框
$(":radio"); // 匹配所有单选按钮
```
![](https://images.gitee.com/uploads/images/2020/1205/122033_5de8e648_7841459.png "屏幕截图.png")

> 1. **`:checked`会选择到`selected`**
> 2. **`:selected`不会选择到`checked`**


## 3.6 筛选方法(jQuery对象的方法)
1. `$(selector).next()`: 选择selector选中的下一个标签
2. `$(selector).nextAll()`: 选择selector选中的下面所有标签
3. `$(selector).nextUntil(_selector)`: 选择selector选中的下面所有标签直到遇到`_selector`选中的标签

4. `$(selector).prev()`：选择selector选中的上一个标签
5. `$(selector).prevAll()`: 选择selector选中的上面所有标签
6. `$(selector).prevUntil(_selector)`: 选择selector选中的上面所有标签直到遇到`_selector`选中的标签

7. `$(selector).parent()`: 获取selector选中的标签的父标签
8. `$(selector).parents()`: 获取selector选中的标签的所有层级的父标签
9. `$(selector).parentsUntil(_selector)`: 选择selector选中的父标签直到遇到`_selector`选中的标签

10. `$(selector).children()`: 获取selector选中的标签的子代标签
11. `$(selector).siblings()`: 获取selector选中的标签的所有兄弟标签
12. `$(selector).find(_selector)`: 在selector选中的标签内部查找`_selector`


**过滤器等价方法**

![](https://images.gitee.com/uploads/images/2020/1205/124837_8628a341_7841459.png "屏幕截图.png")

# 四、jQuery操作

## 4.1 操作class属性值
|js操作类|jQuery操作类|说明|
|:---:|:---:|:---:|
|`classList.add("value")`|`addClass("value")`|添加class的属性值|
|`classList.remove("value")`|removeClass("value")|移除class的属性值|
|`classList.contains("value")`|`hasClass("value")`|判断是否有class属性值|
|`classList.toggle("value")`|toggleClass("value")|有则删除，无则添加|

```js
$("div").addClass("c4");  // 添加类属性
$("div").removeClass("c3"); // 移除属性值c3
$("div").hasClass("c2"); // 判断class是否具有c2属性值
$("div").toggleClass("c2"); // 有则添加，无责删除
```

## 4.2 CSS属性操作
```js
$("p").first().css("color", "red").next().css("color", "blue")
```
> **jQuery对象调用jQuery方法后返回的仍然是一个当前jQuery对象** 

## 4.3 位置操作
```js
$("selector").offset([coordinates]);  // 获取标签相对于窗口的偏移。
$("selector").position(); // 获取标签相对于父标签的偏移
$("selector").scrollTop([val]);  // 获取标签相对滚动条顶部的偏移
$("selector").scrollLeft([val]);  // 获取标签相对于滚动条左侧的偏移
```

## 4.4 尺寸操作
```js
$("selector").height([val|fn]);  // 文本高度
$("selector").width([val|fn]); // 文本宽度
$("selector").innerHeight();   // 文本高度+padding
$("selector").innerWidth();  // 文本宽度+padding
$("selector").outerHeight([options]);  // 文本高度+padding+border
$("selector").outerWidth([options]);  // 文本宽度+padding+border
```

## 4.5 文本操作
|js操作|jQuery操作|
|:---:|:---:|
|`标签对象.innerText()`|`$(selector).text()`|
|`标签对象.innerHtml()`|`$(selector).html()`|

```js
$(selector).html([val|fn]);  // 取得第一个匹配元素的html内容
$(selector).text([val|fn]);  // 取得所有匹配元素的内容。
$(selector).val([val|fn|arr]); // 获得匹配元素的当前值
```
> 1. 无参数表示获取值
> 2. 有参数表示修改值



