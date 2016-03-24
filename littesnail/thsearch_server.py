#!/usr/bin/env python
# encoding=utf-8
import sys
sys.path.append('./littesnail/gen-py')
 
from thsearch import ThSearch
from thsearch.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
 
import socket

from result import Result
from create_result import createResult
from utils import help_info

class SearchHandler:
  def __init__(self):
    self.log = {}

  def search(self, keyword):#keyword in unicode!
    if True:
      r = createResult(keyword) #unicode
      if r == None:
        replyContent = help_info()
      else:
        r.process()
        replyContent = r.result_str
    #except:
    #  print "Exception! for keyword:=", keyword
    #  replyContent = ""
    #  pass
    return replyContent

if __name__ == '__main__':
  handler = SearchHandler()
  processor = ThSearch.Processor(handler)
  transport = TSocket.TServerSocket('localhost',30303)
  tfactory = TTransport.TBufferedTransportFactory()
  pfactory = TBinaryProtocol.TBinaryProtocolFactory()

  server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

  print "Starting python server..."
  server.serve()
  print "done!"