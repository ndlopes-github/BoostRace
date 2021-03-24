#include <pybind11/pybind11.h>
//#include <pybind11/numpy.h>
#include <pybind11/stl.h> //for vector tuple...conversion
#include "odesolvers.h"

namespace py=pybind11;

PYBIND11_MODULE(odesolvers,m) {
  m.def("rk4_ode_system_solver", &rk4_ode_system_solver,
        "Runge-Kutta rk4_ode_system_solver(avg_speeds,init_states,start_time,end_time,time_step) algorithm",
        py::arg("avg_speeds"),
        py::arg("init_states"),
        py::arg("start_time"),
        py::arg("end_time"),
        py::arg("time_step"));
}
