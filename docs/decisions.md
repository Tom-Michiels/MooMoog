# Besluitenlog

| ID | Datum | Status / grond | Besluit |
|---|---|---|---|
| D001 | 2026-10-26 | BEVESTIGD gebruiker | PCB eerst; firmwarewerk uitgesteld. |
| D002 | 2026-10-26 | BEVESTIGD gebruiker / specificatie | Rechtstreeks USB-MIDI-keyboard, zonder computer; merk/model OPEN. |
| D003 | 2026-10-26 | VOORSTEL §8 | Parallel capture via SN74HC165N, 3,3 V; eerst acht-ingangscoupon. Deze IC is aanvullend aan de opgegeven aankopen. |
| D004 | 2026-10-26 | BRON TI SCLS116H | SN74HC165N PDIP-pinout verwerkt; gekochte modulematen blijven onbekend. |
| D005 | 2026-10-26 | VOORSTEL / CNC | 0,4 mm tracks/clearance, expliciete draad-via's; nog procesvalidatie nodig. |
| D006 | 2026-10-26 | VOORSTEL | Vijf secties met 15 registers/120 bits door afronding per sectie; 102 contacten. |
| D007 | 2026-10-26 | OPEN / §14 | Geen EC11-, switch-, ESP32- of audiomodulefootprint zonder maat- en pinoutcontrole. |
| D008 | 2026-10-26 | VOORSTEL | Coupon gebruikt soldeerdraadinterfaces voor contacttests; finale encoders komen op eigen sectie-PCB. |
| D009 | 2026-10-26 | OPEN | B0GMQ92458 onbekend en buiten het elektrische ontwerp gehouden. |
| D010 | 2026-10-26 | BRON + OPEN | CD74HC4067 is analoge mux, TCA9548A I²C-mux. Geen van beide vervangt vanzelf de parallelle contactscanner. |
| D011 | 2026-10-26 | OPEN | ADC, hoofdtelefoongain, VBUS-beveiliging, connectoren en voeding nog te selecteren en testen. |
| D012 | 2026-10-27 | BEVESTIGD gebruiker | Volledig instrument rond Amazon-onderdelen eerst, niet verderbouwen aan alleen SCAN8. R0.2 vervangt de actieve R0.1-opzet. |
| D013 | 2026-10-27 | VOORSTEL o.b.v. D012; kwalificatie OPEN | 7x CD74HC4067 met gekoppelde A/B-muxen en 3 extra muxen voor drukken/switches; 102 contacten. Vervangt D003/D006 in deze kandidaatarchitectuur, niet de betrouwbaarheidseis. |
| D014 | 2026-10-27 | VOORSTEL §7.2 | PCM5102A L=main mono, R=onafhankelijke phonesbus via aparte versterker. Kanaaldata verschillen bewust; main-mute alleen digitaal op L. |
| D015 | 2026-10-27 | VOORSTEL | MAX98357A volgt linker mainbus plus eigen SD; gedeelde aansluiting is conditioneel op bevestiging van A-variant/straps. |
| D016 | 2026-10-27 | OPEN | Alle fysieke module-/encoder-/switchpads blijven ongetekend tot maat/pinmapping. Plaatsingsvakken zijn voorstel-enveloppen, geen footprints. |
| D017 | 2026-10-27 | VOORSTEL | TCA9548A krijgt plek en I²C-branchplan; noodzaak hangt af van gekozen ADC/display. Onbestukt mogelijk. |
| D018 | 2026-10-27 | VOORSTEL | Vijf paneelsecties en één coreprint; grootte nog afstemmen op echte onderdelen/Carvera. Enkelvoudige grote print is niet vrijgegeven. |
| D019 | 2026-10-27 | BEVESTIGD gebruiker | Eén PCB met alle bediening en elektronica; vervangt D018 en afzonderlijke sectieprinten. Gekochte modules worden op de hoofdprint gemonteerd. |
| D020 | 2026-10-27 | BRON Amazon-orders via Safari | B0GMQ92458 is RK097N B10K-potmeter; daarnaast B10K-variant met gele knop, samen 20 besteld. EC11: 20 besteld. Vervangt D009. |
| D021 | 2026-10-27 | BRON Amazon-orders via Safari | MCP23017-E/SS module B0F8Q1TGYZ gevonden in drie bestellingen uit 2025. Beschikbaar aantal onbekend. D013/102-contactindeling vervalt als actuele behoefte; scanning herontwerpen met potmeters en digitale GPIO. |
| D022 | 2026-10-27 | VOORSTEL gebruiker + productpagina | DAC B0GZ4XN5VT is Eltichorix PCM5102 I2S lijnmodule, pak van drie, zichtbaar in winkelmand. Niet als gekocht geregistreerd; pinout en footprint open. |
| D023 | 2026-10-27 | BEVESTIGD gebruiker | Maximale hoofdprintmaat 220 × 150 mm. R0.3 gebruikt deze omtrek; buitenmaat kast is een apart voorstel. |
| D024 | 2026-10-27 | VOORSTEL R0.3 | 20 potmeters + 8 encoders + 18 schakelaars; 2 CD74HC4067 en 3 MCP23017, elk 14 veilige ingangen. TCA9548A niet nodig. Vervangt D013/D017 als actieve architectuur. |
| D025 | 2026-10-27 | BRON fabrikant + Amazon-kandidaten | PCM1808 ingang, TPA6132 hoofdtelefoon, TPS2553 VBUS, USBLC6-2 ESD en externe vaste 5 V/3 A. Modulepinmapping, koppeling, stroomvraag en footprints open. |
| D026 | 2026-10-27 | VOORSTEL CAD | Kast 244 × 166 × 54 mm exclusief knoppen; Ø16 mm geprinte knoppen, 6,2 mm blind gat. Geometrie niet gemeten aan geleverde onderdelen; eerst passing bevestigen. |
| D027 | 2026-10-27 | STATUS | R0.3 logisch schema en CAD gemaakt; 190 componenten / 127 netten. PCB heeft 0 tracks en onbekende modulepads. Geen volledige PCB, Gerbers of maakbaarheidsvrijgave. |

## D028 — 2026-10-27 — Laser-aluminium en klassieke indeling (R0.4)

Gebruiker vraagt een laser-aluminiumpaneel en Minimoog-knopindeling. R0.4 gebruikt een zwarte paneelvoorstelling met lichte gravure, vijf klassieke functiegroepen en de drie oscillator-/mixer-/enveloperijen. PCB blijft 220 × 150 mm; paneelvoorstel 230 × 160 × 1 mm. Eigen opschrift Compact D. Gravuretekst als vectorpaden; snijgaten apart en voorlopig. Klassieke Ø16-mm-ribbelknoppen met afzonderlijke zilverkleurige kap en aanwijzer; geprinte schuifverlengingen vanwege korte gekochte actuators. Inbouwhoogten en passing nog niet vrijgegeven.

## D029 — 2026-10-27 — Onderdeelonderzoek en gedeeltelijke routing

Productgalerijen leveren EC11-contactpatroon en 2,54-mm-USB-header; daarvoor echte pads toegevoegd. MCP23017-envelop gecorrigeerd naar 65 × 19 mm; schakelaars naar 12,7 × 6,7 mm en verspreid over functiegroepen. Niet-bemate onderlinge moduleheaderafstanden en potmeter-/schakelaarpenposities blijven open. Bronnen en alleen de resterende ontbrekende gegevens staan in hardware/compact-r0.4/source-evidence.md en meetlijst.md. Generieke IC- of officiële DevKit-tekeningen niet als clone-footprintbewijs gebruikt.

TPA6132-module in R0.4 op 3,3 V vanwege CTRL-pullup; foto-aansluiting L−/R− gebruikt met L+/R+ aan retour. Voedingsbudget nog te bevestigen. Bekende signaalpads gedeeltelijk gerouteerd; USB-datapaar en hoofdstroomverbindingen blijven gereserveerd voor definitieve gecontroleerde routing. Dit is geen volledige PCB of fabricagevrijgave. Geen Gerbers of CNC-toolpaths uitgegeven.

## D030 — 2026-10-27 — Printbare opsteekknopjes voor 3-pins schakelaars

Gebruiker vraagt expliciet passende 3D-geprinte knopjes op de schuifschakelaars. Drie proefpasvarianten gemaakt met opname 1,6 × 4,0 / 1,8 × 4,1 / 2,0 × 4,2 mm, elk 4 mm diep; buitenmaat 5 × 5 × 12 mm. Greep krijgt drie bovenste groeven en een verruimde insteekmond. STL's staan met de opname omhoog. Complete set van 18 en sets per paneelkleur geleverd. De ontbrekende exacte hendeldikte en slag verhinderen een bevestigde fysieke passing; eerst proefset gebruiken. Assembly en render gebruiken dezelfde nominale kapvorm.

## D031 — 2026-10-27 — Geen audio-ingang; interne pull-ups en USB-hergebruik

Gebruiker bevestigt dat externe audio-ingang niet nodig is. PCM1808, ingangsjack en bijbehorende conditionering vervallen uit de eisen; externe-ingangsmixerbediening en opschrift moeten in de volgende PCB/paneelrevisie vervallen. De bestaande R0.4-export en ZIP zijn nog niet opnieuw gegenereerd en tonen deze oude ingang nog.

MCP23017 ondersteunt via GPPU interne circa 100-kΩ-pull-ups. De 42 afzonderlijke 10-kΩ-contactpull-ups zijn niet standaard vereist: volgende revisie gebruikt interne pulls en softwaredebouncing; robuustheid bij encoderrotatie en storing verifiëren. Dit vervangt geen I²C-buspull-ups, LED-stroombegrenzing of noodzakelijke voedings/audiofuncties. Onboard onderdelen eerst inventariseren voordat externe onderdelen worden toegevoegd.

Voorkeur gebruiker: native ESP32-S3 USB voor USB-MIDI-keyboard, USB-UART-aansluiting voor voeding/programmeren. S3 kan USB-host zijn; USB-UART-bridge is geen USB-MIDI-host. De ARCELI-clone moet wel een passende 5-V-VBUS-voeding en hostaansluiting naar het keyboard kunnen leveren. Doorverbinding, stroomcapaciteit en USB-C-rol zijn niet bewezen door alleen twee aanwezige USB-poorten. Niet als plug-and-play voeding vrijgegeven.

Bronnen: https://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf ; https://docs.espressif.com/projects/arduino-esp32/en/latest/api/usb_host.html ; https://docs.espressif.com/projects/esp-usb/en/latest/esp32s3/usb_device.html .

## D032 — 2026-10-27 — Two boards, sloped panel, wood and PMMA

User approves a separate controls PCB and electronics PCB connected with soldered flat cable, then requests detailed development and realistic renders with CNC wooden sides and PMMA front/rear/bottom. R0.5 supersedes the single-board constraint: control PCB 220 × 150 mm at 15°, core PCB 210 × 90 mm horizontal. MCP expanders/multiplexers stay on the control board. Four output-only MCP pins select both muxes, reducing the interconnect to 12 wires with interleaved returns. Internal contact pull-ups replace 42 external resistors. Audio input and its control pair/LED are removed: 19 pots, 8 encoders, 17 switches. Added passives use through-hole packages. No optional speaker path in R0.5.

## D033 — 2026-10-27 — Screw clearance and maakleerplek logo

User reports screws touching the lettering and requests the maakleerplek logo. R0.5 panel is enlarged to 246 × 172 mm with six screws in a dedicated outer border. Every screw has a checked 4.5-mm-radius engraving-free zone. The official inline SVG wordmark from https://maakleerplek.be/nl is included in monochrome below Compact D. Shape/source preserved in mechanical/split-r0.5/assets.

Enclosure proposal is 266 × 172.14 mm, approximately 104.53 mm total height with feet/knobs. Sides are 18-mm wood, sloped aluminium 1 mm, PMMA panels 3 mm. Aluminium control-board support rails, bottom spacers and printed ribbon strain relief are included. Cut holes and clone-module fit are provisional; CNC STEP is geometry, not toolpaths.

## D034 — 2026-10-27 — R0.5 validation scope

Detailed reconstructed module models replace generic blocks; actual KiCad partial copper is shown in renders. Functional netlists and cable mapping checked. Known pad connections have 53 routed trajectories and zero DRC violations; 45 component instances still lack final footprints, so this is not a complete or production-ready PCB. ARCELI USB host VBUS/current/role verification, audio coupling/gain and final physical dimensions remain open. No fabrication files are released.
