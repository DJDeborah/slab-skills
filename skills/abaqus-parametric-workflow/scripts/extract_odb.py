"""Run with abaqus python; compatible with kernel Python 2.7 and Python 3."""
from __future__ import print_function
from odbAccess import openOdb
import hashlib,json,os,sys

def extract(path):
    stem=os.path.splitext(path)[0]
    if os.path.isfile(stem+'.lck'):raise ValueError('ODB still has an analysis lock; do not extract a running job')
    with open(stem+'.sta') as f:sta=f.read()
    log=''
    if os.path.isfile(stem+'.log'):
        with open(stem+'.log') as f:log=f.read()
    # Interactive jobs can report completion to the console without writing a .log.
    completed='THE ANALYSIS HAS COMPLETED SUCCESSFULLY' in sta.upper()
    if not completed:raise ValueError('Completion records do not confirm success')
    odb=openOdb(path=path,readOnly=True)
    try:
        step=odb.steps['LOAD']; all_data={};tip_regions=[]
        for key,region in step.historyRegions.items():
            available=list(region.historyOutputs.keys())
            if key.startswith('Node ') and 'U2' in available and 'RF2' in available:tip_regions.append(region)
            for name in ('ALLIE','ALLKE','ALLAE','ALLVD','ALLWK','ETOTAL'):
                if name in available:
                    if name in all_data:raise ValueError('Ambiguous global energy region for '+name)
                    all_data[name]=[(float(t),float(v)) for t,v in region.historyOutputs[name].data]
        if len(tip_regions)!=1:raise ValueError('Expected exactly one TIP node history region')
        for name in ('U2','RF2'):all_data[name]=[(float(t),float(v)) for t,v in tip_regions[0].historyOutputs[name].data]
        for name in ('ALLIE','ALLKE','ALLAE','U2','RF2'):
            if name not in all_data:raise ValueError('Missing requested history '+name)
        # Abaqus aligns these outputs in this adapter. Reject ambiguous sampling; do not silently interpolate.
        times=[t for t,v in all_data['ALLIE']]
        for name,data in all_data.items():
            if len(data)!=len(times) or any(abs(t-times[i])>1e-8*max(1.0,abs(t)) for i,(t,v) in enumerate(data)):raise ValueError('History samples are unaligned: '+name)
        rows=[dict([('time',t)]+[(name,data[i][1]) for name,data in all_data.items()]) for i,t in enumerate(times)]
        hashes={}
        for suffix in ('.inp','.sta','.log','.odb'):
            if suffix=='.log' and not os.path.isfile(stem+suffix):continue
            with open(stem+suffix,'rb') as f:hashes[os.path.basename(stem+suffix)]=hashlib.sha256(f.read()).hexdigest()
        return {'completed':True,'completion_evidence':'STA success and readable expected ODB step', 'solver_banner':sta.splitlines()[0] if sta.splitlines() else '', 'step':'LOAD','history':rows,'source_hashes':hashes,'scope':'Elastic beam smoke run; no bifurcation claim.'}
    finally:odb.close()
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: abaqus python extract_odb.py job.odb history.json')
    result=extract(sys.argv[1])
    with open(sys.argv[2],'w') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({'completed':result['completed'],'samples':len(result['history']),'source_hashes':result['source_hashes']},indent=2))
