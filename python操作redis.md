## 八、redis使用

使用python对redis数据类型的简单操作

### 8.1 普通链接与连接池

安装操作redis的库`pip install redis`

redis-py提供两个类Redis和StrictRedis用于实现Redis的命令， StrictRedis用于实现大部分官方的命令，并使用官方的语法和命令， Redis是StrictRedis的子类，用于向后兼容旧版本的redis-py

#### 8.1.1 python操作redis普通链接

```python
import redis

connection = redis.Redis()  # 链接redis服务端，返回链接对象

connection.set('name', 'dyy')

print(connection.get('name'))
```

#### 8.1.2 python操作redis连接池

```python
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)  # 必须将这个连接池做成单例，可以继承重写，也可以通过模块导入的形式。

r = redis.Redis(connection_pool=pool)

print(r.get('name'))
```

必须将这个连接池做成单例，可以继承重写，也可以通过模块导入的形式。

### 8.2 字符串操作(string)

redis中的String在在内存中按照一个name对应一个value来存储

```python
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)  # 必须将这个连接池做成单例，可以继承重写，也可以通过模块导入的形式。

r = redis.Redis(connection_pool=pool)
```

#### 8.2.1 增加

* `r.set(name, value, ex=None, px=None, nx=False, xx=False)`: 给name键设置value值
	1. 以`name: value`形式存放在内存
	2. `ex`: 过期时间，单位秒
	3. `px`: 过期时间，单位毫秒
	4. `nx`: 如果设置为`True`，则只有`name`不存在时，当前`set`操作才执行,值存在，就修改不了，执行没效果
	5. `xx`: 如果设置为`True`，则只有`name`存在时，当前`set`操作才执行，值存在才能修改，值不存在，不会设置新值

* `r.setnx(name, value)`: 当`name`不存在时，给`name`设置`value`值

* `r.setex(name, value, ex)`: 给`name`设置`value`值，`ex`时间内有效
	1. `ex`: 过期时间（数字秒 或 timedelta对象）

* `r.psetex(name, px, value)`: 给`name`设置`value`值，`px`时间内有效
	1. `px`: 过期时间（数字毫秒 或 timedelta对象）

* `r.mset(*args, **kwargs)`: 批量设置值
	1. `r.mset(k1='v1', k2='v2')`或`r.mset({'k1': 'v1', 'k2': 'v2'})`

#### 8.2.2 查找

* `r.get(name)`: 获取`name`对应的值

* `r.mget(keys, *args)`: 获取多个name对应的值
	* `r.mget('k1', 'k2')`或 `r.mget(['k3', 'k4'])`

* `r.getset(name, value)`: 获取原来的值，并设置新值

* `r.getrange(name, start, end)`: 获取`name`对应的字符串的子串
	* `[start, end]`表示字节数

* `r.getbit(name, offset)`: 获取`name`对应二进制数据的`offset`位上的数据(只有0和1)

* `r.bitcount(key, start, end)`: 获取`name`对应的二进制串中1的个数(登录与非登录用户分类)

* `r.strlen(name)`: 返回name对应的字节长度(一个汉族3个字节(utf8))

#### 8.2.3 修改

* `r.setrange(name. offset, value)`: 修该`name`对应字符串`offset`开始后面部分为`value`

* `r.setbit(name, offset, value)`: 修改`name`对应二进制串`offset`位置修改位`value`

* `r.append(name, value)`: 追加`value`到`name`对应的字符串的尾部

#### 8.2.4 字符串当数字使用

* `r.incr(name, amount=1)`: 将`name`对应`value`进行增值操作, `name`不存在则创建, 并赋值为`amount`(访问量统计)

* `r.decr(name, amount=1)`: 将`name`对应`value`进行减值操作, `name`不存在则创建，并赋值为`-amount`(秒杀)

### 8.3 hash操作

redis中的hash结构是值value的结构。

#### 8.3.1 设置

* `r.hset(name, key, value)`: 给`name`设置`key-value`键值对。如果`name`存在，则新增。`key`重复则修改

* `r.hmset(name, mapping)`: 给`name`设置`mapping`中的`key-value`键值对

#### 8.3.2 获取

* `r.hget(name, key)`: 获取`name`对应的`hash`对象中`key`对应的`value`值

* `r.hmget(name, keys, *args)`: 获取`name`对应的`hash`对象中获取多个`key`的值
	1. `keys`: 要获取`key`集合，如：`['k1', 'k2', 'k3']`
	2. `*args`: 要获取的`key`，如：`k1,k2,k3`

* `r.hgetall(name)`: 获取`name`对应的`hash`对象所有值

* `r.hlen(name)`: 获取`name`对应`hash`对象的长度

* `r.hkeys(name)`: 获取`name`对应`hash`对象的`keys`

* `r.hvalues(name)`: 获取`name`对应`hash`对象的`values`

* `r.hincrby(name, key, amount=1)`: 给`name`对应的`hash`对象的`key`的对应的`value`增加`amount`

* `r.hscan(name, cursor=0, match=None, count=None)`: 增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，从而放置内存被撑爆
	1. `name`，redis的name
	2. `cursor`，游标（基于游标分批取获取数据）
	3. `match`，匹配指定`key`，默认`None` 表示所有的`key`
	4. `count`，每次分片最少获取个数，默认`None`表示采用Redis的默认分片个数

  例如
  ```python
    # 第一次：cursor1, data1 = r.hscan('xx', cursor=0, match=None, count=None)
    # 第二次：cursor2, data1 = r.hscan('xx', cursor=cursor1, match=None, count=None)
    # ...
    # 直到返回值cursor的值为0时，表示数据已经通过分片获取完毕
    ```
* `r.hscan_iter(name, match=None, count=None)`: 利用yield封装hscan创建生成器，实现分批去redis中获取数据

#### 8.3.3 判断

* `r.hexists(name, key)`: 判断`name`对应的`hash`对象是否存在`key`

#### 8.3.4 删除

* `r.hdel(name, *keys)`: 删除`name`对应的`hash`对象的`key`

### 8.4 列表操作(list)
redis中的List在在内存中按照一个name对应一个List来存储

#### 8.4.1 增加

* `r.lpush(name, *values)`: 将`value`按顺序从左边插入到`name`对应的列表中

* `r.lpushx(name, *values)`: 当`name`存在时，将`value`按顺序从左边插入到`name`对应的列表中

* `r.rpush(name, *values)`: 将`value`按顺序从右边插入到`name`对应的列表中

* `r.rpushx(name, *values)`: 当`name`存在时，将`value`按顺序从右边插入到`name`对应的列表中

* `r.insert(name, where, refvalue, value)`: 指定在`refvalue`位置的`where`处插入
	1. `where`: `BEFORE` 或 `AFTER`
	2. `refvalue`: 标的值，存在多个，则第一个找到的位置为标的
	3. `value`: 待插入的数据

#### 8.4.2 获取
* `r.llen(name)`: 查看`name`列表的长度

* `r.lindex(name, index)`: 查看name列表的index位置的值

* `r.lrange(name, start, end)`: 获取`name`列表的`[start, end]`区间内的元素

#### 8.4.3 修改
* `r.lset(name, index, value)`: 给`index`位置从新赋值为`value`
	* `index`: 索引，从0开始计数
	
	
#### 8.4.4 删除
* `r.lrem(name, count, value)`: 删除`value`，`count`表示删除次数
	* `count=0`: 删除所用
	* `count>0`: 从前到后删除count个
	* `count<0`: 从后到前删除count个

* `r.lpop(name)`: 在`name`列表的左侧第一个元素删除并返回

* `r.rpop(name)`: 在`name`列表的右侧第一个元素删除并返回

* `r.ltrim(name, start, end)`: 在`name`列表中移除没有在`[start, end]`之间的值

* `r.rpoplpush(src, dst)`: 将`src`右边的值删除，并插入到`dst`列表的左边

* `r.blpop(keys, timeout=0)`: 从keys指定的列表左边开始删除并返回数，如果不能获取到数据则阻塞

* `r.brpop(keys, timeout=0)`: 从keys指定的列表右边开始删除并返回数，如果不能获取到数据则阻塞

* `r.brpoplpush(src, dst, timeout=0)`: 将`src`右边的值删除，并插入到`dst`列表的左边, 如果不能获得数据则阻塞

#### 8.4.5 自定义增量迭代
redis没有提供列表元素的增量迭代，如果想要循环name对应的列表所有元素，
那么就需要之定义，逻辑代码如下
```python
import redis
conn=redis.Redis(host='127.0.0.1',port=6379)
conn.lpush('test',*[1,2,3,4,45,5,6,7,7,8,43,5,6,768,89,9,65,4,23,54,6757,8,68])
# conn.flushall()

def scan_list(name, count=10):
    index = 0
    while True:
        data_list = conn.lrange(name,index,count+index-1)
        if not data_list:
            return
        index += count
        for item in data_list:
            yield item
		    
print(conn.lrange('test',0,100))
for item in scan_list('test',5):
    print('---')
    print(item)
```

### 8.5 集合操作(set)

#### 8.5.1 添加
* `r.sadd(name,*values)`: 给`name`集合添加指定`value`值
  
#### 8.5.2 删除
* `r.srem(name,*values)`: 从`name`集合中删除指定的`value`

* `r.spop(name)`: 随机删除并返回`name`中的一个元素

* `r.smove(src, dst, value)`: 将`src`中的`value`删除并添加到`dst`集合中

#### 8.5.3 获取
* `r.scard(name)`: 获取`name`集合中的元素个数

* `r.smembers(name)`: 获取`name`集合中的所有元素

* `r.srandmember(name)`: 随机返回集合`name`中的元素，不删除

* `r.srandmember(name, numbers)`: 随机从集合`name`中获取`numbers`个元素

* `r.sscan(name, cursor=0, match=None, count=None)`: 分片获取
* `r.sscan_iter(name, match=None, count=None)`: 分片获取

#### 8.5.4 运算
* `r.sismember(name, value)`: 判断`value`是否是`name`集合的元素

* `r.sinter(keys, *args)`: 求交集

* `r.sinterstore(dest,keys,*args)`: 求交集，并将交集保存在`dest`

* `r.sunion(keys.*args)`: 求并集

* `r.sunionstore(dest,keys,*args)`: 求并集，并将并集保存在`dest`

* `r.sdiff(key,*args)`: 求差集

* `r.sdiffstore(dset,key,*args)`: 求差集, 并将差集保存在`dest`中, 返回差集个数

### 8.6 `zset`操作 
有序集合，在集合的基础上，为每元素排序；
元素的排序需要根据另外一个值来进行比较，
所以，对于有序集合，每一个元素有两个值，
即：值和分数，分数专门用来做排序。

#### 8.6.1 添加
* `r.zadd(name, **kwargs)`: 向`name`中添加元素, 如果元素已存在, 则更新其score

* `r.zincrby(name, amount, value)`: 如果在`name`中已经存在元素`value`，则该元素的`score`增加`amount`，否则向该集合中添加该元素，其`score`的值为`amount`

#### 8.6.2 删除
* `r.zrem(name, *values)`: 在`name`中删除`value`

* `r.zremrangebyrank(name, min, max)`: 删除`name`中排名在`min`和`max`之间的`value`，并返回删除的元素个数

* `r.zremrangebyscore(name, min, max)`: 删除`name`中`score`在给定区间的元素，并返回删除的元素个数

#### 8.6.3 获取
* `r.zrank(name, value)`: 返回`name`中元素`value`的排名下标(按`score`从小到大)

* `r.zrevrank(name,value)`: 返回`name`中元素`value`的排名下标(按`score`从大到小)

* `r.zrange(name, start, end, desc=False, withscores=False, score_cast_func=float)`: 按照索引范围获取`name`对应的有序集合的元素, 从小到大排序
	1. `name`: `redis`的`name`
    2. `start`: 有序集合索引起始位置（非分数）
    3. `end`: 有序集合索引结束位置（非分数）
    4. `desc`: 排序规则，默认按照分数从小到大排序
    5. `withscores`: 是否获取元素的分数，默认只获取元素的值
    6. `score_cast_func`: 对分数进行数据转换的函数

* `r.zrevrange(name, start, end, withscores=False, score_cast_func=float)`: 按照索引范围获取`name`对应的有序集合的元素, (从大到小排序)

* `r.zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float)`: 按照分数范围获取name对应的有序集合的元素,从小到大排序

* `zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float)`: 按照分数范围获取name对应的有序集合的元素,从大到小排序

* `r.zscan(name, cursor=0, match=None, count=None, score_cast_func=float)`: 分片获取
* `r.zscan_iter(name, match=None, count=None,score_cast_func=float)`: 分片获取

### 8.7 其他操作

* `r.delete(*names)`: 删除redis中的任意数据类型

* `r.exists(name)`: 检测redis的name是否存在

* `r.keys(pattern='*')`: 根据模型获取redis的name
	* pattern: 正则表达式
* `r.expire(name ,time)`: 为某个redis的某个name设置超时时间

* `r.rename(src, dst)`: 对redis的name重命名为

* `r.move(name, db)`: 将redis的某个值移动到指定的db下

* `r.randomkey()`: 随机获取一个redis的name（不删除）

* `r.type(name)`: 获取name对应值的类型

* `r.scan(cursor=0, match=None, count=None)`: 分片获取name
* `scan_iter(match=None, count=None)`:分片获取name




### 8.8 管道
`redis-py`默认在执行每次请求都会创建（连接池申请连接）和断开（归还连接池）
一次连接操作，如果想要在一次请求中指定多个命令，
则可以使用`pipline`实现一次请求指定多个命令，
并且默认情况下一次`pipline`是原子性操作。

```python
import redis
 
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
 
r = redis.Redis(connection_pool=pool)
 
# pipe = r.pipeline(transaction=False)
pipe = r.pipeline(transaction=True)  # 开启事务
pipe.multi()
pipe.set('name', 'alex')
pipe.set('role', 'sb')
 
pipe.execute()  # 执行事务
```
只有执行了`execute`才能将`redis`中的数据修改
