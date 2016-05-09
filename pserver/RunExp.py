'''
Created on Apr 28, 2011

@author: olaf
'''

# copy firmware
# program motes
# start serial fw on supernodes
# start serial fw on server, dump data
# wait until exp end
# stop serial fw on server
# stop serial fw on supernodes
# erase binaries from motes
# erase tmp file on server and gateways

import subprocess
import csv
import datetime, time
import shlex
import sys
import os

import CreateMotelist
from time import gmtime, strftime


fwBase = 9000    
nodeList = 'nodelist.conf'
expConf = 'exp.conf'

class Node:        
    def __init__(self, id, dev, name, supernode, nodeId):
        self.id = id
        self.dev = dev
        self.name = name
        self.supernode = supernode
        self.nodeId = nodeId
        self.sfPid = None
        
class Exp:        
    def __init__(self, fw, duration):
        self.fw = fw
        self.duration = duration

class ExpError(Exception):
    pass

def execute(commandLine):
    #print commandLine
    args = shlex.split(commandLine)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print 'ERROR!'
        print stdout
        print stderr
        raise ExpError()
    return p.returncode, stdout

def fileName(t):
    return '/tmp/telosb_firmware_' + str(int(t))
    
#def iHex(inFileExe, outFileHex):
#    execute('msp430-objcopy --output-target=ihex ' + inFileExe + ' ' + outFileHex)
    
def setNodeId(iHexIn, iHexOut, nodeId):
    print 'set node ID, ',
    sys.stdout.flush()
    return execute('tos-set-symbols --objcopy msp430-objcopy --objdump msp430-objdump --target ihex ' + iHexIn + ' ' + iHexOut + ' TOS_NODE_ID=' + nodeId + ' ActiveMessageAddressC__addr=' + nodeId)

def copyFirmware(srcFile, supernode, dstFile):
    print 'copy fw, ',
    sys.stdout.flush()
    return execute('scp ' + srcFile + ' ' + supernode +':' + dstFile)       

def programNode(supernode, firmware, port):    
    print 'load fw, ',
    sys.stdout.flush()
    return execute('ssh ' + supernode + ' tos-bsl --telosb -c ' + port + ' -r -e -I -p ' + firmware)

def delFirmware(supernode, file):    
    print 'del fw, ',
    sys.stdout.flush()
    return execute('ssh ' + supernode + ' rm ' + file)
    
def startSfSupernode(supernode, fwPort, port):
    print 'start sf, ',
    sys.stdout.flush()
    return execute('ssh ' + supernode + ' \'nohup sf ' + fwPort + ' ' + port + ' 115200 1>/dev/null 2>&1 & echo $!\'')
    
def startSfServer(duration, file, clients):
    t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print '%s: running experiment, %s minute(s)...' % (t,duration)
    sys.stdout.flush()
    clientStr = ''
    for c in clients:
        clientStr += c + ' '
    return execute('java -cp /home/olaf/projects/testbed/code/java/bin:/opt/tinyos-2.1.1/support/sdk/java/tinyos.jar testbed.Dumper ' + duration + ' ' + file + ' ' + clientStr)

def stopSfSupernode(supernode, pid):
    print 'stop sf, ',
    sys.stdout.flush()
    return execute('ssh ' + supernode + ' kill ' + pid )

#def eraseNode(supernode, port):
#    print 'erase fw, ',
#    sys.stdout.flush()
#    return execute('ssh ' + supernode + ' tos-bsl --telosb -c ' + port + ' -r -e')

def printNodeId(nodeId, id):
    print( 'node ' + nodeId + '(' + id + '): '),
    sys.stdout.flush()

#def prepare(supernode, dev, nodeId, id):
#    printNodeId(nodeId, id)
#    #1. delete image from sensor node
#    ret, out = eraseNode(supernode, dev)    
#    print('done')
#    return ret,out

def start(fwFileName, id, supernode, nodeId, timeStamp, port, name):
    printNodeId(nodeId, id)
    iHexName = fileName(timeStamp) + '_' + nodeId + '.ihex'
    #1. set node id
    setNodeId(fwFileName, iHexName, nodeId)
    #2 copy
    copyFirmware(iHexName, supernode, iHexName)
    #3 install
    programNode(supernode, iHexName, port)
    #4 delete on supernode
    delFirmware(supernode, iHexName)
    #5. start serial forwarder on supernode
    _, pid = startSfSupernode(supernode, str(fwBase + int(nodeId)), port )
    print('done')
    return pid

def stop(supernode, dev, pid, nodeId, id):
    printNodeId(nodeId, id)
    #1. stop serial forwarder on supernode
    stopSfSupernode(supernode, pid)
    #2. delete image from sensor node
    #ret,out = eraseNode(supernode, dev)    
    print('done')
             
def runExp(fwFileName, confFileName, duration, dumpFile):
    print 'Loading new run:'
    f = open(confFileName, 'rb')
    reader = csv.reader(f, delimiter='\t')
    t = datetime.datetime.now()
    t = time.mktime(t.timetuple())
    #program each node, load sf
    nodes = []
    for row in reader:
        id, dev, name, supernode, nodeId = row
        nodes.append( Node(id, dev, name, supernode, nodeId) )
    clientList = []
    #for node in nodes: 
    #    prepare(node.supernode, node.dev, node.nodeId, node.id)    
    try:
        for node in nodes: 
            node.sfPid = start(fwFileName, node.id, node.supernode, node.nodeId, t, node.dev, node.name)
            clientList.append('sf@' + node.supernode + ':' + str(fwBase + int(node.nodeId)))
            clientList.append(node.nodeId)
        #start sf on server
        startSfServer(duration, dumpFile, clientList)
        #stop it all
    except ExpError:
        print 'programming falied, will cleanup now..'
    for node in nodes:
        if node.sfPid != None: 
            stop(node.supernode, node.dev, node.sfPid, node.nodeId, node.id)
    print 'Run done!'
        
def run(confPath, dumpPath):
    f = open(os.path.join(confPath,expConf), 'rb')
    reader = csv.reader(f, delimiter=',')
    exps = []
    for row in reader:
        fw, duration = row
        exps.append( Exp(fw, duration) )
    for i, exp in enumerate(exps):
        t = datetime.datetime.now()
        tstr = t.strftime('.%Y-%m-%d_%H-%M-%S')        
        print '%s: experiment %d of %d: %s' % (t.strftime('%Y-%m-%d %H:%M:%S'), (i + 1), len(exps), exp.fw)
        dumpPath = os.path.join(dumpPath, exp.fw + tstr)
        if not os.path.exists(dumpPath):
            os.mkdir(dumpPath) 
        runExp(os.path.join(confPath,exp.fw), os.path.join(confPath,'nodelist.conf'), exp.duration, os.path.join(dumpPath, 'trace.log'))
        
if __name__ == '__main__':
    nodeListFile = os.path.join(sys.argv[1], 'nodelist.conf')
    CreateMotelist.dumpConfigFile(nodeListFile, ('192.168.200.10','192.168.200.11', '192.168.200.12'))
    run(sys.argv[1], sys.argv[2])
    #run('../../../testbed/test/exp.conf')
