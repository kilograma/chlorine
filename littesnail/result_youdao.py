# -*- coding: utf-8 -*-

from result import Result
from index_wiki import search_index
from utils import get_split, word_seg_for_search, word_seg_for_index, uni_len

import xml.etree.ElementTree as ET
import urllib,urllib2,time,hashlib

class ResultYoudao(Result):

	def __init__(self, queryStr):
		self.queryLine = queryStr
		self.result_str = ""
		return

	def get_result(self):
		self.result_str = self.get_youdao_result()
		return

	def to_string(self):
		return

	def get_youdao_result(self):
		YOUDAO_KEY = 1416234552
		YOUDAO_KEY_FROM = "Hstream"
		YOUDAO_DOC_TYPE = "xml"

		queryStr = self.queryLine
		raw_youdaoURL = "http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=%s&version=1.1&q=" % (YOUDAO_KEY_FROM,YOUDAO_KEY,YOUDAO_DOC_TYPE)	
		youdaoURL = "%s%s" % (raw_youdaoURL,urllib2.quote(queryStr))
		req = urllib2.Request(url=youdaoURL)
		result = urllib2.urlopen(req).read()
		replyContent = self.paraseYouDaoXml(ET.fromstring(result))
		return replyContent.encode("UTF-8")

	def paraseYouDaoXml(self, rootElem):
		replyContent = ''
		if rootElem.tag == 'youdao-fanyi':
			for child in rootElem:
				# 错误码
				if child.tag == 'errorCode':
					if child.text == '20':
						return 'too long to translate\n'
					elif child.text == '30':
						return 'can not be able to translate with effect\n'
					elif child.text == '40':
						return 'can not be able to support this language\n'
					elif child.text == '50':
						return 'invalid key\n'
				# 查询字符串
				elif child.tag == 'query':
					replyContent = "%s%s\n" % (replyContent, child.text)
				# 有道翻译
				elif child.tag == 'translation': 
					replyContent = '%s%s\n%s\n' % (replyContent, '-' + u'有道翻译' + '-' , child[0].text)
				# 有道词典-基本词典
				elif child.tag == 'basic': 
					replyContent = "%s%s\n" % (replyContent, '-' + u'基本词典' + '-')
					for c in child:
						if c.tag == 'phonetic':
							replyContent = '%s%s\n' % (replyContent, c.text)
						elif c.tag == 'explains':
							for ex in c.findall('ex'):
								replyContent = '%s%s\n' % (replyContent, ex.text)
				# 有道词典-网络释义
				elif child.tag == 'web': 
					replyContent = "%s%s\n" % (replyContent, '-' + u'网络释义' + '-')
					for explain in child.findall('explain'):
						for key in explain.findall('key'):
							replyContent = '%s%s\n' % (replyContent, key.text)
						for value in explain.findall('value'):
							for ex in value.findall('ex'):
								replyContent = '%s%s\n' % (replyContent, ex.text)
						replyContent = '%s%s\n' % (replyContent,'--')
		return replyContent