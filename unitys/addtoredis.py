#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 

import os
import sys
import random
import redis
import time

HostIP = '192.168.1.20'

pool = redis.ConnectionPool(host = HostIP,port = 6379, db = 7,password = None,decode_responses = True)

IPQueueMaxLen = 100000
IPQueueMemoryProtection_Time = 1*60
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

#获取所有的代理ip
def get_allips():
    r =  redis.StrictRedis(connection_pool = pool)
    return r.zrange('ips:qgjz',0,-1,desc=True)

#获取IP队列总数
def get_ipqueue_len():
	r =  redis.StrictRedis(connection_pool = pool)
	#print(r.llen("ip:queue"))
	return r.llen("ip:queue")


#在每次爬取之前判断是否大于设置的ip队列大小
# 如果大于则休息，否则继续爬取
def IPQueue_MemoryProtection(func=None):
    def deco(func):
        def wrapper(*args,**kwargs):
            if get_ipqueue_len() < IPQueueMaxLen:
            	print("ip队列不保护")
            	return func(*args,**kwargs)
            else:
            	print("ip队列保护")
            	time.sleep(IPQueueMemoryProtection_Time)
            	return 0
        wrapper.__name__ = func.__name__
        return wrapper
    return deco if not func else deco(func)




 

#获取当前代理池的总量
def get_PoolLen():
	r =  redis.StrictRedis(connection_pool = pool)
	#print(r.zcard("ips:qgjz"))
	return r.zcard("ips:qgjz")


def get_jcThreadNumber():
	poollen = get_PoolLen()
	print(int(poollen/1000))
	if int(poollen/1000)<=0:
		jc_ThreadNumber = 1
	elif int(poollen/1000)<=25:
		jc_ThreadNumber = int(poollen/1000)
	else:
		jc_ThreadNumber = 25
	print("\n\n get_jcThreadNumber  **********",jc_ThreadNumber)
	return jc_ThreadNumber

# 	1. 根据当前池子里的ip数量控制判断ip的存活性的检测周期   Max 10s
# 	2. 根据当前池子里的ip数量控制判断ip的存活性的线程数 	Max 25
# 	3. poollen/1000 
def ipChecker_Thread(func=None):
    def deco(func):
        def wrapper(*args,**kwargs):
            jcThreadNumber = get_jcThreadNumber()
            if jcThreadNumber < 2:
                time.sleep(30)
            return func(jcThreadNumber,*args,**kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return deco if not func else deco(func)



def start_man_api():
    print(" _____________________________________________")
    print(" __  __                  _____  _____       ")
    print("|  \/  |                |_   _||  __  |       ")
    print("| \  / | __ _ _ ___       | |  | |__) |      ")
    print("| |\/| |/ _` | '_  \      | |  |  ___/      ")
    print("| |  | | (_| | | | |     _| |_ | |         ")
    print("|_|  |_|\__,_|_| |_|    |_____||_|         ")
                                                                    
    print(" _____________________________________________")
    print("************************ v0.3  *********************************")
    print("*****     ManGe_IpProxy IP代理池v0.3                       *****")
    print("*****     www.mangenotwork.com                             *****")
    print("*****     https://github.com/mangenotwork/ManGe_IpProxy    *****")
    print("****************************************************************")
    print("\n\n")
    print("【监控】")
    print("--> IPQueue(当前抓取的IP)  : " + str(get_ipqueue_len()))
    print("--> IPPool(当前IP池里的IP) : " + str(get_PoolLen()))
    print("\n\n【IP排名】")



def ManIPinfos():
	while True:
		time.sleep(1)
		#sys.stdout.write( "\n\r  IPQueue : "+ str(get_ipqueue_len())+"  IPPool  : " + str(get_PoolLen())+"\r")
		#sys.stdout.flush()
		os.system('cls')
		start_man_api()


#ManIPinfos()


# 1. 当线程池的数量大于限制数量时，让取队列的线程进行休息，保证了线程池不会无限增长


# 2. 内置redis 启动


# 3. 内置tornado 并开放接口


# 4. 配置文件 config


# 5. 