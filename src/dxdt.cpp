//#include <boost/sort/spreadsort/spreadsort.hpp>
#include<numeric>
#include "typedefs.h"
#include "settings.h"
#include "spline.h"
#include "dxdt.h"
//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
/* HERE WE SHOULD DEFINE THE RHS OF THE ODE SYSTEM*/


//double slope


bool positionsort ( const tri_xvi& l, const tri_xvi& r)
{ return std::get<0>(l) < std::get<0>(r); }



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
