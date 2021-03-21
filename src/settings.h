#pragma once

namespace race{

  // Number of Runners in the Race
  const int NumberOfRunners=2;

  // Number of Waves
  const int NumberOfWaves=3;

  // RK4 parameters

  // Number of Steps
  const int NumberOfSteps=5;

  // time step
  const double dt=1.0;

  // Max simulation Time;
  const double TotalTime=NumberOfSteps*dt;

  // Starting Time
  const double StartTime=0.0;


}
