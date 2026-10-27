# Validatie R0.1 — 26 oktober 2026

Tool: KiCad 9.0.6. Object: uitsluitend SCAN8, niet het volledige instrument.

| Controle | Resultaat | Bewijs |
|---|---|---|
| Schema parser/export | Geslaagd | previews/scan8-schema/scan8.svg |
| ERC | 0 fouten / 0 waarschuwingen | hardware/reports/scan8-erc.json |
| PCB DRC | 0 overtredingen | hardware/reports/scan8-drc.json |
| Onaangesloten verbindingen | 0 | idem |
| Schema-PCB overeenstemming | 0 verschillen | idem |
| Niet-doorgemetalliseerde assemblage | 14 netten verbonden met 36 expliciete draad-via's | hardware/reports/nonplated-connectivity.json |
| Visuele preview | Schema en print bekeken | hardware/previews/png/ |
| Fysieke passing | Niet uitgevoerd | componentmetingen ontbreken |
| Elektrische benchtest | Niet uitgevoerd | geen aangesloten hardware |
| USB-keyboard | Niet uitgevoerd | buiten SCAN8; core/USB-pad nog te ontwerpen |
| Carvera-proces | Niet uitgevoerd | machine/tooling/registratie niet bekend |

De zelfstandige connectivity-check modelleert componentpads uitsluitend op B.Cu en maakt alleen bij de geregistreerde draad-via's een laagverbinding. Daarmee wordt niet op een denkbeeldige geleidende gatwand vertrouwd. Het is een geometrische ontwerpcontrole, geen meting van gesoldeerde onderdelen.

De meegeleverde autorouter maakt een eerste route met ruime regels. De 36 via's en omwegen zijn expliciete beperkingen; optimalisatie en ontkoppel-/retourpadreview zijn nodig vóór een bruikbare paneelprint. Er zijn geen ERC/DRC-waivers toegepast. De runtime kan een wxApp- en fontconfigmelding geven; de opgeslagen KiCad-checkrapporten zijn de ontwerpresultaten.
