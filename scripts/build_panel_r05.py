from pathlib import Path
import json,math,html
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import cairosvg
R=Path(__file__).resolve().parents[1];O=R/'mechanical/split-r0.5';m=json.loads((R/'hardware/split-r0.5/design-master.json').read_text());art=[];texts=[]
font=TTFont('/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf');glyphs=font.getGlyphSet();cmap=font.getBestCmap();units=font['head'].unitsPerEm

def text(s,x,y,size=1.6):
 names=[cmap.get(ord(c),'.notdef') for c in s];width=sum(font['hmtx'][n][0] for n in names)*size/units;x-=width/2
 for n in names:
  pen=SVGPathPen(glyphs);tp=TransformPen(pen,(size/units,0,0,-size/units,x,y));glyphs[n].draw(tp);d=pen.getCommands()
  if d:art.append(f'<path d="{d}"/>')
  x+=font['hmtx'][n][0]*size/units
 texts.append(dict(text=s,size=size))
def line(x1,y1,x2,y2,width=.18):art.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="currentColor" stroke-width="{width}"/>')
for x in [27,90.5,132,197]:line(x,0,x,148,.35)
for x0,x1,name in [(0,27,'CONTROLLERS'),(27,90.5,'OSCILLATOR BANK'),(90.5,132,'MIXER'),(132,197,'MODIFIERS'),(197,220,'OUTPUT')]:
 text(name,(x0+x1)/2,5,2.25);line(x0+1,8,x1-1,8,.45)
for c in m['controls']:
 x,y=c['x'],c['y'];param=c['param']
 for j in range(11):
  a=math.radians(135+j*27);r=8.25;rr=8.85
  if j%2==1 and not (param.endswith('.wave') or param.endswith('.range')):line(x+math.cos(a)*r,y+math.sin(a)*r,x+math.cos(a)*rr,y+math.sin(a)*rr,.17)
  if j%2==0 and not (param.endswith('.wave') or param.endswith('.range')):text(str(j),x+math.cos(a)*9.3,y+math.sin(a)*9.3+.45,1.15)
 if param.endswith('.range'):
  for j,t in enumerate(['LO',"32'","16'","8'","4'","2'"]):
   a=math.radians(135+j*54);text(t,x+math.cos(a)*9.3,y+math.sin(a)*9.3+.4,1.05)
 if param.endswith('.wave'):
  for j in range(6):
   a=math.radians(135+j*54);xx=x+math.cos(a)*9.3;yy=y+math.sin(a)*9.3
   pts=[ [(-1,.5),(0,-.5),(1,.5)], [(-1,.5),(0,-.5),(0,.5),(1,-.5)], [(-1,.5),(1,-.5),(1,.5)], [(-1,.5),(-1,-.5),(0,-.5),(0,.5),(1,.5)], [(-1,.5),(-1,-.5),(-.4,-.5),(-.4,.5),(1,.5)], [(-1,.5),(-1,-.5),(-.7,-.5),(-.7,.5),(1,.5)] ][j]
   for p,q in zip(pts,pts[1:]):line(xx+p[0],yy+p[1],xx+q[0],yy+q[1],.14)
 label=c['label']
 if label in ['CUTOFF FREQUENCY','AMOUNT OF CONTOUR','MODULATION MIX','NOISE VOLUME']:
  parts={'CUTOFF FREQUENCY':['CUTOFF','FREQUENCY'],'AMOUNT OF CONTOUR':['AMOUNT OF','CONTOUR'],'MODULATION MIX':['MODULATION','MIX'],'NOISE VOLUME':['NOISE','VOLUME']}[label]
  for i,t in enumerate(parts):text(t,x,y+13+i*1.8,1.5)
 else:text(label,x,y+13.5,1.5)
for i,y in enumerate([28,68,108],1):
 text('OSCILLATOR '+str(i),59,y-15,1.7)
 if i==1:text('COMPACT',59,28,2.5);text('MODEL D',59,32,2)
for s in m['switches']:
 x,y=s['x'],s['y'];i=int(s['ref'][1:])
 if i not in [2,3,4,5,6,13]:
  tx=x-5.4 if i==5 else x+5.4
  text('ON',tx,y-1.5,1);text('OFF',tx,y+2,1)
 labels={1:'OSC MOD',2:'OSC3 / EG',3:'NOISE / LFO',4:'GLIDE',5:'DECAY',6:'LFO SHAPE',7:'OSC3 KBD',13:'WHITE / PINK',14:'FILTER MOD',15:'KEYTRACK 1',16:'KEYTRACK 2',17:'MAIN OUTPUT',18:'A-440'}
 if i in labels:text(labels[i],x,y+8,1.25)
text('FILTER',163,13,2)
text('FILTER CONTOUR',163,58,1.6)
text('LOUDNESS CONTOUR',163,96,1.7)

text('POWER',208,141,1.3)
text('compact d',163,132,5)
text('DIGITAL MONOPHONIC SYNTHESIZER',163,137,1.4)
import re
logo=(O/'assets/maakleerplek-official.svg').read_text()
inner=re.sub(r'^<svg[^>]*>|</svg>$','',logo.strip())
art.append('<g transform="translate(143,142) scale(.8163265)" fill-rule="evenodd">'+inner+'</g>')

# The PCB coordinates and engraving share origin (0,0) at PCB top left.
head='<svg xmlns="http://www.w3.org/2000/svg" width="246mm" height="172mm" viewBox="-13 -11 246 172">'
preview=head+'<rect x="-13" y="-11" width="246" height="172" fill="#141719"/><g fill="#eeeeea" color="#eeeeea">'+''.join(art)+'</g></svg>'
(O/'panel-preview.svg').write_text(preview)
(O/'panel-engraving-paths.svg').write_text(head+'<g fill="black" color="black">'+''.join(art)+'</g></svg>')
cut=['<rect x="-13" y="-11" width="246" height="172"/>']
for c in m['controls']:cut.append(f'<circle cx="{c["x"]}" cy="{c["y"]}" r="3.6"/>')
for s in m['switches']:cut.append(f'<rect x="{s["x"]-2.7}" y="{s["y"]-5.25}" width="5.4" height="10.5" rx=".5"/>')
for x,y in m['panel_holes']+[[208,135]]:cut.append(f'<circle cx="{x}" cy="{y}" r="1.6"/>')
(O/'panel-cut-PROVISIONAL.svg').write_text(head+'<g fill="none" stroke="red" stroke-width="0.05">'+''.join(cut)+'</g></svg>')
cairosvg.svg2png(bytestring=preview.encode(),write_to=str(O/'panel-preview.png'),output_width=2460,output_height=1720)
(O/'panel-labels.json').write_text(json.dumps(texts,indent=2))
print('Engraving paths, separate provisional cuts and 2300x1600 preview written')
