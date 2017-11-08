# bilibili-album

## Bilibili相册爬虫

## 声明
> 本项目所有图片内容均由 *bilibili* 提供, 获取与共享之行为或有侵犯 *bilibili* 权益的嫌疑, 若被告知需停止共享与使用, 本人会及时删除整个项目. 请您了解相关情况, 并遵守 *bilibili* 协议。

## 截图
以 [浅野菌子](http://link.bilibili.com/p/world/index#/8581342/world/) 相册为例
![screenshot](https://i.loli.net/2017/11/08/5a02eec274479.png "浅野菌子")

## API分析
完整的 url 为 `http://api.vc.bilibili.com/link_draw/v1/doc/ones?poster_uid={uid}&page_size=20&next_offset={next_offset}&noFav=1&noLike=1&platform=pc` 

但实际上仅仅 `http://api.vc.bilibili.com/link_draw/v1/doc/ones?poster_uid={uid}&page_size=20&next_offset={next_offset}` 就可以了

- uid
即用户 id
- next_offset
初始为0, 之后的 next_offset 在返回的 Json 的 data 中给出了
- has_more
data 中还有一个 has_more 变量, 表示之后还有没有更多图片, 0表示已完

## 使用说明
### 注: 默认的下载函数是将所有链接打印出来, 若是要直接下载请删除对应注释
```
>> git clone https://github.com/LewisTian/bilibili-album.git
>> cd bilibili-album
>> pip install -r requirements.txt
>> subl up.txt
# 将要爬取的 up 的 uid 都记录在上述 up.txt 中
>> python album.py

```