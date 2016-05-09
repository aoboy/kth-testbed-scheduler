#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wave import Error
import os
import time
import Queue
import threading
import random
import shlex
import sys
import subprocess
from threading import Thread
import math

sys.path.insert(0,os.pardir)	# to find testserver.py

rootdir=os.path.abspath('./')

MAX_TX_PACKETS = int(16*640)
MAX_SYNCH_PKTS = 100

CONF_CHANNEL_CH_26         = 26
CONF_CHANNEL_CH_25         = 25
CONF_CHANNEL_CH_24         = 24
CONF_CHANNEL_CH_23         = 23
CONF_CHANNEL_CH_22         = 22
CONF_CHANNEL_CH_21         = 21
CONF_CHANNEL_CH_20         = 20
CONF_CHANNEL_CH_19         = 19
CONF_CHANNEL_CH_18         = 18
CONF_CHANNEL_CH_17         = 17
CONF_CHANNEL_CH_16         = 16
CONF_CHANNEL_CH_15         = 15
CONF_CHANNEL_CH_14         = 14
CONF_CHANNEL_CH_13         = 13
CONF_CHANNEL_CH_12         = 12
CONF_CHANNEL_CH_11         = 11


CHANNEL_POOL_SIZE_01       = 29
CHANNEL_POOL_SIZE_02       = 30
CHANNEL_POOL_SIZE_04       = 31
CHANNEL_POOL_SIZE_06       = 32
CHANNEL_POOL_SIZE_08       = 33
CHANNEL_POOL_SIZE_10       = 34
CHANNEL_POOL_SIZE_12       = 35
CHANNEL_POOL_SIZE_14       = 36
CHANNEL_POOL_SIZE_16       = 37


CHANNEL_POOL_SIZE_CH22         = 100
CHANNEL_POOL_SIZE_CH16         = 101
CHANNEL_POOL_SIZE_CH12         = 102

CHANNEL_POOL_SIZE_CH2622       = 200
CHANNEL_POOL_SIZE_CH262216     = 201
CHANNEL_POOL_SIZE_CH26221612   = 202

CHANNEL_POOL_SIZE_CH15         = 203
CHANNEL_POOL_SIZE_CH20         = 204
CHANNEL_POOL_SIZE_CH1520       = 205
CHANNEL_POOL_SIZE_CH25         = 206
CHANNEL_POOL_SIZE_CH26         = 207
CHANNEL_POOL_SIZE_CH15202526   = 208
time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
channel_cache ={}

channel_cache[CONF_CHANNEL_CH_11] = [CONF_CHANNEL_CH_11]
channel_cache[CONF_CHANNEL_CH_12] = [CONF_CHANNEL_CH_12]
channel_cache[CONF_CHANNEL_CH_13] = [CONF_CHANNEL_CH_13]
channel_cache[CONF_CHANNEL_CH_14] = [CONF_CHANNEL_CH_14]
channel_cache[CONF_CHANNEL_CH_15] = [CONF_CHANNEL_CH_15]
channel_cache[CONF_CHANNEL_CH_16] = [CONF_CHANNEL_CH_16]
channel_cache[CONF_CHANNEL_CH_17] = [CONF_CHANNEL_CH_17]
channel_cache[CONF_CHANNEL_CH_18] = [CONF_CHANNEL_CH_18]
channel_cache[CONF_CHANNEL_CH_19] = [CONF_CHANNEL_CH_19]
channel_cache[CONF_CHANNEL_CH_20] = [CONF_CHANNEL_CH_20]
channel_cache[CONF_CHANNEL_CH_21] = [CONF_CHANNEL_CH_21]
channel_cache[CONF_CHANNEL_CH_22] = [CONF_CHANNEL_CH_22]
channel_cache[CONF_CHANNEL_CH_23] = [CONF_CHANNEL_CH_23]
channel_cache[CONF_CHANNEL_CH_24] = [CONF_CHANNEL_CH_24]
channel_cache[CONF_CHANNEL_CH_25] = [CONF_CHANNEL_CH_25]
channel_cache[CONF_CHANNEL_CH_26] = [CONF_CHANNEL_CH_26]

channel_cache[CHANNEL_POOL_SIZE_CH12] = 12
channel_cache[CHANNEL_POOL_SIZE_CH16] = 16
channel_cache[CHANNEL_POOL_SIZE_CH22] = 22
channel_cache[CHANNEL_POOL_SIZE_CH26221612] = [26,22,16,12]

channel_cache[CHANNEL_POOL_SIZE_02] = [26, 17]
channel_cache[CHANNEL_POOL_SIZE_04] = [26, 22, 17, 13]
channel_cache[CHANNEL_POOL_SIZE_08] = [26, 19, 12, 20, 24, 22, 17, 13]
channel_cache[CHANNEL_POOL_SIZE_12] = [26, 19, 12, 20, 24, 16, 23, 18, 25, 22, 17, 13]
channel_cache[CHANNEL_POOL_SIZE_16] = [26, 19, 12, 20, 24, 16, 23, 18, 25, 14, 21, 11, 15, 22, 17, 13]

channel_cache[CHANNEL_POOL_SIZE_CH15]       = [15]
channel_cache[CHANNEL_POOL_SIZE_CH20]       = [20]
channel_cache[CHANNEL_POOL_SIZE_CH25]       = [25]
channel_cache[CHANNEL_POOL_SIZE_CH26]       = [26]
channel_cache[CHANNEL_POOL_SIZE_CH1520]     = [15, 20]
channel_cache[CHANNEL_POOL_SIZE_CH15202526] = [15, 20, 25, 26]


experiment_cases ={}

experiment_cases[CONF_CHANNEL_CH_11] = '11'
experiment_cases[CONF_CHANNEL_CH_12] = '12'
experiment_cases[CONF_CHANNEL_CH_13] = '13'
experiment_cases[CONF_CHANNEL_CH_14] = '14'
experiment_cases[CONF_CHANNEL_CH_15] = '15'
experiment_cases[CONF_CHANNEL_CH_16] = '16'
experiment_cases[CONF_CHANNEL_CH_17] = '17'
experiment_cases[CONF_CHANNEL_CH_18] = '18'
experiment_cases[CONF_CHANNEL_CH_19] = '19'
experiment_cases[CONF_CHANNEL_CH_20] = '20'
experiment_cases[CONF_CHANNEL_CH_21] = '21'
experiment_cases[CONF_CHANNEL_CH_22] = '22'
experiment_cases[CONF_CHANNEL_CH_23] = '23'
experiment_cases[CONF_CHANNEL_CH_24] = '24'
experiment_cases[CONF_CHANNEL_CH_25] = '25'
experiment_cases[CONF_CHANNEL_CH_26] = '26'

experiment_cases[CHANNEL_POOL_SIZE_02] = '02'
experiment_cases[CHANNEL_POOL_SIZE_04] = '04'
experiment_cases[CHANNEL_POOL_SIZE_08] = '08'
experiment_cases[CHANNEL_POOL_SIZE_12] = '12'
experiment_cases[CHANNEL_POOL_SIZE_16] = '16'

experiment_cases[CHANNEL_POOL_SIZE_CH15] = '15'
experiment_cases[CHANNEL_POOL_SIZE_CH20] = '20'
experiment_cases[CHANNEL_POOL_SIZE_CH25] = '25'
experiment_cases[CHANNEL_POOL_SIZE_CH26] = '26'
experiment_cases[CHANNEL_POOL_SIZE_CH1520]     = '1520'
experiment_cases[CHANNEL_POOL_SIZE_CH15202526] = '15202526'

location_cache = {}
location_cache['XBS0KHZF'] = 'CORR-B'
location_cache['XBS0KI3E'] = 'KITCHEN'
location_cache['XBS0JZLB'] = 'B606'
location_cache['XBS0KIF6'] = 'B604'
location_cache['XBS4RXBF'] = 'CORR-B'
location_cache['XBS0LAE8'] = 'B614'
location_cache['XBS0LB3V'] = 'B614'
location_cache['XBS5GZJR'] = 'B610'

location_cache['XBS0KIBM'] = 'CORR-B'
location_cache['XBS0KHXY'] = 'CORR-B'
location_cache['XBS0KHYF'] = 'B618'
location_cache['XBS0SGA4'] = 'B620'
location_cache['XBS14SR2'] = 'C628'
location_cache['XBS0LABO'] = 'C628'
location_cache['XBS5GZPR'] = 'A618'

location_cache['XBS4RXWK'] = 'A618'
location_cache['MFTFL9B1'] = 'A619'
location_cache['XBS4RVSD'] = 'A621'
location_cache['MFTFJ1CU'] = 'CORR-A'
location_cache['MFTFL6WA'] = 'MEETING-R'
location_cache['MFTFIZD7'] = 'CORR-A'
location_cache['XBS5GZ78'] = 'CORR-A'
location_cache['XBS5GZ7U'] = 'A625'
location_cache['MFTFL9LZ'] = 'A627'
location_cache['XBS5H6MF'] = 'CORR-A'

location_cache['XBS0LACQ'] = 'KITCHEN'
location_cache['XBS0LAFQ'] = 'CORR-A'
location_cache['XBS0K5UN'] = 'A607'
location_cache['XBS0K2QI'] = 'A609'
location_cache['XBS0LAAD'] = 'A615'
location_cache['XBS0KI6I'] = 'A613'
location_cache['XBS0KHZZ'] = 'FRONT-PRINT'

#MFTFL9M1
#MFTFIYOZ
#MFTFL8ZR
location_cache['MFTFL9M1'] = 'CORR-A'
location_cache['MFTFIYOZ'] = 'CORR-A'
location_cache['MFTFL8ZR'] = 'CORR-D'




casesList = []
#casesList  = [0xAA49, #AA. channels 15.20 (15-11).(20-11)
#              0xAA4E, #AA. channels 15.25 The index subtraction is necessary to
#              0xAA4F, #AA. channels 15.26 avoid extra conversions at the sensor
#              0xAA9E, #AA. channels 20.25
#              0xAA9F, #AA. channels 20.26
#              0xAAEF  #AA. channels 25.26
#              ]

gateway_ips = []
gateway_ips = ['192.168.200.10', '192.168.200.11', '192.168.200.12', '192.168.200.13']

blackList   = []
blackList   = ['XBS0LACQ', 'XBS5H6MF', 'XBS4RXWK']

gatewaysList = []

def execute(commandLine):
    #print commandLine
    args = shlex.split(commandLine)
    #print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print 'ERROR!'
        print stdout
        print stderr
        exit(-1)
    return stdout

class ExpError(Exception):
    pass

class Node:
    def __init__(self, id, dev, name, supernode, nodeId):
        self.dev_name= dev
        self.name = name
        self.supernode = supernode
        self.node_id = nodeId
        self.dev_id = id
        self.location = location_cache[name]
        self.prgtx_cmd = ''
        self.prgrx_cmd = ''

    def execCmd(self, commandLine):
        #print commandLine
        args = commandLine.split() #shlex.split(commandLine)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print 'ERROR!', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
            print stdout
            print stderr
            raise ExpError()
        return p.returncode, stdout
    def motelist(self):
        cmd = 'ssh '+self.supernode+' motelist '
        myoutput =subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

	ret = []
	for line in myoutput.split('\n'):
	    if line.find('/dev/ttyUSB') != -1:
	        ret.append(line)
	return ret

    def notify2Exec(self, cmdstr):
        print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),'server calling to execute ', cmdstr
        p=subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stderr

    def setNodeID(self, node_id):
        self.node_id = node_id
    def getNodeID(self):
        return self.node_id

    def setDevId(self, dev_id):
        self.dev_id = dev_id
    def getDevId(self):
        return self.dev_id

    def getName(self):
        return self.name

    def programNodeAsRX(self):
        devid = self.getDevIdByName(self.name) + 1
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE=isa_receiver.ihex MOTE='+str(devid)
        return self.execCmd(cmd)

    def programNodeWithIHEXFile(self, srcFile):
        #devid = int(self.getDevIdByName(self.name)) + 1
        #cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE='+srcFile+' MOTE='+str(devid)
        devname = self.getDevNameByName(self.name)
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE='+srcFile+' MOTES=$\''+devname+'\''
        sys.stdout.flush()
        return self.execCmd(cmd)

    def programNodeWithIHEXFileAll(self, srcFile):
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE='+srcFile
        sys.stdout.flush()
        return self.execCmd(cmd)

    def programNodeAsRXAll(self):
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE=isa_receiver.ihex'
        sys.stdout.flush()
        return self.execCmd(cmd)

    def programNodeAsTx(self):
        devid = int(self.getDevIdByName(self.name)) + 1
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE=isa_sender.ihex MOTE='+str(devid)
        sys.stdout.flush()
        return self.execCmd(cmd)

    def getDevIdByName(self, name):
        dev_id = ''
        #cmd = 'motelist '
        myoutput = self.motelist()

        for m in myoutput:
            if m.find(name) != -1:
               devid = m.split()[1]
               dev_id= devid[devid.find('USB')+3]
               break
        return dev_id
    def getDevNameByName(self, name):
        dev_name = self.dev_name
        #cmd = 'motelist '
        myoutput = self.motelist()

        for m in myoutput:
            if m.find(name) != -1:
               devid = m.split()[1]
               dev_name= devid
               break
        return dev_name

    def getNodeIdByDevId(self, dev_id):
        node_id = ''
        cmd     = 'ssh '+self.supernode+ ' ./node_id '+str(dev_id)
        #p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sys.stdout.flush()
	returncode, stdout = self.execCmd(cmd)

        if returncode != 0:
            print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),'ERROR: getting NodeID failed'
            return node_id
        else:
	    for m in stdout.split():
	       if m.find('id:') != -1:
	          try:
		     nodeid   = m[(m.find('id:')+3):]
		     node_id  = str(nodeid)
                     #print 'FOUND_id:',node_id
                     return node_id
	          except:
		    pass
        print 'NodeID Not FOund_ID'
	return node_id

    def triggerNodeTx(self):
        #devid = int(self.getDevIdByName(self.name)) + 1
        dev_name = self.getDevNameByName(self.name)
        cmd   = 'ssh '+self.supernode+' ./transmit '+str(dev_name)
        sys.stdout.flush()
        return self.execCmd(cmd)

    def downloadMoteData(self):
        self.dev_id = self.getDevNameByName(self.name)

        cmd = 'ssh '+self.supernode+' ./sconnect '+self.dev_id

        sys.stdout.flush()

        return self.execCmd(cmd)

 #############################
class Gateway:
    def __init__(self, supernode, casesList):
	self.moteList  = []
	self.supernode = supernode
	self.nodes     = []
        self.casesList = casesList
	self.rxBinaryFile = "./binaries/isa_receiver.ihex"
	self.txBinaryFile = "./binaries/isa_sender.ihex"
        self.ascii_extend = ['€', 'ƒ', '„', '†', '‡', '‰', 'Š', '‹', 'Œ', 'Ž', '‘', '’', '“', '”', '•', '–',
				      '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '¡', '¢', '£', '¤', '¥', '¦', '§', '©',
				      'ª', '«', '¬', '®', '¯', '°', '±', '²', '³', 'µ', '¶', '¹', 'º', '»', '¼', '½',
				      '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ë', 'Ì', 'Í', 'Î',
				      'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ',
				      'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î',
				      'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ',
				      'ÿ']

    def getNodes(self):
        return self.nodes[:]

    def execCmd(self, commandLine):
        #print commandLine
        args = commandLine.split() #shlex.split(commandLine)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print 'ERROR!:::', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
            print stdout
            print stderr
            raise ExpError()
        return p.returncode, stdout

    def motelist(self):
        cmd = 'ssh '+self.supernode+' motelist '
        myoutput =subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

	ret = []
	for line in myoutput.split('\n'):            
	    if line.find('/dev/ttyUSB') != -1:
	        ret.append(line)
	return ret

    def uploadIHEX4Sender(self, destfile):
        cmd = 'scp '+self.txBinaryFile +' '+self.supernode+':/home/gonga/isa_sender.ihex'
        retCode, output = self.execCmd(cmd)
        return retCode, output

    def uploadIHEX4Receiver(self, destfile):
        cmd = 'scp '+self.rxBinaryFile +' '+self.supernode+':/home/gonga/isa_receiver.ihex'
        retCode, output = self.execCmd(cmd)
        return retCode, output

    def triggerSender(self, nodeid):
        for node in self.nodes[:]:
            if node.getNodeID() == nodeid:
                node.triggerTx()

    def uploadIHEX(self, srcFile):
        destfile='/home/gonga/'
        cmd = 'scp /home/gonga/binaries/'+srcFile+' '+self.supernode+':'+destfile
        return self.execCmd(cmd)

    def uploadIHEXNew(self, srcFile):
        destfile='/home/gonga/binaries/'
        cmd = 'scp binaries/'+srcFile+' '+self.supernode+':'+destfile
        return self.execCmd(cmd)

    def uploadIHEXAll(self):
        self.uploadIHEX('isa_sender.ihex')
        try:
            for t in range(0, 1):
              time.sleep(0.5)
        except Exception:
              print 'error sleep after upload..', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
        self.uploadIHEX('isa_receiver.ihex')

    def uploadIHEXFilesWithCase(self):
        for caseId in self.casesList[:]:
            fileNameRcv = 'case'+str(caseId)+'isa_receiver.ihex'
            fileNameSnd = 'case'+str(caseId)+'isa_sender.ihex'

            self.uploadIHEXNew(fileNameRcv)
            try:
                for t in range(0, 1):
                    time.sleep(0.5)
            except Exception:
              print 'error sleep after upload..'
            self.uploadIHEXNew(fileNameSnd)
            print '===>Uploading ',fileNameRcv,' and ',fileNameSnd,' to ',self.supernode

    def programNodeWithIHEXFileAll(self, srcFile):
        self.moteList  = self.motelist()
        motelist = self.moteList
        devs=' MOTES=$\''
        for line in motelist:
            sline = line.split()
            name  = sline[0]
            if name not in blackList:
                 devs += sline[1]+' '

        devs+='\''
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE='+srcFile+devs
        return self.execCmd(cmd)

    def programNodeAsRXAll(self):
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE=isa_receiver.ihex'
        return self.execCmd(cmd)

    def programNodeAsRXAllWithFileName(self, fileName):
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE='+fileName
        return self.execCmd(cmd)

    def programNodeAsTXAll(self):
        self.moteList  = self.motelist()
        motelist = self.moteList
        devs=' MOTES=$\''
        # ' MOTES=$'+
        for line in motelist:
            sline = line.split()
            name  = sline[0]
            if name not in blackList:
                 devs += sline[1]+' '

        devs+='\''
        print devs
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE=isa_sender.ihex'+devs
        retCode, output = self.execCmd(cmd)
        return retCode, output

    def programNodeAsTXAllWithFileName(self, fileName):
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE='+fileName
        retCode, output = self.execCmd(cmd)
        return retCode, output

    def programNodesCaseId(self, fileCaseId):
        cmd = 'ssh '+self.supernode+' make TARGET=sky upload-ihex FILE='+fileCaseId
        retCode, output = self.execCmd(cmd)
        return retCode, output

    def notify2Exec(self, cmdstr):
        print 'server calling to execute ', cmdstr
        p=subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stderr

    def getDevIdByName(self, name):
        dev_id = ''
        #cmd = 'motelist '
        myoutput = self.motelist()

        for m in myoutput:
            if m.find(name) != -1:
               devid = m.split()[1]
               dev_id= devid[devid.find('USB')+3]
               break
        return dev_id

    def getNodeIdByDevId(self, dev_id):
        node_id = ''
        cmd     = 'ssh '+self.supernode+ ' ./node_id '+str(dev_id)
        #p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returncode, stdout = self.execCmd(cmd)

        if returncode != 0:
            print 'ERROR: getting NodeID failed::', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
            return node_id
        else:
	    for m in stdout.split():
	       if m.find('id:') != -1:
	          try:
		     nodeid   = m[(m.find('id:')+3):]
		     node_id  = str(nodeid)
                     #print 'FOUND_id:',node_id
                     return node_id
	          except:
		    pass
        print 'NodeID Not FOund_ID:::', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
        return node_id

    def getNodeIdByDevName(self, dev_name):
        node_id = ''
        cmd     = 'ssh '+self.supernode+ ' ./node_id '+str(dev_name)
        #p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returncode, stdout = self.execCmd(cmd)

        if returncode != 0:
            print 'ERROR: getting NodeID failed::', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
            return node_id
        else:
	    for m in stdout.split():
	       if m.find('id:') != -1:
	          try:
		     nodeid   = m[(m.find('id:')+3):]
		     node_id  = str(nodeid)
                     #print 'FOUND_id:',node_id
                     return node_id
	          except:
		    pass
        print 'NodeID Not FOund_ID:::', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
        return node_id
    
    def createNodes(self):
        self.nodes = []
        self.moteList  = self.motelist()
        motelist = self.moteList
        for line in motelist:
            sline = line.split()
            name  = sline[0]
            if name not in blackList:
                dev_name = sline[1]
                dev_id  = self.getDevIdByName(name)
                #node_id = self.getNodeIdByDevId(dev_id)
                node_id = self.getNodeIdByDevName(dev_name)
                #(self, id, dev, name, supernode, nodeId):
                self.nodes.append(Node(dev_id, dev_name, name, self.supernode, node_id))

    def updateNodes(self):

        for idx in range(0, len(self.nodes)):
            dev_id  = self.getDevIdByName(self.nodes[idx].getName())
            if dev_id != '':
                self.nodes[idx].setDevId(dev_id)

    def downloadData(self, snode, caseid, folder):

        for node in self.nodes[:]:
            if node.getNodeID() != snode:
                returncode = 0,
                output     = []
                try:
                    sys.stdout.flush()
                    returncode, output = node.downloadMoteData()

                    if returncode == 0 and output.find('node_tx') == -1   and output.find('TIMEOUT') == -1:
                        self.saveDataFile(snode, node.getNodeID(), caseid, folder, output)
                    else:
                         print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                         print "Non-exceptional error in downloadData in gateway", node.supernode, " for node ", node.getNodeID()
                except:
                    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                    print "Exception in downloadData in gateway ", node.supernode,' for node ', node.getNodeID()
                    pass

    def saveDataFile(self, snode, rnode, caseid, folder, data):
        #global sender_node_id, exp_case, exp_folder
	got_filename = None
	filename = ''
	file=''
	for substr in data.split('\n'):
	    if  got_filename == None:
	        idx = substr.find('r:')
		if idx != -1:
                   filename = './results/'+folder+str(caseid)+str('link'+snode+'-'+rnode+'.txt')
		   got_filename = True
		   file = open(filename, 'wb')
                   print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
		   print 'save data to file', filename

	    else:
		if substr.find('E') != -1 or substr.find('END') != -1:
		   if got_filename:
			file.close()
                        return True
		   else:
			      return False

                if substr.find('-') != -1 and substr.find('link') == -1:
	            c = substr.split('-')[1]
			  #get rid of all unwanted characters.......
	            for unwanted in self.ascii_extend:
		        if c.find(unwanted) != -1:
		           c.replace(unwanted, '')
	            if c.find('E') != -1 or c.find('END') != -1:
		        if got_filename:
			   file.close()
		           return True
	            if got_filename:
		        file.write(substr+'\n')

		  #end of IF
	return True

    def toString(self):
        print "*---------------------------*"
        print "| GATEWAY: ",self.supernode,' |'
        print "*---------------------------------------------------------*"
        print "| NodeName      devName       devID   NodeID    LocationID|"
        print "*---------------------------------------------------------*"
        for node in self.nodes[:]:
            print node.getName(),'\t', node.dev_name,'\t',node.dev_id,'\t',node.getNodeID(),'  \t', node.location
        print "*---------------------------------------------------------*"
#############################################################################################
class NodeDownloadThread(threading.Thread):
    def  __init__(self, nodes_queue, senderId, caseId, folderId):
        threading.Thread.__init__(self)
        self.queue = nodes_queue
        self.senderId = senderId
        self.caseId   = caseId
        self.folderId = folderId

    def run(self):
        while True:
            startT= time.time()
            g = self.queue.get()
            g.downloadData(self.senderId, self.caseId, self.folderId)
            endT = time.time()
            print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),'===>Node:',g.supernode,' download done! in ', (endT-startT)
            self.queue.task_done()

class ParallelizeGatewayOps(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, remoteFile, operation):
        threading.Thread.__init__(self)
        self.queue          = queue
        self.operation      = operation
        self.remoteFileName = remoteFile

    def run(self):
         while True:
            #dequeue a gateway
            startT= time.time()
            g = self.queue.get()

            if self.operation == 'initHEX':
                  g.uploadIHEX('isa_sender.ihex')
                  print 'Programming GW:',g.supernode
                  myErr, myouput = g.programNodeAsTXAll()
                  endT = time.time()
                  print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                  print '===>Programming isa_sender.ihex on ',g.supernode,' lasted ',(endT-startT), 'seconds'
                  self.queue.task_done()

            if self.operation == 'createNetwork':
                  print '===>Creating Nodes on:', g.supernode
                  g.createNodes()
                  g.toString()
                  endT = time.time()
                  print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                  print '===>Done creating gateway nodes.. on',g.supernode,' in ',(endT-startT), 'seconds'
                  self.queue.task_done()

            if self.operation == 'caseHEX':
                 g.uploadIHEXFilesWithCase()
                 self.queue.task_done()

            if self.operation == 'progAsRxIHEXFileAll':
                 g.programNodeWithIHEXFileAll(self.remoteFileName)
                 endT = time.time()
                 print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                 print '===>Done programming Rxs on ',g.supernode,' in ',(endT-startT), 'seconds'
                 self.queue.task_done()

            if self.operation == 'exec':
                g.notify2Exec()
                self.queue.task_done()

#-------------------------------------------------------------------------------
#############################################################################################
def createReceiverIHEX(poolsize):
    print 'compiling receiver binary for ch_pool_size=', poolsize
    myOutput=''
    try:
       channel_a = ((poolsize & 0x00F0) >> 4)
       channel_b = (poolsize & 0x000F)
       
       cmd ='make recvbin TARGET=sky DEFINES=NODE_IS_RECEIVER DEFINES+=CONF_CHANNEL_POOL_SIZE='+str(poolsize)
       cmd = cmd +' DEFINES+=CONF_CHANNEL_A='+str(channel_a)+' DEFINES+=CONF_CHANNEL_B='+str(channel_b)
       myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
    except Exception:
        print 'sender binary compile error: ', myOutput
        pass
#-------------------------------------------------------------------------------
def createSenderIHEX(poolsize):
    print 'compiling sender binary for  ch_pool_size=',poolsize

    myOutput=''
    try:
       channel_a = ((poolsize & 0x00F0) >> 4)
       channel_b = (poolsize & 0x000F)

       cmd ='make sender TARGET=sky DEFINES=NODE_IS_SENDER DEFINES+=CONF_CHANNEL_POOL_SIZE='+str(poolsize)
       cmd = cmd +' DEFINES+=CONF_CHANNEL_A='+str(channel_a)+' DEFINES+=CONF_CHANNEL_B='+str(channel_b)
       myOutput=subprocess.Popen(cmd.split(),  stdout=subprocess.PIPE).communicate()[0]
    except Exception:
       print 'sender binary compile error: ', myOutput
       pass
def createInitIHEX():
    print 'ninitial IHEX FILE'
    myOutput=''
    try:
       cmd ='make sender TARGET=sky DEFINES=NODE_IS_SENDER '
       myOutput=subprocess.Popen(cmd.split(),  stdout=subprocess.PIPE).communicate()[0]
    except Exception:
       print 'sender binary compile error: ', myOutput
       pass
#-------------------------------------------------------------------------------
#small problem here.. /binares
def changeIHEXFileName(srcFile, caseId):
    cmd = 'mv binaries/'+srcFile+' binaries/case'+str(caseId)+srcFile
    myOutput=subprocess.Popen(cmd.split(),  stdout=subprocess.PIPE).communicate()[0]

#-------------------------------------------------------------------------------
def createIHEX(comp_case):
    notify2Exec("rm -rf obj_* *~ symbols.* *.sky *.map *.a")
    createReceiverIHEX(comp_case)
    #rename the source IHEX
    changeIHEXFileName('isa_receiver.ihex', comp_case)
    notify2Exec("rm -rf obj_* *~ symbols.* *.sky *.map *.a")
    #create the Sender IHEX
    createSenderIHEX(comp_case)
    #rename the sender IHEX
    changeIHEXFileName('isa_sender.ihex', comp_case)
#-------------------------------------------------------------------------------
def uploadIHEX():
    for g in gatewaysList:
        print 'Upload IHEX for:',g.supernode
        g.uploadIHEXAll()

#-------------------------------------------------------------------------------
def notify2Exec(cmdstr):
   print '===>server calling to execute ', cmdstr
   myOutput=subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE).communicate()[0]
#-------------------------------------------------------------------------------
def createFolder(foldername):
    cmd = 'mkdir results/'+foldername
    myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
#-------------------------------------------------------------------------------
def retrieveAtOnce(file):
    return open(os.path.join(os.path.abspath('./'),file),'rb').read()
#-------------------------------------------------------------------------------
def triggerNodeTx(moteid):
    cmd = './transmit '+str(moteid)
    print 'mote transmitting '
    p=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return p.returncode
#-------------------------------------------------------------------------------
def programReceiverMote(moteid):
    cmd ='make TARGET=sky upload-ihex FILE=isa_receiver.ihex MOTE='+str(moteid)
    print 'cmd: ', cmd
    p=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return p.returncode
#-------------------------------------------------------------------------------
def programReceiverMoteAll():
    cmd ='make TARGET=sky upload-ihex FILE=isa_receiver.ihex'
    print 'cmd: ', cmd
    p=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return p.returncode
#-------------------------------------------------------------------------------
def programSenderMote(moteid):
    cmd ='make TARGET=sky upload-ihex FILE=isa_sender.ihex MOTE='+str(moteid)
    print 'cmd: ', cmd
    p=subprocess.Popen(['ssh', supernode, cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return p.returncode
#-------------------------------------------------------------------------------
def wait4Sender2Finish(node_id):
    try:
       counter = int(0)
       time2wait = int(MAX_TX_PACKETS*0.01 + MAX_SYNCH_PKTS*0.01 +5*1)
       print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
       print '==>waiting for node ', node_id,' to finish TX in ', (time2wait - counter),' seconds'
       while (time2wait > counter):
           time.sleep(1)
           counter = int(counter + 1)
           if counter % 10 == 0:
               print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
               print '==>waiting for node ', node_id,' to finish TX in ', (time2wait - counter),' seconds'
    except:
        print 'error while waitin for node to tx'
def sleepApp(slptime):
     time2Sleep = int(slptime)
     try:
        for t in range(0,time2Sleep):
            time.sleep(0.5)
     except Exception:
        print 'error waiting after re/programming sensors as receivers'
#-------------------------------------------------------------------------------
def getGateways():
    global gatewaysList #gateway_ips
    return gatewaysList[:]
#-------------------------------------------------------------------------------
def programGatewaysRx():
    for g in gatewaysList[:]:
        g.programNodeAsRXAll()

def programGatewaysNodesRxAll(remoteFileName):
    queue = []
    startT= time.time()
    queue = Queue.Queue()
    for g in gatewaysList[:]:
        gTh = ParallelizeGatewayOps(queue, remoteFileName, 'progAsRxIHEXFileAll')
        gTh.setDaemon(True)
        gTh.start()
    #fill the queue..
    for g in gatewaysList[:]:
        queue.put(g)

    queue.join()
    endT = time.time()
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '===>Programming all nodes lasted for: ',(endT-startT)
#-------------------------------------------------------------------------------
def retrieveData(snode, caseid, folder):

    nodes_queue    = []
    startT= time.time()

    nodes_queue = Queue.Queue()

    for g in gatewaysList[:]:
        dt = NodeDownloadThread(nodes_queue, snode, caseid, folder)
        dt.setDaemon(True)
        dt.start()
    #fill the queue..
    for g in gatewaysList[:]:
        nodes_queue.put(g)

    nodes_queue.join()
    endT = time.time()

    nodes_queue    = []
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '===>Downloading data Files on Gateways lasted for: ',(endT-startT)
#-------------------------------------------------------------------------------
def genmask():
    MAX_CH = 15
    channels=[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    for i in range(0, MAX_CH):    
        for j in range(i+1, MAX_CH +1):
            mask = 0x0F00
            mask = (mask |((i << 4) & 0x00F0) | (j & 0x000F))

            a = ((mask & 0x00F0) >> 4)
            b = (mask & 0x000F)
            casesList.append(mask)
            #print mask,' ',           
            print channels[a],'.', channels[b],mask,
            #print i,'.',j, ' ',
        print '\n'
def addGateways():
    global gateway_ips, casesList

    queue = []
    #create gateways
    for s in gateway_ips[:]:
        print '==>>Adding Gateway: ', s
        gatewaysList.append(Gateway(s, casesList[:]))

def createAndUploadInitIhex():
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '===>Creating an Initial IHEX'
    #createInitIHEX()
#    #upload initial binary
#    #CAN BE PARALLELIZED
    startT= time.time()
    queue = Queue.Queue()
    for g in gatewaysList[:]:
        gTh = ParallelizeGatewayOps(queue, 'isa_sender.ihex', 'initHEX')
        gTh.setDaemon(True)
        gTh.start()
    #load the program to be executed..
    for g in gatewaysList[:]:
        queue.put(g)

    queue.join()
    endT = time.time()

    time.sleep(20)

def createNetworkNodes():
    global gateway_ips, casesList

    queue = []
    queue = Queue.Queue()
    startT= time.time()
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '===>Creating Network....'
    for g in gatewaysList[:]:
        gTh = ParallelizeGatewayOps(queue, '', 'createNetwork')
        gTh.setDaemon(True)
        gTh.start()

    for g in gatewaysList[:]:
        queue.put(g)

    queue.join()
    endT = time.time()
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '===> Full network created in:',(endT-startT),' seconds'

def createAllBionaries():
    print '===>Creating all binaries'
#    for c in casesList[:]:
#        createIHEX(c)

    #upload all Binaries
    #CAN BE PARALLELIZED
#    queue = []
#    queue = Queue.Queue()
#    startT= time.time()
#    print '===>Uploading All Binaries...'
#    for g in gatewaysList[:]:
#       gTh = ParallelizeGatewayOps(queue,  '', 'caseHEX')
#       gTh.setDaemon(True)
#       gTh.start()
#
#    for g in gatewaysList[:]:
#        queue.put(g)
#
#    queue.join()
#    endT = time.time()
#    print '===>Uploading binaries lasted ', (endT-startT),' seconds'

def experimentRun(snode):
    global gateway_ips, casesList

    ##TESTEEEETE WORKS
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '===>Starting Experiment'
    for idx, case in enumerate(casesList[:]):
        #if True:
        #currCase  = 3949
        currCase = casesList[len(casesList)-idx-1-40]
        a= ((0x000F & currCase)+11)
        b= (((0x00F0 & currCase)>>4)+11)

        folderName = 'Task3/Tsch'+str(b)+str('_')+str(a)+'/'
        #create folder to save the results
        print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
        print '===>Creating folder ',folderName
        createFolder(folderName)

        targetGW   = ''
        targetNode =''
        nodesList  = []

        for g in gatewaysList[:]:
          if g.supernode == '192.168.200.13': # and g.supernode == '192.168.200.13':
            #targetGW = g
            #    break

            nodesList = []
            nodesList = g.getNodes()
            #nodesList  = targetGW.getNodes()
            #Now that we know our Node, let's start...with the cases
            #fileCase = '' #Files need a specific formatation

            #for node in nodesList[len(nodesList)-2:]:
            for node in nodesList[:]:
                targetNode = node
                print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                print '==>case: CH_POOL_SIZE=',currCase                

                #fileCase = 'link'+str(experiment_cases[currCase])+'n'+str(len(channel_cache[int(currCase)]))
                print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                print '===>Programming GWs'
                remoteRxFileName = './binaries/case' + str(currCase) + 'isa_receiver.ihex'

                #programGatewaysNodesRxAll(remoteRxFileName)
                queue = []
                startT= time.time()
                queue = Queue.Queue()
                for gw in gatewaysList[:]:
                    gTh = ParallelizeGatewayOps(queue, remoteRxFileName, 'progAsRxIHEXFileAll')
                    gTh.setDaemon(True)
                    gTh.start()
                #fill the queue..
                for gw in gatewaysList[:]:
                    queue.put(gw)

                queue.join()
                endT = time.time()
                queue = []
                print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                print '===>Programming all nodes lasted for: ',(endT-startT)

                sleepApp(6) #pause for a while

                nodeID =  targetNode.getNodeID()

                print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                print '===>Programming SenderNode:',nodeID
                remoteTxFileName='./binaries/case'+str(currCase)+'isa_sender.ihex'

                targetNode.programNodeWithIHEXFile(remoteTxFileName)

                sleepApp(22) #sleep a while (22)

                print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                print '===>Starting Transmission on: ',nodeID
                targetNode.triggerNodeTx()  #start TX

                wait4Sender2Finish(targetNode.getNodeID())

                print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                print '==>Retrieving Data from GATEWAYS......'
                #retrieveData(targetNode.getNodeID(), '', folderName)

                nodes_queue    = []
                startT= time.time()
                nodes_queue = Queue.Queue()

                for gw in gatewaysList[:]:
                    dt = NodeDownloadThread(nodes_queue, nodeID, '', folderName)
                    dt.setDaemon(True)
                    dt.start()
                #fill the queue..
                for gw in gatewaysList[:]:
                    nodes_queue.put(gw)

                nodes_queue.join()
                endT = time.time()

                nodes_queue    = []
                print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
                print '===>Downloading data Files on Gateways lasted for: ',(endT-startT)

if __name__ == '__main__':
    #generate masks
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '>>=========     GENERATING MASKS/CASES     ============='
    genmask()

    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '\n>>=========RUNNING EXPERIMENT TASK 3a,b,c) ============='
    #experimentRun('7')
    #Add Gateways
    print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
    print '===> adding gateways:',gateway_ips
    addGateways()

    #Init 
    createAndUploadInitIhex()

    #Add nodes to Gateways
    createNetworkNodes()
    
    #
    #createAllBionaries()


    #
    experimentRun('7')

#########################################################
#                    if g.supernode == '192.168.200.13':
#                        targetGW = g
#                        break
#
#                if targetGW == '':
#                    print 'No Gateway found...'
#                    return

    
