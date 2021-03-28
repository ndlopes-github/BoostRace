//#include <boost/sort/spreadsort/spreadsort.hpp>
#include <iostream>
#include<numeric>
#include "typedefs.h"
#include "settings.h"
#include "spline.h"
#include "dxdt.h"
#include <cmath>
//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
/* HERE WE SHOULD DEFINE THE RHS OF THE ODE SYSTEM*/


bool positionsort ( const tri_xvi&l, const tri_xvi& r)
{ return std::get<0>(l) < std::get<0>(r); }

dxdt::dxdt(dvec_i avg_speeds,
           dvec_i slope_factors,
           dvec_i wave_delays,
           dvec_i track_x_data,
           dvec_i track_diff_data,
           dvec_i track_width_data) :
  m_avg_speeds(avg_speeds),
  m_slope_factors(slope_factors),
  m_track_x_data( track_x_data),
  m_track_diff_data( track_diff_data),
  m_wave_delays(wave_delays),
  cs(track_x_data,track_diff_data),
  cs2(track_x_data,track_width_data)
{
  // Define the number of meters in the track
  int Nmeter= floor(round(track_x_data[track_x_data.size()-1]-track_x_data[0]+1));
  std::cout<<"Track has "<< Nmeter <<" meters"<< std::endl;
  for(size_t meter=0;meter<Nmeter;meter ++){
    m_road_z.push_back(cs(meter));
    m_road_dzdx.push_back(cs.deriv(1,meter));
    m_road_w.push_back(cs2(meter));
  };
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

  int MINN=10; // in this case impact should be p=0.4
  int MAXN=20;

  for (size_t idx=0;idx<x.size();idx++){
    auto frontispeeds = dvec_i();
    if (((idx+MINN)<x.size())&&(std::get<0>(sorted_xvi[idx+MINN])-std::get<0>(sorted_xvi[idx])<4)) {
      densityfactor[std::get<2>(sorted_xvi[idx])]=0.4;
      /////////////////////////////////////////
      for (size_t ids=MINN;ids<MAXN;ids++){
        if (idx+ids>=x.size()) break;
        else if ((std::get<0>(sorted_xvi[idx+ids])-std::get<0>(sorted_xvi[idx]))<4)
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
        dxdt[idx]=(1-p)*(cs.deriv(1,x[idx])*m_slope_factors[idx]+m_avg_speeds[idx])+p*VL[idx];
      }
    else
      dxdt[idx]=0.0;
  }
};

//]
