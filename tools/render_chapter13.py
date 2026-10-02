"""Render the English handbook chapter; install requirements-docs.txt first."""
from pathlib import Path
import re
import markdown

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'docs/CHAPTER_13_SLAB_SKILLS.md'
md = markdown.Markdown(extensions=['pymdownx.superfences', 'tables', 'toc'])
body = md.convert(source.read_text(encoding='utf-8'))
body = re.sub(r'(<h[12] id="[^"]+">)(13(?:\.\d+)?\.?)\s+', r'\1<span class="section-number">\2</span> ', body)
style = '''
:root{--blue:#1762ff;--ink:#252a30;--muted:#626a74;--line:#e5e7eb}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:30px}
body{margin:0;background:white;color:var(--ink);font:16px/1.65 Arial,Helvetica,sans-serif}
a{color:var(--blue);text-decoration:underline;text-underline-offset:3px}a:hover{color:#083dac}
aside{position:fixed;inset:0 auto 0 0;width:310px;padding:28px 24px;overflow:auto;border-right:1px solid var(--line);background:#fff}
.brand{color:var(--muted);font-size:12px;letter-spacing:.12em;margin-bottom:22px}
aside a{text-decoration:none;font-size:13px;line-height:1.6}aside ul{padding-left:16px;list-style:none}
aside>.toc>ul{padding-left:0}aside li{margin:9px 0}aside>.toc>ul>li>a{font-weight:bold;font-size:14px}
aside>.toc>ul>li>ul>li>ul{display:none}.toolbar{display:flex;gap:20px;font-size:13px;flex-wrap:wrap;margin-bottom:36px}
main{max-width:880px;margin-left:max(345px,calc((100vw - 880px)/2 + 120px));margin-right:35px;padding:44px 18px 90px}
h1{font-size:28px;line-height:1.3;letter-spacing:-.025em;margin:0 0 32px}h2{font-size:23px;line-height:1.4;letter-spacing:-.02em;margin:34px 0 15px}h3{font-size:18px;margin:23px 0 12px}
.section-number{color:var(--blue);margin-right:5px}p{margin:12px 0}ul,ol{padding-left:26px}li{padding-left:3px;margin:11px 0}li::marker{color:var(--blue)}li>p{margin:8px 0}
hr{border:0;border-top:1px solid var(--line);margin:30px 0}
code{font:14px/1.6 Consolas,Menlo,monospace;background:#f5f6f7;border:1px solid #e7e9ec;border-radius:4px;padding:2px 5px;overflow-wrap:anywhere}
pre{position:relative;background:#f7f8fa;border:1px solid var(--line);border-radius:6px;padding:38px 16px 16px;overflow-x:auto;line-height:1.55;margin:14px 0;white-space:pre}
pre code{padding:0;background:none;border:0;overflow-wrap:normal;font-size:13px}.copy{position:absolute;right:9px;top:7px;border:1px solid #d8dde4;border-radius:4px;background:white;color:#4d5c70;padding:3px 8px;font:12px Arial;cursor:pointer}
table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px}th,td{border:1px solid var(--line);text-align:left;padding:9px 12px;vertical-align:top}th{background:#f7f8fa}table code{font-size:12px}
img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px;margin:8px 0}footer{color:var(--muted);font-size:12px;margin-top:38px;border-top:1px solid var(--line);padding-top:14px}
@media(max-width:1000px){aside{width:250px;padding:24px 16px}main{margin-left:270px;margin-right:15px;padding-left:0;padding-right:0}}
@media(max-width:720px){aside{position:static;width:auto;max-height:245px;border-right:0;border-bottom:1px solid var(--line)}main{margin:0;padding:30px 20px}h1{font-size:25px}h2{font-size:21px}pre{margin-left:-3px;margin-right:-3px}table{display:block;overflow:auto}}
@media print{aside,.toolbar,.copy{display:none}main{margin:0;max-width:none;padding:0}pre{white-space:pre-wrap;break-inside:avoid}a{color:inherit}h2{break-after:avoid}img{max-height:620px;object-fit:contain}}
'''
script = '''
for(const pre of document.querySelectorAll('pre')){const button=document.createElement('button');button.className='copy';button.textContent='Copy';button.type='button';button.setAttribute('aria-label','Copy code block');button.addEventListener('click',async()=>{const code=pre.querySelector('code');try{await navigator.clipboard.writeText(code.textContent);button.textContent='Copied'}catch(error){const range=document.createRange();range.selectNodeContents(code);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);button.textContent='Press Ctrl+C'}});pre.append(button)}
'''
page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>13. SLAB Skills — Practical Setup and Sharing Guide</title><style>'+style+'</style></head><body><aside aria-label="Chapter contents"><div class="brand">SLAB / PRACTICAL HANDBOOK</div>'+md.toc+'</aside><main><nav class="toolbar"><a href="../index.html">Skill directory</a><a href="https://github.com/DJDeborah/slab-skills">GitHub repository</a><a href="CHAPTER_13_SLAB_SKILLS.md" download>Download Markdown</a></nav>'+body+'<footer>Chapter 13 · English practical guide · Documentation added 2026-10-02. Version-specific measurements refer to v0.1.0.</footer></main><script>'+script+'</script></body></html>'
target=ROOT/'docs/chapter13.html'
target.write_text(page,encoding='utf-8')
print('Rendered '+str(target))
