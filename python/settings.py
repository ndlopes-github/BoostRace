# -*- coding: utf-8 -*-
import numpy as np

class parameters():
    def __init__(self):
        self.nrunners=10000 #number of runners
        self.simtime=7200 #time to be simulated in seconds
        self.observerstep=1 #observer time step
        #Waves [[number,delay,init speed]]
        self.waves=np.array([[3333,0.0,3.34],[3333,360.0,2.92],[3334,720.0,2.5]])
        self.minratio= 15./40.  #  15 runners per 40 m2
        self.maxration= 25./40. #  25 runners per 40 m2
