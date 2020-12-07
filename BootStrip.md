# 一、简介
bootstrap框架用于快速搭建前端页面。提供的多种的样式。调节样式也只需要使用class属性进行调节。 **响应式布局** ： 用于自适应显示器大小

[参考文档](https://v3.bootcss.com/)

**引入bootstrap**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>bootstrap起步</title>
    <link rel="stylesheet" href="./bootstrap/css/bootstrap.css">
    <script src="./bootstrap/js/JQuery-3.5.1.js"></script>
    <script src="./bootstrap/js/bootstrap.js"></script>   <!--bootstrap依赖jQuery-->
</head>
<body>

</body>
</html>
```

**布局容器**

`Bootstrap`需要为页面内容和栅格系统包裹一个 `.container` 容器。我们提供了两个作此用处的类。注意，由于`padding`等属性的原因，这两种 容器类不能互相嵌套
```html
<!--用于固定宽度并支持响应式布局的容器-->
<div class="container"> 
  ...
</div>

<!--类用于 100% 宽度，占据全部视口（viewport）的容器-->
<div class="container-fluid"> 
  ...
</div>
```
> **bootstrap布局的网页都写在`.container` 或 `.container-fluid`之中**

# 二、栅格系统
栅格系统用于通过一系列的行（`row`）与列（`column`）的组合来创建页面布局，你的内容就可以放入这些创建好的布局中
* `.row`: 将一行分为12列
* 媒体查询
    ```
    /* 超小屏幕（手机，小于 768px） */
    /* 没有任何媒体查询相关的代码，因为这在 Bootstrap 中是默认的（还记得 Bootstrap 是移动设备优先的吗？） */
    
    /* 小屏幕（平板，大于等于 768px） */
    @media (min-width: @screen-sm-min) { ... }
    
    /* 中等屏幕（桌面显示器，大于等于 992px） */
    @media (min-width: @screen-md-min) { ... }
    
    /* 大屏幕（大桌面显示器，大于等于 1200px） */
    @media (min-width: @screen-lg-min) { ... }
    ```
* 栅格参数
   ![输入图片说明](https://images.gitee.com/uploads/images/2020/1207/133119_1da26393_7841459.png "屏幕截图.png")
   **将这些类都添加上，bootstrap会自动检测屏幕大小，进行布局**
* `.col-md-offset-i`: 从左向右移动i份

# 三、排版
## 3.1 标题排版
`HTML`中的所有标题标签，`<h1>` 到 `<h6>` 均可使用。另外，还提供了 `.h1` 到 `.h6` 类，为的是给内联（`inline`）属性的文本赋予标题的样式
```html
<!--标题-->
<h1>h1. Bootstrap heading</h1>
<h2>h1. Bootstrap heading</h2>
<h3>h1. Bootstrap heading</h3>
<h4>h1. Bootstrap heading</h4>
<h5>h1. Bootstrap heading</h5>
<h6>h1. Bootstrap heading</h6>
<span class="h2">.h2 span</span>
```
> **重写了h标签的样式，并提供class属性值`.hi`用于添加到`inline`标签中使用**
>
```html
<!--副标题-->
<h1>h1. Bootstrap heading <small>Secondary text</small></h1>
<h1>h1. Bootstrap heading <span class="small">Secondary text</span></h1>

```
> **标题内还可以包含 <small> 标签或赋予 .small 类的元素，可以用来标记副标题。**

## 3.2 文本排版
Bootstrap 将全局 `font-size: 14px;`，`line-height: 1.428;`。这些属性直接赋予 `<body>` 元素和所有段落`<p>`元素;
`<p> `标签还被设置了等于`1/2`行高（即 `10px`）的底部外边距（`margin`）;
添加 `.lead` 类可以让段落突出显示。
```html
<!--文本-->
<p class="lead">
    hello world
</p>
```

## 3.3 内联标签
高亮文本`<mark>`
```html
You can use the mark tag to <mark>highlight</mark> text.
```
被删除的文本`<del>`
```html
<del>This line of text is meant to be treated as deleted text.</del>
```
无用的文本`<s>`
```html
<s>This line of text is meant to be treated as deleted text.</s>
```
额外插入的文本`<ins>`
```html
<ins>This line of text is meant to be treated as an addition to the document.</ins>
```
文本添加下划线，使用`<u>` 
```html
<u>This line of text is meant to be treated as an addition to the document.</u>
```
改变文本的大小写
```html
<p class="text-lowercase">Lowercased text.</p>
<p class="text-uppercase">Uppercased text.</p>
<p class="text-capitalize">Capitalized text.</p>
```
缩略语
```html
<abbr title="attribute">attr</abbr>
```
**更多参考官方文档**

## 3.4 表格
* `.table`: 表格
* `.table-striped`: 条纹样式的表格
* `.table-hover`: 鼠标悬停加深颜色
* `.table-bordered`: 边框
* `.table-condensed`: 紧缩表格
* 设置单元格颜色
    ![](https://images.gitee.com/uploads/images/2020/1207/141700_0623001f_7841459.png "屏幕截图.png")

```html
<table class="table table-hover table-bordered text-center">
    <thead>
        <tr>
            <th>ID</th>
            <th>username</th>
            <th>password</th>
        </tr>
    </thead>
    <tbody>
        <tr class="active">
            <td>1</td>
            <td>香兰</td>
            <td>111</td>
        </tr>
        <tr class="success">
            <td>2</td>
            <td>香兰</td>
            <td>222</td>
        </tr>
        <tr class="info">
            <td>3</td>
            <td>香兰</td>
            <td>333</td>
        </tr>
        <tr class="warning">
            <td>4</td>
            <td>香兰</td>
            <td>444</td>
        </tr>
        <tr class="danger">
            <td>5</td>
            <td>香兰</td>
            <td>555</td>
        </tr>
    </tbody>

</table>
```
## 3.5 表单
* `.form-control`: `<input>`、`<textarea>` 和 `<select>` 设置了 `width: 100%;`。 将 `label` 元素和前面提到的控件包裹在 `.form-group` 中可以获得最好的排列
* `.form-inline`: `<form>`中添加，行内表单
```html
<h2 class="text-center">登录页面</h2>
<form action="">
    <div class="form-group">
        <label for="username">username</label>
        <input type="text" class="form-control" id="username">
    </div>
    <div class="form-group">
        <label for="password">password</label>
        <input type="password" class="form-control" id="password">
    </div>
    <button type="submit" class="btn btn-default">提交</button>
</form>

<h2>行内表单</h2>
<form action="" class="form-inline">
    <div class="form-group">
        <label for="username1">username</label>
        <input type="text" class="form-control" id="username1">
    </div>
    <div class="form-group">
        <label for="password1">password</label>
        <input type="password" class="form-control" id="password1">
    </div>
    <button type="submit" class="btn btn-default">Send invitation</button>

</form>
```

## 3.6 按钮
* `.btn`: 在标签`<a>、<button>` 或 `<input>`添加，将标签变为按钮
* 样式
    * `.btn-default`: 默认样式
    * `.btn-primary`: 首选项
    * `.btn-success`
    * `.btn-info`
    * `.btn-warning`
    * `.btn-danger`
    * `btn-link`
* 大小
    * `.btn-lg`: 大尺寸
    * `.btn-sm`：小尺寸
    * `.btn-xs`：超小尺寸
* `.btn-block`: 伸至父元素100%的宽度
* `.active`: 激活状态

```html
<h2>按钮</h2>
<a href="" class="btn btn-default btn-success">Link</a>
<input type="button" class="btn btn-default btn-lg btn-block" value="Input">
```

## 3.7 图片
* `.img-responsive`: 响应式图片
* `.block-center`: 居中
* 图片样式
    * `.img-rounded`
    * `.img-circle`
    * `.img-thumbnail`

```html
<img src="喜羊羊.png" alt="..." class="img-rounded img-responsive">
<img src="喜羊羊.png" alt="..." class="img-circle center-block">
<img src="喜羊羊.png" alt="..." class="img-thumbnail ">
```

# 四、组件
## 4.1 字体图标
在`<span>`标签中添加class属性值，确定图标. 这些都是文本，修改文本的样式即可修改图标样式

[glyphicons](https://v3.bootcss.com/components/#glyphicons)：bootstrap组件

[Font Awesome](http://www.fontawesome.com.cn/): font awesome组件，兼容bootstrap组件

## 4.2 下拉菜单
参见：https://v3.bootcss.com/components/#dropdowns

## 4.3 导航条
参见: https://v3.bootcss.com/components/#navbar
```html
class="navbar navbar-default"  白色
class="navbar navbar-inverse"  黑色
```

## 4.4 分页
参见：https://v3.bootcss.com/components/#pagination

## 4.5 弹出框
参见: https://lipis.github.io/bootstrap-sweetalert/

## 4.6 进度条
参见：https://v3.bootcss.com/components/#progress

## 4.7 媒体对象
参见：https://v3.bootcss.com/components/#media

## 4.8 列表组
参见: https://v3.bootcss.com/components/#list-group

## 4.9 面板
参见：https://v3.bootcss.com/components/#panels

# 五、js插件
参见：https://v3.bootcss.com/javascript/

模态框: https://v3.bootcss.com/javascript/#modals

标签页: https://v3.bootcss.com/javascript/#tabs









