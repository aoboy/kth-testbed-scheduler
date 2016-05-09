#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from wave import Error
import sys, os
import time, random
sys.path.insert(0,os.pardir)	# to find testserver.py

import demoserver

import Pyro.core, Pyro.util

import subprocess
from threading import Thread

import math

global abort, channelcase

abort = 0
channelcase=''

CHUNK_SIZE = 500000

MAX_TX_PACKETS = int(16*640)
MAX_SYNCH_PKTS = 100
######## object that does the callbacks

class CallbackThing(Pyro.core.ObjBase):
	  def __init__(self):
		  Pyro.core.ObjBase.__init__(self)
		  self.clients = []
		  self.rxBinaryFile         = "isa_receiver.ihex"
		  self.txBinaryFile         = "isa_sender.ihex"
		  self.currFile             =''

		  self.isCompiling          = None
		  #self.ch_pool_size = [4, 8, 16, 17, 18, 19, 20, 21, 22]
		  self.ch_pool_size = [12]
		  self.rootdir=os.path.abspath('./')
		  print "File server serving from",self.rootdir
		  self.ascii_extend = ['€', 'ƒ', '„', '†', '‡', '‰', 'Š', '‹', 'Œ', 'Ž', '‘', '’', '“', '”', '•', '–',
				      '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '¡', '¢', '£', '¤', '¥', '¦', '§', '©',
				      'ª', '«', '¬', '®', '¯', '°', '±', '²', '³', 'µ', '¶', '¹', 'º', '»', '¼', '½',
				      '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ë', 'Ì', 'Í', 'Î',
				      'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ',
				      'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î',
				      'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ',
				      'ÿ']
						  
		  thread=Thread(target=self.mainloop)
		  thread.start()
		  print 'main thread created'

		  
	  def register(self, client):
                  if client not in self.clients:
                        print 'REGISTERING: ', client

                        self.clients.append(client)
                        print 'entry n: ', len(self.clients)
		  #client._setOneway('callback') # don't wait for results for this method

	  def get_sndr_file(self):
	      return self.txBinaryFile

	  def get_recv_file(self):
	      return self.rxBinaryFile

	  def retrieveAtOnce(self, file):
		  return open(os.path.join(self.rootdir,file),'rb').read()
	  def openFile(self,file):
		  if hasattr(self.getLocalStorage(), "openfile"):
			  raise IOError("can only read one file at a time, close previous file first")
		  file=os.path.join(self.rootdir,file)
		  self.getLocalStorage().openfile=open(file,'rb')
		  return os.path.getsize(file)
	  def retrieveNextChunk(self):
		  chunk= self.getLocalStorage().openfile.read(CHUNK_SIZE)
		  if chunk:
			  return chunk
		  self.getLocalStorage().openfile.close()
		  return ''
	  def closeFile(self):
		  self.getLocalStorage().openfile.close()
		  del self.getLocalStorage().openfile

	  def set_is_compiling(self):
	      self.isCompiling = True

	  def reset_is_compiling(self):
	      self.isCompiling = False

	  def notify_to_exec(self, cmdstr):
		  print 'server calling to execute ', cmdstr
		  myOutput=subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE).communicate()[0]
		  print myOutput

	  def compile_receiver_binary(self, poolsize):
		  print 'compiling receiver binary for ch_pool_size=', poolsize

		  self.set_is_compiling()

		  myOutput=''
		  try:
		      cmd ='make recvbin TARGET=sky DEFINES=NODE_IS_RECEIVER DEFINES+=CONF_CHANNEL_POOL_SIZE='+str(poolsize)#+str(' isa_receiver.ihex')
		      myOutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
		  except Exception:
		    print 'sender binary compile error: ', myOutput
		    
		  self.reset_is_compiling()

	  def compile_sender_binary(self, poolsize):
		print 'compiling sender binary for  ch_pool_size=',poolsize
		
		self.set_is_compiling()
		myOutput=''
		try:
		      #cmd = 'make sender '+cmdstr
		      cmd ='make sender TARGET=sky DEFINES=NODE_IS_SENDER DEFINES+=CONF_CHANNEL_POOL_SIZE='+str(poolsize) #+str(' isa_sender.ihex')
		      print '', cmd
		      
		      myOutput=subprocess.Popen(cmd.split(),  stdout=subprocess.PIPE).communicate()[0]
		except Exception:
		    print 'sender binary compile error: ', myOutput
		    
		self.reset_is_compiling()
		
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

			  n = int(c, 16)

			  if n != next_n:
			      return False
			  else:
			      next_n = (n + 16)
		  #end of IF
	      if got_filename == True:
		  return True
	      else:
		  return False
	  

	  def save_data_to_file(self, data):
	      #print 'save data to file'

	      got_filename = None
	      node_is_tx   = None
	      filename = ''
	      file=''
	      for substr in data.split('\n'):
		  if got_filename == None:
		      idx = substr.find('r:')

		      if idx != -1:
			  filename = 'Nchannels'+str(channelcase)+str(substr[(idx + 2):])
			  got_filename = True
			  file = open(filename, 'wb')
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
			      #file.write(c+'\n')
			      file.write(substr+'\n')
			  
		  #end of IF
	      return True
	    

	  def print_topology(self):
		  for c in self.clients[:]:		# use a copy of the list
			  try:
				  print '+++++++++++++++++++++++++++++++++++++++++'
				  print 'Gateway: ',c.get_hostname()
				  print '========================================='
				  print '[mote_id,   dev]'

				  mote_id = int(1)
				  for mote in c.get_motelist():
				      if mote:
					  print '[', mote_id,' ', mote, ']'
					  mote_id = int(mote_id + 1)

			  except Pyro.errors.ConnectionClosedError,x:
				  # connection dropped, remove the listener if it's still there
				  # check for existence because other thread may have killed it already
				  if c in self.clients:
					  self.clients.remove(c)
					  print 'Removed dead listener',c
	      
	  def shout(self, message):	
		  print 'Got shout:',message
		  # let it know to all clients!
		  for c in self.clients[:]:		# use a copy of the list
			  try:
				  #print c.get_hostname(), 'shouted ', c.get_motelist()
				  #self.print_topology()
				  #c.download_mote_data(1)
				  time.sleep(2)
				  #c.callback('hello: '+c.get_hostname()) # oneway call
			  except Pyro.errors.ConnectionClosedError,x:
				  # connection dropped, remove the listener if it's still there
				  # check for existence because other thread may have killed it already
				  if c in self.clients:
					  self.clients.remove(c)
					  print 'Removed dead listener',c

	  def get_gateways(self):
	      gws=[]
	      for gw in self.clients[:]:
		  gws.append(gw)
	      
	      return gws
	      
	  def print_g(self):
	      global abort
	      print 'gongaaaaaaaaaa'
	      abort = 1

	  def testfunc(self):
	      print 'testfunccccccc'

	  def mainloop(self):            
	      global abort, channelcase
	      #object=objectURI.getProxy()  # we get our own proxy object because we're running in our own thread.
	      print 'SchedulerServer thread is running.'
	      n = int(1)

	      #self.testfunc()
	      
	      while abort != 1 and len(self.clients[:]) != 1:
		  try:
		      time.sleep(1)
		      n = int(n+1)
		      #for every 10 seconds we print a message
		      if(n%5 == 0):
			  print '==>waiting for all gateways to log in'
			  print '==>len:', len(self.clients[:])
		  except Error:
		      print 'an error occured here:.::.'
	      ######we wait for 5 seconds to
	      try:
		  time.sleep(5)
	      except Exception:
		  print 'error while sleeping'

	      #lets print how many motes are attached to each gateway
	      print '==>printing topology'
	      self.print_topology()
	      ######We loop for each case
	      for case in self.ch_pool_size[:]:
		  try:
		      print '==>case: CH_POOL_SIZE=',case
		      channelcase=str(case)
		      if case == 17:
			channelcase=str('CH22')
		      if case == 18:
			channelcase=str('CH16')
		      if case == 19:
			channelcase=str('CH12')
		      if case == 20:
			channelcase=str('CH2622')
		      if case == 21:
			channelcase=str('CH262216')
		      if case == 22:
			channelcase=str('CH26221612')
		      #compile sender_binary
		      #self.notify_to_exec("make delete")
		      #print '==>compile sender binary'
		      #self.compile_sender_binary(case)
		      ##compile receiver binary
		      #print '==>compile receiver binary'
		      #self.compile_receiver_binary(case)

		      #now we start for the first gateway
		      gateways=[]
		      gateways = get_gateways()

                      print 'len_gateways:', len(gateways)
		      for gw in gateways:
                            print 'using: ', gw.get_hostname()
                            for igw in gateways:
                                    try:
                                        self.notify_to_exec("make delete")
                                        print '==>compile receiver binary'
                                        self.compile_receiver_binary(case)
                                        print '==>copy binary to remote client:', igw.get_hostname()

                                        data = self.retrieveAtOnce(self.rxBinaryFile)

                                        igw.upload_receiver_binary(data)

                                        try:
                                            for t in range(0, 3):
                                                time.sleep(1)
                                        except Exception:
                                            print 'error sleep after upload..'

                                        data =[]
                                        self.notify_to_exec("make delete")
                                        print '==>compile sender binary'
                                        self.compile_sender_binary(case)
                                        data = self.retrieveAtOnce(self.txBinaryFile)
                                        igw.upload_transmitter_binary(data)

                                        #since the binary its there already, we program the receivers
                                        print '==>programming receiveris on: ',igw.get_hostname()
                                        igw.program_all_motes_receivers()

                                        print '==> programming receivers finished...'

                                        igw.notify_to_exec('make sky-reset')

                                    except Exception:
                                        print 'something went wrong when programming all receivers'
			    #end of for igw in self.clients[:]:

			    #we wait till all the motes boot up, after approx 10sec
			    try:
                                for t in range(0,9):
                                    time.sleep(1)
                            except Exception:
                                print 'got problem while waiting motes to boot up'

                            #now we start on the first gateways, by getting its list of
                            #motes and
                            mote_id = 1 #we start on the first mote on that gateway
                            moteList = gw.get_motelist()

                            for mote in moteList:
                                print '==>programming mote=', mote_id, 'on ', gw.get_hostname()
                                gw.program_tx_mote(mote_id)

                                #make the nodes reboot
                                #we wait  the node to reboot
                                try:
                                    for t in range(0,5):
				      time.sleep(1)
				      
                                    gw.notify_to_exec('make sky-reset')
                                except Exception:
                                    print 'sleep exception....'

                                #we wait  the node to reboot
                                try:
                                    for t in range(0,5):
				      time.sleep(1)
                                except Exception:
                                    print 'sleep exception....'

                                #we trigger transmission on the node
                                print '==>trigger tx on mote=', mote_id
                                gw.start_mote_tx(mote_id) #MAX_TX_PACKETS

                                #now we wait for the tx to finish
                                try:
                                    counter = int(0)
                                    time2wait = int(MAX_TX_PACKETS*0.01 + MAX_SYNCH_PKTS*0.01 +5*1)

                                    while (time2wait > counter):
                                        time.sleep(1)
                                        counter = int(counter + 1)
                                        if (counter % 10 == 0):
                                            print 'waiting4Tx to finish in ', (time2wait - counter),' seconds'

                                except Exception:
                                    print 'error while waitin for node to tx'

                                #since we are finished transmitting, we collect results
                                #on all boxes..
                                for box in self.clients[:]:
                                    boxmoteList = box.get_motelist()
                                    box_mote_id = 1

                                    for m in boxmoteList:
                                        queryCtr = int(0)

                                        while queryCtr < 2:
                                            box.download_mote_data(box_mote_id)

                                            my_counter = int(0)
                                            while (box.is_downloading_files()):
                                                my_counter = int(my_counter +1)
                                                time.sleep(0.1)
                                                if ( my_counter % 10 == 0):
                                                    print '==>waiting for ', box.get_hostname()+'.mote['+box_mote_id+'] to upload file'
                                            #end of (box.is_downloading_files()):

                                            box.download_files_reset()

                                            queryCtr = int (queryCtr + 1)
                                        #end of queryCtr < 2:
                                        #we increment the box_mote_id
                                        box_mote_id = int(box_mote_id + 1)
                                    #end of for m in boxmoteList:
                                    #box.notify_to_exec('make sky-reset')

                                    for t in range(0,3):
                                        time.sleep(1)
                                #end of for box in self.clients[:]: #data collection as well

                                #"download is now over, we reprogram the former sender as receiver
                                #and increment the mote_id
                                try:
                                    gw.program_rcv_mote(mote_id)

                                    for t in range(0,4):
                                        time.sleep(1)
                                except Exception:
				  print 'reprogramming tx-to-rx error'

                                #we increment the motelist
                                mote_id = int(mote_id + 1)
                            #end of for mote in moteList:
                      #end gw in gateways:...

		  except Exception:
		      print 'we have got a problem here.'

	      #end of for case in self.ch_pool_size: exit_experiment
	      print 'poling clients to terminate execution'
	      for c in self.clients[:]:
		  try:
		      c.exit_experiment()
		  except Exception:
		      pass
	      #
	      print 'end of experiment....'
	      cmd ='kill -9 $(pidof /usr/bin/python /usr/local/bin/pyro-ns)'
	      myoutput=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

	      print 'killing pyro-ns: ', myoutput

	      exit(1)
	      

demoserver.start(CallbackThing,'callback')

  # while not abort:
  #                for n in self.ch_pool_size:
  #                    try:
  #                        print 'ch_pool: ', n
  #                        time.sleep(3)
  #
  #                    except KeyboardInterrupt:
  #                        abort = 1
  #                        print 'Main thread shutting down gracefully.'
  #                abort = 1
  #            print 'Main thread shutting down gracefully.'
