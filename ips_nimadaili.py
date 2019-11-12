#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 

import re
import time
from lxml import etree
from unitys import mangerequests as mreq
from unitys import mangerpub as rpub
from unitys import addtoredis as toredis

# http://www.nimadaili.com   nimadaili  IP 免费

#mreq.test()





#获取tr
def get_tr_data(html):
    reg = r"<tr.+?</tr>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#获取td
def get_td_data(html):
    reg = r"<td>(.+?)</td>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


def nimadaili_run():

	nimadaili_url = "http://www.nimadaili.com"

	datas1 = mreq.ManGeReq.geturl(nimadaili_url)
	#print(datas1)

	#//*[@id="overflow"]/table/tbody
	ipTbody = '//*[@id="overflow"]/table/tbody'

	ipTbody_datas = rpub.PubXpath.get_html(datas1,ipTbody)

	#print(len(get_tr_data(ipTbody_datas)))

	iplists = get_tr_data(ipTbody_datas)

	for ips in iplists:
		
		try:
			ipsinfos = get_td_data(ips)
			ipnumber = ipsinfos[0]
			iphttps = ipsinfos[2].split(",")[0]
			ipproxy = iphttps.lower()+"://"+ipnumber
			#print(ipnumber)
			#print(iphttps)
			print(ipproxy)
			toredis.add(ipproxy)
			#print("\n\n\n")
		except Exception as e:
			print("--")
		'''
		ipsinfos = get_td_data(ips)
		ipnumber = ipsinfos[0]
		iphttps = ipsinfos[2].split(",")[0]
		ipproxy = iphttps.lower()+"//"+ipnumber
		print(ipnumber)
		print(iphttps)
		print(ipproxy)
		print("\n\n\n")
		'''


#nimadaili_run()


def go_nimadaili_run():
	while 1:
		nimadaili_run()
		print("sleep...")
		time.sleep(10*60)

#go_nimadaili_run()

