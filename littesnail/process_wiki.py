# -*- coding: utf-8 -*-

from index_wiki import search_index
from django.utils import timezone
from models import *

from utils import get_split, word_seg_for_search, word_seg_for_index

def need_wiki_result(queryLine):
	return True

def get_wiki_result(queryLine, user_id, msg_id):# in UTF-8!
	rtStr = ""
	query_date = timezone.now()
	original_query = queryLine
	if queryLine.startswith("百度百科 "):
		queryLine = queryLine[len("百度百科 "):]
	queryLine_back = queryLine
	queryLine = word_seg_for_search(queryLine)
	results_title = search_index(queryLine=queryLine.decode('UTF-8'), query_field="title", N=3)
	id_set = set()
	if len(results_title) == 0:
		rtStr = "竟然没有找到包含%s的百度百科条目...要不要换个词试试?"%queryLine_back
	else:
		rtStr = "您是不是在找下列条目(点击查看):\n\n"
		for url, title, content in results_title:
			excerpt = content.decode('UTF-8')[0:60].encode('UTF-8').replace('\n', " ")
			blank_pos = excerpt.find(" ")
			if blank_pos != -1:
				excerpt = excerpt[blank_pos+1:]
			rtStr += "<a href=\"%s\">%s</a>。%s...\n\n"%(url.strip(), title.strip(), excerpt.strip())
			id_set.add(url)		

	results_title = search_index(queryLine=queryLine, query_field="content", N=20)
	if len(results_title) == 0:
		rtStr = rtStr # do nothing
	else:
		rtStr += "===\n其他人试过回复:\n"
		cnt = 0
		for url, title, _ in results_title:
			if url in id_set:
				continue
			rtStr += "%s\n"%(title.strip())
			id_set.add(url)
			cnt += 1
			if cnt == 10:
				break

	query_result_date = timezone.now()

	uq = UserQuery(user_id=user_id, query_str=original_query, query_date=query_date, query_result_date=query_result_date, query_msg_id=msg_id, query_result=rtStr)
	uq.save()
	return rtStr