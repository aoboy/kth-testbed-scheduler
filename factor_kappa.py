#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#This is the file converter from .TXT to a readable data structure in XML/1's
#Another Modif
#Test

import os,sys,  getopt, getpass
import os.path, time
import traceback
import pexpect
import math
import numpy
from numpy import *

rootdir =os.path.abspath("./")
files=[]
channels=[]


def get_files_dir():
        global files
        files = []
        for a in os.listdir(rootdir):
		if not os.path.isdir(os.path.join(rootdir,a)):
			#if a.find('Nchannels') != -1 and  a.find('link0-') == -1:
                        if a.find('SEQ16Bin') != -1:
                                if a.find('.TXT') != -1 and a.find('?') == -1:
                                    files.append(a)
                                    channels.append(a[(a.find('Pool')+4):a.find('li')])
        return files


def parse_files():

    n_chs=0
    for f, ch in zip(files, channels):
        n_chs = int(ch)
        data = open(os.path.join(rootdir, f),'rb').read()

        row_idx = 0
        column_idx = 0
        
        print 'data_length:',len(data)
        
        data=data.replace(' ', '')

        data_len = len(data.replace('\n', ''))
        n_columns = 640
        print 'data_len:', len(data.replace('\n', ''))
       
        data_vec=[]
       
        for val in list(data):
            #print val,
            if(val != '\n'):
                data_vec.append(val)
   
        link_prob         = zeros([1, n_chs], float)
        prob_xy           = zeros([1, n_chs], float)
        link_prob_counter = zeros([1, n_chs], int)
        prob_xy_counter   = zeros([1, n_chs], int)
        sigma_x           = zeros([1, n_chs], float)
        ro_xy             = zeros([1, n_chs], float)
        ro_min            = zeros([1, n_chs], float)
        ro_max            = zeros([1, n_chs], float)
        kappa_factor      = zeros([1, n_chs], float)

        n = 0
        a = 0
        b = 0
        for n in range(0, len(data_vec)):
            #print val
            link_prob_counter[0][n%n_chs] = link_prob_counter[0][n%n_chs] + int(data_vec[n])

            if (n + 1) < len(data_vec):

                 if int(data_vec[n]) == 1 and  int(data_vec[n+1]) == 1:
                    prob_xy_counter[0][n%n_chs] = prob_xy_counter[0][n%n_chs] + 1
      
        print link_prob_counter
        print prob_xy_counter

        n = 0
        for a, b in zip(link_prob_counter[0], prob_xy_counter[0]):
            #print a, b
            link_prob[0][n] = float(a)/n_columns
            prob_xy[0][n]   = float(b)/n_columns

            sigma_x[0][n]   = math.sqrt(link_prob[0][n]*(1 - link_prob[0][n]))
          
            n = n + 1

        n = 0
        #for a, b in zip(link_prob[0], prob_xy[0]):
        #    print a, b

        print 'sigma:', sigma_x[0]
        print 'link_prob:', link_prob[0]
        print 'prob_xy:', prob_xy[0]

        for n in range(0, len(link_prob[0])):
            
            if n+1 < len(link_prob[0]):

                temp_lprob = link_prob[0][n]*link_prob[0][n+1]
                temp_sigma = sigma_x[0][n]*sigma_x[0][n+1]
                
                #print '->',temp_sigma

                if temp_sigma != 0:
                    ro_xy[0][n] = (prob_xy[0][n] - link_prob[0][n]*link_prob[0][n+1])/temp_sigma
        
                    temp_ro_max = (min(link_prob[0][n], link_prob[0][n+1]) - link_prob[0][n]*link_prob[0][n+1])/temp_sigma
                    ro_max[0][n] = temp_ro_max

                    temp_ro_min = (-1)*temp_lprob/temp_sigma

                    if (link_prob[0][n] + link_prob[0][n+1]) <= 1:
                        ro_min[0][n] = int(-1)*link_prob[0][n]*link_prob[0][n+1]
                    else:
                        temp_ro_min = (link_prob[0][n] + link_prob[0][n+1] - 1 - link_prob[0][n]*link_prob[0][n+1])/temp_sigma
                        ro_min[0][n] = temp_ro_min

                    if ro_xy[0][n] > 0:
                        kappa_factor[0][n] = ro_xy[0][n]/ro_max[0][n]
                    if ro_xy[0][n] < 0:
                        kappa_factor[0][n] = int(-1)*ro_xy[0][n]/ro_min[0][n]
                    if ro_xy[0][n] == 0:
                        kappa_factor[0][n] = 0
                else:
                    ro_xy[0][n] = 0

        print 'ro_xy:',ro_xy[0]
        print 'ro_max:',ro_max[0],'\nro_min:',ro_min[0]
       
        print '>>>kappa_factor:',kappa_factor[0]
        

if __name__ == "__main__":

    try:
        #main()
        filesdir=get_files_dir()
        #for f in filesdir:
        #    print 'file :',f
        parse_files()
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(44)