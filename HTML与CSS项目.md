**html代码**
```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>博客园</title>
    <link rel="stylesheet" href="../CSS/blog-css.css">
</head>
<body>

<div class="blog-left">

    <div class="blog-avatar">
        <img src="./喜羊羊.png" alt="">
    </div>

    <div class="blog-title">
        <p>xxx的博客</p>
    </div>

    <div class="blog-info">
        <p>这个人很懒，什么也没留下</p>
    </div>

    <div class="blog-link">

        <ul>
            <li><a href="">关于我</a></li>
            <li><a href="">微博</a></li>
            <li><a href="">微信公众号</a></li>
        </ul>

    </div>

    <div class="blog-tag">

        <ul>
            <li><a href="">Python</a></li>
            <li><a href="">Java</a></li>
            <li><a href="">Golang</a></li>
        </ul>

    </div>

</div>

<div class="blog-right">

    <div class="article">

        <div class="article-title">
            <span class="title">重金求子</span>
            <span class="date">2020/09/15</span>
        </div>

        <div class="article-body">
            <p>重金求子，事成500万答谢并赠送大别墅一套</p>
        </div>

        <div class="article-bottom">
            <span>Python</span>&emsp;
            <span>Java</span>
        </div>
    </div>

</div>


</body>
</html>
```

**CSS代码**
```css
/*个人博客首页CSS*/

/*通用样式*/
.clearfix:after {
    content: "";
    display: block;
    clear: both;
}
body {
    margin: 0;
    background: lightgray;
}
a {
    text-decoration: none; /*文字装饰*/
}

ul {
    list-style-type: none; /*列表样式*/
    padding-left: 0;
}

/*左侧样式*/
.blog-left {
    float: left;
    height: 100%;
    width: 20%;
    position: fixed;
    background-color: #4e4e4e;
}
.blog-avatar {
    height: 150px;
    width: 150px;
    border: 3px solid white;
    border-radius: 50%;
    margin: 20px auto;
    overflow: hidden;
}
.blog-avatar>img {
    width: 100%;
}

.blog-title, .blog-info {
    color: darkgray;
    font-size: 18px;
    text-align: center; /*文本居中*/
}

.blog-link, .blog-tag {
    font-size: 24px;
}
.blog-link a, .blog-tag a {
    color: darkgray;
}
.blog-link a:hover, .blog-tag a:hover {
    color: white;
}

.blog-link ul, .blog-tag ul {
    text-align: center;
    margin: 30px;
}

/*右侧样式*/

.blog-right {
    float: right;
    width: 80%;
    height: 1000px;
}

.article {
    background-color: white;
    margin: 20px 40px 10px 10px;
    box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.6);
}

.article-title {
    border-left: 8px solid red;
    text-indent: 1em;
}

.title {
    font-size: 36px;
}

.date {
    float: right;
    margin: 20px;
    font-weight: bolder;
}

.article-body {
    font-size: 18px;
    text-indent: 30px;
    border-bottom: 1px solid black;
}

.article-bottom {
    font-size: 16px;
    padding-left: 30px;
    padding-bottom: 10px;
}
```
> 1. `box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.5)`: 设置标签投影
> 2. `list-style-type: none`： 设置列表样式


