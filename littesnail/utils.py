# -*- coding: utf-8 -*-
import re
import jieba

def has_chinese(line):
	p = re.compile(ur'[\u4e00-\u9fa5]+')
	l = p.findall(line.decode('UTF-8'))
	if l == None or len(l) == 0:
		return False
	return True

def get_split(line):
	p = re.compile(ur'([\u4e00-\u9fa5a-zA-Z0-9]+)')
	l = p.findall(line.decode('UTF-8'))
	rt = []
	if l:
		for w in l:
			rt.append(w.encode('UTF-8'))
	return rt

def word_seg_for_index(line):
	s = ' '.join(jieba.cut_for_search(line.decode('UTF-8')))
	#s = ' '.join(line.decode('UTF-8'))
	return s.encode("UTF-8").strip()

def word_seg_for_search(line):
	s = ' '.join(jieba.cut(line.decode('UTF-8'), cut_all=False))
	#s = ' '.join(line.decode('UTF-8'))
	return s.encode('UTF-8').strip()

def uni_len(line):
	return len(line.decode("UTF-8"))

if False:
	print word_seg_for_index("我爱，你74.abc我")
