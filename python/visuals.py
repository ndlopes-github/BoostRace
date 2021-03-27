#!/usr/bin/env python
# coding: utf-8

def remap(x, out_min, out_max):
    return (x) * (out_max - out_min)  + out_min

def racevisuals(anim=True,show=True,save=False,filename=None,nsteps=None,
              track=None,group=None,ninwaves=None,fps=None,dpi=None):

    if anim:
        import numpy as np
        import matplotlib.pyplot as plt
        from tqdm import tqdm
        plt.rcParams['figure.figsize'] = [16, 12]
        plt.rcParams['figure.dpi'] = dpi # 200 e.g. is really fine, but slower


        from matplotlib import animation
        import datetime

        fig = plt.figure(figsize=(20,5))
        x=np.linspace(track.x_data.min(), track.x_data.max(), 1000)
        ax = plt.axes(xlim=(-500, 10200),
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

        # initialization function: plot the background of each frame

        #scat=ax.scatter(group.pos[:,0],Y)
        #scat=ax.scatter([],[],s=3.0)

        def init():
            for line in lines:
                line.set_data([],[])
            return *lines, time_text

        # animation function.  This is called sequentially
        def animate(i):
            time_text.set_text(datetime.timedelta(seconds =i))
            ws=0
            we=0
            for number,line in zip(ninwaves,lines):
                we+=number
                xdata=group.pos[ws:we,i]
                ydata=np.zeros(len(Y[ws:we]))
                for j in range(len(Y[ws:we])):
                    ydata[j]=remap(Y[ws+j],
                                   track.cspline(group.pos[ws+j,i]),
                                   track.cspline(group.pos[ws+j,i])+
                                   2*track.cspline2(group.pos[ws+j,i])+1)
               #ydata=Y[ws:we]+track.cspline(group.pos[ws:we,i])#+track.cspline2(group.pos[ws:we,i])
                #ydata=remap(ydata,ydata.min(),ydata.max(),
                #            track.cspline(group.pos[ws:we,i]).min(),
                #            2*track.cspline2(group.pos[ws:we,i].max()))
                line.set_data(xdata,ydata)
                ws+=number

            return *lines, time_text

        # call the animator.  blit=True means only re-draw the parts that have changed.
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=tqdm(range(nsteps)), interval=20,
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


'''
frames=NumberTimeSteps//2

nums=np.zeros((frames,10000))
for i in range(0,frames):
    nums[i],bins = np.histogram(P[i*2],10000, density=False, range=(0,10000))

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 10000), ylim=(0, 13))
line, = ax.plot([], [], lw=2)
x=np.linspace(0,10000,10000)
plt.plot(x,Estrada(x),'-')
plt.ylim(ymin=0,ymax=10)
plt.xlabel('Road -- meters',fontsize=20)
plt.ylabel('Runners per meter',fontsize=20)

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
                               frames=frames, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
# anim.save('hist_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
print('hist anim done')
plt.show()
plt.clf()
'''
