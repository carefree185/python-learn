# 一、缓存介绍

在动态网站中,用户所有的请求,服务器都会去数据库中进行相应的增,删,查,改,渲染模板,执行业务逻辑,最后生成用户看到的页面.

当一个网站的用户访问量很大的时候,每一次的的后台操作,都会消耗很多的服务端资源,需要使用使用缓存来减轻后端服务器的压力.

缓存是将一些常用的数据保存内存或者memcache中,在一定的时间内有人来访问这些数据时,则不再去执行数据库及渲染等操作,而是直接从内存或memcache的缓存中去取得数据,然后返回给用户.

# 二、Django缓存机制及配置文件
Djangi提供下面六种缓存方式，只需在settings.py中配置即可使用
1. 开发调试缓存
    ```python
    CACHES = {
     'default': {
      'BACKEND': 'django.core.cache.backends.dummy.DummyCache',  # 缓存后台使用的引擎
      'TIMEOUT': 300,            # 缓存超时时间（默认300秒，None表示永不过期，0表示立即过期）
      'OPTIONS':{
       'MAX_ENTRIES': 300,          # 最大缓存记录的数量（默认300）
       'CULL_FREQUENCY': 3,          # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
      },
     }
    }
    ```
    
2. 内存缓存
    ```python
    CACHES = {
     'default': {
      'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # 指定缓存使用的引擎
      'LOCATION': 'unique-snowflake',         # 写在内存中的变量的唯一值 
      'TIMEOUT':300,             # 缓存超时时间(默认为300秒,None表示永不过期)
      'OPTIONS':{
       'MAX_ENTRIES': 300,           # 最大缓存记录的数量（默认300）
       'CULL_FREQUENCY': 3,          # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
      }  
     }
    }
    ```

3. 文件缓存
    ```python
    CACHES = {
     'default': {
      'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', #指定缓存使用的引擎
      'LOCATION': '/var/tmp/django_cache',        #指定缓存的路径
      'TIMEOUT':300,              #缓存超时时间(默认为300秒,None表示永不过期)
      'OPTIONS':{
       'MAX_ENTRIES': 300,            # 最大缓存记录的数量（默认300）
       'CULL_FREQUENCY': 3,           # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
      }
     }   
    }
    ```

4. 数据库缓存(需要先执行`python manage.py createcachetable`创建缓存表)
    ```python
    CACHES = {
     'default': {
      'BACKEND': 'django.core.cache.backends.db.DatabaseCache',  # 指定缓存使用的引擎
      'LOCATION': 'cache_table',          # 数据库表    
      'OPTIONS':{
       'MAX_ENTRIES': 300,           # 最大缓存记录的数量（默认300）
       'CULL_FREQUENCY': 3,          # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
      }  
     }   
    }
    ```

5. Memcache缓存(使用python-memcached模块)
    ```python
    CACHES = {
     'default': {
      'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache', # 指定缓存使用的引擎
      'LOCATION': '192.168.10.100:11211',         # 指定Memcache缓存服务器的IP地址和端口
      'OPTIONS':{
       'MAX_ENTRIES': 300,            # 最大缓存记录的数量（默认300）
       'CULL_FREQUENCY': 3,           # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
      }
     }
    }
    ```
    * location可以配置多个·
        ```python
        'LOCATION': 'unix:/tmp/memcached.sock',   # 指定局域网内的主机名加socket套接字为Memcache缓存服务器
        'LOCATION': [         # 指定一台或多台其他主机ip地址加端口为Memcache缓存服务器
         '192.168.10.100:11211',
         '192.168.10.101:11211',
         '192.168.10.102:11211',
        ]
        ```

6. Memcache缓存(使用pylibmc模块)
    ```python
    settings.py文件配置
     CACHES = {
      'default': {
       'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',  # 指定缓存使用的引擎
       'LOCATION':'192.168.10.100:11211',         # 指定本机的11211端口为Memcache缓存服务器
       'OPTIONS':{
        'MAX_ENTRIES': 300,            # 最大缓存记录的数量（默认300）
        'CULL_FREQUENCY': 3,           # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
       },  
      }
     }
    ```
    * location可以配置多个·
        ```python
        'LOCATION': 'unix:/tmp/memcached.sock',   # 指定局域网内的主机名加socket套接字为Memcache缓存服务器
        'LOCATION': [         # 指定一台或多台其他主机ip地址加端口为Memcache缓存服务器
         '192.168.10.100:11211',
         '192.168.10.101:11211',
         '192.168.10.102:11211',
        ]
        ```
    
# 三、Django缓存的使用
当配置文件配置好之后，可以使用

## 3.1 前后端不分离的缓存使用

### 3.1.1 局部缓存
1. 缓存一个页面，只需要给页面(视图函数)添加装饰器即可
    ```python
    from django.views.decorators.cache import cache_page
    import time
    from .models import *
    
    @cache_page(15)          #超时时间为15秒
    def index(request):
    　　t=time.time()      #获取当前时间
    　　bookList=Book.objects.all()
    　　return render(request,"index.html",locals())
    ```
2. 缓存页面的局部数据，需要用到标签
    ```django
    {% load cache %}
    {% cache 2 'name' %} 
    {# 2是缓存过期时长，name是缓存的键(cache_key)#}
     <h3>缓存:-----:{{ t }}</h3>
    {% endcache %
    ```

### 3.1.2 全局缓存
全局缓存要在中间件实现

```python
MIDDLEWARE_CLASSES = (
    ‘django.middleware.cache.UpdateCacheMiddleware’, #第一
    'django.middleware.common.CommonMiddleware',
    ‘django.middleware.cache.FetchFromCacheMiddleware’, #最后
)
# “update” 必须配置在第一个, 缓存是在此时执行的
# “fetch” 必须配置在最后一个

CACHE_MIDDLEWARE_SECONDS=10  # 缓存过期时长
```

## 3.2 前后端分离
```python
from django.core.cache import cache
cache.set("key", value)  # key,是缓存时的键，value可以是任意数据类型
cache.get("key")  # 获取缓存内容。
```


