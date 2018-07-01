'''
    This file is to check if the one-way switch has been toggled

'''

#import required libraries
import RPi.GPIO as GPIO
import csv
import time

GPIO.setmode(GPIO.BOARD)

l=[5,5] #A list for checking previous state of a switch

while 1:
    l1=[]
    #Checking current state of devices
    with open('devices.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            l1.append(row)
    u=[]  
    # Checking if there is any toggling happening      
    for i in l1:
        flag=0
        GPIO.setup(int(i[2]), GPIO.IN)
        c1=0
        c2=0
        lis=l1.index(i)
        c3=l[lis]
        for j in range(10000):
            if GPIO.input(int(i[2])):
                c1+=1
            else:
                c2+=1      
        if c1+c2==10000:
            if c2>=2000:
                if c3!=0:
                    flag=1
                    if int(i[1]):
                        i[1]='0'
                        
                    else:
                        i[1]='1'
                    c3=0
                    l[lis]=c3
                    print('c',1)
            else:
                if c3!=1:
                    flag=1
                    if int(i[1]):
                        i[1]='0'
                    else:
                        i[1]='1'
                    c3=1
                    l[lis]=c3
                    print('c',2)
        u.append(flag)
    #If toggling happens, write the changes in the database
    if ((len(l1)>=1) and (1 in u)):
        myFile = open('devices.csv', 'w')
        with myFile:
            writer = csv.writer(myFile,lineterminator='\n')
            for i in l1:
                writer.writerow(i)
        myFile.close()        