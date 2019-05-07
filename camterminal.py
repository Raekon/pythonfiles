#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading
import subprocess
import ftplib
import os
import time
import datetime
from PIL import Image

nowtime=(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M'))

class Uploader(threading.Thread): 
    def __init__(self, shoottime, timelapse): 
        threading.Thread.__init__(self) 
        self.Shoottime = shoottime*1000
        self.Timelapse = timelapse*1000
    def run(self):
        os.system("pkill raspivid")
        print("thread running")
        
        dir_cont=os.listdir("/home/pi/Pictures/cam")
        print (dir_cont)
        session = ftplib.FTP('ftp.kongesquash.dk','kongesquash.dk','Raekon75')
        for i in dir_cont:
            img = Image.open("/home/pi/Pictures/cam/{0}".format(i)).convert('L')
            img.save("/home/pi/Pictures/cam/{0}".format(i))
            os.rename("/home/pi/Pictures/cam/{0}".format(i),"/home/pi/Pictures/vault/{0}".format(i))
        dir_cont=os.listdir("/home/pi/Pictures/vault")
        for i in dir_cont:                    
            file= open('/home/pi/Pictures/vault/{0}'.format(i),'rb')
            session.storbinary('STOR skole/vagt/{0}'.format(i), file)
            file.close  
        session.quit
        dir_cont=os.listdir("/home/pi/Pictures/vault")
        for i in dir_cont:
            os.remove("/home/pi/Pictures/vault/{0}".format(i))

class vid_uploader(threading.Thread): 
    def __init__(self, shoottime, timelapse): 
        threading.Thread.__init__(self) 
        self.Shoottime = shoottime*1000
        self.Timelapse = timelapse*1000
    def run(self):
        os.system("pkill raspivid")
        print("thread running")
        
        dir_cont=os.listdir("/home/pi/Pictures/cam")
        print (dir_cont)
        session = ftplib.FTP('ftp.kongesquash.dk','kongesquash.dk','Raekon75')
        for i in dir_cont:                    
            file= open('/home/pi/Pictures/cam/{0}'.format(i),'rb')
            session.storbinary('STOR skole/vagt/{0}'.format(i), file)
            file.close  
        session.quit
        dir_cont=os.listdir("/home/pi/Pictures/cam")
        for i in dir_cont:
            os.remove("/home/pi/Pictures/cam/{0}".format(i))

class Choices ():
    def __init__ (self):
        chooser=1
        while(chooser==1):
            self.media=input("Foto (f) eller Video (v) eller preview (p)?")
            if self.media=="f":
                print("du har valgt foto")
                chooser=2
                while chooser==2:
                    self.minutter=input("hvor mange minutter skal der filmes?")
                    try:
                        self.minutter=int(self.minutter)*60000
                        chooser=3     
                    except ValueError:
                        print("du har ikke skrevet et helt tal\n")
                while chooser==3:
                    self.timelapse=input("hvor mange sekunder imellem hvert billede?")
                    try:
                        self.timelapse=int(self.timelapse)*1000
                        chooser=4
                    except ValueError:
                        print("du har ikke skrevet et helt tal.\n")
                while chooser==4:
                    print("hvilken størrelse skal billederne have?")
                    print("1) 640*480")
                    print("2) 800*600")
                    print("3) 1024*768")
                    print("4) 1280 * 1024")
                    print("5) 1920*1080")
                    print("6) 2592*1944  (max 15 FPS)")
                    self.size=input("")
                    try:
                        size=int(self.size)
                        if (1<= size) and (6>= size):
                            self.size=int(self.size)
                            chooser=5
                            
                        else:
                            self.size=2
                            chooser=5
                    except ValueError:
                        print("Du har ikke skrevet et helt tal")
                while (chooser==5):
                    self.filename=input("hvad skal filen hedde?")
                    if self.filename=="":
                        self.filename=nowtime
                    print (" valg er {0},{1},{2},{3},{4}".format(self.media,self.minutter,self.timelapse,self.size,self.filename))
                    chooser=0
                    
            elif self.media=="v":
                print("du har valgt video \n")
                chooser=12
                while chooser==12:
                    self.minutter=input("hvor mange minutter skal der filmes?")
                    try:
                        self.minutter=int(self.minutter)*60000
                        chooser=13     
                    except ValueError:
                        print("du har ikke skrevet et helt tal\n")                
                while chooser==13:
                    self.framerate=input("hvor mange billeder i sekundet?")
                    try:
                        val=int(self.framerate)
                        chooser=14
                    except ValueError:
                        print("du har ikke skrevet et helt tal.\n")                
                while chooser==14:
                    print("hvilken størrelse skal filmen have?")
                    print("1) 640*480")
                    print("2) 800*600")
                    print("3) 1024*768")
                    print("4) 1280 * 1024")
                    print("5) 1920*1080")
                    self.size=input("")
                    try:
                        size=int(self.size)
                        if (1<= size) and (5>= size):
                            self.size=int(self.size)
                            chooser=15                     
                        else:
                            self.size=2
                            chooser=15
                    except ValueError:
                        print("Du har ikke skrevet et helt tal")
                while (chooser==15):
                    self.filename=input("hvad skal filen hedde?")
                    if self.filename=="":
                        self.filename=nowtime
                    print (" valg er {0},{1},{2},{3},{4}".format(self.media,self.minutter,self.framerate,self.size,self.filename))
                    chooser=0


            elif self.media=="p":
                print("du har valgt preview")
                chooser=0
            else:
                print("du skal vælge f,v, eller p")
    
        
def foto(choice):
    loops=int(choice.minutter/60000/10)  #number of loops
    rest=int((choice.minutter%600000)/60000)  #number of minutes left
    for a in range (loops):  #makes 10 minute loops with upload cycle
        foto_cmd="raspistill -t 600000 -tl {0} -a 12 -md 1 -dt -p 200,200,200,200 -q 90 -o /home/pi/Pictures/cam/{1}%d.jpg".format(choice.timelapse, choice.filename)
        print(foto_cmd)
        print (loops)
        subprocess.run(foto_cmd,shell=True)
        Uploader.run(choice.filename)
    rest=rest*60000
    foto_cmd="raspistill -t {0} -tl {1} -a 12 -md 1 -dt -p 200,200,200,200 -q 90 -o /home/pi/Pictures/cam/{2}%d.jpg".format(rest, choice.timelapse, choice.filename)
    print(rest)
    subprocess.run(foto_cmd,shell=True)
    Uploader.run(choice.filename)
    
def video(choice):
    video_cmd="raspivid -t {0} -fps {1} -md {2} -p 200,200,200,200 -o /home/pi/Pictures/cam/{3}.h264".format(choice.minutter, choice.framerate, choice.size, choice.filename)
    convert_cmd="MP4Box -add  /home/pi/Pictures/cam/{0}.h264 /home/pi/Pictures/cam/{0}.mp4".format(choice.filename)
    print (video_cmd)
    subprocess.run(video_cmd,shell=True)
    subprocess.run(convert_cmd,shell=True)
    os.remove("/home/pi/Pictures/cam/{0}.h264".format(choice.filename))
    vid_uploader.run(choice.filename)

choice = Choices()
if choice.media=="f":
    foto(choice)

elif choice.media=="v":
    video(choice)

elif choice.media=="p":
    print("her skal preview-delen ligge")
