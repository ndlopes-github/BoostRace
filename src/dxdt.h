#pragma once

#include <iostream>
#include "typedefs.h"
#include "settings.h"

//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
class dxdt {

  dvec_i m_avg_speeds;

public:
  dxdt( dvec_i avg_speeds ) : m_avg_speeds(avg_speeds) { }

    void operator() ( const dvec_i &x , dvec_i &dxdt , const double  t )
    {
      dxdt[0] = m_avg_speeds[0]/(1+t);
      dxdt[1] = m_avg_speeds[1]/(1+t);
    }
};
//]
