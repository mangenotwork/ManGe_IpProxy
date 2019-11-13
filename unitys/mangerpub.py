#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 

import re
from lxml import etree



class PubXpath():
	"""docstring for PubXpath"""

	@classmethod
	def get_html(cls,html,xpathcmd):
		html = str(html)
		all_list_datas = []
		datas = etree.HTML(html)
		info = datas.xpath(xpathcmd)
		print(info)
		t=""
		for i in range(len(info)):
			t += etree.tostring(info[i], encoding="utf-8", pretty_print=True).decode("utf-8")
		return t

	@classmethod
	def get_html_tonumber(cls,html,xpathcmd,startobj,endobj):
		html = str(html)
		all_list_datas = []
		datas = etree.HTML(html)
		info = datas.xpath(xpathcmd)
		print(info)
		t=""
		for i in info[startobj:endobj]:
			t += etree.tostring(i, encoding="utf-8", pretty_print=True).decode("utf-8")
		return t


	
#获取tr
def get_onlytr_data(html):
    reg = r"<tr>(.+?)</tr>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

def get_alltr_data(html):
    reg = r"(<tr>|<tr.+?>)(.+?)</tr>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#获取td
def get_onlytd_data(html):
    reg = r"<td>(.+?)</td>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

def get_alltd_data(html):
    reg = r"(<td>|<td.+?>)(.+?)</td>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

def get_propertytd_data(html):
    reg = r"<td.+?>(.+?)</td>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#获取table
def get_table(html):
    reg = r"<table.+?</table>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data
