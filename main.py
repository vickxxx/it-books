#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description: 爬取http://www.allitebooks.org 数据
author: Vick
ctime: 2019-06-21 15:49:49
"""
import csv
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


def fetch_detail():
    fd = open("books.csv", "w")
    fieldnames = ["Name", "Year", "Author", "ISBN-10", "Pages",
                  "Language", "File size", "File format", "Category",
                  "Links"]
    w = csv.DictWriter(fd, fieldnames=fieldnames)
    w.writeheader()

    line_no = 1
    for link in open("book_detail.txt"):
        print(line_no, "#  ", link)
        ret = s.get(link)
        # print(ret.text)
        if ret.status_code == 200:
            detail_bs = BeautifulSoup(ret.text, features="lxml")
            print(detail_bs.title)
            
            dl_bs = detail_bs.find("dl")
            dd_lst = dl_bs.find_all("dd")
            dt_lst = dl_bs.find_all("dt")
            book_info = {}
            book_name = detail_bs.find(class_="single-title").string
            book_info["Name"] = book_name
            for dd, dt in zip(dd_lst, dt_lst):
                # print(dt.string.strip(":"), "\t", dd.string or dd.a.string.strip())
                book_info[dt.string.strip(":")] = (dd.string or dd.a.string).strip()
            dl_link = detail_bs.find_all(class_="download-links")
            # print([i.a["href"] for i in dl_link])
            book_info["Links"] = " , ".join([i.a["href"] for i in dl_link])
            w.writerow(book_info)
            line_no += 1
            fd.flush()
            # print(book_name)
        else:
            print("error~~~~~~~~~~~", link)
    fd.close()


if __name__ == "__main__":
    # fetch_home()
    fetch_detail()