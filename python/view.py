#!/usr/bin/env python
# coding: utf-8
import argparse

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-an", "--anim",default=1, required=False,
   help="1 to produce the animation, 0 otherwise")
ap.add_argument("-sh", "--show",default=1, required=False,
   help="1 to show animation, 0 otherwise ")
ap.add_argument("-af", "--animfile", default=None, required=False,
   help="save animation to file 'foo'.mp4")

args = vars(ap.parse_args())

#### Race Animation ########################################################################
from visuals import *
DPI=150
FPS=25  #Frames per second

ANIM=int(args['anim']) # execute animation
SHOW=0
if ANIM:
    SHOW=int(args['show']) #Show animation

FILENAME=args['animfile']
if(args['animfile'] == None):
    SAVE=0
else:
    SAVE=1 #Save to File

import pickle
#load it

with open(f'results/group.pickle', 'rb') as file:
    group = pickle.load(file)
file.close()


with open(f'results/ninwaves.pickle', 'rb') as file:
    ninwaves = pickle.load(file)
file.close()

racevisuals(anim=ANIM,show=SHOW,save=SAVE,filename=FILENAME,
            group=group,ninwaves=ninwaves,fps=FPS,dpi=DPI)
