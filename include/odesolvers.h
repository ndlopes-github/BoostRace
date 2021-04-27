#pragma once
#include <vector>
#include "typedefs.h"
#include "dxdt.h"




// Runge-Kutta fourth order. Constant time_step
std::tuple<dvec_i,dvec_ij,dvec_ij,dvec_ij> ode_system_solver(
                                            dvec_i avg_speeds,
                                            dvec_i slopes_factors,
                                            dvec_i wave_delays,
                                            dvec_i wave_init_speeds,
                                            dvec_i track_x_data,
                                            dvec_i track_diff_data,
                                            dvec_i track_width_data,
                                            dvec_i init_states,
                                            int observer_number_steps,
                                            double observer_time_step,
                                            double time_step,
                                            double linear_view,
                                            double min_ratio,
                                            double max_ratio,
                                            double min_rho,
                                            double max_rho,
                                            int stepper_switch);
