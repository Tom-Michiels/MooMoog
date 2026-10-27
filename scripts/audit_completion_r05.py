"""Compare required functional terminals against actual copper pads, not just DRC.

Run with KiCad's Python. Missing pads must never disappear from completion counts.
This is a design completeness check, not electrical or physical certification.
"""
from pathlib import Path
import json
import sys
import pcbnew as pcb

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'hardware/split-r0.5'
master = json.loads((OUT / 'design-master.json').read_text())
report = {'manufacturing_ready': False, 'boards': {}, 'unresolved_system_checks': [
    'ARCELI native USB host VBUS source, current limiting and USB-C role',
    '3.3 V regulator current and thermal budget with all modules attached',
    'Purchased module input coupling, pull-ups and configuration straps',
    'Mechanical fit of purchased components and rear connectors',
]}
for name in master['boards']:
    board = pcb.LoadBoard(str(OUT / name / (name + '.kicad_pcb')))
    footprints = {f.GetReference(): f for f in board.GetFootprints()}
    missing, wrong, present, padless = [], [], [], []
    for component in master['components']:
        if component['board'] != name:
            continue
        ref = component['ref']
        footprint = footprints.get(ref)
        pads = {} if footprint is None else {
            p.GetNumber(): p.GetNetname() for p in footprint.Pads() if p.GetNumber()
        }
        if not pads:
            padless.append(ref)
        for pin in component['pins']:
            if pin['net'] is None:
                continue
            terminal = {'ref': ref, 'pin': pin['number'], 'net': pin['net']}
            if pin['number'] not in pads:
                missing.append(terminal)
            elif pads[pin['number']] != pin['net']:
                wrong.append(dict(terminal, actual_net=pads[pin['number']]))
            else:
                present.append(terminal)
    drc_path = OUT / 'reports' / (name + '-drc.json')
    drc = json.loads(drc_path.read_text()) if drc_path.exists() else {}
    report['boards'][name] = {
        'required_connected_terminals': len(missing) + len(wrong) + len(present),
        'terminals_with_matching_pads': len(present),
        'missing_terminals': missing,
        'wrong_net_terminals': wrong,
        'padless_components': padless,
        'drc_unconnected_existing_pads': len(drc.get('unconnected_items', [])),
        'drc_scope_warning': 'Zero DRC unconnected items cannot account for missing pads.',
    }
report['missing_terminal_count'] = sum(len(b['missing_terminals']) for b in report['boards'].values())
report['padless_component_count'] = sum(len(b['padless_components']) for b in report['boards'].values())
(OUT / 'reports/completion-audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'boards'}, indent=2))
sys.exit(1 if report['missing_terminal_count'] or report['unresolved_system_checks'] else 0)
