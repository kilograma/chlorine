# -*- coding: utf-8 -*-

from result import Result
from index_travel import search_index
from utils import get_split, word_seg_for_search, word_seg_for_index, uni_len

class ResultTravel(Result):

	def __init__(self, queryStr):
		self.queryLine = queryStr
		self.result_str = ""
		self.results = []
		return

	def get_result(self):
		queryLine = self.queryLine
		if queryLine.startswith(u"旅游 "):
			queryLine = queryLine[len(u"旅游 "):]
		queryLine = word_seg_for_search(queryLine)
		results_title = search_index(queryLine=queryLine, N=9)
		if len(results_title) == 0:
			pass
		else:
			for url, title in results_title:
				self.results.append([title.strip(), url.strip()])
		return

	def to_string(self):
		queryLine = self.queryLine
		queryLine = word_seg_for_search(queryLine)
		id_set = set()
		if len(self.results) == 0:
			self.result_str = u"竟没找到包含%s的旅游信息...换个词?"%self.queryLine
		else:
			for url, title in self.results:
				self.result_str += u"%s%s\n\n"%(title.strip(), url.strip())
				id_set.add(url)		
		return