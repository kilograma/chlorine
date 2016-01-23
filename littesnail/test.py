# -*- coding: utf-8 -*-

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh import scoring
import jieba
from process_wiki import get_wiki_result



if False:
	from whoosh.qparser import QueryParser
	ix = open_dir("../index/wiki_index_old")
	with ix.searcher() as searcher:
		qstr = ' '.join(jieba.cut("中华共和国", cut_all=False))
		query = QueryParser("title", ix.schema).parse(qstr)
		results = searcher.search(query)
		for r in results:
			print r['title_show'].encode('UTF-8')