module Race
#export model

include("PreProcessing.jl")
using .PreProcessing

AvgTimes=PreProcessing.AvgTimes
WaveDelays=PreProcessing.WaveDelays
WaveInitSpeeds=PreProcessing.WaveInitSpeeds
InitPositions=PreProcessing.InitPositions
NinWaves=PreProcessing.NinWaves
SlopeFactors=PreProcessing.SlopeFactors
track= PreProcessing.track
parameters=PreProcessing.par
nrunners=parameters.nrunners


include("Frunnerclass.jl")
import .Frunnerclass
Frunner=Frunnerclass.Frunner
Runners=Frunnerclass.Runners


include("OdeSystemSolvers.jl")
import .OdeSystemSolvers
solver=OdeSystemSolvers.rk2_solver

 using JLD2


########################################### DEBUG IS REQUERID OS RANDOMS NOT WORKING A FUNCIONAR :/

function model()

    runnerslist=Array{Frunner,1}(undef, nrunners)
    for i in 1:nrunners
        runnerslist[i]=Frunner(AvgTimes[i],WaveDelays[i],WaveInitSpeeds[i],InitPositions[i],SlopeFactors[i])
    end
    allrunners=Runners(runnerslist)

    println(">control sizes:")
    println(">control sizes(allrunners.group)= ", size(allrunners.group))
    println(">control sizes(allrunners.pos)= ", size(allrunners.pos))
    println(">control sizes(allrunners.vels)= ", size(allrunners.vels))
    println(">control sizes(allrunners.rhos)= ", size(allrunners.rhos))
    println(">control: Pre-Processing done")
    println(">control: Starting Race Simulation")

    times, allrunners.pos, allrunners.vels, allrunners.rhos=solver(allrunners,parameters,track)
    println(">Control Race: Processing done")

    println(">Control Race: Writing to files with jld2")
    println(">Control Race: NinWaves", NinWaves)
    #save it


    save_object("./results/times.jld2", times)
    save_object("./results/allrunners.jld2",  allrunners)
    save_object("./results/parameters.jld2",parameters)
    save_object("./results/track.jld2",track)
    save_object("./results/ninwaves.jld2",NinWaves)

end


end
