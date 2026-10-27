# Bronnenregister — 26 oktober 2026

- Specificatie gebruiker: `projectspecification-v1.0.md`, volledig bewaard.
- TI SN74HC165, SCLS116H (december 2015), pinout p.3, voeding/timing verderop: https://www.ti.com/lit/ds/symlink/sn74hc165.pdf . Kopie `sources/sn74hc165-SCLS116H.pdf`, SHA-256 `7ebf4358fa42dc1e0f50848e513a05fe0829a5d83eb4851c310532d2f0f3424e`. Gebruikt voor SCAN8-pinout; geen bewijs van aanwezige voorraad of CNC-passing.
- TI PCM5102A, SLAS859C (mei 2015): https://www.ti.com/lit/ds/symlink/pcm5102a.pdf . Alleen functioneel systeemplan; modulepinout niet bevestigd.
- Espressif USB host: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/usb_host.html . Hostsoftware en USB-voeding zijn afzonderlijke ontwerpstukken; nog niet gebouwd of getest.
- USB MIDI 1.0 (1 november 1999): https://www.usb.org/sites/default/files/midi10.pdf . Beoogde keyboardklasse uit de opdracht, geen compatibiliteitsbewijs van een specifiek keyboard.

De zes Amazon-links zijn opnieuw geprobeerd, maar waren niet toegankelijk via de zoektool. Cataloguszoekresultaten komen overeen met de aanwijzingen in §3 van de specificatie. Dit levert geen nieuwe bevestigde elektrische of mechanische gegevens op. B0GMQ92458 blijft zonder identificatie. De andere vijf blijven catalogusaanwijzingen; het exacte geleverde board en de moduleversie zijn open.

## ASIN-overzicht

| ASIN | Voorlopige rol | Bewijskracht |
|---|---|---|
| B0CP3YCP57 | ESP32-S3-board | Catalogusaanwijzing; geen footprint vrijgegeven |
| B0GMQ92458 | Onbekend | OPEN; geen verbindingen toegewezen |
| B07VF14YNG | CD74HC4067-module | Catalogusaanwijzing; niet opgenomen in SCAN8 |
| B07ZCQZYW1 | TCA9548A-module | Catalogusaanwijzing; niet opgenomen in SCAN8 |
| B09TVDZ8P2 | Mini-SPDT-schakelaars | Catalogusaanwijzing; fysieke passing/contactvolgorde OPEN |
| B0CJY1C287 | MAX98357-module | Catalogusaanwijzing; optioneel, variant OPEN |

De kale EC11-encoders en bestelde PCM5102A komen uit de aangeleverde specificatie; deze zes links bewijzen hun afmetingen of ASIN-koppeling niet.

## Aanvulling R0.2 — 27 oktober 2026

- TI CD74HC4067, SCHS209D, december 2024: https://www.ti.com/lit/ds/symlink/cd74hc4067.pdf . Gebruikt voor 16:1-selectie, enablegedrag en onderscheid HC/HCT. Modulegeometrie blijft OPEN.
- TI TCA9548A: https://www.ti.com/lit/ds/symlink/tca9548a.pdf . Gebruikt voor upstream/downstream-busfuncties, reset en adresstraps. Geen encoder-GPIO aangenomen.
- Analog Devices MAX98357A/B: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf . Gedeelde I²S-bus blijft conditioneel op A-variant; SD/mode-netwerk vereist modulecontrole.
- Espressif DevKitC-1 v1.0: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html . Alleen referentie voor bereikbare SoC-signalen; geen clone-pinout of footprintbewijs.
- Espressif DevKitC-1 v1.1: https://documentation.espressif.com/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html . Onboard-LED verschilt: GPIO48 in de initiële versie, GPIO38 in v1.1. Beide worden in R0.2 vermeden, evenals GPIO35–37 voor mogelijke octal-memorybezetting.

De twee TI-chipdatasheets zijn onder `docs/sources/` opgeslagen; SHA-256 staat in `hardware/full-r0.2/reports/source-checksums.txt`. De MAX98357-bron is online geraadpleegd; de lokale download mislukte. Dit zijn chipbronnen, geen maatbewijs van gekochte modules. Het DSP-bronnenonderzoek van vóór de PCB-prioriteitswijziging is niet als implementatie gebruikt.
