#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 

import redis

HostIP = '192.168.1.20'

pool = redis.ConnectionPool(host = HostIP,port = 6379, db = 7,password = None,decode_responses = True)


#这里网上的教程都错误
#增加元素,注意参数必须是个字典，字典的key是redis的value,字典的value是redis的score


def add(ips):
	r =  redis.StrictRedis(connection_pool = pool)
	r.rpush("ip:queue",ips)


