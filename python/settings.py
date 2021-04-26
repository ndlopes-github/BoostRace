# -*- coding: utf-8 -*-
import numpy as np
from autoclass import autorepr

@autorepr
class parameters():
    def __init__(self):
        self.timestep=0.4 # Initial time step for solver 0.4
        self.observertimestep=1.0 #observer time step in seconds
        self.observernsteps=7200 #number of steps to be saved
        self.endtime=self.observernsteps*self.observertimestep
        #Waves [[number,delay,init speed]]
        self.waves=np.array([[2800,0.0,3.34],[2800,210.0,2.92],[6300,450.0,2.5]])
        self.nrunners=np.sum(self.waves[:,0].astype(int)) #number of runners

        self.minratio= 15./40.  #  15 runners per 40 m2
        self.maxration= 25./40. #  25 runners per 40 m2

        self.linearfrontview=4 # linear impact zone
