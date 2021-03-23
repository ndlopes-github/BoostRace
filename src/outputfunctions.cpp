#include <iostream>
#include <fstream>
#include <vector>
#include"typedefs.h"
//write_times_and_states(times, x_vec);


void print_times_and_states(dvec_i times,dvec_ij x_vec){
  /* output :
     First line contains the times
     each subsequente line contains the positions at each time of each x */

  for(size_t i=0; i<x_vec.size();i++){
    std::cout << times[i] << '\t';
    for(size_t j=0;j<x_vec[i].size();j++ )
      std::cout<< x_vec[i][j]<<"\t";
    std::cout<<std::endl;
  }

}


void write_times_and_states(dvec_i times,dvec_ij x_vec,std::string filename){
  /* output :
     First line contains the times
     each subsequente line contains the positions at each time of each x */

  std::ofstream myfile;
  myfile.open(filename,std::ios::out | std::ios::binary);

  for(size_t i=0; i<x_vec.size();i++){
    myfile<< times[i]<<"\t";
    for(size_t j=0;j<x_vec[i].size();j++ )
      myfile<< x_vec[i][j]<<"\t";
    myfile<<std::endl;
  }

}
