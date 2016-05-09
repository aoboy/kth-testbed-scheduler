#!/usr/bin/env python

import time, random
import Pyro.core
import Pyro.naming
from Pyro.errors import *
from threading import Thread
from socket import gethostname
import subprocess

class Listener(Pyro.core.ObjBase):
	def __init__(self):
                Pyro.core.ObjBase.__init__(self)
                self.hostname             = gethostname()
                self.isProgrammingNode    = None
                self.isDownloadingFiles   = None
                self.isDataCorrect        = None               
                self.motelist             = {}
                self.rxBinaryFile         = "receiver.ihex"
                self.txBinaryFile         = "sender.ihex"
                self.recv_cmd = 'make TARGET=sky upload-ihex FILE=receiver.ihex'
                self.sndr_cmd = 'make TARGET=sky upload-ihex FILE=sender.ihex'
	def callback(self, message):
		print 'GOT CALLBACK: ',message

        def get_hostname(self):
            return self.hostname
        
        def upload_tx_binary(self, bindata):
                print 'uploading binary data <', filename,'>'
                fileobj = open(self.txBinaryFile,  "wb")
                fileobj.write(bindata)
                fileobj.close()

        def upload_rcv_binary(self, bindata):
                print 'uploading binary data <', filename,'>'
                fileobj = open(self.rxBinaryFile, "wb")
                fileobj.write(bindata)
                fileobj.close()
                
        def program_rcv_mote(self, moteid):
                self.isProgrammingNode=True
                cmd ='make TARGET=sky upload-ihex FILE=receiver.ihex MOTE='+moteid
                print ''
                myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

                self.isProgrammingNode=False
                
                return myOutput

        def program_all_motes_receivers(self):
                self.isProgrammingNode=True

                cmd ='make TARGET=sky upload-ihex FILE=receiver.ihex'
                
                myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

                self.isProgrammingNode=False

                print 'out>> ', myOutput
                
        def program_tx_mote(self, moteid):
                self.isProgrammingNode=True

                cmd ='make TARGET=sky upload-ihex FILE=sender.ihex MOTE='+moteid
                
                myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

               
                self.isProgrammingNode=False

                return myOutput

        def notify_to_exec(self, cmdstr):
                print 'server calling to execute ', cmdstr
                myOutput=subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE).communicate()[0]
                print myOutput

        def download_mote_data(self, moteid):
                self.isDownloadingFiles=True
                
                cmd = './sconnect '+`(int(moteid)-1)`
                print 'downloading data'

                proc=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
               
                #get rid of the process...
                os.kill(proc.pid, signal.SIGUSR1)

                self.isDownloadingFiles=False

        def start_mote_tx(self, moteid):
                cmd = './transmit '+moteid
                print 'mote transmitting '

                proc=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

                #get rid of the process...
                os.kill(proc.pid, signal.SIGUSR1)

        def is_programming_mote(self):
                return self.isProgrammingNode

        def programming_mote_reset(self):
                self.isProgrammingNode = False

        def set_motelist(self):
            print 'setting motes list'    
            
        def get_motelist(self):
                #accs = {}
		#for moteid in motelist.keys():
		#	accs[moteid] = self.motelist[moteid].devname()
		#return accs
                self.motelist = []
                copymotelist  = []
                cmd ='make sky-motes'
                myoutput = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
    
                for mote in myoutput.split():
                    copymotelist.append(mote)
                    self.motelist.append(mote)

                return copymotelist

abort=0

def shouter(objectURI):
	global abort
	object=objectURI.getProxy()  # we get our own proxy object because we're running in our own thread.
	print 'Shouter thread is running.'
	while not abort:
		print 'Shouting something'
		object.shout('Hello out there!')
		time.sleep(random.random()*3)
	print'Shouter thread is exiting.'	


def main():
	global abort
	Pyro.core.initServer()
	Pyro.core.initClient()
	daemon = Pyro.core.Daemon()
	locator = Pyro.naming.NameServerLocator()
	NS = locator.getNS()
	daemon.useNameServer(NS)
	listener=Listener()
	daemon.connect(listener)
	serverURI=NS.resolve(':test.callback')
	server = serverURI.getProxy()
	server.register(listener.getProxy())

	thread=Thread(target=shouter, args=(serverURI,))
	thread.start()

	while not abort:
		print 'Waiting for notification...'
		try:
			daemon.handleRequests()
		except KeyboardInterrupt:
			abort=1
			thread.join()
	print 'Exiting.'		

if __name__=='__main__':
	main()

