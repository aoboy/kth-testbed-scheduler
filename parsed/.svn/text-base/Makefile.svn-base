#Makefile for example
CONTIKI = ../../
#CONTIKI = ../..
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
	nohup python pyro_client.py > clientlog.out 2> clientlog.err < /dev/null &

stopcient:
	kill -9 $(pidof python)

runserver:
	nohup python testbedserver.py > serverlog.out 2> serverlog.err < /dev/null &

run-ns:
	nohup pyro-ns > nameserver.out 2> nameserver.err < /dev/null &


convert2xml:
	python convert_hex2bin.py

clear:
	rm -rf *.sky symbols.* obj_* *~ *.class *.pyc sconnect transmit
	make clean
	make compile
cls:
	rm -rf *.class

recvbin:
	rm -rf *.sky symbols.* obj_* *~
	make clean
	#make isa_receiver.upload
	make isa_receiver.ihex
	#cp tmpimage.ihex isa_receiver.ihex

recv:
	rm -rf *.sky symbols.* obj_* *~ 
	make clean
	make isa_receiver.upload
	cp tmpimage.ihex isa_receiver.ihex

sender:
	rm -rf *.sky symbols.* obj_*
	make clean
	#make isa_sender.upload
	make isa_sender.ihex
	#cp tmpimage.ihex isa_sender.ihex

serial:
	make login > $(ARG)

reload:
	make sky-reset

delete:
	make clean
	rm -rf obj_* *~ symbols.* *.sky 


include $(CONTIKI)/Makefile.include
