#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 


import os
import time
import redis
import requests
import threading
import multiprocessing

#from multiprocessing import Process

# 导入 nimadaili 代理
import ips_nimadaili as nimadaili
# 导入 爬取代理
import ips_get as getips
from unitys import addtoredis as toredis


#ip队列
IPQueue = "ip:queue"
#ip代理池
#IPPools = "ips:pool"
IPPools = "ips:qgjz"
#redis主机ip地址
HostIP = '192.168.1.20'

pool = redis.ConnectionPool(host = HostIP,port = 6379, db = 7,password = None,decode_responses = True)
r =  redis.StrictRedis(connection_pool = pool)



#验证代理ip有效性地址
#JCUrl = "http://jzsc2016.mohurd.gov.cn/asite/jsbpp/index"
#JCUrl = "https://www.baidu.com/"
JCUrl = "http://www.httpbin.org/ip"


#验证代理的相对响应时间
NormalTime = 1.0

#判断ip的存活性的线程数
#ipChecker_ThreadNumber = 10

#在ip队列里取出有效ip的线程数
yzips_ThreadNumber = 20






#公用 验证方法  通过对指定网站的请求加以判断IP的有效性
def yzPub(ipinfo):
	httpinfo = str(ipinfo).split("://")
	proxy_dict = {str(httpinfo[0]):str(ipinfo),}
	print(proxy_dict)
	try:
		baidu = requests.get( JCUrl, proxies=proxy_dict, timeout=2)
		seconddata = baidu.elapsed.total_seconds()
		statusCode = baidu.status_code
		print("statusCode ==> ",statusCode)
		print("seconddata ==> ",seconddata)
		if statusCode in [200,302]:
			return True,seconddata
		return False,None
	except Exception as e:
		print(ipinfo," --> ip不可用")
		return False,None



#  1. 取爬回来的IP队列进行验证有效性和时间，再放入 ip池子
def yzips():
	#检查 redis list数据长度如果为空就不执行，让其等待10s
	if r.llen(IPQueue) != 0:
		ipinfo = r.lpop(IPQueue)
		if ipinfo == None:
			return 0
		yzKeys,seconddata = yzPub(ipinfo)
		if yzKeys:
			print(ipinfo," --> ip可用，添加到ip池")
			#r.zadd('ips:ips', {ipinfo:float(seconddata)} )
			r.zadd(IPPools, float(seconddata), ipinfo )
		else:
			print(ipinfo," --> ip不可用")
	else:
		print(" ip:queue is Null wite 10s...")
		time.sleep(10)
	

#执行验证ip
def yzips_run():
	while 1:
		yzips()
		#time.sleep(1)
		print("取下个IP队列")
		print("\n\n")

#验证ip有限的线程
class yzipThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        
    def run(self):
        print("threadID ==> " + str(self.threadID))
        #执行验证ip
        yzips_run()
        print("Exiting " + str(self.threadID))


#检查IP贷理池的存活性的线程
class ipCheckerThread (threading.Thread):
    def __init__(self,threadID,ipslist):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ipslist = ipslist

    def run(self):
        print("threadID ==> " + str(self.threadID))
        #执行检查IP贷理池的存活性
        ipChecker_run(self.ipslist)
        print("Exiting " + str(self.threadID))


#均分list
def div_list(ls,n):
   result = []
   cut = int(len(ls)/n)
   if cut == 0:
       ls = [[x] for x in ls]
       none_array = [[] for i in range(0, n-len(ls))]
       return ls+none_array
   for i in range(0, n-1):
       result.append(ls[cut*i:cut*(1+i)])
   result.append(ls[cut*(n-1):len(ls)])
   return result


#检查器
# 每次全部取出，足个进行验证  能用保留 不能用删除，验证IP的存活性
@toredis.ipChecker_Thread
def ipChecker(ipChecker_ThreadNumber):
    allips = r.zrange( IPPools, 0, -1, desc=True)
    gurpips = div_list( allips, ipChecker_ThreadNumber)
    #开启5个线程
    ps=[]
    # 创建子线程
    for i in range(ipChecker_ThreadNumber):
        p=ipCheckerThread(i, gurpips.pop(0))
        ps.append(p)
 
    # 开启线程
    for i in range(ipChecker_ThreadNumber):
        ps[i].start()
 
    # 阻塞线程
    for i in range(ipChecker_ThreadNumber):
        ps[i].join()
    print("检查有效性线程结束")	


#执行检查IP贷理池的存活性
def ipChecker_run(iplist):
	print(iplist)
	if iplist != []:
	    for ipinfo in iplist:
	        #print(yzPub(ipinfo))
	        # 如果ip还可以用就更新 请求时间； 否则删除
	        yzKeys,seconddata = yzPub(ipinfo)
	        if yzKeys and seconddata < NormalTime:
	            print(ipinfo," --> ip可用，更新到ip池")
	            #r.zadd('ips:ips', {ipinfo:float(seconddata)} )
	            r.zadd(IPPools, float(seconddata), ipinfo )
	        else:
	            print(ipinfo," --> ip不可用")
	            r.zrem(IPPools, ipinfo)
	else:
		time.sleep(10)
		print("iplist is null ipChecker_run wite 10s ...")



#运行ipChecker
def go_ipChecker():
	while True:
		ipChecker()


#运行yzips
def go_yzips():
    ps=[]
    # 创建子线程
    for i in range(yzips_ThreadNumber):
        p=yzipThread(i)
        ps.append(p)
    # 开启线程
    for i in range(yzips_ThreadNumber):
        ps[i].start()
    # 阻塞线程
    for i in range(yzips_ThreadNumber):
        ps[i].join()
    print("线程终止")


#旧的启动方式
def go_main_old():
    print('Parent process %s.' % os.getpid())
    #IP队列赛选进程
    pid_yzips = Process(target=go_yzips, args=())
    #IP池检查进程
    pid_ipChecker = Process(target=go_ipChecker, args=())
    # nimadaili 代理爬虫
    pid_nimadaili = Process(target=nimadaili.go_nimadaili_run, args=())
    # crossincode 代理爬虫
    pid_crossincode = Process(target=getips.get_crossincode_ips, args=())
    # xiladaili 代理爬虫
    pid_xiladaili = Process(target=getips.get_xiladaili_ips, args=())
    print('Child process will start.')
    pid_all = [ pid_nimadaili, pid_yzips, pid_ipChecker, pid_crossincode, pid_xiladaili]
    for i in pid_all:
        i.start()
    for i in pid_all:
        i.join()


#新的启动方式
def go_main():
    #cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=7)
    while True:
        pool.apply_async(go_yzips, ())#IP队列赛选进程
        pool.apply_async(go_ipChecker, ())#IP池检查进程
        pool.apply_async(nimadaili.go_nimadaili_run, ())# nimadaili 代理爬虫
        pool.apply_async(getips.get_kuaidaili_ips, ())# kuaidaili 代理爬虫
        pool.apply_async(getips.get_ip_run, ())# 代理爬虫
        pool.apply_async(getips.get_xicidaili_ips, ())# xici代理爬虫
        #print("有进程死掉,等待3s")
        time.sleep(3)
    print("-----start-----")
    pool.close() # 关闭进程池，关闭后po不再接收新的请求
    pool.join() # 等待po中所有子进程执行完成，必须放在close语句之后
    print("-----end-----")


if __name__=='__main__':
    go_main()