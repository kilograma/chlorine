# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import urllib,urllib2,time,hashlib
import utils

YOUDAO_KEY = 1416234552
YOUDAO_KEY_FROM = "Hstream"
YOUDAO_DOC_TYPE = "xml"


def need_youdao_result(queryStr):
	return not utils.has_chinese(queryStr)


def get_youdao_result(queryStr):
	raw_youdaoURL = "http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=%s&version=1.1&q=" % (YOUDAO_KEY_FROM,YOUDAO_KEY,YOUDAO_DOC_TYPE)	
	youdaoURL = "%s%s" % (raw_youdaoURL,urllib2.quote(queryStr))
	req = urllib2.Request(url=youdaoURL)
	result = urllib2.urlopen(req).read()
	replyContent = paraseYouDaoXml(ET.fromstring(result))
	return replyContent

def paraseYouDaoXml(rootElem):
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

if __name__=='__main__':
	queryStr = "what do you mean?"
	assert(need_youdao_result(queryStr) == True)
