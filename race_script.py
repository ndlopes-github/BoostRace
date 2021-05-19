#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-


import os

def run_free( ):
    os.system('cmake -DUSE_DEBUG=ON CMakeLists.txt')
    os.system('make -j8')
    os.system('mkdir results')
    os.system('python3.9 ./python/race.py')
    os.system('mv results results_free')

def run_normal( ):
    os.system('cmake -DUSE_DEBUG=OFF CMakeLists.txt')
    os.system('make -j8')
    os.system('mkdir results')
    os.system('python3.9 ./python/race.py')

def reports():
    os.system('python3.9 ./python/viewtimes.py')

run_free()
run_normal()
reports()

# Free race
#1 cmake -DUSE_DEBUG=ON CMakeLists.txt

#2 make -j8

#3 race

# 4 results to results_free

# Normal race
#5 cmake -DUSE_DEBUG=OFF CMakeLists.txt

# 6 make -j8

# 7 race

# 8 Save report and images
