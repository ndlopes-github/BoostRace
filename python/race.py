# -*- coding: utf-8 -*-

import argparse
import numpy as np

# Construct the argument parser
ap = argparse.ArgumentParser()


ap.add_argument("-nr", "--nrunners",default=10000, required=False,
   help="number of runners")
ap.add_argument("-nt", "--nsteps",default=6000, required=False,
   help="number of time steps")
ap.add_argument("-dt", "--deltat",default=1, required=False,
   help="Time step in seconds")

args = vars(ap.parse_args())


from frunnerclass import frunner, runners, V # As contas estÃ£o aqui

############## PARAMS ###############################################
RNUM=int(args['nrunners'])
NSTEPS=int(args['nsteps'])



######################################################################


# # Next step: simulations #
###################################################
### RACE SIMULATION ###############################

from tracks import track2 as track
#track.slopeplot()

#Race Settings
nsteps=NSTEPS
dt=float(args['deltat']) #[s]

from timesgenerator import *

rnum=RNUM
ninwaves=[rnum//5,2*rnum//5,2*rnum//5]
wavedelays=[0.0,360.0,500.0]

FAvgTimes, _, InitPositions, WaveDelays = inversepseudosigmoid(number=rnum,
                                                               lnumber=10,
                                                               ldist=0.5,
                                                               ninwaves=ninwaves,
                                                               wavedelays=wavedelays) #Times in minutes
#print(FAvgTimes)

runnerslist=[]
for time,wavedelay in zip(FAvgTimes,WaveDelays):
    runnerslist.append(frunner(time=time,wavedelay=wavedelay))

for frunner,initpos in zip(runnerslist,InitPositions):
    frunner.init(nsteps=NSTEPS,x0=initpos)

group=runners(runnerslist)

#print(group.speedfunctions)


import odesolvers as os
avg_speeds=np.array([1.0,1.2]).tolist()
init_states=np.array([1.0,0]).tolist()
start_time=0.0
end_time=5.0
time_step=1.0

times, positions=os.rk4_ode_system_solver(avg_speeds,init_states,
                                          start_time,end_time,time_step)

print(times,positions)
