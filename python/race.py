# -*- coding: utf-8 -*-
### PRE-PROCESSING ##############################################
import numpy as np
from frunnerclass import frunner, runners # As contas estÃ£o aqui
from settings import parameters
from timesgenerator import *
from tracks import track4 as track

# Load the settings
par=parameters()
print(par)
############## PARAMS ###############################################
rnum=par.nrunners
observer_number_steps=par.observernsteps
time_step=par.timestep
observer_time_step=par.observertimestep
observerdt=par.observertimestep
nwaves=par.numberofwaves
ninwaves=par.waves[:,0:nwaves].astype(int) # TO REMOVE




wavedelays=par.waves[:,nwaves]
waveinitspeeds=par.waves[:,1+nwaves]
linear_view=par.linearfrontview
min_ratio=par.minratio
max_ratio=par.maxratio
min_rho=par.minrho
max_rho=par.maxrho
stepper_switch=par.stepper



### Initial distribution ###
# FAvgTimes, _, InitPositions, WaveDelays,WaveInitSpeeds =\
#     inversepseudosigmoid2(number=rnum,
#                           lnumber=10,
#                           ldist=0.5,
#                           ninwaves=ninwaves,
#                           wavedelays=wavedelays,
#                           waveinitspeeds=waveinitspeeds)

### Initial distribution ###
FAvgTimes, _, InitPositions, WaveDelays,WaveInitSpeeds =\
    inversepseudosigmoid3(number=rnum,
                          lnumber=10,
                          ldist=0.5,
                          ninwaves=ninwaves,
                          wavedelays=wavedelays,
                          waveinitspeeds=waveinitspeeds)

runnerslist=[]
for time,wavedelay,waveinitspeed in zip(FAvgTimes,WaveDelays,WaveInitSpeeds):
    runnerslist.append(frunner(time=time,wavedelay=wavedelay,waveinitspeed=waveinitspeed))

for frunner,initpos in zip(runnerslist,InitPositions):
    frunner.init(nsteps=observer_number_steps,x0=initpos)

group=runners(runnerslist)

#print(group.speedfunctions)


# CONVERTED TO std::vector with PYBIND11
avg_speeds=group.avgspeeds[:]
slope_factors=group.slopefactors[:]
wave_delays=group.wavedelays[:]
wave_init_speeds=group.waveinitspeeds[:]
track_x_data=track.x_data[:]
track_diff_data=track.diff_data[:]
track_width_data=track.width_data[:]
init_states=group.pos[:,0]


### PROCESSING ###########################################################
import odesolvers as os
print('Start C++ Processing')
times, positions, velocities,rhos=os.ode_system_solver(
    avg_speeds,
    slope_factors,
    wave_delays,
    wave_init_speeds,
    track_x_data,
    track_diff_data,
    track_width_data,
    init_states,
    observer_number_steps,
    observer_time_step,
    time_step,
    linear_view,
    min_ratio,
    max_ratio,
    min_rho,
    max_rho,
    stepper_switch)

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
    pickle.dump(observer_number_steps, file)
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

with open(f'results/ninwaves.pickle', 'wb') as file:
    pickle.dump(ninwaves, file)
file.close()
