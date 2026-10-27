# Architecture and assembly detail

## 1. Boards

**Control board, 220 × 150 mm:** 19 B10K pots, eight EC11 encoders with push contacts, 17 SPDT switches, power LED, three MCP23017 modules and two CD74HC4067 modules. Controls are above the PCB; modules and supporting components are underneath. Existing MCP-module address straps set 0x20, 0x21, 0x22.

**Core board, 210 × 90 mm:** ESP32-S3 N16R8, PCM5102 DAC, TPA6132 headphone module, separate main-output jack and a few through-hole support components. Factory module electronics remain assembled. No ADC, audio input or MAX98357 speaker path.

## 2. Soldered ribbon connection

A short 12-conductor 1.27-mm-pitch ribbon fans out to numbered 2.54-mm solder pads at each end. Initial length allowance: 120–150 mm including service slack; trim only after checking the actual enclosure. Do not reverse the red-edge pin-1 end when viewing the underside.

| Wire | Signal | Role |
|---:|---|---|
| 1 | 3V3 | Control-board supply; never 5 V |
| 2 | GND | Power return |
| 3 | I2C_SDA | MCP23017 data, ESP GPIO1 |
| 4 | GND | Adjacent return |
| 5 | I2C_SCL | MCP23017 clock, ESP GPIO2 |
| 6 | GND | Adjacent return |
| 7 | POT_ADC1 | Multiplexer 1 output to core RC / ESP GPIO4 |
| 8 | GND | Analog return |
| 9 | POT_ADC2 | Multiplexer 2 output to core RC / ESP GPIO5 |
| 10 | GND | Analog return |
| 11 | PANEL_IRQ | Shared open-drain MCP interrupt, ESP GPIO10 |
| 12 | GND | Adjacent return |

Both ends are electrically identical, pin 1 to pin 1. All ground conductors terminate to board ground. USB data and audio never run through this ribbon. Each end has a printed 40 × 4 × 4-mm bridge clamp with 36-mm M2 screw spacing; its 2-mm gap accommodates the cable proposal. Final cable thickness and insulation compression require a fit check. Solder first, inspect continuity/shorts, then secure the clamp with the cable relaxed. Leave enough slack to lift the panel without stressing joints.

## 3. Internal pull-ups and scanning

The 41 switch/encoder contacts connect between MCP inputs and ground. Enable the internal approximately 100-kΩ GPPU resistors; the former 42 external 10-kΩ contact resistors are removed. Debounce push switches in firmware; use a quadrature state decoder for encoder A/B, not a long button debounce interval.

Use GPA0..6 and GPB0..6 for contacts. GPA7/GPB7 are output-only according to Microchip's clarification, so they are now useful rather than wasted:

| Output | Net |
|---|---|
| IO1 GPA7 | MUX_S0 |
| IO1 GPB7 | MUX_S1 |
| IO2 GPA7 | MUX_S2 |
| IO2 GPB7 | MUX_S3 |
| IO3 GPA7/GPB7 | Unconnected; configure as outputs low |

Both multiplexers share selection lines; EN is grounded. Nineteen pots use 16 channels on MX1 and 3 on MX2; unused analog channels go to ground. See `controls.csv` for each channel assignment. Pot endpoints connect to 3V3 and GND; the wiper goes to its mux input.

Firmware proposal: BANK=0; IODIRA/B=0x7F on all three chips; enable input pull-ups and only the contact interrupt mask bits. Configure IOCON MIRROR and ODR (0x44) **before** enabling interrupts, then combine INTA outputs on PANEL_IRQ; INTB remains unused. Read both interrupt-capture ports when servicing the shared interrupt, then check current input states. No interrupt is enabled for the unused IO3 GPB6 contact. Interrupt scanning must remain responsive during audio and USB work; bench-test the fastest intended encoder motion.

Update mux-select bits through OLAT shadow registers without overwriting unrelated bits. After both selector writes have completed, allow an initial 100 µs settling interval before sampling; then calibrate settling and filtering on hardware. Two core RC networks (1 kΩ / 1 nF) filter the mux outputs near the ESP ADC. These values are starting points, not measured analog performance. Start I²C conservatively at 100 kHz; increase to 400 kHz only after bus timing and fast-encoder tests. Actual achievable scan rate must be measured with USB/audio active.

## 4. Which discrete parts remain

- RP1 1 kΩ: power-LED current limit.
- RP2 10 kΩ: common MCP reset pull-up.
- RP3/RP4 2.2 kΩ **DNP by default**: optional I²C bus pulls, only if the modules' existing parallel pull-ups are insufficient. Check that all module pulls go to 3V3.
- RP5 10 kΩ: shared open-drain IRQ pull-up.
- RA1/RA2 1 kΩ + CA1/CA2 1 nF: two mux output filters.
- RA3 100 Ω: series resistor for the main output.
- RA4 10 kΩ / RA5 4.7 kΩ: headphone input attenuation proposal; module loading changes the actual ratio.
- RA6/RA7 100 kΩ: DAC mute and headphone enable defaults.
- CP1/CC1 100 nF and CP2/CC2 10 µF: local rail decoupling/bulk reserve.

All these carrier parts use through-hole footprints. Onboard module coupling/decoupling is not duplicated wholesale. Resistor bands in illustrative models are generic; assembly values come from the schematic, not render colours.

## 5. Audio output

I²S uses ESP GPIO15 BCLK, GPIO16 LRCLK and GPIO17 TX. PCM5102 uses its PLL with SCK grounded and I²S format. Main audio is the left DAC channel; headphone audio is the right, independently scaled in firmware from the same mono synth signal. This preserves independent front-panel volume controls without analog audio on the ribbon.

The DAC's built-in stereo jack therefore remains **inside the enclosure and unused**. A separate rear jack carries the left-channel main signal to tip and ring. The TPA6132 onboard jack is the rear headphone output. Its L−/R− inputs receive the attenuated right-channel signal; L+/R+ are returns. Module coupling and gain must be confirmed before release. TPA6132 is supplied from 3V3 so its CTRL pull-up cannot drive the ESP input above 3.3 V. Check available regulator current and dissipation with both headphone channels loaded.

DAC XSMT uses GPIO41 and HP enable GPIO40. Remove or alter any module strap that hard-connects XSMT to a rail before GPIO control. There is no new external-audio path, overload LED or external mixer control.

## 6. USB and power: remaining electrical gate

The design reserves the ESP module's native USB port for a class-compliant USB-MIDI keyboard and USB-UART for power/programming. The native port requires host-mode firmware; the UART bridge cannot host a keyboard. Two physical ports do not establish that the native port can supply VBUS.

Before connecting a bus-powered keyboard, verify the actual ARCELI clone's 5-V paths, diodes, native-port VBUS sourcing, USB-C role wiring and regulator/current capacity. The current schematic does not silently add a connection that could bypass protection or backfeed a computer. If the module cannot power the keyboard correctly, use a correctly powered USB hub or add a protected host-power solution; this decision remains open and may change the rear opening/PCB. No assumption that a generic USB-C adapter alone solves host power.

The control pots alone draw about 6.3 mA at 3.3 V; reserve up to 50 mA for the complete control board until module LED/logic currents are measured. This is an allowance, not a measured consumption figure. The ESP, DAC, headphone amplifier and keyboard require a separate complete power budget.

## Sources

- MCP23017 pull-ups and registers: https://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf
- Output-only GPA7/GPB7: https://support.microchip.com/s/article/GPA7---GPB7-Cannot-Be-Used-as-Inputs-In-MCP23017
- ESP USB host: https://docs.espressif.com/projects/arduino-esp32/en/latest/api/usb_host.html
- ESP native USB wiring: https://docs.espressif.com/projects/esp-usb/en/latest/esp32s3/usb_device.html
- TPA6132A2: https://www.ti.com/lit/ds/symlink/tpa6132a2.pdf
