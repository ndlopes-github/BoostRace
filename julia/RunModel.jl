module RunModelDone
    include("Race.jl")
    import .Race
   # using .Tmp # we can use `using` to bring the exported symbols in `Tmp` into our namespace

Race.model()
end
