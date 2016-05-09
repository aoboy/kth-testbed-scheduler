#!/usr/bin/env python
import os, sys, time, re, getopt, getpass, subprocess
import traceback
import pexpect


#sensors = [  ["sensorname@gwname",sensorstatus, "newcomment", sensorid]    ]
sensors = [   ["XBS4RVSD@alpha",0,"",76]   ]
SHELL = "~\$"
SHELL2 = "~#"
#
# some functions
#
commands=['scp -r channel_hopping gonga@wsntestbed.s3.kth.se:/home/gonga/']
clients={'192.168.200.10':'blub', '192.168.200.11':'blub', '192-168.200.12':'blub'}
#clients={'130.237.43.111':'blub'}



def login(gwname,host,port,user,password):
    global p
    #
    # Login via SSH
    #
    ssh_newkey = "(yes/no)"
    # my ssh command line
    command = 'ssh  -p %s %s@%s '%(port,user,host)
    p=pexpect.spawn(command)
    i=p.expect([ssh_newkey,"assword:",SHELL,SHELL2,pexpect.EOF, pexpect.TIMEOUT,"access denied", "try again","name or service not known","Name or service not known"],timeout=5)
    print "expected %i"%(i)
    #print p.before
    print "--------------------------------------------"
    if i==0:
        p.sendline('yes')
        i=p.expect([ssh_newkey,"assword:",SHELL,SHELL2,pexpect.EOF, pexpect.TIMEOUT,"access denied", "try again","name or service not known","Name or service not known"],timeout=10)
        print "   expected %i"%(i)
	print p.before
	print "--------------------------------------------"
    if i==0:
	print 'after calling %s\n'%(command)
	print 'something went horribly wrong,...'
	return 1
    if i==1:
	print "emptyline"
      #   p.sendline("");
        p.sendline(password)           
        i=p.expect([SHELL,SHELL2,pexpect.EOF,"dfg45wen3","dfg45wen3",pexpect.TIMEOUT,"access denied", "try again","name or service not known","Name or service not known"],timeout=10)
	print " >>> expected %i"%(i)
	print p.before
    if i>=5:
	print 'after calling %s\n'%(command)
        print "I either got key or connection timeout, or access denied"
        print p.before # print out the result
        return 1
    print "login to %s ok"%(gwname)
    return 0

def closeConnection():
    global p
    #
    # close ssh connection
    #
    p.sendline ('exit')
    index = p.expect([pexpect.EOF, "(?i)there are stopped jobs"])
    if index==1:
        p.sendline("exit")
        p.expect(EOF)

def exec_command(command):
    global p
    print "running command %s"%(command)
    p.sendline(command)
    i=p.expect([SHELL,SHELL2,pexpect.EOF,pexpect.TIMEOUT,"error occoured"])
    print p.before
    
    if i == 3:
	    print "       TIMEOUT!"
	    p.expect([SHELL,SHELL2,pexpect.EOF])
	    return 1
    if i == 4:
	    s=p.expect([pexpect.EOF,pexpect.TIMEOUT,"ermission denied","such file","Timeout"])
	    if s <= 1:
	   	 print "       an unknown error occured"
	   	 p.expect([SHELL,SHELL2,pexpect.EOF])
	    	 return 1
	    if s == 2:
	   	print "       permission denied!"
	    	p.expect([SHELL,SHELL2,pexpect.EOF])
	    	return 2
	    if s == 3:
	   	print "       mote not connected"
	    	p.expect([SHELL,SHELL2,pexpect.EOF])
	    	return 3
	    if s == 4:
	   	print "       mote timeout"
	    	p.expect([SHELL,SHELL2,pexpect.EOF])
	    	return 4
    print "       done"
    return 0


def main():
    p = 0
        
    """ script for program sequence """ 
    
    for host, passwd in clients.iteritems():
        print  host, passwd
        s=login(host,host,"22","gonga",passwd)

        if s == 0:
            connected = 1
            print 'connection established'
            for cmd in commands:
		cmd = cmd+' gonga@'+host+':/tmp/'
                exec_command(cmd)
               
        if p != 0:
            closeConnection()

    exit(0)

#if we made it till here everything worked as expected

if __name__ == "__main__":

    try:
        main()
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(44)


#import os.path, time
#print "last modified: %s" % time.ctime(os.path.getmtime(file))
#print "created: %s" % time.ctime(os.path.getctime(file))
#Your other option is to use os.stat:

#import os, time
#(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
#print "last modified: %s" % time.ctime(mtime)
