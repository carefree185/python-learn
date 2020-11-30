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



