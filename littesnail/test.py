# -*- coding: utf-8 -*-

if False:
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

if True:

	lines = []
	title = ""
	url = None
	lc = 0
	baidu_dict = {}
	for line in open("../data/baike_simplified.txt"):
		try:
			lc += 1
			if lc % 1000 == 0:
				print 'baike', lc
			line = line.strip()
			if len(line) == 0:
				continue
			if line.startswith("<doc url="):
				lines = []
				pos_l = line.find("\"") + 1
				pos_r = line.find("\"", pos_l)
				url = line[pos_l:pos_r]
			elif line.startswith("</doc>"):
				baidu_dict[title] = url
			else:
				if len(line) == 0:
					continue
				if len(lines) == 0:
					title = line
				lines.append(line)
		except:
			print line
			pass


	lines = []
	title = ""
	url = None
	lc = 0
	fout = open("../data/mix_simplified.txt", "w")
	for line in open("../data/wiki-simplified.txt"):
		try:
			lc += 1
			if lc % 1000 == 0:
				print 'wiki', lc
			line = line.strip()
			if len(line) == 0:
				continue
			if line.startswith("<doc "):
				lines = []
			elif line.startswith("</doc>"):
				content = '\n'.join(lines)
				pos = content.find("。")
				if pos == -1:
					content = title
				else:
					if title in baidu_dict:
						url = baidu_dict[title]
						content = content[0:pos].strip()
						fout.write("<doc url=\"%s\">\n"%url)
						fout.write(content + "\n")
						fout.write("</doc>\n")

			else:
				if len(line) == 0:
					continue
				if len(lines) == 0:
					title = line
				lines.append(line)
		except:
			print line
			pass

	fout.flush()
	fout.close()