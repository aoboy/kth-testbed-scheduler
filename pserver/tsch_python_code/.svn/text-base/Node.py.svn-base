#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time

import Link
from Link import *

class Node:
    def __init__(self, nodeId, txPackets=10240):
        self.NodeId       = nodeId
        self.NoLinks      = None
        self.TxPackets    = txPackets
        self.ListOfLinks  = []
        self.ListOfFiles  = []
        self.NoLinks      = None
        self.NoColumns    = 16
        self.ChannelIds   = None
        self.AllLinksPrr  = []
        self.AllLinkBeta  = []
        self.AllLinkKappa = []
        self.AllLinkCPDF  = []

    def addLinkFile(self, fileName):
        self.ListOfFiles.append(fileName)
        
    def addLink(self, link):
        for idx, l in enumerate(self.ListOfLinks):
            if l.LinkId == link.LinkId:
                #already exists... this is an update
                self.ListOfLinks[idx] = link
                return
        self.ListOfLinks.append(link)
    def removeLink(self, link):
        for l in self.ListOfLinks[:]:
            if l.LinkId == link.LinkId:
                self.ListOfLinks.remove(link)

    def linkExists(self, nodeId):
        for l in self.ListOfLinks[:]:
            if l.LinkId == nodeId:
                return True
        return False
    def getLinks(self):
        return self.ListOfLinks[:]

    def setChannelIds(self, chs):
        self.ChannelIds = chs

    def createLinks(self):
        #print 'Creating Links'
        for fname in self.ListOfFiles:
            idx = fname.find('link')
            dst_id= fname[(idx+4):-4].split('-')[1]
            data = open(fname,'rb').read()
            data = data.replace('\n', '')
            data = data.split(' ')

            #convert from string to int
            for idx, v in enumerate(data):
                if v != '':
                    data[idx] = int(v)
                else:
                    data.remove('')

            #create a link object
            link = Link(int(dst_id), data)
            link.ChannelIds = self.ChannelIds

            #add a link object to the list of links
            self.ListOfLinks.append(link)

        self.ListOfLinks.sort()
        self.NoLinks = len(self.ListOfLinks)

    def linksPrr(self):
        self.AllLinksPrr = []
        for idx, link in enumerate(self.ListOfLinks):
            linkPrr = self.ListOfLinks[idx].linkPrr()
            self.AllLinksPrr.append(linkPrr)
        return self.AllLinksPrr

    def linksBursts(self, prob_min):
        bursts = []
        for idx, l in enumerate(self.ListOfLinks):
            linkPrr = self.ListOfLinks[idx].linkPrr()
            #if linkPrr >= prob_min:
            bursts.append( self.ListOfLinks[idx].linkBurstLen())

        return bursts

    def avgBeta(self):
        return np.mean(self.AllLinkBeta)
    