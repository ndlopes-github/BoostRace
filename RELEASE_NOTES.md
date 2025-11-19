# BoostRace Release v0.3.0

Release date: 2025-11-19

## Release title
v0.3.0 — Notebook-driven Julia BoostRace with expanded manual

## Summary
This release focuses on documentation improvements to make the project easier to set up and run. The core simulation code was not changed.

What’s included
- Expanded `README.md` manual with detailed setup and run instructions for `JLRace.ipynb` (recommended Julia 1.8.x).
- Clear package installation guidance (packages: CubicSplines, Distributions, Plots, Interpolations; Random and LinearAlgebra are part of the standard library).
- Interactive (IJulia) and legacy script-based run examples (the latter under `deprecated/JuliaSandbox/julia/`).
- Outputs and troubleshooting guidance added to the README.
- Minor editorial housekeeping: clarified plotting utilities and where outputs are saved. A short list of suggested enhancements was preserved in the README but commented out to keep the rendered page concise.

## Breaking changes
None — documentation-only release.

## Verification / How to test
1. Create and activate the project environment (from repo root):

```bash
julia --project=. -e 'import Pkg; Pkg.activate("."); Pkg.instantiate()'
```

2. Install the required packages (if not present):

```bash
julia --project=. -e 'import Pkg; Pkg.add(["CubicSplines","Distributions","Plots","Interpolations"])'
```

3. Start Jupyter with the IJulia kernel and open `JLRace.ipynb`. Run the cells from top to bottom and verify that the plotting cells produce output and no import errors occur.

4. (Optional) Run the legacy script example to smoke-test non-interactive execution:

```bash
julia -e 'include("deprecated/JuliaSandbox/julia/RunModel.jl")'
```

## Suggested tag
`v0.3.0`

## Suggested Git commands to create a release tag and push

```bash
# create annotated tag
git tag -a v0.3.0 -m "v0.3.0 — Notebook-driven Julia BoostRace with expanded manual"
# push tag to origin
git push origin v0.3.0
```

## Next steps
- Add a small example notebook (100 runners) for quick smoke tests.
- Add a `run_example.sh` wrapper to simplify onboarding for new users.
- Consider committing a `Manifest.toml` to pin dependencies for reproducibility.

---

Authors: Ricardo Enguiça and Nuno D. Lopes

Reference: "The modelling of urban running races" (Journal of Mathematics in Industry, 2023)