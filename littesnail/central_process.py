# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode

import xml.etree.ElementTree as ET
import urllib,urllib2,time,hashlib

from process_youdao import get_youdao_result, need_youdao_result
from process_wiki import get_wiki_result, need_wiki_result
from process_special import need_special_result, get_special_result

TOKEN = "weixin"

@csrf_exempt
def handleRequest(request):
	if request.method == 'GET':
		response = HttpResponse(checkSignature(request),content_type="text/plain")
		return response
	elif request.method == 'POST':
		response = HttpResponse(responseMsg(request),content_type="application/xml")
		return response
	else:
		return None

def checkSignature(request):
	global TOKEN
	signature = request.GET.get("signature", None)
	timestamp = request.GET.get("timestamp", None)
	nonce = request.GET.get("nonce", None)
	echoStr = request.GET.get("echostr",None)

	token = TOKEN
	tmpList = [token,timestamp,nonce]
	tmpList.sort()
	tmpstr = "%s%s%s" % tuple(tmpList)
	tmpstr = hashlib.sha1(tmpstr).hexdigest()
	if tmpstr == signature:
		return echoStr
	else:
		return None

def responseMsg(request):
	#rawStr = smart_str(request.raw_post_data)
	rawStr = smart_str(request.body)
	#rawStr = smart_str(request.POST['XML'])
	msg = paraseMsgXml(ET.fromstring(rawStr))
	queryStr = msg.get('Content','You have input nothing~')
	msg_id = msg.get('MsgId', "-1")
	user_id = msg.get("FromUserName", "-1")
	replyContent = ""
	needed_search_count = 5
	try:
		if need_special_result(queryStr):
			replyContent = get_special_result(queryStr, user_id, msg_id)
			print 'special:', queryStr
			print replyContent
		else:
			if need_youdao_result(queryStr):
				replyContent += get_youdao_result(queryStr).encode("UTF-8")
				needed_search_count -= 1 
			if need_wiki_result(queryStr):
				replyContent += get_wiki_result(queryStr, user_id, msg_id)
				needed_search_count -= 1
				print 'wiki', queryStr
				print replyContent
	except:
		print "出问题了", queryStr, user_id
		pass
	if len(replyContent) == 0:
		replyContent = "好像服务出了点问题~~"
	return getReplyXml(msg,replyContent)

def paraseMsgXml(rootElem):
	msg = {}
	if rootElem.tag == 'xml':
		for child in rootElem:
			msg[child.tag] = smart_str(child.text)
	return msg

def getReplyXml(msg,replyContent):
	extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
	extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',replyContent)
	return extTpl
