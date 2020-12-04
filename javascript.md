# 一、JavaScript简介
JavaScript 是互联网上最流行的脚本语言，这门语言可用于 HTML 和 web，更可广泛用于服务器、PC、笔记本电脑、平板电脑和智能手机等设备

**特点**
* JavaScript 是一种轻量级的编程语言。
* JavaScript 是可插入 HTML 页面的编程代码。
    1. 在`script`标签之间书写js代码
    2. `<script src=""></script>`中的src引入外部js代码
* JavaScript 插入 HTML 页面后，可由所有的现代浏览器执行。
* JavaScript 很容易学习。


> 1. 以`{}`为作用域
> 2. 以`;`作为一行语句的结束符

# 二、变量与常量

## 2.1 变量的定义(`var`, `let`)

**定义变量的关键字: `var`, `let`**
> 1. `var`定义的变量的作用域为全局变量。(**不区分全局和局部变量**)
> 2. `let`定义的变量作用域为定义变量的位置。（**区分全局和局部变量**）

```javascript
/*1. var name="小明";*/
var var_name = value;

/*2. let name="小明";*/
let var_name = value; /*es6新语法*/
```

> **变量命名规范** 
> 1. 变量名只能是由 数字、字母、下划线和`$`组成
> 2. 推荐使用驼峰命名规范
> 3. 变量名不能使用关键字

## 2.2 常量的定义(`const`)
在`js`中有限制只读关键字`const`，用于定义为常量
```javascript
const const_name=value
```

# 三、数据类型
**`js`是动态语言, 定义变量是不需要指定数据类型。** 
## 3.1 数值类型(`number`)
```javascript
var a = 11; /*整型*/
var b = 11.11;  /*浮点型*/
typeof var_name; /*查看数据类型*/

var c = NaN; /*not a number 表示不是一个数字*/

/*类型转换*/
parseInt(arg); // 将 arg转为整数，arg是字符串
parseFloat(arg); // 将arg转为浮点数， arg是字符串
```
> 1. `parseInt(arg)`: 将arg是开头的数字转为整数
> 2. `parseFloat(arg)`: 将arg开头的数字转为浮点型
> 3. 如果`arg`没有以数字开头转换为`NaN`

## 3.2 字符串类型(`string`)
```javascript
var string_name="...";
var string_name='...';
var string_name=new String(""); // 不要创建 String 对象。它会拖慢执行速度，并可能产生其他副作用
```
> 1. 不支持三引号定义字符串
> 2. 模板字符串: "``"，原样保存字符串
> 3. 创建字符串时，不要创建为对象

```javascript
var string_name=`多行字符串或模板字符串`;
```
> 模板字符串可以拼接字符串：`${var_name}`，用于格式化字符串
![输入图片说明](https://images.gitee.com/uploads/images/2020/1202/205733_ea834de0_7841459.png "屏幕截图.png")
> 1. 如果`${var_name}`中`var_name`在之前没有定义，则报错
> 2. 字符串拼接: 推荐使用`+`拼接字符串

### 字符串常用方法
1. 获取字符串的长度: `string.length`
2. 移除字符串两边的空白: `string.trim()`，没有参数
3. 移除字符串左边的空白: `string.trimLeft()`
4. 移除字符串右边的空白: `string.trimRight()`
5. 获取指定索引处的值: `string.charAt(index)`
6. 拼接字符串: `string.concat(value1,...)`
7. 获取子序列位置: `string.indexOf(substring, start)`
8. 获取子序列: `string.substring(from， to)`，不支持负数。
9. 切片: `string.slice(start, end)`
10. 小写: `string.toLowerCase()`
11. 大写: `string.toUpperCase()`
12. 分割: `string.split(delimiter, limit)`，拿出`limit`个元素

```js
// 字符串
var s1 = "  abc  ";
// var s2 = new String("abc");
typeof s1
// typeof s2
s1.length

s1.trim()  // 移除两边的空白
s1.trimLeft()  // 移除左边的空白  trimStart()
s1.trimRight()  // 移除右边的空白 trimEnd()
s1.charAt(3)  // 获取索引为3的字符
s1.indexOf("abc")   // 返回abc串在s1中的位置
s1.slice(0, 3)
```

## 3.3 布尔值(`true`, `false`; `[boolean]`)
布尔值表示真假的值。`true`: 真；`false`: 假
> 1. false对应值: 空字符串、0、null、undefined、NaN
> 2. null与undefined的区别
>     * `null`: 表示值为空, 常用于清空值
>     * `undefined`: 表示变量以声明，但是没有初始化。函数没有指定返回值时，返回`undefined`

## 3.4 对象类型(`object`)
### 3.4.1 数组对象(`[]`)
类似于`python`中的列表
```js
// 数组
var array = [1, 2, 3, 4, 5, 'lll']
typeof array

array.length
array.push("sss"); // 尾部添加元素
array.pop();  // 弹出尾部元素
array.unshift("head"); // 头部插入元素
array.shift();  // 删除头部元素
array.slice(0, 3); // 切片
array.reverse();  // 反序
array.join(",");  // 以`,`为分隔符将array数组元素拼接成字符串， 于python相反
array.concat([6,7,8]);  // 将[6,7,8]放到数组array中,新返回一个数组，extend
array.sort();  // 排序

// forEach()
var new_array = [111,222,333,444,555]
new_array.forEach(function (value, index,arr) {
    console.log(value, index, arr)
}, new_array);  // 获取new_array中的每一个元素，交给function执行value: 获取到的值，index:当前值的索引，arr: 数据来源

// splice
new_array.splice(0, 3, 8); // 从0开始删除3个元素, 添加元素8
new_array.splice(0, 3, [9, 10, 11]); // 从0开始删除3个元素, 添加元素[9, 10, 11]

// map
new_array.map(function (value,index,arr) {
    console.log(value, index, arr);
    return value * 2
}, new_array); // value: 从数组中获取的值，index: 值的索引, arr: 值的来源，有返回值，返回值被保存到一个数组中
```

### 3.4.2 自定义对象(`{}`)
类似于`python`中的字典

```js
var d = {"name": "json", "age": 18} // 创建自定义对象
typeof d // object

d["name"]; // 取值
d.name;
for(let i in d){
    /*i获取到自定义对象的键*/
    console.log(i, d[i])
}

var d2 = new Object();  // 创建一个空自定义对象
/*关键字new可以创建所有对象*/
// 添加属性
d2.name = "小明"
d2.age = 20
```

### 3.4.3 date对象
```js
var date = new Date();  // 创建时间日期对象，自动获取当前时间
date.toLocaleString();  // 转为方便查看的时间字符串
date.getDate(); // 获取日期
date.getDay(); // 获取星期数
date.getMonth(); // 获取月份(0, 11)
date.getFullYear(); // 获取年份(完整年份)
date.getHours();  // 获取时
date.getTime();  // 获取时间戳
...

```

### 3.4.4 json对象
```js
JSON.stringify()  /*序列化为json字符串*/
JSON.parse() /*反序列化字符串*/
```
![JSON对象](https://images.gitee.com/uploads/images/2020/1203/172550_af14b1f2_7841459.png "屏幕截图.png")

### 3.4.5 `RegExp`对象(正则对象)
```js

/*正则*/
let reg1 = new RegExp("^[a-zA-Z][a-zA-Z0-9]{5,11}");  // 定义正则对象
let reg2 = /^[a-zA-Z][a-zA-Z0-9]{5,11}/;  // 定义正则
reg1.test("abcd111");  // 匹配数据
reg1.test(); // 返回true, 默认传参undefined

/*正则匹配方法*/
let ss = "abcdsss22";
ss.match(/s/g)  // g表示全局匹配。查找所有匹配而非在找到第一个匹配后停止，对于全局匹配的
```
![输入图片说明](https://images.gitee.com/uploads/images/2020/1204/003001_6b97151e_7841459.png "屏幕截图.png")
![输入图片说明](https://images.gitee.com/uploads/images/2020/1204/003224_1f70fc46_7841459.png "屏幕截图.png")

## 3.5 运算符
运算符中需要注意的点。其他的同python
```js
var num = 10;
var res1 = num++;  // num=11, res1=10; ++自增运算符。先赋值在自增
var res2 = ++num; // num=12, res2=12；先自增在赋值

1=="1";  // true, 值相等，自动转为相同类型比较
1 !="1"; // false, 值不相等
1 === "1";  // false，值和数据类型都要相等，不执行类型转换
1 !== "1"; // true, 值相等，数据类型不同

/*逻辑运算符，于C语言一样*/
true && true; // true
true && false; // false , 遇到false返回false
5 && "5"; // "5"

true || false; // true, 遇到true返回true
false || false; // false
!5 || '4'; // '4'

!true; // false

!false; // true
```

# 四、流程控制
参考C语言的流程控制语句
```js
/*if语句*/
var age = 8;

if(age < 10){
    console.log("小朋友，你好");
} else if (age > 15) { /*else要紧跟则上衣个if的右括号`}`*/
    console.log("你还可以玩几年")
} else {
    console.log("好好学习，别玩了")
}

/*switch case语句*/
var age1 = 13;

switch (parseInt(age1/10)) {
    case 0:
        console.log("你好");
        break; /*如果没有break则匹配到后，则一直执行*/
    case 1:
        console.log("该长大了");
        break;
    default:  /*没有匹配到值*/
        console.log("恭喜成年")
        break;
}


/*for循环*/
for(let i=0; i< 10; i++) {
    /*初始循环变量;条件;循环变量的变化*/
    console.log(i) /*循环体执行的代码*/
}

for (let i = 0; i < array.length; i++) {
    console.log(array[i])
}

/*while循环*/
var i = 0;
while (i < 10) {
    /*条件*/
    console.log(i)
    i++;
}

/*三目运算符*/
res = 3>2? true:false // 条件成立返回true，不成立返回false
```

# 五、函数(`function`)
```js
function fun1() {
    console.log("hello world")
}

function fun2(a, b) {
    console.log(a, b);
    return a + b;  // 返回值，如果返回多个值，只能获取到最后一个值。如果返回多个值，需要自己包装成一个数组。
}

fun1()  // 调用函数
fun2(3, 4)  // 调用时，参数传递太多，和传递太少均不会报错。没有接收到参数用undefined代替

/*限制参数传递*/
function func3(a, b) {
    console.log(arguments);  // 获取到传入函数的所有参数
    if (arguments.length !== 2) {
        console.log("参数传递不正确");
    }
    /*参数正确执行*/
}

/*匿名函数*/
function () {
    console.log("匿名函数");
}

/*箭头函数*/
var func1 = v => v; // 等价于
         /*参数 返回值*/
var func2 = function (v) {
    return v
}

var func3 = (arg1, arg2) => arg1 + arg2;
            /*多个参数           返回值*/
```
> **全局变量与局部变量**: 与`python`变量名查找顺序一致。

# 六、BOM操作
> **浏览器对象模型: 使用js代码操作浏览器** 

**window对象**: 浏览器窗口对象
```js
window.innerHeight;  // 当前窗口的高度

window.innerWidth; // 当前窗口的宽度

window.open(url,target,features); // 新建浏览器窗口，打开指定url, tartget="", features="height=200px,width=100px"

window.close(); // 关闭当前网页
```
**window.navigator对象**
```js
window.navigator.appName;  // 

window.navigator.appVersion; // 浏览器版本

window.navigator.userAgent; // 标识当前是否为浏览器

window.navigator.platform; // 平台信息
```
> **window的子对象，可以省略window不写**

**window.history对象**
```js
window.history.back();  // 回退到上一次请求页面

window.history.forward();  //前进
```

**window.location对象**
![](https://images.gitee.com/uploads/images/2020/1204/112051_3b67b5b9_7841459.png "屏幕截图.png")
```js
window.location.href; // 获取当前页面的url
window.location.href=url; // 页面跳转到url
window.location.reload();  // 刷新页面
```

**弹框**
```js
/*警告框*/
alert("你不要过来啊");
/*确认框*/
confirm("你确定码？");
/*输入提示框*/
prompt("输入号码", "默认值")
```
![输入图片说明](https://images.gitee.com/uploads/images/2020/1204/112914_fe8a7305_7841459.png "屏幕截图.png")

**计时器**
```js
/*过一段时间后触发一次*/
function func1() {
    alert(123);
}

let t = setTimeout(func1, 3000);  // 3秒后执行func1函数

clearTimeout(t); // 取消定时任务

/*每隔一段时间触发(循环)*/
function func2() {
    alert(123)
}
function show() {
    let t = setInterval(func2, 3000);  // 每隔三秒执行一次func2(循环定时任务)
    function inner() {
        clearInterval(t);
    }
    setTimeout(inner, 9000);  // 九秒后触发inner函数
}
show()
```

# 七、DOM操作
> 1. **文档对象模型: 使用js代码操作html页面** 
> 2. **document关键字**

## 7.1 查找标签
**直接查找**
```js
document.getElementById("d1"); // 通过id查找元素
document.getElementsByClassName("c1"); // 通过class查找元素
document.getElementsByTagName("div"); // 通过标签名查找元素
```
![](https://images.gitee.com/uploads/images/2020/1204/115240_409207ee_7841459.png "屏幕截图.png")
> **使用变量接收标签对象时，通常命名为`xxxEle`**


**间接查找**
```js
标签对象.parentElement; // 获取父标签
标签对象.children;  // 获取子代标签，返回数组
标签对象.firstElementChild;  // 获取第一个子代标签
标签对象.lastElementChild; // 获取最后一个子代标签
标签对象.nextElementSibling;  // 获取相邻的下一个兄弟标签
标签对象.previousElementSibling;  // 获取相邻的上一个兄弟标签
```
![](https://images.gitee.com/uploads/images/2020/1204/120635_f17a387c_7841459.png "屏幕截图.png")

## 7.2 节点操作
1. 创建标签，并添加属性，插入到某个标签的后面的文档
```js
let imgEle = document.createElement("img");  // 创建标签

imgEle.src="喜羊羊.png"; // 添加默认属性

imgEle.setAttribute("username", "dyp"); // 设置属性，可以是自定义属性

imgEle.setAttribute("title", "喜羊羊"); // 设置属性，也可以是默认属性

let divEle=document.getElementById("d1"); // 获取要插入标签的位置

divEle.appendChild(imgEle)  // 添加子代标签
```
![](https://images.gitee.com/uploads/images/2020/1204/121639_d7185c30_7841459.png "屏幕截图.png")

2. 创建标签，并添加属性，添加文本内容，插入到某个标签的上边的文档
```js
let aEle=document.createElement("a"); //

aEle.href="https://www.baidu.com"; // 给标签添加默认属性

aEle.innerText="百度"; // 给标签添加文本内容

let divEle=document.getElementById("d1"); //

let pEle=document.getElementById("d2");  //

divEle.insertBefore(aEle, pEle);  // 插入标签到div内部的p标签之前
```
![](https://images.gitee.com/uploads/images/2020/1204/151352_d5f039d8_7841459.png "屏幕截图.png")

* `innerText`: 获取到的是标签中的文本。对其进行赋值时，只会识别为文本。
* `innerHTML`: 获取到的标签。对其进行赋值时，会识别标签。
* **如果对其进行赋值，会覆盖原来的内容**

3. 获取值操作
```js
标签对象.属性名;  // 获取属性值
标签对象.files[0];  // 获取文件
```
![](https://images.gitee.com/uploads/images/2020/1204/152718_2336ffb3_7841459.png "屏幕截图.png")
![输入图片说明](https://images.gitee.com/uploads/images/2020/1204/152948_5adffa32_7841459.png "屏幕截图.png")

4. 属性操作
```js
let divEle = document.getElementById("d1")

divEle.classList;  // 获取标签的类属性，类属性值

divEle.classList.remove("bg_red")  // 移除类属性值

divEle.classList.add("bg_red") // 添加类属性值

divEle.classList.contains("c1") // 判断是否包含类属性值

divEle.classList.contains("c2")  

divEle.classList.toggle("bg_red")  // 有指定类属性则删除

divEle.classList.toggle("bg_red")  // 无指定类属性则添加

标签对象.style.CSS属性名="属性值";  // 修改标签的css属性
```
![](https://images.gitee.com/uploads/images/2020/1204/153819_1605e223_7841459.png "屏幕截图.png")

![](https://images.gitee.com/uploads/images/2020/1204/154320_90d9cb3e_7841459.png "屏幕截图.png")

## 7.3 事件
一些列的动作，在一定的条件执行执行。

### 7.3.1 绑定事件的方法
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DOM</title>

</head>
<body>
<button onclick="func()">点击弹出123</button> <!--通过标签绑定事件-->
<button id="d1">点击弹出456</button>

<script>
    function func() {
        alert(123)
    }

    /*第二种绑定事件 获取标签绑定事件*/
    let btnEle = document.getElementById("d1")
    btnEle.onclick = function () {
        alert(456)
    }
</script>
</body>
</html>
```
> **`script`标签通常放在`body`标签的最底部**
> ```js
>    window.onload = function () {
>        /*等待浏览器窗口加载完毕后执行*/
>    }
>```





