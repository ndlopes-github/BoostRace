//#include <boost/sort/spreadsort/spreadsort.hpp>
#include <iostream>
#include<numeric>
#include "typedefs.h"
#include "settings.h"
#include "spline.h"
#include "dxdt.h"
#include <cmath>
#include <boost/progress.hpp> //deprecated but working
//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
/* HERE WE SHOULD DEFINE THE RHS OF THE ODE SYSTEM*/


dxdt::dxdt(dvec_i avg_speeds,
           dvec_i slope_factors,
           dvec_i wave_delays,
           dvec_i track_x_data,
           dvec_i track_diff_data,
           dvec_i track_width_data):
  m_avg_speeds(avg_speeds),
  m_slope_factors(slope_factors),
  m_track_x_data( track_x_data),
  m_track_diff_data( track_diff_data),
  m_wave_delays(wave_delays),
  road_start(floor(track_x_data[0])),
  road_end(ceil(track_x_data[track_x_data.size()-1])),
  cs(track_x_data,track_diff_data),
  cs2(track_x_data,track_width_data),
  velocities_instance(std::make_shared<dvec_i>(avg_speeds.size(),0)),
  rhos_instance(std::make_shared<dvec_i>(avg_speeds.size(),0))
{
  std::cout <<" Constructing dxdt." << std::endl;
  boost::progress_timer t;
  // Define the number of meters or blocks in the track
  // m_road_z has  the diff elevation of the track per meter/block
  // m_road_dxdz has the slope in each block/meter
  size_t Wsize= road_end-road_start+1;
  std::cout<<"Track has "<< Wsize <<" Width measures"<< std::endl;

  double wi=0.0;
  double wip=0.0;
  for(size_t meter=0;meter<Wsize;meter ++){
    // m_road_z.push_back(cs(meter));
    // m_road_dzdx.push_back(cs.deriv(1,meter));
    m_road_w.push_back(cs2(meter));
   }

  for(size_t meter=0;meter<Wsize;meter++){
    double area=0.0;
    if(meter<Wsize-linear_view)
      for (size_t i=0; i<linear_view; i++)
        area+=m_road_w[meter];
    else area=40;
    m_foresight_area.push_back(area);
    //std::cout<<"Foresight has "<<m_foresight_area[meter] <<" squared meters at position"<< meter<< std::endl;
  }
  std::cout <<"Ending constructor of dxdt. Elapsed time: ";
}






#ifndef DEBUG
void dxdt::operator() ( const dvec_i &x /*state*/ , dvec_i &dxdt , const double  t )
{
  //**** sort all the runners by position ********************
  // generate a tuple with position, velocity, index

  auto sorted_xvi = std::vector<tri_xvi>(x.size());
  for (size_t idx=0; idx<x.size(); idx++){
    // Tuple with (position, instant speed, index)
    sorted_xvi[idx]=std::make_tuple(x[idx],dxdt[idx],idx);
    // Shouldn't  (*velocities_instance)[idx] and dxdt[idx] be equal at this step ?
    // (*velocities_instance)  velocities to be keept by the observer at each time step
    // while dxdt[idx] is update by the intermidiate steps of the stepper/solver.

    #ifdef DEBUG
    if(std::fabs((*velocities_instance)[idx]-dxdt[idx])>1.e-6)
      std::cout<< std::fabs((*velocities_instance)[idx]-dxdt[idx])<< " error"<<std::endl;
    #endif
  }
  // Using lambda function for position sort
  std::sort(sorted_xvi.begin(),sorted_xvi.end(),
            []( const tri_xvi&l, const tri_xvi& r){ return std::get<0>(l) < std::get<0>(r);});
  // end sorting

  // Create a density container for each runner foresight
  auto rho= dvec_i(x.size(),0.0); // rho for density factor. container for the factors that reflects the density
  // Create a container for the average velocities of the 5 runners in front
  // to be used when rho !=0 for
  auto VL = dvec_i(x.size(),0.0); // For VL calculation. average of the  slowest in front of the runner

  // iterate over sorted tuples
  for(std::vector<tri_xvi>::const_iterator i = sorted_xvi.begin(); i != sorted_xvi.end(); ++i)
    {
      if  (std::get<0>(*i)>road_end) continue;
      int xidx=floor(std::get<0>(*i))-road_start; //
      //MINN is the minimum number of runners in the foresight that impacts the runners speed
      int MINN=floor(1./4.*m_foresight_area[xidx]); //floor(1./4.*m_foresight_area) in this case impact should be p=0.4
      int MAXN=2*MINN; //MAX is the maximum number of runners in the foresight that impacts the runners speed
      auto frontispeeds = dvec_i(); // container for the instantaneous speeds of the runners in the foresigh area
      // Guarding conditions for indexing
      if ((MINN<3)|| // At the  worst case (very narrow area) the runner has at least 3 runners in the impact zone
          ((i+MINN)> sorted_xvi.end()-1)|| //there are at least MINN runners in front of runner i
          (std::get<0>(*(i+MINN))-std::get<0>(*i)>=linear_view)) // the MINN runner in front is in the impact zone
        continue;

      rho[std::get<2>(*i)]=0.4;

      for (size_t ids=MINN;ids<MAXN+1;ids++)
        if (i+ids>sorted_xvi.end()-1) continue;
        else if (std::get<0>(*(i+ids))-std::get<0>(*i)<linear_view)
          rho[std::get<2>(*i)]+=(1.0/(2*MAXN)); // This one should be fixed it was 1.0/40.0.

      int ids=0;
      while((i+ids<sorted_xvi.end())&&(ids<MAXN+1)){
        // Note that when ids=0 the runner speed is keept in the first position of the frontispeeds container
        frontispeeds.push_back(dxdt[std::get<2>(*(i+ids))]);
        ids++;}

      // Sort the speeds of the runners in the impact zone
      std::sort(frontispeeds.begin()+1,frontispeeds.end());

       // Runner can not speed up if the guys in front are faster than him
      int navg=MINN/2;
      VL[std::get<2>(*i)]=std::min(std::accumulate(frontispeeds.begin()+1,frontispeeds.begin()+navg+1,0.0)/navg,frontispeeds[0]);

      frontispeeds.clear();

    }

  // Update the system velocities
  double p=0;
  for(size_t idx=0;idx<dxdt.size();idx++)
    {
      p=rho[idx];
      if (t<=m_wave_delays[idx]) continue;
      dxdt[idx]=(1-p)*(cs.deriv(1,x[idx])*m_slope_factors[idx]+m_avg_speeds[idx])+p*VL[idx];
      //dxdt[idx]=(1-p)*(m_road_dzdx[floor(x[idx])-road_start]*m_slope_factors[idx]+m_avg_speeds[idx])+p*VL[idx];

      (*velocities_instance)[idx]=dxdt[idx];// Update the velocities_instance with the dxdt values
      (*rhos_instance)[idx]=rho[idx];
    }

};

#endif















#ifdef DEBUG
void dxdt::operator() ( const dvec_i &x /*state*/ , dvec_i &dxdt , const double  t )
{
  for(size_t idx=0;idx<dxdt.size();idx++)
    {
      if (t<=m_wave_delays[idx]) continue;
      dxdt[idx]=cs.deriv(1,x[idx])*m_slope_factors[idx]+m_avg_speeds[idx];
      (*velocities_instance)[idx]=dxdt[idx]; // Update the velocities_instance with the dxdt values
    }
};
#endif

//]
