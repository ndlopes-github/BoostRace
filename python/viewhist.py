#!/usr/bin/env python
# coding: utf-8

#### Race Animation ########################################################################
from visuals import *

import pickle
#load it
with open(f'results/nsteps.pickle', 'rb') as file:
    nsteps = pickle.load(file)
file.close()

with open(f'results/group.pickle', 'rb') as file:
    group = pickle.load(file)
file.close()


histvisuals(nsteps=nsteps,group=group)
