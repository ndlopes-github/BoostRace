module Race
export model

include("Settings.jl")
import .Settings

include("TimesGenerator.jl")
import .TimesGenerator

include("Frunnerclass.jl")
import .Frunnerclass

function model()
    # println(Settings.par.trackname)
    # println(TimesGenerator.AvgTimes,
    #         TimesGenerator.RandDist,
    #         TimesGenerator.NinWaves,
    #         TimesGenerator.InitPositions,
    #         TimesGenerator.WaveDelays,
    #         TimesGenerator.WaveInitSpeeds)


end


end
