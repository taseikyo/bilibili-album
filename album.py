#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 18:34:07
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

import threading
from collections import namedtuple
from concurrent import futures
import time
import csv
from pprint import pprint
import requests

# http://h.bilibili.com/{doc_id}
header = ['up', 'doc_id', 'view_count', 'like_count', 'title', 'upload_timestamp', 'collect_count']                             
Album = namedtuple('Album', header)
headers = {
    'Host':'api.vc.bilibili.com',
    'Origin':'http://h.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}

total = 0
result = []
lock = threading.Lock()

def run(url):
    global total
    r = requests.get(url, headers = headers, timeout = 6).json()
    if r['code'] == 0:
        time.sleep(1)     # 延迟
        data = r['data']['item']
        up = r['data']['user']
        album = Album(
            up['uid'],                  # up主uid
            data['doc_id'],             # id
            data['view_count'],         # 浏览次数
            data['like_count'],         # 点赞
            data['title'],              # 标题
            data['upload_timestamp'],   # 上传时间
            data['collect_count']       # 收藏数
        )
        with lock:
            result.append(album)
            total += 1
            print(total)
    else:
        sleep(0.5)

def save():
    with open('result.csv', 'w+', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(result)


if __name__ == '__main__':
    urls = ['http://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id={}'.format(i)
            for i in range(100000000)]
    with futures.ThreadPoolExecutor(32) as executor:
        executor.map(run, urls)
    save()