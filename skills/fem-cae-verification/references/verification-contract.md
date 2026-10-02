# Registration fields and checks

Compare: units, E, nu, section radius or dimensions, shear factor, centerline formula and handedness, stress-free shape, root constraints, released tip DOFs, load point and order, NLGEOM, outputs and normalization length.
For this example: circular R=10 mm, pitch=12 mm, turns=2, rw=0.5 mm, E=210000 MPa, nu=0.3, ks=0.9. Root six DOFs fixed, tip six DOFs free. Six independent unit wrench probes. Load reset between steps. Abaqus B31 has explicitly matched transverse shear stiffness and zero slenderness compensation factor. Six U/UR and RF/RM outputs are extracted. Compare both solvers on the same polyline before comparing either against the smooth rod integral.

Reaction: Froot+Ftip=0; Mroot+Mtip+(rtip-rroot) cross Ftip=0. Energy: 2U=f dot q for linear loading. Do not compare raw cross-block eigenvalues of a dimensionally mixed C matrix.
