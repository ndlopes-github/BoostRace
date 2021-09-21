# -*- coding: utf-8 -*-
import numpy as np
from objprint import add_objprint # To print a readable report of the settings

# Track to be considered
from tracks import *

gap=300

@add_objprint
class parameters():
    def __init__(self,
                 timestep=0.4,
                 observertimestep=1.0,
                 observernsteps=8160,
                 endtime=8160,
                 # waves=np.array( [
                 #     [2500,0,0.0,3.34],
                 #     [0,7500,138+gap,2.92]
                 # ]),
                 waves=np.array( [
                     [2500,0,0, 0.0,3.34],
                     [0, 2500,0, 138.0 +1*gap, 2.92],
                     [0,0,5000,  282.0+2*gap, 2.5]
                 ]),
                 linearfrontview=4,
                 minratio= 15./40.,
                 maxratio= 25./40.,
                 minrho=0.4,
                 maxrho=0.8,
                 stepper=2,
                 posweights=np.array([[0.2,0],[2.0,30],[1.5,60],[1.25,120],[1.0,100000]]),
                 track=track_fixed_width(10.0),
                 ldist=0.5
    ):
        self.timestep=timestep # Initial time step for solver 0.4
        self.observertimestep=observertimestep #observer time step in seconds
        self.observernsteps=observernsteps #number of steps to be saved

        self.endtime=endtime

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
        self.ldist=ldist # Line distances at startup in meter


## NOTES & TO DOS

'''
15/10/2021
Testes 3 ondas:
A- 3333,3333,3334; ok
1-3000,166,167; 166,3000,167; 167,167,3000; ok
2-2333,500,500; 500, 2333,500; 500, 500, 2334; ok
B-2500,2500,5000;
1-2200, 100, 200; 100, 2200,200; 200, 200,4600;
2-1900,200,400; 200, 1900, 400; 400,400, 4200;
'''
