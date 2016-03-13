# -*- coding: utf-8 -*-

from result import Result
from index_weibo import search_index
from utils import get_split, word_seg_for_search, word_seg_for_index, uni_len
import random

class ResultWeibo(Result):

	def __init__(self, queryStr):
		self.queryLine = queryStr
		self.result_str = ""
		self.results = []
		return

	def get_result(self):
		queryLine = self.queryLine
		queryLine = word_seg_for_search(queryLine)
		self.results = search_index(queryLine=queryLine, N=200)
		return

	def to_string(self):
		queryLine = self.queryLine
		queryLine = word_seg_for_search(queryLine)
		used_str = set()
		if len(self.results) == 0:
			self.result_str = u"竟然没有含%s的任何信息...你知不知道这个时候该做什么？立马告诉管理员去！"%self.queryLine
		else:
			self.result_str = u""
			lc = 0
			for content in self.results:
				lc += 1
				l_content = len(content)
				if l_content + len(self.result_str) > 640:
					break
				rnd = random.uniform(0, 0.8)
				if rnd > max(1.0/lc, 0.1):
					continue
				self.result_str += u"%s\n\n"%(content.strip())
			#print lc
		return