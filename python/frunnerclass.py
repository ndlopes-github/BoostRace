# coding: utf-8
import numpy as np
#import numba as nb

from objprint import add_objprint # To print a readable report of the settings
np.random.seed(2875620985)


@add_objprint
class runners():
    def __init__(self,group=None):
        self.group=group
        self.pos=np.array([runner.pos for runner in self.group])
        self.vels=np.array([runner.vels for runner in self.group])
        self.rhos=np.array([runner.rhos for runner in self.group])
        self.wavedelays=np.array([runner.wavedelay for runner in self.group])
        self.waveinitspeeds=np.array([runner.waveinitspeed for runner in self.group])
        self.avgspeeds=np.array([runner.avgspeed for runner in self.group])
        self.slopefactors=np.array([runner.slopefactor for runner in self.group])
        self.speedfunctions=np.array([runner.poly1dspeed2 for runner in self.group])
        self.originalspeedfunctions=np.array([runner.poly1dspeed2 for runner in self.group])
        self.size=len(group)
        self.colors=[runner.color for runner in self.group]
        self.names=[runner.name for runner in self.group]
        self.instantspeed=np.zeros(self.size)





@add_objprint
class frunner():
    def __init__(self,time,wavedelay=0.0,waveinitspeed=0.0,wavecolor='b'):
        self.time=time
        self.wavedelay=wavedelay
        self.waveinitspeed=waveinitspeed
        self.avgspeed=10000/(self.time*60) #m/s
        self.color=wavecolor
        self.slopefactor=np.random.uniform(-13.0,-3.0)
        self.poly1dspeed2=np.poly1d([self.slopefactor,self.avgspeed])
        self.name='f'+str(round(self.time,1))



    def init(self,nsteps,x0=0.0,sdelay=0.0):
        self.pos=np.zeros(nsteps+1)
        self.vels=np.zeros(nsteps+1)
        self.rhos=np.zeros(nsteps+1)
        self.pos[0]=x0
        self.rank=None
        self.frontrunners=None
        self.frontrunnerswindow=None
