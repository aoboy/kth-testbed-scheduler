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

####for plotting
import math
from matplotlib import rc
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager
#------------------------------
plt.rcParams['ps.useafm'] = True
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rcParams['pdf.fonttype'] = 42
prop = matplotlib.font_manager.FontProperties(size=7)
####################

rootdir =os.path.abspath("./")
files=[]
channels=[]

def drange(start, stop, step):
     r = start
     while r < stop:
         yield r
         r += step

def frange(start, stop, step):
    vec=[]
    last_n =0;
    num_vals = int(float((stop-start)/step))
    for n in range(0, num_vals):
        last_n = n
        vec.append(float(start + n*step))
        
    idx = len(vec)
    #print num_vals,(stop-start)
    last_value= float(vec[idx -1] +step)
    vec.append(last_value)
    return vec

def sum_vec(vec):
    return sum(vec)

def FnOfX(vec, x):
    n_samples_less_x = 0
    for n in vec:
        if n <= x:
            n_samples_less_x =  n_samples_less_x + 1
    return float(n_samples_less_x)/float(len(vec))
def cdf(data_vec, data_range):
    step_size = float(data_range[1] - data_range[0])/len(data_vec)
    range_samples=frange(data_range[0], data_range[1], step_size)
    cdf_vec=[]
    for n in range(0, len(range_samples)):
       cdf_vec.append(float(FnOfX(data_vec, range_samples[n])))
    return cdf_vec

def cdf2(data_vec, data_range, n_samples):
    step_size = float(data_range[1] - data_range[0])/n_samples
    range_samples=frange(data_range[0], data_range[1], step_size)
    cdf_vec=[]
    for n in range(0, len(range_samples)):
       cdf_vec.append(float(FnOfX(data_vec, range_samples[n])))
    return cdf_vec
def average_vec(vec):
    sum_x = float(sum(vec))
    return (sum_x/float(len(vec)))


def get_files_dir():
        global files
        files = []
        for a in os.listdir(rootdir):
		if not os.path.isdir(os.path.join(rootdir,a)):
			#if a.find('Nchannels') != -1 and  a.find('link0-') == -1:
                        if a.find('Bin') != -1:
                                if a.find('.TXT') != -1 and a.find('?') == -1:
                                    files.append(a)
                                    #channels.append(a[(a.find('Pool')+4):a.find('li')])

        files.sort()

        for a in files:
            channels.append(a[(a.find('Pool')+4):a.find('li')])

        #print files
        #print channels

        return files

def list2str(l):
    b='['
    
    for a in l:
        c='{0:3}'.format(a)
        b += str(c)+' '

    return b+']'

def parse_files():

    n_chs=0
    kappa4vec  = []
    kappa8vec  = []
    kappa16vec = []
    
    resfile = open(os.path.join(rootdir, 'ParsedResults'), 'wb')
    
    for f, ch in zip(files, channels):
        n_chs = int(ch)
    
        data = open(os.path.join(rootdir, f),'rb').read()

	#print 'LINK',f[(f.find('link')+4) : f.find('.TXT')]
        resfile.write('======================NEW LINK==========================\n')
	resfile.write('LINK--->'+f[(f.find('Pool')) : f.find('.TXT')]+'\n')

        resfile.write('n_channels: '+str(n_chs)+'\n')
        
        row_idx = 0
        column_idx = 0
       
        data=data.replace(' ', '')

        data_len = len(data.replace('\n', ''))
        n_columns = 640
        print 'data_len:', len(data.replace('\n', '')), 'n_channels:', n_chs

        resfile.write('data_rows: '+str(n_columns)+' data_length: '+str(data_len)+'\n')
        resfile.write('-------------------------------------------------\n')
        data_vec=[]


        #n_chs=2

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
            link_prob[0][n] = float(a)/((16/n_chs)*n_columns)

            prob_xy[0][n]   = float(b)/((16/n_chs)*n_columns)

            sigma_x[0][n]   = math.sqrt(link_prob[0][n]*(1 - link_prob[0][n]))
          
            n = (n + 1)%n_chs
       
        n = 0
        #for a, b in zip(link_prob[0], prob_xy[0]):
        #    print a, b

        print 'sigma:', sigma_x[0]
        print 'link_prob:', link_prob[0]
        print 'prob_xy:', prob_xy[0]

        resfile.write('sigmas:    '+ list2str(sigma_x[0])+'\n')
        resfile.write('link_prob: '+list2str(link_prob[0])+'\n')
        resfile.write('prob_xy:   '+ list2str(prob_xy[0])+'\n')


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

        resfile.write('ro_xy:  '+list2str(ro_xy[0])+'\n')
        resfile.write('ro_max: '+list2str(ro_max[0])+'\n')
        resfile.write('ro_min: '+list2str(ro_min[0])+'\n')
        resfile.write('>>>kappa_factor: '+list2str(kappa_factor[0])+'\n')
        rvec=[-1.0, 1.0]
        #resfile.write('>>>CDF'+list2str(cdf2(kappa_factor[0], rvec, 10))+'\n')
        resfile.write('>>>CDF'+list2str(cdf(kappa_factor[0], rvec))+'\n')

        #try to collect all Kappas
        #if n_chs == 4:
        #    for val in kappa_factor[0]:
        #        kappa4vec.append(val)
        #if n_chs == 8:
        #     for val in kappa_factor[0]:
        #        kappa8vec.append(val)
        #if n_chs == 16:
        #     for val in kappa_factor[0]:
        #        kappa16vec.append(val)

    resfile.close()

    #print '4channels:',kappa4vec
    #print '8 channels:',kappa4vec
    #print '16channels:',kappa4vec
    #axplts  =[]
    #fig = plt.figure()
    #ax = fig.add_axes([0.14, 0.1, 0.82, 0.87])
    #axnames =['4 channels', '8 channels','16 channels']
    #difg = ['p-', '-x', 'c-']

    #counter = 0

    #mygraph = ax.plot(kappa4vec, difg[counter])
    #ax.grid(True)
    #axplts.append(mygraph)
    #counter = counter + 1

    #mygraph = ax.plot(kappa8vec, difg[counter])
    #ax.grid(True)
    #axplts.append(mygraph)
    #counter = counter + 1

    #mygraph = ax.plot(kappa16vec, difg[counter])
    #ax.grid(True)
    #axplts.append(mygraph)
    #counter = counter + 1

    #plt.legend( (axplts[0], axplts[1], axplts[2]), (axnames[0], axnames[1], axnames[2]), loc='best', prop=prop )

    #fig = plt.gcf()
    #fig.set_size_inches(3.9,3.9)
    #plt.savefig("testbedcellcapacity.eps", dpi=120)
    #plt.savefig("kappa_factor.pdf", dpi=120)

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