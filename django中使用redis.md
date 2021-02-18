### 8.9 Django中使用redis

#### 8.9.1 通用方式
自己在使用的位置写代码

#### 8.9.2 django-redis
`Django`默认不支持`redis`缓存

**直接使用Django的cache使用**
在`settings.py`(配置文件)添加配置
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}
```

**使用redis的链接对象**
```python
from django_redis import get_redis_connection
conn = get_redis_connection('default')
```








