# -*- coding: utf-8 -*-
import numpy as np
from objprint import add_objprint # To print a readable report of the settings

# Track to be considered
from tracks import *

gap=0

@add_objprint
class parameters():
    def __init__(self,
                 timestep=0.4,
                 observertimestep=1.0,
                 observernsteps=7160,
                 endtime=7160,
                 #waves=np.array( [
                 #    [2475,25,0.0,3.34],
                 #    [25,7475,455,2.92]
                 #]),
                 waves=np.array([
                     [3333,0,0, 0.0,3.34],
                     [0,3333,0, 185.0+gap,2.92],
                     [0,0,3334, 383.0+gap*2,2.5]]),
                 linearfrontview=4,
                 minratio= 15./40.,
                 maxratio= 25./40.,
                 minrho=0.4,
                 maxrho=0.8,
                 stepper=2,
                 posweights=np.array([[0.2,0],[2.0,30],[1.5,60],[1.25,120],[1.0,100000]]),
                 track=track_fixed_width(10.0),
                 ldist=0.5
    ):
        self.timestep=timestep # Initial time step for solver 0.4
        self.observertimestep=observertimestep #observer time step in seconds
        self.observernsteps=observernsteps #number of steps to be saved

        self.endtime=endtime

        #Waves [[number,delay,init speed]]
        self.waves=waves
        self.numberofwaves=len(self.waves)
        self.nrunners=np.sum(self.waves[:,0:self.numberofwaves].astype(int)) #number of runners

        self.linearfrontview=linearfrontview # linear impact zone
        self.minratio= minratio  #  15 runners per 40 m2
        self.maxratio= maxratio #  25 runners per 40 m2

        self.minrho=minrho #min weight of the VL speed
        self.maxrho=maxrho #max weight of the VL speed
        self.stepperdict={2 : 'abm2', 3 : 'abm3', 4 : 'abm4', 5 : 'abm5'}
        self.stepper=stepper # '2 : abm2', '3 : abm3', '4 : abm4', '5 : abm5' , # To be implemented '6: rkd5'
        self.integrator=self.stepperdict[self.stepper]
        self.posweights=posweights # Weights for race Metrics Post-Processing
        self.track=track
        self.ldist=ldist # Line distances at startup in meter


## NOTES & TO DOS

'''
2500/2500/5000, 0/210/450
3333/3333/3334, 0/210/450
3333/3333/3334, 0/300/600

waves=np.array([[2800,0.0,3.34],[2800,210.0,2.92],[6300,450.0,2.5]]),
waves=np.array([[3333,0.0,3.34],[3333,210.0,2.92],[3334,450.0,2.5]]),
waves=np.array([[3333,0.0,3.34],[3333,300.0,2.92],[3334,600.0,2.5]]),

waves=np.array([
                     [10000, 0.0,3.34]]
                 ),


waves=np.array([[2500,0,0,0.0,3.34],
                                 [0,2500,0,210.0,2.92],
                                 [0,0,5000,450.0,2.5]]),


waves=np.array([
                     [3333,0,0, 0.0,3.34],
                     [0,3333,0, 210.0,2.92],
                     [0,0,3334, 450.0,2.5]]


com as 3 ondas, fixando a população de cada onda, podíamos testar com os gaps mínimos G1 e G2 iguais aos tempos de saída da onda anterior (por exemplo se a primeira onda demora 2 minutos a sair,
testa-se G1=120, 180, 240, 300, se
G2 demora 150 segundos a sair testa-se
G2=150,
210,
270,
330). Depois faz-se uma matriz de resultados de métrica e regressão na coisa

yo, já experimentaste alguma coisa com as duas ondas?
Em termos de mix tinha pensado em avaliar aqueles delays que falámos no outro dia com as versões:

usando a separação no Q0.5 - 4000Q1,1000Q2/1000Q2,4000Q2 (ou seja trocam 1000), e outra com troca só de 500

waves=np.array( [[5000,0,0.0,3.34],[0,5000,350,2.92]])

usando a separação no Q0.25 (mais comum e assimétrica) - 2000,500/500,7000 (troca de 500) e outra com troca só de 250.

Acho que com isto ficávamos com dados suficientes para avaliar as diferenças principais com 2 ondas


15/10/2021
Testes 3 ondas:
A- 3333,3333,3334;
1-3000,166,167; 166,3000,167; 167,167,3000;
2-2333,500,500; 500, 2333,500; 500, 500, 2334;
B-2500,2500,5000;
1-2200, 100, 200; 100, 2200,200; 200, 200,4600;
2-1900,200,400; 200, 1900, 400; 400,400, 4200;


'''
