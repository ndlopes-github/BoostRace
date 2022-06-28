module Frunnerclass
export Runners, Frunner
using Distributions
using Random


include("Settings.jl")
import .Settings
par=Settings.par


struct Frunner
    time::Float32
    wavedelay::Float32
    waveinitspeed::Float32
    initposition::Float32
    avgspeed::Float32
    slopefactor::Float32
    #poly1dspeed
    # name
    pos::Vector{Float32}
    vels::Vector{Float32}
    rhos::Vector{Float32}
    # rank
    # frontrunners
    # frontrunnerswindow
end

avgspeed(time)=(10000.0/(time*60.0))
slopefactor=rand(Uniform(-13.0,-3.0))

function pos(initposition)
    aux=zeros(par.observernsteps)
    aux[1]=initposition
    return aux
end

vels=zeros(par.observernsteps)
rhos=zeros(par.observernsteps)

Frunner(time,wavedelay,waveinitspeed,initposition)=Frunner(time,wavedelay,waveinitspeed,initposition,
                                              avgspeed(time), slopefactor,pos(initposition),vels,rhos)


struct Runners
    group::Vector{Main.RunModelDone.Race.Frunnerclass.Frunner}
    pos::Vector{Vector{Float32}}
    vels::Vector{Vector{Float32}}
    rhos::Vector{Vector{Float32}}
    wavedelays::Vector{Float32}
    waveinitspeeds::Vector{Float32}
    avgspeeds::Vector{Float32}
    slopefactors::Vector{Float32}
    #     speedfunctions
    #     originalspeedfunctions
    #     size
    #     colors
    #     names
    #     instantspeed
end
positions(group)=[runner.pos for runner in group]
velocities(group)=[runner.vels for runner in group]
rhosall(group)=[runner.rhos for runner in group]
wavedelays(group)=[runner.wavedelay for runner in group]
waveinitspeeds(group)=[runner.waveinitspeed for runner in group]
avgspeeds(group)=[runner.avgspeed for runner in group]
slopefactors(group)=[runner.slopefactor for runner in group]

Runners(group)=Runners(group,positions(group),
                       velocities(group),rhosall(group), wavedelays(group),
                       waveinitspeeds(group),avgspeeds(group),slopefactors(group))


end
