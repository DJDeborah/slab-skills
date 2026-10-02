# Stability, events and contact

For a conservative smooth constrained equilibrium, project the correct Lagrangian Hessian onto admissible perturbations. Define the metric before comparing normalized eigenvalues. Constrained systems include constraint curvature terms; simply deleting constrained rows from an unconstrained Hessian may be incorrect.

A negative feasible second variation establishes local energetic instability under the assumed system. A zero minimum eigenvalue requires higher-order/branch analysis. The sign of an absolute potential-energy value is irrelevant. A lower-energy distant state does not by itself establish reachable landing. Follower/nonconservative loading, damping and dynamic stability need a different operator/criterion.

Unilateral contact: register gaps, multipliers, complementarity and active set. Distinguish first release, a fold on the post-release equilibrium branch, subsequent opening and finite dynamic jump. Contact-feasible one-sided directions can differ from smooth equality-constraint tangent directions. The beam example has no contact and does not verify these assertions for a specimen.

`branch_benchmarks.py` supplies two exact scalar normal forms:

- Fold potential Π(q,λ)=q³/3−λq: equilibrium q²−λ=0, tangent 2q; q>0 is locally stable and q<0 unstable. q=0 is the fold; this normal form is not globally bounded below.
- Supercritical pitchfork Π(q,λ)=q⁴/4−λq²/2: equilibrium q³−λq=0. Central branch tangent −λ; side branches q=±√λ have tangent 2λ. At λ=0 a vanishing tangent alone does not show a finite jump.

The script samples these known branches and checks exact residual/tangent signs. It is an oracle for a future continuation adapter, not a branch-discovery algorithm. Use the actual FE equilibrium branch before interpreting its eigenvalue.
