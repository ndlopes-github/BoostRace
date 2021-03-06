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
#include "typedefs.h"
#include "outputfunctions.h"
#include "settings.h"
#include "odesolvers.h"


/* THIS MAIN FILE WORKS ONLY Unit test for solvers */


int main(int /* argc */ , char** /* argv */ )
{

  std::cout<<"WARNING: MAIN.CPP IS ONLY FOR TESTING THE SOLVERS"<<std::endl;

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
    dvec_i slope_factors{0,0};
    dvec_i wave_delays{0,0};
    dvec_i track_x_data{0,1};
    dvec_i track_diff_data{0,0};
    dvec_i track_width_data{10,10};
    //]



    std::tuple<dvec_i,dvec_ij,dvec_ij> t_and_x=ode_system_solver(
                                                        avg_speeds,
                                                        slope_factors,
                                                        wave_delays,
                                                        track_x_data,
                                                        track_diff_data,
                                                        track_width_data,
                                                        x,
                                                        race::StartTime,
                                                        race::TotalTime,
                                                        race::dt);

    //]
    dvec_i times=std::get<0>(t_and_x);
    dvec_ij states=std::get<1>(t_and_x);
    write_times_and_states(times, states, "times_and_states.bin");
    print_times_and_states(times, states);


    return 0;
}
