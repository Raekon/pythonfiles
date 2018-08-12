from PIL import Image
import threading
import ftplib
import time
import os
import datetime
import guizero



def update_size(width):
    picture_width=int(float(width))
    picture_height=int(picture_width//1.33)
    width_text="{0} x {1}".format(picture_width,picture_height)
    textbox_message.value=width_text
    

def photoUpload():
    box1.show()
 
    
def printit():
    print("virker knappen? {0},{1},{2},{3}".format(minutes.get(),timelapse.get(),filename.get(),picsize.value))
    

    

def photoNoUpload():
    pass

def videoUpload():
    pass

def videoNoUpload():
    pass

app=guizero.App(title="Surveillance tools")

menu=guizero.MenuBar(app,toplevel=["Photo", "Video"],options=[[["With upload",photoUpload],["Without upload",photoNoUpload]],[["with upload",videoUpload],["Without upload",videoNoUpload]]])

box1=guizero.Box(app, layout="grid")
box1.hide()
text1=guizero.Text(box1,text="Hvor mange minutter skal der filmes? ", grid=[0,0])
minutes=guizero.TextBox(box1,text="", grid=[1,0])
minutes.focus()
text2=guizero.Text(box1, text="hvor mange sekunder mellem hvert billede? ",grid=[0,1])
timelapse=guizero.TextBox(box1,text="", grid=[1,1])
text3=guizero.Text(box1, text="filnavn ? ",grid=[0,2])
filename=guizero.TextBox(box1,text="", grid=[1,2])
text4=guizero.Text(box1, text=("størrelse: "),grid=[0,3])
picsize=guizero.Slider(box1, start=640, end=3280, grid=[1,3],command=update_size)
picsize.text_size=1
picsize_message=guizero.Text(box1, text="billedstørrelse", grid=[0,4])
textbox_message=guizero.Text(box1, text="640 x 480",grid=[1,4])
button1=guizero.PushButton(box1, command=printit,  text="Submit",grid=[1,5])
message=guizero.Text(app, text="Hvad skal vi lave i dag?")

app.display()
args=[minutes.get(),timelapse.get(),filename.get(),picsize.value],
