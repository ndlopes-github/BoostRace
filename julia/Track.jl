module Track
export track
using CubicSplines
using Plots
#plotlyjs()
pyplot()
include("Settings.jl")
import .Settings
track_choice=Settings.track


if track_choice=="track1"
    ## Track1 ##
    name="imaginary1"
    data=[-500.0 0.0 10.0 ;
          -400.0  0.0 10.0;
          -300.0 0.0 10.0;
          -200.0 0.0 10.0;
          -100.0 0.0 10.0;
          0.0 0.0 10.0;
          100.0 0.0 10.0;
          1000.0 100.0 10.0;
          2000.0 -50.0 10.0;
          3000.0 -30.0 10.0;
          4000.0 120.0 10.0;
          5000.0 -27.0 10.0;
          6000.0 59.00 10.0;
          7000.0 -100.0 10.0;
          8000.0 -120.0 10.0;
          9000.0 190.0 10.0;
          10000.0 10.0 10.0;
          10100.0 10.0 10.0;
          10200.0 10.0 10.0]
end

if track_choice=="track2"
    name="imaginary2"
    data=[-500.0 0.0 10.0;
          -400.0 0.0 10.0;
          -300.0 0.0 10.0;
          -200.0 0.0 10.0;
          -100.0 0.0 10.0;
          0.0 0.0 10.0;
          100.0 0.0 10.0;
          1000.0 10.0 10.0;
          2000.0 -2.0 5.0;
          2200.0 -2.0 3.0;
          2300.0 -1.0 3.0;
          2400.0 -1.0 3.0;
          2500.0 -1.0 6.0;
          3000.0 -15.0 10.0;
          4000.0 20.0 2.0;
          5000.0 -7.0 10.0;
          6000.0 9.0 10.0;
          7000.0 -10.0 10.0;
          8000.0 -1.0 7.0;
          9000.0 1.0 10.0;
          10000.0 0.0 10.0;
          10100.0 0.0 10.0;
          10200.0 0.0 10.0]
end



struct track_struct
    name
    x_data
    diff_data
    width_data
    cspline
    cspline2
end


x_data=data[:,1]
diff_data=data[:,2]
width_data=data[:,3]
cspline=CubicSpline(x_data,diff_data)
cspline2=CubicSpline(x_data,width_data)
track=track_struct(name,x_data,diff_data,width_data,cspline,cspline2)



function plot_diff_track(track)
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    #fig, ax = plt.subplots(figsize=(6.5, 4))
    #ax.plot(self.x_data,self.diff_data, 'o', label='data')
    ys=track.cspline(xs)
    plot(xs, ys,title="Elevation (m)",reuse=false)
    gui()
    #ax.plot(xs, self.cspline(xs,1), label="S'",color='k')
    #ax.set_xlim(xs.min()-10, xs.max()+10)
    #ax.legend(loc='best', ncol=1)
    #ax.xaxis.set_major_locator(MultipleLocator(1000))
    #ax.grid()
    #plt.show()
end

function plot_width_track(track)
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    #fig, ax = plt.subplots(figsize=(6.5, 4))
    #ax.plot(self.x_data,self.diff_data, 'o', label='data')
    ys=track.cspline2(xs)
    plot(xs, ys,reuse=false)
    gui()
    #ax.plot(xs, self.cspline(xs,1), label="S'",color='k')
    #ax.set_xlim(xs.min()-10, xs.max()+10)
    #ax.legend(loc='best', ncol=1)
    #ax.xaxis.set_major_locator(MultipleLocator(1000))
    #ax.grid()
    #plt.show()
end

function plot_slope_track( track)
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    #fig, ax = plt.subplots(figsize=(6.5, 4))
    #ax.plot(np.linspace(0, self.length, len(self.diff_data)),self.diff_data, 'o', label='data')
    #ax.plot(xs, self.cspline(xs), label="S")
    spline=track.cspline
    slope=zeros(0)
    for x in xs
        append!(slope, 100*gradient(spline,x,1))
    end
    plot(xs, slope,reuse=false)
    gui()
    # ax.set_xlim(xs.min()-10, xs.max()+10)
    #ax.legend(loc='best', ncol=1)
    #ax.xaxis.set_major_locator(MultipleLocator(1000))
    #ax.grid()
    #plt.show()
end

plot_diff_track(track)
plot_width_track(track)
plot_slope_track(track)

end
