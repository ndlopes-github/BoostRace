module OdeSystemSolvers

using ProgressBars
using CubicSplines


# Index r for runner
# Index i for time stepping

# Velocity function dx/dt=F(...)
function F(t, X,allrunners,par,track)
    spline=track.cspline_elev
    nrunners=allrunners.nrunners
    rtrn=zeros(nrunners)

    if par.freerace==true
        # Race for timing reports
        for r in 1:nrunners
            if (t <= allrunners.wavedelays[r]) || (X[r]>10010)
                rtrn[r]=0.0
            else
                rtrn[r]=(allrunners.avgspeeds[r] + gradient(spline,X[r],1)*allrunners.slopefactors[r])
            end
        end

    else
        # sorted indexes of  the runners
        sortedargs=sortperm(X)

        # rho definition (density container)
        rho=zeros(nrunners)
        #For VL calculation. average of the  slowest in front of the runner
        vl=zeros(nrunners)
        foresightarea=zeros(nrunners)

        # First step: counting the number of runner in the frontview  area
        for arg in sortedargs
            if X[arg]< 0.0 continue end #start counting only after crossing the starting line
            if X[arg] > par.racedistance - par.frontviewdistance continue end #stop near the crossing the finish line
            foresightarea[arg]=track.foresightarea_data[ceil(Int,X[arg])+1]
            #minn rf is the minimum number of runners in the foresight that impacts the runners speed
            minn=floor(Int,par.minratio*foresightarea[arg])
            #maxn rf is the minimum number of runners in the foresight that impacts the runners speed
            maxn=floor(Int,par.maxratio*foresightarea[arg])

            for arg_i in sortedargs[arg+minn:min(arg+maxn,nrunners)]
                if X[arg_i]-X[arg]<par.frontviewdistance
                    rho[arg]+=1.0
                else continue
                end
            end
        end

        for r in 1:allrunners.nrunners
            if (t <= allrunners.wavedelays[r]) || (X[r]>10010)
                rtrn[r]=0.0
            elseif X[r]<0 # This Condition can be improved! (wave propagation in lanes)
                rtrn[r]=min(allrunners.waveinitspeeds[r],allrunners.avgspeeds[r])
            else
                rtrn[r]=(allrunners.avgspeeds[r] + gradient(spline,X[r],1)*allrunners.slopefactors[r])
            end
        end

    end
    return rtrn
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
    K1=zeros(nrunners)
    k2=zeros(nrunners)
    #k3=zeros(nrunners)
    #k4=zeros(nrunners)

    for i in ProgressBar(1:obsnsteps-1)
        times[i]=obststep*i
        K1=obststep .* F(times[i], X, allrunners,parameters,track)
        K2=obststep .* F(times[i]+obststep, X .+ K1, allrunners,parameters,track)
        X=X .+ 0.5 .* (K1 .+ K2)

        positions[:,i+1]=X

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
