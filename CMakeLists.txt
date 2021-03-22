cmake_minimum_required(VERSION 3.19)
project(boostrace LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ version selection")  # or 11, 14, 17, 20
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # optional, ensure standard is supported
set(CMAKE_CXX_EXTENSIONS OFF)  # optional, keep compiler extensionsn off
add_compile_options(-O3 -march=native)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules/")



# Set the output folder where your program will be created
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/build)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/build)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

find_package(Boost REQUIRED)
IF (Boost_FOUND)
    INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
    ADD_DEFINITIONS( "-DHAS_BOOST" )
ENDIF()
find_package(Python COMPONENTS Interpreter Development REQUIRED)

set(PROJECT_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/")


set(sources ${sources}
    ${PROJECT_SRC_DIR}/odeint.cpp
    ${PROJECT_SRC_DIR}/outputfunctions.cpp
    ${PROJECT_SRC_DIR}/odesolvers.cpp
)

add_executable(race ${sources})


#if(APPLE)
#find_package(pybind11 CONFIG REQUIRED)
#else()
#IF ON UBUNTU
# AFTER CLONING PYBIND11 TO THE WORKING DIR
# THIS SOLVES LINKAGE ISSUES WITH PYBIND11
#add_subdirectory(pybind11)
#endif()

#pybind11_add_module(speedscpp  ${PROJECT_SRC_DIR}/speeds.cpp)

#message("Do not forget to run the command:")
#message("$source race.source" )
