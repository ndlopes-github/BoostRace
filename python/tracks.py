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
        self.width_data=data[:,2]
        self.cspline=CubicSpline(self.x_data,self.diff_data)
        self.cspline2=CubicSpline(self.x_data,self.width_data)

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


track1= track('imaginary1',data=np.array([[-500.,0.,10.],
                                          [-400.,0.,10.],
                                          [-300.,0.,10.],
                                          [-200.,0.,10.],
                                          [-100.,0.,10.],
                                          [0.,0.,10.],
                                          [100.,0.,10.],
                                          [1000.,100,10],
                                          [2000.,-50.,10.],
                                          [3000.,-30.,10.],
                                          [4000.,120.,10.],
                                          [5000.,-27.,10.],
                                          [6000.,59.0,10.],
                                          [7000.,-100.0,10.],
                                          [8000.,-120.0,10.],
                                          [9000.,190.0,10.],
                                          [10000.0,10.0,10.0],
                                          [10100.0,10.0,10.0],
                                          [10200.0,10.0,10.0]]))

track2= track('imaginary2',data=np.array([[-500,0,10.],
                                          [-400,0,10.],
                                          [-300,0,10.],
                                          [-200,0,10.],
                                          [-100,0,10.],
                                          [0,0,10.],
                                          [100,0,10.],
                                          [1000,10,10.],
                                          [2000,-10,5.0],
                                          [2200,-10,2.0],
                                          [2300,-10,7.0],
                                          [3000,-15.,10.0],
                                          [4000,20,10.],
                                          [5000,-7,10.],
                                          [6000,9.0,10.],
                                          [7000,-10.0,10.],
                                          [8000,-1.0,7.],
                                          [9000,1.0,10.],
                                          [10000,0.0,10.],
                                          [10100,0.0,10.],
                                          [10200,0.0,10.]]))

#track2= track('imaginary2',data=np.array([0,10.0,-10.0,-15.0,20.0,-7.0,
#                                              9.0,-10.0,-1.0,1.,0.]))

if __name__== '__main__':
    track1.plot()
    track1.slopeplot()
    track2.plot()
    track2.slopeplot()
