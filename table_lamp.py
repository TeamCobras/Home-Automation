""" name_port_gpio.py
 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.
"""
 
import fauxmo
import logging
import time
import sys
import RPi.GPIO as GPIO ## Import GPIO library
import csv
 
from debounce_handler import debounce_handler
 
logging.basicConfig(level=logging.DEBUG)
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    #TRIGGERS = {str(sys.argv[1]): int(sys.argv[2])}
    TRIGGERS = {"table lamp": 52000}
    #TRIGGERS = {"kitchen": 52000,"living room":51000}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address,name)
        w=0
        if name == 'table lamp':
            w=7
        else:
            return True
        l1=[]
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
