# -*- coding: utf-8 -*-
import re
import jieba

def has_chinese(line):
	p = re.compile(ur'[\u4e00-\u9fa5]+')
	l = p.findall(line)
	if l == None or len(l) == 0:
		return False
	return True

def get_split(line):
	p = re.compile(ur'([\u4e00-\u9fa5a-zA-Z0-9]+)')
	l = p.findall(line)
	rt = []
	if l:
		for w in l:
			rt.append(w)
	return rt

def word_seg_for_index(line):
	s = ' '.join(jieba.cut_for_search(line))
	#s = ' '.join(line.decode('UTF-8'))
	return s.strip()

def word_seg_for_search(line):
	s = ' '.join(jieba.cut(line, cut_all=False))
	#s = ' '.join(line.decode('UTF-8'))
	return s.strip()

def uni_len(line):
	return len(line)

if False:
	print word_seg_for_index(u"我爱，你74.abc我")
