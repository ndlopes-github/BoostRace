# -*- coding: utf-8 -*-
import numpy as np
from objprint import add_objprint # To print a readable report of the settings

# Track to be considered
from tracks import track7 as track

@add_objprint
class parameters():
    def __init__(self,
                 timestep=0.4,
                 observertimestep=1.0,
                 observernsteps=7200,
                 waves=np.array([
                     [3333,0,0, 0.0,3.34],
                     [0,3333,0, 210.0,2.92],
                     [0,0,3334, 450.0,2.5]]
                 ),
                 linearfrontview=4,
                 minratio= 15./40.,
                 maxratio= 25./40.,
                 minrho=0.4,
                 maxrho=0.8,
                 stepper=2,
                 posweights=np.array([[0.2,0],[2.0,30],[1.5,60],[1.25,120],[1.0,100000]]),
                 track=track
    ):
        self.timestep=timestep # Initial time step for solver 0.4
        self.observertimestep=observertimestep #observer time step in seconds
        self.observernsteps=observernsteps #number of steps to be saved

        self.endtime=self.observernsteps*self.observertimestep

        #Waves [[number,delay,init speed]]
        self.waves=waves
        self.numberofwaves=len(self.waves)
        self.nrunners=np.sum(self.waves[:,0:self.numberofwaves].astype(int)) #number of runners

        self.linearfrontview=linearfrontview # linear impact zone
        self.minratio= minratio  #  15 runners per 40 m2
        self.maxratio= maxratio #  25 runners per 40 m2

        self.minrho=minrho #min weight of the VL speed
        self.maxrho=maxrho #max weight of the VL speed
        self.stepperdict={2 : 'abm2', 3 : 'abm3', 4 : 'abm4', 5 : 'abm5'}
        self.stepper=stepper # '2 : abm2', '3 : abm3', '4 : abm4', '5 : abm5' , # To be implemented '6: rkd5'
        self.integrator=self.stepperdict[self.stepper]
        self.posweights=posweights # Weights for race Metrics Post-Processing
        self.track=track

## NOTES & TO DOS

'''
2500/2500/5000, 0/210/450
3333/3333/3334, 0/210/450
3333/3333/3334, 0/300/600

waves=np.array([[2800,0.0,3.34],[2800,210.0,2.92],[6300,450.0,2.5]]),
waves=np.array([[3333,0.0,3.34],[3333,210.0,2.92],[3334,450.0,2.5]]),
waves=np.array([[3333,0.0,3.34],[3333,300.0,2.92],[3334,600.0,2.5]]),

waves=np.array([[2500,0,0,0.0,3.34],
                                 [0,2500,0,210.0,2.92],
                                 [0,0,5000,450.0,2.5]]),
'''
