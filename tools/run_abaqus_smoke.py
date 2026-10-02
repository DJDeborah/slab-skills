"""Optional licensed Explicit runs, extraction and small beam sensitivity study."""
import argparse,copy,json,subprocess,sys,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def execute(args,cwd,log,timeout=600):
    # Windows CreateProcess does not launch .bat reliably without its shell.
    command=subprocess.list2cmdline(args) if sys.platform=='win32' and str(args[0]).lower().endswith(('.bat','.cmd')) else args
    p=subprocess.run(command,cwd=str(cwd),capture_output=True,text=True,errors='replace',shell=isinstance(command,str),timeout=timeout)
    log.write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
    if p.returncode:raise RuntimeError('Command failed; inspect '+str(log))
def main():
    p=argparse.ArgumentParser();p.add_argument('--abaqus',default='abaqus');p.add_argument('--out',required=True);p.add_argument('--sensitivity',action='store_true');a=p.parse_args();out=Path(a.out).resolve()
    if out.exists():raise FileExistsError('Use a fresh run directory')
    launcher=shutil.which(a.abaqus) or str(Path(a.abaqus).resolve())
    out.mkdir(parents=True);sd=ROOT/'skills/fem-explicit-bifurcation';base=json.loads((sd/'assets/beam-explicit.json').read_text());cases=[('n20_t025',20,.25)]
    if a.sensitivity:cases=[('n10_t025',10,.25),('n20_t025',20,.25),('n20_t050',20,.5)]
    results=[]
    for name,n,duration in cases:
        run=out/name;run.mkdir();c=copy.deepcopy(base);c['geometry']['elements']=n;c['duration']=duration;(run/'config.json').write_text(json.dumps(c,indent=2),encoding='utf-8')
        execute([sys.executable,str(sd/'scripts/prepare_explicit.py'),str(run/'config.json'),'--out',str(run)],run,run/'prepare-console.txt')
        print('Running '+name,flush=True)
        execute([launcher,'job='+c['job'],'input='+c['job']+'.inp','double=both','interactive'],run,run/'solver-console.txt')
        # Old Abaqus launcher may return 0 after a Python error: require extraction artifact.
        execute([launcher,'python',str(sd/'scripts/extract_odb.py'),c['job']+'.odb','history.json'],run,run/'extract-console.txt')
        if not (run/'history.json').is_file():raise RuntimeError('Extraction produced no history; inspect '+str(run/'extract-console.txt'))
        execute([sys.executable,str(sd/'scripts/audit_history.py'),'history.json','--config','config.json','--out','quality.json'],run,run/'audit-console.txt')
        execute([sys.executable,str(sd/'scripts/detect_events.py'),'history.json','--config',str(sd/'assets/events.json'),'--out','events.json'],run,run/'events-console.txt')
        history=json.loads((run/'history.json').read_text());quality=json.loads((run/'quality.json').read_text());events=json.loads((run/'events.json').read_text())
        results.append({'case':name,'elements':n,'duration':duration,'double_precision':True,'quality':quality,'event_candidates':len(events['events']),'final_U2':history['history'][-1]['U2'],'history_samples':len(history['history']),'source_hashes':history['source_hashes']})
    summary={'pass':all(r['quality']['pass'] for r in results),'cases':results,'scope':'Elastic straight beam numerical checks only; no contact or FE bifurcation validation.'}
    if a.sensitivity:
        r10,r20,rslow=[r['quality']['tip_reaction_N'] for r in results];summary['reaction_sensitivity']={'mesh10_to20_relative':abs(r10-r20)/abs(r20),'duration025_to050_relative':abs(r20-rslow)/abs(rslow),'scope':'Sensitivity of final elastic reaction only; no universal convergence order.'}
    (out/'smoke-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,indent=2));return 0 if summary['pass'] else 2
if __name__=='__main__':raise SystemExit(main())
