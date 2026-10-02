import argparse,json,hashlib
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('--results',type=Path,required=True);a.add_argument('--source-root',type=Path);args=a.parse_args();r=json.loads(args.results.read_text(encoding='utf-8'))
checks=r.get('checks',[])
if not checks or any(c.get('passed') is not True for c in checks):raise SystemExit('Missing or failed computed checks')
if args.source_root:
    for name,expected in r['source_hashes'].items():
        p=(args.source_root/name).resolve();root=args.source_root.resolve()
        if not p.is_relative_to(root) or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise SystemExit('Source hash mismatch: '+name)
print(json.dumps({'checks_passed':len(checks),'hashes_checked':bool(args.source_root),'scope':r['scope']}))
