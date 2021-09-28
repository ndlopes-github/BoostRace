#!/usr/bin/env python
# coding: utf-8

import numpy as np
from scipy.interpolate import CubicSpline,interp1d
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)


from objprint import add_objprint # To print a readable report of the settings

@add_objprint
class track():
    def __init__(self,name='',data=None):
        self.name=name
        self.x_data=data[:,0]
        self.diff_data=data[:,1]
        self.width_data=data[:,2]
        self.cspline=CubicSpline(self.x_data,self.diff_data)
        self.cspline2=CubicSpline(self.x_data,self.width_data)
        self.lspline=interp1d(self.x_data,self.diff_data)
        self.lspline2=interp1d(self.x_data,self.width_data)

    def plot(self):
        xs = np.linspace(self.x_data.min(), self.x_data.max(), 1000)
        fig, ax = plt.subplots(figsize=(6.5, 4))
        #ax.plot(self.x_data,self.diff_data, 'o', label='data')
        ax.plot(xs, self.cspline(xs), label='Elevation (m)')
        #ax.plot(xs, self.cspline(xs,1), label="S'",color='k')
        ax.set_xlim(xs.min()-10, xs.max()+10)
        ax.legend(loc='best', ncol=1)
        ax.xaxis.set_major_locator(MultipleLocator(1000))
        ax.grid()
        plt.show()

    def slopeplot(self):
        xs = np.linspace(self.x_data.min(), self.x_data.max(), 1000)
        fig, ax = plt.subplots(figsize=(6.5, 4))
        #ax.plot(np.linspace(0, self.length, len(self.diff_data)),self.diff_data, 'o', label='data')
        #ax.plot(xs, self.cspline(xs), label="S")
        ax.plot(xs, self.cspline(xs,1)*100, label='Slope (%)',color='k')
        ax.set_xlim(xs.min()-10, xs.max()+10)
        ax.legend(loc='best', ncol=1)
        ax.xaxis.set_major_locator(MultipleLocator(1000))
        ax.grid()
        plt.show()

    def widthplot(self):
        xs = np.linspace(self.x_data.min(), self.x_data.max(), 1000)
        fig, ax = plt.subplots(figsize=(6.5, 4))
        #ax.plot(self.x_data,self.width_data, 'o', label='data')
        ax.plot(xs, self.cspline2(xs), label='width (m)')
        #ax.plot(xs, self.cspline(xs,1), label="S'",color='k')
        ax.set_xlim(xs.min()-10, xs.max()+10)
        ax.legend(loc='best', ncol=1)
        # Change major ticks to show every 20.
        ax.xaxis.set_major_locator(MultipleLocator(1000))
       #ax.yaxis.set_major_locator(MultipleLocator(1000))
        ax.grid()
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
                                          [2000,-2,5.0],
                                          [2200,-2,3.0],
                                          [2300,-1,3.0],
                                          [2400,-1,3.0],
                                          [2500,-1,6.0],
                                          [3000,-15.,10.0],
                                          [4000,20,2.],
                                          [5000,-7,10.],
                                          [6000,9.0,10.],
                                          [7000,-10.0,10.],
                                          [8000,-1.0,7.],
                                          [9000,1.0,10.],
                                          [10000,0.0,10.],
                                          [10100,0.0,10.],
                                          [10200,0.0,10.]]))



track3ref= track('imaginary3',data=np.array([[-500,0,16.],
                                             [0,-10.0,16.0],
                                             [220,-12.2,16.0],
                                             [260,-12.6,11.0],
                                             [480,-14.8,11.0],
                                             [520,-15.2,6.0],
                                             [1000,-20.0,6.0],
                                             [1040,-20.0,8.0],
                                             [1500,-20.0,8.0],
                                             [2000,-20,8.0],
                                             [6000,-20,8.],
                                             [6460,-20,8.],
                                             [6500,-20,16.],
                                             [7500,15.0,16.],
                                             [8500,50.0,16.],
                                             [10000,0.0,16.],
                                             [10200,0.0,16.]]))
N=500
auxwidth=np.zeros(N)
auxelev=np.zeros(N)
x=np.linspace(-500,10200,N)

auxlev=track3ref.lspline(x)
auxwidth=track3ref.lspline2(x)
datainterp=np.zeros((len(x),3))
for i in range(len(x)):
    datainterp[i,0]=x[i]
    datainterp[i,1]=auxlev[i]
    datainterp[i,2]=auxwidth[i]

#print(datainterp)

track3=track('silvestre',data=datainterp)


# For fixed width
def track_fixed_width(width):
    return track('flat'+str(width),data=np.array([[-500,0,width],
                                    [0,0,width],
                                    [10000,0,width],
                                    [10200,0.0,width]]))

#track2= track('imaginary2',data=np.array([0,10.0,-10.0,-15.0,20.0,-7.0,
#                                              9.0,-10.0,-1.0,1.,0.]))

if __name__== '__main__':
    track3.plot()
    track3.slopeplot()
    track3.widthplot()

    # track_fixed_width(10.0).plot()
    # track_fixed_width(10.0).slopeplot()
    # track_fixed_width(10.0).widthplot()

    #track2.plot()
    #track2.slopeplot()
