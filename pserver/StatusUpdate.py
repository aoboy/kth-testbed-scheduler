#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wave import Error
import os
import time
import Queue
import threading
import random
import shlex
import sys
import subprocess
from threading import Thread
import math

scmd = 'scp gonga@wsntestbed.s3.kth.se:/home/gonga/Task3Log.out .'

def executeCmd(commandLine):
    #print commandLine
    args = shlex.split(commandLine)
    #print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print 'ERROR!'
        print stdout
        print stderr
        exit(-1)
    return stdout

def sleepApp(deltaT):
    for n in range(0, 4*deltaT):
        time.sleep(0.25)

def polServer(cmd):

    while True:
        executeCmd(cmd)
        sleepApp(5)

if __name__ == '__main__':
    polServer(scmd)


