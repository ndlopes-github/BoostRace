# -*- coding: utf-8 -*-
### PRE-PROCESSING ##############################################
import numpy as np
from frunnerclass import frunner, runners # As contas estão aqui
from settings import parameters
from timesgenerator import *

# Load the settings
par=parameters()
print('control: track name is=', par.track.name)
print(par)


### Initial distribution ###
FAvgTimes, NinWaves, InitPositions, WaveDelays,WaveInitSpeeds =inversepseudosigmoid( )

runnerslist=[]
for time,wavedelay,waveinitspeed in zip(FAvgTimes,WaveDelays,WaveInitSpeeds):
    runnerslist.append(frunner(time=time,wavedelay=wavedelay,waveinitspeed=waveinitspeed))

for frunner,initpos in zip(runnerslist,InitPositions):
    frunner.init(nsteps=par.observernsteps,x0=initpos)

group=runners(runnerslist)
#print(group)


### PROCESSING ###########################################################
import odesolvers as os
print('Start C++ Processing')
times, positions, velocities,rhos=os.ode_system_solver(
    group.avgspeeds[:],
    group.slopefactors[:],
    group.wavedelays[:],
    group.waveinitspeeds[:],
    par.track.x_data[:],
    par.track.diff_data[:],
    par.track.width_data[:],
    group.pos[:,0],
    par.observernsteps,
    par.observertimestep,
    par.timestep,
    par.linearfrontview,
    par.minratio,
    par.maxratio,
    par.minrho,
    par.maxrho,
    par.stepper)

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


with open(f'results/times.pickle', 'wb') as file:
    pickle.dump(times, file)
file.close()

with open(f'results/group.pickle', 'wb') as file:
    pickle.dump(group, file)
file.close()

with open(f'results/ninwaves.pickle', 'wb') as file:
    pickle.dump(NinWaves, file)
file.close()
