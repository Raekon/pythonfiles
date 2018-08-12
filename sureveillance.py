

import threading
import subprocess
import ftplib
import os
import time
import datetime
from PIL import Image

class Surveillance(threading.Thread): 
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


t=1
while t==1:
    timer=int(time.strftime("%H"))
    print (timer)
    if timer>=7 and timer<=23:
        cmd = "raspistill  -o /home/pi/Pictures/cam/test%d.jpg -a 12 -dt -w 1024 -h 800 -q 100 -t 1800000 -tl 2000 -p 200,200,200,200"
        subprocess.run(cmd, shell=True)
        thread=Surveillance(3600,2)
        thread.start()
    else:
        time.sleep(60)
    