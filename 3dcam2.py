#!/usr/bin/env python
# -*- coding: utf-8 -*-# !

import subprocess
import ftplib
import os
import time
import datetime
import RPi.GPIO as gpio
#import picamera
os.system("pkill raspivid")
#camera=picamera.PiCamera()
gpio.setmode(gpio.BCM)
gpio.setup(4,gpio.IN, gpio.PUD_DOWN)   #knap til at vælge antal kvarter
gpio.setup(17,gpio.IN, gpio.PUD_DOWN)   #knap til at vælge timer
gpio.setup(27,gpio.IN,gpio.PUD_DOWN)    #knap til at stoppe programmet
gpio.setup(22,gpio.IN,gpio.PUD_DOWN)    #knap til at starte optagelsen
gpio.setup(5,gpio.OUT, initial=1)  #led til at vise programmet er klar
gpio.setup(6,gpio.OUT, initial=0)  #led til at vise timer
gpio.setup(13,gpio.OUT, initial=0)  #led til at vise kvarter


starttid=time.time()+28800
print(starttid)


def dato():     #finder datoen og laver et filnavn ud af det
    tid=datetime.datetime.now().strftime("%A%d%m%Y%H%M")    #laver datodelen af filnavnet
    filnavn="{0}.h264".format(tid)  #sætter datodelen og filtypen sammen
    print(filnavn)      ##debug  printer filnavnenet til kosnsol
    return(filnavn) #sender filnavnet retur.

def tid(starttid):  #findertiden der skal optages i, ved at trykke på knappen
    debounce=0    #variable for debouncing of the buttons
    kvarter=0   #variable that keeps track of the quarter hours
    timer=0     #variable that keeps track of the hours
    blinktimer=time.time()  #timing variable for the blinking of the chosen length of filming
    os.system("pkill raspivid")   #Kills any existing raspivid processes, that might accidentally run
    print("while fra tid er gået i gang")     #Debugging
    while gpio.input(22)==0 and starttid>=time.time():     #this runs as long as the "Go" button isn't pressed and the allocated time hasn't passed the time-sounter may be unnecessary
    
        if blinktimer+4<=time.time():    #this checks if the blinker function should be started
            blinker(timer,kvarter)      #starts the blinker with the hours and quarterhours as options
            blinktimer=time.time()      #resets the timing variable for checking if it is time to blink.
    
        if gpio.input(27)==1:       #the gpio27 button is the programs killswitch.
            os.system("pkill raspivid")  #Kills any existing raspivid processes, that might accidentally run
            gpio.output(5,0)
            gpio.output(6,0)
            gpio.output(13,0)
            raise SystemExit()      # exits the program
        
        elif gpio.input(4)==1 and gpio.input(17)==1:    # both time buttons will reset the time
            print("begge tidknapper er trykket ned")        #deugging
            kvarter=0
            timer=0
        
        elif debounce==0:       #if the buttons has been released it will check if they has beenpressed again
            #print("debounce er nul")  debugging
            if gpio.input(4)==1:
                kvarter+=1
                debounce=1
                time.sleep(0.2)
                print("kvarter er {0}".format(kvarter))   #for debugging
            
            elif gpio.input(17)==1:
                timer+=1
                debounce=1
                time.sleep(0.2)
                print(" timer er {0}".format(timer))   #for debugging
            
            else:
                pass
                #time.sleep(1)  #for debugging
            
        elif debounce==1 and gpio.input(4)==0 and gpio.input(17)==0:   #resets the debounce var if none of the time buttons are pressetd
            print("Debounce sættes til 0")
            debounce=0
            time.sleep(0.2)    # for debouncing purposes
        elif debounce==1:
            time.sleep(0.2)     #for debouncing purposes
    
    recordTime=timer*60*60+kvarter*15*60   ###FIX ME  husk at der skal ganges med tusind, for at få tiden i sekunder. nu er den i milli
    return (recordTime)
                    
    

def video(filename,recordTime): #optager videoen
    print("jeg har modtaget følgende. filnavn: {0}  tid: {1}".format(filename,recordTime))  #for debugging. Erase
    cmd = "raspivid -w 1280 -h 1024 -t {0} -fps 4 -p 640,512,400,400 -o /home/pi/Pictures/cam/{1}".format(recordTime, filename)
    print (cmd)
    subprocess.run(cmd, shell=True)
    
    
def upload(filename):   #uploader til serveren og sletter originalen
      ##stopper raspivid processen i tilfælde af, at den er fortsat ud over det, den skal
    session = ftplib.FTP('ftp.kongesquash.dk','kongesquash.dk','Raekon75')
    file= open('/home/pi/Pictures/cam/{0}'.format(filename),'rb')
    session.storbinary('STOR skole/{0}.mp4'.format(filename), file)
    file.close
    #####dette skal måske slettes til sidste#####
    file=open('/home/pi/pythonfiles/camera-progs/3dcam.py','rb')        #this uploads the program itself
    session.storbinary('STOR skole/3dcam.py',file)
    file.close
    ######   hertil kører et kopier sig-selv- system skal måske slettes####
    session.quit()
    os.remove("/home/pi/Pictures/cam/{0}".format(filename))
    return()

def blinker(timer,kvarter):  #funktion der blinker med de to leds
    for a in range (0,timer):  #blink for the hours
        gpio.output(6,1)
        time.sleep(0.2)
        gpio.output(6,0)
        time.sleep(0.2)
    for a in range (0,kvarter):    #blink for the quarter-hours
        gpio.output(13,1)
        time.sleep(0.2)
        gpio.output(13,0)
        time.sleep(0.2)
    return()

while starttid>=time.time():
    filnavn=dato()   #sets the filname
    recordTime=tid(starttid)    #the function to set recording time (here is also the blinker
    video(filnavn,recordTime)   #the recording function 
    upload(filnavn) #here, the file gets uploaded
    
    time.sleep(1)
    
    





