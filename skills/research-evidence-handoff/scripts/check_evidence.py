"""Hash local evidence and check role consistency; never judge physical validity."""
import hashlib,json,sys
from pathlib import Path

def audit(manifest,root):
    root=Path(root).resolve(); errors=[]; files=[]; ids=set()
    claims=manifest.get('claims')
    if not isinstance(claims,list) or not claims: raise ValueError('Nonempty claims required')
    for c in claims:
        cid=c['id']
        if cid in ids: errors.append({'claim':cid,'error':'duplicate claim id'})
        ids.add(cid)
        kind=c['claim_type']; role=c['dataset_role']
        if kind not in ('calibration','prediction','solver-verification','mechanism','unverified'):
            errors.append({'claim':cid,'error':'unknown claim type'})
        if kind=='prediction' and role!='holdout':
            errors.append({'claim':cid,'error':'prediction requires declared holdout evidence'})
        if not c.get('artifacts'): errors.append({'claim':cid,'error':'no artifacts'})
        for a in c.get('artifacts',[]):
            rel=Path(a['path']); path=(root/rel).resolve()
            if rel.is_absolute() or not path.is_relative_to(root):
                errors.append({'claim':cid,'error':'artifact outside root'}); continue
            if not path.is_file():
                errors.append({'claim':cid,'path':str(rel),'error':'missing file'}); continue
            hasher=hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda:stream.read(1024*1024),b''): hasher.update(block)
            digest=hasher.hexdigest()
            if a.get('sha256') and a['sha256']!=digest:
                errors.append({'claim':cid,'path':str(rel),'error':'hash mismatch'})
            files.append({'claim':cid,'path':str(rel),'sha256':digest,'bytes':path.stat().st_size})
    return {'traceability_pass':not errors,'files':files,'errors':errors,
            'scope':'Artifact integrity and declared dataset roles only; no truth or completeness certification'}

if __name__=='__main__':
    try:
        if len(sys.argv)!=3: raise ValueError('Usage: check_evidence.py manifest.json root-directory')
        result=audit(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')),sys.argv[2])
        print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(0 if result['traceability_pass'] else 1)
    except (KeyError,ValueError,TypeError,OSError) as e:
        print(json.dumps({'traceability_pass':False,'error':str(e)})); sys.exit(2)
