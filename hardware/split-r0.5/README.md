# Compact D R0.5 — two-board sloped design

This revision implements the agreed split: a sloped control PCB and a separate flat electronics PCB, connected by soldered ribbon cable. It removes external audio input, its controls, the ADC, the overload LED, the external contact pull-up bank and optional speaker amplifier. **This is a detailed design revision, not a manufacturing release.** Several purchased-module/pot/switch footprints remain unverified; those components have no fabricated pad patterns.

## Delivered files

- `control/control.kicad_pro`, `.kicad_sch`, `.kicad_pcb`: control-board project, 220 × 150 mm.
- `core/core.kicad_pro`, `.kicad_sch`, `.kicad_pcb`: electronics-board project, 210 × 90 mm.
- `design-master.json`, `controls.csv`, `switches.csv`, `scan.csv`, `ribbon.csv`: common design data and exact functional connections.
- `previews/`: assembled front/rear, exploded assembly, control PCB top/underside, electronics PCB, and native KiCad renders.
- `../../mechanical/split-r0.5/`: full FreeCAD/STEP assembly, detailed reconstructed component models, CNC side STEP files, provisional laser-cut SVGs, aluminium engraving, printed knobs/caps/clamps and Blender scene.
- `architecture.md`: wiring, scanning, pull-ups, audio and USB power decisions.
- `remaining-verification.md`: specific unresolved information, without repeating known dimensions.

## Mechanical design

15° aluminium top panel, 18-mm CNC-cut wood sides, 3-mm dark PMMA front/rear/bottom. The control PCB sits under the aluminium; the electronics PCB sits horizontally on bottom spacers. Internal rails support the control PCB independently of the visible panel screws. Printed bridges clamp the ribbon at both boards so cable movement does not pull directly on solder joints.

The new screw border increases the aluminium panel to **246 × 172 mm**. Both PCBs remain within the user's 220 × 150-mm maximum. Enclosure outside dimensions are approximately **266 × 172.1 × 104.5 mm including knobs and feet**. Front wood height is 47.2 mm; rear wood height 93.3 mm. These are design proposals, not measured stock-material dimensions.

The six panel screws sit outside the lettering. A raster check of the vector artwork confirms a **4.5-mm clear radius around every screw centre**. Actual head radius in the model is 2.7 mm, leaving 1.8 mm additional clearance to engraving. The official maakleerplek SVG wordmark is taken from https://maakleerplek.be/nl and incorporated unchanged in shape, with a monochrome colour for engraving. The original SVG is preserved with source information.

## What “realistic” means here

The new renders use explicit geometry for module PCBs, headers, individual IC leads, shields, antenna traces, USB mouths/tongues, audio jacks, resistors, capacitors, control housings, shafts, screws and cable. Copper in the Blender views is exported from the actual KiCad segment data, not invented decorative tracks. Native KiCad views use the same locally generated WRL models.

These are **detailed reconstructed models**, not exact vendor STEP files. Unpublished header offsets, shaft/bushing heights and connector details remain assumptions. A photorealistic render cannot prove those fit. See `remaining-verification.md` and the earlier per-product source audit at `sources/amazon-dimensions-r04.md`.

## Electrical and routing status

74 functional components, 19 pots, 8 encoders, 17 switches, 41 digital contacts, one power LED. All **added carrier-board resistors/capacitors are through-hole**; factory-built Amazon modules naturally still contain their own SMD components. There are 12 resistors, 4 ceramic capacitors and 2 electrolytics; two I²C pull-up resistors are DNP unless measurements show they are needed.

53 connection trajectories between currently available pads have been routed: 33 on the control board and 20 on the core board. DRC has no remaining violations or unconnected items **among those pads**. This does **not** mean the boards are electrically complete: 45 component instances still lack final pads, so DRC cannot see their missing connections. Firmware, full USB power verification, audio gain/coupling, return-path/ground-plane design, final routing, production footprints and hardware tests remain outstanding. There is no Gerber or CNC-copper release.

The functional schematic netlists match the design data; ribbon pin assignments match at both ends. Models pass CAD validity checks. Nominal inter-board envelopes retain at least 11.7 mm conservative vertical separation where their projections overlap. This is not a substitute for physical fit checks on the actual modules.

## Reproduction

Run `build_split_r05.py` with KiCad Python, then `route_split_r05.py export/route/apply` for each board (export/apply require KiCad Python; route uses normal Python). Apply once to freshly generated boards. Export pads/tracks with `export_split_pads_r05.py`, generate the panel with `build_panel_r05.py`, generate CAD with `build_split_cad_r05.py` using FreeCAD Python, then render with `render_split_r05.py` in Blender. Cutting diagrams and print-cap variants have separate R05 scripts. `check_split_r05.py` checks exported netlists, DRC reports and nominal inter-board geometry. Do not regenerate over manual edits without saving them first.
