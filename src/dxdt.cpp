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


#define DEBUG


bool positionsort ( const tri_xvi&l, const tri_xvi& r)
{ return std::get<0>(l) < std::get<0>(r); }

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
  road_end(floor(track_x_data[track_x_data.size()-1])),
  cs(track_x_data,track_diff_data),
  cs2(track_x_data,track_width_data),
  velocities_instance(std::make_shared<dvec_i>(avg_speeds.size(),0))
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
    //m_road_z.push_back(cs(meter));
    //m_road_dzdx.push_back(cs.deriv(1,meter));
    m_road_w.push_back(cs2(meter));
   }

  for(size_t meter=0;meter<Wsize;meter ++){
    if(meter<Wsize-linear_view){
      wi=m_road_w[meter];
      wip=m_road_w[meter+linear_view];
    }
    else {wi=10.0; wip=10.0;}
    m_foresight_area.push_back(0.5*(wi+wip)*linear_view);
    //std::cout<<"Foresight has "<<m_foresight_area[meter] <<" squared meters at position"<< meter<< std::endl;
  }

  // Testing Sandbox
  //road_begin = std::make_shared<dvec_i>(m_road_w);
  std::cout<<"Testing Track has "<< road_end-road_start <<" meters"<< std::endl;
  //std::cout<<"Testing Track has "<< (*road_begin)[2500] <<" meters"<< std::endl;
  std::cout<<"Track vector has "<< *(m_road_w.begin()-road_start+road_end) <<" meters"<< std::endl;

  int road_pos=2000;
  std::cout<<"Track vector has "<< *(m_road_w.begin()-road_start+road_pos) <<" meters"<< std::endl;
  road_pos=1996;
  std::cout<<"Foresight has "<< *(m_foresight_area.begin()-road_start+road_pos) <<" squared meters"<<  std::endl;


  std::cout <<"Ending constructor of dxdt. Elapsed time: ";

}


void dxdt::operator() ( const dvec_i &x /*state*/ , dvec_i &dxdt , const double  t )
{

  auto sorted_xvi = std::vector<tri_xvi>(x.size());

  for (size_t idx=0; idx<x.size(); idx++){
    // Tuple with (position, instant speed, index)
    sorted_xvi[idx]=std::make_tuple(x[idx],dxdt[idx],idx);
  }
  std::sort(sorted_xvi.begin(),sorted_xvi.end(),positionsort);

  auto densityfactor= dvec_i(x.size(),0.0); // container for the factors that reflects
  auto VL = dvec_i(x.size(),0.0); // For VL calculation


  for (size_t idx=0;idx<x.size();idx++){
    if (x[idx]>road_end) continue;
    int xidx=floor(x[idx])-road_start;
    //std::cout<<xidx<<std::endl;
    int MINN=floor(1./4.*m_foresight_area[xidx]); //floor(1./4.*m_foresight_area) in this case impact should be p=0.4
    int MAXN=2*MINN;

    auto frontispeeds = dvec_i();
    if (((idx+MINN)<x.size())&&(std::get<0>(sorted_xvi[idx+MINN])-std::get<0>(sorted_xvi[idx])<linear_view)) {
      densityfactor[std::get<2>(sorted_xvi[idx])]=0.4;
      /////////////////////////////////////////
      for (size_t ids=MINN;ids<MAXN;ids++){
        if (idx+ids>=x.size()) break;
        else if ((std::get<0>(sorted_xvi[idx+ids])-std::get<0>(sorted_xvi[idx]))<linear_view)
          densityfactor[std::get<2>(sorted_xvi[idx])]+=(1.0/40.);
      }
      // Get the instantaneous speed for the guys in the impact zone
      int ids=0;
      while((idx+ids<x.size())&&(ids<MAXN)){
        frontispeeds.push_back(std::get<1>(sorted_xvi[idx+ids]));
        ids++;}

      std::sort(frontispeeds.begin()+1,frontispeeds.end());

      if (frontispeeds.size()>5)
        VL[idx]=std::min(std::accumulate(frontispeeds.begin()+1,frontispeeds.begin()+6,0.0)/5,frontispeeds[0]);
      frontispeeds.clear();
    }
  }
  double p=0.0;




  for(size_t idx=0;idx<dxdt.size();idx++){
    if (t>m_wave_delays[idx])
      {
        p=densityfactor[idx];
#ifdef DEBUG
        p=0;
        VL[idx]=0.0;
#endif
        dxdt[idx]=(1-p)*(cs.deriv(1,x[idx])*m_slope_factors[idx]+m_avg_speeds[idx])+p*VL[idx];
      }
    else
      dxdt[idx]=0.0;

    (*velocities_instance)[idx]=dxdt[idx];
  }


};

//]
