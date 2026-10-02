"""Exact normal-form oracle, not a continuation or branch-discovery solver."""
import argparse,json,math
from pathlib import Path

def compute():
    fold=[];pitch=[]
    for lam in (0.0,0.01,0.25,1.0):
        for q in ([0.0] if lam==0 else [-math.sqrt(lam),math.sqrt(lam)]):fold.append({'lambda':lam,'q':q,'residual':q*q-lam,'tangent':2*q,'branch':'fold'})
    for lam in (-1.0,-0.25,0.0,0.25,1.0):
        for q in ([0.0] if lam<=0 else [0.0,-math.sqrt(lam),math.sqrt(lam)]):pitch.append({'lambda':lam,'q':q,'residual':q**3-lam*q,'tangent':3*q*q-lam,'branch':'central' if q==0 else 'side'})
    passed=all(abs(r['residual'])<1e-12 for r in fold+pitch) and all((r['tangent']>0)==(r['q']>0) for r in fold if r['q']!=0) and all(r['tangent']>0 for r in pitch if r['branch']=='side') and all((r['tangent']>0)==(r['lambda']<0) for r in pitch if r['branch']=='central' and r['lambda']!=0)
    return {'pass':passed,'fold':fold,'pitchfork':pitch,'scope':'Known exact normal forms only; no FE branch discovery, contact or dynamic landing verification.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();r=compute();Path(a.out).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps({'pass':r['pass'],'equilibria':len(r['fold'])+len(r['pitchfork']),'scope':r['scope']}));raise SystemExit(0 if r['pass'] else 2)
