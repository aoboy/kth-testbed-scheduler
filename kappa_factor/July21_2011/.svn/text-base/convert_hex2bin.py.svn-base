#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#This is the file converter from .TXT to a readable data structure in XML/1's
#Another Modif
#Test

import os,sys,  getopt, getpass
import os.path, time
import traceback
import pexpect

rootdir =os.path.abspath("./")
files=[]

ch_cache = {}

#ch_cache['Pool4']  = '26.17.13.22'
#ch_cache['Pool8']  = '26.12.20.24.22.17.13.19'
#ch_cache['Pool12'] = '26.12.20.24.16.23.18.25.22.17.13.19'
#ch_cache['Pool16'] = '26.12.20.24.16.23.18.25.14.21.11.15.22.17.13.19'
ch_cache['Pool4']  = '11.12.13.14'
ch_cache['Pool8']  = '11.12.13.14.15.16.17.18'
ch_cache['Pool16'] = '11.12.13.14.15.16.17.18.19.20.21.22.23.24.25.26'

ch_cache['CH2622']    = '26.22'
ch_cache['CH262216']  = '26.22.16'
ch_cache['CH26221612']= '26.22.16.12'

def get_files_dir():
        global files
        files = []
        for a in os.listdir(rootdir):
		if not os.path.isdir(os.path.join(rootdir,a)):
			if a.find('Nchannels') != -1 and  a.find('link0-') == -1:
                                if a.find('.txt') != -1 and a.find('?') == -1:
                                    files.append(a)
        return files

def bin(s):
        return str(s) if s<=1 else bin(s>>1)+str(s&1)

def hex2bin(s):
        hexs = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
                '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
        substr=''
        for ch in list(s):
            substr=substr + hexs[int(ch.upper(), 16)]

        return substr

def get_channel_ids(s):
        global ch_cache

        if s.find('Pool') != -1:
            return ch_cache[s[(s.find('ls')+2):s.find('li')]]
       
        if s.find('NchannelsCH') != -1:
            return s[(s.find('ls')+2):s.find('li')]
        else:
            return "7777"

def parse_file():
        
        for f in files:            
            data = open(os.path.join(rootdir, f),'rb').read()
            newf = open(os.path.join(rootdir, f.replace('txt', 'xml').replace('channels','').replace('N', 'XML')), 'wb')
            resf = open(os.path.join(rootdir, f.replace('N', 'Bin').replace('txt', 'TXT')), 'wb')

            newf.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
            newf.write(' <resultfile>\n')
            newf.write('   <header>\n')

            #newf.write('      <link id="'+)
            idx = f.find('link')
            if idx != -1:
                newf.write('      <link id="'+f[(idx+4):-4]+'">\n')
                newf.write('        <source_moteid>'+f[(idx+4):-4].split('-')[0]+'</source_moteid>\n')
                newf.write('        <dest_moteid>'+f[(idx+4):-4].split('-')[1]+'</dest_moteid>\n')
                print "link:", f[(idx+4):-4]
                newf.write('      </link>\n')
            
            newf.write('      <filedate>'+'%s'%time.ctime(os.path.getmtime(f))+'</filedate>\n')
            newf.write('      <channels>\n')
            str_chs = get_channel_ids(f)
            newf.write('        <num_channels>'+str(len(str_chs.split('.')))+'</num_channels>\n')
            newf.write('        <channel_ids>'+str_chs +'</channel_ids>\n')
            newf.write('      </channels>\n')
            newf.write('   </header>\n')
            newf.write('   <data>\n')
            for row in data.split('\n'):
                if row :
                    try:
                        substr = row.split('-')
                        binstr = hex2bin(substr[1])
                        newf.write('      <data_item mem_id="'+substr[0]+'" data_id="'+substr[1]+'">'+binstr+'</data_item>\n')
			#to accomplish Pablo's concerns
			for b in list(binstr):
			   resf.write(b+' ')
                        resf.write('\n')
                    except:
                        print 'error in the for loop'
            newf.write('   </data>\n')
            newf.write(' </resultfile>\n')
            newf.close()
            resf.close()
            #os.remove(f)
            

if __name__ == "__main__":

    try:
        #main()
        filesdir=get_files_dir()
        #for f in filesdir:
        #    print 'file :',f
        parse_file()
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(44)
