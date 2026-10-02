import argparse,csv,math,json
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('--G',type=float,default=1);a.add_argument('--Gc',type=float,default=1);a.add_argument('--D',type=float,default=2);a.add_argument('--L',type=float,default=4);a.add_argument('--delta',type=float,default=.01);a.add_argument('--out',type=Path,required=True);args=a.parse_args()
G,Gc,D,L=args.G,args.Gc,args.D,args.L
if min(G,Gc,D,L)<=0:raise ValueError('Positive coefficients required')
ell=math.sqrt(D*(G+Gc)/(4*G*Gc))
if L/ell>100:raise ValueError('Use stable exponential formulas when L/ell exceeds 100')
aa=Gc/(G+Gc);tau=G*args.delta/(L-2*ell*aa*math.tanh(L/(2*ell)));args.out.parent.mkdir(parents=True,exist_ok=True)
with args.out.open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['x_mm','v_mm','phi_rad'])
    for i in range(129):
        x=L*i/128;phi=tau/(2*G)*(1-math.cosh((x-L/2)/ell)/math.cosh(L/(2*ell)));v=tau/G*(x-ell*aa*(math.sinh((x-L/2)/ell)+math.sinh(L/(2*ell)))/math.cosh(L/(2*ell)));w.writerow([x,v,phi])
print(json.dumps({'ell_mm':ell,'tau_MPa':tau,'G_effective_MPa':tau*L/args.delta}))
