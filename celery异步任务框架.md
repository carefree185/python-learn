## 十 celery介绍和简单使用

当数据库中的数据被删除时，缓存中的数据没有更新。造成展示页面的数据和 保存的数据不匹配。使用celery来实现定时任务，异步任务

### 10.1 介绍

Celery是一个简单、灵活且可靠的，处理大量消息的分布式系统 专注于实时处理的异步任务队列 同时也支持任务调度

**应用场景**

1. 异步执行: 解决耗时任务,将耗时操作任务提交给Celery去异步执行，比如发送短信/邮件、消息推送、音视频处理等等
2. 延迟执行: 解决延迟任务
3. 定时执行: 解决周期(周期)任务,比如每天数据统计


* **可以不依赖任何服务器，通过自身命令，启动服务(内部支持socket)**
* **celery服务为为其他项目服务提供异步解决任务需求的**

### 10.2 celery异步任务架构

Celery的架构由三部分组成，

1. 消息中间件（message broker）
2. 任务执行单元（worker）
3. 任务执行结果存储（task result store）

![](./.img/celery.jpg)

* **消息中间件**: Celery本身不提供消息服务，但是可以方便的和第三方提供的消息中间件集成。包括，RabbitMQ, Redis等等

* **任务执行单元**: Worker是Celery提供的任务执行的单元，worker并发的运行在分布式的系统节点中

* **任务结果存储**: Task result store用来存储Worker执行的任务的结果，Celery支持以不同方式存储任务的结果，包括AMQP, redis等

### 10.3 celery的两种使用结构

1. 如果 `Celery`对象:`Celery(...)` 是放在一个模块下的
	* 终端切换到该模块所在文件夹位置：scripts
	* 执行启动worker的命令：`celery worker -A 模块名 -l info -P eventlet`
	

2. 如果 Celery对象:Celery(...) 是放在一个包下的
	* 必须在这个包下建一个`celery.py`的文件，将`Celery(...)`产生对象的语句放在该文件中
	* 执行启动`worker`的命令：`celery worker -A 包名 -l info -P eventlet`


* 注：`windows`系统需要`eventlet`支持，`Linux`与`MacOS`直接执行：`celery worker -A 模块名 -l info`


### 10.4 通过包来管理使用Celery--添加异步任务delay

建立一个`celery_task`包，里面必须要有一个`celery.py`文件

在`celery.py`中生成celery的app
```python
from celery import Celery

broker = 'redis://127.0.0.1:6379/1'  # 任务中间件
backend = 'redis://127.0.0.1:6379/2'  # 结果存放

app = Celery(__name__, broker=broker, backend=backend, include=['celery_task.task'])
```
在`celery_task`包中写新建任务`task.py`，在里面写任务
```python
from .celery import app


@app.task
def add(x, y):
    print(x, y)
    return x + y
```
在`app`中包含任务


在任意要添加任务的位置写下列代码
```python
from celery_task.task import add

result = add.delay(3, 4)  # 返回值为任务的uuid值。用于获取任务结果
print(result)
```

在任意要获取结果的位置写下列代码

```python
from celery_task.celery import app
from celery.result import AsyncResult

id = '5f27dc65-493e-48d4-9f03-82546a6b8488'
if __name__ == '__main__':
    async_result = AsyncResult(id=id, app=app)
    if async_result.successful():
        result = async_result.get()
        print(result)
    elif async_result.failed():
        print('任务失败')
    elif async_result.status == 'PENDING':
        print('任务等待中被执行')
    elif async_result.status == 'RETRY':
        print('任务异常后正在重试')
    elif async_result.status == 'STARTED':
        print('任务已经开始被执行')
```


### 10.5 添加延迟任务apply_async
时间使用`utc`标准时间
```python
from celery_task.task import add

# 添加延迟任务
from datetime import datetime, timedelta

eta = datetime.utcnow() + timedelta(seconds=10)  # 需要utc时间

result = add.apply_async(args=(5, 10), eta=eta)  # args是任务需要的参数
print(result)
```








### 10.6 添加定时任务
在`celery.py`中配置
```python
from celery import Celery

broker = 'redis://127.0.0.1:6379/1'  # 任务中间件
backend = 'redis://127.0.0.1:6379/2'  # 结果存放

app = Celery(__name__, broker=broker, backend=backend, include=['celery_task.task'])


app.conf.timezone = 'Asia/Shanghai'  # 设置时区

app.conf.enable_utc = False  # 禁用utc时间

from datetime import timedelta
from celery.schedules import crontab
app.conf.beat_schedule = {
    "add_task": {
        'task': 'celery_task.task.add',  # 指定任务
        # 'schedule': timedelta(seconds=5),  # 时间间隔
        'schedule': crontab(hour=8, day_of_week=1),  # 每周一早上8点执行任务
        'args': (3, 5)  # 任务需要的参数
    }
}
```
启动一个beat，用于自动添加任务
`celery -A celery_task beat -l info`

