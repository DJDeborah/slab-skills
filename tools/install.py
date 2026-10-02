"""Copy complete skills without replacing existing directories; standard library only."""
import argparse,shutil
from pathlib import Path

NAMES=tuple(sorted(p.name for p in (Path(__file__).resolve().parents[1]/'skills').iterdir() if (p/'SKILL.md').is_file()))
def install(source,dest,names):
    dest=dest.resolve();source=source.resolve();targets=[dest/n for n in names]
    if len(names)!=len(set(names)):raise ValueError('duplicate skill selection')
    if dest==source or dest.is_relative_to(source):raise ValueError('destination must be outside package skills source')
    for n,t in zip(names,targets):
        if n not in NAMES or not (source/n/'SKILL.md').is_file():raise ValueError('unknown or missing skill: '+n)
        if t.exists():raise FileExistsError('Refusing to overwrite '+str(t))
    dest.mkdir(parents=True,exist_ok=True);created=[]
    try:
        for n,t in zip(names,targets):shutil.copytree(source/n,t,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));created.append(t)
    except Exception:
        for t in created:shutil.rmtree(t)
        raise
    return [str(t) for t in targets]
if __name__=='__main__':
    p=argparse.ArgumentParser();scope=p.add_mutually_exclusive_group(required=True);scope.add_argument('--project');scope.add_argument('--user',action='store_true');scope.add_argument('--dest');p.add_argument('--skill',action='append',choices=NAMES);a=p.parse_args()
    dest=Path(a.dest) if a.dest else (Path(a.project)/'.agents'/'skills' if a.project else Path.home()/'.agents'/'skills')
    for target in install(Path(__file__).resolve().parents[1]/'skills',dest,a.skill or NAMES):print('Installed '+target)
    print('Use a new Codex task/turn and invoke $skill-name. Script helpers require Python 3.10+.')
