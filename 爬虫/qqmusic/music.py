import math
import requests
# from music_db import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 创建请求头和会话
headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
           }
session = requests.session()


# 下载歌曲
def download(songmid):
    filename = 'C400' + songmid
    # 获取vkey
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?loginUin=0&hostUin=0' \
          '&cid=205361747&uin=0&songmid=%s&filename=%s.m4a&guid=0' % (songmid, filename)
    r = session.get(url, headers=headers)
    vkey = r.json()['data']['items'][0]['vkey']
    # 下载歌曲
    url = 'http://dl.stream.qqmusic.qq.com/%s.m4a?vkey=%s&guid=0&uin=0&fromtag=66' % (
        filename, vkey)
    r = session.get(url, headers=headers)
    f = open('song/' + songmid + '.m4a', 'wb')
    f.write(r.content)
    f.close()
    print("下载完成%s"%songmid)


# 获取歌手的全部歌曲
def get_singer_songs(singermid):
    # 获取歌手姓名和歌曲总数
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=0&hostUin=0&singermid=%s' \
          '&order=listen&begin=0&num=30&songstatus=1' % (singermid)
    r = session.get(url)
    # 获取歌手姓名
    song_singer = r.json()['data']['singer_name']
    # 获取歌曲总数
    songcount = r.json()['data']['total']
    # 根据歌曲总数计算总页数
    pagecount = math.ceil(int(songcount) / 30)
    # 循环页数，获取每一页歌曲信息
    for p in range(pagecount):
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=0&hostUin=0&singermid=%s' \
              '&order=listen&begin=%s&num=30&songstatus=1' % (singermid, p * 30)
        r = session.get(url)
        # 得到每页的歌曲信息
        music_data = r.json()['data']['list']
        # songname-歌名，ablum-专辑，interval-时长，songmid歌曲id，用于下载音频文件
        # 将歌曲信息存放字典song_dict，用于入库
        song_dict = {}
        for i in music_data:
            song_dict['song_name'] = i['musicData']['songname']
            song_dict['song_ablum'] = i['musicData']['albumname']
            song_dict['song_interval'] = i['musicData']['interval']
            song_dict['song_songmid'] = i['musicData']['songmid']
            song_dict['song_singer'] = song_singer
            # 下载歌曲
            download(song_dict['song_songmid'])
            # 入库处理，参数song_dict
            # insert_data(song_dict)
            # song_dict清空处理
            song_dict = {}


# 获取当前字母下全部歌手
def get_genre_singer(key, page_list):
    for p in page_list:
        url = 'https://c.y.qq.com/v8/fcg-bin/v8.fcg?channel=singer&page=list&key=all_all_%s' \
              '&pagesize=100&pagenum=%s&loginUin=0&hostUin=0&format=jsonp' % (key, p + 1)
        r = session.get(url)
        # 循环每一个歌手
        for k in r.json()['data']['list']:
            singermid = k['Fsinger_mid']
            get_singer_songs(singermid)


# 单进程单线程
# 获取全部歌手
def get_all_singer():
    # 获取字母A-Z全部歌手
    for i in range(65, 90):
        key = chr(i)
        # 获取每个字母分类下总歌手页数
        url = 'https://c.y.qq.com/v8/fcg-bin/v8.fcg?channel=singer&page=list&key=all_all_%s' \
              '&pagesize=100&pagenum=%s&loginUin=0&hostUin=0&format=jsonp' % (key, 1)
        r = session.get(url, headers=headers)
        pagenum = r.json()['data']['total_page']
        page_list = [x for x in range(pagenum)]
        # 获取当前字母下全部歌手
        get_genre_singer(key, page_list)


# 多线程
def myThread(genre):
    # 每个字母分类的歌手列表页数
    url = 'https://c.y.qq.com/v8/fcg-bin/v8.fcg?channel=singer&page=list&' \
          'key=all_all_%s&pagesize=100&pagenum=%s&loginUin=0&hostUin=0&format=jsonp' % (genre, 1)
    r = session.get(url, headers=headers)
    pagenum = r.json()['data']['total_page']
    page_list = [x for x in range(pagenum)]
    thread_number = 10
    # 将每个分类总页数平均分给线程数
    list_interval = math.ceil(len(page_list) / thread_number)
    # 设置线程对象
    Thread = ThreadPoolExecutor(max_workers=thread_number)
    for index in range(thread_number):
        # 计算每条线程应执行的页数
        start_num = list_interval * index
        if list_interval * (index + 1) <= len(page_list):
            end_num = list_interval * (index + 1)
        else:
            end_num = len(page_list)
        # 每个线程各自执行不同的歌手列表页数
        Thread.submit(get_genre_singer, genre, page_list[start_num: end_num])


# 多进程
def myProcess():
    with ProcessPoolExecutor(max_workers=26) as executor:
        for i in range(65, 90):
            # 创建26个进程，分别执行A-Z分类
            executor.submit(myThread, chr(i))


if __name__ == '__main__':
    # 执行多进程多线程
    myProcess()
    # 执行单进程单线程
    # get_all_singer()
