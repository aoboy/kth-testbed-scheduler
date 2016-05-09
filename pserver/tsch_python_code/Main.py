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

class Task:
    def __init__(self, id, data):
        self.id   = id
        self.data = data

ListOfStatistics = []


if __name__ == '__main__':
    #print 'Graph Generator'

    '''Generate Stats Objects '''
    ListOfTasks      = []
    ListOfStatistics = []

    #print os.listdir(os.path.abspath('/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/Task21'))

    stats21 = load_files_task21('./')
    #stats22 = stats_generator.load_files_task22('/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/Task22/')

    stats21.sort()
    #stats22.sort()

    ListOfTasks.append(Task('Task21', stats21))
    #ListOfTasks.append(Task('Task22', stats22))

    prob = 0.5

    for task in ListOfTasks:
        print 'Processing Stats for ',task.id
        ListOfStatistics = []
        ListOfStatistics = task.data

        AllPrrs = []

        for idx, stat in enumerate(ListOfStatistics):
            AllPrrs = []
            print 'Generating Stats for: ', stat.StatsId
            #stat.createNodes()
            ListOfStatistics[idx].addLinkFiles()
            for idx2, node in enumerate(ListOfStatistics[idx].ListOfNodes):
                #print 'NodeID:', node.NodeId
                ListOfStatistics[idx].ListOfNodes[idx2].createLinks()
                #print ListOfStatistics[idx].ListOfNodes[idx2].linksPrr()
                for prr in ListOfStatistics[idx].ListOfNodes[idx2].linksPrr():
                    AllPrrs.append(prr)
            ListOfStatistics[idx].AllNodesPrr = AllPrrs

            #compute KappaFactor
            #print 'Computing Kappa'
            #ListOfStatistics[idx].computeKappa()

            print 'Computing Beta'
            ListOfStatistics[idx].computeBeta()

            ListOfStatistics[idx].AllNodesPrr.sort()
            ListOfStatistics[idx].AllNodesKappa.sort()
            ListOfStatistics[idx].AllNodesBeta.sort()

        #plot sorted data
        print 'Ploting Sorted Prr, Beta, and Kappa(-)'
        plot_sorted_prr(ListOfStatistics, 'Link IDs', 'Links Prr', 'Link Packet Recv Ratio', task.id+'LinkPrrsorted')
        plot_sorted_kappa(ListOfStatistics, 'Link IDs', 'Kappa', 'All Kappas Sorted', task.id+'LinksKappasorted')
        plot_sorted_beta(ListOfStatistics, 'Link IDs', 'Beta', 'All Neta Sorted', task.id+'LinksBetasorted')

        #plot CDFs
        print 'Ploting CDFs for Prr, Kappa(-)'
        plot_cdfs_prr(ListOfStatistics, 'Prr', 'CDF', 'All LinksPrr CDF', task.id+'LinkPrrCDF')
        plot_cdfs_kappa(ListOfStatistics, 'Kappa', 'CDF', 'All LinksKappa CDF', task.id+'LinkKappaCDF')
        plot_cdfs_beta(ListOfStatistics, 'Beta', 'CDF', 'All LinksBeta CDF', task.id+'LinkBetaCDF')
