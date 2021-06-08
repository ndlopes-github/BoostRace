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

def inversepseudosigmoid(number,lnumber,ldist,ninwaves,wavedelays):

    RandDist=np.random.uniform(0,1,size=(number,))
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

    #Generate soft mixture of the runners thru waves


    itemcount=0
    for nwave,nrunners in enumerate(ninwaves):
        linecounter=0
        for i in range(nrunners):
            if (i+1)%lnumber==0:
                linecounter+=1
            InitPositions[i+itemcount]=-linecounter*ldist
            WaveDelays[i+itemcount]=wavedelays[nwave]+linecounter*ReactionLineTime
        itemcount+=nrunners

    return AvgTimes, RandDist,InitPositions, WaveDelays




def inversepseudosigmoid2(number,lnumber,ldist,ninwaves,wavedelays,waveinitspeeds):
    assert len(ninwaves)==3, 'Wrong function'
    # w1=[0.8,0.05,0.15]
    # w2=[0.15,0.1,0.75]
    # w3=[0.15,0.1,0.75]


    RD1=np.random.uniform(0,1./3.,size=(int(80*ninwaves[0]/100+0.5),))
    RD2=np.random.uniform(1./3.,2./3,size=(int(5*ninwaves[0]/100+0.5),))
    RD3=np.random.uniform(2./3.,1,size=(int(15*ninwaves[0]/100+0.5),))

    RD4=np.random.uniform(0,1./3.,size=(int(5*ninwaves[1]/100+0.5),))
    RD5=np.random.uniform(1./3.,2./3,size=(int(80*ninwaves[1]/100+0.5),))
    RD6=np.random.uniform(2./3.,1,size=(int(15*ninwaves[1]/100+0.5),))

    RD7=np.random.uniform(0,1./3.,size=(int(15*ninwaves[2]/100+0.5),))
    RD8=np.random.uniform(1./3.,2./3,size=(int(10*ninwaves[2]/100+0.5),))
    RD9=np.random.uniform(2./3.,1,size=(int(75*ninwaves[2]/100+0.5),))


    W1=np.concatenate((RD1,RD2,RD3),axis=None)
    W1=np.random.permutation(W1)
    W2=np.concatenate((RD4,RD5,RD6),axis=None)
    W2=np.random.permutation(W2)
    W3=np.concatenate((RD7,RD8,RD9),axis=None)
    W3=np.random.permutation(W3)

    RandDist=np.concatenate((W1,W2,W3),axis=None)

    AvgTimes=CubicSpline(AcumulatedRelativeRunnerDist,TimeBins)(RandDist)
    print('Control: number of runners',len(AvgTimes))



    #AvgTimes=np.sort(AvgTimes) # The Fastest are in the first Lines

    InitPositions=np.zeros(number)
    WaveDelays=np.zeros(number)
    WaveInitSpeeds=np.zeros(number)
    ninwaves=np.array(ninwaves)
    wavedelays=np.array(wavedelays)

    assert len(W1) == ninwaves[0] and len(W2) == ninwaves[1] and len(W3) == ninwaves[2] , '\n wrong division for wave 1:'+str(ninwaves[0])+'!='+str( len(W1))+ '\n wrong division for wave 2:'+str(ninwaves[1])+'!='+str( len(W2))+'\nwrong division for wave 3:'+str(ninwaves[2])+'!='+str( len(W3))

    assert len(wavedelays)==len(ninwaves),'wave delays and number of waves do not match'

    assert len(waveinitspeeds)==len(ninwaves),'wave speeds and number of waves do not match'

    assert number==ninwaves.sum(),'number of runners in waves do not match'
    nwaves=len(wavedelays)
    assert number==ninwaves.sum(), 'Sum of Waves not matching number of runners'

    #Generate soft mixture of the runners thru waves


    itemcount=0
    for nwave,nrunners in enumerate(ninwaves):
        linecounter=0
        for i in range(nrunners):
            if (i+1)%lnumber==0:
                linecounter+=1
            InitPositions[i+itemcount]=-linecounter*ldist#+0.30*np.random.random_sample()-0.15
            WaveDelays[i+itemcount]=wavedelays[nwave]+linecounter*ReactionLineTime
            WaveInitSpeeds[i+itemcount]=waveinitspeeds[nwave]
        itemcount+=nrunners

    return AvgTimes, RandDist,InitPositions, WaveDelays,WaveInitSpeeds





def inversepseudosigmoid3( ):
    ldist=par.ldist
    number=par.nrunners
    nwaves=par.numberofwaves
    mixwaves=par.waves[:,0:nwaves].astype(int) # TO REMOVE
    print('control: preprocessing times: waves:', mixwaves)
    wavedelays=par.waves[:,nwaves]
    waveinitspeeds=par.waves[:,1+nwaves]

    numberofwaves=len(mixwaves)
    numberofparts=numberofwaves
    print('control: number of waves', numberofwaves)
    waves=np.zeros(number)

    wb=0
    we=0
    for wave in range(numberofwaves):
        parts=np.zeros(np.sum(mixwaves[wave,:numberofwaves]))
        pb=0
        pe=0
        for part in range(numberofparts):
            size=mixwaves[wave,part]
            pe+=size
            wavepart=np.random.uniform(part/numberofparts,(part+1)/numberofparts,
                                       size=(size,))

            parts[pb:pe]=wavepart[:]
            pb=pe
        we+=len(parts)
        print(wb,we)
        assert len(waves[wb:we])==len(parts), ' error '+ str(part)+'  '+str(wave)+' '+str(len(waves[wb:we]))+' '+str(len(parts))
        waves[wb:we]=parts[:]
        wb=we


    RandDist=waves

    AvgTimes=CubicSpline(AcumulatedRelativeRunnerDist,TimeBins)(RandDist)
    print('Control: number of runners',len(AvgTimes))



    #AvgTimes=np.sort(AvgTimes) # The Fastest are in the first Lines

    InitPositions=np.zeros(number)
    WaveDelays=np.zeros(number)
    WaveInitSpeeds=np.zeros(number)
    #mixwaves=np.array(mixwaves)
    wavedelays=np.array(wavedelays)


    #Generate soft mixture of the runners thru waves

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
