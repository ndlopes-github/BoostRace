/*
 Copyright 2010-2012 Karsten Ahnert
 Copyright 2011-2013 Mario Mulansky
 Copyright 2013 Pascal Germroth

 Distributed under the Boost Software License, Version 1.0.
 (See accompanying file LICENSE_1_0.txt or
 copy at http://www.boost.org/LICENSE_1_0.txt)

 // paper for the boost ode integrators

 https://arxiv.org/pdf/1110.3397.pdf
 */


#include <iostream>
#include <vector>
#include <boost/numeric/odeint.hpp>
#include "typedefs.h"
#include "outputfunctions.h"
#include "settings.h"


//[ rhs_class
/* The rhs of x' = f(x) defined as a class */
class speedFunc {

  dvec_i m_avg_speeds;

public:
  speedFunc( dvec_i avg_speeds ) : m_avg_speeds(avg_speeds) { }

    void operator() ( const dvec_i &x , dvec_i &dxdt , const double /* t */ )
    {
        dxdt[0] = m_avg_speeds[0];
        dxdt[1] = m_avg_speeds[1];
    }
};
//]






int main(int /* argc */ , char** /* argv */ )
{

    //[ state_initialization with 0.0
  dvec_i x(race::NumberOfRunners,0.0);
  x[0] = 1.0; // start at x=1.0, p=0.0
  x[1] = 0.0;
    //]


    // //[ integration
    // size_t steps = integrate( harmonic_oscillator ,
    //         x , 0.0 , 10.0 , 0.1 );
    //]



    //[ integration_class
    dvec_i avg_speeds{1,1.2};
    speedFunc sp(avg_speeds);
    //]


    //[ integrate_observ
    std::vector<dvec_i> x_vec;
    dvec_i times;


    //[ define_const_stepper
    boost::numeric::odeint::runge_kutta4< dvec_i > stepper;
    size_t steps = boost::numeric::odeint::integrate_const( stepper , sp , x ,
                                                            race::StartTime,
                                                            race::TotalTime ,
                                                            race::dt,
                                                            observer( x_vec , times ));

    //]

    write_times_and_states(times, x_vec, "times_and_states.bin");
    print_times_and_states(times, x_vec);


    return 0;
}
