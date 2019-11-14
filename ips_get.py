#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 

import re
import time
from lxml import etree
from unitys import mangerequests as mreq
from unitys import mangerpub as rpub
from unitys import addtoredis as toredis


#     crossincode 代理
#     https://lab.crossincode.com/proxy/
#
def get_crossincode_run():
	crossincode_url = "https://lab.crossincode.com/proxy/"
	crossincode_html_1 = mreq.ManGeReq.geturl(crossincode_url)
	#print(crossincode_html_1)
	#  /html/body/div/div/div[2]/div[2]/table/tbody
	crossincode_ipTbody = '/html/body/div/div/div[2]/div[2]/table'
	crossincode_ipTbody_datas = rpub.PubXpath.get_html(crossincode_html_1,crossincode_ipTbody)
	#print(crossincode_ipTbody_datas)
	crossincode_iplist = rpub.get_onlytr_data(crossincode_ipTbody_datas)
	#print(tttaaa)
	for crossincode_ipinfo in crossincode_iplist[1:]:
		##print(crossincode_ipinfo)
		#print("\n\n\n")
		crossincode_iptd = rpub.get_onlytd_data(crossincode_ipinfo)
		#print("ipnumber: ",crossincode_iptd[0])
		#print("port: ",crossincode_iptd[1])
		#print("type: ",crossincode_iptd[3])
		httptype = crossincode_iptd[3]
		ipnumber = crossincode_iptd[0]
		ipport = crossincode_iptd[1]
		iphttpval = httptype.split(',')
		if len(iphttpval) == 2:
			ipproxy1 = iphttpval[0].lower()+"://"+ipnumber+":"+ipport
			print(ipproxy1)
			ipproxy2 = iphttpval[1].lower()+"://"+ipnumber+":"+ipport
			print(ipproxy1)
			toredis.add(ipproxy1)
			toredis.add(ipproxy2)
		else:
			ipproxy1 = iphttpval[0].lower()+"://"+ipnumber+":"+ipport
			print(ipproxy1)
			toredis.add(ipproxy1)

def get_crossincode_ips():
	#加个延时，避免在一起爬取数据
	time.sleep(20)
	while 1:
		get_crossincode_run()
		print("sleep...")
		time.sleep(10*60)



#   xiladaili 代理
#   http://www.xiladaili.com/
#
def get_xiladaili_run():

	xiladaili_url = "http://www.xiladaili.com/"
	xiladaili_html_1 = mreq.ManGeReq.geturl(xiladaili_url)
	#print(xiladaili_html_1)
	#//*[@id="scroll"]/table/tbody
	#/html/body/div/div[3]/div[1]
	xiladaili_ipTbody1 = '/html/body/div/div[3]/div[@id="scroll"]'
	xiladaili_ipTbody_datas1 = rpub.PubXpath.get_html_tonumber(xiladaili_html_1,xiladaili_ipTbody1,0,3)
	#xiladaili_ipTbody2 = '/html/body/div/div[3]/div[2]/table/tbody'
	#xiladaili_ipTbody_datas2 = rpub.PubXpath.get_html(xiladaili_html_1,xiladaili_ipTbody2)
	#print(xiladaili_ipTbody_datas1)
	#print(xiladaili_ipTbody_datas2)
	xiladaili_ip_table = rpub.get_table(xiladaili_ipTbody_datas1)
	print(len(xiladaili_ip_table))
	for xiladaili_ip_lists in xiladaili_ip_table:
		#print(xiladaili_ip_lists)
		for xiladaili_ip_infos in rpub.get_onlytr_data(xiladaili_ip_lists)[2:]:
			#print(xiladaili_ip_infos)
			xiladaili_iptd = rpub.get_onlytd_data(xiladaili_ip_infos)
			httptype = xiladaili_iptd[2]
			ipnumber = xiladaili_iptd[0]
			iphttpval = httptype.split(',')
			if len(iphttpval) == 2:
				ipproxy1 = iphttpval[0].lower()+"://"+ipnumber
				print(ipproxy1)
				ipproxy2 = iphttpval[1].lower()+"://"+ipnumber
				print(ipproxy1)
				toredis.add(ipproxy1)
				toredis.add(ipproxy2)
			else:
				ipproxy1 = iphttpval[0].lower()+"://"+ipnumber
				print(ipproxy1)
				toredis.add(ipproxy1)

def get_xiladaili_ips():
	time.sleep(40)
	while 1:
		get_xiladaili_run()
		print("sleep...")
		time.sleep(10*60)



#		jiangxianli
#		http://ip.jiangxianli.com/?page=1   
#		page 1~3(原网站会更新，取前三页就好)
def get_jiangxianli_run():
	jiangxianli_pg=1
	while jiangxianli_pg<4:
		jiangxianli_url = "http://ip.jiangxianli.com/?page="+str(jiangxianli_pg)
		jiangxianli_html_1 = mreq.ManGeReq.geturl(jiangxianli_url)
		#print(jiangxianli_html_1)
		#/html/body/div/div[2]/div[1]/div[1]/table/tbody
		jiangxianli_ipTbody1 = '/html/body/div/div[2]/div[1]/div[1]/table/tbody'
		jiangxianli_ipTbody_datas1 = rpub.PubXpath.get_html(jiangxianli_html_1,jiangxianli_ipTbody1)
		#print(jiangxianli_ipTbody_datas1)
		for jiangxianli_ip_infos in rpub.get_onlytr_data(jiangxianli_ipTbody_datas1):
			#print(jiangxianli_ip_infos)
			jiangxianli_iptd = rpub.get_onlytd_data(jiangxianli_ip_infos)
			#print(jiangxianli_iptd[0],jiangxianli_iptd[1],jiangxianli_iptd[3])
			ipproxy = jiangxianli_iptd[3].lower()+"://"+jiangxianli_iptd[0]+":"+jiangxianli_iptd[1]
			print(ipproxy)
			toredis.add(ipproxy)
			#print("\n\n")
		jiangxianli_pg+=1

def get_jiangxianli_ips():
	time.sleep(60)
	while 1:
		get_jiangxianli_run()
		print("sleep...")
		time.sleep(10*60)



#		superfastip
#		http://www.superfastip.com/welcome/freeip/1  
#		/1  ~  /10
def get_superfastip_run():
	superfastip_pg = 1
	while superfastip_pg<11:
		superfastip_url = "http://www.superfastip.com/welcome/freeip/"+str(superfastip_pg)
		superfastip_html = mreq.ManGeReq.geturl(superfastip_url)
		#print(superfastip_html)
		#/html/body/div[3]/div/div/div[2]/div/table/tbody
		superfastip_ipTbody = '/html/body/div[3]/div/div/div[2]/div/table/tbody'
		superfastip_ipTbody_datas = rpub.PubXpath.get_html(superfastip_html,superfastip_ipTbody)
		#print(superfastip_ipTbody_datas)
		#print(len(rpub.get_alltr_data(superfastip_ipTbody_datas)))
		for superfastip_ip_infos in rpub.get_alltr_data(superfastip_ipTbody_datas):
			#print(superfastip_ip_infos)
			superfastip_iptd = rpub.get_onlytd_data(superfastip_ip_infos)
			ipproxy = superfastip_iptd[4].lower()+"://"+superfastip_iptd[0]+":"+superfastip_iptd[1]
			print(ipproxy)
			#print("\n\n")
			toredis.add(ipproxy)
		superfastip_pg+=1



#		kxdaili
#		http://www.kxdaili.com/dailiip/1/1.html 
# 		/1  ~  /6
#		http://www.kxdaili.com/dailiip/2/1.html 
# 		/1  ~ /4
def kxdaili_get_ip(html):
	kxdaili_1_ipTbody = '//div[@class="hot-product-content"]/table/tbody'
	kxdaili_1_ipTbody_datas = rpub.PubXpath.get_html(html,kxdaili_1_ipTbody)
	#print(kxdaili_1_ipTbody_datas)
	for kxdaili_1_ip_infos in rpub.get_alltr_data(kxdaili_1_ipTbody_datas):
		kxdaili_1_iptd = rpub.get_onlytd_data(kxdaili_1_ip_infos)
		#print(kxdaili_1_iptd)
		iphttpval = kxdaili_1_iptd[3].split(',')
		if len(iphttpval) == 2:
			ipproxy1 = iphttpval[0].lower()+"://"+kxdaili_1_iptd[0]+":"+kxdaili_1_iptd[1]
			ipproxy2 = iphttpval[1].lower()+"://"+kxdaili_1_iptd[0]+":"+kxdaili_1_iptd[1]
			print(ipproxy1)
			print(ipproxy2)
			toredis.add(ipproxy1)
			toredis.add(ipproxy2)
		else:
			ipproxy1 = iphttpval[0].lower()+"://"+kxdaili_1_iptd[0]+":"+kxdaili_1_iptd[1]
			print(ipproxy1)
			toredis.add(ipproxy1)

def get_kxdaili_run():
	kxdaili_1_pg = 1
	kxdaili_2_pg = 1
	while kxdaili_1_pg < 7:
		kxdaili_1_url = "http://www.kxdaili.com/dailiip/1/"+str(kxdaili_1_pg)+".html"
		kxdaili_1_html = mreq.ManGeReq.geturl(kxdaili_1_url)
		kxdaili_get_ip(kxdaili_1_html)
		kxdaili_1_pg+=1
	while kxdaili_2_pg < 5:
		kxdaili_2_url = "http://www.kxdaili.com/dailiip/2/"+str(kxdaili_2_pg)+".html"
		kxdaili_2_html = mreq.ManGeReq.geturl(kxdaili_2_url)
		kxdaili_get_ip(kxdaili_2_html)
		kxdaili_2_pg+=1



#		mimvp
#		https://proxy.mimvp.com/freesecret.php
#		https://proxy.mimvp.com/freesole.php
# 		https://proxy.mimvp.com/freeopen.php?proxy=in_hp
# 		https://proxy.mimvp.com/freeopen.php?proxy=in_tp
# 		https://proxy.mimvp.com/freeopen.php?proxy=out_hp
# 		https://proxy.mimvp.com/freeopen.php?proxy=out_tp
#  		这个代理可以拿到 Socket类型的，后面开发

#验证码需要图像识别技术， 后面开发
'''
mimvp_url = "https://proxy.mimvp.com/freesecret.php"
mimvp_html = mreq.ManGeReq.geturl(mimvp_url)
#print(mimvp_html)
#//*[@id="mimvp-body"]/div/table/tbody
mimvp_ipTbody = '//*[@id="mimvp-body"]/div/table/tbody'
mimvp_ipTbody_datas = rpub.PubXpath.get_html(mimvp_html,mimvp_ipTbody)
#print(mimvp_ipTbody_datas)
for mimvp_ip_infos in rpub.get_alltr_data(mimvp_ipTbody_datas):
	#print(mimvp_ip_infos)
	mimvp_iptd = rpub.get_propertytd_data(mimvp_ip_infos)
	print(mimvp_iptd)
	iphttpval = mimvp_iptd[3].split('/')
	if len(iphttpval) == 2:
		ipproxy1 = iphttpval[0].lower()+"://"+mimvp_iptd[1]+":"+mimvp_iptd[0]
		ipproxy2 = iphttpval[1].lower()+"://"+mimvp_iptd[1]+":"+mimvp_iptd[0]
		print(ipproxy1)
		print(ipproxy2)
		toredis.add(ipproxy1)
		toredis.add(ipproxy2)
	else:
		ipproxy1 = iphttpval[0].lower()+"://"+mimvp_iptd[1]+":"+mimvp_iptd[0]
		print(ipproxy1)
		toredis.add(ipproxy1)
'''



#		kuaidaili
#		https://www.kuaidaili.com/free/inha/1/ 
#		/1   ~   /1000
def get_kuaidaili_run():
	kuaidaili_pg = 1
	while kuaidaili_pg < 1234:
		kuaidaili_url = "https://www.kuaidaili.com/free/inha/"+str(kuaidaili_pg)+"/"
		#kuaidaili_html = mreq.ManGeReq.geturl_proxy(kuaidaili_url)
		kuaidaili_html = mreq.ManGeReq.geturl(kuaidaili_url)
		#print(kuaidaili_html)
		#//*[@id="list"]/table/tbody
		kuaidaili_ipTbody = '//*[@id="list"]/table/tbody'
		kuaidaili_ipTbody_datas = rpub.PubXpath.get_html(kuaidaili_html,kuaidaili_ipTbody)
		#print(kuaidaili_ipTbody_datas)
		for kuaidaili_ip_infos in rpub.get_alltr_data(kuaidaili_ipTbody_datas):
			kuaidaili_iptd = rpub.get_propertytd_data(kuaidaili_ip_infos)
			#print(kuaidaili_iptd)
			ipproxy = kuaidaili_iptd[3].lower()+"://"+kuaidaili_iptd[0]+":"+kuaidaili_iptd[1]
			print(ipproxy)
			toredis.add(ipproxy)
		kuaidaili_pg+=1
		time.sleep(1)

def get_kuaidaili_ips():
	time.sleep(60)
	while 1:
		get_kuaidaili_run()
		print("sleep...")
		time.sleep(10*60)



#  w66ip
#  http://www.66ip.cn/1.html
#  1~1234
def get_w66ip_run():
	w66ip_pg = 1
	while w66ip_pg < 1234:
		w66ip_url = "http://www.66ip.cn/"+str(w66ip_pg)+".html"
		#w66ip_html = mreq.ManGeReq.geturl_proxy(w66ip_url)
		w66ip_html = mreq.ManGeReq.geturl(w66ip_url)
		#print(w66ip_html)
		#//*[@id="main"]/div/div[1]/table/tbody
		w66ip_ipTbody = '//*[@id="main"]/div/div[1]/table'
		w66ip_ipTbody_datas = rpub.PubXpath.get_html(w66ip_html,w66ip_ipTbody)
		#print(w66ip_ipTbody_datas)
		for w66ip_ip_infos in rpub.get_onlytr_data(w66ip_ipTbody_datas)[2:]:
			#print(w66ip_ip_infos)
			w66ip_iptd = rpub.get_onlytd_data(w66ip_ip_infos)
			ipproxy_1 = "http://"+w66ip_iptd[0]+":"+w66ip_iptd[1]
			ipproxy_2 = "https://"+w66ip_iptd[0]+":"+w66ip_iptd[1]
			print(ipproxy_1)
			print(ipproxy_2)
			toredis.add(ipproxy_1)
			toredis.add(ipproxy_2)
			#print("\n\n\n")
		time.sleep(1)
		w66ip_pg+=1



# 		w89ip
# 		http://www.89ip.cn/index_1.html
# 		1~ 6
def get_w89ip_run():
	w89ip_pg = 1
	while w89ip_pg<7:
		w89ip_url = "http://www.89ip.cn/index_"+str(w89ip_pg)+".html"
		w89ip_html = mreq.ManGeReq.geturl(w89ip_url)
		#print(w89ip_html)
		#/html/body/meta"utf-8"/div[4]/div[1]/div/div[1]/table/tbody
		w89ip_ipTbody = '//table[@class="layui-table"]/tbody'
		w89ip_ipTbody_datas = rpub.PubXpath.get_html(w89ip_html,w89ip_ipTbody)
		#print(w89ip_ipTbody_datas)
		for w89ip_ip_infos in rpub.get_onlytr_data(w89ip_ipTbody_datas):
			#print(w89ip_ip_infos)
			w89ip_iptd = rpub.get_onlytd_data(w89ip_ip_infos)
			#print(w89ip_iptd)
			ipnumber = re.sub('(\n\t\t\t)|(\t\t)','',w89ip_iptd[0])
			port = re.sub('(\n\t\t\t)|(\t\t)','',w89ip_iptd[1])
			ipproxy_1 = "http://"+ipnumber+":"+port
			ipproxy_2 = "https://"+ipnumber+":"+port
			print(ipproxy_1)
			print(ipproxy_2)
			toredis.add(ipproxy_1)
			toredis.add(ipproxy_2)
		time.sleep(1)
		w89ip_pg+=1



# 		json89ip
#		http://www.89ip.cn/tqdl.html?num=1000
#
def get_json89ip_run():
	json89ip_url = "http://www.89ip.cn/tqdl.html?num=1000"
	json89ip_html = mreq.ManGeReq.geturl(json89ip_url)
	#print(json89ip_html)
	#/html/body/meta"utf-8"/div[4]/div[1]/div/div
	json89ip_ipTbody = '//div[@class="fly-panel"]/div/text()'
	json89ip_ipTbody_datas = rpub.PubXpath.get_htmltxt(json89ip_html,json89ip_ipTbody)
	#print(json89ip_ipTbody_datas)
	ipproxy_1 = re.sub('\n','',json89ip_ipTbody_datas[0])
	print(ipproxy_1.split()[0])
	toredis.add("http://"+ipproxy_1.split()[0])
	toredis.add("https://"+ipproxy_1.split()[0])
	for json89ip_ip_infos in json89ip_ipTbody_datas[1:-4]:
		#print(json89ip_ip_infos)
		toredis.add(json89ip_ip_infos)
		ipproxy_1 = "http://"+json89ip_ip_infos
		ipproxy_2 = "https://"+json89ip_ip_infos
		print(ipproxy_1)
		print(ipproxy_2)
		toredis.add(ipproxy_1)
		toredis.add(ipproxy_2)



# 		qydaili
# 		http://www.qydaili.com/free/?action=china&page=1
# 		1~10
def get_qydaili_run():
	qydaili_pg = 1
	while qydaili_pg<11:
		qydaili_url = "http://www.qydaili.com/free/?action=china&page="+str(qydaili_pg)
		qydaili_html = mreq.ManGeReq.geturl(qydaili_url)
		#print(qydaili_html)
		#//*[@id="content"]/section/div[2]/table/tbody
		qydaili_ipTbody = '//div[@class="container"]/table/tbody'
		qydaili_ipTbody_datas = rpub.PubXpath.get_html(qydaili_html,qydaili_ipTbody)
		#print(qydaili_ipTbody_datas)
		#print(rpub.get_onlytr_data(qydaili_ipTbody_datas))
		for qydaili_ip_infos in rpub.get_onlytr_data(qydaili_ipTbody_datas):
			qydaili_iptd = rpub.get_propertytd_data(qydaili_ip_infos)
			#print(qydaili_iptd)
			ipproxy = qydaili_iptd[3].lower()+"://"+qydaili_iptd[0]+":"+qydaili_iptd[1]
			print(ipproxy)
			toredis.add(ipproxy)
		time.sleep(1)
		qydaili_pg+=1



# 		ip3366
# 		http://www.ip3366.net/free/?stype=1&page=1
# 		1~6
def get_ip3366_run():
	ip3366_pg = 1
	while ip3366_pg<7:
		ip3366_url = "http://www.ip3366.net/free/?stype=1&page="+str(ip3366_pg)
		ip3366_html = mreq.ManGeReq.geturl(ip3366_url)
		#print(ip3366_html)
		#//div[@id="list"]/table/tbody
		ip3366_ipTbody = '//div[@id="list"]/table/tbody'
		ip3366_ipTbody_datas = rpub.PubXpath.get_html(ip3366_html,ip3366_ipTbody)
		#print(ip3366_ipTbody_datas)
		for ip3366_ip_infos in rpub.get_onlytr_data(ip3366_ipTbody_datas):
			ip3366_iptd = rpub.get_onlytd_data(ip3366_ip_infos)
			#print(ip3366_iptd)
			ipproxy = ip3366_iptd[3].lower()+"://"+ip3366_iptd[0]+":"+ip3366_iptd[1]
			print(ipproxy)
			toredis.add(ipproxy)
		ip3366_pg+=1
		time.sleep(1)



# 		xicidaili
# 		https://www.xicidaili.com/nn/1
# 		1~2345
def get_xicidaili_run():
	xicidaili_pg = 1
	while xicidaili_pg<2345:
		xicidaili_url = "https://www.xicidaili.com/nn/"+str(xicidaili_pg)
		xicidaili_html = mreq.ManGeReq.geturl(xicidaili_url)
		#print(xicidaili_html)
		#//table[@id="ip_list"]/tbody
		xicidaili_ipTbody = '//div[@id="body"]/table'
		xicidaili_ipTbody_datas = rpub.PubXpath.get_html(xicidaili_html,xicidaili_ipTbody)
		#print(xicidaili_ipTbody_datas)
		for xicidaili_ip_infos in rpub.get_alltr_data(xicidaili_ipTbody_datas)[1:]:
			#print(xicidaili_ip_infos)
			xicidaili_iptd = rpub.get_onlytd_data(xicidaili_ip_infos)
			#print(xicidaili_iptd)
			ipproxy = xicidaili_iptd[3].lower()+"://"+xicidaili_iptd[0]+":"+xicidaili_iptd[1]
			print(ipproxy)
			toredis.add(ipproxy)
			#print("\n\n")
		xicidaili_pg+=1
		time.sleep(1)

def get_xicidaili_ips():
	time.sleep(60)
	while 1:
		get_xicidaili_run()
		print("sleep...")
		time.sleep(10*60)



# 		iphai
# 		http://www.iphai.com/free/ng
# 		http://www.iphai.com/free/wg



#	 	goubanjia
#		http://www.goubanjia.com/
#



#
#
#






def get_ip_run():
	while True:
		get_jiangxianli_run()
		time.sleep(10)
		get_xiladaili_run()
		time.sleep(10)
		get_crossincode_run()
		time.sleep(10)
		get_superfastip_run()
		time.sleep(10)
		get_kxdaili_run()
		time.sleep(10)
		get_w66ip_run()
		time.sleep(10)
		get_w89ip_run()
		time.sleep(10)
		get_json89ip_run()
		time.sleep(10)
		get_qydaili_run()
		time.sleep(10)
		get_ip3366_run()

		time.sleep(10*60)






