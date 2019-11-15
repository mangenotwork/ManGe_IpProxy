import os
import time
import subprocess
import unitys
import webbrowser as web




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
def ManGe_IpProxy_Redis():
    if unitys.Config.openRedis():
        print(unitys.OpenPluginRedisCMD())
        open_py(unitys.OpenPluginRedisCMD())
    else:
        print("不启用内置Redis")

#启动内置servers
def ManGe_IpProxy_Servers():
    if unitys.Config.openServer():
       open_py(unitys.OpenPluginServersCMD())
       time.sleep(1)
       web.open_new_tab("http://127.0.0.1:"+str(unitys.Config.serversPort()))
    else:
        print("不启用内置Servers")

