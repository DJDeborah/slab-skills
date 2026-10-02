import argparse,csv,json,math
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('--config',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--segments',type=int,default=128);args=a.parse_args()
p=json.loads(args.config.read_text());R=float(p['radius']);pitch=float(p['pitch']);turns=float(p['turns']);rw=float(p['wire_radius']);h=p['handedness']
if min(R,pitch,turns,rw,args.segments)<=0 or h not in (-1,1):raise ValueError('Invalid geometry')
if pitch<=2*rw:raise ValueError('Adjacent turns overlap')
args.out.parent.mkdir(parents=True,exist_ok=True)
with args.out.open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['node','x_mm','y_mm','z_mm'])
    for i in range(args.segments+1):
        t=2*math.pi*turns*i/args.segments;w.writerow([i+1,R*math.cos(t),h*R*math.sin(t),pitch*t/(2*math.pi)])
print(json.dumps({'height_mm':pitch*turns,'wire_length_mm':turns*math.sqrt((2*math.pi*R)**2+pitch**2),'curvature_times_radius':R/(R*R+(pitch/(2*math.pi))**2)*rw,'clearance_mm':pitch-2*rw}))
