from pathlib import Path
import json,xml.etree.ElementTree as ET,math,collections
R=Path(__file__).resolve().parents[1];O=R/'hardware/split-r0.5';m=json.loads((O/'design-master.json').read_text());report={}
for bd in ['control','core']:
 members=[c for c in m['components'] if c['board']==bd];root=ET.parse(O/'reports'/f'{bd}-netlist.xml').getroot();actual={n.attrib['name'].lstrip('/'): {(v.attrib['ref'],v.attrib['pin']) for v in n.findall('node')} for n in root.findall('./nets/net')};expected={}
 for c in members:
  for p in c['pins']:
   if p['net']:expected.setdefault(p['net'],set()).add((c['ref'],p['number']))
 actual={k:v for k,v in actual.items() if not k.startswith('unconnected-')}
 assert actual==expected,(bd,{k:(actual.get(k),v) for k,v in expected.items() if actual.get(k)!=v})
 drc=json.loads((O/'reports'/f'{bd}-drc.json').read_text());report[bd]=dict(components=len(members),functional_netlist_matches=True,nets=len(expected),unconnected_known_pads=len(drc['unconnected_items']),other_drc=collections.Counter(v['type'] for v in drc['violations']),tracks=(O/bd/(bd+'.kicad_pcb')).read_text().count('(segment'))
assert len(m['scan'])==41 and len(set((x['module'],x['port']) for x in m['scan']))==41
assert not any(s['port'] in ['GPA7','GPB7'] for s in m['scan'])
for bd in ['control','core']:
 c=next(c for c in m['components'] if c['kind']=='ribbon' and c['board']==bd)
 assert [p['net'] for p in c['pins']]==[p['net'] for p in m['ribbon']]
assert not any(c['ref']=='ADC1' or c['kind'] in ['ic','ferrite'] or (c.get('footprint') and '_SMD:' in c['footprint']) for c in m['components'])
assert not any(c['param']=='mix.external' for c in m['controls'])
report['ribbon_pin_mapping_identical']=True;report['added_carrier_smd_parts']=0;report['manufacturing_ready']=False
(O/'reports/functional-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
# Conservative inter-board clearance of actual reconstructed mesh envelopes.
s=json.loads((R/'mechanical/split-r0.5/scene.json').read_text());co=math.cos(math.pi/12);si=math.sin(math.pi/12);bounds=[]
for ob in s['objects']:
 vs=ob['vertices'];tr=ob.get('transform')
 if tr=='control':vs=[(x+23,3+(y+161)*co-(z-16)*si,48+(y+161)*si+(z-16)*co) for x,y,z in vs]
 elif tr=='core':vs=[(x+28,y+s['case_depth']-7,z+10) for x,y,z in vs]
 mn=[min(v[k] for v in vs) for k in range(3)];mx=[max(v[k] for v in vs) for k in range(3)];bounds.append((ob['name'],ob['group'],mn,mx))
pairs=[]
for a in [b for b in bounds if b[1]=='control']:
 for b in [b for b in bounds if b[1]=='core']:
  if all(a[2][k]<=b[3][k] and b[2][k]<=a[3][k] for k in [0,1]):pairs.append((a[2][2]-b[3][2],a[0],b[0]))
minimum=min(pairs);assert minimum[0]>0,minimum
height=max(b[3][2] for b in bounds)-min(b[2][2] for b in bounds)
r=dict(minimum_conservative_interboard_gap_mm=minimum[0],nearest_envelopes=minimum[1:],overall_height_including_knobs_and_feet_mm=height,scope='Reconstructed nominal geometry only; not vendor dimension validation. Conservative axis-aligned boxes between boards; not a full assembly fit or electrical clearance certification.')
(O/'reports/mechanical-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
