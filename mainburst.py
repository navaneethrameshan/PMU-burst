__author__ = 'navaneeth'
import ocperf
import subprocess
import util
from subprocess import PIPE
import os
import signal
import sys
import shutil
import config
from monitorcpu import *

map_pid_filehandle = {}

def remove_and_open_file():
    for key,values in config.map_pid_filename.items():
        if os.path.exists(values['filename']):
            os.remove(values['filename'])
        map_pid_filehandle[key] = open(values['filename'],'w+')


def write_to_file(filehandle, content):
    list1 = content.split("\n")
    #print list1
    filehandle.writelines(str(content))
    filehandle.write("\n")

def file_close():
    for key in map_pid_filehandle:
        map_pid_filehandle[key].close()


def measure(csvdir=None):

    csvdirname = config.csv_dir

    if csvdir:
        csvdirname = csvdir


    os.umask(0000)
    if os.path.exists(csvdirname):
        shutil.rmtree(csvdirname)
        os.makedirs(csvdirname)
    else:
        os.makedirs(csvdirname)

    count=0
    pid_list=[]
    atleast_one_running = True


    while 1:
        #print "PID_LIST: ", pid_list
        for value in pid_list:
            if value is not None:
                atleast_one_running = True

        if atleast_one_running == True:
            print "Atleast one process running"
            del pid_list[:]
            atleast_one_running = False

        else:
            print "No process running"
            return

        for key, values in config.map_pid_filename.items():
            print "Map Items: " ,config.map_pid_filename
            if values['type'] =='spec':
                pid = util.get_pid_spec(key)
                pid_list.append(pid)
            else:
                pid = util.get_pid(key)
                pid_list.append(pid)


            if pid:
                print "PID: ",key, pid
                try:
                    file_name = csvdirname+values['filename']+"_"+str(count)+".csv"
                    print file_name
                    if values['type'] =='affinity':
                        print "Monitoring " + values['filename']+ "on cores" + config.cores
                        vm_1= subprocess.call(["python", "ocperf.py", "stat", "-e", ','.join(config.counters),"-x,","-a",
                                            "-C", config.cores,"-o",file_name ,"sleep", str(config.monitor_period)])
                        vm_1.wait()
                    else:
                        vm_1= subprocess.call(["python", "ocperf.py", "stat", "-e", ','.join(config.counters),"-x,","-p",
                                            pid, "-o",file_name ,"sleep", str(config.monitor_period)])
                        vm_1.wait()
                    #print vm_1.stdout.read()
                    #write_to_file(map_pid_filehandle[key], vm_1.stdout.read())

                except:
                    continue

        usage = per_processor_usage()
        #CPU values
        file_name = csvdirname+"cpu.csv"
        file_handle = open(file_name,'a')

        file_handle.write(str(usage['1']) +'\n')

        file_handle.close()


        print "---------------------------------------------------"
        print "Done"
        print "---------------------------------------------------"
        count+=1


if __name__ == '__main__':
    measure()
