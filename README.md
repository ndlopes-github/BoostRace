# BoostRace

A computational model for simulating urban running races, implementing a mathematical framework for analyzing the effects of race configuration, course design, and runner distribution on race performance.

## Publication

This software was used to produce the results presented in:

**"The modelling of urban running races"**  
Authors: Ricardo Enguiça and Nuno D. Lopes  
Published in: *Journal of Mathematics in Industry* (2023)  
DOI: [10.1186/s13362-023-00136-3](https://doi.org/10.1186/s13362-023-00136-3)

The paper presents a comprehensive mathematical model for simulating 10km urban running races with 10,000 participants, analyzing factors such as:
- Wave start configurations and time gaps
- Course design (width variations and elevation profiles)
- Runner density and congestion effects
- Optimal race organization strategies

## Implementation

### Julia Version
`JLRace.ipynb` - An integrated Jupyter notebook with a fully functional standalone Julia version of BoostRace.
(Optimizations in progress)


## Example Outputs

Some post-processing visualization examples:

### A snapshot of the race at time 2000(s)
![Snapshot of the race at 2000s](readme_images/snapshot2000.png?raw=true "Snapshot of the race")

### Histogram for the number of bursts along the race
![Histogram for the number of bursts along the race](readme_images/hist.png?raw=true "Histogram of bursts")
