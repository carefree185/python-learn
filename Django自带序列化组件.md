# 一、Django自带的序列化组件
开发项目时，通常时前后端分离的。数据由后端返回，前端渲染。此时`Django`的模板语法不能起到数据渲染的作用。需要使用`json`格式的数据交由前端开发人员进行渲染。在`python`中通常构造成列表嵌套字典的形式，序列化为`json`字符串之后返回给前端。

* **执行构造**: 当我们从数据库中获得数据后，进行如下操作将数据序列化为`json`字符串
    ```python
    def serialize(request):
        user_queryset = User.objects.all()
        from django.core import serializers  # 序列胡组件
        user_list = []
        for user in user_queryset:
            tmp = {
                "pk": user.pk,
                'username': user.username,
                'age': user.age,
                'gender': user.get_gender_display()
            }
            user_list.append(tmp)
        return render(request, 'serialize.html', locals())
    ```
    * 当需要返回的数据字段较为多时，这些做开发效率低下。

* **使用`Django`自带的序列化组件
    ```python
    from django.core import serializers  # 导入序列化组件
    def serialize(request):
        user_queryset = User.objects.all()  # 查询数据
        res = serializers.serialize('json', user_queryset)  # 将数据变为json格式的字符串
        return HttpResponse(res)
    ```
* `Django`自带的序列化组件序列化的数据格式
    ```python
    [{  "model": "app01.user", 
        "pk": 1, 
        "fields": {
            "username": "jason", 
            "age": 18, 
            "gender": 1
            }
    }, 
    {   "model": "app01.user", 
        "pk": 2, 
        "fields": {
            "username": "egon", 
            "age": 23, 
            "gender": 4
            }
    }, 
    {   "model": "app01.user", 
        "pk": 3, 
        "fields": {
            "username": "ddd", 
            "age": 19, 
            "gender": 2
            }
    }, 
    {   "model": "app01.user", 
        "pk": 4, 
        "fields": {
            "username": "\u5c0f\u5170", 
            "age": 24, 
            "gender": 3
            }
    }
    ]
    ```
# 二、数据的批量插入
当涉及到一次性要插入大量数据时，使用orm提供的`bulk_create(iterable)`方法插入数据，可以极大的提高插入效率。如果一条条的插入，会消耗大量的时间
```python
models.Book.objects.bulk_create(book_list)  # 批量插入数据
```

# 三、分页器
## 3.1 分页器
### 3.1.1 前端
```django
<nav aria-label="Page navigation">
  <ul class="pagination">
    <li>
      <a href="#" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
    {{ page_html|safe }}
    <li>
      <a href="#" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
```
### 3.1.2 后端
```python
def pagination(request):
    """
    分页器
    :param request:
    :return:
    """
    book_list = Book.objects.all()  # 查询全部的数据
    total_num = book_list.count()  # 统计数据的条数
    # 想要分页展示，就需要确定每一页展示的数据，当前展示页属
    one_pageData_number = 10   # 假设每页展示10条数据
    # 计算总共由几页
    total_page, more = divmod(total_num, one_pageData_number)
    if more:
        total_page += 1

    # 当前想要展示页码获取
    current_page = request.GET.get("page")  # 获取当前想要展示的页码
    try:
        current_page = int(current_page)
    except Exception:
        current_page = 1

    # 分页制作
    page_html = ''
    pre_page = current_page
    if current_page < 6:
        current_page = 6
    elif current_page + 6 >= total_page:
        current_page = total_page - 5
    for i in range(current_page-5, current_page + 6):
        if pre_page == i:
            page_html += '<li class="active"><a href="?page={0}">{0}</a></li>'.format(i)
        else:
            page_html += '<li><a href="?page={0}">{0}</a></li>'.format(i)

    # 展示数据的获取
    start = (pre_page-1) * one_pageData_number
    end = pre_page * one_pageData_number
    book_queryset = book_list[start: end]

    return render(request, 'batch.html', locals())
```

## 3.3 自定义分页器
```python
class Pagination(object):
    def __init__(self, current_page, all_count, per_page_num=2, pager_count=11):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
                    <nav aria-label='Page navigation>'
                    <ul class='pagination'>
                ''')
        first_page = '<li><a href="?page=%s">首页</a></li>' % (1)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="?page=%s">上一页</a></li>' % (self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = '<li class="active"><a href="?page=%s">%s</a></li>' % (i, i,)
            else:
                temp = '<li><a href="?page=%s">%s</a></li>' % (i, i,)
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?page=%s">下一页</a></li>' % (self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)
        # 尾部添加标签
        page_html_list.append('''
                                           </nav>
                                           </ul>
                                       ''')
        return ''.join(page_html_list)
```


