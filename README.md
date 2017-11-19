# B 站绘画区爬虫

## 声明
> 本项目所有图片内容均由 *bilibili* 提供, 获取与共享之行为或有侵犯 *bilibili* 权益的嫌疑, 若被告知需停止共享与使用, 本人会及时删除整个项目. 请您了解相关情况, 并遵守 *bilibili* 协议。

此项目共包括了两个工作
- 爬取了全站的绘画信息
- 根据 up 主 uid 爬取其相簿的图片

## 1. 爬取全站绘画区信息
共得到 条数据
### 爬取过程
进入 B 站 [绘画区](http://h.bilibili.com/d) , 随便找一个图, 点进去, 打开开发者工具
![album-1](https://github.com/LewisTian/bilibili-album/blob/master/images/album-1.png)
选择 XHR 可以看到 api 的地址
`http://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id={doc_id}`
然后就很简单了, 构造请求 url , 用 requests 请求获取数据, 在此为了提高效率, 使用了多线程
#### 核心代码
```
total = 0
result = []
lock = threading.Lock()
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
            data['collect_count'],       # 收藏数
            data['upload_timestamp']   # 上传时间
        )
        with lock:
            result.append(album)
            total += 1
            print(total)
    else:
        sleep(0.5)
```
#### 多线程
```
urls = ['http://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id={}'.format(i)
            for i in range(1000, 1000000)]
    with futures.ThreadPoolExecutor(32) as executor:
        executor.map(run, urls)
``` 
### 分析


## 2. 根据 up 主 uid 爬取相簿图片
### 截图
以 [浅野菌子](http://link.bilibili.com/p/world/index#/8581342/world/) 相册为例
![screenshot](https://i.loli.net/2017/11/08/5a02eec274479.png "浅野菌子")

### API分析
步骤同上, 点进一个 up 的相簿空间, 例如 [我的](http://link.bilibili.com/p/world/index#/9272615/world/) , 按 f12 打开开发者工具, 勾选 XHR , 刷新就可以得到 API 链接, 完整的 url 为 `http://api.vc.bilibili.com/link_draw/v1/doc/ones?poster_uid={uid}&page_size=20&next_offset={next_offset}&noFav=1&noLike=1&platform=pc` 

但实际上仅仅 `http://api.vc.bilibili.com/link_draw/v1/doc/ones?poster_uid={uid}&page_size=20&next_offset={next_offset}` 就可以了

- uid
即用户 id
- next_offset
初始为 0, 之后的 next_offset 在返回的 Json 的 data 中给出了
- has_more
1 表示之后还有没有更多图片, 0 表示已完

因此, 设置初始的 next_offset 为 0, 然后 while 死循环, 条件为 has_more, 初始设为 1, 之后根据得到的 json 数据更新 next_offset 和 has_more 即可.

### 核心代码
```
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
```

## 使用说明
### 注: 默认的下载函数是将所有链接打印出来, 若是要直接下载请删除对应注释
```
>> git clone https://github.com/LewisTian/bilibili-album.git
>> cd bilibili-album
>> pip install -r requirements.txt
# 第一个
>> python album.py
# 第二个
>> subl up.txt # 将要爬取的 up 的 uid 都记录在 up.txt 中
>> python album_up.py

```
