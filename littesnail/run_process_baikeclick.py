# -*- coding: utf-8 -*-
import fetcher
from django.utils.html import strip_tags
import re


def clean(content, encoding):
	content = re.sub("<[\\s]*?style[^>]*?>[\\s\\S]*?<[\\s]*?\\/[\\s]*?style[\\s]*?>", "", content.lower())
	content = re.sub("<script[^>]*?>[\\s\\S]*?<\\/script>", "", content.lower())
	# content = strip_tags(content.decode(encoding)).encode(encoding).strip()
	# while "  " in content:
	# 	content = content.replace("  ", " ").strip()
	# while "\n\n" in content:
	# 	content = content.replace("\n\n", "\n").strip()
	return content


if True:
	prev_url = None
	fout = open("../data/url_down.txt", "w")
	cnt = 0
	for line in open("/Users/sg/Desktop/dataset/baidu_click/baike_sorted.txt"):
		line = line.strip()
		if len(line) == 0:
			continue
		url, keyword, title = line.split("\t")
		url = url.replace("http://-www", "http://www")
		if url != prev_url:
			prev_url = url
			content, dom, encoding = fetcher.get_contents(url)
			if content == None or dom == None:
				continue
			urls = fetcher.get_urls(url, dom)
			fmid = open("../data/down/%d.txt"%cnt, "w")
			fmid.write(clean(content, encoding))
			fmid.flush()
			fmid.close()
			cnt += 1
			fout.write(url + "\t1\n")
			for u in urls:
				fout.write(u + "\t0\n")
			fout.flush()
		else:
			continue
		if cnt > 10:
			break