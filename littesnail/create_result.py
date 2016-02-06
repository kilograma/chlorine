# -*- coding: utf-8 -*-
import re
from result_wiki import ResultWiki
from result_youdao import ResultYoudao
from result_travel import ResultTravel
from result_food import ResultFood

def createResult(queryStr):
	if queryStr.startswith("旅游 "):
		return ResultTravel(queryStr)
	if queryStr.startswith("百科 "):
		return ResultWiki(queryStr)
	if queryStr.startswith("美食 "):
		return ResultFood(queryStr)
	return ResultYoudao(queryStr)