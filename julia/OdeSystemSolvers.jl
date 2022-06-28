module OdeSystemSolvers
export rk4_solver

using ProgressBars


function F(t, avgspeeds, slopefactors)
    return avgspeeds #.+ slopefactors
end

function rk4_solver(avgspeeds,
                           slopefactors,
                           wavedelays,
                           waveinitspeeds,
                           trackdata,
                           initpositions,
                           observernsteps,
                           observertimestep,
                           timestep,
                           linearfrontview,
                           minratio,
                           maxratio,
                           minrho,
                           maxrho
                    )
    println(">Control: Entering rk4_solver")
    nrunners=size(slopefactors)[1]
    println(">Control: number of runners = ", nrunners)
    # Container for the solutions
    times=zeros(observernsteps)

    positions=zeros(Float32, observernsteps,nrunners)

    for i in 1:nrunners positions[1,i]=initpositions[i][1] end
    println(positions[1,:])

    #println(typeof(positions))
    velocities=zeros(observernsteps,nrunners)
    rhos=zeros(observernsteps,nrunners)

    K1=zeros(nrunners)
    #k2=zeros(nrunners)
    #k3=zeros(nrunners)
    #k4=zeros(nrunners)

    for i in ProgressBar(1:observernsteps-1)
        times[i]=observertimestep*i
        K1=F(times[i], avgspeeds, slopefactors)

        positions[i+1,:]=positions[i,:] .+ observertimestep .* K1
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
    println(positions[observernsteps,:])
    return times, positions,velocities, rhos

end

end
