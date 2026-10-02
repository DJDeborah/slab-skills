"""Compare a limited, explicit physical registration schema; no solver execution."""
import json,math,sys
from pathlib import Path

def number(v):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):
        raise ValueError('Numeric physical inputs must be finite numbers')
    return float(v)

def normalize(d):
    length={'m':1.0,'mm':0.001}[d['units']['length']]
    force={'N':1.0,'kN':1000.0}[d['units']['force']]
    mat=d['material']; sec=d['cross_section']; load=d['loading']
    if mat['law']!='linear_elastic' or sec['type']!='rectangle':
        raise ValueError('Unsupported material or section; requires domain registration')
    E=number(mat['E'])*force/length**2; nu=number(mat['nu'])
    b=number(sec['width'])*length; h=number(sec['height'])*length
    if E<=0 or b<=0 or h<=0 or not -1<nu<0.5: raise ValueError('Invalid elastic input')
    if load['control'] not in ('force','displacement'): raise ValueError('Unsupported load control')
    ports={}
    for k,xyz in d['reference_ports'].items():
        if len(xyz)!=3: raise ValueError('Ports require three coordinates')
        ports[k]=[number(x)*length for x in xyz]
    constraints=d['constraints']
    for p,dofs in constraints.items():
        if p not in ports or not isinstance(dofs,list) or not set(dofs)<=set(('ux','uy','uz','rx','ry','rz')):
            raise ValueError('Invalid constraint record')
    if load['port'] not in ports: raise ValueError('Unknown loading port')
    if not d['observable_definition']: raise ValueError('Missing observable convention')
    return {'ports':ports,'E_Pa':E,'nu':nu,'width_m':b,'height_m':h,
            'constraints':{k:sorted(v) for k,v in constraints.items()},
            'loading':{**load,'amplitude':number(load['amplitude'])*(force if load['control']=='force' else length)},
            'observable_definition':d['observable_definition']}

def differences(a,b,path=''):
    out=[]
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(set(a)|set(b)):
            p=path+'.'+k if path else k
            if k not in a or k not in b: out.append(p+': missing')
            else: out.extend(differences(a[k],b[k],p))
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): out.append(path+': length mismatch')
        else:
            for i,(x,y) in enumerate(zip(a,b)): out.extend(differences(x,y,path+f'[{i}]'))
    elif isinstance(a,(int,float)) and isinstance(b,(int,float)):
        if not math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-12): out.append(path+': numeric mismatch')
    elif a!=b: out.append(path+': convention mismatch')
    return out

def compare(a,b):
    diff=differences(normalize(a),normalize(b))
    return {'case_ids':[a['case_id'],b['case_id']],'registration_match':not diff,'mismatches':diff,
            'scope':'Supported physical input fields only; not mesh, contact, or predictive validation'}

if __name__=='__main__':
    try:
        if len(sys.argv)!=3: raise ValueError('Usage: compare_registration.py analytical.json fem.json')
        result=compare(*[json.loads(Path(p).read_text(encoding='utf-8')) for p in sys.argv[1:]])
        print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(0 if result['registration_match'] else 1)
    except (KeyError,ValueError,TypeError,OSError) as e:
        print(json.dumps({'registration_match':False,'error':str(e)})); sys.exit(2)
