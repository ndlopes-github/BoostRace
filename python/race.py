# -*- coding: utf-8 -*-
### PRE-PROCESSING ##############################################
import argparse
import numpy as np

# Construct the argument parser
ap = argparse.ArgumentParser()


ap.add_argument("-nr", "--nrunners",default=10000, required=False,
   help="number of runners")
ap.add_argument("-nt", "--nsteps",default=7200, required=False,
   help="number of time steps")
ap.add_argument("-dt", "--deltat",default=1.0, required=False,
   help="Time step in seconds")
# ap.add_argument("-an", "--anim",default=1, required=False,
#    help="Generate anim, -an 1")
# ap.add_argument("-sh", "--show",default=1, required=False,
#    help="Generate show, -sh 1")
# ap.add_argument("-af", "--animfile",default='', required=False,
# help="Save animation, -af file.mp4")

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
ninwaves=[rnum//3,rnum//3,rnum//3+1]
wavedelays=[0.0,300.0,600.0]

FAvgTimes, _, InitPositions, WaveDelays = inversepseudosigmoid2(number=rnum,
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


# CONVERTED TO std::vector with PYBIND11
avg_speeds=group.avgspeeds[:]
slope_factors=group.slopefactors[:]
wave_delays=group.wavedelays[:]
track_x_data=track.x_data[:]
track_diff_data=track.diff_data[:]
track_width_data=track.width_data[:]
init_states=group.pos[:,0]

start_time=0.0
time_step=dt
end_time=nsteps*time_step

### PROCESSING ###########################################################
import odesolvers as os
print('Start C++ Processing')
times, positions, velocities,rhos=os.ode_system_solver(
    avg_speeds,
    slope_factors,
    wave_delays,
    track_x_data,
    track_diff_data,
    track_width_data,
    init_states,
    start_time,
    end_time,
    time_step)

print('End C++ Processing')
### POST PROCESSING ######################################################
# Each runner represents a row
# positions are by rows so we have to transpose
group.pos[:,:]=np.transpose(positions)
group.vels[:,:]=np.transpose(velocities)
group.rhos[:,:]=np.transpose(rhos)

print('Writing to files with pickle')
import pickle
#save it
with open(f'results/nsteps.pickle', 'wb') as file:
    pickle.dump(nsteps, file)
file.close()

with open(f'results/times.pickle', 'wb') as file:
    pickle.dump(times, file)
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
