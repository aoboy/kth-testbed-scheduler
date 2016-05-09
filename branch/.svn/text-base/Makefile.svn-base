#Makefile for example
CONTIKI = ../../isa_mikael_pablo_gonga
ifndef TARGET
TARGET=sky
endif



DEFUSB="USB0"
OUTDEV="/dev/tty"

OUTDEV_USB="$OUTDEV$DEFUSB"

## WARNING .... This Makefile is used by multiple applications
# setting the defines VARIABLE can only be done by a  remote process..
###DEFINES=NODE_IS_RECEIVER NODE_IS_SENDER


compile:
	gcc -g linux-serialdump.c -o download
	@echo "==>download application created"
	gcc -g node_transmit.c -o transmit
	@echo "==> command tx application created..."
	gcc -g serialconnect.c -o sconnect

runclient:
	java -Djava.security.policy=client.policy -XX:+DisableExplicitGC GWScheduler

runserver:
	java -Djava.security.policy=server.policy -Djava.rmi.server.hostname=gonga-rt-gx760.s3.kth.se Scheduler $(ARG)
#	java -Djava.security.policy=server.policy -Djava.rmi.server.hostname=192.168.1.100 Scheduler  $(ARG)
#	java -Djava.security.policy=server.policy -Djava.rmi.server.hostname=130.237.43.111 Scheduler  $(ARG)

clear:
	rm -rf *.sky symbols.* obj_* *~ *.class *.pyc sconnect transmit
	make clean

cls:
	rm -rf *.class

recvbin:
	rm -rf *.sky symbols.* obj_* *~
	make clean
	make isa_receiver.upload
	cp tmpimage.ihex isa_receiver.ihex

recv:
	rm -rf *.sky symbols.* obj_* *~ 
	make clean
	make isa_receiver.upload
	cp tmpimage.ihex isa_receiver.ihex

sender:
	rm -rf *.sky symbols.* obj_*
	make clean
	make isa_sender.upload
	cp tmpimage.ihex isa_sender.ihex

serial:
	make login > $(ARG)

reload:
	make sky-reset

delete:
	make clean
	rm -rf obj_* *~ symbols.* *.sky

include $(CONTIKI)/Makefile.include
