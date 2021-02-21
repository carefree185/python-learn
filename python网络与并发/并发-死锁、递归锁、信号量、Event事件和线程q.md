# 死锁
程序中使用锁过于的的情况会容易造成程序卡死(阻塞)

```python
from threading import Thread, Lock
import time

loc1 = Lock()  # 生成锁1
loc2 = Lock()  # 生成锁2


class MyThread(Thread):
    def run(self):
        self.func1()
        self.func2()

    def func1(self):
        loc1.acquire()  # 枪锁1
        print("线程%s 抢到锁loc1" % self.name)
        loc2.acquire()  # 枪锁2
        print("线程%s 抢到锁loc2" % self.name)
        loc2.release()  # 释放锁2
        loc1.release()  # 释放锁1

    def func2(self):
        loc2.acquire()  # 枪锁2
        print("线程%s 抢到锁loc2" % self.name)
        time.sleep(2)
        loc1.acquire()  # 枪锁1
        print("线程%s 抢到锁loc1" % self.name)
        loc1.release()  # 释放锁1
        loc2.release()  # 释放锁2


if __name__ == '__main__':
    for i in range(10):
        t = MyThread()
        t.start()
```
> 1. 程序开启了10个线程，假设`Thread-1`抢到`GIL`则`Thread-1`开始执行
> 2. `Thread-1`先执行`func1`，它可以顺利抢到`loc1`，没有线程和他争抢，顺利执行下去.
> 3. `Thread-1`执行到`func2`，还没有线程和它抢锁，也可以顺利拿到`loc2`，此时`Thread-1`遇到阻塞，此时释放`GIL`, 切换线程. 此时假设`Thread-2`抢到`GIL`，线程`Thread-2`开始执行
> 4. `Thread-2`此时也没有其他线程给他竞争锁`loc1`, 开始执行，当`Thread-2`要开始抢锁`loc2`时，`Thread-1`持有锁`loc2`还未释放，会导致`Thread-2`阻塞。此时，释放`GIL`。此时唯有的两把锁被线程`Thread-1`和`Thread-2`占据。就算其他线程抢到了`GIL`，也不会获取到`loc1`和`loc2`，导致其他线程不会执行。会立即切换
> 5. 不妨假设就切换到了线程`Thread-1`，此时`Thread-1`需要获取锁`loc1`, 但是此时锁`loc1`还被线程`Thread-2`占居。这样就导致了程序阻塞
****
# 递归锁

当递归锁被一个线程或进程获取到后，这个线程或进程可以 **连续** 的`acquire`和`release`，
> 1. 锁的内部有一个计数器, 当被`acquire`一次，计数器`+1`; 被`release`一次，计数器`-1`
> 2. **只要计数器不为`0`, 其他的线程或进程都不能获取到这把锁** 

```python
from threading import Thread, RLock
import time


loc1 = loc2 = RLock()


class MyThread(Thread):
    def run(self):
        self.func1()
        self.func2()

    def func1(self):
        loc1.acquire()  # 枪锁1
        print("线程%s 抢到锁loc1" % self.name)
        loc2.acquire()  # 枪锁2
        print("线程%s 抢到锁loc2" % self.name)
        loc2.release()  # 释放锁2
        print("线程%s 释放锁loc2" % self.name)
        loc1.release()  # 释放锁1
        print("线程%s 释放锁loc1" % self.name)

    def func2(self):
        loc2.acquire()  # 枪锁2
        print("线程%s 抢到锁loc2" % self.name)
        time.sleep(2)
        loc1.acquire()  # 枪锁1
        print("线程%s 抢到锁loc1" % self.name)
        loc1.release()  # 释放锁1
        print("线程%s 释放锁loc1" % self.name)
        loc2.release()  # 释放锁2
        print("线程%s 释放锁loc2" % self.name)


if __name__ == '__main__':
    for i in range(10):
        t = MyThread()
        t.start()


```

****
# 信号量
**信号量在并发中是指的锁**
* 信号量`semaphore`可以控制同时运行执行的线程数量。
* 信号量`semaphore`内部维护了一个条件变量和一个计数器。

```python
from threading import Thread, Semaphore, current_thread
import time
import random

sm = Semaphore(5)  # 每次能够运行的线程


def task():
    sm.acquire()
    print(f"{current_thread().name}正在运行: {time.time()} ")
    time.sleep(random.randint(2, 4))
    print(f"{current_thread().name}结束: {time.time()} ")
    sm.release()


if __name__ == '__main__':
    for i in range(20):
        t = Thread(target=task)
        t.start()
```
****
# `Event`事件
进程(线程)需要等待其他的进程(线程)运行结束后才能结束运行，类似与发送信号

```python
from threading import Thread, Event, current_thread
import time

event = Event()  # 创建等待事件


def light():
    while True:
        print("红灯亮着")
        time.sleep(3)
        print("绿灯亮了")
        # 告诉等待红灯的人可走了
        event.set()  # 发送信号


def car():
    print(f"{current_thread().name}在等待")
    event.wait()  # 等待信号, 收到信号结束等待
    print(f"{current_thread().name}等待结束")


if __name__ == '__main__':
    t = Thread(target=light)
    t.start()

    for i in range(20):
        Thread(target=car).start()
```
****
# 线程`Q`(线程使用的队列)
同一个进程下的多个线程数据共享，使用队列保证多个线程操作同一份数据时不会出现数据混淆问题，保证数据安全。

## 一、`queue` 模块定义了下列类和异常

###  1.1 类

* class `queue.Queue(maxsize=0)`

  FIFO队列的构造函数。

  * `maxsize`是一个整数，它设置可以放置在队列中的项数的上限。一旦达到此大小，插入将阻塞，直到使用队列项。
  * 如果`maxsize`小于或等于零，则队列大小为无穷大。

* *class* `queue.LifoQueue(maxsize=0)`

  LIFO 队列构造函数。 

  * `maxsize`是个整数，用于设置可以放入队列中的项目数的上限。当达到这个大小的时候，插入操作将阻塞至队列中的项目被消费掉。
  * 如果 `maxsize` 小于等于零，队列尺寸为无限大。

* *class* `queue.PriorityQueue(maxsize=0)`

  优先级队列构造函数。

  *  `maxsize`是个整数，用于设置可以放入队列中的项目数的上限。当达到这个大小的时候，插入操作将阻塞至队列中的项目被消费掉。
  * 如果`maxsize`小于等于零，队列尺寸为无限大。
  * 这个队列保存的是元组`(level, data)`

* *class* `queue.SimpleQueue`

  无界的 FIFO 队列构造函数。简单的队列，缺少任务跟踪等高级功能。

### 1.2 异常

- exception `queue.Empty`

  对空的 `Queue` 对象，调用非阻塞的 `get()` (or `get_nowait()`) 时，引发的异常。

- *exception* `queue.Full`

  对满的 `Queue`对象，调用非阻塞的`put()` (or `put_nowait()`) 时，引发的异常。

## 二、Queue对象的方法

队列对象 (`Queue`, `LifoQueue`, 或者 `PriorityQueue`) 提供下列描述的公共方法。

* `Queue.qsize()`

  ​	返回队列的大致大小。注意:

  * `qsize()` > 0 不保证后续的 `get() `不被阻塞
  * `qsize() `<` maxsize` 也不保证 `put() `不被阻塞。

* `Queue.empty()`

  如果队列为空，返回 `True` ，否则返回 `False` 。

  * 如果 empty() 返回 `True` ，不保证后续调用的 `put()` 不被阻塞。类似的，
  * 如果 empty() 返回 `False` ，也不保证后续调用的` get() `不被阻塞。

* `Queue.full()`

  如果队列是满的返回 `True` ，否则返回 `False` 。

  * 如果` full()` 返回 `True` 不保证后续调用的 `get()` 不被阻塞。类似的，
  * 如果` full()` 返回 `False` 也不保证后续调用的` put() `不被阻塞

* `Queue.put(item, block=True, timeout=None)`

  将 *item* 放入队列。

  * 如果可选参数 `block = true` 并且 `timeout = None` (默认)，则在必要时阻塞至有空闲插槽可用。	
    * 如果 `timeout` 是个正数，将最多阻塞 `timeout`秒，如果在这段时间没有可用的空闲插槽，将引发 `Full` 异常。
  * 反之 `block = false`，如果空闲插槽立即可用，则把 `item` 放入队列，否则引发 `Full`异常 ( 在这种情况下，`timeout` 将被忽略)。

* `Queue.put_nowait(item)`

  相当于 `put(item, False)` 

* `Queue.get(block=True, timeout=None)`

  从队列中移除并返回一个项目

  * 如果可选参数 `block= true` 并且 `timeout = None` (默认值)，则在必要时阻塞至项目可得到。
    * 如果 `timeout` 是个正数，将最多阻塞 `timeout` 秒，如果在这段时间内项目不能得到，将引发 `Empty` 异常。
  * 反之 (`block = false`) , 如果一个项目立即可得到，则返回一个项目
    * 否则引发 `Empty`异常 (这种情况下，*timeout* 将被忽略)。
  * `POSIX`系统3.0之前，以及所有版本的Windows系统中，如果 `block = true `并且 `timeout = None` ， 这个操作将进入基础锁的不间断等待。这意味着，没有异常能发生，尤其是 `SIGINT `将不会触发 `KeyboardInterrupt`异常。

* `Queue.get_nowait()`

  相当于 `get(False)` 

* `Queue.task_done()`

  表示前面排队的任务已经被完成。被队列的消费者线程使用。

  * 每个`get()`被用于获取一个任务， 后续调用 `task_done()` 告诉队列，该任务的处理已经完成。

  * 如果 `join()`当前正在阻塞，在所有条目都被处理后，将解除阻塞(意味着每个 `put()` 进队列的条目的 `task_done()` 都被收到)。

  * 如果被调用的次数多于放入队列中的项目数量，将引发 `ValueError` 异常 。

* `Queue.join()`

  阻塞至队列中所有的元素都被接收和处理完毕。

  * 当条目添加到队列的时候，未完成任务的计数就会增加。每当消费者线程调用 `task_done()`表示这个条目已经被回收，该条目所有工作已经完成，未完成计数就会减少。当未完成计数降到零的时候，`join()` 阻塞被解除。

## 三、 `SimpleQueue`对象的方法

- `SimpleQueue.qsize()`

  返回队列的大致大小。注意，`qsize() `> 0 不保证后续的 get() 不被阻塞。

- `SimpleQueue.empty()`

  如果队列为空，返回 `True` ，否则返回 `False` 。

  * 如果 empty() 返回 `False` ，不保证后续调用的 get() 不被阻塞。

- `SimpleQueue.put(item, block=True, timeout=None)`

  将 *item* 放入队列。此方法永不阻塞，始终成功（除了潜在的低级错误，例如内存分配失败）。

  * 可选参数 *block* 和 *timeout* 仅仅是为了保持 `Queue.put()`的兼容性而提供，其值被忽略。
  * `CPython`实现细节:这个方法有一个可重入的C实现。也就是说，一个put()或get()调用可以被同一线程中的另一个put()调用中断，而不会死锁或破坏队列中的内部状态。这使得它适合于在析构函数中使用，如:`__del__`方法或`weakref`回调函数。

- `SimpleQueue.put_nowait(item)`

  相当于 `put(item)` ，仅为保持 `Queue.put_nowait()`兼容性而提供。

- `SimpleQueue.get(block=True, timeout=None)`

  从队列中移除并返回一个项目。

  * 如果可选参数 `block = true` 并且 `timeout = None` (默认值)，则在必要时阻塞至项目可得到。
    * 如果 `timeout` 是个正数，将最多阻塞 `timeout` 秒，如果在这段时间内项目不能得到，将引发 `Empty` 异常。
  * 反之 (`block = false`) , 如果一个项目立即可得到，则返回一个项目，否则引发 `Empty` 异常 (这种情况下，`timeout` 将被忽略)。

- `SimpleQueue.get_nowait()`

  相当于 `get(False)` 。





