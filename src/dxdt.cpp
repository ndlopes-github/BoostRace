#include "typedefs.h"
#include "settings.h"
#include "dxdt.h"

//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
/* HERE WE SHOULD DEFINE THE RHS OF THE ODE SYSTEM*/


//double slope


void dxdt::operator() ( const dvec_i &x , dvec_i &dxdt , const double  t )
{


  //  auto sortedpositions = dvec_i(x);



  for(size_t idx=0;idx<dxdt.size();idx++){
    if (t>m_wave_delays[idx])
      dxdt[idx]=m_avg_speeds[idx]+cs.deriv(1,x[idx])*m_slope_factors[idx];
    else
      dxdt[idx]=0.0;
  }
};

//]
