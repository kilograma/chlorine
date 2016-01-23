# -*- coding: utf-8 -*-

from index_wiki import search_index
from django.utils import timezone
from models import *

def need_wiki_result(queryLine):
	return True


def get_wiki_result(queryLine, user_id, msg_id):# in unicode!
	rtStr = ""
	query_date = timezone.now()
	original_query = queryLine
	return ""
	if queryLine.startswith(u"维基编号 "):
		iid = queryLine[len(u"维基编号 "):]
		results = search_index(queryLine=iid, query_field="iid", N=1)
		if len(results) == 0:
			rtStr = "竟然没有找到和维基百科编号%s相关的条目...真的不是输错数字了吗?"%iid
		else:
			rtStr = "关于%s，维基百科链接：https://zh.wikipedia.org/wiki?curid=%s。我们为您匹配的正文如下:\n%s\n"%(results[0]["title_show"], results[0]["iid"] ,results[0]["content_show"])
	else:
		results_title = search_index(queryLine=queryLine, query_field="title", N=10)
		id_set = set()
		if len(results_title) == 0:
			rtStr = "竟然没有找到和包含%s的维基条目...要不要换个词试试?"%(queryLine.encode("UTF-8"))
		else:
			rtStr = "您是不是在找下面的条目:\n"
			for iid, title, content in results_title:
				rtStr += "%s(回复\"维基编号 %s\"查看详情)\n"
				id_set.add(iid)

		results_title = search_index(queryLine=queryLine, query_field="content", N=20)
		if len(results_title) == 0:
			rtStr = rtStr # do nothing
		else:
			rtStr += "还有一些相关条目也可以考虑:\n"
			cnt = 0
			for iid, title, content in results_title:
				if iid in id_set:
					continue
				rtStr += "%s(回复\"维基编号 %s\"查看详情)\n"
				id_set.add(iid)
				cnt += 1
				if cnt == 5:
					break

	query_result_date = timezone.now()

	uq = UserQuery(user_id=user_id, query_str=original_query, query_date=query_date, query_result_date=query_result_date, query_msg_id=msg_id, query_result=rtStr)
	uq.save()
	return rtStr