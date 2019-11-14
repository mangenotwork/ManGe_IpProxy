import os
import time
import subprocess


def ManGe_IpProxy_Path():
	return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



def open_py(args):
    open_py_p = subprocess.Popen(args, shell=True)
    #print("Run "+str(args)+" PID : "+str(open_py_p.pid))
    #print("[debug] ++++ PID ++++ = "+str(open_py_p.pid))
    #all_line = open_py_p.stdout.read()
    #print("[PID Debug] open_py() = "+all_line.decode('utf-8'))
    time.sleep(1)
    open_py_p.kill()
    return open_py_p.pid



#开启 Redis
def start_redis():
    Redis_path = Man_API_Path+"\\Redis-x64-3.2.100\\"
    start_redis_cmd = Redis_path+"redis-server.exe "+Redis_path+"redis.windows.conf"
    print(start_redis_cmd)
    open_py(start_redis_cmd)


def ManGe_IpProxy_Servers():
	path = ManGe_IpProxy_Path()+"\\unitys\\ipapi.py"
	print(path)
	open_py("python "+path)

