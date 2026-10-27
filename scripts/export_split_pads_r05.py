import pcbnew as p,json
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'hardware/split-r0.5'
result={};tracks={}
for bd in ['control','core']:
 b=p.LoadBoard(str(O/bd/(bd+'.kicad_pcb')));pads=[]
 for f in b.GetFootprints():
  for a in f.Pads():
   pads.append(dict(ref=f.GetReference(),pin=a.GetNumber(),x=p.ToMM(a.GetPosition().x),y=p.ToMM(a.GetPosition().y),size=[p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)],drill=[p.ToMM(a.GetDrillSize().x),p.ToMM(a.GetDrillSize().y)],npth=a.GetAttribute()==p.PAD_ATTRIB_NPTH))
 tracks[bd]=[]
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):
   pads.append(dict(ref='VIA',pin='',x=p.ToMM(t.GetPosition().x),y=p.ToMM(t.GetPosition().y),size=[p.ToMM(t.GetWidth())]*2,drill=[p.ToMM(t.GetDrillValue())]*2,npth=False))
  else:tracks[bd].append(dict(start=[p.ToMM(t.GetStart().x),p.ToMM(t.GetStart().y)],end=[p.ToMM(t.GetEnd().x),p.ToMM(t.GetEnd().y)],width=p.ToMM(t.GetWidth()),layer='top' if t.GetLayer()==p.F_Cu else 'bottom',net=t.GetNetname()))
 result[bd]=pads
(O/'reports/pads.json').write_text(json.dumps(result))

(O/'reports/tracks.json').write_text(json.dumps(tracks))
