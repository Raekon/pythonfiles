from PIL import Image
import threading
import ftplib
import time
import os
import datetime
import guizero

width_text=""


def update_size(width):
    picture_width=int(float(width))
    picture_height=int(picture_width//1.33)
    print(int(picture_height))
    width_text="{0} x {1}".format(picture_width,picture_height)
    message_text.value=picture_height
    print (width_text)


def photoUpload():
    
    box1=guizero.Box(app, layout="grid")
    text1=guizero.Text(box1,text="Hvor mange minutter skal der filmes? ", grid=[0,0])
    minutes=guizero.TextBox(box1,text="", grid=[1,0])
    minutes.focus()
    text2=guizero.Text(box1, text="hvor mange sekunder mellem hvert billede? ",grid=[0,1])
    timelapse=guizero.TextBox(box1,text="", grid=[1,1])
    text3=guizero.Text(box1, text="filnavn ? ",grid=[0,2])
    filename=guizero.TextBox(box1,text="", grid=[1,2])
    text4=guizero.Text(box1, text=("størrelse: "),grid=[0,3])
    picsize=guizero.Slider(box1, start=640, end=3280, grid=[1,3])
    
    
       
    
    button1=guizero.PushButton(box1, command=lambda:printit(minutes.get(),timelapse.get(),filename.get()), text="Submit",grid=[1,5])
    
def printit(minutes,timelapse,filename):
    print("virker knappen? {0},{1},{2}".format(minutes,timelapse,filename))
    

    

def photoNoUpload():
    pass

def videoUpload():
    pass

def videoNoUpload():
    pass

app=guizero.App(title="Surveillance tools")

menu=guizero.MenuBar(app,toplevel=["Photo", "Video"],options=[[["With upload",photoUpload],["Without upload",photoNoUpload]],[["with upload",videoUpload],["Without upload",videoNoUpload]]])
picsize=guizero.Slider(box1, start=640, end=3280, grid=[1,3])
textbox_message=guizero.TextBox(app)
message=guizero.Text(app, text="Hvad skal vi lave i dag?")

app.display()

