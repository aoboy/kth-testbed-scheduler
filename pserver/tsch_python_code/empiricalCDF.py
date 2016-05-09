#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time

import matplotlib
matplotlib.use('Agg')

import numpy as np
import pylab as P

def empirical_cdf_ccdf(data_vec, data_range, no_samples=None):

    num_samples = no_samples
    if no_samples == None:
        num_samples = 100

    N = len(data_vec)

    data       = data_vec.sort()
    size_range = data_range[1] - data_range[0]
    stepSize   = (1.0*size_range)/num_samples

    range_samples = np.arange(data_range[0], data_range[1]+stepSize, stepSize)
    len_range = len(range_samples)

    cdf, bins, patches = P.hist(data_vec, len_range, normed=1, histtype='step', cumulative=True)


    ccdf, bins, patches = P.hist(data_vec, bins=bins, normed=1, histtype='step', cumulative=-1)

    return cdf, ccdf
    
