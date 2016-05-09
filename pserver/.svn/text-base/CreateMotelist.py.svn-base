'''
Created on Apr 27, 2011

@author: olaf
'''


import subprocess
import csv

def motelist(supernode):
    p = subprocess.Popen(['ssh', supernode, ' ps -ux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print 'ERROR!'
        print stderr
    else:
        sList = stdout.splitlines()
        ret = []
        for line in sList:
            ret.append(line)
        return ret

def dumpConfigFile(outFileName, supernodeList):
    outF = open(outFileName, 'wb')    
    writer = csv.writer(outF, delimiter='\t')
    #writer.writerow(('id', 'dev', 'name', 'supernode', 'nodeid'))
    id = 1
    for supernode in supernodeList:
        nodes = motelist(supernode)
        if nodes != None:
            for node in nodes:
                node.append(supernode)
                node.append(id)
                id += 1  
                writer.writerow(node)
    outF.close()

if __name__ == '__main__':
    #dumpConfigFile('nodelist.conf', ('192.168.200.10','192.168.200.11', '192.168.200.12'))
    dumpConfigFile('nodelist.conf', ('130.237.43.144'))
