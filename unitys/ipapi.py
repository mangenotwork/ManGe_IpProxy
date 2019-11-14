# -*- coding:utf-8 -*-
import os,sys,json

from tornado.web import Application, RequestHandler, url
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options,define
import tornado.options


import addtoredis as addtoredis


define("port", default=9123, type=int)


class IndexHandler(RequestHandler):

   def set_default_headers(self):
        # 第二种响应头设置方式
        print("---------> 响应头set_default_headers()执行")
        self.set_header("Content-type", "application/json; charset=utf-8")
        self.set_header("Mange", "ManGe")
   def get(self):
        #print(addtoredis.get_allips())
        #print(type(addtoredis.get_allips()))
        datas = {'status':'succeed','iplist':addtoredis.get_allips()}
        self.write(json.dumps(datas).encode('utf-8').decode("unicode-escape"))
        self.set_header("Content-type", "application/json; charset=utf-8")





URL_PATH = [
	url(r"/", IndexHandler, name="IndexHandler"),
            ]


if __name__ == "__main__":
    app = Application(URL_PATH)
    tornado.options.parse_command_line()
    http_server = HTTPServer(app)
    http_server.listen(9123)
    IOLoop.current().start()
