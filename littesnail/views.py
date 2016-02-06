# -*- coding: utf-8 -*-
from django.http import HttpResponse
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh import scoring
import jieba
import os

def test_wiki(request):
	from result_wiki import ResultWiki
	if True:
		from whoosh.qparser import QueryParser
		print os.getcwd()
		ix = open_dir("index/wiki_index")
		with ix.searcher() as searcher:
			qstr = "数学"
			r = ResultWiki(qstr)
			r.process()
			rstr = r.result_str
			print rstr
			print "=============="
			qstr = ' '.join(jieba.cut("数学", cut_all=False))
			query = QueryParser("title", ix.schema).parse(qstr)
			results = searcher.search(query)
			for r in results:
			 	print r['title_show'].encode('UTF-8')
	return HttpResponse("Done")

def test_travel(request):
	from result_travel import ResultTravel
	if True:
		from whoosh.qparser import QueryParser
		ix = open_dir("index/travel_index")
		with ix.searcher() as searcher:
			qstr = "首尔"
			r = ResultTravel(qstr)
			r.process()
			rstr = r.result_str
			print rstr
			print "=============="
			qstr = ' '.join(jieba.cut("首尔", cut_all=False))
			query = QueryParser("title", ix.schema).parse(qstr)
			results = searcher.search(query)
			for r in results:
			 	print r['title_show'].encode('UTF-8')
	return HttpResponse("Done")

def test_youdao(request):
	from result_youdao import ResultYoudao
	r = ResultYoudao("I am a boy.")
	r.process()
	rstr = r.result_str
	return HttpResponse(rstr)

def test_food(request):
	from result_food import ResultFood
	if True:
		from whoosh.qparser import QueryParser
		ix = open_dir("index/food_index")
		with ix.searcher() as searcher:
			qstr = "猪肉"
			r = ResultFood(qstr)
			r.process()
			rstr = r.result_str
			print rstr
			print "=============="
			qstr = ' '.join(jieba.cut("京酱肉丝", cut_all=False))
			query = QueryParser("title", ix.schema).parse(qstr)
			results = searcher.search(query)
			for r in results:
			 	print r['title_show'].encode('UTF-8')
	return HttpResponse("Done")


