#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this program should ask the user, which type of camera action he wants to make in the remote pi.
#options should include streamed footage, stills and video (timelapse and otherwise.

import subprocess
import time
import datetime
import ftplib
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(4,gpio.IN, gpio.PUD_UP)

minutter=0  #minuttallet til evt filnavn
sekunder=0  #skeundtallet
timerne=0     #timetallet
polls = 0     #antal gange poll-funktionen har kørt (til debugging)
filename="a"   #varabel til filnavnet, stykket sammen af ovesntående info

userchoice=0   #hvilket valg, film eller video
runtime=0      # hvor lang tid skal den optage i alt
timelapse=0    # hvor lang tid skal der være mellem billederne
fps=0          #hvor mange billeder i sekundet på filmen
size=0         #standardstørrelse på billeder
height=0       #højde på billedet. - defaulter til mode 4
width=0        #bredde på billedet - defaulter til mode 4
dateonpictures="n"     # skal der dato på billederne


keepmealive=1

def Billeder():
    try:
        runtime = int(input ("hvor mange minutter skal der optages i >>  "))
    except ValueError:
        print("Der var en fejl i tallet. Det må ikke være bogstaver")
        print()
        Billeder()
    else:
        print()
        print ("ok, der skal optages i {0} minutter".format(runtime))
        print()
        runtime = runtime*60000
        return(runtime)
        BillederTimelapse()
        
def BillederTimelapse():
    try:
        timelapse = int(input("hvor mange sekunder skal der være mellem hvert billede?>>  "))
    except ValueError:
        print(" Der var en fejl i antallet af sekunder... der skal bruges et tal")
        print()
        BillederTimelapse()
    else:
        print()
        print("ok, der skal optages et billede for hver {0} sekunder".format(timelapse))
        print()
        return(timelapse)
        BillederSize()

def BillederSize():
    print("hvad er størrelsen på billederne? ")
    print("Standardstørrelser er : ")
    print("1) 1920x1080 (16:9) max 30 frames")
    print("2) 3280x2464 (4:3)   max 15 frames")
    print("4) 1640x1232 (4:3)   max 40 frames")
    print("5) 1640x922  (16:9)   max 40 frames")
    print("6) 1280x720    (16:9) 40-90 frames")
    print("7) 640x480    (4:3)   40-90 frames")
    print ("0)  speciel størrelse")
    try:
        size=int(input("størrelse >>  "))
    except ValueError:
        print("dit valg skal være et tal  ")
        print()
        BillederSize()
    else:
        if size==0:
            CustomSize()
            
        elif size==3:
            print("der er ikke nogen 3'er...")
            print()
            BillederSize()
        else:
            print("størrelse ok")
            print()
            return(size)
            DateOnPicture()

def DateOnPicture():
    dateonpictures=input("skal der dato på billederne?  (j/n)   >>")
    if dateonpictures=="j":
        print("ok, der kommer dato på billederne.")
        print()
        return("-a 8")
        Filename()
    elif dateonpictures=="n":
        print("ok, der kommer ikke dato på billederne.")
        print()
        return()
        Filename()
    else:
        print("jeg forstår ikke hvad du skriver. det skal være \"j\" eller \"n\"...")
        DateOnPicture()

def Filename():
    filename=input("hvad skal filen hedde? (der kommer timestamp på til sidst)   >>")
    return(filename)
    Resume() 
    
        
while keepmealive==1:    #main loop
    
    userchoice = input ("billeder (b), video (v) eller stream (s)?")
    
    if userchoice=="b":
        runtime=Billeder()
        timelapse=BillederTimelapse()
        size=BillederSize()
        dateonpicture=DateOnPicture()
        filename=Filename()
        print("optage tid er {0} timelapse er {1} størrelse er {2} dato {3} filnavn {4}".format(runtime, timelapse, size, dateonpicture, filename)) 
        if input("er disse settings rigtige? (j/n)")=="j":
            print ("så kører vi")
            cmd = "raspistill -md {0} -q 75 -t {1} -tl {2} -p 100,100,400,300 {3} -ts -e jpg -o /home/pi/Pictures/cam/{4}%d.jpg".format(size,runtime, timelapse, dateonpicture, filename)
            print (cmd)
            subprocess.call(cmd, shell=True)
            time.sleep(runtime)
    elif userchoice=="v":
        pass
    
    elif userchoice=="s":
        pass
    
    else:
        pass