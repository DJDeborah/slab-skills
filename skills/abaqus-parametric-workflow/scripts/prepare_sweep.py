"""Freeze a bounded beam parameter plan and prepare all decks without launching a solver."""
import argparse,copy,hashlib,itertools,json,math
from pathlib import Path
from datetime import datetime,timezone
import prepare_explicit

ALLOWED={'geometry.length','geometry.width','geometry.thickness','geometry.elements','material.E','material.nu','material.density','duration','tip_displacement'}
HELPERS=('prepare_explicit.py','extract_odb.py','audit_history.py','prepare_sweep.py','run_sweep.py')
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def helper_hashes():return {n:sha(Path(__file__).parent/n) for n in HELPERS}
def configurations(d,max_cases):
    axes=d.get('axes',{})
    if not isinstance(axes,dict) or set(axes)-ALLOWED:raise ValueError('unsupported parameter axis')
    if isinstance(max_cases,bool) or not isinstance(max_cases,int) or max_cases<1:raise ValueError('max_cases must be a positive integer')
    count=1
    for key,values in axes.items():
        if not isinstance(values,list) or not values:raise ValueError('axis needs nonempty values: '+key)
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in values):raise ValueError('axis values must be finite numbers')
        if len(set(values))!=len(values):raise ValueError('duplicate axis values: '+key)
        count*=len(values)
    if count>max_cases:raise ValueError('requested %d cases exceeds max_cases=%d'%(count,max_cases))
    result=[];identities=set();keys=list(axes)
    for values in itertools.product(*(axes[k] for k in keys)):
        c=copy.deepcopy(d['base']);parameters=dict(zip(keys,values))
        for key,value in parameters.items():
            if key=='tip_displacement':
                for bc in c['constraints']:
                    if bc['region']=='TIP' and 2 in bc['dofs']:bc['value']=value
            elif '.' in key:
                group,field=key.split('.');c[group][field]=value
            else:c[key]=value
        L=c['geometry']['length'];eps=max(abs(L)*1e-6,1e-6)
        c['regions']={'ROOT':{'bbox':[-eps,eps,-eps,eps],'expected_count':1},'TIP':{'bbox':[L-eps,L+eps,-eps,eps],'expected_count':1}}
        # Canonical identity is computed before the derived job name.
        c['job']='beam_explicit';identity=hashlib.sha256(canonical(c).encode()).hexdigest()[:12]
        if identity in identities:raise ValueError('duplicate normalized configuration')
        identities.add(identity);case='beam_'+identity;c['job']=case
        deck,registration=prepare_explicit.prepare(c)
        result.append({'case_id':case,'parameters':parameters,'config':c,'deck':deck,'registration':registration})
    return result
def prepare(d,out,max_cases=16):
    cases=configurations(d,max_cases);out=Path(out)
    if out.exists():raise FileExistsError('Use a new run directory: '+str(out))
    out.mkdir(parents=True);plan={'schema':'slab-sweep/1','created_utc':datetime.now(timezone.utc).isoformat(),'study_sha256':hashlib.sha256(canonical(d).encode()).hexdigest(),'helper_hashes':helper_hashes(),'cases':[],'scope':'Elastic B21 cantilever teaching sweep only.'}
    for case in cases:
        folder=out/case['case_id'];folder.mkdir();config=folder/'config.json';config.write_text(json.dumps(case['config'],indent=2)+'\n',encoding='utf-8',newline='\n');inp=folder/(case['case_id']+'.inp');inp.write_text(case['deck'],encoding='ascii',newline='\n');reg=folder/'registration.json';reg.write_text(json.dumps(case['registration'],indent=2)+'\n',encoding='utf-8',newline='\n')
        plan['cases'].append({'case_id':case['case_id'],'parameters':case['parameters'],'folder':case['case_id'],'config_sha256':sha(config),'input_sha256':sha(inp),'registration_sha256':sha(reg)})
        (folder/'status.json').write_text(json.dumps({'state':'prepared','attempt':0},indent=2)+'\n',encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8',newline='\n');return plan
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('config');p.add_argument('--out',required=True);p.add_argument('--max-cases',type=int,default=16);a=p.parse_args()
    try:plan=prepare(json.loads(Path(a.config).read_text(encoding='utf-8-sig')),a.out,a.max_cases)
    except (ValueError,KeyError,TypeError,FileExistsError) as e:print('REJECTED: '+str(e));raise SystemExit(2)
    print(json.dumps({'prepared_cases':len(plan['cases']),'manifest':str(Path(a.out)/'manifest.json'),'solver_launched':False},indent=2))
