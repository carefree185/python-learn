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


