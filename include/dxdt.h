#pragma once

#include "typedefs.h"
#include "spline.h"

//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
/* HERE WE SHOULD DEFINE THE RHS OF THE ODE SYSTEM*/


//double slope


class dxdt{
  dvec_i m_avg_speeds;
  dvec_i m_slope_factors;
  dvec_i m_track_x_data;
  dvec_i m_track_diff_data;
  dvec_i m_wave_delays;
  tk::spline cs;

public:

  dxdt(dvec_i avg_speeds,
       dvec_i slope_factors,
       dvec_i wave_delays,
       dvec_i track_x_data,
       dvec_i track_diff_data) :
    m_avg_speeds(avg_speeds),
    m_slope_factors(slope_factors),
    m_wave_delays(wave_delays),
    m_track_x_data( track_x_data),
    m_track_diff_data( track_diff_data),
    cs(track_x_data,track_diff_data)
  {/*One can operate here*/ }


  void operator() ( const dvec_i &x /*state*/ , dvec_i &dxdt , const double  t );
};
