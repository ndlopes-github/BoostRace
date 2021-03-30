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


  boost::progress_display &m_show_progress;

  observer( dvec_ij &states , dvec_i &times, dvec_ij &vels,dxtd &f, boost::progress_display &show_progress )
    : m_states(states) , m_times(times), m_dxdt(vels),m_show_progress(show_progress) { }
  //Constructor for the m_states and m_times member of the struct

  void operator()( const dvec_i &x , double t)
    {
        m_states.push_back( x );
        m_times.push_back( t );
        m_dxdt.push_back( *(dxdt.velocities_instance));
        ++m_show_progress;
    }
};



// Fixed stept RK4 solver by boost.

std::pair<dvec_i,dvec_ij> ode_system_solver(
                                            dvec_i avg_speeds,
                                            dvec_i slope_factors,
                                            dvec_i wave_delays,
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
  auto times =dvec_i();
  auto vels = dvec_ij();
  auto f= dxdt(avg_speeds,
               slope_factors,
               wave_delays,
               track_x_data,
               track_diff_data,
               track_width_data);


  //boost::numeric::odeint::runge_kutta4< dvec_i > stepper;
  boost::numeric::odeint::adams_bashforth_moulton<2,dvec_i > stepper;
  std::cout<< "adams_bashforth_moulton of order "<< stepper.order() <<std::endl;

  boost::progress_display show_progress(end_time);

  size_t steps = boost::numeric::odeint::integrate_const(stepper , f , init_states ,
                                                         start_time,
                                                         end_time,
                                                         time_step,
                                                         observer(x_vec,times,
                                                                  vels,
                                                                  f,
                                                                  show_progress));


  // std::function<void(const dvec_ij &, double)> observer =
  //   [&x_vec, &times, &show_progress](const dvec_i &x, double t) {
  //     x_vec.push_back(x);
  //     times.push_back(t);
  //     ++show_progress;
  //     //res_rho.push_back(*(rhs_class.rho_binned));
  //     //res_vel.push_back(*(rhs_class.velocity));
  //     //if (t >= last_printed + 60 - 1e-13) {
  //     //    cout << "t=" << t << endl;
  //     //    last_printed = t;
  //           //}
  //   };

  // size_t steps = boost::numeric::odeint::integrate_const(stepper , f , init_states ,
  //                                                        start_time,
  //                                                        end_time,
  //                                                        time_step,
  //                                                        observer);


  // for( double t=0.0 ; t<end_time; t+= time_step )
  //   stepper.do_step( f , init_states, t, time_step, observer(x_vec,times, show_progress));

  std::cout <<"Ending ode_system_solver. Elapsed time: ";


  return std::make_pair(times,x_vec);
};
