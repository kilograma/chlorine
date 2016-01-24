# -*- coding: utf-8 -*-

from index_travel import search_index
from django.utils import timezone
from models import *

from utils import get_split, word_seg_for_search, word_seg_for_index

def need_travel_result(queryLine):
	if queryLine.startswith("旅游 "):
		return True
	return False

def get_travel_result(queryLine, user_id, msg_id):# in UTF-8!
	rtStr = ""
	query_date = timezone.now()
	original_query = queryLine
	if queryLine.startswith("旅游 "):
		queryLine = queryLine[len("旅游 "):]
	queryLine_back = queryLine
	queryLine = word_seg_for_search(queryLine)
	results_title = search_index(queryLine=queryLine.decode('UTF-8'), N=13)
	id_set = set()
	if len(results_title) == 0:
		rtStr = "竟然没有找到包含%s的旅游信息...要不要换个词试试?"%queryLine_back
	else:
		rtStr = "看看这些:\n====\n"
		for url, title in results_title:
			rtStr += "<a href=\"%s\">%s</a>\n\n"%(url.strip(), title.strip())
			id_set.add(url)		

	query_result_date = timezone.now()

	uq = UserQuery(user_id=user_id, query_str=original_query, query_date=query_date, query_result_date=query_result_date, query_msg_id=msg_id, query_result=rtStr)
	uq.save()
	return rtStr