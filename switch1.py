'''
    This is a backup file for using a 2-way switch instead of a 1-way switch

'''

import RPi.GPIO as GPIO
import csv
import time

GPIO.setmode(GPIO.BOARD)

lw=[0,0]

while 1:
    l1=[]
    
    with open('devices.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            l1.append(row)

    for i in l1:
        GPIO.setup(int(i[2]), GPIO.IN)
        a=GPIO.input(int(i[2]))
        print(a)
        if int(a)!=lw[l1.index(i)]:
            lw[l1.index(i)]=int(a)
            if int(i[1]):
                i[1]='0'
            else:
                i[1]='1'

    myFile = open('devices.csv', 'w')
    with myFile:
        writer = csv.writer(myFile,lineterminator='\n')
        for i in l1:
            writer.writerow(i)
    myFile.close()
    time.sleep(0.5)