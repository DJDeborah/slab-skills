"""Execute a frozen serial study with actual completion/extraction checks and resume."""
import argparse,csv,json,shutil,subprocess,sys,os,signal
from pathlib import Path
from datetime import datetime,timezone
import prepare_sweep

def dump(path,d):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');temp.replace(path)
def verify_plan(plan,base):
    if plan.get('schema')!='slab-sweep/1' or not plan.get('cases'):raise ValueError('unsupported or empty study manifest')
    if plan['helper_hashes']!=prepare_sweep.helper_hashes():raise ValueError('frozen helper source changed; prepare a new study')
    ids=set()
    for case in plan['cases']:
        ident=case['case_id']
        if ident in ids:raise ValueError('duplicate case ID')
        ids.add(ident);folder=(base/case['folder']).resolve()
        if not folder.is_relative_to(base.resolve()) or folder.name!=ident:raise ValueError('case folder escapes plan or identity mismatch')
        for file,key in [('config.json','config_sha256'),(ident+'.inp','input_sha256'),('registration.json','registration_sha256')]:
            if prepare_sweep.sha(folder/file)!=case[key]:raise ValueError('frozen '+file+' changed')
def verify_completed(status,folder):
    if not status.get('evidence_hashes'):raise ValueError('completed case lacks evidence hashes')
    for relative,expected in status['evidence_hashes'].items():
        p=(folder/relative).resolve()
        if not p.is_relative_to(folder.resolve()) or prepare_sweep.sha(p)!=expected:raise ValueError('completed evidence changed: '+relative)
def command(args,cwd,log,timeout):
    use_shell=sys.platform=='win32' and str(args[0]).lower().endswith(('.bat','.cmd'))
    with log.open('w',encoding='utf-8') as f:
        proc=subprocess.Popen(subprocess.list2cmdline(args) if use_shell else args,cwd=str(cwd),stdout=f,stderr=subprocess.STDOUT,shell=use_shell,start_new_session=sys.platform!='win32')
        try:code=proc.wait(timeout=timeout)
        except (subprocess.TimeoutExpired,KeyboardInterrupt):
            # Terminate only this launched process tree; do not leave a solver consuming tokens.
            if sys.platform=='win32':subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],stdout=f,stderr=subprocess.STDOUT)
            else:os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
            raise
    if code:raise RuntimeError('command failed; see '+log.name)
def summarize(plan,base):
    fields=['case_id','state','parameters','attempt','final_U2','final_RF2','max_ke_ie','quality_pass','evidence_folder'];rows=[]
    for c in plan['cases']:
        s=json.loads((base/c['folder']/'status.json').read_text(encoding='utf-8'));q=s.get('quality',{});rows.append({'case_id':c['case_id'],'state':s['state'],'parameters':json.dumps(c['parameters'],sort_keys=True),'attempt':s.get('attempt',0),'final_U2':s.get('final_U2'),'final_RF2':q.get('tip_reaction_N'),'max_ke_ie':q.get('max_ke_ie'),'quality_pass':q.get('pass'),'evidence_folder':s.get('evidence_folder','')})
    with (base/'summary.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    return rows
def run(plan,base,launcher,execute=False,max_jobs=2,resume=False,retry_failed=False,timeout=600):
    verify_plan(plan,base)
    if max_jobs<1 or timeout<=0:raise ValueError('max_jobs and timeout must be positive')
    if not execute:return {'solver_launched':False,'planned_cases':len(plan['cases']),'max_jobs':max_jobs,'case_ids':[c['case_id'] for c in plan['cases']]}
    resolved=shutil.which(launcher) or str(Path(launcher).resolve());launched=0;skipped=0
    for c in plan['cases']:
        folder=base/c['folder'];statuspath=folder/'status.json';status=json.loads(statuspath.read_text(encoding='utf-8'));state=status['state']
        if state=='completed':
            if not resume:raise ValueError('existing completed case; use --resume')
            verify_completed(status,folder);skipped+=1;continue
        if state in ('running','failed','interrupted') and not (resume and retry_failed):raise ValueError('noncompleted existing attempt requires --resume --retry-failed')
        if state not in ('prepared','running','failed','interrupted'):raise ValueError('unknown execution state')
        if launched>=max_jobs:break
        attempt=int(status.get('attempt',0))+1;work=folder/'attempts'/('%03d'%attempt)
        if work.exists():raise ValueError('attempt directory already exists')
        work.mkdir(parents=True);job=c['case_id'];shutil.copyfile(folder/(job+'.inp'),work/(job+'.inp'));status={'state':'running','attempt':attempt,'started_utc':datetime.now(timezone.utc).isoformat(),'evidence_folder':str(work.relative_to(folder))};dump(statuspath,status);launched+=1
        try:
            print('Running '+job,flush=True)
            command([resolved,'job='+job,'input='+job+'.inp','double=both','interactive'],work,work/'solver-console.txt',timeout)
            command([resolved,'python',str(Path(__file__).parent/'extract_odb.py'),job+'.odb','history.json'],work,work/'extract-console.txt',timeout)
            if not (work/'history.json').is_file():raise RuntimeError('no extracted history despite launcher return code')
            command([sys.executable,str(Path(__file__).parent/'audit_history.py'),'history.json','--config',str(folder/'config.json'),'--out','quality.json'],work,work/'audit-console.txt',timeout)
            quality=json.loads((work/'quality.json').read_text());history=json.loads((work/'history.json').read_text());status.update(state='completed',quality=quality,final_U2=history['history'][-1]['U2'],completion_evidence=history['completion_evidence'],evidence_hashes={str(p.relative_to(folder)):prepare_sweep.sha(p) for p in (work/'history.json',work/'quality.json',work/(job+'.sta'),work/(job+'.odb'))})
        except (Exception,KeyboardInterrupt) as e:
            status.update(state='interrupted' if isinstance(e,(KeyboardInterrupt,subprocess.TimeoutExpired)) else 'failed',error=type(e).__name__+': '+str(e));dump(statuspath,status);summarize(plan,base);raise
        status['ended_utc']=datetime.now(timezone.utc).isoformat();dump(statuspath,status);summarize(plan,base)
    rows=summarize(plan,base);return {'solver_launched':bool(launched),'launched':launched,'skipped_completed':skipped,'completed':sum(r['state']=='completed' for r in rows),'total':len(rows),'scope':'Elastic numerical beam sweep; no buckling or experimental validation.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--abaqus',default='abaqus');p.add_argument('--execute',action='store_true');p.add_argument('--max-jobs',type=int,default=2);p.add_argument('--resume',action='store_true');p.add_argument('--retry-failed',action='store_true');p.add_argument('--timeout',type=float,default=600);a=p.parse_args();path=Path(a.manifest).resolve()
    try:r=run(json.loads(path.read_text(encoding='utf-8')),path.parent,a.abaqus,a.execute,a.max_jobs,a.resume,a.retry_failed,a.timeout)
    except (ValueError,RuntimeError,subprocess.TimeoutExpired) as e:print('STOPPED: '+str(e));raise SystemExit(2)
    print(json.dumps(r,indent=2))
