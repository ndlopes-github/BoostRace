#!/usr/bin/env python
# coding: utf-8

#### Race Animation ########################################################################
from visuals import *


import pickle
#load it

with open(f'results/group.pickle', 'rb') as file:
    group = pickle.load(file)
file.close()

with open(f'results/times.pickle', 'rb') as file:
    times = pickle.load(file)
file.close()


with open(f'results_free/group.pickle', 'rb') as file:
    group_free = pickle.load(file)
file.close()

with open(f'results_free/times.pickle', 'rb') as file:
    times_free = pickle.load(file)
file.close()

timesvisuals(times=times,times_free=times_free,group=group,group_free=group_free)
