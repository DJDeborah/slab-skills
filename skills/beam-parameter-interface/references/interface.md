# Interface and model contract

The standalone interface is a newly generalized sharing example, inspired by earlier parameter studies and interactive beam/angle views. It is not presented as a recovered historical GUI. It needs only a modern browser; no cloud service, third-party CDN or solver license.

Units: N-mm-tonne-s. Rectangular section I=width×thickness³/12. Cantilever reaction under prescribed tip displacement δ: F=3EIδ/L³. Analytical displacement v(x)=δx²(3L−x)/(2L³). Maximum small-deflection bending stress magnitude is 6|F|L/(width×thickness²). Plot magnification is explicitly labeled and never changes the exported physical δ.

Config fields agree with the planar B21 adapter: named ROOT/TIP boxes, ROOT DOFs [1,2,6] fixed, TIP U2 smooth ramp, linear elastic E/ν/density, duration, mesh count and quality settings. Shape preview is analytical. Export records actual physical parameters and adjusts the named TIP to the selected L.

Import accepts only the supported adapter/units/protocol and requires ROOT/TIP selections to match the beam endpoints. Additional BCs or amplitude types are rejected. Project-specific contact/periodic/follower-force models need new adapters and a correspondingly different UI contract.

The sweep exporter multiplies width by 0.8/1/1.2, keeping other current inputs fixed; edit the JSON for other studies. It is a demonstration sweep, not an optimized scientific design. Browser configuration export does not execute any licensed solver.
