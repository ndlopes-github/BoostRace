# -*- coding: utf-8 -*-
import numpy as np
from autoclass import autorepr

@autorepr
class parameters():
    def __init__(self,timestep=0.4,
                 observertimestep=1.0,
                 observernsteps=7200,
                 waves=np.array([[2800,0.0,3.34],[2800,210.0,2.92],[6300,450.0,2.5]]),
                 linearfrontview=4,
                 minratio= 15./40.,
                 maxratio= 25./40.,
                 minrho=0.4,
                 maxrho=0.8,
                 stepper=2
    ):
        self.timestep=timestep # Initial time step for solver 0.4
        self.observertimestep=observertimestep #observer time step in seconds
        self.observernsteps=observernsteps #number of steps to be saved

        self.endtime=self.observernsteps*self.observertimestep

        #Waves [[number,delay,init speed]]
        self.waves=waves
        self.nrunners=np.sum(self.waves[:,0].astype(int)) #number of runners

        self.linearfrontview=linearfrontview # linear impact zone
        self.minratio= minratio  #  15 runners per 40 m2
        self.maxratio= maxratio #  25 runners per 40 m2

        self.minrho=minrho #min weight of the VL speed
        self.maxrho=maxrho #max weight of the VL speed

        self.stepper=stepper # '2 : abm2', '3 : abm3', '4 : abm4', '5 : abm5' , # To be implemented '6: rkd5'
