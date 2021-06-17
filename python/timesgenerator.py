# coding: utf-8

import numpy as np
from scipy.interpolate import CubicSpline
from settings import parameters

np.random.seed(993869)

par=parameters()
nsteps=par.observernsteps


######### Histogram data
TimeBins=np.arange(start=30, stop=101, step=1)
ReactionLineTime=0.4

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



def inversepseudosigmoid( ):
    ldist=par.ldist
    nrunners=par.nrunners
    nwaves=par.numberofwaves
    mixwaves=par.waves[:,0:nwaves].astype(int) # TO REMOVE


    print('control: preprocessing times: waves:', mixwaves)

    wavedelays=par.waves[:,nwaves]
    waveinitspeeds=par.waves[:,1+nwaves]

    numberofwaves=len(mixwaves)
    numberofparts=numberofwaves


    partitions=np.zeros(len(mixwaves)+1)
    for part in range(numberofwaves):
        partitions[part+1]=partitions[part]+np.sum(mixwaves[:,part])/nrunners



    print('control: partitions', partitions)
    print('control: number of waves', numberofwaves)
    waves=np.zeros(nrunners)

    wb=0
    we=0
    for wave in range(numberofwaves):
        parts=np.zeros(np.sum(mixwaves[wave,:numberofwaves]))
        pb=0
        pe=0
        for part in range(numberofparts):
            size=mixwaves[wave,part]
            pe+=size
            ##     wavepart=np.random.uniform(pb/nrunners,pe/nrunners,
            ##                               size=(size,))
            ##            wavepart=np.random.uniform(part/numberofparts,(part+1)/numberofparts,
            ##                                  size=(size,))
            wavepart=np.random.uniform(partitions[part],partitions[part+1],size=(size,))
            #            print('control: uniform part begin=', pb/nrunners, 'end=', pe/nrunners)
            print('control: uniform part begin=', partitions[part], 'end=', partitions[part+1])
            parts[pb:pe]=wavepart[:]
            pb=pe
        we+=len(parts)
        print(wb,we)
        assert len(waves[wb:we])==len(parts), ' error '+ str(part)+'  '+str(wave)+' '+str(len(waves[wb:we]))+' '+str(len(parts))
        #mix parts in each wave
        parts=np.random.permutation(parts)
        waves[wb:we]=parts[:]
        wb=we


    RandDist=waves

    AvgTimes=CubicSpline(AcumulatedRelativeRunnerDist,TimeBins)(RandDist)
    print('Control: number of runners',len(AvgTimes))



    #AvgTimes=np.sort(AvgTimes) # The Fastest are in the first Lines

    InitPositions=np.zeros(nrunners)
    WaveDelays=np.zeros(nrunners)
    WaveInitSpeeds=np.zeros(nrunners)
    wavedelays=np.array(wavedelays)



    # Position along the start line
    NinWaves=np.zeros(numberofwaves).astype(int)
    for wave in range(numberofwaves):
        NinWaves[wave]=np.sum(mixwaves[wave,:numberofwaves])


    itemcount=0
    for nwave,nrunners in enumerate(NinWaves):
        linecounter=0
        for i in range(nrunners):
            if (i+1)%int(par.track.cspline2(-linecounter*ldist))==0:
                linecounter+=1
            InitPositions[i+itemcount]=-linecounter*ldist#+0.30*np.random.random_sample()-0.15
            WaveDelays[i+itemcount]=wavedelays[nwave]+linecounter*ReactionLineTime
            WaveInitSpeeds[i+itemcount]=waveinitspeeds[nwave]
        itemcount+=nrunners

    return AvgTimes, NinWaves,InitPositions, WaveDelays,WaveInitSpeeds




if __name__== '__main__':
    import matplotlib.pyplot as plt
    acp=AcumulatedRelativeRunnerDist
    plt.plot(TimeBins,acp)
    plt.show()
    plt.clf()
    plt.plot(acp,TimeBins,'ko',ms=2.)
    plt.plot(acp,CubicSpline(acp,TimeBins)(acp),'r-',lw=0.5)
    AvgTimes,RandDist,_,_=inversepseudosigmoid2(10000,10,0.5,[3333,3333,3334],[0,360,720])
    plt.plot(RandDist, AvgTimes,'b+')
    plt.show()
    print(AvgTimes)
