#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import threading
import subprocess
import ftplib
import os
import time
import datetime
from PIL import Image

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
            file= open('/home/pi/Pictures/cam/{0}'.format(i),'rb')
            session.storbinary('STOR skole/vagt/{0}'.format(i), file)
            file.close  
        session.quit
        dir_cont=os.listdir("/home/pi/Pictures/cam")
        for i in dir_cont:
            os.remove("/home/pi/Pictures/cam/{0}".format(i))
            
Uploader.run("a")