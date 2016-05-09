#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#This is the file converter from .TXT to a readable data structure in XML/1's
#Another Modif
#Test

import os,sys,  getopt, getpass
import os.path, time
import traceback
import pexpect
#from Image import directories

rootdir =os.path.abspath("./")
files=[]
directories = []

ch_cache = {}

ch_cache['02'] = '26.17'
ch_cache['04'] = '26.22.17.13'
ch_cache['08'] = '26.19.12.20.24.22.17.13'
ch_cache['12'] = '26.19.12.20.24.16.23.18.25.22.17.13'
ch_cache['16'] = '26.19.12.20.24.16.23.18.25.14.21.11.15.22.17.13'


ch_cache['11']='11'
ch_cache['12']='12'
ch_cache['13']='13'
ch_cache['14']='14'
ch_cache['15']='15'
ch_cache['16']='16'
ch_cache['17']='17'
ch_cache['18']='18'
ch_cache['19']='19'
ch_cache['20']='20'
ch_cache['21']='21'
ch_cache['22']='22'
ch_cache['23']='23'
ch_cache['24']='24'
ch_cache['25']='25'
ch_cache['26']='26'
ch_cache['1520']='15.20'
ch_cache['15202526']='15.20.25.26'

ch_cache['Pool4']  = '11.12.13.14'
ch_cache['Pool8']  = '11.12.13.14.15.16.17.18'
ch_cache['Pool16'] = '11.12.13.14.15.16.17.18.19.20.21.22.23.24.25.26'

ch_cache['Pool4']  = '11.12.13.14'
ch_cache['Pool8']  = '11.12.13.14.15.16.17.18'
ch_cache['Pool16'] = '11.12.13.14.15.16.17.18.19.20.21.22.23.24.25.26'


loc_cache = {}
loc_cache[8] = ['XBS0KHZF' ,'CORR-B']
loc_cache[9] = ['XBS0KI3E' ,'KITCHEN']
loc_cache[10] = ['XBS0JZLB' ,'B606']
loc_cache[11] = ['XBS0KIF6' ,'B604']
loc_cache[12] = ['XBS4RXBF' ,'CORR-B']
loc_cache[13] = ['XBS0LAE8' ,'B614']
loc_cache[14] = ['XBS0LB3V' ,'B614']
loc_cache[15] = ['XBS5GZJR' ,'B610']

loc_cache[16] = ['XBS0KIBM' ,'CORR-B']
loc_cache[17] = ['XBS0KHXY' ,'CORR-B']
loc_cache[18] = ['XBS0KHYF' ,'B618']
loc_cache[19] = ['XBS0SGA4' ,'B620']
loc_cache[20] = ['XBS14SR2' ,'C628']
loc_cache[21] = ['XBS0LABO' ,'C628']
loc_cache[22] = ['XBS5GZPR' ,'A618']

loc_cache[32] = ['XBS4RXWK' ,'A618']
loc_cache[29] = ['MFTFL9B1' ,'A619']
loc_cache[28] = ['XBS4RVSD' ,'A621']
loc_cache[30] = ['MFTFJ1CU' ,'CORR-A']
loc_cache[31] = ['MFTFL6WA' ,'MEETING-R']
loc_cache[26] = ['MFTFIZD7' ,'CORR-A']
loc_cache[27] = ['XBS5GZ78' ,'CORR-A']
loc_cache[24] = ['XBS5GZ7U' ,'A625']
loc_cache[25] = ['MFTFL9LZ' ,'A627']
loc_cache[23] = ['XBS5H6MF' ,'CORR-A']

loc_cache[1] = ['XBS0LACQ' ,'KITCHEN']
loc_cache[2] = ['XBS0LAFQ' ,'CORR-A']
loc_cache[3] = ['XBS0K5UN' ,'A607']
loc_cache[4] = ['XBS0K2QI' ,'A609']
loc_cache[5] = ['XBS0LAAD' ,'A615']
loc_cache[6] = ['XBS0KI6I' ,'A613']
loc_cache[7] = ['XBS0KHZZ' ,'FRONT-PRINT']


rootdir =os.path.abspath("./")
files=[]
directories = []

def parseFiles():
    global directories, files

    #list first the directories
    directories = os.listdir(rootdir)
    directories.sort()

    for dir in directories:
        if  os.path.isdir(os.path.join(rootdir,dir)):
            if dir.find('Task2Pool') != -1 and dir.find('.') == -1:
                #directories.append(a)
                print 'Parsing DIR: ', dir
                for fname in os.listdir(os.path.join(rootdir,dir)):
                    if fname.find('ExpChannels') != -1 and  fname.find('link0-') == -1:
                        if fname.find('.txt') != -1 and fname.find('?') == -1:
                            #print dir,'/',fname
                            fileName = os.path.join(rootdir, dir+'/'+fname)
                            data = open(fileName,'rb').read()
                            newf = open(fileName.replace('.txt', '.xml').replace('ExpC', 'TschXMLC').replace('ls', 'lsPool'), 'wb')
                            resf = open(fileName.replace('.txt', '.TXT').replace('ExpC', 'TschBinC').replace('ls', 'lsPool'), 'wb')

                            newf.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
                            newf.write(' <resultfile>\n')
                            newf.write('   <header>\n')

                            #newf.write('      <link id="'+)
                            idx = fname.find('link')
                            if idx != -1:
                                newf.write('      <link id="'+fname[(idx+4):-4]+'">\n')
                                src_id = fname[(idx+4):-4].split('-')[0]
                                moteinfo = loc_cache[int(src_id)]
                                newf.write('        <source_mote name="'+ moteinfo[0]+'" location="'+moteinfo[1]+'">'+src_id+'</source_mote>\n')

                                dst_id= fname[(idx+4):-4].split('-')[1]
                                moteinfo = loc_cache[int(dst_id)]
                                newf.write('        <dest_mote name="'+moteinfo[0]+'" location="'+moteinfo[1]+'">'+dst_id+'</dest_mote>\n')
                                #newf.write('        <location>'+)
                                newf.write('      </link>\n')

                            newf.write('      <filedate>'+'%s'%time.ctime(os.path.getmtime(fileName))+'</filedate>\n')
                            newf.write('      <channels>\n')
                            str_chs = get_channel_ids(fname)
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
    channels = s[s.find('ls')+2: s.find('li')-2]

    return ch_cache[channels.replace('n', '')]

if __name__ == "__main__":

    try:
        parseFiles()

    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(44)
