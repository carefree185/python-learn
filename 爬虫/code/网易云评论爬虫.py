import binascii
import json
import re

import aiohttp
import math
import random
import base64
import asyncio
from datetime import datetime
from urllib import parse
from Cryptodome.Cipher import AES

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    # 'Postman-Token':'4cbfd1e6-63bf-4136-a041-e2678695b419',
    "origin": 'https://music.163.com',
    # 'referer':'https://music.163.com/song?id=1372035522',
    # 'accept-encoding':'gzip,deflate,br',
    'Accept': '*/*',
    'Host': 'music.163.com',
    'content-lenth': '472',
    'Cache-Control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    # 'Cookie':'iuqxldmzr_=32; _ntes_nnid=a6f29f40998c88c693bc910331bd6bea,1558011234325; _ntes_nuid=a6f29f40998c88c693bc910331bd6bea; _ga=GA1.2.2120707788.1559308501; WM_TID=pV2C%2BjTrRwBBAAERUVJojniTwk8%2B8Zta; JSESSIONID-WYYY=nvf%2BggodQRfcT%2BTvBRmANqMrsDeQCxRvqwFsxDr3eJvNNWhGYFhfCXKFkfAfOdbHhpCsMzT39mAeJ7ZamBQZbiwwtnSZD%5CPWRqKxD9t6dGKD3bTVjomjgB39DB07RNIWI32bYKa2H4fg1qQgqI%2FR%2B%2Br%2BZXJvgFg1Vh%2FA2XRj9S4p0EMu%3A1560927288799; WM_NI=DthwcEQf5Ew2NbTIZmSNhSnm%2F8VWsg5RxhkYogvs2luEwZ6m5UhdzbHYPIr654ZBWKV4o22%2BEwb9BvdLS%2BFOmOAEUG%2B8xd8az4CX%2FiAL%2BZkz3syA0onCPkhQwCtL4pkUcjg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed2d650989c9cd1dc4bb6b88eb2c84e979f9aaff773afb6fb83d950bcb19ecce92af0fea7c3b92a88aca898e24f93bafba6f63a8ebe9caad9679192a8b4ed67ede89ab8f26df78eb889ea53adb9ba94b168b79bb9bbb567f78ba885f96a8c87a0aaf13ef7ec96a3d64196eca1d3b12187a9aedac17ea8949dccc545af918fa6d84de9e8b885bb6bbaec8db9ae638394e5bbea72f1adb7a2b365ae9da08ceb5bb59dbcadb77ca98bad8be637e2a3'
}


def random_key(num=16):
    rand_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    c = ""
    assert num % 16 == 0, ValueError('num must be divided by 16')
    i = 0
    while num > i:
        i += 1
        e = random.random() * len(rand_string)
        e = math.floor(e)
        c += rand_string[e]

    return c


def file_explanation(text):
    """
    最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
    :param text: 待处理的明文
    :return: 拼接好的明文
    """

    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(text.encode('utf-8'))
    # utf-8 编码时，英文占1个byte，而中文占3个byte
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    padding_text = chr(padding) * padding
    return text + padding_text


def aes_encrypt(content: str, key: str):
    """
    aes，cbc模式加密
    :param content: 待加密的字符串
    :param key: 加密使用的key
    :return: 返回加密的密文
    """
    key_bytes = key.encode('utf-8')
    iv = '0102030405060708'.encode('utf-8')

    ipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    content = file_explanation(content)  # 将明文拼接
    encrypt_content = ipher.encrypt(content.encode('utf-8'))
    return str(base64.b64encode(encrypt_content), encoding='utf-8')


def rsa_encrypt(message, rsa_n, rsa_e):
    """
    rsa加密随机生成的aes_key值，加密方式时将随机aes_key转为十六进制的数字m，对m进行rsa_e的次方后取与rsa_n的余数，转为16进制后，使用0填充至256
    :param message: random_key(16), 函数生成的值
    :param rsa_n: 网页分析获得：00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
    :param rsa_e: 网页分析获得：010001
    :return:
    """
    # 将网页提取到的n值和e值转为16精制数
    rsa_n = int(rsa_n, 16)
    rsa_e = int(rsa_e, 16)

    message = message[::-1]
    rs = pow(int(binascii.hexlify(message.encode('utf-8')), 16), rsa_e, rsa_n)
    return format(rs, 'x').zfill(256)


def get_form_data(song_id, page_num, page_size):
    """
    获取请求需要发送的参数
    :param song_id: 歌曲id
    :param page_num: 评论页数
    :return:
    """
    params = {"rid": "R_SO_4_%s" % song_id,
              "threadId": "R_SO_4_%s" % song_id,
              "pageNo": str(page_num),
              "pageSize": "200",
              # "cursor": "1586861856136",
              "offset": f"{(page_num - 1) * 20}",
              "orderType": "2",
              "csrf_token": ""
              }

    params = json.dumps(params)
    form_data = {
        "params": "",
        "encSecKey": ""
    }
    i = random_key()
    # 第一次加密 aes_key: 0CoJUm6Qyw8W8jud
    aes_key = "0CoJUm6Qyw8W8jud"
    params = aes_encrypt(params, aes_key)
    # 第二次加密的aes_key: "RdNyba5FKnpxqvtq"
    aes_key = i
    params = aes_encrypt(params, aes_key)
    # 加密第二次aes_key，
    rsa_n = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    rsa_e = "010001"
    encSecKey = rsa_encrypt(i, rsa_n, rsa_e)
    form_data["params"] = params
    form_data["encSecKey"] = encSecKey
    print(form_data)
    form_data = parse.urlencode(form_data)
    return form_data


async def response(form_data):
    """
    发送请求，获取评论数据
    :param form_data:
    :return:
    """
    url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    async with aiohttp.ClientSession() as s:
        async with await s.post(url=url, data=form_data, headers=header) as response:
            if response.status == 200:
                json_object = await response.text()
                return json_object
            else:
                return None


def callback(task):
    """
    回调函数，处理返回数据
    :param task:
    :return:
    """
    print(task)
    text = task.result()
    ex = r'"commentId":\d+,"content":"(.*?)"'
    comments = re.findall(ex, text)
    print(comments)


def get_tasks(songid, total_page, page_size):
    """
    获取歌曲id，生成任务对象
    :param songid:
    :return: 任务对象列表
    """
    task_list = []
    for page_no in range(1, total_page + 1):
        formdata = get_form_data(songid, total_page, page_size)
        c = response(formdata)
        task = asyncio.ensure_future(c)
        task.add_done_callback(callback)
        task_list.append(task)
    return task_list


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(get_tasks('27646687', 3, 20)))
