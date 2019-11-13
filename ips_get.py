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

			#print(httptype)
			#print(ipnumber)

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







#		superfastip
#		http://www.superfastip.com/welcome/freeip/1  
#		/1  ~  /10





#		kxdaili
#		http://www.kxdaili.com/dailiip/1/1.html 
#		http://www.kxdaili.com/dailiip/2/1.html 







#		mimvp
#		https://proxy.mimvp.com/freesecret.php?proxy=in_hp&sort=&page=1 
#		https://proxy.mimvp.com/freesole.php
# 		https://proxy.mimvp.com/freeopen.php?proxy=in_hp&sort=&page=1







#		kuaidaili
#		https://www.kuaidaili.com/free/inha/1/ 
#		/1   ~   /100

