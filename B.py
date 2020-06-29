# -*- coding: utf-8 -*-

import requests
import json
import re


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


def get_info(url):
    content = requests.get(url).text
    # print(content)
    cid, aid = re.findall("cid=(.*?)&aid=(\d+)&", content)[0]
    title = re.findall('h1 title="(.*?)" class="video-title"', content)[0]
    print(title, aid, cid)
    get_video(title.replace(":", ""), aid, cid)


def get_cid(aid):
    url = "https://api.bilibili.com/x/player/pagelist?aid={}".format(aid)
    content = json.loads(requests.get(url).content)
    data = content.get("data")
    for d in data:
        cid = d.get("cid")
        return cid


if __name__ == '__main__':
    link = input("输入需要下载的B站视频链接:").replace(" ", "")
    # link = "https://www.bilibili.com/video/BV1RK411V7pu"
    get_info(link)
