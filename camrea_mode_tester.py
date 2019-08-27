import threading
import subprocess
import ftplib
import os
import time
import datetime
from PIL import Image

mode=1

quality=100

iso=400

ev = ""#"-ev 4"

awb = "auto"

ss= 400

exposure="auto"

ag = "" #"-ag 1"

dg = "" #"-dg 1"


cmd = "raspistill -w 1920 -h 1080 -md {0} -q {1} -t 4000 -ISO {2} {3} -awb {4} -ss {5} -ex {6} {7} {8} -ts -o /home/pi/Pictures/cam/testers%d".format(mode, quality, iso, ev, awb, ss, exposure, ag, dg)
subprocess.run(cmd,shell=True)

cmd2 = "raspistill -w 1920 -h 1080 -md {0} -ts -q {1} -t 4000 -o /home/pi/Pictures/cam/auto%d".format(mode, quality)
subprocess.run(cmd2,shell=True)