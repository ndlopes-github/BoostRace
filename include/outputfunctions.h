#pragma once

#include <iostream>
#include <vector>
#include"typedefs.h"



// print to std::cout
void print_times_and_states(dvec_i times,dvec_ij x_vec);
// write to file
void write_times_and_states(dvec_i times,dvec_ij x_vec,std::string filename);
