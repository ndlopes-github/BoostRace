## Welcome to the GitHub page for the paper "The modeling of urban races"

Here we show some simulations done with the BoostRace code that is introduced in the paper.

### Settings for the simulation
Some of the settings used:

gap=180\
timestep=0.4\
observertimestep=1.0\
observernsteps=7080\
endtime=7080\
waves=np.array([[2333,500,500, 0.0,3.34],
                [500,2333,500, 214 +1*gap, 2.92],
                [500,500,2334,  440.0+2*gap, 2.5]
                ])\                 
linearfrontview=4\
minratio= 15./40.\
maxratio= 25./40.\
minrho=0.4\
maxrho=0.8\
stepper=2\
posweights=np.array([[0.2,0],[2.0,30],[1.5,60],[1.25,120],[1.0,100000]])\
track=track2\
ldist=0.5

more details at [settings.py](https://github.com/ndlopes-github/BoostRace/blob/main/python/settings.py)

### Results and animation
[Animation](https://user-images.githubusercontent.com/58338787/157900110-efebdc3d-d6e0-471e-8544-a106e0083d1e.mp4) and ![Image](src)


For more details see [submitted paper]().

### Contacts
ricardo.roque@isel.pt

nuno.lopes@isel.pt
