"""Local structural audit; no importance score and no truth certification."""
import argparse, json, math
from pathlib import Path

def audit(d):
    errors=[]
    for k in ('question','decision','baseline','mechanism','observable','scope','claim'):
        if not isinstance(d.get(k),str) or not d[k].strip(): errors.append('missing meaningful '+k)
    tier=d.get('evidence_tier')
    if tier not in ('proposal','calibrated','holdout','experiment'): errors.append('invalid evidence_tier')
    evidence=d.get('evidence',[])
    if not isinstance(evidence,list) or not evidence: errors.append('evidence ledger is empty'); evidence=[]
    ids=[]
    for e in evidence:
        if not all(isinstance(e.get(k),str) and e[k].strip() for k in ('id','role','source')): errors.append('incomplete evidence record')
        ids.append(e.get('id'))
    if len(ids)!=len(set(ids)): errors.append('duplicate evidence ID')
    if tier!='proposal' and not any(e.get('role')==tier for e in evidence): errors.append('claim tier has no matching evidence role')
    rivals=d.get('rivals',[])
    if not rivals or any(not r.get('explanation') or not r.get('discriminating_test') for r in rivals): errors.append('rival explanation and discriminating test required')
    f=d.get('falsifier',{}); v=f.get('threshold')
    if not f.get('metric') or f.get('comparator') not in ('<','<=','>','>=','==') or isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v): errors.append('falsifier needs metric, comparator and finite numeric threshold')
    if not d.get('controls'): errors.append('mechanism-specific control required')
    cal=set(d.get('calibration_cases',[])); hold=set(d.get('holdout_cases',[]))
    if cal & hold: errors.append('calibration/holdout leakage: '+', '.join(sorted(cal & hold)))
    if tier=='holdout' and not hold: errors.append('holdout claim needs held-out cases')
    return {'pass':not errors,'errors':errors,'scope':'Contract completeness only; scientific significance requires source review.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--out');a=p.parse_args()
    result=audit(json.loads(Path(a.input).read_text(encoding='utf-8-sig')))
    text=json.dumps(result,indent=2,ensure_ascii=False)
    if a.out: Path(a.out).write_text(text+'\n',encoding='utf-8')
    print(text);return 0 if result['pass'] else 2
if __name__=='__main__':raise SystemExit(main())
