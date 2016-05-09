'''
Created on May 9, 2011

@author: olaf
'''
import subprocess
import shlex
import sys

server = 'olaf@wsntestbed.s3.kth.se'
path = 'testbed/'
remoteNodeList = 'nodelist.conf'
remoteExpConf = 'exp.conf'

def execute(commandLine):
    #print commandLine
    args = shlex.split(commandLine)
    #print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print 'ERROR!'
        #print stdout
        print stderr
        exit(-1)
    #return stdout

def createExp(name, nodeList):
    print 'init, ',
    sys.stdout.flush()
    execute('ssh ' + server + ' mkdir ' + path + name)
    print 'copy node list, ',
    sys.stdout.flush()
    execute('scp ' + nodeList + ' ' + server +':' + path + name + '/' + remoteNodeList)       
    print 'copy run script, ',
    sys.stdout.flush()
    execute('ssh ' + server + ' cp projects/testbed/code/runExp.sh ' + path + name )
    #execute('scp ' + server + ':projects/testbed/code/runExp.sh ' + server +':' + path + name + '/runExp.sh' )       
    print('done')
                
def addExp(name, fwName, fw, duration):
    #copy fw
    print 'add to config, ',
    sys.stdout.flush()
    execute('ssh ' + server + ' echo -e "' + fwName + '.exe,' + duration + '" >> ' + path + name + '/' + remoteExpConf)
    #add to conf: fw, duration, nodelist, dump
    print 'copy fw, ',
    sys.stdout.flush()
    execute('scp ' + fw + ' ' + server +':' + path + name + '/' + fwName + '.exe' )       
    print('done')
    
def updateExp(name, fwName, fw):    
    print 'copy fw, ',
    sys.stdout.flush()
    execute('scp ' + fw + ' ' + server +':' + path + name + '/' + fwName + '.exe' )       
    print('done')
    
def run():
    if sys.argv[1] == 'create':
        createExp(sys.argv[2], sys.argv[3])
    if sys.argv[1] == 'add':
        addExp(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    if sys.argv[1] == 'update':
        updateExp(sys.argv[2], sys.argv[3], sys.argv[4])
    
if __name__ == '__main__':
    run()
    #createExp('test', 'nodelist.conf')
    #addExp('test', 'TestSerial.exe', '1' )
    #addExp('test', 'TestSerial.exe', '2' )
    #addExp('test', 'TestSerial.exe', '1' )
