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
        print("thread running")
        dir_cont=os.listdir("/home/pi/Pictures/cam")
        print (dir_cont)
        session = ftplib.FTP('ftp.kongesquash.dk','kongesquash.dk','Raekon75')
        for i in dir_cont:
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
        chooser=0
        while chooser==0:
            self.version=input("Raspicam version 1 eller 2? ")
            try:
                if (int(self.version)==1 or int(self.version)==2):
                    chooser=1
            except ValueError:
                print("Du skal vælge enten 1 eller 2")
            
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
                    
                    print("    model 1          model 2")
                    print("1) 1920*1080         1920*1080")
                    print("2) 2592*1944         3280*2464")
                    print("3) 2592*1944         3280*2464")
                    print("4) 1296*972          1640*1232")
                    print("5) 1296*730          1640*922")
                    print("6)  640*480          1280*720")
                    print("7)  640*480           640*480")
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
                    self.flipped=input("skal billedet flippes? (j) (n)")
                    if self.flipped=="n":
                        self.flipped=""
                    elif self.flipped=="j":
                        self.flipped="-hf -vf"
                    chooser=6
                while (chooser==6):
                    self.filename=input("hvad skal filen hedde?")
                    if (self.filename==""):
                        self.filename=nowtime
                    print (" valg er {0},{1},{2},{3},{4},{5}".format(self.media,self.minutter,self.timelapse,self.size,self.flipped,self.filename))
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
                    print("hvilken størrelse skal filmen have?")
                    print("    model 1                      model 2")
                    print("1) 1920*1080 (1-30 fps)        1920*1080 (.1-30 fps)")
                    print("2) 2592*1944 (1-15 fps)        3280*2464 (.1-15 fps)")
                    print("3) 2592*1944 (0,16-1 fps)      3280*2464 (.1-15 fps)")
                    print("4) 1296*972  (1-42 fps)        1640*1232 (.1-40 fps)")
                    print("5) 1296*730  (1-49 fps)        1640*922  (.1-40 fps)")
                    print("6)  640*480  (42-60 fps)       1280*720  (40-90 fps)")
                    print("7)  640*480  (60-90 fps)        640*480  (90-200 fps)")
                    self.size=input("")
                    try:
                        size=int(self.size)
                        if (1<= size) and (7>= size):
                            self.size=int(self.size)
                            chooser=14                     
                        else:
                            self.size=0
                            chooser=14
                    except ValueError:
                        print("Du har ikke skrevet et helt tal")
                        
                while chooser==14:
                    self.framerate=input("hvor mange billeder i sekundet?")
                    try:
                        val=int(self.framerate)
                        chooser=15
                    except ValueError:
                        print("du har ikke skrevet et helt tal.\n")
                while chooser==15:
                    self.flipped=input("skal filmen flippes?  (j) (n)")
                    if self.flipped=="n":
                        self.flipped=""
                    elif self.flipped=="j":
                        self.flipped="-hf -vf"
                    chooser=16
                while (chooser==16):
                    self.filename=input("hvad skal filen hedde?")
                    if self.filename=="":
                        self.filename=nowtime
                    print (" valg er {0},{1},{2},{3},{4}{5}".format(self.media,self.minutter,self.framerate,self.size,self.flipped,self.filename))
                    chooser=0


            elif self.media=="p":
                print("du har valgt preview")
                chooser=0
            else:
                print("du skal vælge f,v, eller p")
    
        
def foto(choice):
    print("fotoloop kører")
    loops=int(choice.minutter/60000/10)  #number of loops
    rest=int((choice.minutter%600000)/60000)  #number of minutes left3
    print("version valgt er {0}".format(choice.version))
    if (choice.version=="1"):
        Switcher={
            0:"",
            1:"-w 1920 -h 1080",
            2:"-w 2592 -h 1944",
            3:"-w 2592 -h 1944",
            4:"-w 1296 -h 972",
            5:"-w 1296 -h 730",
            6:"-w 640 -h 480",
            7:"-w 640 -h 480"}
    else:
        Switcher={
            0:"",
            1:"-w 1920 -h 1080",
            2:"-w 3280 -h 2464",
            3:"-w 3280 -h 2464",
            4:"-w 1640 -h 1232",
            5:"-w 1640 -h 922",
            6:"-w 1280 -h 720",
            7:"-w 640 -h 480"}
    print (Switcher[1])
    
    
    for a in range (loops):  #makes 10 minute loops with upload cycle
        foto_cmd="raspistill -t 600000 -tl {0} -a 12 -md {1} {2} {3} -dt -p 200,200,200,200 -q 100 -o /home/pi/Pictures/cam/{4}%d.jpg".format(choice.timelapse, choice.size, Switcher[choice.size],choice.flipped,choice.filename)
        print(foto_cmd)
        print (loops)
        subprocess.run(foto_cmd,shell=True)
        Uploader.run(choice.filename)
    rest=rest*60000
    foto_cmd="raspistill -t {0} -tl {1} -a 12 -md {2} {3} {4} -dt -p 200,200,200,200 -q 100 -o /home/pi/Pictures/cam/{5}%d.jpg".format(rest, choice.timelapse, choice.size, Switcher[choice.size], choice.flipped,choice.filename)
    print(foto_cmd)
    print(rest)
    subprocess.run(foto_cmd,shell=True)
    #Uploader.run(choice.filename)
    
def video(choice):
    if (choice.version==1):
        Switcher={
            0:"",
            1:"-w 1920 -h 1080",
            2:"-w 2592 -h 1944",
            3:"-w 2592 -h 1944",
            4:"-w 1296 -h 972",
            5:"-w 1296 -h 730",
            6:"-w 640 -h 480",
            7:"-w 640 -h 480"}
    else: 
        Switcher={
            0:"",
            1:"-w 1920 -h 1080",
            2:"-w 3280 -h 2464",
            3:"-w 3280 -h 2464",
            4:"-w 1640 -h 1232",
            5:"-w 1640 -h 922",
            6:"-w 1280 -h 720",
            7:"-w 640 -h 480"}
    
    print (Switcher[1])
    video_cmd="raspivid -t {0} -fps {1} -md {2} {3} {4} -p 200,200,200,200 -o /home/pi/Pictures/cam/{5}.h264".format(choice.minutter, choice.framerate, choice.size, Switcher[choice.size],choice.flipped, choice.filename)
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
