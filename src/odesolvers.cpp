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
                                            int observer_number_steps,
                                            double observer_time_step,
                                            double time_step,
                                            double linear_view,
                                            double min_ratio,
                                            double max_ratio,
                                            double min_rho,
                                            double max_rho,
                                            int stepper_switch){

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
               track_width_data,
               linear_view,
               min_ratio,
               max_ratio,
               min_rho,
               max_rho);

  auto stepper2 =  boost::numeric::odeint::adams_bashforth_moulton<2,dvec_i >{};
  auto stepper3 =  boost::numeric::odeint::adams_bashforth_moulton<3,dvec_i >{};
  auto stepper4 =  boost::numeric::odeint::adams_bashforth_moulton<4,dvec_i >{};
  auto stepper5 =  boost::numeric::odeint::adams_bashforth_moulton<5,dvec_i >{};

  // Variable time step solver
  typedef  boost::numeric::odeint::runge_kutta_dopri5< dvec_i > stepper_type;
  auto stepper6 = boost::numeric::odeint::make_controlled( 1.0e-1, 1.0e-3 , stepper_type());


  boost::progress_display show_progress(observer_number_steps);

  // Observer times
  std::vector<double> observer_times(observer_number_steps+1);
  for (size_t  i=0; i<observer_times.size();i++)
    {observer_times[i]=observer_time_step*i;}

  size_t steps=0;
  switch (stepper_switch)
    {
    case 2:
      steps = boost::numeric::odeint::integrate_times(stepper2, f , init_states ,
                                                      observer_times,
                                                      time_step,
                                                      observer(x_vec,times,
                                                               vels,
                                                               rhos,
                                                               f,
                                                               show_progress));
      break;

    case 3:
      steps = boost::numeric::odeint::integrate_times(stepper3, f , init_states ,
                                                      observer_times,
                                                      time_step,
                                                      observer(x_vec,times,
                                                               vels,
                                                               rhos,
                                                               f,
                                                               show_progress));
      break;


    case 4:
      steps = boost::numeric::odeint::integrate_times(stepper4, f , init_states ,
                                                      observer_times,
                                                      time_step,
                                                      observer(x_vec,times,
                                                               vels,
                                                               rhos,
                                                               f,
                                                               show_progress));
      break;

    case 5:
      steps = boost::numeric::odeint::integrate_times(stepper5, f , init_states ,
                                                      observer_times,
                                                      time_step,
                                                      observer(x_vec,times,
                                                               vels,
                                                               rhos,
                                                               f,
                                                               show_progress));
      break;

    case 6:
      steps = boost::numeric::odeint::integrate_times(stepper6, f , init_states ,
                                                      observer_times,
                                                      time_step,
                                                      observer(x_vec,times,
                                                               vels,
                                                               rhos,
                                                               f,
                                                               show_progress));
      break;
    }

  std::cout <<"Ending ode_system_solver. Elapsed time: ";


  return std::make_tuple(times,x_vec,vels,rhos);
};
