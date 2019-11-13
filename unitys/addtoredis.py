#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 

import random
import redis

HostIP = '192.168.1.20'

pool = redis.ConnectionPool(host = HostIP,port = 6379, db = 7,password = None,decode_responses = True)


#这里网上的教程都错误
#增加元素,注意参数必须是个字典，字典的key是redis的value,字典的value是redis的score


def add(ips):
	r =  redis.StrictRedis(connection_pool = pool)
	r.rpush("ip:queue",ips)

def get_ips():
    r =  redis.StrictRedis(connection_pool = pool)
    ipnumber = r.zcard('ips:qgjz')
    if ipnumber <= 1:
        number = 0
    else:
        number = random.randint(0, ipnumber-1)
    a = r.zrange('ips:qgjz',0,-1,desc=True)
    #print(a)
    print(a[number])
    return a[number]
