__author__ = 'navaneeth'
from subprocess import Popen, PIPE
import config

def get_pid(process):
    fd = Popen(['ps', '-ef'], stdout = PIPE)
    p1 = Popen(['grep', process ], stdin= fd.stdout, stdout = PIPE)
    p2 = Popen(['grep', '-v', 'grep'], stdin= p1.stdout, stdout = PIPE)
    s = p2.stdout.readline().split()
    if s:
        return s[1]

def get_pid_spec(process):
    fd = Popen(['ps', '-ef'], stdout = PIPE)
    p1 = Popen(['grep', process ], stdin= fd.stdout, stdout = PIPE)
    p2 = Popen(['grep', '-v', 'grep'], stdin= p1.stdout, stdout = PIPE)
    p3 = Popen(['grep', '-v', '/bin/sh'], stdin= p2.stdout, stdout = PIPE)
    p4 = Popen(['grep', '-v', 'specinvoke'], stdin= p3.stdout, stdout = PIPE)
    p5 = Popen(['grep', '-v', 'runspec'], stdin= p4.stdout, stdout = PIPE)
    s = p5.stdout.readline().split()
    if s:
        return s[1]

def setup_config(process_1, process_2):
    config.csv_dir = "csv-automated-burst-all/"+ str(process_1[4:])+"-"+str(process_2[4:])+"/"
    config.map_pid_filename={str(process_1[4:]):{'filename':str(process_1[4:]), 'type':'spec'},
                             str(process_2[4:]):{'filename':str(process_2[4:]), 'type':'spec'}}
    config.result_dir="result-automated-burst-all/" + str(process_1[4:])+"-"+str(process_2[4:])+"/"

if __name__ == '__main__':
   print  get_pid_spec("lbm")