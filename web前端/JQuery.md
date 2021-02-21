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
|`标签对象.innerText()`|`$(selector).text(val)`|
|`标签对象.innerHtml()`|`$(selector).html(val)`|
|`标签对象.files[0]`|`$(selector)[index].files[1]`|
|`标签对象.value`|`$(selector).val(val)`|
```js
$(selector).html([val|fn]);  // 取得第一个匹配元素的html内容
$(selector).text([val|fn]);  // 取得所有匹配元素的内容。
​```js
$(selector).val([val|fn|arr]); // 获取文本框中的值，或设置文本框的值(value属性的)
$(selector)[index].files[0]; // 获取文件对象
```

> 1. 无参数表示获取值
> 2. 有参数表示修改值

## 4.6 属性操作
|js操作|jQuery操作|
|:---:|:---:|
|`标签对象.setAttribute()`|`$(selector).attr(name, value)`|
|`标签对象.getAttribute()`|`$(selector).attr(name)`|
|`标签对象.removeAttribute()`|`$(selector).removeAttr(name)`|

```js

```
> **针对用户选择的标签`checkbox` `select`使用`$(selector).prop(name, value)`进行操作**

## 4.7 文档处理
|js操作|jQuery操作|
|:---:|:---:|
|`createElement("标签名")`|`$("标签")`|
|内部添加||
|`appendChild(标签对象)`|`$(selector).append(content|fn)`|
||`$("标签").appendTo($(selector))`|
|``|`$(selector).prepend(content|fn)`|
||`$("标签").prependTo($(selector))`|
|外部添加||
||`$(selector).after(content|fn)`|
||`$("标签").insertAfter($(selector))`|
||`$(selector).before(content|fn)`|
||`$("标签").insertBefore($(selector))`|
|删除标签||
||`$(selector).empty()`|
||`$(selector).remove([expr])`|
||`$(selector).detach([expr])`|

![](https://images.gitee.com/uploads/images/2020/1206/224310_d150100d_7841459.png "屏幕截图.png")

# 五、事件操作
**jquery中的事件** 

![输入图片说明](https://images.gitee.com/uploads/images/2020/1206/230312_3339b21f_7841459.png "屏幕截图.png")

## 5.1 jQuery事件的绑定
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>事件绑定</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
</head>
<body>
<button id="d1">第一种</button>
<button id="d2">第二种</button>

<script>
    // 第一种
    $("#d1").click(function () {
            alert("不要说话");
        }
    );
    // 第二种
    $("#d2").on("click", function () {
        alert("来跳舞");
    });
</script>
</body>
</html>
```

## 5.2 事件实例

**点击复制**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>事件实例</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
</head>
<body>
<button id="d1">点击复制</button>

<script>

    $("#d1").on("click", function () {
        let $btnEle = $(this).clone(true);  // 克隆一份, 默认至克隆html和css，不克隆事件, true指定克隆事件
        $btnEle.insertAfter("body");
    })

</script>

</body>
</html>
```
> 1. `this`: 当前操作的标签对象
> 2. `$(selector).clone(false)`: 克隆一份，默认不复制事件。true: 复制事件

**模态框的出现与消失**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        body {
            margin: 0;
        }
        .cover {
            position: fixed;
            left: 0;
            right: 0;
            top: 0;
            bottom: 0;
            background-color: rgba(127,127,127, 0.5);
            z-index: 999;
        }
        .modal {
            background-color: white;
            height: 200px;
            width: 300px;
            position: fixed;
            left: 50%;
            top: 50%;
            z-index: 999;
            margin-left: -150px;
            margin-top: -100px;

        }
        .hide {
            display: none;
        }

    </style>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
</head>
<body>

<div>
    <h1>正常内容</h1>
    <a href="">hello</a>
</div>
<button id="show">出现</button>
<div class="cover hide"></div>

<div class="modal hide">
    <h1>登录页面</h1>
    <p>username: <label>
        <input type="text">
    </label></p>
    <p>password: <label>
        <input type="password">
    </label></p>
    <input type="button" value="提交" id="submit">
    <input type="button" value="取消" id="cancel">
</div>

<script>
    let $coverEle = $(".cover")
    let $modalEle = $(".modal")
    // 出现模态框
    $("#show").on("click", function () {
        $coverEle.removeClass("hide")
        $modalEle.removeClass("hide")
    })

    // 取消模态框
    $("#cancel").click(function () {
        $coverEle.addClass("hide")
        $modalEle.addClass("hide")
    })

</script>

</body>
</html>
```

**点击某个标签展示其下面的内容**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>小标题</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
    <style>
        body {
            margin: 0;
        }
        .left {
            float: left;
            background-color: darkgray;
            width: 20%;
            height: 100%;
            position: fixed;
        }
        .title {
            font-size: 28px;
            color: white;
            text-align: center;
        }
        .items {
            border: 1px solid black;
        }
        .hide {
            display: none;
        }
    </style>
</head>
<body>
<div class="left">

    <div class="menu">
        <div class="title">一
            <div class="items hide">111</div>
            <div class="items hide">222</div>
            <div class="items hide">333</div>
        </div>

        <div class="title">二
            <div class="items hide">111</div>
            <div class="items hide">222</div>
            <div class="items hide">333</div>
        </div>

        <div class="title">三
            <div class="items hide">111</div>
            <div class="items hide">222</div>
            <div class="items hide">333</div>
        </div>
    </div>

</div>

<script>
    $(".title").click(function () {
        $(".items").addClass('hide')
        $(this).children().removeClass("hide")
    })
</script>
</body>
</html>
```

**返回顶部**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>返回顶部</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
    <style>
        .hide {
            display: none;
        }

        #d1 {
            position: fixed;
            background-color: black;
            right: 20px;
            bottom: 20px;
            height: 50px;
            width: 100px;
            text-align: center;
            line-height: 50px;
        }

    </style>
</head>
<body>
<a href="" id="d1" class="hide">回到顶部</a>
<div style="height: 500px; background-color: rebeccapurple"></div>
<div style="height: 500px; background-color: gray"></div>
<div style="height: 500px; background-color: greenyellow"></div>


<script>
    let $window = $(window);
    let $aEle = $("#d1");
    $window.scroll(function () {
        if($window.scrollTop() > 500) {
            $aEle.removeClass("hide")
        }else {
            $aEle.addClass("hide")
        }
        console.log($window.scrollTop())
    })
    $aEle.click(function () {
        $window.scrollTop(0);
        console.log($window.scrollTop())
    })

</script>
</body>
</html>
```
**自定义登录校验**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
</head>
<body>
<p>
    username: <input type="text" id="username">
    <span style="color: red"></span>
</p>
<p>
    password:<input type="password" id="password">
    <span style="color: red"></span>
</p>
<p><input type="button" id="btn" value="提交"></p>

<script>
    let $userName = $("#username");
    let $passWord = $("#password");
    $("#btn").click(function () {
        // 获取用户输入的用户名和密码
        let userName = $userName.val();
        let passWord = $passWord.val();

        if (!userName) {
            $userName.next().text("用户名不能为空");
        } else {
            $userName.next().text("")
        }

        if(!passWord) {
            $passWord.next().text("密码不能为空");
        } else {
            $passWord.next().text("")
        }

    })
    $("input").focus(function () {
        $(this).next().text("")
    })

</script>

</body>
</html>
```

**input框实时监控**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>输入框实时监控</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
</head>
<body>
<input type="text" id="d1">

<script>
    $("#d1").on("input",function () {
        console.log(this.value)
    })
    
</script>

</body>
</html>
```

**hover事件**
> 内部封装了两个事件: `鼠标移入悬停，鼠标移出`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>hover事件</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
</head>
<body>
<p id="d1">hello world</p>

<script>
    $("#d1").hover(function () {
        console.log("鼠标悬停")
    }, function () {
        console.log("鼠标移出")
    })
</script>

</body>
</html>
```

**键盘按下事件**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>键盘按下事件</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
</head>
<body>

<script>
    $(window).keydown(function (event) {
        console.log(event.keyCode); // keyCode对应字符的ascii码
    });
</script>
</body>
</html>
```

**阻止后续事件执行**
```html
<form action="">
    <span id="d1" style="color:red;"></span>
    <input type="submit" id="d2">
</form>

<script>
    $("#d2").click(function (event) {
        $("#d1").text("提交完成")
        // 阻止标签后续事件执行
        // 方式1
        // return false
        // 方式2
        event.preventDefault()

    })
</script>
```

**阻止事件冒泡**
```html
<div id="d1"> div
    <p id="d2"> p
        <span id="d3">span</span>
    </p>
</div>

<script>
    // 对于标签的某一个事件被触发，会寻找其父标签对应事件，并执行
    $("#d1").click(function () {
        alert("div")
    })

    $("#d2").click(function (e) {
        alert("p")
        e.stopPropagation()  // 阻止事件冒泡
    })

    $("#d3").click(function () {
        alert("span")
        return false // 阻止事件冒泡
    })
</script>
```

**事件委托**
```html
<button>委托</button>

<script>
    /*
    // 给button绑定点击事件
    $("button").click(function () {
            alert(123)
        }
    )
    // 动态创建的button没有点击事件
    let $btnEle = $("<button>")
    $btnEle.text("你好啊")
    $("body").append($btnEle)
    */

    // 事件委托
    $("body").on("click", "button", function () {
        alert(123)
    });  // 将body中所有的click事件委托给button按钮出发
    // 无论是动态创建的还是写好的都可以触发。

</script>
```

**页面加载**
```html
<script>
    $(document).ready(function () {
        
    })  // 等待document加载完毕后执行function
    $(function () {
        // js代码
    }) // 等待页面加载完毕执行
</script>
```

# 六、动画效果
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>页面动画</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
    <style>
        #d1 {
            background-color: red;
            width: 20%;
            height: 1000px;
        }
    </style>
</head>
<body>
<div id="d1"></div>

<script>
    let $divEle = $("#d1");
    $divEle.hide(5000);  // 5秒后隐藏
    $divEle.show(5000);  // 5秒后展示
    $divEle.slideUp(5000);  // 5秒后向上消失
    $divEle.slideDown(5000);  // 5秒后向下出现
    $divEle.fadeOut(5000); // 5秒渐变消失
    $divEle.fadeIn(5000);  // 5秒渐变出现
    $divEle.fadeTo(5000, 0.4);  // 5秒渐变到0.4透明度
</script>
</body>
</html>
```

**补充**
```js
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>each函数</title>
    <script src="../JavaScript/JQuery-3.5.1.js"></script>
    <style>
        #d1 {
            background-color: red;
            width: 20%;
            height: 1000px;
        }
    </style>
</head>
<body>
<div></div>
<div></div>
<div></div>
<div></div>
<div></div>
<div></div>
<div></div>
<div></div>
<div></div>
<div></div>
<script>
    
    $("div").each(function (index, obj) {
        console.log(index, obj)
    })
    
    $.each([1,2,3,4,5], function (index, obj) {
        console.log(index, obj)
    })
    
</script>
</body>
</html>
```
> **each相当于一个for循环**


```js
$("div").data("info", "你快回来"); // 临时存储数据，用户不能看见
$("div").first().data("info") // 获取数据
$("div").first().removeData("info");  // 删除数据
```





