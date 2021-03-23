#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "odesolvers.h"

namespace py=pybind11;

PYBIND11_MODULE(odesolvers,m) {
  m.def("rk4_ode_system_solver", &rk4_ode_system_solver,
        "Runge-Kutta rk4_ode_system_solver(f,init_states,start_time,end_time,time_step) algorithm");
}
