__author__ = 'navaneeth'
from subprocess import Popen, PIPE
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

if __name__ == '__main__':
   print  get_pid_spec("lbm")