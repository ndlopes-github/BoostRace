# -*- coding: utf-8 -*-

class parameters():
    def __init__(self):
        self.nrunners=10000 #number of runners
        self.simtime=7200 #time to be simulated in seconds
        self.observerstep=1 #observer time step
        #Waves [[number,delay]]
        self.waves=[[3333,0.0],[3333,360.0],[3334,720.0]]
