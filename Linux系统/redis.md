# NoSQL分类

NoSQL大体上可以分为4种类型: **key-value、Document-Oriented\Column-Family DataBases、Graph-Oriented Databases**

## Key-value(键值)数据库

键值数据库就像在传统语言中使用的哈希表。可以通过key来添加、查询或删除、鉴于使用主键访问、所以会获得不错的性能及扩展性。

常见的产品有: **Riak、Redis、Memcache**等。

使用场景: **存储用户信息(会话、配置文件、参数等等)**

* 如果查询是通过值进行的，则不适用该数据库
* 需要存储数据之间的关系，则不适用该数据库
* 事务支持，键值数据库中事务支持不好

## Document-Oriented(面向文档)数据库

将数据以文档的形式存储，每个文档都是自包含的数据单元，是一系列数据项的集合。每个数据项都有一个名称与对应值

常见产品: **MongoDB、CouchDB**等

使用场景: **日志、分析**

* 在不同的文档上添加事务

## 列存储数据库

将数据存储在列族中，一个列族存储经常被一起查询的相关数据。

使用场景: **日志，博客平台**

* 不支持事务和原型设计

## 图数据库

# redis

## 命令安装

```
yum install -y redis
```

## 编译安装

```shell
wget https://download.redis.io/releases/redis-5.0.11.tar.gz

tar -xf redis-5.0.11.tar.gz

cd redis-5.0.11

make

make test
```

## 编译生成的可执行文件

```shell
redis-benchmark  # 性能测试
redis-check-aof  # 检查修复aof文件
redis-check-rdb  # 检查修复rdb文件
redis-cli        # redis的客户端
redis-sentinel   # redis的集群
redis-server     # redis的服务端
redis-trib.rb    # 集群管理
```

## 启动redis

```shell
./src/redis-server # 默认端口是6379，默认启动会占用终端
```

## 性能测试

默认是100000,50个同时发起连接

```shell
./src/redis-benchmark -q

PING_INLINE: 73855.24 requests per second
PING_BULK: 73800.73 requests per second
SET: 74074.07 requests per second
GET: 72833.21 requests per second
INCR: 73637.70 requests per second
LPUSH: 73855.24 requests per second
RPUSH: 70175.44 requests per second
LPOP: 72202.16 requests per second
RPOP: 74183.98 requests per second
SADD: 74962.52 requests per second
HSET: 75642.96 requests per second
SPOP: 73746.31 requests per second
LPUSH (needed to benchmark LRANGE): 74850.30 requests per second
LRANGE_100 (first 100 elements): 48379.30 requests per second
LRANGE_300 (first 300 elements): 24172.11 requests per second
LRANGE_500 (first 450 elements): 18670.65 requests per second
LRANGE_600 (first 600 elements): 15384.62 requests per second
MSET (10 keys): 78186.08 requests per second
```

## 连接redis

```shell
./src/redis-cli
```

* `-h` ip地址
* `-p` 端口
* `-s` 套接字
* `-a` 密码
* `-n` 指定redis的库

`redis`的命令是不区分大小写

## 命令

1. `ping`: 测试redis连接是否成功，返回`pong`表示成功

2. `info`: 查看系统信息

3. `echo`: 输出指定内容

4. `quit exit`: 退出连接

5. `select n`: 选择第`n`个数据库

## redis中的数据类型

- `string`：字符串
- `hash`
- `list`：列表
- `set`：集合
- `zset`：有序集合

### 全局key操作

|命令|作用|
|:---:|:---:|
|`del key`|删除`key`|
|`exists key`|判断`key`是否存在，存在为`1`，不存在为`0`|
|`expire key seconds`|设置过期时间, 过期自动删除|
|`ttl key`|返回`key`的剩余生存时间,`-1`表示永久存在，`-2`表示不存在|
|`persist key`|移除指定`key`的生存时间|
|`pexpire key millseconds`|设置过期时间，以毫秒为单位|
|`pttl key`|查看`key`的生存周期，毫秒为单位|
|`keys pattern`|查看满足`patter`规则的所有`key`, 支持模糊匹配|
|`type key`|查看`key`类型|
|`move key n`|移动`key`到`n`号数据库|
|`rename key newkey`|改名, `key`不存在报错，`newkey`存在则覆盖|
|`renamenx key newkey`|改名, `key`不存在报错，`newkey`存在则不进行操作|
|`randomkey`|随机获取一个`key`|

### string命令

|命令|作用||
|:---:|:---:|:---:|
|`set key value [ex seconds][px millseconds] [nx][xx]`|设置`key-value`，可以设置过期时间|`ex or px`: 过期时间; `nx`：key不存在设置，`xx`：`key`存在才操作|
|`get key`|获取`key`对应的值|`key`不存在返回`nil`|
|`mset key1 value1 [key2 value2 ...]`|设置多组值|该操作为原子操作，要么全成功，要么全失败|
|`mget key1 [key2 key3 ...]`|获取多组值||
|`getset key value`|获取指定`key`，并设置为`value`|`key`不能存在返回`nil`|
|`strlen key`|获取`key`对应的`value`的长度||
|`apppend key value`|在`key`对应`value`后面追加额外的`value`|`key`存在则追加，`key`不存在则新建|
|`incr key`|将`key`对应的数字加上`1`| `key`存在则进行加值操作，否则设置为`1`|
|`decr key`|将`key`对应的数字减去`1`|`key`存在则进行减值操作，否在设置为`-1`|
|`incrby key amount`|将`key`对应的数字加上`amount`|`amount`默认为1, key存在则进行加值操作，否则设置为`amount`|
|`decrby key amount`|将`key`对应的数字减去`amount`|`amount`默认为1，key存在则进行减值操作，否在设置为`-amount`|
|`getrange key start end`|`key`对应`value`进行切片操作|`[start, end]`|
|`incrbyfloat key amount`|增值操作，`amount`为浮点数|末日保留17位小数|

### list操作命令

> - 列表的元素类型为string，
> - 按照插入顺序排序

| 命令 | 作用 | 其他 |
|:---: |:---:|:---:|
|`lpush key value [value ...]`| 在头部插入数据|`key`不存在则创建|
|`lpushx key value [value...]`| 在头部插入数据|`key`不存在则不进行任何操作|
|`rpush key value [value ...]`| 在尾部添加数据|`key`不存在则创建|
|`rpushx key value [value...]`| 在尾部添加数据|`key`不存则不进行任何操作|
|`lindex key index`           | 返回列表中索引为`index`的元素的值| `index`从`0`开始，当`index`超出索引时返回`null` |
|`linsert key [before after] value1 value2`|在`value1`前面或后面插入`value2`|`value1`不存在则不进行任何操作|
|`lrange key start stop`      | 查看索引范围内元素的值||
|`llen key`                   | 返回列表的长度||
|`lrem key count value`       | 删除`value`，`count`表示删除次数|`count=0`删除所有，`count>0`从前到后删除`count`个, `count<0`从后到前删除`count`个|
|`ltrim key start end`        | 移除没有在`[start, end]`之间的元素值||
|`lset key index newvalue`    | 指定索引号进行修改||
|`lpop key`                   | 从头部删除数据，返回删除的数据 |`key`不存在返回`nil`|
|`rpop key`                   | 从尾部删除数据，返回删除的数据 ||

### hash操作命令

> * 是一个键值(`key=>value`)对集合。
> * 是`string` 类型的 `field` 和 `value` 的映射表，`hash` 特别适合用于存储对象, `field` 域, `value` 值

| 命令| 作用| 其他 |
| :---: | :---: | :---: |
| `hset key field value`                       | 将`field-value`设置到`key`指定`hash`表中 | 若`key`不存在会新建hash表再赋值，已存在则会覆盖； |
| `hsetnx key field value`                     | 将`field-value`设置到`key`指定`hash`表中 | 若`field`以存在则操作无效，`field`不存在则新增|
| `hmset key field1 value1[field2 value2 ...]` | 同时将多个`field-value`设置到`key`指定`hash`表中 ||
| `hget key field`                             | 获取`value`值||
| `hmget key field[field...]`                  | 获取多个`value`||
| `hvals key`                                  | 获取全部`value`||
| `hkeys key`                                  | 获取所有的`field`||
| `hgetall key`                                | 获取全部`field` 和 `value`||
| `hlen key`                                   | 查看有几个键值对||
| `hexists key field`                          | 判断hash表中指定`field`是否存在| 若存在，则返回1；若key或field不存在，则返回0    |
| `hdel key field [field ...]`                 | 删除`key`中的`field`||
| `hexists key field`                          | 判断`key`中是否存在`field`|0表示不存在，1表示存在|
| `hincrby key field amount`                   | 对`key`中`field`对应的`value`进行增值操作||


### set操做命令

> * 元素为string类型
> * 无序集合
> * 元素具有唯一性，不重复 

| 命令 | 作用 | 其他 |
| :---: | :---: | :---: |
| `sadd key member [member...]` | 将一个或多个`member`元素加入到集合key中 | 若member已存在那么会忽略此元素 |
| `scard key`                   | 返回集合`key`中元素的个数 | |
| `smembers key`                | 获取集合`key`中所有元素 | |
| `sismember key member`        | 判断集合存在某个值 | 判断`member`在`key`中是否已存在, 返回0或1 |
| `srem key member [member...]` | 移除一个或多个元素 | 不存在的member会被忽略，返回被移除元素个数|
| `spop key [count]`            | 随机删除 | |
| `sdiff key1 key2`             | 求集合`key1`与集合`key2`差集|`key1-key2`|
| `sinter key1 key2`            | 求集合`key1`与集合`key2`的交集||
| `sunion key1 key2`            | 求集合`key1`与结合`key2`的并集||
| `smove src dst value`         | 将集合`src`中的`value`移动到集合`dst`|`dst`如果不存则新建， `src`如果不存在则不进行操作|
| `srandmenber key count`       | 随机获取`key`中的`count`个元素| `count`默认为 `1`|


### zset操作命令
> * 类似于Set
> * 不同的是Sorted中的每个成员都分配了一个分数（Score）用于对其中的成员进行排序（升序）。
> * zset的成员是唯一的,但分数(score)却可以重复。

| 命令                                         | 作用                              | 其他                    |
| -------------------------------------------- | --------------------------------- | ----------------------- |
| `zadd key score member [ [score member] ..]` | 添加数据                          | 存在就更新              |
| `zscore key member`                          | 查看`score`值                       |                         |
| `zrange key start stop[withscores]`          | 按索引返回`key`的成员               | `withscores`表示显示`score` |
| `zrangebyscore key min max`                  | 返回集合中 `score` 在给定区间的元素 |                         |
| `zrem key member [member...]`                | 移除有序集合中的一个或多个元素    | 若`member`不存在则忽略    |
| `zremrangebyrank min max`                    | 删除集合中索引在给定区间的元素    |                         |
| `zremrangebyscore  min max`                  | 删除集合中 `score` 在给定区间的元素 |                         |


# redis主从





