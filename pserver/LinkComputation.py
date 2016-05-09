
import csv
#import networkx as nx
#from curses import idcok
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc
#import pylab
import os

plt.rcParams['ps.useafm'] = True
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rcParams['pdf.fonttype'] = 3 #[42 or 3]
prop = matplotlib.font_manager.FontProperties(size=3)

class Node:
    def __init__(self, id):
        self.id = id
        self.links = {}
        self.reset()

    def reset(self):                
        self.delay = float('inf')
        self.hops = float('inf')
        self.etx = float('inf')
        self.parentId= None
        self.parents = 0
        self.parentNodes = []
        self.parentLinks = []
#        self.childNodes = []
        
    def addLink(self, dst, data, path):
        if dst.id not in self.links:
            self.links[dst.id] = Link(self, dst, data, path)
                        
    def __str__(self):
        return str(self.id) + ', ' + str(self.edc)
            
    def computeParents(self):
        for link in self.links.values():
            if link.dst.edc <= self.nextHopEdc:
                self.parentLinks.append(link)
                self.parentNodes.append(link.dst)   
#                link.dst.childNodes.append(self)                
        self.parents = len(self.parentNodes)             
    
    def computeEtx(self, sinkId):
        changed = False
        if self.id == sinkId:
            if self.etx == float('inf'):
                self.etx = 0
                self.delay = 0
                self.hops = 0
                self.parentId=None
                self.parents = 0
                changed = True
        else:
            etxSorted = sorted( self.links.values(), etxCompare )
            for link in etxSorted:
                etx = link.dst.etx + 1.0 / link.rel
                #if self.etx > etx:
                if self.etx > etx:
                    self.etx = etx
                    changed = True
                    self.parentId=link
                    self.parents = 1
                    self.delay = link.dst.delay + (1.0 / link.rel)
                    self.hops =  link.dst.hops + 1
        return changed

    def nextHop(self, packet):
        if self.etx != 0:
            idx_tx = (packet.time/10)%10240

            if self.parentId != None:
                ret = self.parentId.data[idx_tx]
                delayT= 10
                if ret == 0:
                    for k in range(idx_tx+1, len(self.parentId.data)):
                        delayT = delayT + 10
                        if self.parentId.data[k] != 0:
                            break #successful
                packet.update(delayT, self.parentId.dst.id)
                #self.parentId.dst.nextHop(packet)
                self.parentId.dst.nextHop(packet)
            else:
                delayT= 10
                packet.update(delayT, self.id)
        else:
            return

def etxCompare(linkA, linkB):
    return cmp(linkA.dst.etx, linkB.dst.etx)

##3
class Link:
    def __init__(self, src, dst, data, path):
        self.src = src
        self.dst = dst
        self.rel = np.mean(data)
        self.count = 1
        self.data  = data
        self.path  = path
    def update(self, rel):
        self.count += 1
        if rel > self.rel:
            self.rel = rel
            
    def getSeq(self):
        return (self.src, self.dst, {'weight':self.rel})

    def __repr__(self):
        return str(self.src.id) + ',' + str(self.dst.id) + ',' + str(self.rel) + ',' + str(self.path)

    def __str__(self):
        return self.__repr__()

class Packet:
    def __init__(self, src, seqno, simtime):
        self.src   = src
        self.seqno = seqno
        self.delay = 0
        self.hops  = 0
        self.time  = simtime
        self.parents = []
    def update(self, delay, parent):
        self.parents.append(parent)
        self.delay += delay
        self.hops  +=1
        self.time  += delay
        
def buildTreeEtx(nodes, sinkId):
    for node in nodes.values():
        node.reset()
    again = True
    while again:
        again = False
        for node in nodes.values():
            ret = node.computeEtx(sinkId)
            if ret:
                again = True

def cleanupLinks(nodes):
    #remove unidirectional links
    for node in nodes.values():
        for k,v in node.links.items():
            if v.count < 2:
                del node.links[k]                
    for k,v in nodes.items():
        if len(v.links) == 0:
            del nodes[k]
        
def getNode(nodes, id):
    if id not in nodes:
        node = Node(id)
        nodes[id] = node
    return nodes[id]

def addLink(nodes, srcId, dstId, data, path):
    #print str(srcId) + ' ' + str(dstId) + ' ' + str(rel)
    src = getNode(nodes, srcId)
    dst = getNode(nodes, dstId)
    src.addLink(dst, data, path)
    #dst.addLink(src, rel)
#def getListFiles(dirPath):

def loadData(fname):
    idx = fname.find('link')
    src = fname[(idx+4):-4].split('-')[0]
    dst = fname[(idx+4):-4].split('-')[1]
    
    data = open(fname,'rb').read()
    data = data.replace('\n', '')
    data = data.split(' ')
    
    for idx, v in enumerate(data):
        if v != '':
            data[idx] = int(v)
        else:
            data.remove('')
    return src, dst, data

#def loadFiles(path):
    
def load(listFiles):
    nodes = {}    
    for fname in listFiles:
        src, dst, data = loadData(fname)
        addLink(nodes, int(src), int(dst), data, fname)

    #cleanupLinks(nodes)
    return nodes

def createCSV(fname, nodes):
    csv = open(fname,'wb')
    for node in nodes.values():
        for k,v in node.links.items():            
            csv_item = node.links[k].__str__()
            csv.write(csv_item+'\n')

def reload(csvfileName):
    nodes = {}
    f = open(csvfileName, 'rb')
    fileReader = csv.reader(f, delimiter=',')
    for row in fileReader:
        src, dst, rel, path = row
        #print src,'-',dst,' PRR:',rel
        src, dst, data = loadData(path)
        addLink(nodes, int(src), int(dst), data, path)

    return nodes

def reloadLessP(csvfileName, prob):
    nodes = {}
    f = open(csvfileName, 'rb')
    fileReader = csv.reader(f, delimiter=',')
    for row in fileReader:
        src, dst, rel, path = row
        #print src,'-',dst,' PRR:',rel
        src, dst, data = loadData(path)
        if np.mean(data) <= prob:
            addLink(nodes, int(src), int(dst), data, path)

    return nodes

def reloadLessThanP(csvfileName, links):
    nodes = {}
    f = open(csvfileName, 'rb')
    fileReader = csv.reader(f, delimiter=',')
    for row in fileReader:
        src, dst, rel, path = row
        linkFound = False
        for l in links:
            if int(src) == l.src.id and int(dst) == l.dst.id:
                linkFound = True
                break

        if linkFound == False:
            src, dst, data = loadData(path)
            addLink(nodes, int(src), int(dst), data, path)

    return nodes

def removeLinks(nodes, prob):
    links = []
    for node in nodes.values():
        for k,v in node.links.items():
            if node.links[k].rel >= prob:
                links.append(node.links[k])
    return links

def printLinks(nodes):
    for node in nodes.values():
      for k,v in node.links.items():
        print node.id,'-',node.links[k].dst.id,'-',node.links[k].rel
#def getTreeHelper(nodes, node, treeNodes, treeLinks):
#    parentNodes = node.parentNodes     
#    parentLinks = node.parentLinks
#    treeLinks.extend(parentLinks)
#    for node in parentNodes:
#        if node.id not in treeNodes:
#            treeNodes[node.id] = node
#            getTreeHelper(nodes, node, treeNodes, treeLinks)        
#
#def getTree(node, nodes):
#    treeNodes = {}
#    treeLinks = []
#    treeNodes[node.id] = node
#    getTreeHelper(nodes, node, treeNodes, treeLinks)
#    return treeNodes, treeLinks

#def linksToLinkSeqs(links):
#    linkSeqs =[]
#    for link in links:
#        linkSeqs.append(link.getSeq())
#    return linkSeqs
#
#def plotTop(srcId, nodes, linkSeq, f):
#    f = os.path.join(f, 'route')
#    if not os.path.exists(f):
#        os.mkdir(f)
#    fig = plt.figure(figsize=(20,20))
#    G=nx.Graph()
#    G.add_no80des_from(nodes)
#    G.add_edges_from(linkSeq)
#    pos=nx.spring_layout(G, weighted=True)
#    colors=[]
#    for (_,_,d) in G.edges(data=True):
#        colors.append(d['weight'])
#    if len(colors) > 0:
#        edgeLabels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)]) 
#        nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors, edge_vmin = 0, edge_vmax=max(colors), width=4,edge_cmap=pylab.get_cmap('brg'))
#        nx.draw_networkx_edge_labels(G,pos,edge_labels=edgeLabels)
#    plt.axis('off')
#    plt.savefig(os.path.join(f, str(srcId) + '.png'))
#    plt.close(fig)
    
def plotCumulativeHist(fig, n, rows, columns, values, slots, axisLabel):
    ax = fig.add_subplot(rows, columns, n)
    for value, label in values:
        ax.hist(value, slots, label=label, cumulative=True, histtype='step')
    ax.set_xlabel(axisLabel)
    ax.set_ylabel('count')
    ax.legend(loc='upper right')
    ax.grid()
            
def plotAvgBar(fig, n, rows, columns, values, yAxisLabel):
    avgs = []
    labels = []
    for value, label in values:
        avgs.append(np.average(value))
        labels.append(label)    
    ind = np.arange(len(values))  # the x locations for the groups
    width = 0.5       # the width of the bars
    ax = fig.add_subplot(rows, columns, n)
    ax.bar(ind, avgs, width)

    ax.set_ylabel(yAxisLabel)
    ax.set_xticks(ind + width / 2.0)
    ax.set_xticklabels( labels )
    ax.grid()

def plotter(path, edcList, delayList, hopsList, parentList):
    fig = plt.figure()

    plotCumulativeHist(fig, 1, 4, 2, edcList, 50,'metric') 
    plotCumulativeHist(fig, 3, 4, 2, delayList, 50, 'delay (in duty cycles)') 
    plotCumulativeHist(fig, 5, 4, 2, hopsList, 50, 'hops') 
    plotCumulativeHist(fig, 7, 4, 2, parentList, 50, 'parents') 

    plotAvgBar(fig, 2, 4, 2, edcList, 'avg. metric') 
    plotAvgBar(fig, 4, 4, 2, delayList, 'avg. delay (in duty cycles)') 
    plotAvgBar(fig, 6, 4, 2, hopsList, 'avg. hops') 
    plotAvgBar(fig, 8, 4, 2, parentList, 'avg. parents') 

    fig.set_size_inches(20,15)
    plt.savefig(os.path.join(path, 'stats.png'))
    #plt.show() # display
    plt.close(fig)
    

def perTxPenEdc(sinkId, nodes, txPen, f):
    buildTreeEdc(nodes, sinkId, txPen)
    
    edcs = [node.edc for node in nodes.values()]
    delays = [node.delay for node in nodes.values()]
    hops = [node.hops for node in nodes.values()]
    parents = [node.parents for node in nodes.values()]
    return edcs, delays, hops, parents

def etx(nodes, sinkId):
    buildTreeEtx(nodes, sinkId)

#    etx = [node.etx for node in nodes.values()]
#    delays = [node.delay for node in nodes.values()]
#    hops = [node.hops for node in nodes.values()]
#    parents = [node.parents for node in nodes.values()]
#    return etx, delays, hops, parents

def compute(nodes, sinkId, path, txPenList):
    edcList = []
    delayList = []
    hopList = []
    parentList = []
    for txPen in txPenList:
        edcs, delays, hops, parents = perTxPenEdc(sinkId, nodes, txPen, path)
        edcList.append((edcs, str(txPen)))
        delayList.append((delays, str(txPen)))
        hopList.append((hops, str(txPen)))
        parentList.append((parents, str(txPen)))
    etxs, delays, hops, parents = etx(sinkId, nodes, path)
    edcList.append((etxs, 'etx'))
    delayList.append((delays, 'etx'))
    hopList.append((hops, 'etx'))
    parentList.append((parents, 'etx'))
    return edcList, delayList, hopList, parentList

def loadExperiments(path, cases, csvprefix):
    for case in cases:
        newpath = str(path)+str(case)+'/'
        filesList = os.listdir(os.path.abspath(newpath))
        filesList.sort()
        listFiles = []
        for fname in filesList:
            if fname.find('link') != -1:
                #print os.path.join(newpath, fname)
                listFiles.append(os.path.join(newpath, fname))

        nodes = load(listFiles)
        csv_name='./csvMAC/'+csvprefix+str(case)+'.csv'
        createCSV(csv_name, nodes)
        
def loadT2RepeatExperiments(path):

    directories = os.listdir(os.path.abspath(path))

    directories.sort()

    for dir in directories:
        if dir.find('Tsch') != -1 or dir.find('Ch') != -1:
            dirPath = path +dir+'/'
            filesList = os.listdir(os.path.abspath(dirPath))
            filesList.sort()
            listFiles = []
            listFiles = []
            for fname in filesList:
                if fname.find('link') != -1:
                    #print os.path.join(newpath, fname)
                    listFiles.append(os.path.join(dirPath, fname))

            nodes = load(listFiles)
            csv_name='./csvMAC2/'+dir+'.csv'
            createCSV(csv_name, nodes)

def run(file, sinkId):
    nodes = load(file)
    path, _ = os.path.split(file)
    f = os.path.join(path, 'traces')
    if not os.path.exists(f):
        os.mkdir(f)
    thresholdList = (0, 0.1, 0.5, 0.9, 1)
    edc, delay, hop, parent = compute(nodes, sinkId, f, thresholdList)    
    plotter(f, edc, delay, hop, parent)

def conv2str(labelsList):
    retList = []
    for label in labelsList:
        retList.append(str(int(label)))
    return retList


def plotStdBar(fig, n, rows, columns, values, yAxisLabel, figInfo):
    avgs = []
    labels = []
    for value, label in values:
        avgs.append(np.std(value))
        labels.append(label)
    ind = np.arange(len(values))  # the x locations for the groups
    width = 0.6       # the width of the bars
    ax = fig.add_subplot(rows, columns, n)
    ax.bar(ind+width/2, avgs, width)

    ax.set_title(figInfo, size=5)
    ax.set_ylabel(yAxisLabel, size=4)
    ax.set_xticks(ind + width / 2.0)
    ax.set_xticklabels(labels, size=3)
    ax.set_yticklabels(conv2str(ax.get_yticks()), size=4)
    ax.grid(True)

def plotAvgBar4(fig, n, rows, columns, values, yAxisLabel, figInfo):
    avgs = []
    labels = []
    for value, label in values:
        avgs.append(np.average(value))
        labels.append(label)
    ind = np.arange(len(values))  # the x locations for the groups
    width = 0.6       # the width of the bars
    ax = fig.add_subplot(rows, columns, n)
    ax.bar(ind+width/2, avgs, width)

    ax.set_title(figInfo, size=5)
    ax.set_ylabel(yAxisLabel, size=4)
    #ax.set_xlim((0, np.max(avgs)+1), size=4)
    ax.set_xticks(ind + width / 2.0)
    ax.set_xticklabels(labels, size=3)

    labelsList = []
    for label in ax.get_yticks()[:]:
        labelsList.append(str(label))
        #return retLis

    ax.set_yticklabels(labelsList, size=4)
    ax.grid(True)

def plotAvgBar3(fig, n, rows, columns, values, yAxisLabel, figInfo):
    avgs = []
    labels = []
    for value, label in values:
        avgs.append(np.max(value))
        labels.append(label)
    ind = np.arange(len(values))  # the x locations for the groups
    width = 0.6       # the width of the bars
    ax = fig.add_subplot(rows, columns, n)
    ax.bar(ind+width/2, avgs, width)

    ax.set_title(figInfo, size=5)
    ax.set_ylabel(yAxisLabel, size=4)
    ax.set_xticks(ind + width / 2.0)
    ax.set_xticklabels(labels, size=3)
    ax.set_yticklabels(conv2str(ax.get_yticks()), size=4)
    ax.grid(True)

def plotAvgBar2(fig, n, rows, columns, values, yAxisLabel, figInfo):
    avgs = []
    labels = []
    for value, label in values:
        avgs.append(np.average(value))
        labels.append(label)
    ind = np.arange(len(values))  # the x locations for the groups
    width = 0.6       # the width of the bars
    ax = fig.add_subplot(rows, columns, n)
    ax.bar(ind+width/2, avgs, width)

    ax.set_title(figInfo, size=5)
    ax.set_ylabel(yAxisLabel, size=4)
    ax.set_xticks(ind + width / 2.0)
    ax.set_xticklabels(labels, size=3)
    ax.set_yticklabels(conv2str(ax.get_yticks()), size=4)
    ax.grid(True)

def plotter2(path, delayList, hopsCountList,figInfo, figName):
    fig = plt.figure()

    figTitle='Average Delay('+figInfo+')'
    plotAvgBar2(fig, 1, 2, 2, delayList, 'avg. delay (in ms)', figTitle)

    figTitle='Maximum Delay('+figInfo+')'
    plotAvgBar3(fig, 3, 2, 2, delayList, 'max. delay (in ms)', figTitle)

    figTitle='Delay Std('+figInfo+')'
    plotStdBar(fig, 2, 2, 2, delayList, 'std delay (in ms)', figTitle)

    
    figTitle='Average HopCount('+figInfo+')'
    plotAvgBar4(fig, 4, 2, 2, hopsCountList, 'avg hop count', figTitle)

    fig.set_size_inches(8,7)
    plt.savefig(os.path.join(path, figName+'Delay.pdf'))
    #plt.show() # display
    plt.close(fig)

def plotter3(path, delayList):
    fig = plt.figure()

    plotAvgBar3(fig, 1, 4, 2, delayList, 'max. delay (in ms)')

    fig.set_size_inches(5,4)
    plt.savefig(os.path.join(path, 'MaxDelay.pdf'))
    #plt.show() # display
    plt.close(fig)

##MAIN
if __name__ == '__main__':
    #path1 = '/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/Task22/Tsch'
    Tsch  = [2,4,8,12,16]
    #path2 = '/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/Task21/Ch'
    path3 = '/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/T2Repeat/'
    #path4 = '/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/T2Repeat/Ch'
    ChIDS = [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

    
    #loadExperiments(path4, ChIDS, 'Ch')
     
    #loadT2RepeatExperiments(path3)

    #nodes=reload('/home/gonga/channel_hopping/pyro-testbed/pserver/csvMAC/Tsch16.csv')
    csvpath = '/home/gonga/channel_hopping/pyro-testbed/pserver/csvMAC2/'
######################
    casesList = []
    casesList.append((Tsch, 'Tsch'))
    casesList.append((ChIDS,'Ch'))

    nodesList = range(1,33)

    prob_threshold     = 0.9
#
    baseNodes = reload(csvpath+'Ch26.csv')
    links     = removeLinks(baseNodes, prob_threshold)

    #print [ l.__str__() for l in links]

#    for caseType, caseLabel in casesList:
#        for case in caseType:
#            print 'Processing:',caseLabel,case
#            fcase = csvpath+caseLabel+str(case)+str('.csv')
#            nodes = []
#            nodes = reloadLessThanP(fcase, links)
#            #etx(nodes, sinkId)
#
#            printLinks(nodes)

#
#    for sinkId in [3, 11, 21, 26]:
#        for nodeId in nodesList:
#           if sinkId != nodeId:
#                print 'Sink:',sinkId,'NodeId:',nodeId
#                delaysList = []
#                hopsCountList   = []
#                for caseType, caseLabel in casesList:
#                    for case in caseType:
#                        print 'Processing:',caseLabel,case
#                        fcase = csvpath+caseLabel+str(case)+str('.csv')
#                        nodes = []
#                        nodes = reloadLessThanP(fcase, links)
#                        #nodes = reloadLessP(fcase, 0.9)
#                        etx(nodes, sinkId)
#
#                        simTime = 0
#                        deltaT  = 500
#                        hops    = 0
#
#                        delays = []
#                        hopCount=[]
#                        node = getNode(nodes, nodeId)
#                        for seqno in range(0,10000):
#                            parentIds = []
#                            #parentIds.append(node.id)
#                            p = Packet(node, seqno, simTime)
#                            #node.forward(node, simTime, 0, seqno, hops, parentIds)
#                            node.nextHop(p)
#                            delays.append(p.delay)
#                            hopCount.append(p.hops)
#                            #print p.src.id, ' ',p.delay,' ',p.hops, ' ', p.time, ' ', p.parents
#                            simTime = simTime + deltaT
#                        #append delays
#                        delaysList.append((delays,caseLabel+str(case)))
#                        hopsCountList.append((hopCount,caseLabel+str(case)))
#                ##plot graphs
#                figName = 'PSink'+str(sinkId)+'Node'+str(nodeId)
#                figInfo = 'src:'+str(nodeId)+' dst:'+str(sinkId)+' deltaT:'+str(deltaT)+str('ms')+' P <'+str(int(prob_threshold*100))
#                plotter2(csvpath, delaysList, hopsCountList,figInfo, figName)
######################
#delaysList = []
#for caseType, caseLabel in casesList:
#    for case in caseType:
#        print 'Processing:',caseLabel,case
#        fcase = csvpath+caseLabel+str(case)+str('.csv')
#        nodes=reload(fcase)
#        etx(nodes, 26)
#
#        simTime = 0
#        deltaT  = 500
#        hops    = 0
#
#        delays = []
#        node = getNode(nodes, 11)
#        for seqno in range(0,10000):
#            parentIds = []
#            #parentIds.append(node.id)
#            p = Packet(node, seqno, simTime)
#            #node.forward(node, simTime, 0, seqno, hops, parentIds)
#            node.nextHop(p)
#            delays.append(p.delay)
#            #print p.src.id, ' ',p.delay,' ',p.hops, ' ', p.time, ' ', p.parents
#            simTime = simTime + deltaT
#        #append delays
#        delaysList.append((delays,caseLabel+str(case)))
###plot graphs
#plotter2(csvpath, delaysList)
