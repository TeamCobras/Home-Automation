'''
	This file has been shared by Nassir Malik
	# IOT-Pi3-Alexa-Automation

	Youtube tutorial https://www.youtube.com/watch?v=uS5dTx8vjq4
	Ported from original repos for python 3
	https://github.com/toddmedema/echo
	https://github.com/xtacocorex/CHIP_IO 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.

	We are very grateful to him as this file has helped us a lot in our project.
	We had to make minor changes to make the code work as per our requirement.

    
'''
#importing required libraries and header files
import fauxmo
import logging
import picamera
import time
import sys
import RPi.GPIO as GPIO
import csv
from random import randint
 
from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)
 
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"camera": 52000,"recorder":51500,"tablefan":50000,"tablelamp":51200} #These are the various triggers. Names can be changed as per requirement.

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)
        w=0
        if name == 'tablelamp':
            w=7  #pin number of the relay connected to the table lamp
        elif name =="tablefan":
            w=13 #pin number of the relay connected to the table fan
        elif name=="camera":#For camera, start a preview and click image
            camera=picamera.PiCamera()
            camera.start_preview()
            time.sleep(3)
            camera.capture('img'+str(randint(0,10000))+'.jpg')
            camera.stop_preview()
            camera.close()
            return True
        elif name=="recorder":#For recorder, start a preview and record a video for 5 sec(can be changed)
            camera=picamera.PiCamera()
            camera.start_preview()
            time.sleep(1)
            camera.start_recording('vid'+str(randint(0,10000))+'.h264')
            time.sleep(5)
            camera.stop_recording()
            camera.stop_preview()
            camera.close()
            return True
        l1=[]
        #Reading the present state of the devices
        with open('devices.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if int(row[0]) == w:
                    if state:
                        state1 = '1'
                    else:
                        state1='0'
                    row[1]= state1
                l1.append(row)
        if len(l1)>=1:
        	#write the new states of the devices if any change made, or write the same data
            myFile = open('devices.csv', 'w')
            with myFile:
                writer = csv.writer(myFile,lineterminator='\n')
                for i in l1:
                    writer.writerow(i)
            myFile.close()
        
        return True
 
if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)
 
    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ e.args  )
            break