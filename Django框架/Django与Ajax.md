# 一、Ajax简介
Ajax 是一种在无需重新加载整个网页的情况下，能够更新部分网页的技术。**异步提交，局部刷新**
## 1.1 什么是 AJAX ？
* AJAX = 异步 JavaScript 和 XML。
* AJAX 是一种用于创建快速动态网页的技术。
* 通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。
* 传统的网页（不使用 AJAX）如果需要更新内容，必需重载整个网页面。
* 有很多使用 AJAX 的应用程序案例：新浪微博、Google 地图、开心网、GitHub注册等等

## 1.2 工作原理
![](https://images.gitee.com/uploads/images/2020/1213/133757_eb32eb3f_7841459.png "ajax-yl.png")

# 二、JQuery封装的Ajax
## 2.1 基础语法
```js
$.ajax({
    // 1. 指定提交地址
    url:'', // 与form表单规律一样
    // 2. 指定请求方式
    type: 'post', // 不指定默认为get
    // 3. 提交的数据
    data: { },
    dataType:'JSON', // 后端返回的是json格式字符串的数据时，自动反序列化
    // 4. 回调函数 后端返回结果后自动触发， args: 后端返回的结果
    success: function (args) {
        $("#d3").val(args)
    }
})
```
> 1. 后端使用`HttpResponse`返回数据，不会自动反序列化
> 2. 后端使用`JsonResponse`返回的数据，会自动反序列化

## 2.2 提交json格式数据
**前后端传输数据时，一定要确保编码格式与数据真正编码格式是一致的.** 

```js
$.ajax({
    url:'',
    type:'post',
    data: JSON.stringify({
        'username': 'dyp',
        'password': 28
    }),  // 数据转为json格式  {"username":"dyp","password":28}
    contentType: 'application/json',  // 自定编码格式
    success: function (args) {

    }
})
```
> 1. 发送`json`格式的数据，Django后端不会做任何处理，直接保存在`request.body`之中
> 2. 对于json数据，要在Django后端使用json模块自己处理

## 2.3 提交文件

```js
// 需要先生成一个FormData对象
let form_data = new FormData()
// 添加普通键值对
form_data.append('username', $("#d1").val())
form_data.append('password', $("#d2").val())
// 添加文件对象
form_data.append('file', $("#d3")[0].files[0])
// 将对象发生给后端
$.ajax({
    url: '',
    type: 'post',
    data:form_data,
    // ajax发送文件必须使用参数
    contentType: false,  // 不需要使用任何编码, django后端可以识别FormData对象
    processData: false,  // 不对数据进行任何处理

    success: function (args) {

    }

})
```
> 1. 需要内置对象`FormData`
> 2. ajax指定参数:`contentType: false 和 processData: false`
> 3. Django后端会将普通文本解析到`request.POST`, 文件数据解析到`request.FILES`

# 三、前后端传输数据的编码格式
1. `application/x-www-form-urlencoded`
2. `multipart/form-data`
3. `json`

## 3.1 `form`表单`post`请求的编码格式
* 默认的数据编码格式: `application/x-www-form-urlencoded`
    * 数据组织格式为`username=111&password=111`向后端提交数据
    * `Django`后端将符合`application/x-www-form-urlencoded`格式组织的数据解析封装到了`request.POST`之中

* `multipart/form-data`
    * `Django`后端将普通的键值对解析到`request.POST`中
    * `Django`后端将文件解析到`request.FILES`中

* `form`表单无法发送`json`格式数据


## 3.2 `Ajax`的`post`请求的数据编码格式
* 默认编码: `application/x-www-form-urlencoded`












