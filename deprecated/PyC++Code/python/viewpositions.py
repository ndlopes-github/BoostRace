#!/usr/bin/env python
# coding: utf-8

#### Race Animation ########################################################################
from visuals import spystep
import argparse
# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-fr", "--firstrunner",default=0, required=False,
   help="First runner to consider, default 0")
ap.add_argument("-lr", "--lastrunner",default=100, required=False,
   help="First runner to consider, default 10000")
ap.add_argument("-st", "--step", default=0, required=False,
   help="Step to plot")

args = vars(ap.parse_args())

fr=int(args['firstrunner'])
lr=int(args['lastrunner'])
st=int(args['step'])


import pickle
#load it

with open(f'results/group.pickle', 'rb') as file:
    group= pickle.load(file)
file.close()


spystep(ws=fr,we=lr,step=st, group=group)
