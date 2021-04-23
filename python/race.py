# -*- coding: utf-8 -*-
### PRE-PROCESSING ##############################################
import numpy as np
from frunnerclass import frunner, runners, V # As contas estÃ£o aqui
from settings import parameters
from timesgenerator import *
from tracks import track2 as track

# Load the settings
par=parameters()

############## PARAMS ###############################################
rnum=par.nrunners
nsteps=par.simtime
dt=par.observerstep
ninwaves=par.waves[:,0].astype(int)
wavedelays=par.waves[:,1]
waveinitspeeds=par.waves[:,2]

### Initial distribution ###
FAvgTimes, _, InitPositions, WaveDelays,WaveInitSpeeds =\
    inversepseudosigmoid2(number=rnum,
                          lnumber=10,
                          ldist=0.5,
                          ninwaves=ninwaves,
                          wavedelays=wavedelays,
                          waveinitspeeds=waveinitspeeds)

runnerslist=[]
for time,wavedelay,waveinitspeed in zip(FAvgTimes,WaveDelays,WaveInitSpeeds):
    runnerslist.append(frunner(time=time,wavedelay=wavedelay,waveinitspeed=waveinitspeed))

for frunner,initpos in zip(runnerslist,InitPositions):
    frunner.init(nsteps=nsteps,x0=initpos)

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
    wave_init_speeds,
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
