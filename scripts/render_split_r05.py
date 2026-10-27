import bpy,bmesh,json,math
from mathutils import Vector,Matrix
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'mechanical/split-r0.5';H=R/'hardware/split-r0.5/previews';s=json.loads((O/'scene.json').read_text());bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);mats={};groups={};parents={};DEP=s['case_depth'];rot=Matrix.Rotation(math.radians(15),4,'X');trans=Matrix.Translation((23,3,48))@rot@Matrix.Translation((0,161,-16))
for name in ['control','core','panel']:
 ob=bpy.data.objects.new(name+'_assembly',None);bpy.context.collection.objects.link(ob);ob.matrix_world=Matrix.Translation((28,DEP-7,10)) if name=='core' else trans;parents[name]=ob

def mat(col,name=''):
 key=name or str(col)
 if key not in mats:
  m=bpy.data.materials.new(key);m.diffuse_color=col;m.use_nodes=True;n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.38
  if name=='metal' or col[0]>.6 and abs(col[0]-col[1])<.08:p.inputs['Metallic'].default_value=.8;p.inputs['Roughness'].default_value=.26
  if name=='wood':
   tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=5;tex.inputs['Detail'].default_value=5;tex.inputs['Roughness'].default_value=.7
   coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(18,.25,5);m.node_tree.links.new(coord.outputs['Generated'],mapping.inputs[0]);m.node_tree.links.new(mapping.outputs['Vector'],tex.inputs['Vector'])
   ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.2;ramp.color_ramp.elements[0].color=(.055,.018,.006,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(.36,.17,.065,1);m.node_tree.links.new(tex.outputs['Fac'],ramp.inputs[0]);m.node_tree.links.new(ramp.outputs['Color'],p.inputs['Base Color'])
   bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.12;m.node_tree.links.new(tex.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs[0],p.inputs['Normal']);p.inputs['Roughness'].default_value=.32
  if name=='PMMA':p.inputs['Roughness'].default_value=.16;p.inputs['Coat Weight'].default_value=.45;p.inputs['IOR'].default_value=1.49;p.inputs['Transmission Weight'].default_value=.12
  mats[key]=m
 return mats[key]
for v in s['objects']:
 mesh=bpy.data.meshes.new(v['name']);mesh.from_pydata(v['vertices'],[],v['faces']);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();ob=bpy.data.objects.new(v['name'],mesh);bpy.context.collection.objects.link(ob)
 materialname='wood' if v['name'].startswith('Walnut') else 'PMMA' if v['name'].startswith('PMMA') else ''
 ob.data.materials.append(mat(v['color'],materialname));groups[ob.name]=v['group']
 if v.get('transform'):ob.parent=parents['panel' if v['group']=='panel' else v['transform']]
 if not v['name'].startswith(('Engraved','Copper_pad','PMMA')) and not v['name'].endswith('_PCB'):
  mod=ob.modifiers.new('Machined edge highlights','BEVEL');mod.width=.45 if materialname=='wood' else .08;mod.segments=3;mod.limit_method='ANGLE'
# Copper shown here is exported from the actual partial KiCad routing, never decorative traces.
for bd,tracks in json.loads((R/'hardware/split-r0.5/reports/tracks.json').read_text()).items():
 for i,t in enumerate(tracks):
  cu=bpy.data.curves.new('Copper','CURVE');cu.dimensions='3D';cu.bevel_depth=t['width']/2;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(1)
  for bp,xy in zip(sp.points,[t['start'],t['end']]):bp.co=(xy[0],-xy[1],0,1)
  ob=bpy.data.objects.new('Copper_'+bd+'_'+str(i),cu);bpy.context.collection.objects.link(ob);ob.location.z=1.61 if t['layer']=='top' else -.01;ob.scale.z=.12;ob.parent=parents[bd];ob.data.materials.append(mat((.07,.25,.14,1)));groups[ob.name]=bd
image=bpy.data.images.load(str(O/'panel-preview.png'));image.pack();ob=bpy.data.objects['Engraved_aluminium_panel'];mt=bpy.data.materials.new('Laser aluminium engraving');mt.use_nodes=True;p=mt.node_tree.nodes.get('Principled BSDF');p.inputs['Metallic'].default_value=.5;p.inputs['Roughness'].default_value=.33;tx=mt.node_tree.nodes.new('ShaderNodeTexImage');tx.image=image;mt.node_tree.links.new(tx.outputs['Color'],p.inputs['Base Color']);ob.data.materials.clear();ob.data.materials.append(mt);uv=ob.data.uv_layers.new(name='Panel artwork')
for poly in ob.data.polygons:
 for li in poly.loop_indices:
  v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=((v.x+13)/246,(v.y+161)/172)

def label(t,loc,size,group,flip=False,ang=0,parent=None):
 cu=bpy.data.curves.new(t,'FONT');cu.body=t;cu.align_x='CENTER';cu.size=size;cu.extrude=.003;ob=bpy.data.objects.new(t,cu);bpy.context.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(math.pi if flip else 0,0,math.radians(ang));ob.data.materials.append(mat((.84,.85,.78,1)));groups[ob.name]=group
 if parent:ob.parent=parents[parent]
 return ob
for l in s['labels']:label(l['text'],(l['x'],l['y'],l['z']),l['size'],l['board'],l.get('flip',False),l.get('angle',0),l['board'])
for t,x,z in [('POWER / UART',52,30),('USB MIDI HOST',64,35),('MAIN',172,30),('PHONES',201,30)]:
 ob=label(t,(x,DEP+.02,z),1.8,'case');ob.rotation_euler=(math.pi/2,0,math.pi)
# Ribbon with 12 individual insulated conductors, fanned into solder pads at each end.
for i in range(12):
 x=(i-5.5)*2.54;start=trans@Vector((135+x,-139,-.3));end=Vector((28+95+x,DEP-7-78,11.7));mid=(i-5.5)*1.27;pts=[start,trans@Vector((135+mid,-133,-1)),Vector((145+mid,55,23)),Vector((123+mid,DEP-7-84,12.6)),end]
 cu=bpy.data.curves.new('Ribbon conductor','CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=.62;cu.bevel_resolution=3;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for bp,pt in zip(sp.bezier_points,pts):bp.co=pt;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 ob=bpy.data.objects.new('Ribbon_'+str(i+1),cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat((.6,.025,.02,1) if i==0 else (.42,.44,.47,1)));groups[ob.name]='cable'
# Studio and physically based lights.
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.16,.18,.22,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45
for name,loc,power,size in [('Key',(-100,-180,400),2800000,250),('Fill',(400,-10,250),1900000,220),('Rim',(100,350,260),2300000,180)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((133,85,45))-ob.location).to_track_quat('-Z','Y').to_euler()
# A lower softbox lights the underside inspection render.
data=bpy.data.lights.new('Underside softbox','AREA');data.energy=1700000;data.size=180;ob=bpy.data.objects.new('Underside softbox',data);bpy.context.collection.objects.link(ob);ob.location=(80,20,-160);ob.rotation_euler=(Vector((133,85,45))-ob.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.mesh.primitive_plane_add(size=2000,location=(133,85,-4.1));floor=bpy.context.object;floor.name='Studio floor';floor.data.materials.append(mat((.11,.13,.16,1)))
bpy.ops.object.camera_add(location=(390,-330,280));cam=bpy.context.object;cam.data.type='ORTHO';sc=bpy.context.scene;sc.camera=cam;sc.render.engine='CYCLES';sc.cycles.samples=48;sc.cycles.use_denoising=True;sc.render.resolution_x=2000;sc.render.resolution_y=1400;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='AgX'

def render(name,loc,target,scale,visible=None):
 for ob in bpy.data.objects:
  if ob.name in groups:ob.hide_render=visible is not None and groups[ob.name] not in visible
 floor.hide_render=visible is not None;cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;sc.render.filepath=str(H/(name+'.png'));bpy.ops.render.render(write_still=True)
render('assembled-front',(390,-330,280),(133,82,45),350)
bpy.ops.wm.save_as_mainfile(filepath=str(O/'split-realistic.blend'))
render('assembled-rear',(370,400,240),(133,85,45),350)
render('control-pcb-top',(340,-170,360),(133,85,65),280,{'control'})
render('control-pcb-underside',(330,-190,-230),(133,85,65),280,{'control'})
render('electronics-pcb',(300,-100,240),(133,117,18),245,{'core'})
saved_groups={n:groups[n] for n in ['PMMA_front','Walnut_right']}
for n in saved_groups:groups[n]='cutaway-hidden'
render('interior-cable',(350,-280,45),(133,85,30),320,{'control','core','case','cable'})
groups.update(saved_groups)
parents['panel'].location.z+=155;parents['control'].location.z+=75
render('exploded',(450,-390,370),(133,85,130),560,{'panel','control','core','case'})
print('Seven detailed CAD renders completed')
