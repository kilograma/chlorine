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
	print responseMsg("北京", True)
	print "==================="
	print responseMsg("龟龟", True)
	print "==================="
	print responseMsg("龟龟", True)
	print "==================="
	print responseMsg("龟龟", True)
	print "==================="
	print responseMsg("龟龟", True)
	print "==================="
	print responseMsg("生活大爆炸", True)
	print "==================="
	print responseMsg("龟儿子", True)
	print "==================="
	print responseMsg("皮蛋瘦肉粥", True)
	print "==================="
