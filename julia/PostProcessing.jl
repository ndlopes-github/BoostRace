module PostProcessing
using Plots
# To be available directly with "using .PostProcessing" (no prefix required)
# with import .PostProcessing prefix is necessary.
export times, allrunners,parameters, track, ninwaves, runnersidx
export snapshot,speedsvisuals,phasevisuals,rhosvisuals#,timesvisuals
#pyplot()
plotlyjs()
using JLD2
using Random
using Distributions
using LinearAlgebra
using Dates
using DelimitedFiles
Random.seed!(1234)


function snapshot(steps,allrunners,parameters,track,ninwaves)
    nrunners=allrunners.nrunners
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    ys=track.cspline_elev(xs)
    ws=track.cspline_width(xs)
    yws=ys .+ ws

    println(length(steps))
    for step in steps
        time=Int(step*parameters.observertimestep)
        X=allrunners.pos[:, step]
        YWS=zeros(nrunners)
        for r in 1:nrunners
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
        tm=lpad(time,4,"0")
        savefig("./reports/pngs/snapshot$tm.png")
    end
    #gui()
end


function histsnapshot(steps,allrunners,parameters)
    for step in steps
        bins=0:round(Int,parameters.frontviewdistance):round(Int,parameters.racedistance)
        histogram(allrunners.pos[:,step],bins=bins,label=false)
        xlabel!("Road (m)")
        ylabel!("Runners per 4 (m)")
        tm=lpad(time,4,"0")
        savefig("./reports/pngs/hist$tm.png")
    end
end


function speedsvisuals(runnersidxs,allrunners,parameters,track)
    nrunners=allrunners.nrunners
    nsteps=parameters.observernsteps
    time=parameters.observertimestep*nsteps

    t=range(start=0.0,stop=time,length=nsteps)

    plot(title="Speed Profile")
    xlabel!("Time (s)")
    ylabel!("Speed (m/s)")

    for runner in runnersidxs #range(group.size):
        plot!(t,allrunners.vels[runner,:],lw=0.5,label=false)
    end
    plot!(size=(800,400))
    savefig("./reports/pdfs/speeds_profile.pdf")
    gui()
end


function phasevisuals(runnersidxs,allrunners)

    plot(title="Phase Profile")
    xlabel!("Position (m)")
    ylabel!("Speed (m/s)")

    for runner in runnersidxs #range(group.size):
        plot!(allrunners.pos[runner,:],allrunners.vels[runner,:],lw=0.5,label="")
    end
    plot!(size=(800,400))
    savefig("./reports/pdfs/Phases.pdf")
    gui()
end


function rhosvisuals(runnersidxs,allrunners)
    nrunners=allrunners.nrunners
    nsteps=parameters.observernsteps
    time=parameters.observertimestep*nsteps

    t=range(start=0.0,stop=time,length=nsteps)

    plot(title="Rho Profile")
    xlabel!("Time (s)")
    ylabel!("Rho")

    for runner in runnersidxs #range(group.size):
        plot!(t,allrunners.rhos[runner,:],lw=0.5,label="")
    end
    plot!(size=(800,400))
    savefig("./reports/pdfs/rhos.pdf")
    gui()
end



function timesvisuals(times,allrunners,allrunners_training,parameters)
    par=parameters
    nrunners=allrunners.nrunners
    starttimes=zeros(nrunners)
    endtimes=zeros(nrunners)

    for runner in 1:nrunners
        tsidx=findfirst(x->(x>0.0), allrunners.pos[runner,:])
        teidx=findfirst(x->(x>=par.racedistance),allrunners.pos[runner,:])
        starttimes[runner]=times[tsidx]
        endtimes[runner]=times[teidx]
        #println(runner, ">>>>>>>>>>> ", teidx)
    end

    println(">control Post-Processing: par.waves")
    println(display(par.waves))
    r0=1
    r1=sum(Int,par.waves[1, 1:par.numberofwaves])
    wave_departure=maximum(starttimes[r0:r1])
    wave_time_gap_to_cross=maximum(starttimes[r0:r1])-minimum(starttimes[r0:r1])+1
    println(">control Post-Processing: departures computation")
    println(">control Post-Processing: departures: wave: ",1, " departure:",  wave_departure)
    println(">control Post-Processing: departures: wave: ",1, " time gap to cross:",  wave_time_gap_to_cross)

    wavetxt=" ["*string(par.waves[1,1:size(par.waves)[1]])[9: end-1]*" ,0.0 ,"*string(par.waves[1,end])*"]"
    acumulated_wave_time_gap_to_cross=wave_time_gap_to_cross


    for j in range(2,size(par.waves)[1])
        r0+=sum(Int,par.waves[j-1, 1: par.numberofwaves])
        r1=r0+sum(Int,par.waves[j,1: par.numberofwaves])-1
        wave_departure=maximum(starttimes[r0:r1])
        wavetxt*="\n ["*string(par.waves[j,1:size(par.waves)[1]])[9:end-1]*","*string(acumulated_wave_time_gap_to_cross)*
        " + "*string(j-1)*"*gap ,"*string(par.waves[j,end])*"]"
        wave_time_gap_to_cross=maximum(starttimes[r0:r1])-minimum(starttimes[r0:r1])+1
        acumulated_wave_time_gap_to_cross+=wave_time_gap_to_cross
        println(">control Post-Processing: departures: wave: ",j, " departure:",  wave_departure)
        println(">control Post-Processing: departures: wave: ",j, " time gap to cross: ",  wave_time_gap_to_cross)
    end

    println(">control Post-Processing: suggested setting for waves after initial running for tune settings")
    println(">control Post-Processing: start********************************************************")
    println(wavetxt)
    println(">control Post-Processing: stop*********************************************************")


    runnertimes=endtimes-starttimes
    racetime=maximum(endtimes)
    slowrunners=argmax(endtimes)
    mintime=minimum(runnertimes)
    worsttime=maximum(runnertimes)
    winrunners=argmin(runnertimes)
    losrunners=argmax(runnertimes)

    starttimes_training=zeros(nrunners)
    endtimes_training=zeros(nrunners)


    for runner in 1:nrunners
        tsidx=findfirst(x->(x>0.0), allrunners_training.pos[runner,:])
        teidx=findfirst(x->(x>=par.racedistance),allrunners_training.pos[runner,:])
        starttimes_training[runner]=times[tsidx]
        endtimes_training[runner]=times[teidx]
    end

    runnertimes_training=endtimes_training-starttimes_training


    plot(1:nrunners,runnertimes,ms=0.8,label="Race",seriestype = :scatter,
         #markersize=0.5,
        # markeralpha = .5,
         markerstrokecolor = "orange",
         reuse=false)
    plot!(1:nrunners,runnertimes_training,ms=0.8,label="Training",seriestype = :scatter,
          #markersize=0.5,
         # markeralpha = 0.5,
         markerstrokecolor ="blue")
    ylabel!("Time in seconds")
    xlabel!("Runner index")
    gui()
    savefig("./reports/pngs/personaltimings.png")

    errors=runnertimes-runnertimes_training
    println(">control Post-Processing: debug:  length of  negative errors: ",length(findall(x->(x<0.0),errors)))
    println(">control Post-Processing: debug: negative errors: ",errors[findall(x->(x<0.0),errors)])
    println(">control Post-Processing: debug: args negative errors: ",findall(x->(x<0.0),errors))
    println(">control Post-Processing: departure: runners  affected by the velocity rule at departure ",
          length(findall(x->(x!=0.0),starttimes-starttimes_training)))

    #println("training times',runnertimes_free[np.where(errors<0)])
    # print('times',runnertimes[np.where(errors<0)])
    # print('free start',starttimes_free[np.where(errors<0)])
    # print('start',starttimes[np.where(errors<0)])
    # print('free end',endtimes_free[np.where(errors<0)])
    # print('end',endtimes[np.where(errors<0)])

    println(">control Post-Processing: par.posweights")
    println(display(par.posweights))


    t1=par.posweights[2,2]
    t2=par.posweights[3,2]
    t3=par.posweights[4,2]
    t4=par.posweights[5,2]

    w0=par.posweights[1,1]
    w1=par.posweights[2,1]
    w2=par.posweights[3,1]
    w3=par.posweights[4,1]
    w4=par.posweights[5,1]


    errorspen=zeros(length(errors))
    count_t1=0
    count_t2=0
    count_t3=0
    count_t4=0

    for (idx,error) in enumerate(errors)
        if error <= t1
            errorspen[idx]=error*w1
            count_t1+=1
        elseif t1 < error <= t2
            errorspen[idx]=w1*t1+(error-t1)*w2
            count_t2+=1
        elseif t2 < error <= t3
            errorspen[idx]=w1*t1+(t2-t1)*w2+(error-t2)*w3
            count_t3+=1
        else
            errorspen[idx]=w1*t1+(t2-t1)*w2+(t3-t2)*w3+(error-t3)*w4
            count_t4+=1
        end
    end
    println(">control Post-Processing: number of runners with time loss in [0,", t1,"] is ", count_t1)
    println(">control Post-Processing: number of runners with time loss in ]",t1,",", t2,"] is ", count_t2)
    println(">control Post-Processing: number of runners with time loss in ]",t2,",", t3,"] is ", count_t3)
    println(">control Post-Processing: number of runners with time loss > ",t3, " is ", count_t4)

    errorspen .+= w0 .* starttimes
    negerrors=findall(x->(x<0.0),errorspen)
    println(">control Post-Processing: debug: warning: number of negative penalized errors:", length(negerrors))
    println(">control Post-Processing: debug: warning: runners with negative penalized errors:", negerrors)

    println(">control Post-Processing: waves description: errors computation for metric")
    r0=1
    r1=1
     for j in range(2,size(par.waves)[1])
         r0+=sum(Int,par.waves[j-1, 1:par.numberofwaves])
         r1=r0+sum(Int,par.waves[j, 1:par.numberofwaves])
         errorspen[r0:r1-1].-= w0.*par.waves[j,par.numberofwaves+1]
         println(">control Post-Processing:  wave ",
                 j-1, "start: ",r0," wave end: ",r1-1,", ",par.waves[j,par.numberofwaves+1])
     end


    println(">control Post-Processing: race time: ", racetime)
    println(">control Post-Processing: slowest racer: ", slowrunners)

    println(">control Post-Processing: best race time: ", mintime)
    println(">control Post-Processing: winner: ", winrunners)

    println(">control Post-Processing: worst race time: ", worsttime)
    println(">control Post-Processing: last: ", losrunners)

    metricerror=sum(errorspen)/length(errorspen)
    println(">control Post-Processing: metric error: ", metricerror)
    l1error=norm(errors,1)/length(errors)
    println(">control Post-Processing:  l1 error: ", l1error)


    plot(1:nrunners,errors,ms=0.5,label="Time lost",seriestype = :scatter, markerstrokecolor = "orange",
         title="Averaged time and metric losses = "*
         string(round(Int,l1error))*", "
         *string(round(Int,metricerror)))
    plot!(1:nrunners,errorspen,ms=0.5,label="Metric score",seriestype = :scatter, markerstrokecolor = "blue",)
    ylabel!("Time in seconds (total race time: "*string(ceil(Int,racetime))*")")
    xlabel!("Runner index")
    savefig("./reports/pngs/errors_report.png")
    gui()

    outfile = "./reports/simpletex.txt"
    open(outfile, "a") do f
        println(f,"start*************")
        println(f,now())
        println(f,"")
        writedlm(f,par.waves)
        println(f,"")
        println(f,l1error)
        println(f,metricerror)
        println(f,racetime)
        println(f,"stop*************")
    end
end


## Function calls

#race_visuals(times,allrunners,parameters,track)
function load_objects()
    times=load_object("./results/times.jld2")
    allrunners=load_object("./results/allrunners.jld2")
    allrunners_training=load_object("./training_results/allrunners.jld2")
    parameters=load_object("./results/parameters.jld2")
    track=load_object("./results/track.jld2")
    ninwaves=load_object("./results/ninwaves.jld2")
    return times, allrunners, allrunners_training,parameters, track, ninwaves
end


times, allrunners, allrunners_training,parameters, track, ninwaves=load_objects()
#snapshot(1:30:7001,allrunners,parameters,track,ninwaves)  #requires include("Track.jl")
histsnapshot(2000,allrunners,parameters)
# runnersidxs=rand(1:allrunners.nrunners,30)
# speedsvisuals(runnersidxs,allrunners,parameters,track)
# phasevisuals(runnersidxs,allrunners)
# rhosvisuals(runnersidxs,allrunners)


#timesvisuals(times,allrunners,allrunners_training,parameters)
# times=Nothing
#allrunners=Nothing
#allrunners_training=Nothing
#parameters=Nothing
#track=Nothing
#ninwaves=Nothing
#GC.gc()
end


# convert png series to gif
# convert -delay 2 -loop 0 *.png -scale 480x270 sheban.gif
# convert png series to mp4
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 output.mp4
