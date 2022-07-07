module OdeSystemSolvers
export rk2

using ProgressBars
using CubicSplines





function Rho(t,X,V, allrunners,par,track,training)


    return R
    end

# Index r for runner
# Index i for time stepping

# Velocity function dx/dt=F(...)
function F(t,X,V, allrunners,par,track,training)
    ## Some alias to simplify
    spline=track.cspline_elev
    nrunners=allrunners.nrunners
    minrho=par.minrho
    maxrho=par.maxrho
    minratio=par.minratio
    maxratio=par.maxratio
    fvdist=par.frontviewdistance
    VL=zeros(nrunners)
    racedistance=par.racedistance
    epsm=100
    R=zeros(nrunners)

    if training==true
        # Race for timing reports
        for r in 1:nrunners
            # Stop epsm=100m after the finishing line
            if (t <= allrunners.wavedelays[r]) || (X[r]>=racedistance+epsm)
                V[r]=0.0
            else
                V[r]=(allrunners.avgspeeds[r] + gradient(spline,X[r],1)*allrunners.slopefactors[r])
            end
        end
    elseif training==false

        # sorted indexes of  the runners
        sortedargs=sortperm(X)
        # rho definition (density container)
        #For VL calculation. average of the  slowest in front of the runner
        foresightarea=zeros(nrunners)

        # First step: counting the number of runner in the frontview  area
        for (arg_idx, arg) in enumerate(sortedargs)
            if X[arg]< 0.0 continue end #start counting only after crossing the starting line
            if X[arg] > racedistance - fvdist continue end #stop near the crossing the finish line
            foresightarea[arg]=track.foresightarea_data[ceil(Int,X[arg])+1]
            #minn rf is the minimum number of runners in the foresight that impacts the runners speed

            minn=floor(Int, minratio*foresightarea[arg]) #min number of  runners for impact area
            maxn=floor(Int, maxratio*foresightarea[arg]) #min number of  runners for impact are
            #println(minn," ",maxn)
            # continue conditions
            if minn<3 continue end #At least 3 runners in the impact area
            if arg_idx+minn>length(sortedargs) continue end
            if X[sortedargs[arg_idx+minn]]-X[arg]>= fvdist continue end

            rhocounter=1.0
            ############ CONFIRMAR
            argsofguysinfront=sortedargs[arg_idx+1:min(arg_idx+maxn,nrunners)]
            #println(arg_idx+minn:min(arg_idx+maxn,nrunners))

            for arg_i in argsofguysinfront
                if X[arg_i]-X[arg]>fvdist continue
                else rhocounter+=1.0
                end
            end

            if (rhocounter/foresightarea[arg])>maxratio
                R[arg]=maxrho
                #println(rho[arg])
            elseif ((rhocounter/foresightarea[arg]<=maxratio)
                    && (rhocounter/foresightarea[arg]>=minratio))
                D_A=rhocounter/foresightarea[arg]
                R[arg]=(minrho*(D_A-maxratio)-maxrho*(D_A-minratio))/(minratio-maxratio)
                #println(rho[arg])
            end



            lngth=floor(Int,minn/2) #
            if lngth <2 continue end
            sortedspeeds=sort(V[argsofguysinfront])
            slowersspeeds=sortedspeeds[1:lngth]
            slowersavgspeed=sum(slowersspeeds)/length(slowersspeeds)
            VL[arg]=min(slowersavgspeed,V[arg])
            #############################################################################

            # last step compute av speed of the slower guyes
        end



        for r in 1:allrunners.nrunners
            if (t <= allrunners.wavedelays[r]) || (X[r]>=racedistance+epsm)
                V[r]=0.0
            elseif X[r]<0 # This Condition can be improved! (wave propagation in lanes)
                V[r]=min(allrunners.waveinitspeeds[r],allrunners.avgspeeds[r])
            else
                rspeed=(allrunners.avgspeeds[r]+gradient(spline,X[r],1)*allrunners.slopefactors[r])
                V[r]=(1.0-R[r])*rspeed+R[r]*VL[r]
            end
        end

    end
    return V, R
end





function rk2(allrunners,parameters,track,training)
    println(">Control OdeSystemSolvers: Entering rk2_solver")

    nrunners=allrunners.nrunners
    obsnsteps=parameters.observernsteps
    obststep=parameters.observertimestep
    dt=parameters.timestep
    nsteps=ceil(Int,parameters.endtime/dt)
    println(">Control OdeSystemSolvers: total number of time steps = ", nsteps)
    avgspeeds=allrunners.avgspeeds
    slopefactors=allrunners.slopefactors

    println(">Control OdeSystemSolvers: number of runners = ", nrunners)
    # Container for the solutions
    times=zeros(obsnsteps)

    # Internal Copy of allrunners.positions
    positions=allrunners.pos
    println(">control OdeSystemSolvers: size(positions)= ", size(positions))
    println(">control OdeSystemSolvers: initial positions= ", positions[nrunners-10:nrunners,1])

    #println(typeof(positions))
    velocities=zeros(nrunners,obsnsteps)
    rhos=zeros(nrunners,obsnsteps)

    X1=positions[:,1] #rk Updated positions
    X0=positions[:,1] #rk old positions
    V=velocities[:,1] # useless since it is 0

    K1=zeros(nrunners)
    K2=zeros(nrunners)
    #k3=zeros(nrunners)
    #k4=zeros(nrunners)
    j=0
    for i in ProgressBar(0:nsteps-1)
        t=dt*i
        V, R = F(t, X0, V, allrunners,parameters,track,training) #update velocities
        K1=dt .* V
        V, R = F(t+dt, X0 .+ K1, V, allrunners,parameters,track,training) #update velocities
        K2=dt .* V
        X1=X0 .+ 0.5 .* (K1 .+ K2) # update positions

        ## Containers for Observer
        if ((i+1)*dt>=(obststep*j) && i*dt<=(obststep*j))
            delta=(j*obststep-i*dt)/dt
            beta=1.0-delta
            times[j+1]=obststep*(j+1)
            ## interpolations
            positions[:,j+1]= beta .* X0 .+ delta .*X1
            velocities[:,j+1]=V #beta .* velocities[:,j] .+delta.* V
            rhos[:,j+1]=R #beta .* rhos[:,j] .+ delta .* R
            if (j+1 == obsnsteps) break end
            j+=1
        end
        X0=X1
    end

    return times, positions,velocities, rhos

end

end
