"""Detailed reconstructed component CAD. Not vendor-certified geometry."""
import FreeCAD as A, Part, Mesh, json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];H=R/'hardware/split-r0.5';O=R/'mechanical/split-r0.5';m=json.loads((H/'design-master.json').read_text());V=A.Vector;scene=[];checks=[];component_solids={'control':[],'core':[],'panel':[]};doc=A.newDocument('Compact_D_Split_R05');angle=15;co=math.cos(math.radians(angle));si=math.sin(math.radians(angle));DEP=172*co+6
colors={'green':[.025,.18,.095,1],'blue':[.02,.12,.36,1],'black':[.018,.022,.027,1],'metal':[.62,.65,.68,1],'gold':[.68,.45,.12,1],'white':[.8,.81,.74,1],'tan':[.5,.27,.09,1],'red':[.65,.035,.018,1],'wood':[.27,.11,.04,1],'pmma':[.045,.06,.07,1]}
def box(w,d,h,x=0,y=0,z=0):return Part.makeBox(w,d,h,V(x,y,z))
def cyl(r,h,x=0,y=0,z=0):return Part.makeCylinder(r,h,V(x,y,z))
def panelworld(shape):
 sh=shape.copy();sh.translate(V(0,161,-16));sh.rotate(V(0,0,0),V(1,0,0),15);sh.translate(V(23,3,48));return sh
def coreworld(shape):
 sh=shape.copy();sh.translate(V(28,DEP-7,10));return sh

def record(name,sh,col,group,transform=None):
 assert sh.isValid(),name
 vs,ts=sh.tessellate(.12);entry=dict(name=name,vertices=[[v.x,v.y,v.z] for v in vs],faces=ts,color=colors[col] if isinstance(col,str) else col,group=group)
 if transform:entry['transform']=transform
 scene.append(entry)
 if transform and not name.endswith('_PCB'):component_solids[group].append(panelworld(sh) if transform=='control' else coreworld(sh))
 checks.append(dict(name=name,valid=True,volume=sh.Volume))
 return sh

def document(name,sh):
 ob=doc.addObject('PartDesign::Feature',name);ob.Shape=sh;return ob
# Build parts in local PCB coordinates and retain transform metadata for exploded views.
for bd,data in m['boards'].items():
 w,h=data['size'];sh=box(w,h,1.6,0,-h)
 for x,y in data['holes']:sh=sh.cut(cyl(1.6,2,x,-y,-.2))
 for pa in json.loads((H/'reports/pads.json').read_text())[bd]:
  dx,dy=pa['drill'];x=pa['x'];y=-pa['y']
  if dx and dy:
   if abs(dx-dy)<.01:hole=cyl(dx/2,2,x,y,-.2)
   else:hole=box(dx,dy,2,x-dx/2,y-dy/2,-.2)
   sh=sh.cut(hole)
   if not pa['npth']:
    for zz in [-.025,1.6]:
     ring=cyl(min(pa['size'])/2,.025,x,y,zz).cut(cyl(max(dx,dy)/2,.1,x,y,zz-.01))
     if not ring.isNull() and ring.Volume>0:record('Copper_pad_'+pa['ref']+'_'+pa['pin'],ring,'gold',bd,bd)
 record(bd+'_PCB',sh,'green',bd,bd);document(bd+'_PCB',panelworld(sh) if bd=='control' else coreworld(sh));sh.exportStep(str(O/(bd+'-pcb-outline.step')))
# Detailed component pieces and markings. Pin locations on unknown modules are visual approximations only.
labels=[]
for c in m['components']:
 ref=c['ref'];bd=c['board'];w,d=c['size'];k=c['kind'];pieces=[];local_labels=[]
 def put(sh,col):pieces.append((sh,col))
 def mark(t,x,y,z,size=1):local_labels.append(dict(text=t,x=x,y=y,z=z,size=size))
 def terminal(x,y,z0=0,height=8):
  put(box(2.3,2.3,2.4,x-1.15,y-1.15,z0),'black');put(box(.6,.6,height,x-.3,y-.3,z0-1),'gold')
 def chip(x,y,z,ww,dd,pins=14):
  put(box(ww,dd,1.1,x-ww/2,y-dd/2,z),'black')
  for row in [-1,1]:
   for i in range(pins):put(box(.32,1.1,.22,x+(i-(pins-1)/2)*min(.65,(ww-1)/(pins-1))-.16,y+row*(dd/2+.25)-.55,z+.12),'metal')
  put(cyl(.28,.03,x-ww/2+.65,y+dd/2-.65,z+1.1),'white')
 def smd(x,y,z,ww=1.6,dd=.8,col='black'):
  put(box(ww,dd,.6,x-ww/2,y-dd/2,z),col)
  for s in [-1,1]:put(box(.35,dd,.63,x+s*(ww/2-.17)-.175,y-dd/2,z),'metal')
 def usbc(x,y,z):
  # Connector shell with actual open mouth, black tongue and gold contacts.
  sh=box(9,7,3.2,x-4.5,y-3.5,z).cut(box(7.8,7.2,2.1,x-3.9,y-3.6,z+.55));put(sh,'metal');put(box(6.5,5,.65,x-3.25,y-3.6,z+1.25),'black')
  for i in range(8):put(box(.3,2,.08,x-2.1+i*.6,y-3.7,z+1.9),'gold')
 def jack(x,y,z):
  put(box(8,10,5,x-4,y-5,z),'black');sh=cyl(3,5).cut(cyl(1.8,5.1,0,0,-.05));sh.rotate(V(0,0,0),V(1,0,0),90);sh.translate(V(x,y-5,z+2.5));put(sh,'metal')
 if k in ['encoder','pot']:
  height=7 if k=='encoder' else 10.5
  put(box(w,d,height,-w/2,-d/2),'black' if k=='pot' else 'tan')
  # Folded metal housing with real open sides instead of a solid rectangular block.
  shell=box(w+.2,d+.2,height,-w/2-.1,-d/2-.1).cut(box(w-.8,d+1,height-1,-w/2+.4,-d/2-.5,.3));put(shell,'metal')
  put(cyl(3.5,6,0,0,height),'metal');put(cyl(3,15,0,0,height),'metal')
  for j in range(12):
   a=j*math.pi/6;put(box(.22,.22,6,2.7*math.cos(a),2.7*math.sin(a),height+9),'metal')
  # Anti-rotation tabs and visible connector pins, approximate for unmeasured pots.
  for x,y in ([(-7.5,-2.5),(-7.5,0),(-7.5,2.5),(7,-2.5),(7,2.5)] if k=='encoder' else [(-2.5,-5.8),(0,-5.8),(2.5,-5.8)]):put(box(.6,.65,4,x-.3,y-.325,-3),'metal')
  mark('EC11' if k=='encoder' else 'B10K',0,-d/2+1.4,height+.03,1.1)
 elif k=='switch':
  put(box(w,d,1.1,-w/2,-d/2),'tan');put(box(w,d,5.5,-w/2,-d/2,1.1).cut(box(2,7,1,-1,-3.5,5.7)),'metal');put(box(1.5,3.8,5,-.75,-1.9,6.5),'black')
  for y in [-4,0,4]:put(box(.7,.5,4,-.35,y-.25,-3),'metal')
 elif k=='module':
  z=8 if bd=='control' else 5;board=box(w,d,1.6,-w/2,-d/2,z);put(board,'blue' if ref!='MCU1' else 'black')
  if ref.startswith('IO'):
   for i in range(20):terminal(-17+i*2.54,-6,z-5,8)
   for x in [-29,-26.46]:
    for i in range(7):terminal(x,-7.62+i*2.54,z-5,8)
   chip(9,1,z+1.6,10,5.3,14);mark('MCP23017',9,1,z+2.73,1.2);mark('0x'+str(20+int(ref[-1])-1),22,5,z+1.63,1.3)
   for i in range(5):smd(-10+i*3,4,z+1.6)
   for i in range(3):smd(22+i*3,0,z+1.6,col='tan')
  elif ref.startswith('MX'):
   for i in range(16):terminal((i-7.5)*2.54,-6,z-5,8)
   for i in range(8):terminal((i-3.5)*2.54,6,z-5,8)
   chip(0,0,z+1.6,8,4.4,12);mark('4067',0,0,z+2.73,1.3);smd(14,2,z+1.6,col='tan')
  elif ref=='MCU1':
   for x in [-12.7,12.7]:
    for i in range(22):terminal(x,(i-10.5)*2.54,z-3.5,7)
   # PCB antenna at front, shielded module next to it, twin USB-C at rear.
   put(box(18,25,1,-9,-2,z+1.6),'black');put(box(17.2,18,2.4,-8.6,-1,z+2.6),'metal');mark('ESP32-S3',0,9,z+5.03,2);mark('N16R8',0,5.5,z+5.03,1.25)
   for i in range(5):put(box(1,6,.06,-7+i*3,21,z+2.65),'gold')
   put(box(15,1,.06,-7,26,z+2.65),'gold')
   usbc(-6,-31,z+1.6);usbc(6,-31,z+1.6);chip(0,-15,z+1.6,4,4,8)
   for x in [-8,8]:
    put(box(3.5,3.5,1.5,x-1.75,-21,z+1.6),'metal');put(cyl(1,1,x,-19.25,z+3.1),'black')
   for i in range(9):smd(-8+(i%3)*4,-11+(i//3)*3,z+1.6,col='tan' if i%2 else 'black')
   mark('USB',-6,-23,z+1.65,1);mark('UART',6,-23,z+1.65,1)
  elif ref=='DAC1':
   for i in range(6):terminal(-11,(i-2.5)*2.54,z-3.5,7)
   chip(0,0,z+1.6,9.7,4.4,14);mark('PCM5102',0,0,z+2.75,1.25);jack(8,-5,z+1.6)
   for i in range(8):smd(-7+(i%4)*3,5+(i//4)*3,z+1.6,col='tan' if i%2 else 'black')
   mark('DAC / INTERNAL',0,-10,z+1.65,.8)
  elif ref=='HP1':
   for i in range(6):terminal(-9,(i-2.5)*2.54,z-3.5,7)
   jack(1,-8,z+1.6);chip(1,1,z+1.6,3,3,5);mark('6132',1,1,z+2.75,.8)
   for i in range(8):smd(-5+(i%4)*3,6+(i//4)*3,z+1.6,col='tan' if i%2 else 'black')
   mark('PHONES',2,11,z+1.65,1)
 elif k=='R':
  sh=Part.makeCylinder(1.15,6.3,V(1.93,0,1.3),V(1,0,0));put(sh,'tan')
  for i,col in enumerate(['red','black','black','gold']):put(Part.makeCylinder(1.17,.38,V(2.7+i*1.35,0,1.3),V(1,0,0)),col)
  for x in [0,10.16]:put(cyl(.28,3,x,0,-1.5),'metal');put(Part.makeCylinder(.28,2,V(x if x==0 else x-2,0,1.3),V(1,0,0)),'metal')
 elif k=='C':
  put(box(3,1.6,3,-.25,-.8,1),'tan')
  for x in [0,2.5]:put(cyl(.25,3,x,0,-1),'metal')
 elif k=='electrolytic':
  put(cyl(2.5,6,0,0,1),'black');put(cyl(2.2,.2,0,0,7),'metal');put(box(.2,4,.05,-.1,-2,7.2),'black');put(box(4,.2,.05,-2,-.1,7.2),'black')
  for x in [0,2]:put(cyl(.25,3,x,0,-1),'metal')
 elif k=='led':
  put(cyl(1.5,3,0,0,16),'red');put(Part.makeSphere(1.5,V(0,0,19)),'red')
  for x in [0,2.54]:put(cyl(.25,17,x,0,-1),'metal')
 elif k=='connector':jack(0,-2,0)
 elif k=='ribbon':
  for i in range(12):put(cyl(.95,.08,(i-5.5)*2.54,0,.02).cut(cyl(.5,.2,(i-5.5)*2.54,0,-.02)),'gold')
 if ref in ['MCU1','HP1','JMAIN']:
  for sh,col in pieces:sh.rotate(V(0,0,0),V(0,0,1),180)
  for ll in local_labels:ll['x']=-ll['x'];ll['y']=-ll['y'];ll['angle']=180
 # Save individual detailed WRL models and scene parts in board-local coordinates.
 blocks=['#VRML V2.0 utf8\n']
 for idx,(sh,color) in enumerate(pieces):
  vs,ts=sh.tessellate(.12);col=colors[color];coords=', '.join(' '.join(str(round(t/2.54,6)) for t in (v.x,v.y,v.z)) for v in vs);faces=', '.join(' '.join(map(str,list(t)+[-1])) for t in ts)
  blocks.append('Shape { appearance Appearance { material Material { diffuseColor '+' '.join(map(str,col[:3]))+' } } geometry IndexedFaceSet { coord Coordinate { point [ '+coords+' ] } coordIndex [ '+faces+' ] } }')
  sh=sh.copy()
  if c['side']=='B':sh.rotate(V(0,0,0),V(1,0,0),180)
  sh.translate(V(c['xy'][0],-c['xy'][1],1.6 if c['side']=='F' else 0));record(ref+'_'+str(idx),sh,color,bd,bd)
 (H/bd/'models'/f'{ref}.wrl').write_text('\n'.join(blocks))
 for l in local_labels:
  if c['side']=='B':l['y']=-l['y'];l['z']=-l['z'];l['flip']=True
  l['x']+=c['xy'][0];l['y']-=c['xy'][1];l['z']+=1.6 if c['side']=='F' else 0;l['board']=bd;labels.append(l)
 labels.append(dict(text=ref,x=c['xy'][0],y=-c['xy'][1]+d/2+1.8,z=1.65 if c['side']=='F' else -.05,size=1.2,board=bd,flip=c['side']=='B'))
# Panel with dedicated screw border, never through legends.
panel=box(246,172,1,-13,-161,16)
for c in m['controls']:panel=panel.cut(cyl(3.6,2,c['x'],-c['y'],15.5))
for s in m['switches']:panel=panel.cut(box(5.4,10.5,2,s['x']-2.7,-s['y']-5.25,15.5))
for x,y in m['panel_holes']+[[208,135]]:panel=panel.cut(cyl(1.6,2,x,-y,15.5))
record('Engraved_aluminium_panel',panel,'black','panel','control');document('Aluminium_panel',panelworld(panel));panel.exportStep(str(O/'aluminium-panel-provisional.step'))
for x,y in m['panel_holes']:
 screw=cyl(2.7,1.4,x,-y,17).cut(box(.7,4,.7,x-.35,-y-2,17.8)).cut(box(4,.7,.7,x-2,-y-.35,17.8));record('Panel_screw',screw,'metal','panel','control')
# Previously constructed real knob and printed switch cap geometry.
knob=Part.Shape();knob.read(str(O/'knob-classic-16mm.step'));cap=Part.Shape();cap.read(str(O/'knob-silver-cap.step'))
for c in m['controls']:
 for name,shape,col,z in [('Knob',knob,'black',19),('Cap',cap,'metal',32.35)]:
  sh=shape.copy();sh.translate(V(c['x'],-c['y'],z));record(name+'_'+c['ref'],sh,col,'panel','control')
 record('Pointer_'+c['ref'],box(.6,1.8,.2,c['x']-.3,-c['y']+6,20.15),'white','panel','control')
swc=Part.Shape();swc.read(str(O/'switch-caps/switch-cap-nominal.step'));swc.rotate(V(0,0,0),V(1,0,0),180);swc.translate(V(0,0,12))
for s in m['switches']:
 sh=swc.copy();sh.translate(V(s['x'],-s['y'],10));record('Slider_'+s['ref'],sh,{'orange':[.88,.23,.025,1],'blue':[.08,.32,.6,1],'white':colors['white'],'black':colors['black']}[s['color']],'panel','control')
# CNC wood sides. Sloped ledge supports aluminium; pockets for PMMA panel edges.
front=48-3*math.tan(math.radians(15));back=48+(DEP-3)*math.tan(math.radians(15))
poly=Part.makePolygon([V(0,0,0),V(0,DEP,0),V(0,DEP,back),V(0,0,front),V(0,0,0)]);side=Part.Face(poly).extrude(V(18,0,0))
for name,x in [('left',0),('right',248)]:
 sh=side.copy();sh.translate(V(x,0,0))
 # 3.2 mm-wide internal edge rebates, 2.0 mm depth in wood.
 xx=16 if name=='left' else 248
 for y in [0,DEP-3.2]:sh=sh.cut(box(2,3.2,110,xx,y,0))
 sh=sh.cut(box(2,DEP,3.2,xx,0,3))
 for yy in [5,145]:sh=sh.cut(panelworld(box(238.4,8.4,6.4,-9.2,-yy-4.2,-8.2)))
 # Top panel overlap cut to actual sloping plane and pilot bores normal to slope.
 for py in [-6,75,156]:
  hole=cyl(1.2,14,-8 if name=='left' else 228,-py,3.5);hole=panelworld(hole);sh=sh.cut(hole)
 record('Walnut_'+name,sh,'wood','case');ob=document('CNC_wood_'+name,sh);sh.exportStep(str(O/('wood-'+name+'-CNC.step')));Mesh.export([ob],str(O/('wood-'+name+'.stl')))
# PMMA panels fit rebates with design clearance. Final kerf allowance belongs to fabricator.
frontp=box(233.6,3,front-3.5,16.2,0,3.3);rearp=box(233.6,3,back-3.5,16.2,DEP-3,3.3)
# Connector openings are provisional: native USB + UART; separate main and headphone jack.
for x,wid in [(52,10),(64,10)]:rearp=rearp.cut(box(wid,5,6,x-wid/2,DEP-4,16))
for x,zz in [(172,14.1),(201,20.7)]:
 hole=Part.makeCylinder(3.6,5,V(x,DEP-4,zz),V(0,1,0));rearp=rearp.cut(hole)
bottom=box(233.6,DEP-6.4,3,16.2,3.2,3.2)
for x in range(95,170,8):bottom=bottom.cut(box(3,25,4,x,60,2.7))
# Core support bolts + four feet; rubber washers isolate PMMA from bolt preload.
for x,y in m['boards']['core']['holes']:bottom=bottom.cut(cyl(1.8,4,x+28,DEP-7-y,2.7))
for name,sh in [('PMMA_front',frontp),('PMMA_rear',rearp),('PMMA_bottom',bottom)]:
 record(name,sh,'pmma','case');document(name,sh);sh.exportStep(str(O/(name+'-provisional.step')))
for x in [27,239]:
 for y in [14,DEP-14]:record('Rubber_foot',cyl(6,4,x,y,-4),'black','case')
for x,y in m['boards']['core']['holes']:
 sh=cyl(3,3.8,x+28,DEP-7-y,6.2).cut(cyl(1.6,4,x+28,DEP-7-y,6.1));record('Core_spacer',sh,'metal','case')
# Control PCB fixed on internal rails, independent from visible panel screws.
for yy in [5,145]:
 rail=box(238,8,6,-9,-yy-4,-8)
 for xx in [5,110,215]:rail=rail.cut(cyl(1.6,7,xx,-yy,-8.5))
 record('Control_internal_rail',rail,'metal','control','control')
 if yy==5:
  localrail=rail.copy();localrail.translate(V(9,yy+4,8));localrail.exportStep(str(O/'control-support-rail-238x8x6.step'))
 for xx in [5,110,215]:record('Control_spacer',cyl(3,2,xx,-yy,-2).cut(cyl(1.6,2.2,xx,-yy,-2.1)),'metal','control','control')
# Printed ribbon clamps: 40 x 4 x 4 mm, 36 mm M2 hole spacing, 2 mm cable clearance.
clamp=box(40,4,2,-20,-2,2).fuse(box(4,4,2,-20,-2,0)).fuse(box(4,4,2,16,-2,0))
for xx in [-18,18]:clamp=clamp.cut(cyl(1.1,5,xx,0,-.5))
clamp.exportStep(str(O/'ribbon-strain-relief.step'));pr=clamp.copy();pr.rotate(V(0,0,0),V(1,0,0),180);pr.translate(V(0,0,4));po=document('Ribbon_clamp_print',pr);Mesh.export([po],str(O/'ribbon-strain-relief-print.stl'));doc.removeObject(po.Name)
for bd,x,y in [('control',135,133),('core',95,84)]:
 sh=clamp.copy()
 if bd=='control':sh.rotate(V(0,0,0),V(1,0,0),180)
 sh.translate(V(x,-y,0 if bd=='control' else 1.6));record('Ribbon_clamp_'+bd,sh,'black',bd,bd)
for key,solids in component_solids.items():document('Detailed_'+key+'_assembly',Part.makeCompound(solids))
doc.recompute();doc.saveAs(str(O/'split-assembly.FCStd'));Part.export(doc.Objects,str(O/'split-enclosure-and-boards.step'))
(O/'scene.json').write_text(json.dumps(dict(objects=scene,labels=labels,case_depth=DEP,notes='Detailed reconstructed modules, not verified vendor CAD. No invented copper routing. Physical fit unverified.')))
(O/'geometry-checks.json').write_text(json.dumps(dict(solids=len(checks),all_valid=True,items=checks),indent=2))
print('Detailed CAD:',len(scene),'valid shapes; two boards, aluminium, CNC wood, PMMA panels')
