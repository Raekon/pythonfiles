import threading
import subprocess
import ftplib
import os
import time
import datetime
from PIL import Image
import gpiozero

pir  = gpiozero.MotionSensor(14)
running=True
def movement():
    print("movement")
    foto_cmd="raspistill -t 2000 -a 12 -md 5 -dt -p 200,200,200,200 -q 100 -o /home/pi/Pictures/cam/%d.jpg"
    subprocess.run(foto_cmd,shell=True)
    
while running==True:
    pir.when_motion = movement
        

