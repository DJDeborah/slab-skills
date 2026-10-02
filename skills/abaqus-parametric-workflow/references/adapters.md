# Adapter extension

The shipped model is a straight elastic planar B21 beam with one clamped end and a smooth prescribed tip displacement. This is a numerical teaching study, not a recovered publication-specific specimen.

For a new model implement equivalent stages: validate parameter schema → build geometry/mesh → resolve named regions and DOFs → emit solver input and registration → extract actual outputs → audit scope-appropriate quantities. Preserve case/config/input hashes and execution state. Add a small licensed smoke case and an informative failure control.

Extend geometry/material/contact/topology only together with its outputs and verification. If a parameter changes the topology, case ID and mapping must reflect it. For a meshed beam family record element formulation, section director and reference centerline. For a nonlinear branch study add equilibrium residual, feasible tangent/mode extraction and continuation; the sweep driver supplies orchestration, not those mathematical capabilities.

The helpers are Python 3.10+ standard library. ODB extraction runs under Abaqus Python (tested on 2.7.3/R2019x); portable Python does not import `odbAccess`. Solver commands use explicit arguments and a resolved launcher. The built-in serial queue limits license consumption; multi-machine schedulers need another adapter.
