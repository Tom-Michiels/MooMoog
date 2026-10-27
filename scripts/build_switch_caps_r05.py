"""Printable slide-switch extensions, provisional fit variants for purchased switch."""
import FreeCAD as A, Part, Mesh, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'mechanical/split-r0.5/switch-caps';O.mkdir(exist_ok=True)
m=json.loads((R/'hardware/split-r0.5/design-master.json').read_text());doc=A.newDocument('SwitchCaps');V=A.Vector

def cap(width,length):
 body=Part.makeBox(5,5,12,V(-2.5,-2.5,0))
 socket=Part.makeBox(width,length,4.01,V(-width/2,-length/2,-.01))
 # A small lead-in on the socket mouth; no overhang inside the blind socket.
 entry=Part.makeBox(width+.3,length+.3,.5,V(-(width+.3)/2,-(length+.3)/2,-.01))
 body=body.cut(socket.fuse(entry))
 for y in [-1,0,1]:body=body.cut(Part.makeBox(3,.35,.35,V(-1.5,y-.175,11.7)))
 assert body.isValid() and len(body.Solids)==1
 return body

def printable(shape):
 s=shape.copy();s.rotate(V(0,0,0),V(1,0,0),180);s.translate(V(0,0,12));return s

def export(name,shape):
 ob=doc.addObject('PartDesign::Feature',name.replace('-','_'));ob.Shape=shape
 Mesh.export([ob],str(O/(name+'.stl')));shape.exportStep(str(O/(name+'.step')))
 return ob

variants=[('tight',1.6,4.0),('nominal',1.8,4.1),('loose',2.0,4.2)];report=[];fit=[]
for i,(name,w,l) in enumerate(variants):
 shape=cap(w,l);export('switch-cap-'+name,printable(shape))
 s=printable(shape);s.translate(V(i*9,0,0));fit.append(s)
 report.append(dict(variant=name,socket_mm=[w,l,4],outside_mm=[5,5,12],volume_mm3=shape.Volume,valid=shape.isValid()))
export('fit-set-left-tight-middle-nominal-right-loose',Part.makeCompound(fit))
counts={};full=[]
for color in ['orange','blue','white','black']:
 switches=[s for s in m['switches'] if s['color']==color];counts[color]=len(switches);parts=[]
 for i,s in enumerate(switches):
  p=printable(cap(1.8,4.1));p.translate(V(i%6*9,i//6*9,0));parts.append(p)
  p=printable(cap(1.8,4.1));n=len(full);p.translate(V(n%6*9,n//6*9,0));full.append(p)
 export('nominal-'+color+'-'+str(len(parts))+'-caps',Part.makeCompound(parts))
export('nominal-complete-set-17-caps',Part.makeCompound(full))
doc.recompute();doc.saveAs(str(O/'switch-caps.FCStd'))
(O/'fit-check.json').write_text(json.dumps(dict(variants=report,color_counts=counts,physical_fit_verified=False,print_orientation='Visible top on bed, socket upwards; first print fit set only',panel_slot_mm=[5.4,10.5],lateral_clearance_per_side_mm=.2),indent=2))
print(json.dumps(dict(variants=3,full_set=len(full),color_counts=counts,valid=True,physical_fit_verified=False)))
