# -*- coding: utf-8 -*-
from django.http import HttpResponse
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh import scoring
import jieba
import os

def test(request):
	return HttpResponse("Test ok!")
	from process_wiki import get_wiki_result
	if True:
		from whoosh.qparser import QueryParser
		print os.getcwd()
		ix = open_dir("index/wiki_index")
		with ix.searcher() as searcher:
			qstr = "中华共和国"
			rstr = get_wiki_result(qstr, "-1", "-1")
			print rstr
			print "=============="
			qstr = ' '.join(jieba.cut("中华共和国", cut_all=False))
			query = QueryParser("title", ix.schema).parse(qstr)
			results = searcher.search(query)
			for r in results:
			 	print r['title_show'].encode('UTF-8')
	return HttpResponse("Done")

