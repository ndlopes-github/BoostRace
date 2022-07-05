module OdeSystemSolvers
export rk2

using ProgressBars
using CubicSplines


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
    R=zeros(nrunners)

    if training==true
        # Race for timing reports
        for r in 1:nrunners
            if (t <= allrunners.wavedelays[r]) || (X[r]>racedistance)
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
            if arg_idx+minn>size(sortedargs)[1] continue end
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

            ############### CORRIGIR ####################################################
            lngth=floor(Int,minn/2) #
            if lngth <2 continue end
            sortedspeeds=sort(V[argsofguysinfront])
            slowersspeeds=sortedspeeds[1:lngth]
            slowersavgspeed=sum(slowersspeeds)/size(slowersspeeds)[1]
            VL[arg]=min(slowersavgspeed,V[arg])
            #############################################################################

            # last step compute av speed of the slower guyes

        end



        for r in 1:allrunners.nrunners
            if (t <= allrunners.wavedelays[r]) || (X[r]>racedistance)
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

    X=positions[:,1]
    V=velocities[:,1] # useless since it is 0

    K1=zeros(nrunners)
    K2=zeros(nrunners)
    #k3=zeros(nrunners)
    #k4=zeros(nrunners)

    for i in ProgressBar(1:obsnsteps-1)
        times[i]=obststep*i
        V, R = F(times[i], X, V, allrunners,parameters,track,training) #update velocities
        K1=obststep .* V
        V, R = F(times[i]+obststep, X .+ K1, V, allrunners,parameters,track,training) #update velocities
        K2=obststep .* V
        X=X .+ 0.5 .* (K1 .+ K2) # update positions

        positions[:,i+1]=X
        velocities[:,i+1]=V
        rhos[:,i+1]=R

        #velocities[i,:]=F(times[i])
        #rhos[i,:]=rk_rhos
    end
    #println(positions[observernsteps,:])
    return times, positions,velocities, rhos

end

end
