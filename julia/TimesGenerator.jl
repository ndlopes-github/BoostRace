module TimesGenerator
export AvgTimes, NinWaves,InitPositions, WaveDelays,WaveInitSpeeds
using Distributions
using Random
using CubicSplines
using Plots
plotlyjs()

include("Settings.jl")
import .Settings
par=Settings.par
nsteps=par.observernsteps


include("Track.jl")
import .Track

track=Track.track


TimeBins=[i for i in 30:100]
println(TimeBins)

ReactionLineTime=0.4

RunnerDist=[15,18,20,17,18,18,31,40,45,72,96,88,109,131,155,192,
            207,270,281,263,326,298,268,240,309,296,346,313,323,347,
            286,325,281,274,291,252 ,285,220,220,207,213,180,172,145,140,
            151,112,145,96,85,85,87,85,73,42,47,27,39,45,31,28,29,24,21,15,21,14,17,14,12,12]

AcumulatedRelativeRunnerDist=cumsum(RunnerDist/sum(RunnerDist))
println("AcumulatedRelativeRunnerDis=",AcumulatedRelativeRunnerDist)

function inversepseudosigmoid( )
    ldist=Settings.par.ldist
    nrunners=Int(Settings.par.nrunners)
    nwaves=Settings.par.numberofwaves


    mixwaves=Int.(Settings.par.waves[:,1:nwaves])
    println("control: preprocessing times: waves:")
    println(mixwaves)
    println(size(mixwaves))

    wavedelays=Settings.par.waves[:,nwaves+1]
    waveinitspeeds=Settings.par.waves[:,nwaves+2]
    #println(wavedelays)
    #println(waveinitspeeds)

    partitions=zeros(size(mixwaves)[1]+1)
    for part in range(1,nwaves)
        partitions[part+1]=partitions[part]+sum(mixwaves[:,part])/nrunners
    end

    println("control: partitions")
    println(partitions)
    println("control: number of waves")
    println(nwaves)

    waves=zeros(nrunners)
    wb=1
    we=1

    for wave in range(1, nwaves)
        parts=zeros(sum(mixwaves[wave, 1 : nwaves]))
        pb=1
        pe=1
        for part in range(1, nwaves)
            size=mixwaves[wave,part]
            println(size)
            pe+=size
            wavepart=rand(Uniform(partitions[part],partitions[part+1]),size)
            println("control: uniform part begin= ", partitions[part], "end= ", partitions[part+1])
            parts[pb:pe-1]=wavepart
            pb=pe
        end
        we+=size(parts)[1]
        println(wb," ", we-1)
        #mix parts in each wave
        shuffle!(parts)
        waves[wb:we-1]=parts
        wb=we
    end

    RandDist=waves
    #println(RandDist)
    println(size(AcumulatedRelativeRunnerDist))
    println(size(TimeBins))

    AvgTimes=CubicSpline(AcumulatedRelativeRunnerDist,TimeBins,  extrapl=[1, ], extrapr=[1, ])[RandDist]
    println("Control: number of runners",size(AvgTimes))
    sort!(AvgTimes) # The Fastest are in the first Lines

    InitPositions=zeros(nrunners)
    WaveDelays=zeros(nrunners)
    WaveInitSpeeds=zeros(nrunners)




    # Position along the start line
    NinWaves=Int.(zeros(nwaves))
    for wave in range(1,nwaves)
        NinWaves[wave]=sum(mixwaves[wave, 1: nwaves])
    end


    itemcount=0
    for (nwave,nrunners) in enumerate(NinWaves)
        linecounter=0
        for i in range(1,nrunners)
            # To avoid truncations due to the cubic spline
            auxwidthcontrl=Int(floor(track.cspline2(-linecounter*ldist)+0.5))

            if (i+1)%auxwidthcontrl==0
                linecounter+=1
            end
            InitPositions[i+itemcount]=-linecounter*ldist#+0.30*np.random.random_sample()-0.15
            WaveDelays[i+itemcount]=wavedelays[nwave]+linecounter*ReactionLineTime
            WaveInitSpeeds[i+itemcount]=waveinitspeeds[nwave]
        end
        itemcount+=nrunners
    end

    return AvgTimes, NinWaves,InitPositions, WaveDelays,WaveInitSpeeds
end

AvgTimes, NinWaves,InitPositions, WaveDelays,WaveInitSpeeds= inversepseudosigmoid()

display(
plot(TimeBins,AcumulatedRelativeRunnerDist,
     title=" Acumulated Relative Runner Distribution", reuse=false)
)
display(
plot(AcumulatedRelativeRunnerDist,TimeBins,
     title="Inverse Acumulated Relative Runner Distribution", reuse=false)
)
#    plt.plot(acp,CubicSpline(acp,TimeBins)(acp),'r-',lw=0.5)
#    AvgTimes,RandDist,_,_=inversepseudosigmoid2(10000,10,0.5,[3333,3333,3334],[0,360,720])
#    plt.plot(RandDist, AvgTimes,'b+')
#    plt.show()
#    print(AvgTimes)


end
