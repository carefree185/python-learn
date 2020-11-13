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

# `Event`事件

# 线程`Q`
