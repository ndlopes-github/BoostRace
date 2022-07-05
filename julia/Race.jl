module Race
export race, training

# Expose: AvgTimes, WaveDelays, WaveInitSpeeds, InitPositions, NinWaves, SlopeFactors, track, parameters
include("PreProcessing.jl")
using .PreProcessing
nrunners=parameters.nrunners
dump(parameters) # This prints the parameters in a human readable format.

#Expose: Frunner, Runners
include("Frunnerclass.jl")
using .Frunnerclass

#Expose rk2_solver
include("OdeSystemSolvers.jl")
using .OdeSystemSolvers
solver=rk2


using JLD2


########################################### DEBUG IS REQUERID OS RANDOMS NOT WORKING A FUNCIONAR :/

function race()
    println(">control Race: model")
    runnerslist=Array{Frunner,1}(undef, nrunners)
    for i in 1:nrunners
        runnerslist[i]=Frunner(AvgTimes[i],WaveDelays[i],WaveInitSpeeds[i],InitPositions[i],SlopeFactors[i])
    end
    allrunners=Runners(runnerslist)

    println(">control Race: sizes(allrunners.group)= ", size(allrunners.group))
    println(">control Race: sizes(allrunners.pos)= ", size(allrunners.pos))
    println(">control Race: sizes(allrunners.vels)= ", size(allrunners.vels))
    println(">control Race: sizes(allrunners.rhos)= ", size(allrunners.rhos))
    println(">control Race: Pre-Processing done")
    println(">control Race: Starting Race Simulation")

    times, allrunners.pos, allrunners.vels, allrunners.rhos=solver(allrunners,parameters,track,false)
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

function training()
    training=true
    println(">control Training Race")
    runnerslist=Array{Frunner,1}(undef, nrunners)
    for i in 1:nrunners
        runnerslist[i]=Frunner(AvgTimes[i],WaveDelays[i],WaveInitSpeeds[i],InitPositions[i],SlopeFactors[i])
    end
    allrunners=Runners(runnerslist)

    println(">control Training Race: sizes:")
    println(">control Training Race: sizes(allrunners.group)= ", size(allrunners.group))
    println(">control Training Race: sizes(allrunners.pos)= ", size(allrunners.pos))
    println(">control Training Race: sizes(allrunners.vels)= ", size(allrunners.vels))
    println(">control Training Race: sizes(allrunners.rhos)= ", size(allrunners.rhos))
    println(">control Training Race: Pre-Processing done")
    println(">control Training Race: Starting Race Simulation")

    times, allrunners.pos, allrunners.vels, allrunners.rhos=solver(allrunners,parameters,track,training)
    println(">Control Training Race: Processing done")

    println(">Control Training Race: Writing to files with jld2")
    println(">Control Training Race: NinWaves", NinWaves)
    #save it


    save_object("./training_results/times.jld2", times)
    save_object("./training_results/allrunners.jld2",  allrunners)
    save_object("./training_results/parameters.jld2",parameters)
    save_object("./training_results/track.jld2",track)
    save_object("./training_results/ninwaves.jld2",NinWaves)

end


end
