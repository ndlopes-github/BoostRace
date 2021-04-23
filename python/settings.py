# -*- coding: utf-8 -*-
import numpy as np

class parameters():
    def __init__(self):
        self.simtime=7200 #time to be simulated in seconds
        self.observerstep=1 #observer time step
        #Waves [[number,delay,init speed]]
        self.waves=np.array([[2800,0.0,3.34],[2800,210.0,2.92],[6300,450.0,2.5]])
        self.nrunners=np.sum(self.waves[:,0].astype(int)) #number of runners
        self.minratio= 15./40.  #  15 runners per 40 m2
        self.maxration= 25./40. #  25 runners per 40 m2
