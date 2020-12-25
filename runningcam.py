#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading
import subprocess
import ftplib
import os
import time
import datetime
from PIL import Image
startup=0
while(True):
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
            session = ftplib.FTP('ftp.vestergade22.dk','vestergade22.dk','Raekon75')
            for i in dir_cont:
                img = Image.open("/home/pi/Pictures/cam/{0}".format(i)).convert('RGB')
                img.save("/home/pi/Pictures/cam/{0}".format(i))
                os.rename("/home/pi/Pictures/cam/{0}".format(i),"/home/pi/Pictures/vault/{0}".format(i))
            dir_cont=os.listdir("/home/pi/Pictures/vault")
            for i in dir_cont:                    
                file= open('/home/pi/Pictures/vault/{0}'.format(i),'rb')
                session.storbinary('STOR 3dcam/{0}'.format(i), file)
                file.close  
            session.quit
            dir_cont=os.listdir("/home/pi/Pictures/vault")
            for i in dir_cont:
                os.remove("/home/pi/Pictures/vault/{0}".format(i))

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
    ##Her startes løkken der vælger alle parametrene            
            while(chooser==1):
                chooser=2
                while chooser==2:
                    self.timelapse=input("hvor mange sekunder imellem hvert billede?")
                    try:
                        self.timelapse=int(self.timelapse)*1000
                        chooser=4
                    except ValueError:
                        print("du har ikke skrevet et helt tal.\n")
                    while chooser==4:
                        self.filename=input("hvad skal filen hedde?")
                        if self.filename=="":
                            self.filename=nowtime
                        chooser=6
                    while (chooser==6):
                        self.flip=input("Skal billedet flippes? (j/n) ")
                        if self.flip=="j" or self.flip=="n":
                            chooser=0
                        else:
                            print("Du skal vælge enten j eller n")

    def foto(choice):
        if (choice.version=="1"):
            Switcher={
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
        
        if (choice.flip=="j"):
            Flip="-hf -vf"
        else:
            Flip=""
        
        foto_cmd="raspistill  -tl {0} -a 12 -md 1 -w 1920 -h 1080 -dt -p 200,200,200,200 {1} -q 100 -o /home/pi/Pictures/cam/{2}%d.jpg".format(choice.timelapse,Flip,choice.filename)
        print(foto_cmd)
        subprocess.run(foto_cmd,shell=True)
        Uploader.run(choice.filename)
    if (startup==0):
        startup=1
        choice=Choices()
    foto(choice)

    ## Preview-delen ligger oppe i choise-classen. dermed starter den medievælgeren forfra hver gang

    ##elif choice.media=="p":
    ##    print("her skal preview-delen ligge")

