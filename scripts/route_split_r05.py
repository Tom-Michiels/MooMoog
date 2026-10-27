"""Reuse the checked R04 router on known pads only; board must be freshly generated before apply."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1];mode,bd=sys.argv[1:3];assert bd in ['control','core'];O=R/'hardware/split-r0.5'/bd;(O/'reports').mkdir(exist_ok=True)
source={'export':'export_route_r04.py','route':'route_known_r04.py','apply':'apply_routes_r04.py'}[mode]
s=(R/'scripts'/source).read_text().replace('hardware/compact-r0.4','hardware/split-r0.5/'+bd).replace('compact.kicad_pcb',bd+'.kicad_pcb')
if bd=='core':s=s.replace('W=881;H=601','W=841;H=361')
exec(compile(s,source,'exec'))
