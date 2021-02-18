# 一、redis介绍

Redis是由意大利人Salvatore Sanfilippo（网名：antirez）开发的一款内存高速缓存数据库。Redis全称为：Remote Dictionary Server，该软件使用C语言编写，Redis是一个key-value存储系统，它支持丰富的数据类型，如： **string、list、set、zset(sorted set)、hash** 。

**Redis特点**: Redis以内存作为数据存储介质，所以读写数据的效率极高，远远超过数据库。

**Redis应用场景**: 因为Redis交换数据快，所以在服务器中常用来存储一些需要频繁调取的数据， 将这种热点数据存到Redis（内存）中，要用的时候，直接从内存取，极大的提高了速度和节约了服务器的开销。

## 1.1 比较memcache
**相较于memcache**
1. memcache只支持字符串类型
2. memcache不支持**持久化**(不能将数据放在硬盘上)

## 1.2 redis的优势
1. **速度快**，数据在内存中以`key-value`形式保存保存，查找速度快。
2. 它支持**丰富的数据类型**，如： **string、list、set、zset(sorted set)、hash** 。
3. **支持事务**，操作都是原子性
4. **丰富的特性**，可用于缓存、消息、按`key`设置过期时间

## 1.3 基于单进程、单线程架构
redis基于单进程、单线程，不存在并发访问问题。redis6.0后修改为多线程
* 数据保存在内存
* io多路复用技术
* 没有进程和线程直接的切换

# 二、redis安装

## 2.1 命令安装

```shell
sudo apt update
sudo apt install redis-server
```

## 2.2 编译安装

* 下载

  ```shell
  sudo wget http://download.redis.io/releases/redis-5.0.5.tar.gz
  sudo tar -zvxf redis-5.0.5.tar.gz
  ```

* 编译

  ```shell
  cd redis-5.0.5
  make
  ```

* 安装

  ```shell
  cd src
  sudo make install
  ```

* 配置

  ```shell
  sudo mkdir /etc/redis
  cd ..
  sudo cp redis.conf /etc/redis
  sudo vim /etc/redis/redis.conf  # 将属性daemonize的值改为为yes
  cd utils
  sudo cp redis_init_script /etc/init.d/redis
  sudo vim /etc/init.d/redis  # 打开启动文件按下面内容进行修改
  ```

  ```shell
  #!/bin/sh
  # chkconfig: 2345 10 90   // 此处修改
  # description: Start and Stop redis  //此处修改
  # Simple Redis init.d script conceived to work on Linux systems
  # as it does use of the /proc filesystem.
  
  ### BEGIN INIT INFO
  # Provides:     redis_6379
  # Default-Start:        2 3 4 5
  # Default-Stop:         0 1 6
  # Short-Description:    Redis data structure server
  # Description:          Redis data structure server. See https://redis.io
  ### END INIT INFO
  
  REDISPORT=6379
  EXEC=/usr/local/bin/redis-server  # 自己的安装路径，默认可修改
  CLIEXEC=/usr/local/bin/redis-cli  # 自己的安装路径，默认可修改
  
  PIDFILE=/var/run/redis_6379.pid   # redis.conf 文件里面有。可复制过来
  CONF="/etc/redis/redis.conf"  # 配置文件redis.conf所在目录
  case "$1" in
      start)
          if [ -f $PIDFILE ]
          then
                  echo "$PIDFILE exists, process is already running or crashed"
          else
                  echo "Starting Redis server..."
                  $EXEC $CON &  # 添加 & 表示可以后台运行
          fi
          ;;
      stop)
          if [ ! -f $PIDFILE ]
          then
                  echo "$PIDFILE does not exist, process is not running"
  
          else
                  PID=$(cat $PIDFILE)
                  echo "Stopping ..."
                  $CLIEXEC -p $REDISPORT shutdown
                  while [ -x /proc/${PID} ]
                  do
                      echo "Waiting for Redis to shutdown ..."
                      sleep 1
                  done
                  echo "Redis stopped"
          fi
          ;;
      *)
          echo "Please use start or stop as first argument"
          ;;
  esac
  
  ```

* 使文件生效

  * 可以重启电脑

  * 执行命令

    ```shell
    sudo chmod +x /etc/init.d/redis
    sudo update-rc.d redis defaults
    ```


# 三、常用命令

## 3.1 进入退出

| 命令                | 作用                              |
| ------------------- | --------------------------------- |
| `redis-cli`         | 进入Redis数据库，但是不能显示中文 |
| `redis-cli   --raw` | 进入Redis数据库，能显示中文       |
| `exit`              | 退出数据库                        |

**补充命令：** `select n` 

> 该命令用于切换到指定的数据库，数据库索引号 index 用数字值指定，以 0 作为起始索引值。
> 默认使用 0 号数据库   默认开16个库
>
> **比如：**
>
> 使用1号数据库
>
> `select 1`

## 3.2 数据类型

`Redis`数据库有五大数据类型

| 数据类型 |   含义   |
| :------: | :------: |
| `String` |  字符串  |
|  `Hash`  |   哈希   |
|  `List`  |   列表   |
|  `Set`   |   集合   |
|  `Zset`  | 有序集合 |

### 3.2.1 String类型数据的操作命令

> * string 类型是 redis 最基本的类型, 
> * string 类型，一个 key 对应一个 value，一个 value 最大能存储512MB的数据。

| 命令                                | 作用                                    | 其他                                                         |
| :---------------------------------- | --------------------------------------- | ------------------------------------------------------------ |
| `set key value`                     | 设置给定 `key` 的值                     | 如果 `key` 已经存储其他值，` SET` 就覆写旧值，且无视类型     |
| `mset key1 value1 [key2 value2 ..]` | 为多组`key`设置值                       | 该操作为原子操作，要么一组都设置成功，要么一组都设置失败     |
| `get key`                           | 返回`key`的值                           | 若`key`不存在则返回`nil`                                     |
| `mget key1 [key2 ... ]`             | 返回一个或多个`key`的值                 | 若`key`不存在返回`nil`，若`key`存在但不是字符串返回`nil`     |
| `append key value`                  | 将指定的值追加到`key`末尾               | 若`key`不存在，则创建并赋值，返回追加后的字符串长度          |
### 3.2.2 全局key操作命令

| 命令                            | 作用                                    | 其他                                                         |
| :------------------------------ | :-------------------------------------- | :----------------------------------------------------------- |
| `ttl key`                       | 返回`key`的剩余生存时间                 | `-1 `表示永久存在，` -2`表示不存在                           |
| `set  key  value  ex  seconds ` | 设置`key`的同时，设置过期时间(单位：秒) | `key `过期后将不再可用，会被系统自动删除。                   |
| `persist key`                   | 移除指定`key`的生存时间                 | 成功返回`1`，若`key`不存在或不存在生存时间时返回`0`；        |
| `rename key newkey`             | 改名                                    | 当`key`和`newkey`相同或者`key`不存在时返回一个错误，当`newkey`已存在时则会覆盖； |
| `keys * `                       | 查看所有的`key`                         |                                                              |
| `del key`                       | 删除                                    | 返回成功的个数                                               |
| `exists key`                    | 查看`key`是否存在                       | 返回存在个个数                                               |
| `type key`                      | 查看key类型                             |                                                              |
| `expire key seconds`            | 设置过期时间                            |                                                              |

### 3.2.3 List数据类型操作命令

> - 列表的元素类型为string，
> - 按照插入顺序排序

| 命令                          | 作用                   | 其他                                    |
| ----------------------------- | ---------------------- | --------------------------------------- |
| `lpush key value[value...]`   | 在头部插入数据         |                                         |
| `rpush key value [value ...]` | 在尾部添加数据         |                                         |
| `lindex key index`            | 返回列表中元素的值     | index从0开始，当index超出索引时返回null |
| `lrange key start stop`       | 查看索引范围内元素的值 |                                         |
| `llen key`                    | 返回列表的长度         |                                         |
| `lset key index newvalue`     | 指定索引号进行修改     |                                         |
| `lpop key`                    | 头部删除数据           |                                         |
| `rpop key`                    | 尾部删除数据           |                                         |

### 3.2.4 Hash数据类型操作命令

> * 是一个键值(key=>value)对集合。
> * 是string 类型的 field 和 value 的映射表，hash 特别适合用于存储对象, field 域, value 值

| 命令                                         | 作用                                | 其他                                            |
| -------------------------------------------- | ----------------------------------- | ----------------------------------------------- |
| `hset key field value`                       | 将field-value设置到hash表中         | 若key不存在会新建hash表再赋值，已存在则会覆盖； |
| `hmset key field1 value1[field2 value2 ...]` | 同时将多个field-value设置到hash表中 |                                                 |
| `hget key field`                             | 获取`value`值                       |                                                 |
| `hmget key field[field...]`                  | 获取多个`value`                     |                                                 |
| `hvals key`                                  | 获取全部`value`                     |                                                 |
| `hkeys key`                                  | 获取所有的`field`                   |                                                 |
| `hgetall key`                                | 获取全部`field` 和 `value`          |                                                 |
| `hlen key`                                   | 查看有几个键值对                    |                                                 |
| `hexists key field`                          | 判断hash表中指定`field`是否存在     | 若存在，则返回1；若key或field不存在，则返回0    |
| `hdel key field`                             | 删除                                |                                                 |

### 3.2.5 Set数据类型操作名

> * 元素为string类型
> * 无序集合
> * 元素具有唯一性，不重复 

| 命令                          | 作用                                    | 其他                                                  |
| ----------------------------- | --------------------------------------- | ----------------------------------------------------- |
| `sadd key member [member...]` | 将一个或多个`member`元素加入到集合key中 | 若member已存在那么会忽略此元素                        |
| `scard key`                   | 返回集合key中元素的个数                 |                                                       |
| `smembers key`                | 获取集合中所有元素                      |                                                       |
| `sismember key member`        | 判断集合存在某个值                      | 判断member在key中是否已存在, 返回0或1                 |
| `srem key member [member...]` | 移除一个或多个元素                      | 不存在的member会被忽略，返回被移除元素个数            |
| `spop key`                    | 随机删除                                | 移除并返回集合中的一个随机元素，当key不存在时返回NULL |

### 3.2.6 Zset数据类型的操作命令

> * 类似于Set
> * 不同的是Sorted中的每个成员都分配了一个分数（Score）用于对其中的成员进行排序（升序）。
> * zset的成员是唯一的,但分数(score)却可以重复。

| 命令                                         | 作用                              | 其他                    |
| -------------------------------------------- | --------------------------------- | ----------------------- |
| `zadd key score member [ [score member] ..]` | 添加数据                          | 存在就更新              |
| `zscore key member`                          | 查看score值                       |                         |
| `zrange key start stop[withscores]`          | 按索引返回key的成员               | withscores表示显示score |
| `zrangebyscore key min max`                  | 返回集合中 score 在给定区间的元素 |                         |
| `zrem key member [member...]`                | 移除有序集合中的一个或多个元素    | 若member不存在则忽略    |
| `zremrangebyrank min max`                    | 删除集合中索引在给定区间的元素    |                         |
| `zremrangebyscore  min max`                  | 删除集合中 score 在给定区间的元素 |                         |














