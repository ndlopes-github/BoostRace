#include <vector>
#include <boost/numeric/odeint.hpp>
//#include <boost/timer/timer.hpp> //updated but not working
#include <boost/progress.hpp> //deprecated but working
#include "typedefs.h"
#include "dxdt.h"
//#include <functional>


struct observer
{
  dvec_ij &m_states;
  dvec_i &m_times;
  dvec_ij &m_dxdt;
  dvec_ij &m_rho;
  dxdt &m_f; // object from dxdt class to track


  boost::progress_display &m_show_progress;

  observer( dvec_ij &states , dvec_i &times,
            dvec_ij &vels,
            dvec_ij &rho,
            dxdt &f,
            boost::progress_display &show_progress )
    : m_states(states) , m_times(times),
      m_dxdt(vels),
      m_rho(rho),
      m_f(f),
      m_show_progress(show_progress) { }
  //Constructor for the m_states and m_times member of the struct

  void operator()( const dvec_i &x , double t)
    {
        m_states.push_back( x );
        m_times.push_back( t );
        m_dxdt.push_back(*(m_f.velocities_instance));
        m_rho.push_back(*(m_f.rhos_instance));
        ++m_show_progress;
    }
};



// Fixed stept RK4 solver by boost.

std::tuple<dvec_i,dvec_ij,dvec_ij,dvec_ij> ode_system_solver(
                                            dvec_i avg_speeds,
                                            dvec_i slope_factors,
                                            dvec_i wave_delays,
                                            dvec_i wave_init_speeds,
                                            dvec_i track_x_data,
                                            dvec_i track_diff_data,
                                            dvec_i track_width_data,
                                            dvec_i init_states,
                                            double start_time,
                                            double end_time,
                                            double time_step){

  // Timer
  boost::progress_timer t;
  // boost::timer::auto_cpu_timer t;
  std::cout <<" Starting ode_system_solver." << std::endl;

  //[ integrate_observ
  auto x_vec = dvec_ij() ; //container for the solutions
  auto times =dvec_i();    // contanier for the times
  auto vels = dvec_ij();   // container for the velocities
  auto rhos = dvec_ij();   // container for the rhos

  auto f= dxdt(avg_speeds,
               slope_factors,
               wave_delays,
               wave_init_speeds,
               track_x_data,
               track_diff_data,
               track_width_data);


  //boost::numeric::odeint::runge_kutta4< dvec_i > stepper;
  boost::numeric::odeint::adams_bashforth_moulton<2,dvec_i > stepper;
  std::cout<< "adams_bashforth_moulton of order "<< stepper.order() <<std::endl;

  boost::progress_display show_progress(end_time);
  ## check how to use integrate_times
  ## https://fossies.org/linux/boost/libs/numeric/odeint/examples/integrate_times.cpp
  size_t steps = boost::numeric::odeint::integrate_const(stepper , f , init_states ,
                                                         start_time,
                                                         end_time,
                                                         time_step,
                                                         observer(x_vec,times,
                                                                  vels,
                                                                  rhos,
                                                                  f,
                                                                  show_progress));




  // for( double t=0.0 ; t<end_time; t+= time_step )
  //   stepper.do_step( f , init_states, t, time_step, observer(x_vec,times, show_progress));

  std::cout <<"Ending ode_system_solver. Elapsed time: ";


  return std::make_tuple(times,x_vec,vels,rhos);
};
