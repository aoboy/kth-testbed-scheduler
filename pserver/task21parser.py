
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time
import traceback
import pexpect
import shlex
import subprocess
#KTH - The Royal Institute of Technology
# Automatic Control Lab
#  Prof. Mikael Johansson's Group
#    Author: Antonio Gonga (El-Guapo Angoleno): gonga@kth.se, PhD Student
#Parser file: This file is used to parse data files into a readable format to MATLAB...it
#             also creats XML files.


rootdir =os.path.abspath("./")
files=[]
directories = []

masks = [0xAA49, #AA. channels 15.20 (15-11).(20-11)
         0xAA4E, #AA. channels 15.25 The index subtraction is necessary to
         0xAA4F, #AA. channels 15.26 avoid extra conversions at the sensor
         0xAA9E, #AA. channels 20.25
         0xAA9F, #AA. channels 20.26
         0xAAEF  #AA. channels 25.26
              ]


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

ch_cache = {}
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

def main():
    for i in range(11, N):
        for j in range(i+1, N+1):
            mask = 0x0000
            mask = (mask | ((i<<4) & 0xF0))
            mask = (mask | (j & 0x0F))
            mask = (0xBB00 | mask)
            masks.append(mask)
            #print '(',i,',',j,')',
            print mask,
        print '\n'

def demask():
    for m in masks:
        a= ((0x000F & m)+11)
        b= (((0x00F0 & m)>>4)+11)
        print '(',b,',',a,')',

def execCmd(commandLine):
    #print commandLine
    args = shlex.split(commandLine)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print 'ERROR!'
        print stdout
        print stderr
        sys.exit(1)
    return p.returncode, stdout

def get_channel_ids(s):
    channels = s[s.find('ls')+2: s.find('li')-2]

    return ch_cache[channels.replace('n', '')]

def hex2bin(s):
        hexs = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
                '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
        substr=''
        for ch in list(s):
            substr=substr + hexs[int(ch.upper(), 16)]

        return substr

def create_description():
 desc = open(os.path.join(rootdir, 'README.txt'), 'wb' )
 desc.write('Task 2.1\n Single channel transmission from any to any: n(n-1) files\n')
 desc.write('node Ni send P packets on channel Cn, where n=[11-26] results saved on Chn\n')
 desc.write('There are also XML files available\n')
 desc.close()


def rename_dir():
    directories = os.listdir(rootdir)
    directories.sort()

    try:
        cmd ='rm -rf OriginalFiles/ XML/'
        execCmd(cmd)
        print 'Erasing OriginalFiles/'
    except:
        print 'Exception 1'
        pass

    try:
        cmd ='mkdir OriginalFiles/ XML/'
        execCmd(cmd)
        print 'Created OriginalFiles/'
    except:
        print 'Exception 2'
        pass
    
    for dir in directories:
        if  os.path.isdir(os.path.join(rootdir,dir)):
            if dir.find('Ch') != -1 and dir.find('.') == -1:
            #directories.append(a)
                print 'Parsing DIR: ', dir
                newName= 'XML/XML'+dir+'/'
                newDirs=[newName, 'OriginalFiles/'+dir+'/']

                cmd = 'mkdir '
                for d in newDirs:
                    cmd = cmd + str(d+' ')
               
                execCmd(cmd)


                for fname in os.listdir(os.path.join(rootdir,dir)):
                    if fname.find('SingleChannels') != -1 and  fname.find('link0-') == -1:
                        if fname.find('.txt') != -1 and fname.find('?') == -1:

                            fileName=''

                            if fname.find('n1') != -1:
                                newFileName = dir+'/'+fname[fname.find('link'):]
                                fileName = os.path.join(rootdir, dir+'/'+fname)
                                write_file(fileName, newFileName)

                                newFileName = newDirs[0]+fname[fname.find('link'):]
                                write_xml(fileName, newFileName)


                            cmd = 'mv '+fileName +' '+ os.path.join(rootdir, 'OriginalFiles/'+dir+'/')
                            execCmd(cmd)

def write_file(fileName, newFileName):
    data = open(fileName,'rb').read()
    newBinFile = open(newFileName.replace('.txt', '.TXT'), 'wb')

    for row in data.split('\n'):
        if row :
            try:
                substr = row.split('-')
                binstr = hex2bin(substr[1])

                for b in list(binstr):
                    newBinFile.write(b+' ')
                newBinFile.write('\n')
            except:
                print 'error in the for loop'

    newBinFile.close()


def write_xml(fileName, newFileName):
    data = open(fileName,'rb').read()
    newXmlFile = open(newFileName.replace('.txt', '.xml'), 'wb')

    newXmlFile.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    newXmlFile.write(' <resultfile>\n')
    newXmlFile.write('   <header>\n')
    fname = fileName
    idx = fname.find('link')
    if idx != -1:
        newXmlFile.write('      <link id="'+fname[(idx+4):-4]+'">\n')
        src_id = fname[(idx+4):-4].split('-')[0]
        moteinfo = loc_cache[int(src_id)]
        newXmlFile.write('        <source_mote name="'+ moteinfo[0]+'" location="'+moteinfo[1]+'">'+src_id+'</source_mote>\n')

        dst_id= fname[(idx+4):-4].split('-')[1]
        moteinfo = loc_cache[int(dst_id)]
        newXmlFile.write('        <dest_mote name="'+moteinfo[0]+'" location="'+moteinfo[1]+'">'+dst_id+'</dest_mote>\n')
        newXmlFile.write('      </link>\n')

        newXmlFile.write('      <filedate>'+'%s'%time.ctime(os.path.getmtime(fileName))+'</filedate>\n')
        newXmlFile.write('      <channels>\n')
        str_chs = get_channel_ids(fname)
        newXmlFile.write('        <num_channels>'+str(len(str_chs.split('.')))+'</num_channels>\n')
        newXmlFile.write('        <channel_ids>'+str_chs +'</channel_ids>\n')
        newXmlFile.write('      </channels>\n')
        newXmlFile.write('   </header>\n')
        newXmlFile.write('   <data>\n')
        for row in data.split('\n'):
            if row :
                try:
                    substr = row.split('-')
                    binstr = hex2bin(substr[1])
                    newXmlFile.write('      <data_item mem_id="'+substr[0]+'" data_id="'+substr[1]+'">'+binstr+'</data_item>\n')
                except Exception:
                    print 'error in the for loop:==>', Exception
        newXmlFile.write('   </data>\n')
        newXmlFile.write(' </resultfile>\n')
        newXmlFile.close()
if __name__ == '__main__':
    #main()
    create_description()
    rename_dir()
