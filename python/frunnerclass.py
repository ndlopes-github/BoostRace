# coding: utf-8
import numpy as np
#import numba as nb

from autoclass import autorepr
np.random.seed(2875620985)


@autorepr
class runners():
    def __init__(self,group=None):
        self.group=group
        self.pos=np.array([runner.pos for runner in self.group])
        self.wavedelays=np.array([runner.wavedelay for runner in self.group])
        self.avgspeeds=np.array([runner.avgspeed for runner in self.group])
        self.slopefactors=np.array([runner.slopefactor for runner in self.group])
        self.speedfunctions=np.array([runner.poly1dspeed2 for runner in self.group])
        self.originalspeedfunctions=np.array([runner.poly1dspeed2 for runner in self.group])
        self.size=len(group)
        self.colors=[runner.color for runner in self.group]
        self.names=[runner.name for runner in self.group]
        self.instantspeed=np.zeros(self.size)

    #@nb.jit
    def setpositions(self,K,i):
        self.pos[:,i+1]=self.pos[:,i]+1./6.0*(K[0]+2*K[1]+2*K[2]+K[3])
        for index,runner in enumerate(self.group):
            runner.pos[i+1]=self.pos[index,i+1]


    #@nb.jit
    def getsorted(self,i):
        #get the sorted order of the runners at i step
        #sorted np.arrays with runners number and position
        #last->first
        sortedrunners=np.argsort(self.pos[:,i+1])
        sortedpositions=np.sort(self.pos[:,i+1])
        N=len(sortedpositions)
        dists=sortedpositions[10:]-sortedpositions[:-10]
        slowers=np.where(dists<4)
        #print(slowers[0],len(slowers[0]))
        return sortedrunners,sortedpositions,dists,slowers

    def updatespeeds(self,sortedpositions, sortedrunners,slowers):
        #get the sorted order of the runners at i step
        #sorted np.arrays with runners number and position
        #last->first

        p=0.5
        self.speedfunctions[:,0]=self.originalspeedfunctions[:,0]
        self.speedfunctions[:,1]=self.originalspeedfunctions[:,1]

        for i in slowers[0]:
            assert len(slowers[0])>0, 'enters non valid loop slowers[0]'
            speeds=np.zeros(10)
            for j in range(10):
                speeds[j]=self.instantspeed[sortedrunners[i+j+1]]
            speeds=np.sort(speeds)
            VL=speeds[:5].mean() #Choose the slowest 5 in front of the runner

            self.speedfunctions[sortedrunners[i],0]=\
                (1-p)*self.speedfunctions[sortedrunners[i],0]
            self.speedfunctions[sortedrunners[i],1]=\
                (1-p)*self.speedfunctions[sortedrunners[i],1]+p*VL

        starters=np.where(sortedpositions<0)
        for runner in starters[0]:
            self.speedfunctions[sortedrunners[runner],0]=0.0 #
            self.speedfunctions[sortedrunners[runner],1]=2.5 #


    def setinstantspeed(self,i,dt):
        self.instantspeed=(self.pos[:,i+1]-self.pos[:,i])/dt
        #print(self.instantspeed)




#############################


### Velocity Definition depending on slope ###
#@nb.jit
def V(positions,speedfunctions,track):
    #avgspeeds=avgspeeds/3.6 # Reducing to m/s
    #print(positions[:,i])
    #positions=np.where(positions>=track.length,track.length,positions)
    speeds=speedfunctions[:,0]*(track.cspline(positions,1))+speedfunctions[:,1]
    return speeds



@autorepr
class frunner():
    def __init__(self,time,wavedelay=0.0,wavecolor='b'):
        self.time=time
        self.wavedelay=wavedelay
        self.avgspeed=10000/(self.time*60)
        self.color=wavecolor
        self.slopefactor=np.random.uniform(-13.0,-3.0)
        self.poly1dspeed2=np.poly1d([self.slopefactor,self.avgspeed])
        self.name='f'+str(round(self.time,1))



    def init(self,nsteps,x0=0.0,sdelay=0.0):
        self.pos=np.zeros(nsteps)
        self.pos[0]=x0
        self.rank=None
        self.frontrunners=None
        self.frontrunnerswindow=None
'''
FRunner=[]
for time in TimeBins:
    for pack in RunnerDist:
    FRunner.append(frunner(time))
'''
