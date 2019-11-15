# -*- coding:utf-8 -*-
import os
import redis
import configparser


def ManGe_IpProxy_Path():
	return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def ManGe_IpProxy_Conf_Path():
	return ManGe_IpProxy_Path()+"\\main.conf"

def PluginRedisPath():
	return ManGe_IpProxy_Path()+"\\Redis-x64-3.2.100\\"

def OpenPluginRedisCMD():
	return PluginRedisPath()+"redis-server.exe "+PluginRedisPath()+"redis.windows.conf"

def OpenPluginServersCMD():
	return "python "+ManGe_IpProxy_Path()+"\\unitys\\ipservers.py"


#读取配置文件
class Config():

	@staticmethod
	def get_config( sector, item):
		config = configparser.ConfigParser()
		config.read(ManGe_IpProxy_Conf_Path(), encoding="utf-8")
		value = config.get(sector, item)
		return value

	@staticmethod
	def redisHost():
		return Config.get_config('RedisInfo', 'host')

	@staticmethod
	def redisPort():
		return Config.get_config('RedisInfo', 'port')

	@staticmethod
	def redisDB():
		return Config.get_config('RedisInfo', 'db')

	@staticmethod
	def ipQueue():
		return Config.get_config('IPPoolInfo', 'ipqueue')

	@staticmethod
	def ipPool():
		return Config.get_config('IPPoolInfo', 'ippools')

	@staticmethod
	def ipQueueMaxLen():
		return int(Config.get_config('IPPoolInfo', 'ipqueueMaxLen'))

	@staticmethod
	def ipQueueMemoryProtection_Time():
		return int(Config.get_config('IPPoolInfo', 'ipQueueMemoryProtection_Time'))
	
	@staticmethod
	def ipPoolMaxLen():
		return int(Config.get_config('IPPoolInfo', 'ipPoolMaxLen'))
	
	@staticmethod
	def jcUrl():
		return Config.get_config('ManGeIPPool', 'jcUrl')

	@staticmethod
	def normalTime():
		return float(Config.get_config('ManGeIPPool', 'normalTime'))

	@staticmethod
	def yzipThreadNumber():
		return int(Config.get_config('ManGeIPPool', 'yzips_ThreadNumber'))

	@staticmethod
	def openRedis():
		if Config.get_config('GoInit', 'openredis') in ["true","True","TRUE"]:
			return True
		else:
			return False
	
	@staticmethod
	def openServer():
		if Config.get_config('GoInit', 'openserver') in ["true","True","TRUE"]:
			return True
		else:
			return False

	@staticmethod
	def serversPort():
		return int(Config.get_config('GoInit', 'serversport'))
	

def RedisConPool():
	return redis.ConnectionPool(host = Config.redisHost(),
								port = Config.redisPort(), 
								db = Config.redisDB(),
								password = None,
								decode_responses = True)