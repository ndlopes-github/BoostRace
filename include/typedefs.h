#pragma once

#include <vector>
#include <tuple>

/* The type of container used to hold the state vector */
typedef std::vector<double> dvec_i; // vector of doubles //state_type

typedef std::vector<dvec_i> dvec_ij; // vector of vectores of doubles (matrix)

typedef std::vector<int> ivec_i; // vector of ints

typedef std::vector<ivec_i> ivec_ij; // vector of ints

typedef std::tuple<double,double,int> tri_xvi; // Triade with positions, velocity, index
