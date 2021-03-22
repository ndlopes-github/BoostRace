#pragma once

#include <vector>
#include <boost/numeric/odeint.hpp>
#include "typedefs.h"






std::pair<dvec_i,dvec_ij> rk4_ode_system_solver(dxdt f, dvec_i init_states,
                                                double start_time,
                                                double end_time,
                                                double time_step);
