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


def get_files_dir():
        global files
        files = []
        for a in os.listdir(rootdir):
		if not os.path.isdir(os.path.join(rootdir,a)):
			#if a.find('Nchannels') != -1 and  a.find('link0-') == -1:
                        if a.find('ones') != -1:
                                if a.find('.txt') != -1 and a.find('?') == -1:
                                    files.append(a)
        return files


def parse_files():

    for f in files:
        data = open(os.path.join(rootdir, f),'rb').read()
        probs  = zeros([2,25], int)
        #prob_x = zeros([1,16], float)
        #prob_xy= zeros([1,16], float)

        row_idx = 0
        column_idx = 0
        #print data
        for row in data.split('\n'):
           if len(row) != 0:
             
                row_idx = 0
                for val in list(row):

                    probs[row_idx][column_idx]= val #row[col]
                    row_idx=int(row_idx+1)
                  
                column_idx = int(column_idx + 1)

        #print sum(probs[15])
        print probs
        prob_x  =[]
        prob_xy =[]
        sigma_x =[]
        ro_xy   =[]
        ro_min  =[]
        ro_max  =[]
        kappa_factor=[]
        for n in range(0, 2):
            #print float(sum(probs[n]))/50.0
            prob=float(sum(probs[n]))/25
            prob_x.append(prob)
            sigma_=math.sqrt(prob*(1-prob))
            sigma_x.append(sigma_)

            nb=0
            if n < 1:
                nb= n +1
            else:
                nb = 0
            counter_xy_1=0
            for a, b in zip(probs[n], probs[nb]):
                if  a == b:
                    counter_xy_1 = int(counter_xy_1 +1)

            prob_xy.append(float(counter_xy_1)/25.0)

        print 'prob_chs:',prob_x
        #print '\n'
        print 'sigma_x', sigma_x
        print 'prob_xy:', prob_xy

        #calculate the cross-correlation index
        for n in range(0, 2):
            nb=0
            if n < 1:
                nb = n + 1
            else:
                nb = 0
            temp_sigma_xy = sigma_x[n]*sigma_x[nb]
            if temp_sigma_xy != 0:
                #calculate cross_xy
                temp_ro = (prob_xy[n] - prob_x[n]*prob_x[nb])/temp_sigma_xy
                ro_xy.append(temp_ro)

                #calculate crox_xymax
                temp_pxy = prob_x[n]*prob_x[nb]
                ro_max.append((min(prob_x[n], prob_x[nb]) -  temp_pxy)/temp_sigma_xy)

                #calculate ro_min
                temp_val=0
                if (prob_x[n] + prob_x[nb]) <= 1:
                    temp_val = int(-1)*temp_pxy/temp_sigma_xy
                    ro_min.append(temp_val)
                else:
                    temp_val = (prob_x[n] + prob_x[nb] - 1 - temp_pxy)/temp_sigma_xy
                    ro_min.append(temp_val)

                temp_kappa = 0
                if (temp_ro > 0):
                    #print 'here',ro_xy[n], ro_max[n]
                    temp_kappa = temp_ro/ro_max[n]
                    kappa_factor.append(temp_kappa)
                if (temp_ro < 0):
                    temp_kappa = int(-1)*float(temp_ro)/temp_val
                    kappa_factor.append(temp_kappa)
            else:
                ro_xy.append(0)
                kappa_factor.append(0)

            #calculate Kappa_Factor
            #temp_kappa = 0
            #if (ro_xy[n] > 0):
            #    #print 'here',ro_xy[n], ro_max[n]
            #    temp_kappa = ro_xy[n]/ro_max[n]
            #    kappa_factor.append(temp_kappa)
            #if (ro_xy[n] < 0):
            #    temp_kappa = int(-1)*float(ro_xy[n])/ro_min[n]
            #    kappa_factor.append(temp_kappa)
            #if (ro_xy[n] == 0):
            #    kappa_factor.append(0)
            
            #temp_sigma_xy = 0
        #for n in range(0, 16):
            #print 'P[',n,']=',prob_x[n]/50
               
        #print probs
        print 'Results\n-------------------------------'
        print 'ro_xy:',ro_xy
        print 'ro_min:',ro_min
        print 'ro_max:',ro_max
        print 'kappa:', kappa_factor

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