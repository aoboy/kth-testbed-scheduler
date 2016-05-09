#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time

import numpy as np
import Node
import kappa_factor as kf
import beta_factor as  bf
import cond_prob_window as cpw


from Node import *


class NetworkStatistics:
    def __init__(self, statsId, noNodes, nColumns, chIDs):
        self.StatsId = statsId
        self.NoNodes = noNodes
        self.NoLinks = None
        self.NoColumns = nColumns
        self.ChannelIds = chIDs
        self.NodeStats  = []        
        self.ListOfNodes = []
        self.ListOfFiles = []        
        self.AllNodesPrr = []
        self.AllNodesKappa = []
        self.AllNodesBurstL = []
        self.AllNodesBeta  = []
        self.MaxWindow     = 50 #default value
        #self.TxRxConnectMat = zeros([self.NoNodes, self.NoNodes], int)

    def createNodes(self):
       for n in range(0, self.NoNodes):
           node = Node(int(n+1), 640*16)
           node.setChannelIds(self.ChannelIds)

           self.ListOfNodes.append(node)
          
   
    def addLinkFiles(self):
      '''Add the link files to each node'''
      for fname in self.ListOfFiles:
          idx = fname.find('link')
          src_id = fname[(idx+4):-4].split('-')[0]

          for idx, node in enumerate(self.ListOfNodes):
              if self.ListOfNodes[idx].NodeId == int(src_id):
                 self.ListOfNodes[idx].addLinkFile(fname)

    def computeKappa(self):
        if len(self.ChannelIds) != 0:
            if len(self.ChannelIds) == 1:
                self.allKappaSpatial()
            else:
                self.allKappaFrequencyCorrelation()

    def allKappaSpatial(self):
        AllKappas = []
        for  node in self.ListOfNodes:
            for idx, link in enumerate(node.ListOfLinks):
                ref_trace = link.RawData
                ''''''
                for idx1 in range(idx+1, len(node.ListOfLinks)):
                    cross_trace = node.ListOfLinks[idx1].RawData
                    kappa = kf.kappa_factor(ref_trace, cross_trace)
                    AllKappas.append(kappa)

        self.AllNodesKappa = []
        self.AllNodesKappa = AllKappas

    def allKappaFrequencyCorrelation(self):
        AllKappas = []
        for  node in self.ListOfNodes:
            for link in node.ListOfLinks:
                kappa_vec = kf.kappa_factor_frequency(link.RawData, len(self.ChannelIds))
                #kappa is a vector of NCh-1 kappas
                for kp in kappa_vec:
                    AllKappas.append(kp)

        print 'Ch:',len(AllKappas)
        self.AllNodesKappa = []
        self.AllNodesKappa = AllKappas


    def computeBeta(self):
        #self.beta()
        self.betaAndCrossCPDF()

    def beta(self):
        print 'Betaaaaaaaaaaa'
        AllBetas = []
        for k, node in enumerate(self.ListOfNodes):
            linksLen = len(self.ListOfNodes[k].ListOfLinks)
            if linksLen != 0:
                print 'Node:',node.NodeId 
                #beta_factor_vec = [] #np.zeros((1, linksLen), float)
                link_prr_vec   = []
                link_prr_vec   = np.zeros((1, linksLen))

                for idx in range(0, linksLen):
                    main_data  = node.ListOfLinks[idx].RawData
                    cross_data = main_data
                    lprr = self.ListOfNodes[k].ListOfLinks[idx].linkPrr()
                    link_prr_vec[0][idx] = lprr

                    link_cpdf  = []
                    link_cpdf  = np.zeros((1, 2*self.MaxWindow+1))

                    for window in range(0, self.MaxWindow):
                        cond_evn0  = 0
                        cond_evn1  = 1
                        
                        x0 = cpw.condProbWindow(main_data, cross_data, window, 1, cond_evn0)
                        x1 = cpw.condProbWindow(main_data, cross_data, window, 1, cond_evn1)
                        link_cpdf[0][self.MaxWindow+1-window] = x0
                        link_cpdf[0][self.MaxWindow+1+window] = x1

                    bfact = bf.beta_factor(self.MaxWindow, link_cpdf[0], link_prr_vec[0][idx])
                    #beta_factor_vec.append(bfact)
                    AllBetas.append(bfact)
                    self.ListOfNodes[k].AllLinkBeta.append(bfact)
                print 'Betas:', self.ListOfNodes[k].AllLinkBeta

        self.AllNodesBeta = AllBetas


    def betaAndCrossCPDF(self):

        for k, node in enumerate(self.ListOfNodes):
            outLinksSize = len(self.ListOfNodes[k].ListOfLinks)

            if outLinksSize:
                for idx in range(0, outLinksSize):
                    main_data = node.ListOfLinks[idx].RawData
                    link_prr  = node.ListOfLinks[idx].linkPrr()

                    print 'Beta4Node:',node.NodeId

                    for idx1 in range(0, outLinksSize):
                        cross_data = node.ListOfLinks[idx1].RawData

                        link_cpdf  = np.zeros((1, 2*self.MaxWindow+1))

                        for window in range(0, self.MaxWindow):
                            cond_evn0 = 1
                            cond_evn1 = 1
                            X0 = cpw.condProbWindow(main_data, cross_data, window, 1, cond_evn0)
                            X1 = cpw.condProbWindow(main_data, cross_data, window, 1, cond_evn1)
                            link_cpdf[0][self.MaxWindow - window]     = X0
                            link_cpdf[0][self.MaxWindow + 1 + window] = X1

                        if idx == idx1:
                            beta = bf.beta_factor(self.MaxWindow, link_cpdf[0], link_prr)
                            self.ListOfNodes[k].AllLinkBeta.append(beta)
                            print beta,

                            #accumulate all betas
                            self.AllNodesBeta.append(beta)

                        self.ListOfNodes[k].AllLinkCPDF.append(link_cpdf)