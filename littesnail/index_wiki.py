# -*- coding: utf-8 -*-

from whoosh.index import create_in, open_dir
from whoosh.fields import *
import jieba
from whoosh.qparser import QueryParser

WIKI_INDEX_DIR = "../index/wiki_index"

ix = None

def make_index(wiki_path):
	schema = Schema(iid=ID(stored=True, unique=True), title=TEXT, title_show=STORED, content=TEXT, content_show=STORED)
	global ix
	global WIKI_INDEX_DIR

	ix = create_in(WIKI_INDEX_DIR, schema)
	writer = ix.writer()

	lines = []
	title = ""
	iid = -1
	lc = 0
	for line in open(wiki_path):
		try:
			lc += 1
			if lc % 100 == 0:
				print lc
			line = line.strip()
			if len(line) == 0:
				continue
			if line.startswith("<doc id="):
				lines = []
				pos_l = line.find("\"") + 1
				pos_r = line.find("\"", pos_l)
				iid = int(line[pos_l:pos_r])
			elif line.startswith("</doc>"):
				l_tks = []
				for l in lines:
					tks = jieba.cut_for_search(l)
					l_tks += tks
				content = ' '.join(l_tks)
				content_show = '\n'.join(lines)
				writer.add_document(iid=str(iid).decode('UTF-8'), title=' '.join(jieba.cut_for_search(title.decode('UTF-8'))), title_show=title.decode('UTF-8'), content=content, content_show=content_show.decode('UTF-8'))
			else:
				if len(line) == 0:
					continue
				if len(lines) == 0:
					title = line
				lines.append(line)
		except:
			print line
			pass

	writer.commit()
	return

def search_index(queryLine, query_field, N):#UTF8 str
	global ix
	global WIKI_INDEX_DIR
	if not ix:
		ix = open_dir(WIKI_INDEX_DIR)

	rt = []

	with ix.searcher() as searcher:
		#qstr = ' '.join(jieba.cut(queryLine, cut_all=False))
		query = QueryParser(query_field, ix.schema).parse(queryLine)
		results = searcher.search(query)
		for r in results:
			rt.append([r['iid'].encode('utf-8'), r['title_show'].encode('UTF-8'), r['content_show'].encode('UTF-8')])
			N -= 1
			if N == 0:
				break
	return rt



if False:
	make_index('../data/wiki-simplified.txt')