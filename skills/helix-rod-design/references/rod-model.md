# Circular helical rod model

Use mm, N and MPa. For a increasing from 0 to 2*pi*n:
r(a)=[R*cos(a), h*R*sin(a), p*a/(2*pi)], h=+1 or -1.
Let b=p/(2*pi), ds/da=sqrt(R^2+b^2), curvature=R/(R^2+b^2), torsion=h*b/(R^2+b^2).
A=pi*rw^2, I=pi*rw^4/4, J=2I, G=E/[2(1+nu)].

At a cut, F=Ftip, M=Mtip+(rtip-r) cross Ftip. With t the unit tangent,
Sf=tt/(EA)+(I3-tt)/(ks*GA); Sm=tt/(GJ)+(I3-tt)/(EI).
Let B=[[I3,0],[skew(rtip-r),I3]]. Cport=integral B^T diag(Sf,Sm) B ds.
This is a linear initially-curved rod energy with a circular section and no prestress. Numerical quadrature evaluates the integral in the project.

Every C block has its own units: translation/force mm/N; rotation/force rad/N; translation/moment mm/(N mm); rotation/moment rad/(N mm). For a scaled comparison use qbar=[u,l0*theta] and fbar=[F,M/l0], so Cbar=S*C*S with S=diag(1,1,1,l0,l0,l0).
Circular isotropy removes dependence on section director choice in this model. A rectangular or anisotropic rod requires transported material directors and a full section tensor; do not reuse the circular formula silently.
