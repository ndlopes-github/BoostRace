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
    time=step*parameters.observertimestep
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    ys=track.cspline_elev(xs)
    ws=track.cspline_width(xs)
    yws=ys .+ ws

    X=allrunners.pos[:, step]
    YWS=zeros(nrunners)
    for r in range(1,nrunners)
        YWS[r]=rand(Uniform(0,1))*track.cspline_width(X[r])+track.cspline_elev(X[r])
    end


    colors=["orange","cyan","green","purple","brown","pink","gray","azure","olive","blue"]
    nwaves=size(ninwaves)[1]


    plot(xs, ys,title="Race Snapshot t=$time (s)",label="Elevation")
    xlabel!("Track length (m)")
    ylabel!("Track elevation (m)")
    plot!(xs,yws,label="Width")
    wb=1
    we=0
    n=0
    for (color,counter) in zip(colors[1:nwaves],ninwaves)
        n+=1
        we+=counter
        plot!(X[wb:we],YWS[wb:we],seriestype = :scatter,
              markersize=0.3,
              markeralpha = 1.0,
              markerstrokecolor =color,
              label="wave $n")
        wb=we+1
    end
    plot!(size=(800,400))
    savefig("snapshot$time.pdf")
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
snapshot(1000,allrunners,parameters,track,ninwaves)

#=
function speedsvisuals(rstep,allrunners,parameters,track,ninwaves):
    nrunners=allrunners.nrunners
    time=step*parameters.observertimestep
    nsteps=parameters.nobservertimesteps

    t=range(0, nsteps, nsteps+1)
    ax = plt.axes(xlim=(0, 6000),
                  ylim=(group.vels[:,:].min(),
                        group.vels[:,:].max()))

    plt.xlabel('Time',fontsize=20)
    plt.ylabel('Speeds (m/s)',fontsize=20)

    for runner in runnerslist: #range(group.size):
        plt.plot(t,group.vels[runner,:],lw=0.5,label=str(runner))

    if len(runnerslist)<11:
        plt.legend()
    plt.show()
=#


end
