#include <pybind11/pybind11.h>
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
#include <vector>
#include <boost/numeric/odeint.hpp>
#include "typedefs.h"
#include "dxdt.h"

using namespace pybind11;

struct observer
{
  dvec_ij & m_states;
  dvec_i& m_times;

  observer( std::vector< dvec_i > &states , dvec_i &times )
    : m_states(states) , m_times(times) { } //Constructor for the m_states and m_times member of the strut

  void operator()( const dvec_i &x , double t )
    {
        m_states.push_back( x );
        m_times.push_back( t );
    }
};




// Fixed stept RK4 solver by boost.

std::pair<dvec_i,dvec_ij> rk4_ode_system_solver(dxdt f, dvec_i init_states,
                                                double start_time,
                                                double end_time,
                                                double time_step){
  //[ integrate_observ
  std::vector<dvec_i> x_vec;
  dvec_i times;

  boost::numeric::odeint::runge_kutta4< dvec_i > stepper;
  size_t steps = boost::numeric::odeint::integrate_const(stepper , f , init_states ,
                                                         start_time,
                                                         end_time,
                                                         time_step,
                                                         observer(x_vec,times));
  return std::make_pair(times,x_vec);
};




PYBIND11_MODULE(odesolvers,m) {
  m.def("rk4_ode_system_solver", &rk4_ode_system_solver,
        "Runge-Kutta rk4_ode_system_solver(f,init_states,start_time,end_time,time_step) algorithm");
}
