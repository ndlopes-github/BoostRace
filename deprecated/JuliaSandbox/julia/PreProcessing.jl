module PreProcessing
export AvgTimes, WaveDelays, WaveInitSpeeds,InitPositions,NinWaves,SlopeFactors, track,parameters
using Random
using Distributions
using CubicSplines
using Plots
plotlyjs()
Random.seed!(1234)

include("Settings.jl")
import .Settings
parameters=Settings.par
println(">Control PreProcessing: dump(parameters)")
dump(parameters) # This prints the parameters in a human readable format.

include("Track.jl")
track=Track.track
println(">Control PreProcessing: dump(track)")
dump(track)

TimeBins=[i for i in 30:100]
println(">Control PreProcessing: TimeBins= ", TimeBins[1:5])

ReactionLineTime=0.4

RunnerDist=[15,18,20,17,18,18,31,40,45,72,96,88,109,131,155,192,
            207,270,281,263,326,298,268,240,309,296,346,313,323,347,
            286,325,281,274,291,252 ,285,220,220,207,213,180,172,145,140,
            151,112,145,96,85,85,87,85,73,42,47,27,39,45,31,28,29,24,21,15,21,14,17,14,12,12]

AcumulatedRelativeRunnerDist=cumsum(RunnerDist/sum(RunnerDist))
println(">Control PreProcessing: AcumulatedRelativeRunnerDis=", AcumulatedRelativeRunnerDist[1:5])

function inversepseudosigmoid( )
    par=parameters
    ldist=par.ldist
    nrunners=Int(par.nrunners)
    nwaves=par.numberofwaves
    mixwaves=Int.(par.waves[:,1:nwaves])

    println(">Control PreProcessing size(mixwaves) =", size(mixwaves))

    wavedelays=par.waves[:,nwaves+1]
    waveinitspeeds=par.waves[:,nwaves+2]

    partitions=zeros(Float32,size(mixwaves)[1]+1)
    for part in range(1,nwaves)
        partitions[part+1]=partitions[part]+sum(mixwaves[:,part])/nrunners
    end

    println(">Control PreProcessing: partitions ", partitions)
    println(">Control PreProcessing: number of waves",  nwaves)

    waves=zeros(Float32,nrunners)
    wb=1
    we=1

    for wave in range(1, nwaves)
        parts=zeros(Float32,sum(mixwaves[wave, 1 : nwaves]))
        pb=1
        pe=1
        for part in range(1, nwaves)
            size=mixwaves[wave,part]
            println(">Control PreProcessing: sizes of parts of mixwaves:",  size)
            pe+=size
            wavepart=rand(Uniform(partitions[part],partitions[part+1]),size)
            println(">Control PreProcessing: uniform part begin= ", partitions[part], " end= ", partitions[part+1])
            parts[pb:pe-1]=wavepart
            pb=pe
        end
        we+=size(parts)[1]
        println(">Control PreProcessing: uniform wb = ", wb," we-1 = ", we-1)
        #mix parts in each wave
        shuffle!(parts)
        waves[wb:we-1]=parts
        wb=we
    end

    RandDist=waves
    #println(RandDist)
    println(">Control PreProcessing: size(AcumulatedRelativeRunnerDist) = ", size(AcumulatedRelativeRunnerDist))
    println(">Control PreProcessing: size(TimeBins) = ", size(TimeBins))

    AvgTimes=CubicSpline(AcumulatedRelativeRunnerDist,TimeBins,  extrapl=[1, ], extrapr=[1, ])[RandDist]
    println(">Control PreProcessing:: number of runners =",size(AvgTimes))
    #sort!(AvgTimes) # The Fastest are in the first Lines

    InitPositions=zeros(Float32,nrunners)
    WaveDelays=zeros(Float32,nrunners)
    WaveInitSpeeds=zeros(Float32,nrunners)
    SlopeFactors=rand(Uniform(-13.0,-3.0),nrunners)

    # Position along the start line
    NinWaves=Int.(zeros(Float32,nwaves))
    for wave in range(1,nwaves)
        NinWaves[wave]=sum(mixwaves[wave, 1: nwaves])
    end


    itemcount=0
    for (nwave,nrunners) in enumerate(NinWaves)
        linecounter=0
        for i in range(1,nrunners)
            # To avoid truncations due to the cubic spline
            auxwidthcontrl=Int(floor(track.cspline_width(-linecounter*ldist)+0.5))

            if (i+1)%auxwidthcontrl==0
                linecounter+=1
            end
            InitPositions[i+itemcount]=-linecounter*ldist#+0.30*np.random.random_sample()-0.15
            WaveDelays[i+itemcount]=wavedelays[nwave]+linecounter*ReactionLineTime
            WaveInitSpeeds[i+itemcount]=waveinitspeeds[nwave]
        end
        itemcount+=nrunners
    end

    return AvgTimes, RandDist, NinWaves,InitPositions, WaveDelays,WaveInitSpeeds,SlopeFactors
end

AvgTimes, RandDist,NinWaves,InitPositions, WaveDelays,WaveInitSpeeds, SlopeFactors= inversepseudosigmoid()



if parameters.logplot==true
#=
    display(
        plot(TimeBins,AcumulatedRelativeRunnerDist,
             title=" Acumulated Relative Runner Distribution", reuse=false)
    )
    display(
        plot(AcumulatedRelativeRunnerDist,TimeBins,
             title="Inverse Acumulated Relative Runner Distribution", reuse=false)
    )
=#
    plot(AcumulatedRelativeRunnerDist,
         CubicSpline(AcumulatedRelativeRunnerDist,TimeBins,
                     extrapl=[1, ], extrapr=[1, ])[AcumulatedRelativeRunnerDist],
         linecolor = :red,lw=2)
    # sort()
    plot!(RandDist,sort(AvgTimes),seriestype = :scatter,
          title="Random Times Distribution",
          markersize=0.3,
          markeralpha = 0.4,
          markercolor = :blue )
    gui()
end

end
