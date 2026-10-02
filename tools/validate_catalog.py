"""Validate skill identity/UI resources and the maintained catalogue. Requires PyYAML."""
import argparse,json,re,sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
def validate():
    errors=[];records=[];catalog=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'));entries={x['name']:x for x in catalog['skills']}
    for folder in sorted((ROOT/'skills').iterdir()):
        if not folder.is_dir():continue
        entry=folder/'SKILL.md'
        if not entry.is_file():errors.append('missing SKILL.md: '+folder.name);continue
        text=entry.read_text(encoding='utf-8');m=re.match(r'^---\s*\n(.*?)\n---\s*\n',text,re.S)
        if not m:errors.append('missing frontmatter: '+folder.name);continue
        try:meta=yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:errors.append('invalid YAML: '+folder.name);continue
        if meta.get('name')!=folder.name or not re.fullmatch(r'[a-z0-9-]{1,64}',folder.name):errors.append('invalid name: '+folder.name)
        if not isinstance(meta.get('description'),str) or not meta['description'].strip():errors.append('missing description: '+folder.name)
        ui=folder/'agents/openai.yaml'
        if not ui.is_file():errors.append('missing Codex UI metadata: '+folder.name)
        else:
            interface=yaml.safe_load(ui.read_text(encoding='utf-8')).get('interface',{})
            if not 25<=len(interface.get('short_description',''))<=64:errors.append('UI short_description length: '+folder.name)
            if '$'+folder.name not in interface.get('default_prompt',''):errors.append('missing invocation: '+folder.name)
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if not link.startswith(('https://','http://','#')):
                target=(folder/link).resolve()
                if not target.is_relative_to(folder.resolve()) or not target.is_file():errors.append('broken/escaping reference: '+folder.name+'/'+link)
        if folder.name not in entries:errors.append('skill absent from catalogue: '+folder.name)
        records.append({'name':folder.name,'scripts':len(list((folder/'scripts').glob('*.py'))) if (folder/'scripts').exists() else 0,'references':len(list((folder/'references').glob('*'))) if (folder/'references').exists() else 0})
    if len(entries)!=len(catalog['skills']):errors.append('duplicate catalogue identity')
    if set(entries)!={r['name'] for r in records}:errors.append('catalogue contains nonexistent skills')
    for e in entries.values():
        for k in ('category','summary_zh','license','runtime','verification','source'):
            if not e.get(k):errors.append('catalogue missing '+k+': '+e['name'])
    return {'pass':not errors,'skills':records,'errors':errors,'scope':'Installable structure and resource linkage only; not agent/scientific effectiveness.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out');a=p.parse_args();result=validate();text=json.dumps(result,indent=2,ensure_ascii=False)
    if a.out:Path(a.out).write_text(text+'\n',encoding='utf-8')
    print(text);raise SystemExit(0 if result['pass'] else 2)
