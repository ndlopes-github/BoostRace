#include <pybind11/pybind11.h>
//#include <pybind11/numpy.h>
#include <pybind11/stl.h> //for vector tuple...conversion
#include "odesolvers.h"

namespace py=pybind11;

PYBIND11_MODULE(odesolvers,m) {
  m.def("ode_system_solver", &ode_system_solver,
        "ode_system_solver(avg_speeds, init_states, start_time, end_time, time_step,linear_view,min_ratio.... ) algorithm",
        py::arg("avg_speeds"),
        py::arg("slope_factors"),
        py::arg("wave_delays"),
        py::arg("wave_init_speeds"),
        py::arg("track_x_data"),
        py::arg("track_diff_data"),
        py::arg("track_width_data"),
        py::arg("init_states"),
        py::arg("start_time"),
        py::arg("end_time"),
        py::arg("time_step"),
        py::arg("linear_view"),
        py::arg("min_ratio"),
        py::arg("max_ratio"),
        py::arg("min_rho"),
        py::arg("max_rho"),
        py::arg("stepper_switch"));
}
