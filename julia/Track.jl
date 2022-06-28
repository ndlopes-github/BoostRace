module Track
export track
using CubicSplines
using Plots
plotlyjs()
#pyplot()
include("Settings.jl")
import .Settings
par=Settings.par
trackname=par.trackname
data=par.trackdata

struct track_struct
    name::String
    x_data::Vector{Float32}
    diff_data::Vector{Float32}
    width_data::Vector{Float32}
    cspline::CubicSplines.CubicSpline{Float32}
    cspline2::CubicSplines.CubicSpline{Float32}
end

x_data=data[:,1]
diff_data=data[:,2]
width_data=data[:,3]
cspline=CubicSpline(x_data,diff_data)
cspline2=CubicSpline(x_data,width_data)
track=track_struct(trackname,x_data,diff_data,width_data,cspline,cspline2)



function plot_diff_track(track)
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    ys=track.cspline(xs)
    display(plot(xs, ys,title="Elevation (m)",reuse=false))


end

function plot_width_track(track)
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    #fig, ax = plt.subplots(figsize=(6.5, 4))
    #ax.plot(self.x_data,self.diff_data, 'o', label='data')
    ys=track.cspline2(xs)
    display(plot(xs, ys,reuse=false, title="Width (m)"))

end

function plot_slope_track(track)
    xs = range(start=minimum(track.x_data), stop=maximum(track.x_data), length=1000)
    spline=track.cspline
    slope=zeros(0)
    for x in xs
        append!(slope, 100*gradient(spline,x,1))
    end
  display(plot(xs, slope,reuse=false,title="Slope (%)"))

end


if par.logplot==true
    plot_diff_track(track)
    plot_width_track(track)
    plot_slope_track(track)
end

end
