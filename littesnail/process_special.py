# -*- coding: utf-8 -*-

from process_youdao import get_youdao_result, need_youdao_result
from process_wiki import get_wiki_result, need_wiki_result
from process_travel import need_travel_result, get_travel_result

def need_special_result(queryStr):
	if queryStr.startswith("旅游 "):
		return True
	if queryStr.startswith("百度百科 "):
		return True
	return False

def get_special_result(queryStr, user_id, msg_id):
	if queryLine.startswith("旅游 "):
		return get_travel_result(queryLine=queryStr, user_id=user_id, msg_id=msg_id)
	if queryLine.startswith("百度百科 "):
		return get_wiki_result(queryLine=queryStr, user_id=user_id, msg_id=msg_id)
	return None