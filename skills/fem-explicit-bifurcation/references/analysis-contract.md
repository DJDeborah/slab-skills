# Analysis contract

Choose the question first:

| Question | Appropriate evidence |
|---|---|
| Is the model registered and numerically sound? | units/DOFs/BCs, completed job, balance, convergence |
| Does a force drop or rapid opening occur? | resolved dynamic time histories and event definitions |
| Where does an equilibrium branch lose local stability? | equilibrium residual, feasible constrained tangent, tracked mode |
| Is the point a fold or branch bifurcation? | branch continuation, transversality/higher-order analysis as appropriate |
| What configuration is reached after snap? | dynamics, loading protocol, damping/contact, landing evidence |

The default N-mm-tonne-s system uses E in N/mm² and density in tonne/mm³. There is no built-in Abaqus unit system. Steel density 7.85e-9 tonne/mm³ is an example, not a material recommendation. For other units change every dimensional quantity together.

`prepare_explicit.py` generates only a straight, linearly elastic planar B21 cantilever with displacement control. It rejects unsupported topology, material and unit choices rather than silently emitting a plausible deck. It does not add mass scaling. Geometry and node count are configurable. Small-deformation Euler–Bernoulli reaction is a smoke reference, not an exact solution to the nonlinear dynamic FE model.

Energy ratios: meaningful IE is above `internal_energy_floor_fraction` times the peak IE. Audit only `window_fraction` of the duration, and report masked points. The ratios and reaction tolerance are configurable smoke criteria; passing them is insufficient for a quasi-static buckling study. Test duration and mesh sensitivity on the event displacement, path and landing of interest. Preserve high-KE transition windows separately. ALLAE/ALLIE is a discretization diagnostic, not universally a strict acceptance threshold.

Official references: [Abaqus quasi-static Explicit](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEGSARefMap/simagsa-m-Quasi-sb.htm), [unstable collapse and Riks](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEANLRefMap/simaanl-c-postbuckling.htm). The former explains why inertia must be checked; the latter explains load-displacement continuation and its restrictions. Neither turns a force drop into a bifurcation certificate.
