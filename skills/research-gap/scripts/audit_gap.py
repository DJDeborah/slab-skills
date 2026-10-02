"""Audit a supplied search ledger. This script does not discover or certify gaps."""
import argparse,csv,json,re
from pathlib import Path
from datetime import date

def doi_key(s):
    return re.sub(r'^(https?://(dx\.)?doi\.org/|doi:\s*)','',s.strip().lower())
def audit(d,rows):
    errors=[]; warnings=[]
    for k in ('domain','gap_statement','search_scope','decisive_test'):
        if not d.get(k): errors.append('missing '+k)
    if d.get('claim_type')!='bounded': errors.append('finite ledger cannot establish a universal absence claim')
    try: cutoff=date.fromisoformat(d['cutoff_date'])
    except (KeyError,ValueError,TypeError): cutoff=None;errors.append('invalid cutoff_date')
    if not d.get('counterexample_queries'): errors.append('record an adversarial search actually performed')
    included={};dois={}; duplicates=[]
    for i,r in enumerate(rows,2):
        if not all(r.get(k,'').strip() for k in ('study_id','query','engine','searched_on','title','decision')): errors.append('incomplete ledger row '+str(i))
        try:
            day=date.fromisoformat(r.get('searched_on',''))
            if cutoff and day>cutoff: errors.append('ledger search is after stated cutoff at row '+str(i))
        except ValueError: errors.append('invalid search date at row '+str(i))
        if r.get('decision') not in ('include','exclude','unknown'): errors.append('invalid inclusion decision at row '+str(i))
        if r.get('decision')=='include':
            if not r.get('url','').startswith(('https://','http://')) or not r.get('passage') or not r.get('capability_note'): errors.append('included study lacks source/passage/assessment: '+r.get('study_id',''))
            included[r.get('study_id')]=r
        if r.get('decision')=='exclude' and not r.get('capability_note'): errors.append('exclusion needs reason')
        key=doi_key(r.get('doi',''))
        if key:
            if key in dois and dois[key]!=r.get('study_id'): duplicates.append([dois[key],r.get('study_id')]);errors.append('same DOI has different study IDs')
            dois[key]=r.get('study_id')
    studies=d.get('nearest_studies',[])
    if not studies: errors.append('nearest-study matrix is empty')
    for s in studies:
        if s.get('study_id') not in included: errors.append('nearest study not supported by included ledger: '+str(s.get('study_id')))
        if s.get('assessment') not in ('absent','partial','unknown','present'): errors.append('invalid capability assessment')
        if not s.get('capability') or not s.get('unresolved'): errors.append('nearest study needs capability and unresolved issue')
        if s.get('assessment')=='present':warnings.append('Review whether this study defeats the gap: '+s['study_id'])
        if s.get('assessment')=='unknown':warnings.append('Unknown source access is not evidence of absence: '+s['study_id'])
    if any(r.get('engine')=='DEMO-only' for r in rows):warnings.append('Synthetic fixture only; not literature-backed novelty.')
    return {'pass':not errors,'errors':errors,'warnings':warnings,'included_studies':len(included),'queries':len(set(r.get('query') for r in rows)),'duplicate_dois':duplicates,'scope':'Provenance and boundedness audit, not novelty verification.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('gap');p.add_argument('ledger');p.add_argument('--out');a=p.parse_args()
    with open(a.ledger,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    result=audit(json.loads(Path(a.gap).read_text(encoding='utf-8-sig')),rows);text=json.dumps(result,indent=2,ensure_ascii=False)
    if a.out:Path(a.out).write_text(text+'\n',encoding='utf-8')
    print(text);return 0 if result['pass'] else 2
if __name__=='__main__':raise SystemExit(main())
