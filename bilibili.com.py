# -*- coding: utf-8 -*-

import requests
import json


def get_video(title, aid, cid):
    url = "https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn=32".format(aid, cid)

    content = requests.get(url).content

    data = json.loads(content)
    durl = data.get("data").get("durl")

    v_headers = {
        "Accept": "*/*",
        "Origin": "https://www.bilibili.com",
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",

    }

    for v in durl:
        v_url = v.get("url")
        v_content = requests.get(v_url, headers=v_headers).content

        with open("{}.flv".format(title), "wb") as f:
            f.write(v_content)


def get_list(url):
    content = requests.get(url).text

    data = json.loads(content)

    v_list = data.get("result")

    for v in v_list:
        title = v.get("title")
        play = v.get("play")  # 播放量
        video_review = v.get("video_review")  # 弹幕数
        pubdate = v.get("pubdate")  # 发布时间
        author = v.get("author")  # 作者
        v_link = v.get("arcurl")  # 链接
        aid = v.get("id")
        cid = get_cid(aid)
        get_video(title, aid, cid)
        break


def get_cid(aid):
    url = "https://api.bilibili.com/x/player/pagelist?aid={}".format(aid)
    content = json.loads(requests.get(url).content)
    data = content.get("data")
    for d in data:
        cid = d.get("cid")
        return cid


if __name__ == '__main__':
    link = "https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=39&page=2&pagesize=20&jsonp=jsonp&time_from=20200420&time_to=20200427&_=1587959170028"
    get_list(link)
