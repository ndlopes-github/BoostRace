module PostProcessing
using Plots
#pyplot()
plotlyjs()
using JLD2
using Random
using Distributions
Random.seed!(1234)

times=load_object("./results/times.jld2")
allrunners=load_object("./results/allrunners.jld2")
parameters=load_object("./results/parameters.jld2")
track=load_object("./results/track.jld2")
ninwaves=load_object("./results/ninwaves.jld2")

function snapshot(step,allrunners,parameters,track,ninwaves)
    nrunners=allrunners.nrunners
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    ys=track.cspline_elev(xs)
    ws=track.cspline_width(xs)
    yws=ys .+ ws

    X=allrunners.pos[:, step]
    YWS=zeros(nrunners)
    for r in range(1,nrunners)
        YWS[r]=rand(Uniform(0,1))*track.cspline_width(X[r])+track.cspline_elev(X[r])
    end

    plot(xs, ys,title="Race Snapshot",label="Elevation")
    xlabel!("Track length in (m)")
    plot!(xs,yws,label="Width")
    plot!(X,YWS,seriestype = :scatter,
          markersize=0.2,
          markeralpha = 1.0,
          markerstrokecolor =:blue, label="Positions")

    gui()
end


function race_visuals(times,allrunners,parameters,track)
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    ys=track.cspline_elev(xs)
    ws=track.cspline_width(xs)
    yws=ys .+ ws

    plot(xs, ys,reuse=false)
    plot!(xs,yws)
    gui()

end

#race_visuals(times,allrunners,parameters,track)
snapshot(2500,allrunners,parameters,track,ninwaves)

end
