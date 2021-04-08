#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from tqdm import tqdm
import datetime
np.random.seed(2875620985)


def racevisuals(anim=True,show=True,save=False,filename=None,nsteps=None,
                track=None,group=None,ninwaves=None,fps=None,dpi=None,cache_frame_data=True):

    if anim:
        plt.rcParams['figure.figsize'] = [8, 6]
        plt.rcParams['figure.dpi'] = dpi # 200 e.g. is really fine, but slower


        fig = plt.figure(figsize=(20,5))
        x=np.linspace(track.x_data.min(), track.x_data.max(), 1000)
        ax = plt.axes(xlim=(track.x_data.min(), track.x_data.max()),
                      ylim=(track.cspline(x).min()-1,
                            track.cspline(x).max()+2*track.cspline2(x).max()+1))
        plt.vlines(0.0,-1,22,'k')
        plt.vlines(10000.,-1,22,'k')
        plt.plot(x,track.cspline(x),'-')
        plt.plot(x,track.cspline(x)+2*track.cspline2(x)+1,'-')
        plt.plot([],[],'.')


        #WE NEED TO SPLIT THE WAVES IN COLORS

        lines=[]
        colors=['tab:blue','tab:orange', 'tab:green','tab:red','tab:purple','tab:brown',\
                'tab:pink','tab:gray','tab:olive','tab:cyan']
        nwaves=len(ninwaves)
        assert nwaves<11, '10 wave colors available'
        for color in colors[:nwaves]:
            lineaux = ax.plot([], [],'.',color=color, ms=1.0)[0]
            lines.append(lineaux)



        #plt.legend(loc='best',ncol=5)
        #plt.ylim(ymin=0,ymax=10)

        plt.xlabel('Road -- (x)meters',fontsize=20)
        plt.ylabel('Road -- (y) ',fontsize=20)
        time_text = ax.text(0.9, 0.1, '', transform=ax.transAxes)

        #normal distribution of Y along the width of the road
        Y=np.random.uniform(0,1,group.size)
        #print(Y)

        # Clean data for linear spline
        #group.pos[:,:]=np.where(group.pos[:,:]>track.x_data.max(),track.x_data.max(),
        #                        group.pos[:,:])

        # initialization function: plot the background of each frame

        #Pre-process roadelevation -> roadZ
        roadZ=np.zeros((group.size,nsteps))
        #Pre-process road width-> RoadW
        roadW=np.zeros((group.size,nsteps))
        for i in range(nsteps):
            roadZ[:,i]=track.cspline(group.pos[:,i])
            roadW[:,i]=track.cspline2(group.pos[:,i])


        def init():
            for line in lines:
                line.set_data([],[])
            return *lines, time_text

        # animation function.  This is called sequentially
        def animate(i):
            i=i
            time_text.set_text(datetime.timedelta(seconds =i))
            ws=0
            we=0
            for number,line in zip(ninwaves,lines):
                we+=number
                xdata=group.pos[ws:we,i]
                ydata=Y[ws:we]*(2*roadW[ws:we,i]+1)+roadZ[ws:we,i]
                line.set_data(xdata,ydata)
                ws+=number

            return *lines, time_text

        # call the animator.  blit=True means only re-draw the parts that have changed.
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=tqdm(range(nsteps)), interval=1,
                                       blit=True,repeat=False)

        # save the animation as an mp4.  This requires ffmpeg or mencoder to be
        # installed.  The extra_args ensure that the x264 codec is used, so that
        # the video can be embedded in html5.  You may need to adjust this for
        # your system: for more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
        if show:
            plt.show()
        if save:
            writer = animation.FFMpegWriter(fps=fps)
            #writer.setup(fig,str(FNumber)+'race_animation.mp4',-1)
            #writer.finish()
            anim.save(filename+'.mp4', writer=writer,dpi=dpi) #25 normal #


def speedsvisuals(runnerslist=None,nsteps=None,track=None,group=None,ninwaves=None,dpi=None):

    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams['figure.dpi'] = dpi # 200 e.g. is really fine, but slower



    fig = plt.figure(figsize=(20,5))
    t=np.linspace(0, nsteps, nsteps+1)
    ax = plt.axes(xlim=(0, 6000),
                  ylim=(group.vels[:,:].min(),
                        group.vels[:,:].max()))

    plt.xlabel('Time',fontsize=20)
    plt.ylabel('Speeds (m/s)',fontsize=20)

    for runner in runnerslist:
        plt.plot(t,group.vels[runner,:],lw=0.5,label=str(runner))

    if len(runnerslist)<11:
        plt.legend()
    plt.show()

def rhossvisuals(runnerslist=None,nsteps=None,track=None,group=None,ninwaves=None,dpi=None):

    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams['figure.dpi'] = dpi # 200 e.g. is really fine, but slower



    fig = plt.figure(figsize=(20,5))
    t=np.linspace(0, nsteps, nsteps+1)
    ax = plt.axes(xlim=(0, 6000),
                  ylim=(group.rhos[:,:].min(),
                        group.rhos[:,:].max()))
    print(group.rhos[:,:].max())

    plt.xlabel('Time',fontsize=20)
    plt.ylabel('weight p',fontsize=20)

    for runner in runnerslist:
        plt.plot(t,group.rhos[runner,:],lw=0.25,label=str(runner))

    if len(runnerslist)<11:
        plt.legend()
    plt.show()


def histvisuals(nsteps=None,group=None):
    plt.rcParams['figure.figsize'] = [12, 6]
    plt.rcParams['figure.dpi'] = 100 # 200 e.g. is really fine, but slower

    frames=nsteps
    nums=np.zeros((frames,10000))

    for i in range(0,frames):
        nums[i],bins = np.histogram(group.pos[:,i],10000, density=False, range=(0,10000))


        # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 10000), ylim=(0, 40))
    line, = ax.plot([], [], lw=2)
    x=np.linspace(0,10000,10000)
    # plt.plot(x,Estrada(x),'-')
    #plt.ylim(ymin=0,ymax=30)
    plt.xlabel('Road -- meters',fontsize=20)
    plt.ylabel('Runners per 4m',fontsize=20)

    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        return line,

    # animation function.  This is called sequentially
    def animate(i):
        x = bins[0:len(bins)-1]
        y = nums[i]
        line.set_data(x, y)
        return line,


    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=tqdm(range(frames)), interval=20, blit=True)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    # anim.save('hist_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    print('hist anim done')
    plt.show()
    plt.clf()


def timesvisuals(times=None,times_free=None,group=None,group_free=None):
   #print(times)

    starttimes=np.zeros(group.size)
    endtimes=np.zeros(group.size)

    for runner in range(group.size):
        tsidx=np.min(np.where(group.pos[runner,:]>0))
        teidx=np.min(np.where(group.pos[runner,:]>10000))
        starttimes[runner]=times[tsidx]
        endtimes[runner]=times[teidx]

    runnertimes=endtimes-starttimes

    starttimes_free=np.zeros(group_free.size)
    endtimes_free=np.zeros(group_free.size)

    for runner in range(group_free.size):
        tsidx=np.min(np.where(group_free.pos[runner,:]>0))
        teidx=np.min(np.where(group_free.pos[runner,:]>10000))
        starttimes[runner]=times[tsidx]
        endtimes[runner]=times[teidx]

    runnertimes_free=endtimes-starttimes



    # rnt=[]
    # for rt in runnertimes:
    #     rnt.append(datetime.timedelta(seconds =rt))

    # print(rnt)
    #print(runnertimes)
    plt.plot(runnertimes,'o',ms=0.5,label='Race')
    plt.plot(runnertimes_free,'o',ms=0.5,label='Alone')
   # plt.yticks(np.arange())
    plt.ylabel("Time in seconds")
    plt.xlabel("Runner index")
    plt.legend()
    plt.show()

    plt.plot(runnertimes-runnertimes_free,'o',ms=0.5,label='Errors')
    plt.ylabel("Time in seconds")
    plt.xlabel("Runner index")
    plt.legend()
    plt.show()
