#Makefile for example
CONTIKI = /home/aogo/channel_hopping
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


pollserver:
	#TASKs 3a,b,c)
	nohup python StatusUpdate.py > StatusLog.out 2> StatusLog.err < /dev/null &

clear:
	@echo "GONGA"

	
include $(CONTIKI)/Makefile.include
