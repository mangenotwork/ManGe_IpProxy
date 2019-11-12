import os
import time
import threading
import redis
import requests

from multiprocessing import Process

# 导入 nimadaili 代理
import ips_nimadaili as nimadaili
import ips_get as getips

HostIP = '192.168.1.20'

pool = redis.ConnectionPool(host = HostIP,port = 6379, db = 7,password = None,decode_responses = True)
r =  redis.StrictRedis(connection_pool = pool)


#验证代理ip有效性地址
#JCUrl = "http://jzsc2016.mohurd.gov.cn/asite/jsbpp/index"
JCUrl = "https://www.baidu.com/"
#JCUrl = "http://www.httpbin.org/ip"

#验证代理的相对响应时间
NormalTime = 1.0


#公用 验证方法  通过对指定网站的请求加以判断
def yzPub(ipinfo):
	httpinfo = str(ipinfo).split("//")
	#print(httpinfo)
	proxy_dict = {str(httpinfo[0]):str(ipinfo),}
	print(proxy_dict)
	try:
		baidu = requests.get( JCUrl, proxies=proxy_dict)
		#print(baidu.status_code)
		seconddata = baidu.elapsed.total_seconds()
		#print(seconddata)
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
	if r.llen("ip:queue") != 0:
		ipinfo = r.lpop("ip:queue")
		if ipinfo == None:
			return 0
		yzKeys,seconddata = yzPub(ipinfo)
		if yzKeys:
			print(ipinfo," --> ip可用，添加到ip池")
			#r.zadd('ips:ips', {ipinfo:float(seconddata)} )
			r.zadd('ips:ips', float(seconddata),ipinfo )
		else:
			print(ipinfo," --> ip不可用")
	else:
		print(" ip:queue is Null wite 10s...")
		time.sleep(10)
	'''
	ipinfo = r.lpop("ip:queue")
	if ipinfo == None:
		return 0
	#print(ipinfo)
	#print(type(ipinfo))
	httpinfo = str(ipinfo).split("//")
	#print(httpinfo)
	proxy_dict = {str(httpinfo[0]):str(ipinfo),}
	print(proxy_dict)

	try:
		baidu = requests.get( JCUrl, proxies=proxy_dict)
		print(baidu.status_code)
		
		seconddata = baidu.elapsed.total_seconds()
		print(seconddata)
		statusCode = baidu.status_code
		print("statusCode ==> ",statusCode)
		if statusCode in [200,302]:
			print(ipinfo," --> ip可用，添加到ip池")
			#r.zadd('ips:ips', {ipinfo:float(seconddata)} )
			r.zadd('ips:ips', float(seconddata),ipinfo )

	except Exception as e:
		print(ipinfo," --> ip不可用")
	'''
	'''
	baidu = requests.get("https://www.baidu.com/",proxies=proxy_dict)
	print(baidu.status_code)
	
	seconddata = baidu.elapsed.total_seconds()
	print(seconddata)
	if baidu.status_code == 200:
		print("22222")
		#r.zadd('ips:ips', {ipinfo:float(seconddata)} )
		r.zadd('ips:ips', float(seconddata),ipinfo )
	'''

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
# 每次全部取出，足个进行验证  能用保留 不能用删除，验证完成后休息1分钟
def ipChecker():
    allips = r.zrange('ips:ips',0,-1,desc=True)
    gurpips = div_list(allips,3)
    #开启5个线程
    PID_test_number = 3
    ps=[]
    # 创建子线程
    for i in range(PID_test_number):
        p=ipCheckerThread(i,gurpips.pop(0))
        ps.append(p)
 
    # 开启线程
    for i in range(PID_test_number):
        ps[i].start()
 
    # 阻塞线程
    for i in range(PID_test_number):
        ps[i].join()
    print("检查有效性线程结束")	

#执行检查IP贷理池的存活性
def ipChecker_run(iplist):
    print(iplist)
    for ipinfo in iplist:
        print(yzPub(ipinfo))
        # 如果ip还可以用就更新 请求时间； 否则删除
        yzKeys,seconddata = yzPub(ipinfo)
        if yzKeys and seconddata < NormalTime:
            print(ipinfo," --> ip可用，更新到ip池")
            #r.zadd('ips:ips', {ipinfo:float(seconddata)} )
            r.zadd('ips:ips', float(seconddata),ipinfo )
        else:
            print(ipinfo," --> ip不可用")
            r.zrem('ips:ips',ipinfo)

#运行ipChecker
def go_ipChecker():
	while True:
		ipChecker()

#运行yzips
def go_yzips():
	#开5个线程
    PID_test_number = 2

    ps=[]
    # 创建子线程
    for i in range(PID_test_number):
        p=yzipThread(i)
        ps.append(p)
 
    # 开启线程
    for i in range(PID_test_number):
        ps[i].start()
 
    # 阻塞线程
    for i in range(PID_test_number):
        ps[i].join()
    print("线程终止")



if __name__=='__main__':
    #run_yzips()
    
    print('Parent process %s.' % os.getpid())
    # nimadaili 代理爬虫
    pid_nimadaili = Process(target=nimadaili.go_nimadaili_run, args=())
    #IP队列赛选进程
    pid_yzips = Process(target=go_yzips, args=())
    #IP池检查进程
    pid_ipChecker = Process(target=go_ipChecker, args=())
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

    '''
    p.start()
    p2.start()
    p3.start()

    p.join()
    p2.join()
    p3.join()
	'''
    print('Child process end.')
    
    #yzips()
    


