#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import time, random
import Pyro.core
import Pyro.naming
from Pyro.errors import *
from threading import Thread
from socket import gethostname
import subprocess
import sys, signal, os

global serverURI, abort

motelist= {}

abort=0

class Listener(Pyro.core.ObjBase):
	def __init__(self):
                Pyro.core.ObjBase.__init__(self)
                self.hostname             = gethostname()
                self.isProgrammingNode    = None
                self.isDownloadingFiles   = None
                self.isDataCorrect        = None               
                self.mote_list             = {}
                self.rxBinaryFile         = "isa_receiver.ihex"
                self.txBinaryFile         = "isa_sender.ihex"

                self.ascii_extend = ['€', 'ƒ', '„', '†', '‡', '‰', 'Š', '‹', 'Œ', 'Ž', '‘', '’', '“', '”', '•', '–',
                                     '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '¡', '¢', '£', '¤', '¥', '¦', '§', '©',
                                     'ª', '«', '¬', '®', '¯', '°', '±', '²', '³', 'µ', '¶', '¹', 'º', '»', '¼', '½',
                                     '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ë', 'Ì', 'Í', 'Î',
                                     'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ',
                                     'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î',
                                     'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ',
                                     'ÿ']      

	def callback(self, message):
		print 'GOT CALLBACK: ',message

        def get_hostname(self):
            return gethostname()
        
        def upload_transmitter_binary(self, bindata):
                print 'uploading binary data <', self.txBinaryFile,'>'
                fileobj = open(self.txBinaryFile,  "wb")
                fileobj.write(bindata)
                fileobj.close()

        def upload_receiver_binary(self, bindata):
                try:
                    print 'uploading binary data <', self.rxBinaryFile,'>'
                    fileobj = open(self.rxBinaryFile, "wb")
                    fileobj.write(bindata)
                    fileobj.close()
                except IOError, ex:
                    print ex
                
        def program_rcv_mote(self, moteid):
                self.isProgrammingNode=True
                cmd ='make TARGET=sky upload-ihex FILE=isa_receiver.ihex MOTE='+str(moteid)
                print 'cmd: ', cmd
                myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
               
                self.isProgrammingNode=False
                
                #return myOutput

        def program_all_motes_receivers(self):
                self.isProgrammingNode=True

                cmd ='make TARGET=sky upload-ihex FILE=isa_receiver.ihex'
                print 'cmd: ', cmd
                
                myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

                self.isProgrammingNode=False

               #print 'out>> ', myOutput
                
        def program_tx_mote(self, moteid):
                self.isProgrammingNode=True

                cmd ='make TARGET=sky upload-ihex FILE=isa_sender.ihex MOTE='+str(moteid)
                print 'cmd: ', cmd
                
                myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

               
                self.isProgrammingNode=False

                #return myOutput

        def notify_to_exec(self, cmdstr):
                print 'server calling to execute ', cmdstr
                myOutput=subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE).communicate()[0]
                print myOutput

        def check_data_integrity(self, data):
            print 'checking data integrity'

            got_filename = None
            node_is_tx   = None
            filename = ''
            n = 0
            next_n = 0
            for substr in data.split('\n'):
                if got_filename == None:
                    idx = substr.find('r:')

                    if idx != -1:
                        filename = substr[(idx + 2):]
                        got_filename = True
                else:

                    if substr.find('E') != -1 or substr.find('END') != -1:
                        return True

                    if substr.find('-') != -1 and substr.find('link') == -1:
                        c = substr.split('-')[0]
                        #get rid of all unwanted characters.......
                        for unwanted in self.ascii_extend:
                            if c.find(unwanted) != -1:
                                c.replace(unwanted, '')
                        if c.find('E') != -1 or c.find('END') != -1:
                            return True
                        try:
                           n = int(c, 16)

                           if n != next_n:
                             return False
                           else:
                             next_n = (n + 16)
                        except:
                           pass
                #end of IF
            if got_filename == True:
                return True
            else:
                return False

        def download_mote_data(self, moteid):
                self.isDownloadingFiles=True
                
                cmd = './sconnect '+str((int(moteid)-1))
                print 'downloading data at ', cmd

                myoutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

                if myoutput.find('node_tx') != -1:
                    #node is a tx, skeep
                    self.isDownloadingFiles=False
                    return
                else:
                    if self.check_data_integrity(myoutput) == True:
                        obj=serverURI.getProxy()
                        obj.save_data_to_file(myoutput)

                        self.isDownloadingFiles=False
                    else:
                        self.isDownloadingFiles=True
                #print myoutput
                #get rid of the process...
                #os.kill(proc.pid, signal.SIGUSR1)
                #obj=serverURI.getProxy()
                #if obj.check_data_integrity(myoutput):
                #    obj.save_data_to_file(myoutput)
                
                

        def start_mote_tx(self, moteid):
                cmd = './transmit '+str(moteid)
                print 'mote transmitting '

                proc=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

                #get rid of the process...
                #os.kill(proc.pid, signal.SIGUSR1)

        def is_programming_mote(self):
                return self.isProgrammingNode

        def programming_mote_reset(self):
                self.isProgrammingNode = None

        def is_downloading_files(self):
            return self.isDownloadingFiles

        def download_files_reset(self):
            self.isDownloadingFiles = None

        def set_motelist(self):
            print 'setting motes list'    

            self.mote_list  = []
            cmd = 'make sky-motes'
            myoutput = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

            for mote in myoutput.split():
                if mote:
                    self.mote_list.append(mote)



        def get_motelist(self):
                      
                copymotelist  = []
                cmd ='make sky-motes'
                myoutput = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

                print 'motes: ',myoutput
                #for mote in myoutput.split():
                for mote in myoutput.split(): #use the copy of the list instead
                    if mote and mote.find('/dev/ttyUSB') != -1:
                        copymotelist.append(mote)                      

                return copymotelist #myoutput #

        def get_devid_by_motename(self, mote_name):
            dev_id = ''
            cmd = 'motelist '
            myoutput =subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

            for m in myoutput.split('\n'):
                if m.find(mote_name) != -1:
                    devid = m.split()[1]
                    dev_id= devid[devid.find('USB')+3]
                    break;
            return dev_id

        def get_node_id(self, usb_idx):
            usb_devs=[]
            cmd = './node_id '+str(int(usb_idx))

            node_id=''

            myoutput =subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
            
            for myid in myoutput.split():
                try:
                    if myid.find('id:') != -1:
                        id_idx = myid[(myid.find('id:')+3):]
                        node_id = str(id_idx)
                        break
                except Exception:
                    print 'error getting node_ids'

            return node_id

        def add2cache(self, cached):
            global motelist
            motelist={}
            cache2=cached.split(',')

            for a in cache2:
                idx= a.find(':')
                key = a[:(idx)]
                val = a[(idx+1):]
                motelist[key] = val

        def get_cache(self):
            motes = self.get_motelist()
            mydic=''

            for mote in motes:
                cache_idx = mote[(mote.find('USB')+3):]

                node_id = self.get_node_id(cache_idx)

                if int(node_id):
                    if mydic == '':
                        mydic += str(cache_idx)+str(':'+node_id)
                    else:
                        mydic += ','+ str(cache_idx)+str(':'+node_id)
            #
            self.add2cache(mydic)
            return motelist

        def exit_experiment(self):
            global abort
            abort = 1
            cmd ='kill -9 $(pidof python)'
            myoutput = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
            sys.exit(0)

def shouter(objectURI):
	global abort
	object=objectURI.getProxy()  # we get our own proxy object because we're running in our own thread.
	print 'Shouter thread is running.'
        n = int(1)
	while not abort:
		print 'Shouting something'
		#object.shout('Hello out there!')
		time.sleep(random.random()*3)
                if n == 2:
                    break
                n = int(n+1)
	print'Shouter thread is exiting.'	


def main():
	global abort, serverURI
	Pyro.core.initServer()
	Pyro.core.initClient()
	daemon = Pyro.core.Daemon(host="192.168.200.10")
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
		#print 'Waiting for notification...'
		try:
			daemon.handleRequests()
		except KeyboardInterrupt:
			abort=1
			thread.join()
	print 'Exiting.'		

if __name__=='__main__':
	main()

