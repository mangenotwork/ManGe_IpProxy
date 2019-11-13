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

#get_kuaidaili_run()





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
# 		1~5







# 		qydaili
# 		http://www.qydaili.com/free/?action=china&page=1
# 		1~25







# 		ip3366
# 		http://www.ip3366.net/free/?stype=1&page=1
# 		1~6






# 		xicidaili
# 		https://www.xicidaili.com/nn/1
# 		1~2345








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

		time.sleep(10*60)






