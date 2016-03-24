# -*- coding: utf-8 -*-
import re
from result_wiki import ResultWiki
from result_youdao import ResultYoudao
from result_travel import ResultTravel
from result_food import ResultFood
from result_weibo import ResultWeibo
from result_shuji import ResultShuji
from utils import has_chinese

def createResult(queryStr):
	if queryStr.startswith(u"旅游 "):
		return ResultTravel(queryStr)
	if queryStr.startswith(u"百科 "):
		return ResultWiki(queryStr)
	if queryStr.startswith(u"美食 "):
		return ResultFood(queryStr)
	if queryStr.startswith(u"文艺 "):
		return ResultShuji(queryStr)
	if has_chinese(queryStr):
		return ResultWeibo(queryStr)
	#return ResultYoudao(queryStr)
	return None