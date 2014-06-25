from fabric.api import *
import json
import urllib2
import shelve
import os
import socket, paramiko
import fabric.version
nodes = ['10.0.3.27']


if __name__ =='__main__':
    path= os.path.join(os.path.dirname(__file__), 'node_list_shelf.db')
    success_list = []
    if(os.path.exists(path)):
        os.remove(path)

    print nodes


# We can then specify host(s) and run the same commands across those systems
env.user = 'ubuntu'
env.password = 'ubuntu'
env.warn_only = True


def uptime():
    if _is_host_up(env.host, int(env.port)) is True:
        run("uptime")

def run_spec(app,result):
    if _is_host_up(env.host, int(env.port)) is True:
        with cd("cpu2006-installed"):
            run(". ./shrc; nohup runspec --config nav-gcc43.cfg --noreportable --nobuild --iterations=1 "+ app+" >" +result+ " &", pty=False)


def _is_host_up(host, port):
    # Set the timeout
    original_timeout = socket.getdefaulttimeout()
    new_timeout = 10
    socket.setdefaulttimeout(new_timeout)
    host_status = False
    try:
        transport = paramiko.Transport((host, port))
        host_status = True
    except:
        print('***Warning*** Host {host} on port {port} is down.'.format(
            host=host, port=port)
            )
    socket.setdefaulttimeout(original_timeout)
    return host_status
