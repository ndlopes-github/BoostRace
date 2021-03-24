#pragma once
#include <vector>
#include "typedefs.h"
#include "dxdt.h"




// Runge-Kutta fourth order. Constant time_step
std::pair<dvec_i,dvec_ij> rk4_ode_system_solver(dvec_i avg_speeds,
                                                dvec_i init_states,
                                                double start_time,
                                                double end_time,
                                                double time_step);
