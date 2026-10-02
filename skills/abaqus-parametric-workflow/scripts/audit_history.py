"""Energy/reaction smoke audit. Does not infer equilibrium bifurcation."""
import argparse,json,math
from pathlib import Path

def audit(d,c):
    errors=[]
    if d.get('completed') is not True:errors.append('solver completion not confirmed')
    rows=d.get('history',[]);needed=('time','U2','RF2','ALLIE','ALLKE','ALLAE')
    if len(rows)<3 or any(any(isinstance(r.get(k),bool) or not isinstance(r.get(k),(int,float)) or not math.isfinite(r[k]) for k in needed) for r in rows):return {'pass':False,'errors':errors+['missing/nonfinite required histories'],'scope':'No stability claim.'}
    if any(rows[i]['time']<=rows[i-1]['time'] for i in range(1,len(rows))):errors.append('history times must be strictly increasing')
    duration=c['duration']
    if abs(rows[-1]['time']-duration)>duration*1e-5:errors.append('history does not reach configured end time')
    q=c['quality'];start,end=q['window_fraction']
    if not 0<=start<end<=1:raise ValueError('invalid quality window')
    peak=max(abs(r['ALLIE']) for r in rows);floor=q['internal_energy_floor_fraction']*peak
    window=[r for r in rows if start*duration<=r['time']<=end*duration]
    selected=[r for r in window if abs(r['ALLIE'])>max(floor,1e-30)]
    if not selected:errors.append('no meaningful internal energy in audit window')
    ke=max((abs(r['ALLKE']/r['ALLIE']) for r in selected),default=None);ae=max((abs(r['ALLAE']/r['ALLIE']) for r in selected),default=None)
    if ke is not None and ke>q['max_ke_ie']:errors.append('kinetic/internal ratio exceeds configured smoke limit')
    if ae is not None and ae>q['max_ae_ie']:errors.append('artificial/internal ratio exceeds configured smoke limit')
    g=c['geometry'];E=c['material']['E'];tipbc=[b for b in c['constraints'] if b['region']=='TIP' and 2 in b['dofs']][0];target=tipbc['value']
    expected=3*E*(g['width']*g['thickness']**3/12)*target/g['length']**3
    reaction=rows[-1]['RF2'];err=abs(reaction-expected)/abs(expected) if expected else abs(reaction)
    if err>q['reaction_relative_tolerance']:errors.append('tip reaction differs from small-deformation reference')
    if abs(rows[-1]['U2']-target)>max(1e-7,abs(target)*1e-5):errors.append('prescribed tip displacement mismatch')
    if any(r['ALLKE']<0 or r['ALLIE']<-1e-15 for r in rows):errors.append('negative energy in elastic smoke model')
    return {'pass':not errors,'errors':errors,'window_fraction':[start,end],'window_samples':len(window),'meaningful_samples':len(selected),'masked_samples':len(window)-len(selected),'max_ke_ie':ke,'max_ae_ie':ae,'full_history_max_ke_ie':max((abs(r['ALLKE']/r['ALLIE']) for r in rows if abs(r['ALLIE'])>max(floor,1e-30)),default=None),'tip_reaction_N':reaction,'expected_tip_reaction_N':expected,'reaction_relative_error':err,'scope':'Elastic numerical smoke only; event, mesh/rate convergence and FE bifurcation unverified.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('history');p.add_argument('--config',required=True);p.add_argument('--out');a=p.parse_args();d=json.loads(Path(a.history).read_text(encoding='utf-8-sig'));c=json.loads(Path(a.config).read_text(encoding='utf-8-sig'));r=audit(d,c);text=json.dumps(r,indent=2,allow_nan=False)
    if a.out:Path(a.out).write_text(text+'\n',encoding='utf-8')
    print(text);return 0 if r['pass'] else 2
if __name__=='__main__':raise SystemExit(main())
