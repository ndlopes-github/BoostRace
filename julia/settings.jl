module Settings
export par

struct parameters
    timestep
    observertimestep
    observetnsteps
    endtime
    waves
    linearfrontview
    minratio
    maxratio
    minrho
    maxrho
    posweights
    track
    ldist
end

gap=180
waves=[[2333 500 500  0.0 3.34] [500 2333 500  (214 +1*gap) 2.92] [500 500 2334  (440.0+2*gap) 2.5]]
posweights=[[0.2 0] [2.0 30] [1.5 60] [1.25 120] [1.0 100000]]
par=parameters(0.4,1.0,7080, 7080, waves,4,(15.0/40.0), (25.0/40.0),0.4,0.8,posweights,0.5)

end
