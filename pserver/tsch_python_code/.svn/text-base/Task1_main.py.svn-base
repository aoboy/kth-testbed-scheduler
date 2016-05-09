#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time
import subprocess
#KTH - The Royal Institute of Technology
# Automatic Control Lab
#  Prof. Mikael Johansson's Group
#    Author: Antonio Gonga (El-Guapo Angoleno): gonga@kth.se, PhD Student

#Parser file: This file is used to parse data files into a readable format to MATLAB...it
#             also creats XML files.

import matplotlib
matplotlib.use('Agg')

import stats_generator
import Node
import Link
import Burst
import burst_finder
import beta_factor
import empiricalCDF as cdf

from stats_generator import *
from empiricalCDF import *

from plot_cdfs import *


ListOfStatistics = []


if __name__ == '__main__':
    #print 'Graph Generator'

    '''Generate Stats Objects '''
    ListOfTrials    = []
    ListOfStatistics = []

    #print os.listdir(os.path.abspath('/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/Task21'))

    ListOfTrials = stats_generator.load_files_task21('/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/Task1/')



    for tidx, trial in enumerate(ListOfTrials):
        print 'Processing Stats for Trial', trial.name
        ListOfStatistics = []
        ListOfStatistics = task.data
        

        for idx, stat in enumerate(ListOfTrials[tidx].ListOfStatistics):
            AllPrrs = []
            print 'Generating Stats for: ', stat.StatsId
            #stat.createNodes()
            ListOfTrials[tidx].ListOfStatistics[idx].addLinkFiles()
            for idx2, node in enumerate(ListOfStatistics[idx].ListOfNodes):
                #print 'NodeID:', node.NodeId
                ListOfTrials[tidx].ListOfStatistics[idx].ListOfNodes[idx2].createLinks()
                #print ListOfStatistics[idx].ListOfNodes[idx2].linksPrr()
                for prr in ListOfStatistics[idx].ListOfNodes[idx2].linksPrr():
                    AllPrrs.append(prr)
            ListOfStatistics[idx].AllNodesPrr = AllPrrs

            #compute KappaFactor
            ListOfStatistics[idx].computeKappa()

            ListOfStatistics[idx].AllNodesPrr.sort()
            ListOfStatistics[idx].AllNodesKappa.sort()

        #plot sorted data
        print 'Ploting Sorted Prr, Beta, and Kappa(-)'
        plot_sorted_prr(ListOfStatistics, 'Link IDs', 'Links Prr', 'Link Packet Recv Ratio', task.id+'LinkPrrsorted')
        plot_sorted_kappa(ListOfStatistics, 'Link IDs', 'Kappa', 'All Kappas Sorted', task.id+'LinksKappasorted')

        #plot CDFs
        print 'Ploting CDFs for Prr, Kappa(-)'
        plot_cdfs_prr(ListOfStatistics, 'Prr', 'CDF', 'All LinksPrr CDF', task.id+'LinkPrrCDF')
        plot_cdfs_kappa(ListOfStatistics, 'Kappa', 'CDF', 'All LinksKappa CDF', task.id+'LinkKappaCDF')
