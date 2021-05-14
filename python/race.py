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


### Initial distribution ###
nwaves=par.numberofwaves
mixwaves=par.waves[:,0:nwaves].astype(int) # TO REMOVE
wavedelays=par.waves[:,nwaves]
waveinitspeeds=par.waves[:,1+nwaves]

FAvgTimes, NinWaves, InitPositions, WaveDelays,WaveInitSpeeds =\
    inversepseudosigmoid3(number=par.nrunners,
                          lnumber=10,
                          ldist=0.5,
                          mixwaves=mixwaves,
                          wavedelays=wavedelays,
                          waveinitspeeds=waveinitspeeds)

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
    track.x_data[:],
    track.diff_data[:],
    track.width_data[:],
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

with open(f'results/nsteps.pickle', 'wb') as file:
    pickle.dump(par.observernsteps, file)
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
    pickle.dump(NinWaves, file)
file.close()
