module OdeSystemSolvers

using ProgressBars
using CubicSplines


# Index r for runner
# Index i for time stepping

function F(t, X,allrunners,par,track)
    spline=track.cspline_elev
    rtrn=zeros(allrunners.nrunners)


    for r in 1:allrunners.nrunners
        if (t <= allrunners.wavedelays[r]) || (X[r]>10000)
            rtrn[r]=0.0
        else
            rtrn[r]=allrunners.avgspeeds[r] + gradient(spline,X[r],1)*allrunners.slopefactors[r]
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
        K1=F(times[i], X, allrunners,parameters,track)
        K2=F(times[i]+obststep, X, allrunners,parameters,track)
        X=X .+ 0.5*obststep .* (K1 .+ K2)

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
