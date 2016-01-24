# -*- coding: utf-8 -*-

if True:
	fout = open("../data/mafengwo.pure.txt", "w")
	valid_url_prefix = set(["http://www.mafengwo.cn/jt/","http://www.mafengwo.cn/i/","http://www.mafengwo.cn/baike/","http://www.mafengwo.cn/crj/","http://www.mafengwo.cn/cy-i/", "http://www.mafengwo.cn/dt-i/", "http://www.mafengwo.cn/gonglve/", "http://www.mafengwo.cn/jd-i/", "http://www.mafengwo.cn/jt-i/", "http://www.mafengwo.cn/oad/"])
	invalid_url_prefix = set(["http://www.mafengwo.cn/jd/","http://www.mafengwo.cn/lines/","http://www.mafengwo.cn/path/","http://www.mafengwo.cn/photo/","http://www.mafengwo.cn/hotel/","http://www.mafengwo.cn/gw/","http://www.mafengwo.cn/cy/"])
	for line in open("../data/mafengwo.pennyjobshare.txt"):
		line = line.strip()
		ss = line.split("\t")
		if len(ss) != 2:
			continue
		url, title = ss
		b_vl = False
		for prefix in valid_url_prefix:
			if url.startswith(prefix):
				b_vl = True
				break
		b_iv = False
		for prefix in invalid_url_prefix:
			if url.startswith(prefix):
				b_iv = True
				break
		if not b_vl and not b_iv:
			print url, title
		if b_vl:
			fout.write("\t".join([url, title]) + "\n")
	fout.flush()
	fout.close()