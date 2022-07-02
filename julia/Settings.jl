module Settings
using Interpolations
export par

# TODO: ORGANIZATION

logplot=true
freerace=false

racedistance=10000.0 #in meters

timestep=0.2 # should divide observertimestep
observertimestep=1.0
observernsteps=7080
endtime=7080.0
frontviewdistance=4.0 # Linear Reference distance in front of the runner
minratio=15.0/40.0
maxratio=25.0/40.0
minrho=0.4
maxrho=0.8
posweights=[0.2 0; 2.0 30;  1.5 60;  1.25 120; 1.0 100000]
ldist=0.5

gap=60

waves=[ 2333 500 500 0.0 3.34;
        500  2333 500 (214 +1*gap) 2.92;
        500 500 2334 (440.0+2*gap) 2.5]


#=
    trackname="track1"
    trackdata=[-500.0 0.0 10.0 ;
          -400.0  0.0 10.0;
          -300.0 0.0 10.0;
          -200.0 0.0 10.0;
          -100.0 0.0 10.0;
          0.0 0.0 10.0;
          100.0 0.0 10.0;
          1000.0 100.0 10.0;
          2000.0 -50.0 10.0;
          3000.0 -30.0 10.0;
          4000.0 120.0 10.0;
          5000.0 -27.0 10.0;
          6000.0 59.00 10.0;
          7000.0 -100.0 10.0;
          8000.0 -120.0 10.0;
          9000.0 190.0 10.0;
          10000.0 10.0 10.0;
          10100.0 10.0 10.0;
          10200.0 10.0 10.0]
=#

#=
    trackname="track2"
    trackdata=[-500.0 0.0 10.0;
          -400.0 0.0 10.0;
          -300.0 0.0 10.0;
          -200.0 0.0 10.0;
          -100.0 0.0 10.0;
          0.0 0.0 10.0;
          100.0 0.0 10.0;
          1000.0 10.0 10.0;
          2000.0 -2.0 5.0;
          2200.0 -2.0 3.0;
          2300.0 -1.0 3.0;
          2400.0 -1.0 3.0;
          2500.0 -1.0 6.0;
          3000.0 -15.0 10.0;
          4000.0 20.0 2.0;
          5000.0 -7.0 10.0;
          6000.0 9.0 10.0;
          7000.0 -10.0 10.0;
          8000.0 -1.0 7.0;
          9000.0 1.0 10.0;
          10000.0 0.0 10.0;
          10100.0 0.0 10.0;
          10200.0 0.0 10.0]
=#

trackname="silvestre"
data_aux=[-500.0 10.0 16.0;
          220.0 (-0.02*220.0) 16.0;
          260.0 (-0.02*260.0) 11.0;
          480.0 (-0.02*480.0) 11.0;
          520.0 (-0.02*520.0) 6.0;
          1000.0 -20.0 6.0;
          1040.0 -20.0 8.0;
          1500.0 -20.0 8.0;
          2000.0 -20.0 8.0;
          6000.0 -20.0 8.0;
          6500.0 -20.0 8.0;
          7460.0 13.6 8.0;
          7500.0 15.0 16.0;
          8500.0 50.0 16.0;
          10000.0 0.0 16.0;
          10500.0 (-1050.0/3+1000.0/3.0) 16.0]
N=501
#auxwidth=zeros(N)
#auxlevel=zeros(N)
x=range(start=-500.0,stop=10500,length=N)
aux_diff_lspline=LinearInterpolation(data_aux[:,1],data_aux[:,2])
aux_width_lspline=LinearInterpolation(data_aux[:,1],data_aux[:,3])
auxlevel=aux_diff_lspline.(x)
auxwidth=aux_width_lspline.(x)
trackdata=zeros(N,3)
for i in range(1,N)
    trackdata[i,1]=x[i]
    trackdata[i,2]=auxlevel[i]
    trackdata[i,3]=auxwidth[i]
end

##############################################################################

struct Parameters
    timestep::Float32
    observertimestep::Float32
    observernsteps::Int16
    endtime::Float32
    waves::Matrix{Float32}
    frontviewdistance::Float32
    minratio::Float32
    maxratio::Float32
    minrho::Float32
    maxrho::Float32
    posweights::Matrix{Float32}
    ldist::Float32
    numberofwaves::Int8
    nrunners::Int16
    trackname::String
    trackdata::Matrix{Float32}
    racedistance::Float32
    freerace::Bool
    logplot::Bool
end

numberofwaves=size(waves)[1]
nrunners=Int(sum(waves[:,1:numberofwaves]))
println(">Control Settings: nrunners = ", nrunners)
par=Parameters(timestep,observertimestep,observernsteps, endtime,
               waves,frontviewdistance,minratio,maxratio,minrho,maxrho,
               posweights,ldist, numberofwaves, nrunners, trackname,trackdata,
               racedistance,freerace,logplot)


end
