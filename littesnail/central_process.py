# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode

import xml.etree.ElementTree as ET
import urllib,urllib2,time,hashlib
from django.utils import timezone

from models import *

# from process_youdao import get_youdao_result, need_youdao_result
# from process_wiki import get_wiki_result, need_wiki_result
# from process_special import need_special_result, get_special_result

from result import Result
from create_result import createResult

import sys
sys.path.append('./littesnail/gen-py')

from thsearch import ThSearch
from thsearch.ttypes import *
from thsearch.constants import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

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

def responseMsg(request, is_test=False):
	if not is_test:
		rawStr = smart_str(request.body)
		msg = paraseMsgXml(ET.fromstring(rawStr))
		queryStr = msg.get('Content','You have input nothing~')
		msg_id = msg.get('MsgId', "-1")
		user_id = msg.get("FromUserName", "-1")
		query_date = timezone.now()
	else:
		queryStr = request
	replyContent = ""
	needed_search_count = 5
	if True:
		transport = TSocket.TSocket('localhost', 30303)
  		transport = TTransport.TBufferedTransport(transport)
  		protocol = TBinaryProtocol.TBinaryProtocol(transport)
  		client = ThSearch.Client(protocol)
  		transport.open()
  		replyContent = client.search(queryStr.decode("UTF-8"))
	if len(replyContent) == 0:
		replyContent = u"好像服务出了点问题~~深吸一口气...嚎！不，再试一次..."

	uni_reply = replyContent[:640]
	replyContent = uni_reply.encode("UTF-8")

	if not is_test:
		query_result_date = timezone.now()

		uq = UserQuery(user_id=user_id, query_str=queryStr, query_date=query_date, query_result_date=query_result_date, query_msg_id=msg_id, query_result=replyContent)
		uq.save()

		return getReplyXml(msg,replyContent)
	else:
		return replyContent

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
