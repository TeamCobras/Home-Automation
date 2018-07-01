from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as bs
import requests
import csv
import re
import picamera
import time
import random

def index(request):
    return render(request, 'dashboard.html', {})

@csrf_exempt
def work(request): # Function called when we click a applet in the dashboard
    i=1
    name=''
    name1=''
    while True:
        r=request.POST.get('applet_button'+str(i))
        if r=='1':
            name='applet_image'+str(i)
            name1='Light'+str(i)
            break
        else:
            i+=1
    if i==1 or i==2:
        l1=[]
        state=0
        with open('devices.csv', 'r') as f:
            reader = csv.reader(f)
            v=1
            for row in reader:
                if v==i:
                    print(row[1])
                    if int(row[1]):
                        state=0
                    else:
                        state=1
                    row[1]= str(state)
                l1.append(row)
                v+=1
        print(l1)
        if len(l1)>=1:
            myFile = open('devices.csv', 'w')
            with myFile:
                writer = csv.writer(myFile,lineterminator='\n')
                for k1 in l1:
                    writer.writerow(k1)
            myFile.close()
    else:
        camera=picamera.PiCamera()
        if i==3:
            camera.start_preview()
            time.sleep(3)
            camera.capture('photos/img'+str(random.randint(0,10000))+'.jpg')
            camera.stop_preview()
            camera.close()
        elif i==4:
            camera.start_preview()
            time.sleep(1)
            camera.start_recording('videos/vid'+str(random.randint(0,10000))+'.h264')
            time.sleep(5)
            camera.stop_recording()
            camera.stop_preview()
            camera.close()
    time.sleep(0.8)
    return render(request, 'dashboard.html')
