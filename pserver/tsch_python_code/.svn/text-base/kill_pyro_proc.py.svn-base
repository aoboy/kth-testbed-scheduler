#!/usr/bin/env python


import sys, os
import subprocess
import traceback

proc2kill=[]

def killprocess(cmd):
    output =subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

    print 'here is the result....:', output

def get_processes(args):
    output=subprocess.Popen('ps -ux'.split(), stdout=subprocess.PIPE).communicate()[0]

    myproc=[]
    for a in output.split('\n'):
        if a.find('python') != -1 and a.find('kill_pyro_proc') == -1:
            for ag in args:
                if a.find(ag) != -1:
                    print a
                    myproc.append(a)

    myproc_num=[]
    for p in myproc:
        myproc_num.append(p.split()[1])

    killcmd='kill -9 '
    for p in myproc_num:
        print p,
        killcmd += str(p+' ')
        
    return killcmd


if __name__ == "__main__":

    try:
        print 'argv[0]', sys.argv[1:]
        args=sys.argv[1:]
        cmd=get_processes(args)
        killprocess(cmd)
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(44)
