#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-07 23:33:30
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS
import re
import os
from time import sleep

class Album(requests.Session):
    def __init__(self):
        super(Album, self).__init__()
        self.api = 'http://api.vc.bilibili.com/link_draw/v1/doc/ones?poster_uid={uid}&page_size=20&next_offset={next_offset}'
        self.album = []

    def __del__(self):
        self.close()
    
    def update_uid(self, uid):
        self.uid = uid

    def run(self):
        has_more = 1
        next_offset = 0
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
            "Host":"api.vc.bilibili.com",
            "Origin":"http://link.bilibili.com",
            "Referer":"http://link.bilibili.com/p/center/index",
        })
        while has_more:
            url = self.api.format(uid = self.uid, next_offset = next_offset)
            r = self.get(url)
            data = r.json()['data']
            has_more = data['has_more']
            next_offset = data['next_offset']
            items = data['items']
            for x in items:
                upload_timestamp = x['upload_timestamp']
                pics = x['pictures']
                for i in pics:
                    self.album.append(i['img_src'])
        self.download(self.album)
    
    def download(self, pics):
        '''推荐打印所有链接然后使用迅雷下载'''
        for x in pics:
            print(x)
        '''
        self.headers.update({
            "Host":"i0.hdslb.com",
            "Referer":"http://link.bilibili.com/p/world/index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        })
        if not os.path.exists(self.uid):
            os.mkdir(self.uid)
        for x in pics:
            name = x.split('/')[-1]
            r = self.get(x)
            with open(self.uid + '/' + name, 'wb') as f:
                f.write(r.content)
            sleep(5)
        '''

if __name__ == '__main__':
    a = Album()
    with open('up.txt') as f:
        for up in f.readlines():
            a.update_uid(up)
            a.run()

