#include "typedefs.h"
#include "settings.h"
#include "dxdt.h"

//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
/* HERE WE SHOULD DEFINE THE RHS OF THE ODE SYSTEM*/


void dxdt::operator() ( const dvec_i &x , dvec_i &dxdt , const double  t )
{
  for(size_t idx=0;idx<dxdt.size();idx++){
    dxdt[idx]=m_avg_speeds[idx];
  }
};

//]
