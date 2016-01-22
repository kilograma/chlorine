# -*- coding: utf-8 -*-
import re

def has_chinese(line):
	p = re.compile(ur'([\u4e00-\u9fa5]+)')
	l = p.findall(line.decode('UTF-8'))
	if l == None or len(l) == 0:
		return False
	return True