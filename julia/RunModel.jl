module RunModel
t=@elapsed begin
    include("Race.jl")
    using .Race
    # using .Tmp # we can use `using` to bring the exported symbols in `Tmp` into our namespace
    training()
    race()
end
println(">Elapsed time=", t)
end
