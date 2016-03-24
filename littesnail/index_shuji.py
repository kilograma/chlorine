# -*- coding: utf-8 -*-
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from utils import *

WEIBO_INDEX_DIR = "index/shuji_index"

ix = None

def make_index(weibo_path):
	schema = Schema(content=TEXT, content_show=STORED)
	global ix
	global WEIBO_INDEX_DIR

	valid_keys = set()
	for line in open("../data/shuji_key.txt"):
		line = line.strip()
		if len(line) != 0:
			valid_keys.add(line.decode("UTF-8"))

	ix = create_in(WEIBO_INDEX_DIR, schema)
	writer = ix.writer()

	lines = []
	title = ""
	url = None
	lc = 0
	p = re.compile(ur'《[^ ]+?》')
	for line in open(weibo_path):
		if True:
			lc += 1
			if lc % 10000 == 0:
				print lc
				#if lc >= 5000000:
				#	break
			line = line.strip().decode("UTF-8")
			if len(line) == 0:
				continue
			keys = set()
			objs = p.findall(line)
			for obj in objs:
				obj = obj[1:-1]
				if obj in valid_keys:
					keys.add(obj)
					obj1 = re.sub(ur'[0-9a-zA-Z]+', ur'', obj).strip()
					if len(obj1) > 0 and obj != obj1:
						keys.add(obj1)
			content_show = line
			content = ' '.join(keys).strip()
			if len(content) == 0:
				continue
			#content = word_seg_for_index(line).strip()
			#content_show = line
			writer.add_document(content=content, content_show=content_show)

	writer.commit()
	return

def search_index(queryLine, N):#unicode!!!
	global ix
	global WEIBO_INDEX_DIR
	if not ix:
		ix = open_dir(WEIBO_INDEX_DIR)
	rt = []
	with ix.searcher() as searcher:
		query = QueryParser('content', ix.schema).parse(queryLine)
		results = searcher.search(query, limit=N)
		for r in results:
			rt.append(r['content_show'])
			N -= 1
			#print N
			if N == 0:
				break
	return rt



if False:
	make_index('../data/weibo_shuji.txt')
