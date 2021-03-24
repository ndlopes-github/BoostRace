# coding: utf-8

import numpy as np
from scipy.interpolate import CubicSpline
np.random.seed(993869)

######### Histogram data
TimeBins=np.arange(start=30, stop=101, step=1)

RunnerDist=np.array([15,18,20,17,18,18,31,40,45,72,96,88,109,131,155,192,207,270,281,263,326,298,268,240,309,296,346,
                     313,323,347,286,325,281,274,291,252,285,220,220,207,213,180,172,145,140,151,112,145,96,85,85,87,85,73,42,47,
                     27,39,45,31,28,29,24,21,15,21,14,17,14,12,12])
'''
RunnerDist=np.array([5,8,10,12,13,18,31,40,45,72,96,88,109,131,155,
          194,209,270,283,265,328,298,268,240,309,296,346,313,
            323,347,286,325,281,274,291,252,285,220,220,207,213,
            180,172,145,140,151,112,145,96,85,85,87,85,73,42,47,
            27,39,45,31,28,29,24,21,20,24,18,21,17,15,20])
'''

#HistGroup=np.array(list(zip(TimeBins,RunnerDist)))

AcumulatedRelativeRunnerDist=np.cumsum(RunnerDist/np.sum(RunnerDist))

def inversepseudosigmoid(number,lnumber,ldist,ninwaves,wavedelays):
    RandDist=np.random.uniform(0.,1.0,size=(number,))
    AvgTimes=CubicSpline(AcumulatedRelativeRunnerDist,TimeBins)(RandDist)
    AvgTimes=np.sort(AvgTimes) # The Fastest are in the first Lines
    InitPositions=np.zeros(number)
    WaveDelays=np.zeros(number)
    ninwaves=np.array(ninwaves)
    wavedelays=np.array(wavedelays)

    assert len(wavedelays)==len(ninwaves),'wave delays and number of waves do not match'
    assert number==ninwaves.sum(),'number of runners in waves do not match'
    nwaves=len(wavedelays)
    assert number==ninwaves.sum(), 'Sum of Waves not matching number of runners'
    itemcount=0
    for nwave,nrunners in enumerate(ninwaves):
        linecounter=0
        for i in range(nrunners):
            if (i+1)%lnumber==0:
                linecounter+=1
            InitPositions[i+itemcount]=-linecounter*ldist
            WaveDelays[i+itemcount]=wavedelays[nwave]
        itemcount+=nrunners

    return AvgTimes, RandDist,InitPositions, WaveDelays



if __name__== '__main__':
    import matplotlib.pyplot as plt
    acp=AcumulatedRelativeRunnerDist
    plt.plot(TimeBins,acp)
    plt.show()
    plt.clf()
    plt.plot(acp,TimeBins,'ko',ms=2.)
    plt.plot(acp,CubicSpline(acp,TimeBins)(acp),'r-',lw=0.5)
    AvgTimes,RandDist,_,_=inversepseudosigmoid(1000,10,0.5,[200,400,400],[0,360,720])
    plt.plot(RandDist, AvgTimes,'b+')
    plt.show()
    print(AvgTimes)
