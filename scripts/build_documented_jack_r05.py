"""Prepare a sourced replacement footprint; not yet integrated into the assembly."""
from pathlib import Path
import json
import pcbnew as pcb
R = Path(__file__).resolve().parents[1]
O = R / 'hardware/split-r0.5/core/libraries/Documented.pretty'
O.mkdir(parents=True, exist_ok=True)
fp = pcb.FOOTPRINT(None)
name = 'SameSky_SJ1-3523N_Datasheet_2024'
fp.SetFPID(pcb.LIB_ID('Documented', name))
fp.SetReference('JMAIN')
fp.SetValue('SJ1-3523N')
def v(x,y): return pcb.VECTOR2I(pcb.FromMM(x), pcb.FromMM(y))
for number, x,y,dx,dy in [('1',0,0,1.5,.8), ('2',-5,5,.8,1.5), ('3',5,5,.8,1.5)]:
    p=pcb.PAD(fp);p.SetNumber(number);p.SetAttribute(pcb.PAD_ATTRIB_PTH)
    p.SetShape(pcb.PAD_SHAPE_OVAL);p.SetDrillShape(pcb.PAD_DRILL_SHAPE_OBLONG)
    p.SetDrillSize(v(dx,dy));p.SetSize(v(dx+.8,dy+.8))
    p.SetLayerSet(pcb.LSET.AllCuMask());p.SetPosition(v(x,y));fp.Add(p)
for x,y in [(-5,-2.5),(-5,0),(5,-2.5),(5,0),(0,5)]:
    p=pcb.PAD(fp);p.SetAttribute(pcb.PAD_ATTRIB_NPTH);p.SetShape(pcb.PAD_SHAPE_CIRCLE)
    p.SetDrillSize(v(1.2,1.2));p.SetSize(v(1.2,1.2));p.SetLayerSet(pcb.LSET.AllCuMask())
    p.SetPosition(v(x,y));fp.Add(p)
for corners in [[(-6,-3.5),(6,-3.5),(6,7.5),(-6,7.5)], [(-3,-6.8),(3,-6.8),(3,-3.5),(-3,-3.5)]]:
    for start,end in zip(corners,corners[1:]+corners[:1]):
        s=pcb.PCB_SHAPE(fp);s.SetShape(pcb.SHAPE_T_SEGMENT);s.SetStart(v(*start));s.SetEnd(v(*end))
        s.SetLayer(pcb.F_Fab);s.SetWidth(pcb.FromMM(.1));fp.Add(s)
pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(O),fp)
data = {
 'part':'Same Sky SJ1-3523N', 'status':'DOCUMENTED_CANDIDATE_NOT_ASSEMBLY_INTEGRATED',
 'source':'https://www.sameskydevices.com/product/resource/sj1-352xn.pdf',
 'drawing_date':'2024-09-12','drawing_page':2,
 'pin_mapping':{'1':'SLEEVE/GND','2':'TIP/MAIN_LINE','3':'RING/MAIN_LINE'},
 'origin':'sleeve terminal; top view; mouth towards negative Y',
 'body_mm':[12,11,5], 'nose_length_mm':3.3,'nose_diameter_mm':6,
 'mating_axis_height_above_body_base_mm':2.5,
 'remaining_design_work':[
   'Integrate board edge/notch under nose, which extends below body base.',
   'Position jack so plug body clears the 3 mm PMMA rear panel.',
   'Update main board, schematic, enclosure aperture and CAD together.',
   'Route output and ground after integration; do not substitute generic PJ307.',
 ],
 'procurement':'No exact Amazon.de listing confirmed; buy the exact manufacturer part from an electronics distributor.'
}
(O.parent/'main-jack-candidate.json').write_text(json.dumps(data,indent=2)+'\n')
print('Saved documented footprint and pin mapping; not installed on active PCB.')
