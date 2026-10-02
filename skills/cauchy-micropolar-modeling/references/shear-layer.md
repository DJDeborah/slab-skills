# Analytic micropolar shear layer

Assume a planar isotropic material varying along x. Independent microrotation phi rotates about z. Use engineering strain vector
eta=[exx,eyy,gamma_xy,rxy,l0*phi_x,l0*phi_y],
gamma_xy=u_y+v_x, rxy=v_x-u_y-2*phi.
Q normal block E/(1-nu^2)*[[1,nu],[nu,1]], shear G=E/[2(1+nu)], skew Gc and curvature D/l0^2. Q entries are MPa; D is N and l0 is mm. The conventional force/couple stresses follow from this explicit strain mapping, not from assuming each eta entry is a conventional tensor component.
C is the first 3 by 3 restriction at rxy=0 and zero curvature. This diagonal nonchiral benchmark is not a homogenized helix lattice.

For u=0, v=v(x), phi=phi(x), w=.5*G*v_x^2+.5*Gc*(v_x-2*phi)^2+.5*D*phi_x^2.
Force traction tau=(G+Gc)*v_x-2*Gc*phi is constant.
Rotation equation -D*phi_xx+4*Gc*phi-2*Gc*v_x=0.
Couple traction is D*phi_x. Boundary data v(0)=0, v(L)=delta; clamped phi(0)=phi(L)=0.
ell=sqrt(D*(G+Gc)/(4*G*Gc)), a=Gc/(G+Gc).
tau=G*delta/[L-2*ell*a*tanh(L/(2*ell))].
phi(x)=tau/(2G)*[1-cosh((x-L/2)/ell)/cosh(L/(2*ell))].
v(x)=tau/G*[x-ell*a*(sinh((x-L/2)/ell)+sinh(L/(2*ell)))/cosh(L/(2*ell))].

For free couple traction at both ends phi=delta/(2L), v=delta*x/L, tau=G*delta/L. Under clamped rotation G_eff tends to G+Gc for L/ell small and to G for L/ell large. These are consequences of the chosen energy and BCs, not fitted material observations. The helper rejects L/ell>100 to avoid hyperbolic overflow; use a numerically stable exponential form for a larger domain.
