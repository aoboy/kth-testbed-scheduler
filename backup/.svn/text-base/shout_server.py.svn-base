#!/usr/bin/env python
import sys, os
sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver

import Pyro.core, Pyro.util

import subprocess

######## object that does the callbacks

class CallbackThing(Pyro.core.ObjBase):
	def __init__(self):
                Pyro.core.ObjBase.__init__(self)
                self.clients = []
                self.rxBinaryFile         = "receiver.ihex"
                self.txBinaryFile         = "sender.ihex"

                self.isCompiling          = None
                self.rootdir=os.path.abspath(rootdir)
                self.ascii_extend = ['€', 'ƒ', '„', '†', '‡', '‰', 'Š', '‹', 'Œ', 'Ž', '‘', '’', '“', '”', '•', '–',
                                     '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '¡', '¢', '£', '¤', '¥', '¦', '§', '©',
                                     'ª', '«', '¬', '®', '¯', '°', '±', '²', '³', 'µ', '¶', '¹', 'º', '»', '¼', '½',
                                     '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ë', 'Ì', 'Í', 'Î',
                                     'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ',
                                     'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î',
                                     'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ',
                                     'ÿ']
		print "File server serving from",self.rootdir
                
	def register(self, client):
		print 'REGISTER',client
		self.clients.append(client)
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
        def close_file(self):
                print 'closing file'

        def compile_recv_binary(self, cmdstr):
                print 'compiling binary for ', cmdstr
                self.isCompiling = True

                cmd = 'make rcv '+cmdstr
                myOutput=subprocess.Popen([self.recv_cmd, 'MOTE='+moteid], stdout=subprocess.PIPE).communicate()[0]


        def compile_sndr_binary(self, cmdstr):
               print 'compiling binary for ', cmdstr
               self.isCompiling = True

               cmd = 'make sender '+cmdstr
               myOutput=subprocess.Popen([self.recv_cmd, 'MOTE='+moteid], stdout=subprocess.PIPE).communicate()[0]
               
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
                        for unwanted in ascii_extend:
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
            print 'checking data integrity'

            got_filename = None
            node_is_tx   = None
            filename = ''
            file=''
            for substr in data.split('\n'):
                if got_filename == None:
                    idx = substr.find('r:')

                    if idx != -1:
                        filename = substr[(idx + 2):]
                        got_filename = True
                        file = open(filename, 'wb')
                else:

                    if substr.find('E') != -1 or substr.find('END') != -1:
                        return True

                    if substr.find('-') != -1 and substr.find('link') == -1:
                        c = substr.split('-')[1]
                        #get rid of all unwanted characters.......
                        for unwanted in ascii_extend:
                            if c.find(unwanted) != -1:
                                c.replace(unwanted, '')
                        if c.find('E') != -1 or c.find('END') != -1:
                            if got_filename:
                                file.close()
                            return
                        if got_filename:
                            file.write(c+'+n')
                        
                #end of IF
          

        def print_topology(self):
                for c in self.clients[:]:		# use a copy of the list
			try:
                                print '========================================='
				print 'Gateway: ',c.get_hostname()
                                print '========================================='
                                print '[mote_id, dev]'

                                mote_id = 1
                                for mote in c.get_motelist():
                                    if mote:
                                        print '[', mote_id, mote, ']\n'
                                    
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
				c.callback('Somebody shouted: '+message) # oneway call
			except Pyro.errors.ConnectionClosedError,x:
				# connection dropped, remove the listener if it's still there
				# check for existence because other thread may have killed it already
				if c in self.clients:
					self.clients.remove(c)
					print 'Removed dead listener',c


######## main program

testserver.start(CallbackThing,'callback')

