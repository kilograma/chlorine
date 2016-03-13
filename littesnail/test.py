# -*- coding: utf-8 -*-

import sys
import os
import re

def get_only_chinese(line):
	p = re.compile(ur'([\u4e00-\u9fa5]+)')
	l = p.findall(line.decode('UTF-8'))
	s = ""
	if l:
		for w in l:
			s += w.encode('UTF-8').strip()
	return s

punc_set = set(['，', '。', '！', '？', '《'])

if True:
	junk_words = None
	if junk_words == None:
		junk_words = set()
		for l in open("clean_keywords.txt", "r"):
			if len(l.strip()) > 0:
				junk_words.add(l.strip())
	fout = open("data/weibo_new.txt", "w")
	lc = 0
	prev_bare_line = "";
	for line in open("/Volumes/Elements/apple/weibo_raw_sorted.txt"):
		line = line.strip();
		lc += 1
		if lc % 100000 == 0:
			print lc
			#if lc > 4000000:
			#	break
		line_bare = get_only_chinese(line)
		if len(line_bare) == 0 or prev_bare_line == line_bare:
			continue
		prev_bare_line = line_bare
		if line[0] != line_bare[0]:# not init with a chinese char
			continue 
		if len(line_bare.decode("UTF-8")) < 25:
			continue
		ok = False
		for punc in punc_set:
			if punc in line:
				ok = True
		if ok:
			for word in junk_words:
				if word in line:
					ok = False
					break
		if ok:
			fout.write(line + "\n")
	fout.flush()
	fout.close()