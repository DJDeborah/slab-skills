# Fast benchmark choices

For ideal straight slender beams with linear elastic material, Euler pinned–pinned buckling provides Pcrit = pi^2 EI/L^2; cantilever and clamped–clamped boundaries change the effective length. An Euler benchmark verifies implementation, not contact-rich slit snapping, shell imperfection sensitivity, or finite landing states. Refine at least three meshes tracking a named quantity. Check the mode and eigenproblem residual as well as the load.

For a robot controller, use multiple declared initial states/seeds, an uncontrolled or simple-controller baseline, time-step refinement, saturation/contact diagnostics, and an observable task metric. Ground-truth state feedback is not camera perception. A pendulum or arm smoke test does not validate a humanoid policy, VLA, sim-to-real, or hardware behavior.

For metamaterial comparisons, match density, material law, cell scale, boundary convention and deformation regime. Cauchy C and micropolar Q are different objects. Fix DOF ordering, engineering-versus-tensor shear and curvature scaling before comparing entries. Repetition of a supercell is not by itself a novel infinite periodic material. Check energy, reaction and symmetry consistency, then a finite specimen or independent formulation as needed.
