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

def help_info():
	usage_str = u"关于主页菌，需要使用下列方法调戏:\n"
	usage_str += u"  回复『旅游+空格+关键词』，获得该地旅游信息，例如『旅游 韩国』、『旅游 天安门』\n"
	usage_str += u"  回复『文艺+空格+关键词』，获得该书籍、电影等的评价，例如『文艺 红楼梦』、『文艺 一步之遥』\n"
	usage_str += u"  回复『百科+空格+关键词』，获得该词条的百科信息，例如『百科 计算机』\n"
	usage_str += u"  回复『美食+空格+关键词』，获得该美食详情，例如『美食 鱼香肉丝』\n"
	usage_str += u"  回复『任何没有汉字的东西』，我们帮你翻译\n"
	return usage_str

if False:
	print word_seg_for_index(u"我爱，你74.abc我")
