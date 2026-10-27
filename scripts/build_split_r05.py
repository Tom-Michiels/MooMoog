from pathlib import Path
import json,math,csv,uuid,copy
import pcbnew as pcb
R=Path(__file__).resolve().parents[1];O=R/'hardware/split-r0.5';old=json.loads((R/'hardware/split-r0.5/sources/r04-design-master.json').read_text())
controls=[c for c in old['controls'] if c['param']!='mix.external'];switches=[s for s in old['switches'] if s['param']!='mix.external_enable'];keep={c['ref'] for c in controls+switches}
cs=[copy.deepcopy(c) for c in old['components'] if c['ref'] in keep or c['ref'] in ['IO1','IO2','IO3','MX1','MX2','MCU1','DAC1','HP1']]
for c in cs:
 c['board']='core' if c['ref'] in ['MCU1','DAC1','HP1'] else 'control'
 c['sheet']=c['board'];c['side']='F' if c['board']=='core' or c['kind'] in ['pot','encoder','switch'] else 'B'
 if c['kind']=='pot':
  for p in c['pins']:
   if p['number']=='WIPER':p['net']=c['ref']+'_W'
 if c['ref']=='MCU1':c['xy']=[30,31]
 if c['ref']=='DAC1':c['xy']=[112,42]
 if c['ref']=='HP1':c['xy']=[174,13]
 if c['ref'].startswith('IO'):c['xy']=[78,{'IO1':32,'IO2':55,'IO3':78}[c['ref']]]
 if c['ref'].startswith('MX'):c['xy']=[69,99 if c['ref']=='MX1' else 121]

def pins(c,values):c['pins']=[dict(number=str(k),name=str(k),net=v) for k,v in values.items()]
ports=[f'GP{b}{i}' for b in 'AB' for i in range(7)];contacts=[]
for c in cs:
 if c['kind']=='encoder':contacts += [(c['ref'],p['number'],p['net']) for p in c['pins'] if p['number'] in ['A','B','SW1']]
for s in switches:contacts.append((s['ref'],'ON',s['ref']+'_ON'))
scan=[dict(control=a,pin=b,net=n,module='IO'+str(i//14+1),port=ports[i%14]) for i,(a,b,n) in enumerate(contacts)]
for c in cs:
 ref=c['ref']
 if ref.startswith('IO'):
  mi=int(ref[2:]);v={'VDD':'3V3','VSS':'GND','SDA':'I2C_SDA','SCL':'I2C_SCL','RESET':'IO_RESET','INTA':'PANEL_IRQ','INTB':None,**{f'A{i}':('3V3' if (mi-1)&(1<<i) else 'GND') for i in range(3)}}
  v.update({p:next((r['net'] for r in scan if r['module']==ref and r['port']==p),None) for p in ports})
  v.update({'GPA7':f'MUX_S{2*(mi-1)}' if mi<3 else None,'GPB7':f'MUX_S{2*(mi-1)+1}' if mi<3 else None});pins(c,v)
  c['notes']='Internal pull-ups enabled for 14 safe inputs; A7/B7 outputs only. IOCON open-drain interrupt. Address straps 0x20..0x22.'
 if ref.startswith('MX'):
  mi=int(ref[2:]);pots=[p for p in controls if p['kind']=='pot'];v={'VCC':'3V3','GND':'GND','SIG':f'POT_ADC{mi}','EN':'GND',**{f'S{i}':f'MUX_S{i}' for i in range(4)}}
  for i in range(16):
   k=(mi-1)*16+i;v[f'C{i}']=pots[k]['ref']+'_W' if k<len(pots) else 'GND'
   if k<len(pots):pots[k].update(mux=ref,channel=i,net=v[f'C{i}'])
  pins(c,v)
 if ref=='MCU1':pins(c,{'5V':'SYS_5V','3V3':'3V3','GND':'GND','GPIO1':'I2C_SDA','GPIO2':'I2C_SCL','GPIO4':'POT_ADC1_FILTER','GPIO5':'POT_ADC2_FILTER','GPIO10':'PANEL_IRQ','GPIO15':'I2S_BCLK','GPIO16':'I2S_LRCLK','GPIO17':'I2S_TX','GPIO40':'HP_EN','GPIO41':'DAC_MUTE_N'});c['notes']='Native USB host uses module ports. Host VBUS / USB-C role / current capability UNVERIFIED. No external USB data branch. Module USB supplies SYS_5V only after power-path verification.'
 if ref=='DAC1':pins(c,{'VIN':'SYS_5V','GND':'GND','BCK':'I2S_BCLK','LCK':'I2S_LRCLK','DIN':'I2S_TX','SCK':'GND','FMT':'GND','XSMT':'DAC_MUTE_N','OUTL':'MAIN_L','OUTR':'MAIN_R'});c['notes']='Stereo jack used as mono duplicated L/R main output. Both channels same synth signal. Software main volume affects headphone feed too; phones knob controls extra analog attenuation.'
 if ref=='HP1':pins(c,{'VCC':'3V3','GND':'GND','L-':'HP_FEED','R-':'HP_FEED','L+':'GND','R+':'GND','CTRL':'HP_EN','DET':None,'OUTL':'PHONES_L','OUTR':'PHONES_R'});c['notes']='Independent phones control requires audio potentiometer on core or alternative firmware DAC split. See architecture decision: default retains digital split, DAC jack NOT main jack.'
# Retain existing digital independent mono busses, with separate main jack. No audio runs through ribbon.
dac=next(c for c in cs if c['ref']=='DAC1');pins(dac,{'VIN':'SYS_5V','GND':'GND','BCK':'I2S_BCLK','LCK':'I2S_LRCLK','DIN':'I2S_TX','SCK':'GND','FMT':'GND','XSMT':'DAC_MUTE_N','OUTL':'MAIN_RAW','OUTR':'PHONES_RAW'});dac['notes']='L=main mono, R=phones mono independently scaled in firmware. Built-in DAC stereo jack unused and internal. H3 strap must not fight XSMT GPIO.'
next(c for c in cs if c['ref']=='HP1')['notes']='3V3 supply; L-/R- input, L+/R+ ground. Onboard phones jack used. Verify coupling and gain.'

def add(ref,value,kind,board,xy,size,values,fp=None,side=None,notes=''):
 c=dict(ref=ref,value=value,kind=kind,board=board,sheet=board,xy=xy,size=size,side=side or ('B' if board=='control' else 'F'),footprint=fp,notes=notes);pins(c,values);cs.append(c);return c
# Few supporting parts, all through-hole on carrier; modules retain their factory SMD components.
parts=[('RP1','1k','control',[200,124],'PWR_LED','GND'),('RP2','10k','control',[114,24],'IO_RESET','3V3'),('RP3','2k2 DNP','control',[114,30],'I2C_SDA','3V3'),('RP4','2k2 DNP','control',[114,36],'I2C_SCL','3V3'),('RP5','10k','core',[67,57],'PANEL_IRQ','3V3'),('RA1','1k','core',[67,67],'POT_ADC1','POT_ADC1_FILTER'),('RA2','1k','core',[67,77],'POT_ADC2','POT_ADC2_FILTER'),('RA3','100R','core',[139,35],'MAIN_RAW','MAIN_LINE'),('RA4','10k','core',[145,54],'PHONES_RAW','HP_FEED'),('RA5','4k7','core',[145,62],'HP_FEED','GND'),('RA6','100k','core',[110,54],'DAC_MUTE_N','GND'),('RA7','100k','core',[110,62],'HP_EN','GND')]
for ref,val,bd,xy,a,b in parts:add(ref,val,'R',bd,xy,[6.3,2.5],{'1':a,'2':b},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal')
for ref,val,bd,xy,a,b in [('CA1','1nF','core',[54,67],'POT_ADC1_FILTER','GND'),('CA2','1nF','core',[54,77],'POT_ADC2_FILTER','GND'),('CP1','100nF','control',[114,46],'3V3','GND'),('CC1','100nF','core',[65,35],'3V3','GND')]:add(ref,val,'C',bd,xy,[4,3],{'1':a,'2':b},'Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm')
for ref,bd,xy,net in [('CP2','control',[114,56],'3V3'),('CC2','core',[76,35],'SYS_5V')]:add(ref,'10uF 10V','electrolytic',bd,xy,[5,5],{'1':net,'2':'GND'},'Capacitor_THT:CP_Radial_D5.0mm_P2.00mm')
add('LED2','Power LED','led','control',[208,135],[3,3],{'1':'GND','2':'PWR_LED'},'LED_THT:LED_D3.0mm',side='F')
# Cathode to resistor, anode to 3V3: correct above logical assignment.
pins(cs[-1],{'1':'PWR_LED','2':'3V3'})
add('JMAIN','3.5mm MAIN output / MPN pending','connector','core',[144,5],[12,14],{'TIP':'MAIN_LINE','RING':'MAIN_LINE','SLEEVE':'GND'},notes='Physical jack exact pin mapping remains unresolved; no pads invented.')
ribbon=['3V3','GND','I2C_SDA','GND','I2C_SCL','GND','POT_ADC1','GND','POT_ADC2','GND','PANEL_IRQ','GND']
for ref,bd,xy in [('JPANEL','control',[135,139]),('JCORE','core',[95,78])]:add(ref,'12-way soldered ribbon','ribbon',bd,xy,[31,5],{i+1:n for i,n in enumerate(ribbon)},notes='2.54 mm single-row solder pads; 1.27 mm ribbon fans out. Red edge pin 1. Separate strain relief required.')
m=dict(revision='0.5',status='DETAILED_SPLIT_DESIGN_NOT_MANUFACTURING_READY',controls=controls,switches=switches,scan=scan,components=cs,ribbon=[dict(pin=i+1,net=n) for i,n in enumerate(ribbon)],boards={'control':dict(size=[220,150],holes=[[5,5],[110,5],[215,5],[5,145],[110,145],[215,145]]),'core':dict(size=[210,90],holes=[[5,5],[205,5],[5,85],[205,85]])},panel_holes=[[-8,-6],[228,-6],[-8,75],[228,75],[-8,156],[228,156]],case=dict(slope_deg=15,wood_thickness=18,pmma_thickness=3,aluminium_thickness=1,panel=[246,172],outside_width=266,outside_depth=172.139,front_panel_z=48),removed=['audio input','PCM1808','external input mixer pot and switch','overload LED','42 external contact pullups','per-pot RC networks','optional speaker amplifier'],notes=['Schematic functional module terminals are not verified physical pin numbers.','Only purchased part envelopes with supporting evidence are fixed; individual module models are reconstructed approximations.','USB host power path remains unresolved on ARCELI clone.','R0.4 tracks not reused across new board split.'])
(O/'design-master.json').write_text(json.dumps(m,indent=2))
for name,rows in [('ribbon',m['ribbon']),('controls',controls),('switches',switches),('scan',scan)]:
 with (O/(name+'.csv')).open('w') as f:
  keys=list(dict.fromkeys(k for r in rows for k in r));w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
# KiCad actual placements, verified pads only. Reuse verified encoder footprint from R04.
lib=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
def V(x,y):return pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))
for bd,data in m['boards'].items():
 folder=O/bd;(folder/'models').mkdir(exist_ok=True);b=pcb.BOARD();b.SetCopperLayerCount(2);nets={}
 members=[c for c in cs if c['board']==bd]
 for n in sorted({p['net'] for c in members for p in c['pins'] if p['net']}):nets[n]=pcb.NETINFO_ITEM(b,n);b.Add(nets[n])
 w,h=data['size']
 for a,z in [((0,0),(w,0)),((w,0),(w,h)),((w,h),(0,h)),((0,h),(0,0))]:
  sh=pcb.PCB_SHAPE();sh.SetShape(pcb.SHAPE_T_SEGMENT);sh.SetStart(V(*a));sh.SetEnd(V(*z));sh.SetLayer(pcb.Edge_Cuts);sh.SetWidth(pcb.FromMM(.1));b.Add(sh)
 for c in members:
  if c['footprint']:
   f,n=c['footprint'].split(':');fp=pcb.FootprintLoad(str(lib/(f+'.pretty')),n)
  elif c['kind']=='encoder':
   fp=pcb.FootprintLoad(str(O/'control/libraries/Compact.pretty'),c['ref'])
  else:
   fp=pcb.FOOTPRINT(b)
   if c['kind']=='ribbon':
    for i in range(12):
     p=pcb.PAD(fp);p.SetNumber(str(i+1));p.SetAttribute(pcb.PAD_ATTRIB_PTH);p.SetShape(pcb.PAD_SHAPE_CIRCLE);p.SetSize(V(1.9,1.9));p.SetDrillSize(V(1,1));p.SetLayerSet(pcb.LSET.AllCuMask());p.SetPosition(V((i-5.5)*2.54,0));fp.Add(p)
  fp.Models().clear();fp.SetReference(c['ref']);fp.SetValue(c['value']);fp.Reference().SetVisible(False);fp.Value().SetVisible(False)
  for p in fp.Pads():
   net=next((n['net'] for n in c['pins'] if n['number']==p.GetNumber()),None)
   if net:p.SetNet(nets[net])
  for a,z in [((-c['size'][0]/2,-c['size'][1]/2),(c['size'][0]/2,-c['size'][1]/2)),((-c['size'][0]/2,c['size'][1]/2),(c['size'][0]/2,c['size'][1]/2))]:
   sh=pcb.PCB_SHAPE(fp);sh.SetShape(pcb.SHAPE_T_SEGMENT);sh.SetStart(V(*a));sh.SetEnd(V(*z));sh.SetLayer(pcb.F_Fab);sh.SetWidth(pcb.FromMM(.1));fp.Add(sh)
  model=pcb.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/models/'+c['ref']+'.wrl';fp.Add3DModel(model);fp.SetPosition(V(*c['xy']));b.Add(fp)
  if c['side']=='B':fp.Flip(V(*c['xy']),False)
 for i,xy in enumerate(data['holes']):
  fp=pcb.FootprintLoad(str(lib/'MountingHole.pretty'),'MountingHole_3.2mm_M3');fp.SetReference('H'+str(i+1));fp.SetPosition(V(*xy));b.Add(fp)
 for i,xy in enumerate(([[117,133],[153,133]] if bd=='control' else [[77,84],[113,84]])):
  fp=pcb.FootprintLoad(str(lib/'MountingHole.pretty'),'MountingHole_2.2mm_M2');fp.SetReference('HC'+str(i+1));fp.SetPosition(V(*xy));b.Add(fp)
 pcb.SaveBoard(str(folder/(bd+'.kicad_pcb')),b);(folder/(bd+'.kicad_pro')).write_text('{}')
# Functional schematic per board, all net labels explicit; no falsely numbered module pins.
Q=lambda s:json.dumps(str(s));ID=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,'split-r05/'+s))
for bd in m['boards']:
 members=[c for c in cs if c['board']==bd];symbols=[];objs=[];x=25.4;y=25.4;root=ID(bd)
 for c in members:
  height=(len(c['pins'])+1)*2.54
  syms=[]
  for i,p in enumerate(c['pins']):syms.append(f'(pin passive line (at -7.62 {-2.54*(i+1)} 0) (length 2.54) (name {Q(p["number"])} (effects (font (size .8 .8)))) (number {Q(p["number"])} (effects (font (size .8 .8)))))')
  symbols.append(f'(symbol {Q("Split:"+c["ref"])} (pin_names (offset .6)) (in_bom yes) (on_board yes) (property "Reference" {Q(c["ref"])} (at 0 2.54 0) (effects (font (size 1 1)))) (property "Value" {Q(c["value"])} (at 0 0 0) (effects (font (size 1 1)))) (symbol "{c["ref"]}_0_1" (rectangle (start -5.08 0) (end 60.96 {-height}) (stroke (width .2) (type default)) (fill (type background)))) (symbol "{c["ref"]}_1_1" {"".join(syms)}))')
  if y+height>530:x+=101.6;y=25.4
  objs.append(f'(symbol (lib_id {Q("Split:"+c["ref"])}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {ID(c["ref"])}) (property "Reference" {Q(c["ref"])} (at {x+20} {y-6} 0) (effects (font (size 1 1)))) (property "Value" {Q(c["value"])} (at {x+25} {y-2.54} 0) (effects (font (size .85 .85)))) (instances (project {Q(bd)} (path "/{root}" (reference {Q(c["ref"])}) (unit 1)))))')
  for i,p in enumerate(c['pins']):
   xx=x-7.62;yy=round(y+2.54*(i+1),4);objs.append(f'(no_connect (at {xx} {yy}) (uuid {ID(c["ref"]+p["number"]+"nc")}))' if p['net'] is None else f'(global_label {Q(p["net"])} (shape passive) (at {xx} {yy} 0) (effects (font (size .8 .8)) (justify right)) (uuid {ID(c["ref"]+p["number"]+"net")}))')
  y=round(y+math.ceil((height+15.24)/2.54)*2.54,4)
 assert x<800
 (O/bd/(bd+'.kicad_sch')).write_text(f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {root}) (paper "A1") (title_block (title "Compact D R05 / {bd} / functional draft") (rev "0.5 NOT FOR MANUFACTURE")) (lib_symbols {"".join(symbols)}) {"".join(objs)})')
print(json.dumps(dict(components=len(cs),pots=len([c for c in controls if c['kind']=='pot']),encoders=8,switches=len(switches),contacts=len(scan),new_carrier_smd_parts=0,boards=2,ribbon_wires=12,tracks=0)))
