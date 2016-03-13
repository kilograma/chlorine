# -*- coding: utf-8 -*-

from result import Result
from index_food import search_index
from utils import get_split, word_seg_for_search, word_seg_for_index, uni_len

class ResultFood(Result):

	def __init__(self, queryStr):
		self.match_results = []
		self.queryLine = queryStr
		self.queryLine_untokenized = ""
		self.result_str = ""
		return

	def get_result(self):
		rtStr = ""
		queryLine = self.queryLine
		if queryLine.startswith(u"美食 "):
			queryLine = queryLine[len(u"美食 "):]
		self.queryLine_untokenized = queryLine
		queryLine = word_seg_for_search(queryLine)
		results_title = search_index(queryLine=queryLine, query_field="title", N=20)
		id_set = set()
		for title, content in results_title:
			title = title.strip()
			if title in id_set:
				continue
			id_set.add(title)
			content = content.replace(u'\n', u" ").strip()
			if title == self.queryLine_untokenized:
				rs = title + "\n" + content
				self.result_str = rs[0:640]
				return
			self.match_results.append(title)

		results_content = search_index(queryLine=queryLine, query_field="content", N=20)

		for title, _ in results_content:
			title = title.strip()
			if title in id_set:
				continue
			self.match_results.append(title)
		return

	def to_string(self):
		if len(self.result_str) != 0:
			return
		id_set = set()
		if len(self.match_results) == 0:
			self.result_str = u"我真傻，真的，我单知道雪天里野兽在深山里没有食吃....\n竟没找到包含%s的美食..\n\n小Tips:先用简单的词(比如茄子)搜索，然后根据提示逐步扩大搜索范围.\n"%self.queryLine
		else:
			self.result_str = u"菜谱里竟然没有菜和您要的菜完美重名!要不扩大一下搜索范围，例如:\n\n"
			cnt = 0
			for title in self.match_results:
				self.result_str += u"%s\n"%(title.strip())
				cnt += 1
				if cnt == 30:
					break
		return