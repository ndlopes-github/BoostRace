#include <vector>
#include <boost/numeric/odeint.hpp>
//#include <boost/timer/timer.hpp> //updated but not working
#include <boost/progress.hpp> //deprecated but working
#include "typedefs.h"
#include "dxdt.h"



struct observer
{
  dvec_ij &m_states;
  dvec_i &m_times;
  boost::progress_display &m_show_progress;

  observer( dvec_ij &states , dvec_i &times,boost::progress_display &show_progress )
    : m_states(states) , m_times(times), m_show_progress(show_progress) { }
  //Constructor for the m_states and m_times member of the struct

  void operator()( const dvec_i &x , double t)
    {
        m_states.push_back( x );
        m_times.push_back( t );
        ++m_show_progress;
    }
};




// Fixed stept RK4 solver by boost.

std::pair<dvec_i,dvec_ij> rk4_ode_system_solver(
                                                dvec_i avg_speeds,
                                                dvec_i slope_factors,
                                                dvec_i track_x_data,
                                                dvec_i track_diff_data,
                                                dvec_i init_states,
                                                double start_time,
                                                double end_time,
                                                double time_step){

  // Timer
  // boost::timer::auto_cpu_timer t;
  boost::progress_timer t;
  std::cout <<" Starting rk4_ode_system_solver." << std::endl;;

  //[ integrate_observ
  dvec_ij x_vec; //container for the solutions
  dvec_i times;

  dxdt f(avg_speeds,
         slope_factors,
         track_x_data,
         track_diff_data);

  boost::progress_display show_progress(end_time);

  boost::numeric::odeint::runge_kutta4< dvec_i > stepper;
  size_t steps = boost::numeric::odeint::integrate_const(stepper , f , init_states ,
                                                         start_time,
                                                         end_time,
                                                         time_step,
                                                         observer(x_vec,times,show_progress));

  std::cout <<"Ending rk4_ode_system_solver. Elapsed time: ";


  return std::make_pair(times,x_vec);
};
