"""Run the four portable workflows without a license or external packages."""
import argparse,csv,hashlib,json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def run(script,*args):
    p=subprocess.run([sys.executable,str(script),*map(str,args)],capture_output=True,text=True,encoding='utf-8')
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out)
    if out.exists():raise FileExistsError('Use a fresh demo output folder')
    out.mkdir(parents=True);skills=ROOT/'skills'
    for name,file in (('research-significance','significance.json'),('research-gap','gap.json'),('research-gap','search-ledger.csv'),('fem-explicit-bifurcation','beam-explicit.json')):(out/file).write_bytes((skills/name/'assets'/file).read_bytes())
    run(skills/'research-significance/scripts/audit_significance.py',out/'significance.json','--out',out/'significance-audit.json')
    run(skills/'research-gap/scripts/audit_gap.py',out/'gap.json',out/'search-ledger.csv','--out',out/'gap-audit.json')
    run(skills/'fem-explicit-bifurcation/scripts/prepare_explicit.py',out/'beam-explicit.json','--out',out/'prepared-beam')
    run(skills/'fem-explicit-bifurcation/scripts/branch_benchmarks.py','--out',out/'branches.json')
    manifest={'claims':[{'id':'C1','text':'The sampled exact scalar normal forms pass residual and tangent-sign checks.','status':'supported','evidence_ids':['E1']},{'id':'C2','text':'Boundary-driven path selection remains a prospective hypothesis.','status':'proposed','evidence_ids':['E2']}],'figures':[],'evidence':[{'id':'E1','path':'branches.json','sha256':hashlib.sha256((out/'branches.json').read_bytes()).hexdigest(),'role':'numerical-verification'},{'id':'E2','path':'significance.json','sha256':hashlib.sha256((out/'significance.json').read_bytes()).hexdigest(),'role':'proposal'}],'required_assets':['C1','C2']}
    (out/'manuscript-map.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (out/'draft.md').write_text('# Demonstration draft\n\nThe sampled exact scalar normal forms satisfy their equilibrium residuals and expected tangent signs [claim:C1]. These checks concern the known scalar examples and provide a small oracle for future continuation work. They do not validate an FE equilibrium branch.\n\nBoundary-driven path selection is a prospective research question [claim:C2]. A registered unseen boundary case and loading-duration control would test whether a proposed change follows the constraints or inertia. No specimen-level result is claimed.\n',encoding='utf-8')
    run(skills/'research-writing/scripts/audit_manuscript.py',out/'manuscript-map.json',out/'draft.md','--out',out/'writing-audit.json')
    summary={'pass':True,'demonstrated':['prospective significance contract','synthetic bounded gap ledger','claim/evidence writing audit','registered Explicit input deck','known scalar branch oracle'],'not_demonstrated':['real literature novelty','agent writing-quality improvement','licensed FE execution','FE bifurcation or contact validation']}
    (out/'demo-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
