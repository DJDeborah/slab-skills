"""Draw original model/workflow schematics as PNG for document import."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
def font(size):
    for f in (Path('C:/Windows/Fonts/arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')):
        if f.is_file():return ImageFont.truetype(str(f),size)
    return ImageFont.load_default()
def text(d,xy,s,size=19,color='#14344d'):
    d.text(xy,s,font=font(size),fill=color)

im=Image.new('RGB',(1100,340),'#eef3f8');d=ImageDraw.Draw(im)
text(d,(40,22),'Registered elastic B21 cantilever',26)
d.line((130,95,130,265),fill='#14344d',width=8)
for y in range(110,261,30):d.line((96,y,130,y-15),fill='#607e91',width=3)
d.rectangle((134,158,914,180),fill='#178b85')
for x in (134,914):d.ellipse((x-8,161,x+8,177),fill='#14344d')
text(d,(175,90),'ROOT: U1 = U2 = UR3 = 0',21)
text(d,(710,80),'TIP: prescribed U2(t)',21)
text(d,(710,110),'Smooth Step, 0 to delta',17)
d.line((914,188,914,242,904,228),fill='#b24d29',width=4);d.line((914,242,924,228),fill='#b24d29',width=4)
text(d,(140,274),'x = 0');text(d,(800,274),'x = L; selectors move with L',18)
text(d,(370,204),'section b x h; I = b h^3 / 12',18)
text(d,(40,313),'Schematic. Named-set counts are checked before solving.',15)
im.save(ROOT/'docs/assets/beam-boundaries.png')

im=Image.new('RGB',(1100,280),'#102d3a');d=ImageDraw.Draw(im)
text(d,(35,20),'Reproducible parameter study',25,'#eef8f5')
for x,title,detail in [(30,'UI / JSON','units, geometry, axes'),(245,'Register + freeze','named sets, SHA256'),(460,'Serial solve','caps, timeout, attempts'),(675,'Extract + audit','STA / ODB / energy'),(890,'Evidence + resume','hashes + status')]:
    d.rounded_rectangle((x,85,x+180,185),radius=12,fill='#214b58',outline='#4d9298',width=2)
    text(d,(x+12,112),title,18,'#eef8f5');text(d,(x+12,148),detail,13,'#aed8d8')
    if x<890:d.line((x+184,134,x+207,134,x+200,127),fill='#e3af65',width=3);d.line((x+207,134,x+200,141),fill='#e3af65',width=3)
text(d,(35,215),'Reuse the workflow; implement and verify the physics adapter for each new model.',17,'#eef8f5')
im.save(ROOT/'docs/assets/parametric-workflow.png')
print('Rendered model/workflow PNGs.')
