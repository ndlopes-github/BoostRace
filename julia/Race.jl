module Race
export model

include("Settings.jl")
 import .Settings
par=Settings.par
nrunners=par.nrunners #Number of runners

include("OdeSystemSolvers.jl")
import .OdeSystemSolvers
rk4_solver=OdeSystemSolvers.rk4_solver

include("TimesGenerator.jl")
import .TimesGenerator
AvgTimes=TimesGenerator.AvgTimes
WaveDelays=TimesGenerator.WaveDelays
WaveInitSpeeds=TimesGenerator.WaveInitSpeeds
InitPositions=TimesGenerator.InitPositions

include("Frunnerclass.jl")
import .Frunnerclass
Frunner=Frunnerclass.Frunner
Runners=Frunnerclass.Runners

function model()

    runnerslist=Array{Frunner,1}(undef, nrunners)
    for i in 1:nrunners
        runnerslist[i]=Frunner(AvgTimes[i],WaveDelays[i],WaveInitSpeeds[i],InitPositions[i])
    end

    group=Runners(runnerslist)
    println(">control: Pre-Processing done")
    println(">control: Starting Race Simulation")

    times, positions,velocities,rhos=rk4_solver(
        group.avgspeeds,
        group.slopefactors,
        group.wavedelays,
        group.waveinitspeeds,
        par.trackdata,
        group.pos[:,1],
        par.observernsteps,
        par.observertimestep,
        par.timestep,
        par.linearfrontview,
        par.minratio,
        par.maxratio,
        par.minrho,
        par.maxrho
    )
    println(">control: Processing done")

end


end
