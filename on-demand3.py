from PIL import Image
import threading
import ftplib
import time
import os
import datetime
import guizero
import subprocess



def update_size(width):
    picture_width=int(float(width))
    picture_height=int(picture_width//1.33)
    width_text="{0} x {1}".format(picture_width,picture_height)
    textbox_message.value=width_text
    

def key_choice(data):
    key=data.key
    if(key=="f"):
        photo_choice()
    elif(key=="v"):
        video_choice()
    elif(key=="p"):
        preview_only()
        
def preview_only():
    cmd="raspivid -n -ih -t 0 -rot 0 -w 640 -h 480 -b 500000 -fps 15 -o -|nc -lkv4 5001"
    subprocess.run(cmd,shell=True)

def photo_choice():
    box0.hide()
    box1.show()
 
    
def printit():
    print("virker knappen? {0},{1},{2},{3}".format(minutes.get(),timelapse.get(),filename.get(),picsize.value))
    try:
        minute=int(minutes.get())
        print(minute*55)
    except ValueError:
        print("tiden er ikke angivet som et tal")
    

def photoUploadShooter():
    try:
        minutter=int(minutes.get())*60000
        timelapse_int=int(timelapse.get())*1000
        pic_width=int(picsize.value)
        pic_height=int(pic_width/1.33)
        print("der tages timelapse i {0} sekunder, med {1} sekunder mellem shots, i en opløsning på {2} x {3}".format(minutes.get(),timelapse.get(),pic_width,pic_height))
        cmd="raspistill  -o /home/pi/Pictures/cam/{0}%d.jpg -a 12 -dt -w {1} -h {2} -ISO 100 -q 100 -t {3} -tl {4} -p 200,200,200,200".format(filename.get(),pic_width,pic_height,minutter,timelapse_int)
        subprocess.run(cmd,shell=True)
        
    except ValueError:
        print("en af tiderne var ikke et tal. Ændre tiden til et tal")


def photoNoUpload():
    pass

def video_choice():
    pass

def videoNoUpload():
    pass

app=guizero.App(title="Surveillance tools")

menu=guizero.MenuBar(app,toplevel=["Photo", "Video"],options=[[["With upload",photo_choice],["Without upload",photoNoUpload]],[["with upload",video_choice],["Without upload",videoNoUpload]]])
message=guizero.Text(app, text="Hvad skal vi lave i dag?",grid=[0,0])
blank_message=guizero.Text(app, text="")
box0=guizero.Box(app, layout="grid")
box0_text0=guizero.PushButton(box0, text="Tryk f for foto", command=photo_choice, grid=[0,2])
box0_text1=guizero.PushButton(box0, text="Tryk v for video", command=video_choice, grid=[0,3])
box0_text2=guizero.PushButton(box0, text="Tryk p for livepreview", command=preview_only, grid=[0,4])
box0.show()
box1=guizero.Box(app, layout="grid")
box1.hide()
text1=guizero.Text(box1,text="Hvor mange minutter skal der optages? ", grid=[0,0])
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
button1=guizero.PushButton(box1, command=photoUploadShooter,  text="Submit",grid=[1,5])

box2=guizero.Box(app, layout="grid")
box2.hide()
box2_text1=guizero.Text(box2,text="Hvor mange minutter skal der optages? ", grid=[0,0])
box2_minutes=guizero.TextBox(box2,text="", grid=[1,0])
box2_minutes.focus()
box2_text2=guizero.Text(box2, text="Hvad er framerate? (billeder pr. sekund)",grid=[0,1])
box2_timelapse=guizero.TextBox(box2,text="", grid=[1,1])
box2_text3=guizero.Text(box2, text="filnavn ? ",grid=[0,2])
box2_filename=guizero.TextBox(box2,text="", grid=[1,2])
box2_text4=guizero.Text(box2, text=("størrelse: "),grid=[0,3])
box2_picsize=guizero.Slider(box2, start=640, end=3280, grid=[1,3],command=update_size)
box2_picsize.text_size=1
box2_picsize_message=guizero.Text(box2, text="billedstørrelse", grid=[0,4])
box2_textbox_message=guizero.Text(box2, text="640 x 480",grid=[1,4])
box2_button1=guizero.PushButton(box2, command=photoUploadShooter,  text="Submit",grid=[1,5])


app.when_key_pressed= key_choice

app.display()

#args=[minutes.get(),timelapse.get(),filename.get(),picsize.value]
# git hub  zMtZLSvEGVEt6Bg4