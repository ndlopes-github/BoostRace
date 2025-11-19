# BoostRace

A computational model for simulating urban running races, implementing a mathematical framework for analyzing the effects of race configuration, course design, and runner distribution on race performance.

## Publication

This software was used to produce the results presented in:

**"The modelling of urban running races"**  
Authors: <br>
 **Ricardo Enguiça**  ORCID: https://orcid.org/0000-0002-3407-7757 <br>
 **Nuno D. Lopes**  ORCID: https://orcid.org/0000-0001-9577-0347 <br>
Published in: ***Journal of Mathematics in Industry*** (August 2023)  
DOI: [10.1186/s13362-023-00136-3](https://doi.org/10.1186/s13362-023-00136-3)

The paper presents a comprehensive mathematical model for simulating 10km urban running races with 10,000 participants, analyzing factors such as:
- Wave start configurations and time gaps
- Course design (width variations and elevation profiles)
- Runner density and congestion effects
- Optimal race organization strategies

## Implementation

### Julia 
`JLRace.ipynb` - An integrated Jupyter notebook with a fully functional standalone Julia version of BoostRace.


## Quick manual

This project includes `JLRace.ipynb`, a self-contained Julia notebook that prepares and runs the BoostRace simulation. Below are the minimal steps to run and explore the model.

Prerequisites
- Julia 1.8 (the notebook was written for Julia 1.8.x).
- The notebook uses common packages such as `Random`, `Distributions`, `CubicSplines`, `Plots`, `LinearAlgebra`, and `Interpolations`. Install them in Julia before running the notebook (for example using the package REPL: `pkg> add Random Distributions CubicSplines Plots Interpolations`).

How to run
1. Open `JLRace.ipynb` with Jupyter (IJulia) or another notebook viewer that supports Julia kernels.
2. Run the cells top-to-bottom. The notebook defines model parameters (race distance, time step, waves, course profile, etc.) in early cells — edit those to change the scenario.
3. The main simulation constructs parameter and course structures, prepares runner lists/waves, and calls the solver (the notebook uses functions equivalent to `RunModel.race()` in the Julia modules).

Key configurable items
- Numerical parameters: `timestep`, `observertimestep`, `observernsteps`, `endtime`.
- Race configuration: `waves` matrix, `gap` and `ldist` control wave timing and starting layout.
- Course profile: `courseauxdata` (distance, elevation, width) — the notebook builds interpolators from this.
- Teams/Exceptions: The notebook shows how to set `team` and `exceptionrunners` for focused reports.

Outputs
- The notebook/Julia modules write results to `./results/` (in the deprecated Julia sandbox code the outputs included `times.jld2`, `allrunners.jld2`, `parameters.jld2`, and `track.jld2`).
- The notebook also contains plotting routines to visualize elevation, width, snapshots and post-processing figures (examples are shown in `readme_images/`).

Tips
- Change only a few parameters at a time and re-run to understand their effects.
- If you get package errors, activate a fresh environment and add the packages used by the notebook.
- For long simulations, consider reducing `nrunners` or observer frequency while experimenting.

Expanded setup and run guide

1) Create and activate a Julia environment

Open a terminal in the project root and (optionally) create a local project environment. This keeps package versions isolated:

```bash
# from the repository root
julia --project=. -e 'import Pkg; Pkg.activate("."); Pkg.instantiate()'
```

If you don't have a `Manifest.toml`, the command above will create and activate the environment. You can add required packages explicitly (below).

2) Install the notebook dependencies

The notebook uses the following Julia packages (listed in `Project.toml`):
- CubicSplines
- Distributions
- Plots
- Interpolations
- Random and LinearAlgebra are part of Julia's standard library

Install them via the package REPL or a one-liner. Example:

```bash
julia --project=. -e 'import Pkg; Pkg.add(["CubicSplines","Distributions","Plots","Interpolations"])'
```

3) Run interactively (recommended)

- Start Jupyter with IJulia (install IJulia if you don't have it) and open `JLRace.ipynb`.
- Execute cells from the top. Early cells set key parameters (race distance, time steps, `waves`, `courseauxdata`, `team`, and `exceptionrunners`). Edit these before running the simulation cells to customise scenarios.

4) Non-interactive / script-based run (deprecated Julia sandbox)

There's a legacy Julia module under `deprecated/JuliaSandbox/julia/` with `RunModel.jl` and `Race.jl` that show how to run the simulation as a script. To run that code from the project root:

```bash
# run Julia with the sandbox as project (if you want to use its Project.toml)
julia -e 'include("deprecated/JuliaSandbox/julia/RunModel.jl")'
```

Note: the notebook implements the same logic inline; prefer `JLRace.ipynb` for exploration and visualization.

5) Outputs and results

- When the model runs it writes result files (in the legacy code these were saved to `./results/` as `times.jld2`, `allrunners.jld2`, `parameters.jld2`, and `track.jld2`).
- The notebook also contains plotting utilities to produce snapshots and histograms — examples are in the `readme_images/` folder.

6) Troubleshooting

- Package/version issues: ensure your Julia version is compatible with the project's `Project.toml` (the file lists `julia = "1.7"` but the notebook targets 1.8 — Julia 1.8.x is recommended). Use `julia --version` to check.
- If plots or displays don't render in Jupyter, verify the IJulia kernel is using the same Julia environment (`using Pkg; Pkg.status()` will show installed packages).
- Long run times: reduce `nrunners` or shorten `endtime` while testing, or increase `timestep`/`observertimestep` to collect fewer samples.


<!--
7) Suggested next steps (optional enhancements)
- Add a `Manifest.toml` to pin working package versions for reproducibility.
- Provide a small example notebook or script that runs a very-small problem (e.g., 100 runners) for quick smoke testing.
- Add a short shell script (`run_example.sh`) that sets up the environment and launches the notebook for new users.
-->


## Example Outputs

Some post-processing visualization examples:

### A snapshot of the race at time 2000(s)
![Snapshot of the race at 2000s](readme_images/snapshot2000.png?raw=true "Snapshot of the race")

### Histogram for the number of bursts along the race
![Histogram for the number of bursts along the race](readme_images/hist.png?raw=true "Histogram of bursts")

# Contributing

We welcome contributions to this project! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request. We appreciate your involvement in making this implementation more robust and accurate.

# License

This project is currently under MIT license. Please refer to the LICENSE file for more information.

# Contact

If you have any questions or inquiries regarding this codebase or the associated paper, please contact: [nuno(dot)lopes(at)isel(dot)pt]