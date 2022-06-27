module Race
export model

include("Settings.jl")
import .Settings

include("TimesGenerator.jl")
import .TimesGenerator


function model()
    println(Settings.par)
    #println(TimesGenerator.inversepseudosigmoid())
end

# your other definitions here

end
