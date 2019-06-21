#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description: 爬取http://www.allitebooks.org 数据
author: Vick
ctime: 2019-06-21 15:49:49
"""

import requests
from bs4 import BeautifulSoup

url = "http://www.allitebooks.org/page/{}/"

s = requests.Session()


def fetch_home():
    index = 1
    while True:
        ret = s.get(url.format(index))
        # print(ret.text)
        if ret.status_code == 200:
            home_bs = BeautifulSoup(ret.text, features="lxml")
            print(home_bs.title.text)
            article_bs = home_bs.find_all("article")
            # print(article_bs[0])
            # print(len(article_bs))
            with open("book_detail.txt", "a") as fd:
                for i in article_bs:
                    link = i.find("a")["href"]
                    fd.write(link)
                    print(index, "\t", link)
                    fd.write("\n")
            index += 1
        if ret.status_code == 404:
            break
        

if __name__ == "__main__":
    fetch_home()