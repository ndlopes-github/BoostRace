# -*- coding: utf-8 -*-
import numpy as np
from objprint import add_objprint # To print a readable report of the settings

# Track to be considered
from tracks import *

gap=180

@add_objprint
class parameters():
    def __init__(self,
                 timestep=0.4,
                 observertimestep=1.0,
                 observernsteps=10000,#9160,
                 endtime=10000,#9160,
                 waves=np.array([[10000,0.0,2.92]]),
                 # waves=np.array( [
                 #     [3333,0,0, 0.0,3.34],
                 #     [0,3333,0, 116 +1*gap, 2.92],
                 #     [0,0,3334,  239.0+2*gap, 2.5]
                 # ]),
                 # waves=np.array( [
                 #     [3000,166,167, 0.0,3.34],
                 #     [166,3000,167, 133 +1*gap, 2.92],
                 #     [167,167,3000,  266.0+2*gap, 2.5]
                 # ]),
                 # waves=np.array( [
                 #     [2333,500,500, 0.0,3.34],
                 #     [500,2333,500, 214 +1*gap, 2.92],
                 #     [500,500,2334,  440.0+2*gap, 2.5]
                 # ]),
                 #  waves=np.array( [
                 #      [2500,0,0,0, 0.0,3.34],
                 #      [0,2500,0,0, 86 +1*gap, 2.92],
                 #      [0,0,2500,0,  176.0+2*gap, 2.5],
                 #      [0,0,0,2500,  271.0+3*gap, 2.4]
                 # ]),
                 # waves=np.array( [
                 #     [2050,150,150,150, 0.0,3.34],
                 #     [150,2050,150,150, 107 +1*gap, 2.92],
                 #     [150,150,2050,150,  206.0+2*gap, 2.5],
                 #     [150,150,150,2050,  314.0+3*gap, 2.4]
                 # ]),
                 # waves=np.array( [
                 #     [2000,100,100,100, 0.0,3.34],
                 #     [100,2000,100,200, 92 +1*gap, 2.92],
                 #     [100,100,2000,100,  186.0+2*gap, 2.5],
                 #     [300,300,300,2100,  278.0+3*gap, 2.4]
                 # ]),
                 linearfrontview=4,
                 minratio= 15./40.,
                 maxratio= 25./40.,
                 minrho=0.4,
                 maxrho=0.8,
                 stepper=2,
                 posweights=np.array([[0.2,0],[2.0,30],[1.5,60],[1.25,120],[1.0,100000]]),
                 track=track_fixed_width(20.0),
                 #track=track2,
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
B-2500,2500,5000;ok
1-2200, 100, 200; 100, 2200,200; 200, 200,4600; ok
2-1900,200,400; 200, 1900, 400; 400,400, 4200; ok
'''
