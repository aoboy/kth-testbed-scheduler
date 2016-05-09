#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time
import traceback
import pexpect
import shlex
import subprocess
#KTH - The Royal Institute of Technology
# Automatic Control Lab
#  Prof. Mikael Johansson's Group
#    Author: Antonio Gonga (El-Guapo Angoleno): gonga@kth.se, PhD Student
#Parser file: This file is used to parse data files into a readable format to MATLAB...it
#             also creats XML files.

import NetworkStatistics
from NetworkStatistics import *


ch_cache = {}
ch_cache['11']='11'
ch_cache['12']='12'
ch_cache['13']='13'
ch_cache['14']='14'
ch_cache['15']='15'
ch_cache['16']='16'
ch_cache['17']='17'
ch_cache['18']='18'
ch_cache['19']='19'
ch_cache['20']='20'
ch_cache['21']='21'
ch_cache['22']='22'
ch_cache['23']='23'
ch_cache['24']='24'
ch_cache['25']='25'
ch_cache['26']='26'
ch_cache['1520']='15.20'
ch_cache['15202526']='15.20.25.26'

ch_cache['Tsch2']  = '26.17'
ch_cache['Tsch4']  = '26.22.17.13'
ch_cache['Tsch8']  = '26.19.12.20.24.22.17.13'
ch_cache['Tsch12'] = '26.19.12.20.24.16.23.18.25.22.17.13'
ch_cache['Tsch16'] = '26.19.12.20.24.16.23.18.25.14.21.11.15.22.17.13'

rootdir =os.path.abspath("./")
directories = []

ListOfTrials = []
#src_id = fname[(idx+4):-4].split('-')[0]
class Trial:
    def __init__(self, name, path):
        self.name = name
        self.path = path        
        self.avgBeta  = []
        self.avgKappa = []
        self.avgPrSuc = []
        self.ListOfStatistics = []

def load_files_task1(pathFiles):
    directories = os.listdir(os.path.abspath(pathFiles))
    directories.sort()

    for dir in directories:
        if os.path.isdir(os.path.join(pathFiles, dir)):
            if dir.find('Trial') != -1:
                trial = Trial(dir, os.path.join(pathFiles, dir))                

                for dir in directories:
                    if  os.path.isdir(os.path.join(rootdir,dir)):
                        if dir.find('Ch') != -1 and dir.find('.') == -1:
                            statsId = dir[dir.find('Ch')+2]
                            chIDs = [int(statsId)]
                            netStats = NetworkStatistics(dir, 32, 16,  chIDs)

                            for fname in os.listdir(os.path.join(rootdir,dir)):
                                if fname.find('link') != -1 and  fname.find('link0-') == -1:
                                    if fname.find('.TXT') != -1 and fname.find('?') == -1:

                                        fileName=''
                                        fileName = os.path.join(rootdir, dir+'/'+fname)

                                        netStats.ListOfFiles.append(fileName)
                            #initializes the list of nodes
                            netStats.createNodes()
                            #append this stats
                            trial.ListOfStatistics.append(netStats)
                        elif dir.find('Tsch') != -1 and dir.find('.') == -1:
                            chIDs = []
                            statsId = dir[dir.find('Tsch')+4]
                            if statsId == '1':
                                chIDs = ch_cache['1520'].split('.')
                            elif statsId == '2':
                                chIDs = ch_cache['15202526'].split('.')

                            for idx, v in enumerate(chIDs):
                                chIDs[idx] = int(v)

                            netStats = NetworkStatistics(dir, 32, 16,  chIDs)
                            for fname in os.listdir(os.path.join(rootdir,dir)):
                                if fname.find('link') != -1 and  fname.find('link0-') == -1:
                                    if fname.find('.TXT') != -1 and fname.find('?') == -1:

                                        fileName=''
                                        fileName = os.path.join(rootdir, dir+'/'+fname)

                                        netStats.ListOfFiles.append(fileName)
                            #initializes the list of nodes
                            netStats.createNodes()
                            #append this stats
                            trial.ListOfStatistics.append(netStats)
                ListOfTrials.append(trial)
    return ListOfTrials

def load_files_task21(pathFiles):
    directories = os.listdir(os.path.abspath(pathFiles))
    directories.sort()

    ListOfStatistics = []

    print 'Parsing Stats for Task 21'

    for dir in directories:
        if  os.path.isdir(os.path.join(pathFiles,dir)):
            if dir.find('Ch') != -1 and dir.find('.') == -1:
                statsId = dir[dir.find('Ch')+2]
                chIDs = [int(statsId)]
                netStats = NetworkStatistics(dir, 32, 16,  chIDs)

                for fname in os.listdir(os.path.join(pathFiles,dir)):
                    if fname.find('link') != -1 and  fname.find('link0-') == -1:
                        if fname.find('.TXT') != -1 and fname.find('?') == -1:

                            fileName=''
                            fileName = os.path.join(pathFiles, dir+'/'+fname)

                            netStats.ListOfFiles.append(fileName)
                #initializes the list of nodes
                netStats.createNodes()
                #append this stats
                ListOfStatistics.append(netStats)            

    return ListOfStatistics

def load_files_task22(pathFiles):
    directories = os.listdir(os.path.abspath(pathFiles))
    directories.sort()

    ListOfStatistics = []

    print 'Parsing Stats for Task 22'
    for dir in directories:
        if  os.path.isdir(os.path.join(pathFiles,dir)):
            if dir.find('Tsch') != -1 and dir.find('.') == -1:
                chIDs = []
                statsId = dir
                chIDs = ch_cache[dir].split('.')
               
                for idx, v in enumerate(chIDs):
                    chIDs[idx] = int(v)

                netStats = NetworkStatistics(dir, 32, 16,  chIDs)
                for fname in os.listdir(os.path.join(pathFiles,dir)):
                    if fname.find('link') != -1 and  fname.find('link0-') == -1:
                        if fname.find('.TXT') != -1 and fname.find('?') == -1:

                            fileName=''
                            fileName = os.path.join(pathFiles, dir+'/'+fname)

                            netStats.ListOfFiles.append(fileName)
                #initializes the list of nodes
                netStats.createNodes()
                #append this stats
                ListOfStatistics.append(netStats)

    return ListOfStatistics