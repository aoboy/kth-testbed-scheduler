#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time

import numpy as np
import Burst
import burst_finder as burst
import kappa_factor as kf

from Burst import *
from burst_finder import *

class Link:
    def __init__(self, linkId, raw_data):
        self.LinkId = linkId            
        self.RawData   = raw_data        
        self.RxPackets = 0
        self.AvgPrSucc = 0
        self.Beta      = 0
        self.Kappa     = [] #should be the size of NoChannelsIds-1 in case of TSch
        self.Burst     = Burst
        self.NoRows    = None
        self.NoColumns = None
        self.ChannelIds= []
        self.burstL    = 0

    def setRowsColsAndChannelIds(self, n_rows, n_cols, channels):
        self.NoRows     = n_rows
        self.NoColumns  = n_cols
        self.ChannelIds = channels
        self.RxPackets  = np.zeros((self.NoRows, self.NoColumns), int)

    def addRawData(self, data):
        self.RawData = data.replace('\n', '')

    def linkPrr(self):
        self.AvgPrSucc = np.mean(self.RawData)        
        return self.AvgPrSucc

    def linkBurstLen(self):
        burstLen = 0
        counter  = 0
        for bit in self.RawData:
            if bit == 0:
                counter = counter + 1
            else:
                if burstLen < counter:
                    burstLen = counter
                counter = 0
        return burstLen

    def avgLinkPrrChannel(self, no_chs):
        '''return the Packet receptio ratio per channel'''        
	newLen = len(self.RawData)/no_chs
      
        if len(self.RawData)%no_chs:
	    newLen = newLen + 1
        
        m = np.resizee(self.RawData, (newLen ,no_chs))
        m = m.T #transpose the matrix to easily compute the PRR

        chPrr = np.zeros((1,no_chs), float)
        for n in range(0, len(m)):
            chPrr[n] = np.mean(m[n])

        return chPrr

    def avgLinkPrr(self):
        return np.mean(RawData)

    def setRawData(self, rawData):
        self.RawData = rawData

    def getBursts(self):
        rx_matrix = np.reshape(self.RawData, (self.NoRows, self.NoColumns))

        self.Burst=burst.burst_finder(rx_matrix, self.NoRows, self.NoColumns)
    def bettaFactor(self):
        pass

    def kappaFactorSpatial(self, ListOfNodes):
        pass

    def kappaFactorFrequency(self,  NoChannels):
	newLen = len(self.RawData)/NoChannels

        if len(self.RawData)%NoChannels:
	   newLen = newLen + 1

        m = np.resize(self.RawData, (newLen ,NoChannels))
        m = m.T #transpose the matrix to easily compute the PRR

        kappas = []
        for idx in range(0, len(m)):
            for idx2 in range(idx+1, len(m)):
                kappa = kf.kappa_factor(m[idx], m[idx2])
                kappas.append(kappa)

        self.Kappa = []
        self.Kappa = kappas
        return kappas
