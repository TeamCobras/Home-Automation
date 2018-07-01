"""
    
    This file is the main file for wrting the state of the devices to the GPIO pins. 
    Here,  we read the database of the devices(here we used a csv file) and write it to the GPIO pins.
    Also, we keep updating the state of the device to dashboard.

"""

#import required libraries

import RPi.GPIO as GPIO
import csv
import time
import requests
from bs4 import BeautifulSoup as bs


lw=[0]*2   #list of all flags


while True:
    #reading the states of the devices and giving output
    with open('devices.csv', 'r') as f:
        reader = csv.reader(f)
        wa=0
        lk=[]
        for row in reader:
            w,v=(row[0],row[1])
            lk.append(int(v))
            if int(v):
                if not lw[wa]:
                    GPIO.setmode(GPIO.BOARD)
                    GPIO.setup(int(w),GPIO.OUT)
                GPIO.output(int(w),GPIO.HIGH)
                lw[wa]=1
            else:
                GPIO.cleanup([int(w)])
                lw[wa]=0
            wa+=1
    print(len(lk))
    
    #Making changes in the dashboard
    r=requests.get('http://127.0.0.1:8000/home/')
    html=bs(r.content,'html.parser')
    html=str(html.prettify())
    str1='../../static/light_on.png'
    str2='../../static/light.png'
    l=[]
    name=[]
    for w1 in range(len(lk)):
        name1='applet_image'+str(w1+1)
        name2='Light'+str(w1+1)
        name.append([name1,name2])
    k=0
    flag=0
    flag1=0
    for line in html.split('\n'):
        if not flag:
            j=line.find(name[k][0])+7+len(name[k][0])
            if j!=6+len(name[k][0]):
                g=line.find('.png"')+4
                if lk[k]:
                    line=line[:j]+str1+line[g:]
                else:
                    line=line[:j]+str2+line[g:]
                flag=1
            l.append(line)
        elif not flag1:
            j=line.find(name[k][1])+1+len(name[k][1])
            if j!=len(name[k][1]):
                if lk[k]:
                    line=line[:j]+'ON'
                else:
                    line=line[:j]+'OFF'
                flag1=1
                
                if k<len(lk)-1:
                    k+=1
                    flag=0
                    flag1=0
            l.append(line)
        else:
            l.append(line)
    html=''
    for w in l:
        html+=w+'\n'
    soup = bs(html,'html.parser')
    soup=soup.prettify()
    my_html_string = str(soup)
    f=open('home/templates/dashboard.html','w')
    c=f.write(my_html_string)
    f.close()
    time.sleep(0.5)

    
GPIO.cleanup()