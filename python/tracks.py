#!/usr/bin/env python
# coding: utf-8

import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

from autoclass import autorepr

@autorepr
class track():
    def __init__(self,name='',data=None):
        self.name=name
        self.x_data=data[:,0]
        self.diff_data=data[:,1]
        self.cspline=CubicSpline(self.x_data,self.diff_data)

    def plot(self):
        xs = np.linspace(self.x_data.min(), self.x_data.max(), 1000)
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(self.x_data,self.diff_data, 'o', label='data')
        ax.plot(xs, self.cspline(xs), label="S")
        #ax.plot(xs, self.cspline(xs,1), label="S'",color='k')
        ax.set_xlim(xs.min()-10, xs.max()+10)
        ax.legend(loc='lower left', ncol=1)
        plt.show()

    def slopeplot(self):
        xs = np.linspace(self.x_data.min(), self.x_data.max(), 1000)
        fig, ax = plt.subplots(figsize=(6.5, 4))
        #ax.plot(np.linspace(0, self.length, len(self.diff_data)),self.diff_data, 'o', label='data')
        #ax.plot(xs, self.cspline(xs), label="S")
        ax.plot(xs, self.cspline(xs,1), label="Slope variation'",color='k')
        ax.set_xlim(xs.min()-10, xs.max()+10)
        ax.legend(loc='lower left', ncol=1)
        plt.show()


track1= track('imaginary1',data=np.array([[-500,0],
                                          [-400,0],
                                          [-300,0],
                                          [-200,0],
                                          [-100,0],
                                          [0,0],
                                          [100,0],
                                          [1000,100],
                                          [2000,-50],
                                          [3000,-30],
                                          [4000,120],
                                          [5000,-27],
                                          [6000,59.0],
                                          [7000,-100.0],
                                          [8000,-120.0],
                                          [9000,190.0],
                                          [10000,10.0]]))

track2= track('imaginary2',data=np.array([[-500,0],
                                          [-400,0],
                                          [-300,0],
                                          [-200,0],
                                          [-100,0],
                                          [0,0],
                                          [100,0],
                                          [1000,10],
                                          [2000,-10],
                                          [3000,-15],
                                          [4000,20],
                                          [5000,-7],
                                          [6000,9.0],
                                          [7000,-10.0],
                                          [8000,-1.0],
                                          [9000,1.0],
                                          [10000,0.0]]))

#track2= track('imaginary2',data=np.array([0,10.0,-10.0,-15.0,20.0,-7.0,
#                                              9.0,-10.0,-1.0,1.,0.]))

if __name__== '__main__':
    track1.plot()
    track1.slopeplot()
    track2.plot()
    track2.slopeplot()
