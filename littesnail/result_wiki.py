# -*- coding: utf-8 -*-

from result import Result
from index_wiki import search_index
from utils import get_split, word_seg_for_search, word_seg_for_index, uni_len

class ResultWiki(Result):

	def __init__(self, queryStr):
		self.title_match_results = []
		self.content_match_results = []
		self.queryLine = queryStr
		self.result_str = ""
		return

	def get_result(self):
		rtStr = ""
		queryLine = self.queryLine
		if queryLine.startswith("百科 "):
			queryLine = queryLine[len("百科 "):]
		queryLine = word_seg_for_search(queryLine)
		results_title = search_index(queryLine=queryLine.decode('UTF-8'), query_field="title", N=10)
		for url, title, content in results_title:
			excerpt = content.replace('\n', " ")
			blank_pos = excerpt.find(" ")
			if blank_pos != -1:
				excerpt = excerpt[blank_pos+1:]
			self.title_match_results.append([url.strip(), title.strip(), excerpt.strip()])

		results_content = search_index(queryLine=queryLine.decode('UTF-8'), query_field="content", N=10)

		for url, title, _ in results_content:
			self.content_match_results.append([url.strip(), title.strip()])
		return

	def to_string(self):
		id_set = set()
		if len(self.title_match_results) == 0:
			self.result_str = "竟没找到包含%s的百科条目..换个词?\n"%self.queryLine
		else:
			self.result_str = "客官，我们有(点击查看):\n\n"
			cnt = 0
			for url, title, content in self.title_match_results:
				excerpt = content.decode('UTF-8')[0:60].encode('UTF-8').replace('\n', " ")
				blank_pos = excerpt.find(" ")
				if blank_pos != -1:
					excerpt = excerpt[blank_pos+1:]
				this_result =  "<a href=\"%s\">%s</a>。%s...\n\n"%(url.strip(), title.strip(), excerpt.strip())
				if uni_len(self.result_str) + uni_len(self.result_str) >= 650:
					break
				self.result_str += this_result
				id_set.add(url)		
				cnt += 1
				if cnt > 3:
					break

		if len(self.content_match_results) == 0:
			pass
		else:
			cnt = 0
			for url, title in self.content_match_results:
				if url in id_set:
					continue
				if cnt == 0:
					self.result_str += "===\n其他人试过:\n"
				self.result_str += "%s\n"%(title.strip())
				id_set.add(url)
				cnt += 1
				if cnt == 10:
					break
		return