# -*- coding: utf-8 -*-

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from utils import get_split, word_seg_for_search, word_seg_for_index

WIKI_INDEX_DIR = "index/travel_index"

ix = None

def make_index(travel_raw_path):
	schema = Schema(url=ID(stored=True, unique=True), title=TEXT, title_show=STORED)
	global ix
	global WIKI_INDEX_DIR

	ix = create_in(WIKI_INDEX_DIR, schema)
	writer = ix.writer()

	lc = 0
	for line in open(travel_raw_path):
		try:
			lc += 1
			if lc % 100 == 0:
				print lc
			line = line.strip()
			ss = line.split("\t")
			if len(ss) != 2:
				continue
			url, title = ss
			writer.add_document(url=url, title=word_seg_for_index(title).decode('UTF-8'), title_show=title.decode('UTF-8'))
		except:
			print line
			pass

	writer.commit()
	return

def search_index(queryLine, N):#unicode!!!
	global ix
	global WIKI_INDEX_DIR
	if not ix:
		ix = open_dir(WIKI_INDEX_DIR)
	rt = []
	with ix.searcher() as searcher:
		query = QueryParser("title", ix.schema).parse(queryLine)
		results = searcher.search(query)
		for r in results:
			rt.append([r['url'], r['title_show']])
			N -= 1
			if N == 0:
				break
	return rt



if False:
	make_index('data/mafengwo.pure.txt')