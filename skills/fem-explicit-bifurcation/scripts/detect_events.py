"""Observable event candidates; no static stability or snap certification."""
import argparse,json,math
from pathlib import Path

def detect(rows,c):
    force=c.get('force_field','RF2');sign=c.get('force_sign',1);span=c.get('window_samples',3);fraction=c.get('force_drop_fraction',0.15);floor=c.get('force_floor',1e-8);persistence=c.get('persistence_samples',3)
    if sign not in (-1,1) or isinstance(span,bool) or not isinstance(span,int) or span<1 or not 0<fraction<1 or floor<=0 or isinstance(persistence,bool) or not isinstance(persistence,int) or persistence<1:raise ValueError('invalid event configuration')
    if any(not all(isinstance(r.get(k),(int,float)) and math.isfinite(r[k]) for k in ('time',force)) for r in rows):raise ValueError('missing or nonfinite history')
    if any(rows[i]['time']<=rows[i-1]['time'] for i in range(1,len(rows))):raise ValueError('nonmonotone time')
    events=[];last_drop=-span-1
    for i in range(span,len(rows)):
        before=sign*rows[i-span][force];after=sign*rows[i][force]
        if before>floor and (before-after)/before>=fraction and i-last_drop>span:
            events.append({'type':'force-drop-candidate','time':rows[i]['time'],'relative_drop':(before-after)/before,'sample_index':i});last_drop=i
    field=c.get('opening_field');threshold=c.get('opening_threshold')
    if field:
        if not isinstance(threshold,(int,float)) or not math.isfinite(threshold):raise ValueError('opening threshold required')
        if any(not isinstance(r.get(field),(int,float)) or not math.isfinite(r[field]) for r in rows):raise ValueError('missing opening history')
        start=None;above=False
        for i,r in enumerate(rows):
            if r[field]>=threshold:
                if start is None:start=i
                if not above and i-start+1>=persistence:
                    events.append({'type':'sustained-opening-candidate','time':rows[start]['time'],'confirmed_at':r['time'],'sample_index':start});above=True
            else:start=None;above=False
    return {'events':events,'configuration':c,'scope':'Threshold-defined observable candidates only; no equilibrium bifurcation or physical landing claim.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('history');p.add_argument('--config',required=True);p.add_argument('--out',required=True);a=p.parse_args();d=json.loads(Path(a.history).read_text(encoding='utf-8-sig'));c=json.loads(Path(a.config).read_text(encoding='utf-8-sig'));r=detect(d['history'],c);Path(a.out).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps({'events':len(r['events']),'scope':r['scope']}))
