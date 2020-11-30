# 一、CSS简介
* CSS 指层叠样式表 (Cascading Style Sheets) 
* 样式定义如何显示 HTML 元素 
* 样式通常存储在样式表中 
* 把样式添加到 HTML 4.0 中，是为了解决内容与表现分离的问题 
* 外部样式表可以极大提高工作效率 
* 外部样式表通常存储在 CSS 文件中 
* 多个样式定义可层叠为一 
* 目的：分离页面结构与页面样式

# 二、CSS的引入方式
* 内联样式
  * 在标签的`style`属性书写CSS样式
  * `<p style="color: red;">color</p>`
  * 可以写多个样式，每个样式用分号隔开
  
* 内部样式
  * 在head标签中添加style标签，将CSS样式书写在style标签里面
```html
<head>
    <style>
        css样式
    </style>
</head>
```

* 外联样式
  * 在head标签中用link标签将css文件引入到html页面中
  * <link rel="stylesheet" href="">
    * rel 引入内容调用
    * href css文件的路径地址
```html
<head>
    <link rel="stylesheet" href="url">
</head>
```

* 导入样式
```html
<head>
    <style>
        @import url("statics/css");
    </style>
</head>
```

**样式优先级: 行内样式>内部样式>外联样式>导入样式**
```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>CSS的引入方式</title>
    <!--内部引入-->
    <style>
        h1 {
            color: chartreuse;
        }
    </style>
    <link rel="stylesheet" href="../CSS/mycss.css">  <!--常用用的引入方式-->

</head>
<body>
    <h1 style="color: yellow;">Hello World</h1>  <!--行内引入一般不用-->
</body>
</html>
```


# 三、CSS基础语法
* CSS 规则由两个主要的部分构成：选择器，以及一条或多条声明。
  * `selector {declaration1; declaration2; ... declarationN }`
  * 选择器通常是您需要改变样式的 HTML 元素。
  * 每条声明由一个属性和一个值组成。
    * 属性（property）是您希望设置的样式属性（style attribute）。
    每个属性有一个值。属性和值被冒号分开。
      * `selector {property: value}`

* 注释
  * `/*被注释的CSS样式*/`

# 四、CSS选择器

## 4.1 基本选择器
```css
/*id选择器*/
#div1 { /*选择id为div1的标签*/
    color: greenyellow;
}
/*类选择器*/
.p_class { /*选择class包含p_class的标签*/
    color: red;
}
/*标签选择器*/
span { /*选择所有的span标签*/
    color: darkblue;
}
/*通配符选择器*/
* { /*选择页面上的所有标签*/
    color: brown;
}
```

## 4.2 CSS高级选择器
### 4.2.1 组合选择器
```css
/*后代选择器*/
div span { /*选择div标签中的所有span标签*/
    color: red;
}
/*子代选择器*/
div > span { /*选择div中的第一级span标签*/
    color: red;
}
/*相邻兄弟选择器*/
div + span { /*选择与div相邻的span标签*/
    color: red;
}
/*兄弟选择器*/
div ~ span { /*选择与div同级的后面的所有span标签*/
    color: red;
}
```

### 4.2.2 属性选择器
```css
/*属性选择器*/
[username] { /*选择具有username属性的标签*/
    background-color: greenyellow;
}

[username="xx"] { /*选择属性username值为xx的标签*/
    background-color: green;
}

p[username] {  /*选择含有username属性的p标签*/
    background-color: wheat;
}

input[username="yy"] {/*选择含有username属性且属性值为yy的input标签*/
    background-color: greenyellow;
}
```
### 4.2.3 分组与嵌套
```css
/*并集选择器*/
div, p, span { /*选择div，p，span标签*/
    color: red;
}
#d1,.c1,span {
    color: red;
}
```

### 4.2.4 伪类选择器
* 标签存在伪类: `标签: 伪类`
* **a标签的状态** 
    1. `a:link` 初始状态(未被点击的状态)
    2. `a:hover` 鼠标悬浮态
    3. `a:active` 激活太，被点击的状态
    4. `a:visited` 访问后状态
* 其他标签也可以使用

```css
a:link { /*初始状态*/
    color: green;
}
a:hover { /*鼠标悬停状态*/
    color: greenyellow;
}
a:active { /*被点击状态*/
    color: black;
}
a:visited { /*点击后状态*/
    color:darkgray;
}

input:focus { /*input框获取焦点（input框被选中）*/
    background-color: black;
    color: white;
}
```

### 4.2.5 伪元素选择器
* 标签存在伪元素，`标签:伪标签`

```css
p:first-letter { /*修改文本的第一个字*/
    /*font-size: 48px;*/
    /*color: orange;*/
}
p:before { /*在p段落开头添加内容，内容不能被复制*/
    content: "你好";
    color: blue;
}

p:after { /*在p段落结束添加内容*/
    content: "再见";
    color: orange;
}
/*before和after通常用于清楚浮动，解决父标签塌陷问题*/
```

## 4.3 选择器的优先级
* **相同的选择器，距离标签近的样式生效** 
* **id选择器 &gt; class选择器 &gt; 标签选择器** 
* **行内选择器优先级最高**
* **匹配越精准的选择器优先级越高**

# 五、CSS属性
## 5.1 `height`和`width`属性
```css
p {
    background-color: red;
    height: 200px;
    width: 400px;
}

span {
    background-color: green;
    height: 200px;
    width: 400px;
    /*行内标签不能设置长宽，即是设置也不会生效*/
}
```
> 1. **只有块级标签才能设置height和width属性**
> 2. 行内标签不能设置长宽，即是 **设置也不会生效**

## 5.2 字体属性(`font`) 
```css
p {
    font-family: 'Consolas', 'Monaco', 'Bitstream Vera Sans Mono', monospace; /*设置字体*/
    font-size: 24px; /*字体大小*/
    font-weight: bolder; /*字体粗细*/
    color: rgba(62, 146, 154, 0.5);  /*字体颜色 英文单词，十六进制颜色编号，rgb值，rgba值*/
    /*获取颜色，pycharm提供的取色器 QQ截图功能提供*/
}
```

## 5.3 文本属性
```css
p {
    width: 500px;
    background-color: black;
    color: white;
    text-align: left;  /*文本对齐方式 center居中对齐 right右对齐 left左对齐，默认 justify两端对其*/
    text-decoration: underline; /*文字装饰 underline下划线 overline上划线 line-through删除线 none无装饰*/
    font-size: 16px;
    text-indent: 32px; /*首行缩进32px*/
}
a{
    text-decoration: none;  /*无文本装饰 通常用于去除a标签的默认装饰*/
}
```

## 5.4 背景属性
```css
div {
    width: 500px;
    height: 500px;
    background-color: gainsboro;
    background-image: url("./葫芦娃.png"); /*背景图片，默认会铺满*/
    background-repeat: no-repeat; /*背景图片填充类型 no-repeat不平铺 repeat-x repeat-y在某个坐标上平铺*/
    /*浏览器页面是一个三维立体，x轴水平，y轴竖直，z轴指向用户*/
    background-position: center center; /*控制背景图片的位置 左|上*/
    background-attachment: fixed; /*图片位置固定*/
    /*
    background: gainsboro(背景色) url("./葫芦娃.png")(背景图片) no-repeat(背景图片填充类型) center(左边位置) center(上边位置);
    */
}
```

## 5.5 边框属性
```css
p {
    height: 50px;
    background-color: red;
    border-width: 5px; /*边框的宽度*/
    border-style: solid; /*边框样式*/
    border-color: aqua; /*边框颜色*/
    /*
     border: 5px solid aqua; 位置不固定
    */
}
.four {
    height: 50px;
    width: 500px;
    background-color: orange;
    /*左边框*/
    border-left-width: 5px;
    border-left-color: aqua;
    border-left-style: dotted;
    /*有边框*/
    border-right-width: 5px;
    border-right-color: deepskyblue;
    border-right-style: dashed;
    /*上边框*/
    border-top-width: 5px;
    border-top-color: skyblue;
    border-top-style: dashed;
    /*下边框*/
    border-bottom-width: 5px;
    border-bottom-color: blue;
    border-bottom-style: solid;
}

#cycle {
    background-color: greenyellow;
    height: 400px;
    width: 400px;
    border-radius: 50%; /*设置边框转角，高度和宽度一样则是园，不一样则是椭圆*/
}
```

## 5.6 display属性
```css
display: inline|block|inline-block|none
```
> 1. `inline`: 将标签变为行内标签的性质
> 2. `block`: 将标签变为块级标签的性质
> 3. `inline-block`: 让标签同时具有行内标签和块标签的性质。（占一行且可以设置长宽）
> 4. `none`: 隐藏标签，不展示

## 5.7 盒子模型
![盒子模型](https://images.gitee.com/uploads/images/2020/1201/002457_42ed1df8_7841459.png "屏幕截图.png")

> * `Margin（外边距）`: 清除边框区域。Margin 没有背景颜色，它是完全透明
> * `Border（边框）`: 边框周围的填充和内容。边框是受到盒子的背景颜色影响
> * `Padding（内边距）`: 清除内容周围的区域。会受到框中填充的背景颜色影响
> * `Content（内容）`: 盒子的内容，显示文本和图像




