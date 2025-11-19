#pragma once

#include "typedefs.h"
#include "spline.h"
#include <memory>

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
  dvec_i m_wave_init_speeds;
  //std::shared_ptr<dvec_i> road_begin;
  int road_start;
  int road_end;
  int m_linear_view; //linear impact zone for velocity perturbation, maybe passed as arg
  double m_min_ratio;
  double m_max_ratio;
  double m_min_rho;
  double m_max_rho;
  // dvec_i m_road_z; // not required for now
  //dvec_i m_road_dzdx; // not required for now
  //int m_road_dzdx[10701];
  dvec_i m_road_w;
  dvec_i m_foresight_area;

  //  dvec_i m_departure_times;  //to hold the times for departure for each runner

  tk::spline cs;
  tk::spline cs2;

public:
  std::shared_ptr<dvec_i> velocities_instance;
  std::shared_ptr<dvec_i> rhos_instance;


  dxdt(dvec_i avg_speeds,
       dvec_i slope_factors,
       dvec_i wave_delays,
       dvec_i wave_init_speeds,
       dvec_i track_x_data,
       dvec_i track_diff_data,
       dvec_i track_width_data,
       double linear_view,
       double min_ratio,
       double max_ratio,
       double min_rho,
       double max_rho);


  void operator() ( const dvec_i &x /*state*/ , dvec_i &dxdt , const double  t );
};
