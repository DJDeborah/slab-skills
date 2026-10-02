"""Check provenance, preservation and tagged claim coverage; no semantic truth claim."""
import argparse,hashlib,json,re
from pathlib import Path

def audit(d,text,base):
    errors=[];warnings=[];records=d.get('evidence',[]);evidence={e.get('id'):e for e in records}
    if len(evidence)!=len(records):errors.append('duplicate evidence ID')
    for e in records:
        p=Path(e.get('path',''))
        if p.is_absolute():errors.append('evidence path must be project-relative');continue
        target=(base/p).resolve()
        if not target.is_relative_to(base.resolve()):errors.append('evidence path escapes project');continue
        if not target.is_file():errors.append('missing evidence file: '+str(p));continue
        expected=e.get('sha256','')
        if expected and hashlib.sha256(target.read_bytes()).hexdigest()!=expected:errors.append('evidence hash mismatch: '+str(p))
        if not expected:warnings.append('unfrozen evidence hash: '+str(p))
        if e.get('role') not in ('proposal','calibration','holdout','experiment','numerical-verification','theory'):errors.append('invalid evidence role')
    known=set(); tags=set(re.findall(r'\[(?:claim|figure):([\w-]+)\]',text))
    for group in ('claims','figures'):
        for item in d.get(group,[]):
            ident=item.get('id');
            if not ident or ident in known:errors.append('missing or duplicate claim/figure ID')
            known.add(ident)
            for eid in item.get('evidence_ids',[]):
                if eid not in evidence:errors.append('unknown evidence reference: '+str(eid))
            if group=='claims':
                if item.get('status') not in ('proposed','supported','disputed','untested'):errors.append('invalid claim status')
                if item.get('status')=='supported' and not any(evidence.get(eid,{}).get('role') not in (None,'proposal') for eid in item.get('evidence_ids',[])):errors.append('supported claim lacks non-proposal evidence: '+str(ident))
    for ident in tags-known:errors.append('unknown manuscript tag: '+str(ident))
    for ident in d.get('required_assets',[]):
        if ident not in known:errors.append('required asset missing from inventory: '+str(ident))
        elif ident not in tags:errors.append('required asset omitted from manuscript: '+str(ident))
    for phrase in ('first-ever','universally predicts','fully validated','zero eigenvalue proves snapping'):
        if phrase in text.lower():warnings.append('Inspect potentially overstrong wording: '+phrase)
    return {'pass':not errors,'errors':errors,'warnings':warnings,'scope':'Traceability and preservation audit only; review actual scientific content.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('draft');p.add_argument('--out');a=p.parse_args();m=Path(a.manifest)
    result=audit(json.loads(m.read_text(encoding='utf-8-sig')),Path(a.draft).read_text(encoding='utf-8-sig'),m.parent);text=json.dumps(result,indent=2,ensure_ascii=False)
    if a.out:Path(a.out).write_text(text+'\n',encoding='utf-8')
    print(text);return 0 if result['pass'] else 2
if __name__=='__main__':raise SystemExit(main())
