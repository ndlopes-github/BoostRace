module Race
export model

include("Settings.jl")
import .Settings

include("TimesGenerator.jl")
import .TimesGenerator


function model()
    println(Settings.par)
    println(TimesGenerator.AvgTimes,TimesGenerator.NinWaves,
            TimesGenerator.InitPositions,TimesGenerator.WaveDelays,
            TimesGenerator.WaveInitSpeeds)
end


end
