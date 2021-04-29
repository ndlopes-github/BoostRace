#!/usr/bin/env python
# coding: utf-8
import argparse

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-fr", "--firstrunner",default=0, required=False,
   help="First runner to consider, default 0")
ap.add_argument("-lr", "--lastrunner",default=10000, required=False,
   help="First runner to consider, default 10000")
ap.add_argument("-nr", "--nrunners", default=10, required=False,
   help="Number of runners to plot")

args = vars(ap.parse_args())

#### Race Animation ########################################################################
from visuals import rhossvisuals


import pickle
#load it
with open(f'results/nsteps.pickle', 'rb') as file:
    nsteps = pickle.load(file)
file.close()

with open(f'results/group.pickle', 'rb') as file:
    group = pickle.load(file)
file.close()

with open(f'results/ninwaves.pickle', 'rb') as file:
    ninwaves = pickle.load(file)
file.close()

import random
fr=int(args['firstrunner'])
lr=int(args['lastrunner'])
nr=int(args['nrunners'])
rlist=random.sample(range(fr,lr),nr)

rhossvisuals(rlist,nsteps=nsteps,group=group,ninwaves=ninwaves,dpi=100)
