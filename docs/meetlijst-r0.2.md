# Meetmethode voor de volledige PCB — bijgewerkt 27 oktober 2026

**Eén PCB is vereist.** De oude sectiematen en 7-mux/28-encoder-aantallen vervallen. Eerst nodig: maximale breedte × hoogte van de ene print (ook bruikbaar CNC-gebied inclusief klemmen), paneeldikte, afstand paneel–PCB en knopcentra. Potmeters en MCP23017 zijn inmiddels geïdentificeerd; onderstaande meetmethode blijft van toepassing.

**Je hoeft niet alle identieke onderdelen te meten: één van elk type/revisie volstaat, plus een telling van de rest.** Bij zichtbaar verschillende revisies elk type apart meten. Lever de waarden in mm, met de oriëntatie die hieronder is aangegeven. Foto's van voor- en achterkant zijn nodig om pinlabels en richting te koppelen; een foto met liniaal alleen is niet nauwkeurig genoeg voor de gaatjes.

## Meetafspraak voor modules

Kijk op de componentzijde (de zijde met de chips), tekst leesbaar, en kies de linkeronderhoek van de module als O=(0,0). X naar rechts, Y naar boven. Noteer welke kant de USB/audio-aansluiting op wijst. Een foto van de achterkant is gespiegeld ten opzichte van dit coördinatenstelsel: geef de kijkrichting erbij.

KiCad/mastercoördinaten gebruiken Y omlaag. Bij omzetting naar de footprint moet Y dus van teken wisselen en moet de gekozen moduleoriëntatie worden toegepast; foto’s worden niet blind overgenomen.

Meet per module:

- **L, W, t:** lengte, breedte en printdikte. Neem kunststof connectorbehuizingen en overhang apart mee.
- **Pinraster p:** hart-op-hart tussen aansluitpinnen. Meet bij voorkeur van het hart van de eerste tot de laatste pin; geef de afstand en het aantal tussenruimten. Meet meerdere rijen afzonderlijk.
- **Rijafstand d:** hartlijn tot hartlijn tussen parallelle rijen, plus eventuele verschuiving langs de rij.
- **x₁, y₁:** hart van de eerste pin van iedere rij ten opzichte van O. Vermeld het op de module gedrukte label van die eerste pin en de richting waarin de rij doorloopt.
- **Pinaantal en volgorde:** alle labels in volgorde per rij. Geen standaard DevKit- of modulepinout aannemen.
- **Pindoorsnede:** rond: diameter; vierkant: zijde én liefst grootste diagonaal. Noteer pinlengte onder de module en of er al headers zijn gesoldeerd. Dit bepaalt het boorgat met gekozen soldeerspeling.
- **Montagegaten:** aantal, diameter en hart-X/Y van ieder gat. Ook sleuven, uitsparingen en metalen delen noteren.
- **Hoogtes:** hoogste component boven de print, laagste onderdeel/pinnen onder de print, en gewenste afstand tot de carrier. Bij gebruik van sockets: exacte socket-MPN, hoogte en footprint.
- **Connectorzone:** positie en afmetingen van USB/jack/schroefklem, uitsteken buiten de print en ruimte die stekker + kabelbocht vragen.

Doelnauwkeurigheid van de meting: pincentra/gaten ±0,1 mm of beter, pindoorsnede ±0,05 mm waar meetbaar, body/hoogte ±0,2 mm. Dit zijn meetdoelen, geen al gekozen boortoleranties. Noteer de werkelijke onzekerheid. Boorgaten krijgen pas een definitieve diameter na pen-/draadmaat en de Carvera-boorproef.

## Per Amazon-onderdeel

| Onderdeel | Precies nog nodig, boven op de modulemetingen |
|---|---|
| **1 — B0CP3YCP57 / ESP32-S3** | Foto's beide zijden; modulemarkering (bijv. N16R8), PCB-revisie, complete headerlabels; headerpinaantallen, rijafstand en offset; beide USB-connectoren en BOOT/RESET-posities; antennezijde en antennerand-X/Y; regulator-/USB-UART-markering; aanwezige soldeerjumpers. Bij verifieerbaar officieel bord is een exacte fabrikanttekening voldoende voor de nominale maten, met fysieke controle. |
| **2 — B0GMQ92458** | RK097N B10K-potmeter geïdentificeerd. Meet de X/Y-posities van drie aansluitpinnen en alle ankerlippen t.o.v. de as, hun doorsnede, bodymaat, hoogte vanaf PCB tot as/schroefdraad en asdiameter. Listing noemt 10,5 × 13,5 × 28 mm en as Ø6 × 15 mm, maar geeft geen gevalideerde boorcoördinaten. Meet ook de variant met gele knop afzonderlijk. |
| **3 — B07VF14YNG / CD74HC4067-module** | Chipmarkering met **HC of HCT**; positie/volgorde C0…C15, SIG/COM, S0…S3, EN, VCC en GND; alle rijen en offsets; eventuele EN-jumper, weerstanden of buffers; aantallen per revisie. **Ontwerpaantal: 7 modules**, voorraad onbekend. |
| **4 — B07ZCQZYW1 / TCA9548A-module** | Beide headerpatronen; upstream SDA/SCL en SD0/SC0…SD7/SC7-volgorde; locatie A0/A1/A2-jumpers; is RESET naar een pad/header uitgevoerd; aanwezige pull-upwaarden per tak. Ontwerpaantal: 1. |
| **5 — B09TVDZ8P2 / schuifschakelaar** | Huis L/W/H; de X/Y-harten van alle signaalpinnen en ankers; pinbreedte/-dikte en uitsteeklengte; actuator breedte/dikte/hoogte boven PCB en totale slag; hartpositie in beide eindstanden; bevestigingsgaten of lippen; benodigde sleufvorm. Continuïteit meten: welke pin is common en welke worp hoort bij welke stand. **18 stuks voor digitale functies**; powerbediening apart en nog te kiezen. |
| **6 — B0CJY1C287 / MAX98357-module** | Markering **A of B**; pinvolgorde VIN/GND/BCLK/LRC/DIN/SD/GAIN; speakerklempositie, steek, schroef-/draadtoegang; mode-/gainweerstanden of jumpers; maximale componenthoogte. Ook speakerimpedantie, vermogen en aansluitwijze nodig. Ontwerpaantal: 1. |

## Kale EC11-encoders — 28 posities

Voor de encoder geldt een andere oorsprong: **hart van de as**, gezien vanaf de aszijde naar het encoderhuis. Markeer een vaste bovenkant, X naar rechts en Y naar boven. Een onderaanzicht moet naar deze oriëntatie worden vertaald.

1. Huisbreedte, huisdiepte en hoogte van PCB-bovenvlak tot hoogste huispunt.
2. X/Y van A-, common- en B-pinnen ten opzichte van het ashart; pinbreedte/-dikte en lengte onder de print.
3. X/Y en doorsnede van de twee drukschakelaarpinnen. Bevestig dat deze elektrisch losstaan van A/B/common.
4. X/Y van **ieder montageanker**; ankerbreedte en -dikte. Geef aan of ronde gaten of sleuven nodig zijn. Meet metalen lippen apart van signaalpinnen.
5. Bus buitendiameter, schroefdraadtype/-spoed, totale buslengte en daadwerkelijk bruikbare schroefdraadlengte vanaf het huis.
6. Asdiameter, D-vlak/vertanding/rond, lengte vanaf bus en vanaf PCB, plus drukweg.
7. Bijbehorende moer en ring: dikte, buitendiameter/sleutelwijdte.
8. Knop: buitendiameter, hoogte, boring, insteekdiepte, klem-/stelschroefpositie. Dit bepaalt hartafstand en vingerruimte.
9. Elektrisch: A/common/B-identificatie, draairichting, detents per omwenteling, volledige quadratuurcycli per omwenteling en A/B-rusttoestand bij een detent.

Een volledige EC11-fabrikanttekening met exact MPN kan de nominale geometrie leveren; 'EC11' of de Amazon-ASIN alleen bepaalt die geometrie niet.

## Bestelde PCM5102A-module

De zes nieuwe links koppelen dit onderdeel nog niet betrouwbaar aan een ASIN. Geef de producttitel en beide modulefoto's. Meet het volledige modulepakket volgens de afspraak hierboven, inclusief jack/headeroverhang. Noteer labels VIN/3V3/GND/BCK/LRCK/DIN/SCK/XSMT/FMT/DEMP/FLT voor zover aanwezig, alle soldeerbrugstanden, regulator-markering en de L/R/GND-uitgangen. Bevestig of XSMT apart bereikbaar is. Voeg de voedingstekening toe als de leverancier die levert; VIN van een module is niet hetzelfde als de kale chipvoeding.

## Paneel, kast, aansluitingen en machine

| Gegeven | Nodig voor |
|---|---|
| Gewenste maximale paneelbreedte/-hoogte en hellingshoek; beschikbare binnendiepte | Definitieve PCB-grootte en plaatsing; huidige vakken zijn ruimtevoorstellen |
| Paneeldikte, eventuele achterzijdige uitsparingen, ring/moerstack | Bruikbare encoderbus, schakelaarhoogte en standoffhoogte |
| Knopdiameter + gewenste minimale ruimte tussen knoppen | Definitieve bedieningscentra |
| Binnenmaten houten kast, wanddikte en toegang servicepaneel | Printsteunen, kabelroutes en montage |
| Exacte USB-hostconnector/adapter, DC-aansluiting, audiojacks, speakerterminal, kabelconnectoren | MPN/datasheet, footprint, uitsparing, mating part, richting en kabelruimte |
| Carvera-model, werkelijk bruikbaar X/Y-bereik met fixture, plaatdikte, beschikbare boor/freesdiameters en registratiemethode | Printsegmentatie, via's, gaten en vrijgave dubbelzijdige CAM |
| Stockprintdikte + koperzijde/dikte; type draad-via/rivet en diens diameter | Padannulus, boorgat en assemblage |

## Gegevens die geen maten zijn, maar ook nodig blijven

- USB-MIDI-keyboard: merk/model en connector, voeding via USB of eigen adapter, opgegeven stroom; later werkelijk verbruik en hosttest. Alleen 'USB-keyboard' bevestigt nog geen class-compliant MIDI of stroomverbruik.
- Exacte voorraad van modules, encoders en schakelaars. Zeven 4067-modules zijn een ontwerpaantal, geen claim over je verpakking.
- Product 2 identificeren; onbekende modules krijgen geen gok-pinout.
- ADC/ingangsconditionering, hoofdtelefoonversterker en beschermde hostvoeding selecteren. Deze functies ontbreken nog als uitgewerkte schakeling; geometrie alleen lost dat niet op.
- USB-/boardvoedingsschema en jumperstanden: nodig om VBUS en programmeren zonder terugvoeding aan te sluiten.

**Minimale eerste aanlevering:** producttitel van link 2; boven-/onderfoto van ESP32, 4067, TCA9548A, MAX98357 en PCM5102A; één encoder en één schakelaar met de bovenstaande pin- en ankermaten. De rest kan in het meegeleverde `hardware/measurements/r0.2/measurements.csv` worden aangevuld.

## Aanvulling: MCP23017-module

Create idea MCP23017-E/SS, B0F8Q1TGYZ: meet module en headergeometrie volgens bovenstaande methode. Noteer labels, adresjumpers A0–A2, RESET, INTA/INTB, aanwezige pull-ups en voedingsmarkeringen. Aantal daadwerkelijk beschikbare modules nog vaststellen.
