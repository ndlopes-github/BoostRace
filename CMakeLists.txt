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

set(PROJECT_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/")
set(PROJECT_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include/")


#ALL THE CPP FILES SHOULD BE LISTED HERE
add_library(${PROJECT_NAME} STATIC
    src/outputfunctions.cpp
    src/odesolvers.cpp
    src/dxdt.cpp)

#DIR FOR THE HEADER FILES
include_directories(include/)

set(sources ${sources}
    ${PROJECT_SRC_DIR}/main.cpp)

# TESTING EXECUTABLE
add_executable(race ${sources})
target_link_libraries(race ${PROJECT_NAME}) #LINK WITH THE LIBRARIES AND HEADERS
set_target_properties(race PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED ON)


#find_package(Python COMPONENTS Interpreter Development REQUIRED)
#if(APPLE)
#find_package(pybind11 CONFIG REQUIRED)
#else()
#IF ON UBUNTU
# AFTER CLONING PYBIND11 TO THE WORKING DIR
# THIS SOLVES LINKAGE ISSUES WITH PYBIND11
#add_subdirectory(pybind11)
#endif()


#set(pysources src/outputfunctions.cpp
#    src/odesolvers.cpp
#    src/dxdt.cpp
#    src/outputfunctions.cpp
#    src/odesolvers.cpp
#)

#pybind11_add_module(odesolvers  ${pysources})
#target_link_libraries(odesolvers PRIVATE ${PROJECT_NAME})
#set_target_properties(odesolvers PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED ON)
#target_include_directories(odesolvers PRIVATE pybind11::embed ${PROJECT_INCLUDE_DIR})

message("Do not forget to run the command:")
message("$source env_config.source" )
