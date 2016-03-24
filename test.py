# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "littesnail.settings")
import littesnail.wsgi
from littesnail.central_process import responseMsg

if True:
	print responseMsg("旅游 首尔", True)
	print "==================="
if True:
	print responseMsg("美食 京酱肉丝", True)
	print "==================="
if False:
	print responseMsg("fuck", True)
	print "==================="
if False:
	print responseMsg("百科 北京", True)
	print "==================="

if True:
	print responseMsg("文艺 哈利波特", True)
	print "==================="
	print responseMsg("文艺 茶花女", True)
	print "==================="
	print responseMsg("文艺 三国演义", True)
	print "==================="
	print responseMsg("文艺 钢铁是怎样炼成的", True)
	print "==================="
	print responseMsg("文艺 茶馆", True)
	print "==================="
	print responseMsg("文艺 生活大爆炸", True)
	print "==================="
