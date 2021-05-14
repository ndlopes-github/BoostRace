#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from tqdm import tqdm
import datetime
from settings import parameters
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

    for runner in runnerslist: #range(group.size):
        plt.plot(t,group.vels[runner,:],lw=0.5,label=str(runner))

    if len(runnerslist)<11:
        plt.legend()
    plt.show()


def phasevisuals(runnerslist=None,nsteps=None,track=None,group=None,ninwaves=None,dpi=None):

    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams['figure.dpi'] = dpi # 200 e.g. is really fine, but slower



    fig = plt.figure(figsize=(20,5))
    t=np.linspace(0, nsteps, nsteps+1)
    ax = plt.axes(xlim=(group.pos[:,:].min(),
                        10010),
                  ylim=(group.vels[:,:].min(),
                        group.vels[:,:].max()))

    plt.xlabel('Positions (m)',fontsize=20)
    plt.ylabel('Speeds (m/s)',fontsize=20)

    for runner in runnerslist:
        plt.plot(group.pos[runner,:],group.vels[runner,:],lw=0.5,label=str(runner))

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

    starttimes=np.zeros(group.size)
    endtimes=np.zeros(group.size)


    for runner in range(group.size):
        tsidx=np.min(np.where(group.pos[runner,:]>0))
        teidx=np.min(np.where(group.pos[runner,:]>10000))
        starttimes[runner]=times[tsidx]
        endtimes[runner]=times[teidx]

    runnertimes=endtimes-starttimes

    racetime=np.max(endtimes)
    slowrunners=np.argmax(endtimes)

    starttimes_free=np.zeros(group_free.size)
    endtimes_free=np.zeros(group_free.size)

    for runner in range(group_free.size):
        tsidx=np.min(np.where(group_free.pos[runner,:]>0))
        teidx=np.min(np.where(group_free.pos[runner,:]>10000))
        starttimes_free[runner]=times[tsidx]
        endtimes_free[runner]=times[teidx]

    runnertimes_free=endtimes_free-starttimes_free



    plt.plot(runnertimes,'o',ms=0.5,label='Race')
    plt.plot(runnertimes_free,'o',ms=0.5,label='Alone')
    plt.ylabel("Time in seconds")
    plt.xlabel("Runner index")
    plt.legend()
    plt.savefig('personaltimings.png')
    plt.clf()

    errors=runnertimes-runnertimes_free
    print(*np.where(errors<0))
    print('Runners  affected by the velocity rule at departure')
    print(len(*np.where(starttimes!=starttimes_free)))

    # print('free times',runnertimes_free[np.where(errors<0)])
    # print('times',runnertimes[np.where(errors<0)])
    # print('free start',starttimes_free[np.where(errors<0)])
    # print('start',starttimes[np.where(errors<0)])
    # print('free end',endtimes_free[np.where(errors<0)])
    # print('end',endtimes[np.where(errors<0)])

    par=parameters()
    t1=par.posweights[1,1]
    t2=par.posweights[2,1]
    t3=par.posweights[3,1]
    t4=par.posweights[4,1]

    w0=par.posweights[0,0]
    w1=par.posweights[1,0]
    w2=par.posweights[2,0]
    w3=par.posweights[3,0]
    w4=par.posweights[4,0]


    errorspen=np.zeros(len(errors))
    count_t1=0
    count_t2=0
    count_t3=0
    count_t4=0
    for idx,error in enumerate(errors):
        if error <= t1:
            errorspen[idx]=error*w1
            count_t1+=1
        elif t1 < error <= t2:
            errorspen[idx]=w1*t1+(error-t1)*w2
            count_t2+=1
        elif t2 < error <= t3 :
            errorspen[idx]=w1*t1+(t2-t1)*w2+(error-t2)*w3
            count_t3+=1
        else :
            errorspen[idx]=w1*t1+(t2-t1)*w2+(t3-t2)*w3+(error-t3)*w4
            count_t4+=1

    print('control: number of runners with time loss in [0,', t1,'] is', count_t1)
    print('control: number of runners with time loss in ]',t1,',', t2,'] is', count_t2)
    print('control: number of runners with time loss in ]',t2,',', t3,'] is', count_t3)
    print('control: number of runners with time loss >',t3, ' is', count_t4)

    errorspen+=starttimes*w0
    negerrors=np.where(errorspen<0)
    print(len(negerrors[0]))
    print(negerrors)
    if len(negerrors)>0:
        print('warning: negative penalized errors:',)

    print('control:', par.waves)
    r0=0
    r1=0
    for j in range(1,len(par.waves)):
        r0+=np.sum(par.waves[:par.numberofwaves,j-1]).astype(int)
        r1=np.sum(par.waves[:par.numberofwaves,j]).astype(int)
        errorspen[r0:r1]-=w0*par.waves[j,1]
        print('control',r0,' ',r1,', ',par.waves[j,1])


    plt.plot(errors,'o',ms=0.5,label='Errors')
    plt.plot(errorspen,'o',ms=0.5,label='PErrors')
    plt.ylabel('Time in seconds (total='+str(racetime)+')')

    print('control: race time is', racetime)
    print('control: slowest racer=', slowrunners)

    metricerror=np.sum(errorspen)
    print('control: metric error=', metricerror)

    plt.xlabel('Runner index (slow runners= '+str(slowrunners)+')')
    plt.title('l1 norm='+str(np.linalg.norm(errors,ord=1))+\
              '\n metric ='+str(metricerror)+\
              ' delays ='+str(par.waves[:,par.numberofwaves]))
    #plt.text(0,550,'l1 norm='+str(np.linalg.norm(errors,ord=1)))
    #plt.text(0,500,'metric ='+str(np.sum(errorspen)))
    plt.text(0,300,'waves ='+str(par.waves[:,0:par.numberofwaves]))
    #plt.text(0,400,'delays ='+str(par.waves[:,1]))
    #plt.text(0,350,'speeds_0 ='+str(par.waves[:,2]))
    plt.legend(loc=9 )
    plt.savefig('errors_report.png')
    plt.clf()
