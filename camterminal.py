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

class Choices ():
    def __init__ (self):
        chooser=1
        sub_chooser=1
        while(chooser==1):
            self.media=input("Foto (f) eller Video (v) eller preview (p)?")
            if self.media=="f":
                print("du har valgt foto")
                chooser=2
                while chooser==2:
                    self.minutter=input("hvor mange minutter skal der filmes?")
                    try:
                        val=int(self.minutter)
                        chooser=3     
                    except ValueError:
                        print("du har ikke skrevet et helt tal\n")
                while chooser==3:
                    self.timelapse=input("hvor mange sekunder imellem hvert billede?")
                    try:
                        val=int(self.timelapse)
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
            elif self.media=="v":
                print("du har valgt video \n")
                self.minutter=input("hvor mange minutter skal der filmes?")
                try:
                    val=int(self.minutter)
                    chooser=0
                except ValueError:
                    print("du har ikke skrevet et helt tal")
                
                
            elif self.media=="p":
                print("du har valgt preview")
                chooser=0
            else:
                ("du skal vælge f,v, eller p")
        
            
p1 = Choices()
print (p1.media)