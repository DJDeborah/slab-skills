"""Generate a bounded B21 Explicit adapter, with auditable named selections."""
import argparse,hashlib,json,math,re
from pathlib import Path

def positive(v,name):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0:raise ValueError(name+' must be finite and positive')
    return v
def prepare(c):
    if c.get('adapter')!='abaqus-b21-cantilever' or c.get('units')!='N-mm-tonne-s':raise ValueError('unsupported adapter or units')
    job=c.get('job','')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,60}',job):raise ValueError('invalid job name')
    g=c['geometry'];L=positive(g['length'],'length');a=positive(g['width'],'width');b=positive(g['thickness'],'thickness');n=g['elements']
    if isinstance(n,bool) or not isinstance(n,int) or not 2<=n<=10000:raise ValueError('elements must be an integer in [2,10000]')
    m=c['material'];E=positive(m['E'],'E');rho=positive(m['density'],'density');nu=m['nu']
    if not isinstance(nu,(int,float)) or not -1<nu<0.5:raise ValueError('nu must be in (-1,0.5)')
    duration=positive(c['duration'],'duration');outputs=c['outputs']
    if isinstance(outputs,bool) or not isinstance(outputs,int) or not 10<=outputs<=100000:raise ValueError('outputs must be integer in [10,100000]')
    nodes=[(i+1,L*i/n,0.0) for i in range(n+1)];sets={}
    for name,selector in c['regions'].items():
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',name):raise ValueError('invalid region name')
        box=selector['bbox']
        if len(box)!=4 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in box) or box[0]>box[1] or box[2]>box[3]:raise ValueError('invalid bbox')
        ids=[i for i,x,y in nodes if box[0]<=x<=box[1] and box[2]<=y<=box[3]]
        if not ids or len(ids)!=selector['expected_count']:raise ValueError('region '+name+' selects '+str(len(ids))+' nodes; expected '+str(selector['expected_count']))
        sets[name]=ids
    dofs={};fixed=[];ramped=[]
    for bc in c['constraints']:
        region=bc['region']
        if region not in sets:raise ValueError('unknown BC region')
        val=bc['value']
        if isinstance(val,bool) or not isinstance(val,(int,float)) or not math.isfinite(val):raise ValueError('invalid BC value')
        amp=bc.get('amplitude')
        if amp not in (None,'RAMP'):raise ValueError('unsupported amplitude')
        for d in bc['dofs']:
            if d not in (1,2,6):raise ValueError('unsupported B21 DOF')
            for node in sets[region]:
                key=(node,d)
                if key in dofs:raise ValueError('duplicate/conflicting BC on node '+str(node)+' DOF '+str(d))
                dofs[key]=(val,amp)
            (ramped if amp else fixed).append('%s, %d, %d, %.12g'%(region,d,d,val))
    # This benchmark deliberately supports one physical model. Other models need an adapter.
    if sets.get('ROOT')!=[1] or sets.get('TIP')!=[n+1]:raise ValueError('cantilever adapter requires ROOT at x=0 and TIP at x=L')
    required={(1,1),(1,2),(1,6),(n+1,2)}
    if set(dofs)!=required or any(dofs[(1,d)]!=(0.0,None) for d in (1,2,6)) or dofs[(n+1,2)][1]!='RAMP':raise ValueError('unsupported cantilever boundary protocol')
    tip=dofs[(n+1,2)][0]
    lines=['*Heading','Generated small-deformation cantilever smoke benchmark','*Node']
    lines+=['%d, %.12g, %.12g'%v for v in nodes]
    lines+=['*Element, type=B21, elset=BEAM']+['%d, %d, %d'%(i,i,i+1) for i in range(1,n+1)]
    for name,ids in sets.items():lines+=['*Nset, nset='+name,', '.join(map(str,ids))]
    lines+=['*Material, name=ELASTIC','*Elastic','%.12g, %.12g'%(E,nu),'*Density','%.12g'%rho,'*Beam Section, elset=BEAM, material=ELASTIC, section=RECT','%.12g, %.12g'%(a,b),'0., 0., -1.','*Boundary']+fixed
    lines+=['*Amplitude, name=RAMP, definition=SMOOTH STEP','0., 0., %.12g, 1.'%duration,'*Step, name=LOAD, nlgeom=YES','*Dynamic, Explicit',', %.12g'%duration,'*Boundary, amplitude=RAMP']+ramped
    lines+=['*Output, field, number interval=20','*Node Output','U, RF','*Output, history, time interval=%.12g'%(duration/outputs),'*Energy Output','ALLIE, ALLKE, ALLAE, ALLVD, ALLWK, ETOTAL','*Node Output, nset=TIP','U2, RF2','*End Step']
    deck='\n'.join(lines)+'\n';reg={'adapter':c['adapter'],'units':c['units'],'node_count':len(nodes),'element_count':n,'regions':sets,'constraints':c['constraints'],'section_director':[0,0,-1],'density':rho,'mass_scaling':False,'expected_small_deflection_tip_reaction_N':3*E*(a*b**3/12)*tip/L**3,'scope':'Elastic straight beam only; no contact or buckling verification.'}
    reg['input_sha256']=hashlib.sha256(deck.encode()).hexdigest()
    return deck,reg
def main():
    p=argparse.ArgumentParser();p.add_argument('config');p.add_argument('--out',required=True);a=p.parse_args();c=json.loads(Path(a.config).read_text(encoding='utf-8-sig'))
    try:deck,reg=prepare(c)
    except (ValueError,KeyError,TypeError) as e:print('REJECTED: '+str(e));return 2
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    for name in (c['job']+'.inp','registration.json'):
        if (out/name).exists():raise FileExistsError('Use a fresh run directory: '+str(out/name))
    (out/(c['job']+'.inp')).write_text(deck,encoding='ascii',newline='\n');(out/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8');print(json.dumps(reg,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
