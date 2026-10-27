# Sloped enclosure — wood, aluminium and PMMA

## Material and dimensions

| Part | Nominal dimensions | Process / finish |
|---|---|---|
| Control panel | 246 × 172 × 1 mm | Black laser-markable aluminium, light engraving |
| Two sides | 18 mm thick, 172.14 mm deep; 47.20 mm front / 93.32 mm rear height | CNC solid wood; walnut finish shown |
| Front | 233.60 × 43.70 × 3 mm | Laser-cut dark PMMA |
| Rear | 233.60 × 89.82 × 3 mm | Laser-cut dark PMMA; provisional connector openings |
| Bottom | 233.60 × 165.74 × 3 mm | Laser-cut dark PMMA, ventilation and board mounting |
| Control PCB | 220 × 150 × 1.6 mm | 15° slope, modules below |
| Electronics PCB | 210 × 90 × 1.6 mm | Horizontal, separate from controls |

Outside width 266 mm, depth 172.14 mm and nominal overall height 104.53 mm including knobs and feet. The bigger aluminium border is deliberate: it keeps the screws clear of the artwork while retaining the board-size limit.

## Files and intended use

- `split-assembly.FCStd`, `split-enclosure-and-boards.step`: assembly with detailed reconstructed components, boards and enclosure. Vendor-part geometry is not certified.
- `wood-left-CNC.step`, `wood-right-CNC.step`: separate wood sides with PMMA rebates, rail pockets and panel screw pilots. Use STEP for CAM; `wood-side-outline-REFERENCE.svg` is only a silhouette reference.
- `PMMA-*-CUT-PROVISIONAL.svg`: separate 1:1 cutting outlines, no engraving mixed in. Rear openings need actual connector fit confirmation. Apply measured material thickness and machine kerf, not an assumed universal kerf.
- `panel-engraving-paths.svg`: finished artwork with all typography as vector paths and the official monochrome maakleerplek wordmark. Import as marking/engraving, not through-cutting.
- `panel-cut-PROVISIONAL.svg`: aluminium outline, control holes, switch slots and six screw holes. Shaft/bushing heights and switch stroke still require a fit check.
- `panel-preview.svg` / `.png`: artwork preview. The six holes are visible in the cut file and assembled renders, not printed as graphics in the engraving.
- `ribbon-strain-relief.step`, `ribbon-strain-relief-print.stl`: two identical clamp bridges. STL is oriented flat side down, cable gap upwards.
- `knob-classic-16mm.*`, `knob-silver-cap.*`: 27 knob bodies and caps required. Print one for fit first.
- `switch-caps/`: 17 caps after removing the external-input switch; three fit variants and a trial set, plus colour sets (2 orange, 5 blue, 6 white, 4 black).
- `split-realistic.blend`: assembled render scene; panel artwork packed into the file. The rendered views are in `../../hardware/split-r0.5/previews/`.

## Mounting detail

The aluminium bears on the sloped wooden side edges, overlapping each side by 8 mm. Six approximately 3-mm wood screws use the proposed 2.4-mm pilots; final pilot/length depends on the actual wood and chosen screw. These are not claimed to be M3 threaded inserts. The 3.2-mm clearance holes are all in a clean outer border. Every centre has a checked 4.5-mm engraving-free radius.

The control PCB mounts on two 238 × 8 × 6-mm aluminium rails (`control-support-rail-238x8x6.step`) at PCB y=5 and y=145 mm, with six M3 PCB support positions. Use two matching rails; their holes are 14, 119 and 224 mm from one end, centred across the 8-mm width. Rail ends enter pockets in the inner faces of the sides. The rails sit below the board, independent of the top-panel screws. Rail corner relief and corresponding wood-pocket cutter radius must be reconciled in CAM before machining; sharp internal CAD corners are not a toolpath.

The electronics board stands 3.8 mm above the upper surface of the 3-mm bottom panel. Its four mounting holes are 200 × 80 mm apart. Use washers/spacers rather than loading the PMMA directly with a small screw head. Four adhesive rubber feet provide clearance underneath the bottom vents. The PMMA sheets are captured in the side rebates; remove a side for bottom-panel service. The top can be unscrewed separately, within ribbon-cable slack.

The cable bridges use M2 fasteners on 36-mm centres. Their 2-mm internal clearance is a proposal for the selected ribbon and must grip gently without crushing insulation. Solder pad numbers and clamp holes are present on both KiCad boards.

## Suggested fabrication sequence

1. Make a paper/card panel and rear-opening fit template. Confirm the real shafts, switches and USB/audio connectors before cutting final panels.
2. Print one rotary knob, the three switch-cap trial variants and one ribbon clamp. Select clearances using the actual parts.
3. CAM the two wood sides from the inner face: rebates/pockets, then outside profile. Allow tool-radius relief at internal corners. Drill the angled panel screw pilots in a separate setup or drill guide normal to the slope.
4. Cut the PMMA using its measured thickness/kerf, then check a dry assembly in the rebates. Remove masking only when fabrication and dry fit are complete.
5. Cut and engrave the aluminium after the control mounting heights are settled. Assemble the boards on their rails/spacers, then solder and clamp the ribbon.

The CAD models and visible geometry are substantially more detailed than R0.4, but unpublished module dimensions remain provisional. No copper milling or production release accompanies these enclosure files.
