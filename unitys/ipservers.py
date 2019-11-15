# -*- coding:utf-8 -*-
import os,sys,json
import redis
from tornado.web import Application, RequestHandler, url
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options,define
import tornado.options
import configparser


Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\\main.conf"

def get_config( sector, item):
    config = configparser.ConfigParser()
    config.read(Path, encoding="utf-8")
    value = config.get(sector, item)
    return value

Port = int(get_config('GoInit', 'serversport'))

pool = redis.ConnectionPool(host = get_config('RedisInfo', 'host'),
                            port = get_config('RedisInfo', 'port'), 
                            db = get_config('RedisInfo', 'db'),
                            password = None,
                            decode_responses = True)

def get_ips():
    r =  redis.StrictRedis(connection_pool = pool)
    return r.zrange(get_config('IPPoolInfo', 'ippools'),0,-1,desc=True)


define("port", default=Port, type=int)


class IndexHandler(RequestHandler):

   def set_default_headers(self):
        # 第二种响应头设置方式
        print("---------> 响应头set_default_headers()执行")
        self.set_header("Content-type", "application/json; charset=utf-8")
        self.set_header("Mange", "ManGe")
   def get(self):
        datas = {'status':'succeed','iplist':get_ips()}
        #datas = {'status':'succeed'}
        self.write(json.dumps(datas).encode('utf-8').decode("unicode-escape"))
        self.set_header("Content-type", "application/json; charset=utf-8")





URL_PATH = [
	url(r"/", IndexHandler, name="IndexHandler"),
            ]


if __name__ == "__main__":
    app = Application(URL_PATH)
    tornado.options.parse_command_line()
    http_server = HTTPServer(app)
    http_server.listen(Port)
    IOLoop.current().start()
