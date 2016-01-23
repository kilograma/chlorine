# -*- coding: utf-8 -*-
"""
Created on Tue Spt  15 15:27:31 2014

@author: kilograma
"""
import os
import sys
import urllib2,urllib  
import bs4
import HTMLParser  
import urlparse  
import cookielib  
import string  
import re  
import zlib
import time

import traceback


def get_encoding(content):
    utf8_pos = content.find("utf-8")
    gb2312_pos = content.find("gb2312")
    gbk_pos = content.find("gbk")
    if utf8_pos == -1:
        utf8_pos = sys.maxint
    if gb2312_pos == -1:
        gb2312_pos = sys.maxint
    if gbk_pos == -1:
        gbk_pos = sys.maxint

    if utf8_pos < gb2312_pos and utf8_pos < gbk_pos:
        return "UTF-8"
    if gb2312_pos < utf8_pos and gb2312_pos < gbk_pos:
        return "GB2312"
    return "GBK"



def get_contents(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
    try:
        req = urllib2.Request(url,headers=headers)
        content = urllib2.urlopen(req).read()
        encoding = get_encoding(content.lower())
        #print encoding
        #if not "charset=\"utf-8\"" in content and not "charset=utf-8" in content:
        #    encoding = "GB2312"
        dom = bs4.BeautifulSoup(content,from_encoding=encoding)
        return content, dom, encoding
    except:
        return None, None, None
	

def get_urls(url, dom):
	#寻找url_prefix
    url_prefix = url
    slim_pos = url.find('/', 9)
    if slim_pos != -1:
        url_prefix = url[:slim_pos]
    #继续广搜其他url
    all_a = dom.find_all(name='a')
    urls = set()
    for a in all_a:
        if not 'href' in a.attrs:
            continue
        href = a['href']
        if href.startswith('/'):
            href = url_prefix + href

        url_ok = True  #判断url前缀是否符合要求
        # TO BE ADDED
        if not url_ok:
            continue
        urls.add(url)
    return urls
  
    