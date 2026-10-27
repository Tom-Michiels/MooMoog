# Remaining verification — only parts used by R0.5

## Missing reliable mechanical information

| Part | Missing information |
|---|---|
| Both RK097N pot variants | Exact three-terminal and mounting-tab coordinates relative to shaft; terminal sections; shaft/bushing heights from PCB. The published Ø6 × 15-mm shaft dimension alone is insufficient. |
| RUNCCI 3-pin switches | Pin-centre pitch/sections, actuator thickness and full travel. Printed cap variants are trial fits. |
| ARCELI ESP32-S3 | Actual row spacing and header-to-edge coordinates for this clone; USB connector face/height. The official DevKit drawing is not proof for the clone. |
| MCP23017 modules | Relative x/y offset of the dual 7-pin header to the 20-pin header. The 65 × 19-mm body and 2.54-mm pitch are already known. |
| HW-178 CD74HC4067 | Distance and offset between the 8- and 16-pin header rows. |
| PCM5102 and TPA6132 modules | Relative header positions, connector/body heights and mounting-hole coordinates. |
| EC11 | Which of the two mounting-tab variants is supplied; electrical contact geometry has been found and used. |
| Main output jack | Final exact part and physical tip/ring/sleeve mapping; selecting this is design work, not a request to measure an unspecified part. |

There is no longer any need to measure a PCM1808, external-input jack, MAX98357, or separate USB-A module for this proposed architecture. USB host-power verification can still force a change to the connector solution.

## Electrical work still needed

- Verify ARCELI USB-C roles, 5-V paths and keyboard VBUS sourcing/current capability. A bus-powered keyboard is not yet proven to work directly from the native port.
- Establish the keyboard's USB-MIDI compatibility and current requirement.
- Confirm available 3.3-V regulator current and thermal margin for ESP, control board and headphone amplifier.
- Confirm existing module I²C pulls, reset circuitry, audio coupling/gain and DAC mute strap before adding/removing matching parts.
- Finalize physical footprints, copper/return paths, power widths, nonplated-via assembly if CNC-milled, and complete hardware/firmware tests.

The detailed 3D models do not resolve these missing measurements. The zero-violation DRC covers the pads currently present; it cannot detect absent module/pot/switch connections.
