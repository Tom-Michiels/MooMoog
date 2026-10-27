from pathlib import Path
import math,json
R=Path(__file__).resolve().parents[1];O=R/'mechanical/split-r0.5';m=json.loads((R/'hardware/split-r0.5/design-master.json').read_text());D=172*math.cos(math.radians(15))+6;front=48-3*math.tan(math.radians(15));back=48+(D-3)*math.tan(math.radians(15));W=233.6

def svg(name,w,h,items):
 text=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}"><g fill="none" stroke="red" stroke-width="0.05">'+''.join(items)+'</g></svg>'
 (O/(name+'.svg')).write_text(text)
svg('PMMA-front-CUT-PROVISIONAL',W,front-3.5,[f'<rect x="0" y="0" width="{W}" height="{front-3.5}"/>'])
items=[f'<rect x="0" y="0" width="{W}" height="{back-3.5}"/>']
for x in [52,64]:items.append(f'<rect x="{x-16.2-5}" y="{back-3.5-(16-3.3)-6}" width="10" height="6"/>')
for x,z in [(172,14.1),(201,20.7)]:items.append(f'<circle cx="{x-16.2}" cy="{back-3.5-(z-3.3)}" r="3.6"/>')
# These files use bottom-left-like engineering coordinates, mark orientation in accompanying README.
svg('PMMA-rear-CUT-PROVISIONAL',W,back-3.5,items)
items=[f'<rect x="0" y="0" width="{W}" height="{D-6.4}"/>']
for x in range(95,170,8):items.append(f'<rect x="{x-16.2}" y="{60-3.2}" width="3" height="25"/>')
for x,y in m['boards']['core']['holes']:items.append(f'<circle cx="{x+28-16.2}" cy="{D-7-y-3.2}" r="1.8"/>')
svg('PMMA-bottom-CUT-PROVISIONAL',W,D-6.4,items)
svg('wood-side-outline-REFERENCE',D,back,[f'<path d="M0,0 L{D},0 L{D},{back} L0,{front} Z"/>'])
(O/'dimensions.json').write_text(json.dumps(dict(board_control_mm=[220,150,1.6],board_core_mm=[210,90,1.6],aluminium_panel_mm=[246,172,1],wood_sides_mm=[18,D,back],pmma_front_mm=[W,front-3.5,3],pmma_rear_mm=[W,back-3.5,3],pmma_bottom_mm=[W,D-6.4,3],outside_width_mm=266,outside_depth_mm=D,wood_front_height_mm=front,wood_rear_height_mm=back,slope_deg=15,connector_openings_verified=False),indent=2))
