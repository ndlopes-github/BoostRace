module OdeSystemSolvers

using ProgressBars
using CubicSplines


# Index r for runner
# Index i for time stepping

# Velocity function dx/dt=F(...)
function F(t, X,V,allrunners,par,track)
    ## Some alias to simplify
    spline=track.cspline_elev
    nrunners=allrunners.nrunners
    minrho=par.minrho
    maxrho=par.maxrho
    minratio=par.minratio
    maxratio=par.maxratio
    fvdist=par.frontviewdistance
    VL=zeros(nrunners)

    if par.freerace==true
        # Race for timing reports
        for r in 1:nrunners
            if (t <= allrunners.wavedelays[r]) || (X[r]>10010)
                V[r]=0.0
            else
                V[r]=(allrunners.avgspeeds[r] + gradient(spline,X[r],1)*allrunners.slopefactors[r])
            end
        end

    else
        # sorted indexes of  the runners
        sortedargs=sortperm(X)
        # rho definition (density container)
        rho=zeros(nrunners)
        #For VL calculation. average of the  slowest in front of the runner
        foresightarea=zeros(nrunners)

        # First step: counting the number of runner in the frontview  area
        for (arg_idx, arg) in enumerate(sortedargs)
            if X[arg]< 0.0 continue end #start counting only after crossing the starting line
            if X[arg] > par.racedistance - fvdist continue end #stop near the crossing the finish line
            foresightarea[arg]=track.foresightarea_data[ceil(Int,X[arg])+1]
            #minn rf is the minimum number of runners in the foresight that impacts the runners speed

            minn=floor(Int, minratio*foresightarea[arg]) #min number of  runners for impact area
            maxn=floor(Int, maxratio*foresightarea[arg]) #min number of  runners for impact are
            #println(minn," ",maxn)
            # continue conditions
            if minn<3 continue end #At least 3 runners in the impact area
            if arg_idx+minn>size(sortedargs)[1] continue end
            if X[arg_idx+minn]-X[arg]>= fvdist continue end

            rhocounter=3
            ############ CONFIRMAR
            argsofguysinfront=sortedargs[arg_idx+minn:min(arg_idx+maxn,nrunners)]
            #println(arg_idx+minn:min(arg_idx+maxn,nrunners))

            for arg_i in argsofguysinfront
                if X[arg_i]-X[arg]>fvdist continue
                else rhocounter+=1.0
                end
            end

            if (rhocounter/foresightarea[arg])>maxratio
                rho[arg]=maxrho
                #println(rho[arg])
            elseif ((rhocounter/foresightarea[arg]<=maxratio)
                    && (rhocounter/foresightarea[arg]>=minratio))
                D_A=rhocounter/foresightarea[arg]
                rho[arg]=(minrho*(D_A-maxratio)-maxrho*(D_A-minratio))/(minratio-maxratio)
                #println(rho[arg])
            end

            ############### CORRIGIR ####################################################
            lngth=floor(Int,minn/2) #
            if lngth <2 continue end
            sortedspeeds=sort(V[argsofguysinfront])
            slowersspeeds=sortedspeeds
            slowersavgspeed=sum(slowersspeeds)/size(slowersspeeds)[1]
            VL[arg]=min(slowersavgspeed,V[arg])
            #############################################################################

            # last step compute av speed of the slower guyes

        end



        for r in 1:allrunners.nrunners
            if (t <= allrunners.wavedelays[r]) || (X[r]>10010)
                V[r]=0.0
            elseif X[r]<0 # This Condition can be improved! (wave propagation in lanes)
                V[r]=min(allrunners.waveinitspeeds[r],allrunners.avgspeeds[r])
            else
                rspeed=(allrunners.avgspeeds[r] +
                        gradient(spline,X[r],1)*allrunners.slopefactors[r])
                V[r]=(1.0-rho[r])*rspeed+rho[r]*VL[r]
                #println("VR ",V[r])
            end
        end

    end
    return V
end







function rk2_solver(allrunners,parameters,track)
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
    k2=zeros(nrunners)
    #k3=zeros(nrunners)
    #k4=zeros(nrunners)

    for i in ProgressBar(1:obsnsteps-1)
        times[i]=obststep*i
        V=F(times[i], X, V,allrunners,parameters,track) #update velocities
        K1=obststep .* V
        K2=obststep .* F(times[i]+obststep, X .+ K1, V, allrunners,parameters,track)
        X=X .+ 0.5 .* (K1 .+ K2) # update positions

        positions[:,i+1]=X
        velocities[:,i+1]=V
        #=
        function rungekutta4(f, y0, t)
            n = length(t)
            y = zeros((n, length(y0)))
            y[1,:] = y0
            for i in 1:n-1
                h = t[i+1] - t[i]
                k1 = f(y[i,:], t[i])
                k2 = f(y[i,:] + k1 * h/2, t[i] + h/2)
                k3 = f(y[i,:] + k2 * h/2, t[i] + h/2)
                k4 = f(y[i,:] + k3 * h, t[i] + h)
                y[i+1,:] = y[i,:] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
            end
            return y
        end
        =#

        #positions[i+1,:]=X[i+1]
        #velocities[i,:]=F(times[i])
        #rhos[i,:]=rk_rhos
    end
    #println(positions[observernsteps,:])
    return times, positions,velocities, rhos

end

end
