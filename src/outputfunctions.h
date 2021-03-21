#pragma once

#include <iostream>
#include <vector>
#include"typedefs.h"



// print to std::cout
void print_times_and_states(dvec_i times,dvec_ij x_vec);
// write to file
void write_times_and_states(dvec_i times,dvec_ij x_vec,std::string filename);


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
