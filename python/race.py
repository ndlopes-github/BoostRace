# -*- coding: utf-8 -*-
### PRE-PROCESSING ##############################################
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
avg_speeds=group.avgspeeds[:]
init_states=group.pos[:,0]
start_time=0.0
time_step=1.0
end_time=nsteps*time_step

### PROCESSING ###########################################################
print('Start C++ Processing')
times, positions=os.rk4_ode_system_solver(avg_speeds,init_states,
                                          start_time,end_time,time_step)
print('End C++ Processing')
### POST PROCESSING ######################################################
# Each runner represents a row
# positions are by rows so we have to transpose
group.pos[:,:]=np.transpose(positions)
print('Writing to files with pickle C++')
import pickle
#save it
with open(f'results/nsteps.pickle', 'wb') as file:
    pickle.dump(nsteps, file)
file.close()

with open(f'results/group.pickle', 'wb') as file:
    pickle.dump(group, file)
file.close()

with open(f'results/track.pickle', 'wb') as file:
    pickle.dump(track, file)
file.close()

with open(f'results/runnerslist.pickle', 'wb') as file:
    pickle.dump(runnerslist, file)
file.close()

with open(f'results/ninwaves.pickle', 'wb') as file:
    pickle.dump(ninwaves, file)
file.close()
