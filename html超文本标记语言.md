# 一、HTML简介
## 1.1 HTML是什么
* 超文本标记语言(HyperText Mark-up Language)
* 用来设计网页的标记语言
* 用该语言编写的文件以 .html或.htm为可扩展名
* 有浏览器解释执行
* 不区分大小写，建议小写

## 1.2 HTML标签
* html由于描述功能的符号称为"标签"
* 标签都是封装在一对尖括号"<...>"之中，如\<html>是一个标签
* 封闭类型的标签(也称双标签), 如\<p></p>就是一个双标签
* 非封闭标签(也称单标签)，如\<br>就是一个单标签

**web浏览器的的作用就是解析html文件并展示html文件类容**

## 1.3 HTML元素
* **开始标签**到**结束标签**中的所有代码
* 元素内容指**开始标签**到**结束标签**之间的所有内容
* **空元素**以开始标签结束
* 大多数的html元素都有属性

## 1.4 HTML属性
* 属性是用于修饰元素的
  * 必须位于开始标签里
  * 一个元素可能有多个属性，每个属性用空格隔开
  * 多个属性之间部分先后
* 每个属性都有值
  * 属性和属性值之间用**等号**连接
  * 属性值包含在**引号**中
  * 属性总以**键值对**形式出现 

* 示例
  * style是属性
  * "text-align: center"为属性值
```html
<p style="text-align: center">段落标签属性</p>
```

## 1.5 HTML注释
* 写代码时添加注释是一个好习惯
* 注释仅文本可见，浏览器不解析
* 注释没有属性
* 语法
```html
<!--注释语法-->
```
1. \<!-- -->之间的内容不显示
2. 不可以嵌套
3. 不可以位于标签的尖括号"<>"内部

# 二、HTML的文档结构
```html
<!DOCTYPE html> <!--文档类型声明-->
<html lang="zh"> 
    <head>  <!--head里面的标签，是用来配置基础渲染设置-->
        <meta charset="UTF-8">
        <title>网页标题</title>
    </head>
    
    <body bgcolor="red">
    <!--网页主体，可视化区域-->
    <!--浏览器渲染的部分-->
    </body>
</html>
```

# 三、`HTML`中`head`标签中常用的标签

```html
<meta charset="UTF-8">  <!--配置网页解析的编码-->
<meta http-equiv="refresh" content="5;URL=https://www.baidu.com">  <!--两秒后跳转到指定url-->
<meta http-equiv="x-ua-compatible" content="IE=edge"> <!--ie浏览器以最高级模式渲染-->

<meta name="keywords" content="内容">  <!--网页关键字，用于提升网页查询出来的概率-->
<meta name="description" content="描述内容">  <!--网页描述，描述当前网页的信息-->

<title>head标签中的常用标签</title>  <!--网页标题-->
<style>
    #书写css代码
</style>
<script src="外部js文件的路径或网址">
    // 书写js代码或者引入外部js文件
</script>
<link rel="stylesheet" href="外部css文件的路径或网址">  <!--引入外部css文件-->
```
> 1. `<meta>`: 单标签，用于配置一些浏览器对此页面的解析信息
> 2. `<title>标题</title>`：双标签，标题标签，网页标题
> 3. `<style>...</style>`: 双标签，该标签中书写的是css样式表
> 4. `<script>...</script>`: 双标签，该标签中书写js代码或是引入外部js代码
> 5. `<link rel="stylesheet" href="">`: 单标签，用于引入外部css样式表

# 四、`HTML`中`body`标签中的常用标签
## 4.1 基本标签
```html
<!--第一个学习的标签-->
<h1>一级标题标签h1</h1>
<h2>二级标题标签h2</h2>
<h3>三级标题标签h3</h3>
<h4>四级标题标签h4</h4>
<h5>五级标题标签h5</h5>
<h6>六级标题标签h6</h6>
普通文本，非标签中的文本

<!--第二个标签-->
<b>加粗标签b</b>
<i>斜体标签i</i>
<u>下划线u</u>
<s>删除线s</s>

<!--第三个标签-->
<p>段落标签p</p>

<p>
    <h3>出塞</h3>
    <h6>[唐] 王昌龄</h6>
    秦时明月汉时关，万里长征人未还。<br /> <!--换行-->
    <hr>  <!--水平分隔线-->
    但使龙城飞将在，不教胡马度阴山。
</p>
```
> 1. 块级标签：每个标签独占一行，常见的标签有  **标题标签h** ， **段落标签p** 
> 2. 行内标签：文本撑开多大就占多大，常见的标签有  **加粗标签b** ， **斜体字标签i**   **下划线标签u**   **删除线标签s** 

## 4.2 特殊符号
1. `&nbsp;`: 空格，一个英文字符
2. `&gt;`: 大于符号`>`
3. `&lt;`: 小于符号`<`
4. `&amp;`: `&`
5. `&yen;`: 羊角符&yen;
6. `&copy;`: 版权符号&copy;
7. `&reg;`: 商标符号&reg;

# 五、常用标签
## 5.1 无语义标签
`div`标签和`span`标签
> 1. div标签是块级标签
> 2. span标签是行内标签

这两个标签通常是用来布局网页的，使用div标签划分区域，然后向div中填写内容。普通文本通常先使用span标签。

> **标签的嵌套规则**
> 1. 块级标签可以修改长宽，行内标签不可以修改
> 2. 块级标签内部可以 **嵌套任意块级标签和行内标签** ； **`p`标签只能嵌套行内标签**，浏览器会自动将`p`标签中的块级标签分开展示。
> 3. 行内标签不能嵌套块级标签，只能嵌套行内标签。

## 5.2 图片标签(img)
```html
<img src="图片的目录或网址" alt="图片渲染失败后显示的内容" title="鼠标悬停时展示的文本" height="高度" width="宽度">
```
> 1. `src`: 图片地址
> 2. `alt`: 图片渲染失败后显示的文本
> 3. `title`: 鼠标悬浮的时后展示的信息
> 4. `height | width`: 高度和宽度，只修改一个时，另外一个参数会等比例缩放

## 5.3 超链接标签(a)
```html
<a href="要访问的url" >访问百度</a>
```
> 标签指定的网址没有被访问过，a标签字体颜色默认问蓝色，如果被访问过为紫色
> 1. `href`: 要访问的url
> 2. `target`：打开新网址的目标； `_self`，当前窗口，`_blank`，新建窗口打开

**锚点功能实现**
```html
<a href="#mid" id="top">顶部，指向中部</a>

<div style="height: 1000px; background-color: red"></div>

<a href="#top" id="mid">中部,返回顶部</a>

<div style="height: 1000px; background-color: yellow"></div>

<a href="" id="bottom">底部</a>
```
> 1. `href="#id值"`：指向id所在的标签，点击即可跳转到对应的标签位置

> **标签都是有的属性，由默认属性和自定义属性**
> 1. `id`: 属性，标签的身份证号，同一个id值只能出现一次
> 2. `class`: 属性，分类标签，一个标签可以设定多个class值

## 5.4 列表标签
### 5.4.1 无序列表
```html
<ul >
    <li>第一项</li>
    <li>第二项</li>
    <li>第三项</li>
</ul>
```
>  **默认效果** <br>
> ![输入图片说明](https://images.gitee.com/uploads/images/2020/1129/192324_98d0183b_7841459.png "屏幕截图.png")

> **属性指定**
> 1. `type`: 修改标签前面圆点的样式; `circle`: 空心圆点, `none`: 无圆点

### 5.4.2 有序列表
```html
<ol>
    <li>第一项</li>
    <li>第二项</li>
    <li>第三项</li>
</ol>
```
> **默认效果**<br>
> ![输入图片说明](https://images.gitee.com/uploads/images/2020/1129/192308_7676e59a_7841459.png "屏幕截图.png")

> **属性**
> 1. `type`: 指定序号样式（数字、字母、罗马数字等）
> 2. `start`: 指定序号开始值（只有数字生效，字母不生效）

### 5.4.3 标题列表
```html
<dl>
    <dt>标题1</dt>
    <dd>内容1</dd>
    <dt>标题2</dt>
    <dd>内容2</dd>
    <dt>标题3</dt>
    <dd>内容3</dd>
</dl>
```
> **默认效果**<br>
> ![输入图片说明](https://images.gitee.com/uploads/images/2020/1129/192801_c23341f7_7841459.png "屏幕截图.png")

## 5.5 表格标签
```html
<table>
    <caption>学生表</caption> <!--表格标题-->
    <thead><!--表头 存放字段信息-->
        <tr> <!--一对tr标签表示一行-->
            <th>姓名</th> <!--加粗th标签内的数据-->
            <th>学号</th>
            <th>性别</th>
        </tr>
    </thead>

    <tbody> <!--表单， 存放数据-->
        <tr> <!--一对tr标签表示一行-->
            <td>小明</td>  <!--正常文本-->
            <td>001</td>
            <td>男</td>
        </tr>
        <tr>
            <td>小芳</td>
            <td>002</td>
            <td>女</td>
        </tr>
    </tbody>

</table>
```

**表格说明** 
* `<table> </table>`标签 声明一个列表
  * 常用属性
  
    |属性|描述|说明|
    |:---:|:---:|:---:|
    |`width`|表格的宽度||
    |`height`|表格的高度||
    |`align`|表格的水平对齐方式||
    |`background`|表格的背景图片||
    |`bgcolor`|表格的背景颜色||
    |`border`|表的边框(以像素为单位)|默认无边框|
    |`bordercolor`|表格边框颜色|border属性值大于1时生效|
    |`cellspacing`|单元格之间的距离||
    |`cellpadding`|单元格内容与单元个边框之间的距离||
    
* `<tr> </tr>`标签 表示一行 只能包含`<td>`和`<th>`标签
  * 常用属性
      
    |属性|描述|
    |:---:|:---:|
    |`height`|行高|
    |`align`|行内容的水平对齐方式|
    |`valign`|行内容的垂直对齐方式|
    |`bgcolor`|行背景颜色|

* `<td> </td>`标签 表示一个单元格
  * 常用属性
      
    |属性|描述|
    |:---:|:---:|
    |`width`|单元格宽|
    |`height`|单元格高|
    |`align`|单元格内元素水平对齐方式|
    |`valign`|单元格内元素垂直对齐方式|
    |`bgcolor`|单元格背景颜色|
    |`colspan`|单元格跨列|
    |`rowspan`|单元格跨行|
    
  * 单元格合并
      * 合并行
        * 即跨行合并
        * 设置属性 `rowspan="n"` n表示合并n行
      * 合并列
        * 即跨列合并
        * 设置属性 `colspan="n"` n表示合并n列
      * 注意：合并后要将多余的单元格删除
  
* `<th> </th>`标签 表示每一列的字段
* `<thead> </thead>`标签 表头
* `<tbody> </tbody>`标签 表体
* `<tfoot> </tfoot>`标签 表尾

**表格通常使用前端框架的样式**

## 5.6 表单
获取前端用户输入的数据，基于网络发送数据给服务端

### 5.6.1 表单域标签
`<form></form>`表单, 接受用户输入的信息，并将信息提交到服务器。
要提交到服务器里面的数据都需要包含在form表单里面。
语法：`<form action="url" method="get|post" name=""> </form>`
表单是由窗体和控件组成，一个表单应该包含用户填写信息的**输入框**
提交**按钮**等；这些输入框，按钮称为**控件**；表单就像容器来容纳这些控件
```html
<form action="" method="" name="">  <!--表单域标签-->
    <!--此标签中的数据，都会被捕获，然后提交到服务器-->
    <!--
    action：数据提交到的服务端路径
        1. action=""：向当前页面的url提交数据
        2. action="url"：向指定的url提交数据
        3. action="/路径"：自动拼接当前服务端的ip和port
     -->
</form>
```
> **form表单域表的属性**
> * `action`: 指定表单域内数据提交的位置
>     1. action=""：向当前页面的`url`提交数据
>     2. action="url"：向指定的`url`提交数据
>     3. action="/路径"：自动拼接当前服务端的`ip`和`port`
> * `method`: 提交数据的方法(get或post)
>     1. `get`: `get`提交的数据可以在`url`中查看
>     2. `post`: `post`提交数据较大
> * `name`: 为表单域命名，用于区别没有页面中的多个表单域

一个完整的表单包含以下三个部分：
* 表单标签
  * 包含在from标签中的标签
* 表单域
  * form标签包含的区域
* 表单按钮
  * 用来提交表单内容到服务器中。
  
**表单域和表单按钮都是表单元素**


### 5.6.2 input标签
`input`标签是一个行内标签，通常配合`label`标签一起使用

```html
<label for="">
    提示信息: <input type="" id="" name="" value="" placeholder="提示信息">
</label>
<label for="password">提示信息：</label>
<input type="" id="" name="" value="">
```
> 1. `label`标签配合`input`使用提高用户的使用体验
> 2. `for`: 填写`input`标签的`id`值，当点击被`label`标签包含的为位置是，选中输入框

**input标签的常用属性**
* `type`: 更改形状，
* `name`: 定义输入内容的变量名(提交数据时的`key`)
* `value`: 指定控件的初始值(默认值), `input`输入的值都是保存在`value`属性中(提交数据时的`value`)
* `placeholder`: 提示信息
* `multiple`: 多值输入，逗号(`,`)隔开;常用在`email`和`url`的输入 无须赋值
* `autofocus`: 自动获取焦点 一个页面只能加一个 无须赋值
* `required`: 防止域为空时提交表单 无须赋值
* `checked`: 默认选中数据
* `minlength` 和 `maxlength`: 元素允许的最小字符和最大字符个数

#### 5.6.2.1 文本框(`type="text"` 默认属性)
```html
<input type="text" name="username" value="如果不输入，使用值为默认值" placeholder="请输入用户名">  <!--输入用户名-->
```

#### 5.6.2.2 密文框(`type="password"`) 
```html
<input type="text" name="username" placeholder="请输入密码"> <!--输入密码-->
```

#### 5.6.2.3 日期域(`type="date"`)
```html
<input type="date" name="birthday"> <!--选择日期-->
```

#### 5.6.2.4 单选选按钮(`type="radio"`)
```html
<ul type="none">
    <li>
        <label for="boy">男</label>
        <input type="radio" name="gender" value="0" id="boy" checked>
    </li>

    <li>
        <label for="girl">女</label>
        <input type="radio" name="gender" value="1" id="girl">
    </li>
</ul>
```
> 1. `name`: 每个选项都必须用相同的`name`属性值(提交时的`key`)
> 2. `value`: 每个选项要不同的`value`属性值(提交时的`value`)
> 3. `checked|checked="checked"`: 默认选择，属性名和属性值一样时，只需要写属性名即可

#### 5.6.2.5 复选框(`type="checkbox"`)
```html
<ul type="none">
    <li>
        <label for="sing">唱歌</label>
        <input type="checkbox" name="hobby" value="sing" id="sing">
    </li>
    <li>
        <label for="dance">跳舞</label>
        <input type="checkbox" name="hobby" value="dance" id="dance">
    </li>
    <li>
        <label for="game">打游戏</label>
        <input type="checkbox" name="hobby" value="game" id="game">
    </li>
</ul>
```
> 1. `name`: 每个选项都必须用相同的`name`属性值(提交时的`key`)
> 2. `value`: 每个选项要不同的`value`属性值(提交时的`value`)


#### 5.6.2.6 按钮
1. 普通按钮(`type="button"`)
    ```html
    <input type="button" value="普通按钮">
    ```
    > * 点击按钮时，无任何事件执行

2. 提交按钮(`type="submit"`)
    ```html
    <input type="submit" value="提交">
    ```
    > * 点击按钮时，触发提交数据事件

3. 重置按钮(`type="reset"`)
    ```html
    <input type="reset" value="重置">
    ```
    > * 点击按钮时，触发清空输入数据事件

4. 按钮标签(`<button type="submit|reset|button"></button>`)
    ```html
    <button type="submit">提交按钮</button>
    <button type="reset">重置按钮</button>
    <button type="button">普通按钮</button>
    ```

5. 图片按钮(`type="image"`)
    ```html
    <input type="image" src="url">
    ```
    > * `src: 用于引用图片
    > * 点击按钮时，触发提交数据事件


#### 5.6.2.7 隐藏域(`type="hidden"`)
```html
<input type="hidden"
```

#### 5.6.2.8 文件上传(`type="file"`)
```html
<input type="file" name="file">
```

### 5.6.3 下拉框(`select`标签)
```html

```




