# import time
#
#
# import asyncio


# def callback(task):
#     print("i am callback")
#     print(task.result())

#
#
# async def test():
#     print("i am async test")
#     return "hhh"
#
#
# c = test()  # 创建协程对象
#
# task = asyncio.ensure_future(c)  # 将协程对象封装为任务对象
# task.add_done_callback(callback)  # 绑定回调函数
# loop = asyncio.get_event_loop()  # 创建时间循环
# loop.run_until_complete(task)


# 多任务

# def callback(task):
#     print("i am callback")
#     print(task.result())
#
#
# start = time.time()
#
#
# async def get_request(url):
#     print('当前下载任务: %s' % url)
#     await asyncio.sleep(2)
#     print('当前下载任务: %s 下载成功' % url)
#     return "hhh"
#
#
# urls = ["www.1.com", 'www.2.com', "www.3.com"]
#
# tasks = []
# for i in urls:
#     c = get_request(i)
#     task = asyncio.ensure_future(c)
#     task.add_done_callback(callback)  # 绑定回调函数，用于处理数据
#     tasks.append(task)
#
# loop = asyncio.get_event_loop()
#
# # 注意挂起操作需要手动挂起
# loop.run_until_complete(asyncio.wait(tasks))
#
# print(time.time() - start)

import requests
import aiohttp
import time
import asyncio


urls = [
    "http://127.0.0.1:5000/index",
    "http://127.0.0.1:5000/index1"
]

start = time.time()


def callback(task):
    print(task.result())


# async def get_request(url):
#     response = requests.get(url)
#     return response.text

async def get_request(url):
    async with aiohttp.ClientSession() as s:
        async with await s.get(url=url) as response:
            page = await response.text()

    return page

task_list = []
for i in urls:
    c = get_request(i)
    task = asyncio.ensure_future(c)
    task.add_done_callback(callback)
    task_list.append(task)

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait(task_list))

print(time.time() - start)
