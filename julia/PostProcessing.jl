module PostProcessing
using Plots
# To be available directly with "using .PostProcessing" (no prefix required)
# with import .PostProcessing prefix is necessary.
export times, allrunners,parameters, track, ninwaves, snapshot
#pyplot()
plotlyjs()
using JLD2
using Random
using Distributions
Random.seed!(1234)

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


function speedsvisuals(runnersidxs,allrunners,parameters,track)
    nrunners=allrunners.nrunners
    nsteps=parameters.observernsteps
    time=parameters.observertimestep*nsteps

    t=range(0,time,nsteps)

    plot(title="Speed Profile")
    xlabel!("Time (s)")
    ylabel!("Speed (m/s)")

    for runner in runnersidxs #range(group.size):
        plot!(t,allrunners.vels[runner,:],lw=0.5,label="")
    end
    plot!(size=(800,400))
    savefig("speeds_profile.pdf")
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
    savefig("Phases.pdf")
    gui()
end


function rhosvisuals(runnersidxs,allrunners)
    nrunners=allrunners.nrunners
    nsteps=parameters.observernsteps
    time=parameters.observertimestep*nsteps

    t=range(0,time,nsteps)

    plot(title="Rho Profile")
    xlabel!("Time (s)")
    ylabel!("Rho")

    for runner in runnersidxs #range(group.size):
        plot!(t,allrunners.rhos[runner,:],lw=0.5,label="")
    end
    plot!(size=(800,400))
    savefig("rhos.pdf")
    gui()
end

#=
function timesvisuals(times,times_free,allrunners,allrunnersfree,parameters)
    par=parameters
    nrunners=allrunners.nrunners
    starttimes=zeros(nrunners)
    endtimes=zeros(nrunners)

    #Wave departure times#
    #for wave in waves:
    #for runner in wave:
    #       pass




    for runner in range(group.size):
        tsidx=np.min(np.where(group.pos[runner,:]>0))
        teidx=np.min(np.where(group.pos[runner,:]>10000))
        starttimes[runner]=times[tsidx]
        endtimes[runner]=times[teidx]

    print('control: waves description: departures computation')
    print('control:********************************************')
    print(str(par.waves))
    print('control:********************************************')
    r0=0
    r1=np.sum(par.waves[0, :par.numberofwaves]).astype(int)
    wave_departure=np.max(starttimes[r0:r1])
    wave_time_gap_to_cross=np.max(starttimes[r0:r1])-np.min(starttimes[r0:r1])+1
    print('control: departures:  wave: ',0, ' departure:',  wave_departure)
    print('control: departures:  wave: ',0, ' time gap to cross:',  wave_time_gap_to_cross)

    wavestxt=repr(par.waves[0,:len(par.waves)])[6:-2]+', '+str(0.0)+','+str(par.waves[0,-1])+'],'
    acumulated_wave_time_gap_to_cross=wave_time_gap_to_cross
    for j in range(1,len(par.waves)):
        r0+=np.sum(par.waves[j-1, :par.numberofwaves]).astype(int)
        r1=r0+np.sum(par.waves[j, :par.numberofwaves]).astype(int)
        wave_departure=np.max(starttimes[r0:r1])
        wavestxt+='\n'+repr(par.waves[j,:len(par.waves)])[6:-2]+', '+str(acumulated_wave_time_gap_to_cross)+' +'\
                   +str(j)+' * gap ,'+str(par.waves[j,-1])+'],'

        wave_time_gap_to_cross=np.max(starttimes[r0:r1])-np.min(starttimes[r0:r1])+1
        acumulated_wave_time_gap_to_cross+=wave_time_gap_to_cross
        print('control: departures:  wave: ',j, ' departure:',  wave_departure)
        print('control: departures:  wave: ',j, ' time gap to cross:',  wave_time_gap_to_cross)

    print('control: suggested setting for waves after initial running for tune settings')
    print(wavestxt,sep=',')
    print('control:  end *************************************************************')

    runnertimes=endtimes-starttimes

    racetime=np.max(endtimes)
    slowrunners=np.argmax(endtimes)

    mintime=np.min(runnertimes)
    worsttime=np.max(runnertimes)
    winrunners=np.argmin(runnertimes)
    losrunners=np.argmax(runnertimes)

    starttimes_free=np.zeros(group_free.size)
    endtimes_free=np.zeros(group_free.size)

    for runner in range(group_free.size):
        tsidx=np.min(np.where(group_free.pos[runner,:]>0))
        teidx=np.min(np.where(group_free.pos[runner,:]>10000))
        starttimes_free[runner]=times[tsidx]
        endtimes_free[runner]=times[teidx]

    runnertimes_free=endtimes_free-starttimes_free



    plt.plot(runnertimes,'o',ms=0.5,label='Race')
    plt.plot(runnertimes_free,'o',ms=0.5,label='Alone')
    plt.ylabel("Time in seconds")
    plt.xlabel("Runner index")
    plt.legend()
    plt.savefig('./reports/personaltimings.png')
    plt.clf()

    errors=runnertimes-runnertimes_free
    print('control:debug:  # negative errors: ',len(*np.where(errors<0)))
    print('control:debug: negative errors: ',*zip(*np.where(errors<0), errors[np.where(errors<0)]))

    print('control: departure: runners  affected by the velocity rule at departure', len(*np.where(starttimes!=starttimes_free)))

    # print('free times',runnertimes_free[np.where(errors<0)])
    # print('times',runnertimes[np.where(errors<0)])
    # print('free start',starttimes_free[np.where(errors<0)])
    # print('start',starttimes[np.where(errors<0)])
    # print('free end',endtimes_free[np.where(errors<0)])
    # print('end',endtimes[np.where(errors<0)])


    t1=par.posweights[1,1]
    t2=par.posweights[2,1]
    t3=par.posweights[3,1]
    t4=par.posweights[4,1]

    w0=par.posweights[0,0]
    w1=par.posweights[1,0]
    w2=par.posweights[2,0]
    w3=par.posweights[3,0]
    w4=par.posweights[4,0]


    errorspen=np.zeros(len(errors))
    count_t1=0
    count_t2=0
    count_t3=0
    count_t4=0
    for idx,error in enumerate(errors):
        if error <= t1:
            errorspen[idx]=error*w1
            count_t1+=1
        elif t1 < error <= t2:
            errorspen[idx]=w1*t1+(error-t1)*w2
            count_t2+=1
        elif t2 < error <= t3 :
            errorspen[idx]=w1*t1+(t2-t1)*w2+(error-t2)*w3
            count_t3+=1
        else :
            errorspen[idx]=w1*t1+(t2-t1)*w2+(t3-t2)*w3+(error-t3)*w4
            count_t4+=1

    print('control: number of runners with time loss in [0,', t1,'] is', count_t1)
    print('control: number of runners with time loss in ]',t1,',', t2,'] is', count_t2)
    print('control: number of runners with time loss in ]',t2,',', t3,'] is', count_t3)
    print('control: number of runners with time loss >',t3, ' is', count_t4)

    errorspen+=starttimes*w0
    negerrors=np.where(errorspen<0)
    print('control: debug: warning: number of negative penalized errors:', len(negerrors[0]))
    print('control: debug: warning: runners with negative penalized errors:', *negerrors)

    print('control: waves description: errors computation for metric')
    print(par.waves)
    print('control: *************************************************')
    r0=0
    r1=0
    for j in range(1,len(par.waves)):
        r0+=np.sum(par.waves[j-1, :par.numberofwaves]).astype(int)
        r1=r0+np.sum(par.waves[j, :par.numberofwaves]).astype(int)
        errorspen[r0:r1]-=w0*par.waves[j,par.numberofwaves]
        print('control: wave ', j,' start: ',r0,'wave end: ',r1-1,', ',par.waves[j,par.numberofwaves])


    plt.plot(errors,'o',ms=0.5,label='Time lost')
    plt.plot(errorspen,'o',ms=0.5,label='Metric score')
    plt.ylabel('Time in seconds (total race time: '+str(int(racetime))+')')

    print('control: race time: ', racetime)
    print('control: slowest racer: ', slowrunners)

    print('control: best race time: ', mintime)
    print('control: winner: ', winrunners)

    print('control: worst race time: ', worsttime)
    print('control: last: ', losrunners)

    metricerror=np.sum(errorspen)/len(errorspen)
    print('control: metric error:', metricerror)
    l1error=np.linalg.norm(errors,ord=1)/len(errors)
    print('control: l1 error:', l1error)


    plt.xlabel('Runner index')
    plt.title('Averaged time lost ='+str(int(l1error))+\
              '\n Averaged metric score='+str(int(metricerror))+\
              ' departure times ='+str(par.waves[:,par.numberofwaves]))
    #plt.text(0,550,'l1 norm='+str(np.linalg.norm(errors,ord=1)))
    #plt.text(0,500,'metric ='+str(np.sum(errorspen)))
    plt.text(0,350,'waves ='+str(par.waves[:,0:par.numberofwaves]))
    #plt.text(0,400,'delays ='+str(par.waves[:,1]))
    #plt.text(0,350,'speeds_0 ='+str(par.waves[:,2]))
    plt.legend(loc=9 )
    plt.savefig('./reports/errors_report.png')
    plt.clf()

    logtex=open('./reports/simpletex.txt','a')
    print(datetime.datetime.now(), file=logtex)
    for x in par.waves:
        print('& $(',end='', file=logtex)
        for i in range(len(par.waves)):
            print('{:d}, '.format(int(x[i])), end='',file=logtex)
        i=len(par.waves)
        print('{:d}, '.format(int(x[i])), end='',file=logtex)
        i=len(par.waves)+1
        print('{:.2f} '.format(x[i]), end='',file=logtex)
        print(')$',file=logtex)

    text='''& ${l1error:.1f}$
& ${metricerror:.1f}$
& ${racetime:4d}$ \\\\'''.format(l1error=l1error,metricerror=metricerror,racetime=int(racetime))
    print(text+'\n\n',file=logtex)
end
=#

## Function calls

#race_visuals(times,allrunners,parameters,track)
times=load_object("./results/times.jld2")
allrunners=load_object("./results/allrunners.jld2")
parameters=load_object("./results/parameters.jld2")
track=load_object("./results/track.jld2")
ninwaves=load_object("./results/ninwaves.jld2")


snapshot(1000,allrunners,parameters,track,ninwaves)
runnersidxs=rand(1:allrunners.nrunners,30)
speedsvisuals(runnersidxs,allrunners,parameters,track)
phasevisuals(runnersidxs,allrunners)
rhosvisuals(runnersidxs,allrunners)

#timesvisuals(times=times,times_free=times_free,group=group,group_free=group_free)

end
