from pathlib import Path
import zipfile
R=Path(__file__).resolve().parents[1];out=R/'Compact-D-R05-TWO-BOARDS-DESIGN-NOT-PRODUCTION.zip';files=[]
for folder in ['hardware/split-r0.5','mechanical/split-r0.5']:
 for p in (R/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.FCBak','.blend1','.log','.kicad_prl'] and p.name not in ['.DS_Store','website-source.html','route-input.json','route-paths.json'] and not p.name.endswith('.lck'):files.append(p)
files+=list((R/'scripts').glob('*r05.py'))
for f in ['scripts/export_route_r04.py','scripts/route_known_r04.py','scripts/apply_routes_r04.py','README.md','docs/decisions.md','docs/projectspecification-v1.0.md','hardware/inventory-2026-10-27.json']:files.append(R/f)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.relative_to(R))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(out.name, len(files),'files',round(out.stat().st_size/1048576,1),'MiB; archive integrity verified')
