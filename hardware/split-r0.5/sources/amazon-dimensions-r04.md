# Broncontrole — 27 oktober 2026

De Amazon-galerijen zijn per onderdeel bekeken. Een IC-datasheet bevestigt geen gatenpatroon van een clone-module. Fotopixels zijn niet naar boorcoördinaten omgerekend.

| Onderdeel / bron | Wat wel is vastgesteld | Wat niet uit de bron volgt |
|---|---|---|
| [RK097N B10K B0GMQ92458](https://www.amazon.de/dp/B0GMQ92458), maatfoto 2 | 10,5 × 13,5 × 28 mm opgegeven contour; as Ø6 × 15 mm | Pen- en lipcoördinaten ten opzichte van de as; ashoogte vanaf PCB; exacte tweede potmetervariant |
| [EC11 B09SG3HF9N](https://www.amazon.de/dp/B09SG3HF9N), tekeningen 2–3 | Huis 15 × 12,5; as Ø6; M7×0,75; signaalrijen op x −7,5 en +7 mm, pitch 2,5 mm; boor Ø1 mm; lipcentra y ±5,55 mm | Tekening noemt twee lipvarianten A=2,0/2,5 mm zonder koppeling aan geleverde variant. Voorlopige ruimere sleuf 2,7 × 1,8 mm toegepast; proefpassing vereist |
| [Schakelaar B09TVDZ8P2](https://www.amazon.de/dp/B09TVDZ8P2), maatfoto 2 | Huis 12,7 × 6,7 × 6,5; actuator 5 mm boven huis, breedte 3,8 mm | Hartafstand drie aansluitpennen en volledige actuatordikte/slag ontbreken; tekst en foto spreken elkaar tegen over totale hoogte |
| [ESP32-S3 B0CP3YCP57](https://www.amazon.de/dp/B0CP3YCP57), foto's 2/5/6 | Twee rijen van 22 pennen; GPIO-labels; dual USB-C, CH343P | Geen clone-maattekening of schema van 5 V-verdeling; officiële Espressif-boardmaat mag niet automatisch worden overgenomen |
| [MCP23017 B0F8Q1TGYZ](https://www.amazon.de/dp/B0F8Q1TGYZ), tekst + foto 6 | 65 × 19 mm; 2,54 mm raster; 20-polige I/O-rij en dubbele 7-polige controlerij; pinlabels leesbaar | Relatieve x/y-offset van de twee headergroepen en exacte printrandafstanden |
| [CD74HC4067 B07VF14YNG](https://www.amazon.de/dp/B07VF14YNG), foto 2 | HW-178; 16-kanaalsrij, 8-polige stuurrij; SIG,S3,S2,S1,S0,EN,VCC,GND | Rijafstand en verschuiving tussen de rijen niet bemaat; 40 × 17 mm is een nominale HW-178-envelop |
| [PCM1808 B09BTLPBM4](https://www.amazon.de/dp/B09BTLPBM4) | Pinlabels op drie headers; 5 V en 3,3 V; zichtbare condensatoren | Onderlinge headerposities, boorgaten, connectorhoogte; volledig moduleschema en condensatorwaarden |
| [PCM5102 B0GZ4XN5VT](https://www.amazon.de/dp/B0GZ4XN5VT), foto's 5–6 | 6-polige I²S-header en 9-polige zijheader; strapfuncties H1–H4 | Relatieve headerposities; H3-stand van geleverd exemplaar. Bij GPIO-besturing van XSMT mag deze niet hard aan voeding vastzitten |
| [TPA6132 B0FQ5T6MKC](https://www.amazon.de/dp/B0FQ5T6MKC), foto's 1/5 | L−/R− als enkelzijdige signaalingang, L+/R+ als retour; CTRL en DET; modulevoeding 2,3–5,5 V | Padcoördinaten, jackhoogte, volledige gain/koppelconfiguratie. Ontwerp nu op 3,3 V om CTRL-pullup binnen ESP-logicaniveau te houden |
| [USB-A B0C5JM2BW4](https://www.amazon.de/dp/B0C5JM2BW4), tekst + foto 2 | Module 17 × 17; connector 14 × 13 × 6; één rij 4 aansluitingen op 2,54 mm; VBUS,D−,D+,GND | Ligging header tegenover USB-mond voor de kastuitsparing; geen aparte shieldpen. De 4-polige header heeft nu echte PCB-pads |
| [PJ-307 B0CR3Y1YX2](https://www.amazon.de/dp/B0CR3Y1YX2), tekening 2 | Huis 14 × 12 × 5 mm; mechanische tekening met vijf contacten en positioneerpennen | Niet eenduidig welke nummers tip/ring/sleeve zijn bij dit verkochte exemplaar; verschillende PJ-307-fabrikanten gebruiken afwijkende nummering |
| [MAX98357 B0CJY1C287](https://www.amazon.de/dp/B0CJY1C287) | Headerlabels en schema in galerij; blijft optioneel | Exacte mechanische headeroffset nog niet bevestigd |

## Primaire elektrische bronnen

- [Espressif DevKitC-1](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html): alleen referentieontwerp, geen maatbewijs voor ARCELI-clone.
- [TI PCM1808](https://www.ti.com/lit/ds/symlink/pcm1808.pdf): ADC-voeding, klok- en formaatvereisten.
- [TI TPA6132A2](https://www.ti.com/lit/ds/symlink/tpa6132a2.pdf): versterkerinterface en voedingsbereik.
- [TI TPS2553](https://www.ti.com/lit/ds/symlink/tps2553.pdf): stroombegrenzing en pinmapping.
- [ST USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf): 1/6 en 3/4 zijn de doorlopende datakanalen; 2=GND, 5=VBUS.
- [Microchip MCP23017](https://support.microchip.com/s/article/GPA7---GPB7-Cannot-Be-Used-as-Inputs-In-MCP23017): GPA7/GPB7 niet gebruiken als contactingangen.

De ontbrekende voedingsjack, hoofdschakelaar en zekering moeten nog door de ontwerper worden geselecteerd; dat is geen meetopdracht aan de gebruiker. Geen productieclaim op grond van deze broncontrole.
