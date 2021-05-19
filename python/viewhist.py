#!/usr/bin/env python
# coding: utf-8

#### Race Animation ########################################################################
from visuals import *

import pickle
#load it

with open(f'results/group.pickle', 'rb') as file:
    group = pickle.load(file)
file.close()


histvisuals(group=group)
