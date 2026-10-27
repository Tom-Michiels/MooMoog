# Digitale Minimoog Model D-replica — projectspecificatie

Versie 1.0 · 26 oktober 2026 · taal: Nederlands

## 1. Doel en status

Bouw een zelfstandig bespeelbare, monofone digitale synthesizer met de bediening en indeling van de door de gebruiker aangeleverde Minimoog Model D-foto. Gebruik een ESP32-S3 voor digitale klankopwekking, kale EC11-encoders op eigen printplaten, de reeds bestelde PCM5102A voor lijnuitgang, een CNC-gefreesd bedieningspaneel en een houten behuizing. Printplaten worden tweezijdig op een Makera Carvera gefreesd.

**Verplicht: een USB-MIDI-keyboard rechtstreeks aansluiten, zonder computer ertussen.** De gebruiker heeft in deze sessie bevestigd dat het om USB-MIDI gaat. De synthesizer moet dus USB-host zijn. USB-MIDI naar een computer is een afzonderlijke, optionele gebruiksmodus.

Dit document is de opdracht voor verdere software-, elektronica- en mechanische ontwikkeling. Firmware en logische schema's kunnen direct worden uitgewerkt. Definitieve footprints, mechanische passing, PCB-routing en freesbestanden vereisen eerst de verificaties in §14. Dit document is geen vrijgegeven fabricagepakket en claimt geen exacte analoge klankidentiteit.

### Statuslabels

- **BEVESTIGD:** rechtstreeks door gebruiker of beschikbaar referentiemateriaal bevestigd.
- **BRON:** eigenschap van een chip of referentie-instrument onderbouwd met fabrikantdocumentatie; zegt niets over de uitvoering van een gekochte module.
- **VOORSTEL:** concrete standaard voor implementatie, aanpasbaar na metingen of gebruikerskeuze.
- **OPEN:** ontbrekende gegevens; niet invullen met een plausibele maar onbewezen waarde.

De voorgeschiedenis is gedeeltelijk toegankelijk: meerdere eerdere assistentantwoorden bevatten alleen verwijzingen zonder inhoud. De oorspronkelijke paneelfoto is wel teruggevonden en bekeken. Eerdere niet-zichtbare aanbevelingen gelden daarom niet als vaststaande ontwerpkeuzes.

## 2. Afbakening en opleveringen

### Verplichte eindfunctionaliteit

1. Drie onafhankelijke digitale oscillatoren, noise, mixer, resonant laagdoorlaatfilter en twee contouren.
2. Alle zichtbare geluidsbedieningen uit de referentiefoto met de functies in §4, plus bereikbare glide/decay- en modulatiebediening.
3. Rechtstreekse ontvangst van een ondersteund class-compliant USB-MIDI-keyboard.
4. PCM5102A-lijnuitgang, hoofdvolume, main-output mute en A-440-referentietoon.
5. Werkende externe audio-invoer door filter/VCA en hoofdtelefoonuitgang met eigen volume voor de volledige referentiepaneelversie. Hiervoor ontbreken nog ADC- en hoofdtelefoonhardware; een eerdere prototypefase mag die missen, de volledige versie niet stilzwijgend.
6. Stabiele, klikarme bediening en reproduceerbare firmwarebuild.
7. Bewerkbare KiCad-, firmware- en mechanische CAD-bronnen, lokale bibliotheken, BOM, assemblage- en Carvera-instructies.

### Optioneel

MAX98357-luidsprekeruitgang, fysieke pitch/mod-wielen, geïntegreerd klavier, DIN-MIDI, MIDI OUT/THRU, USB-MIDI-device naar computer, presetscherm of extra waardedisplay. Polyfonie, sequencer, effecten en analoge CV/gate-aansluitingen horen niet bij de basisopdracht. De dedicated LFO uit de foto hoort wel bij de klankfuncties.

**Geen gelijkstelling van digitaal en analoog:** dit is een functionele digitale interpretatie met Minimoog-achtige klankdoelen. Exacte transistor-, drift-, filter- en schaalmodellen vragen afzonderlijke referentiemetingen.

## 3. Onderdelenregister en BOM

### 3.1 Aangeleverde Amazon-identificaties

De ASIN identificeert een winkelvermelding, niet betrouwbaar een fabrikantonderdeel, printrevisie of footprint. Rechtstreekse Amazon-pagina's waren tijdens deze controle niet uitleesbaar. Zoekindexen geven onderstaande **catalogusaanwijzingen**, geen bevestigde technische identiteit. Deze aanwijzingen mogen niet als basis voor footprint, spanning of pinout worden gebruikt.

| ID | Aangeleverde link | Identificatie / zekerheid | Gebruik en nog te controleren |
|---|---|---|---|
| BOM-01 | [B0CP3YCP57](https://www.amazon.de/dp/B0CP3YCP57) | Zoekaanwijzing: ARCELI ESP32-S3 DevKitC-1-achtige boardset, WROOM-1 N16R8. ESP32-S3 is projectkeuze; exact geleverd board OPEN. | Processor/USB-host. Lees modulemarkering, meet headers, controleer USB-UART/OTG, regulator en voedingsschema. Claim N16R8 pas na fysieke controle. |
| BOM-02 | [B0GMQ92458](https://www.amazon.de/dp/B0GMQ92458) | **Ongeïdentificeerd.** Geen bruikbare productidentificatie gevonden. | Producttitel, foto's beide zijden en markeringen nodig. Geen functie, spanning, hoeveelheid of footprint toewijzen. Niet aannemen dat dit de PCM5102A is. |
| BOM-03 | [B07VF14YNG](https://www.amazon.de/dp/B07VF14YNG) | Zoekaanwijzing: ICQUANZX CD74HC4067 16:1-multiplexermodules. | Alleen inzetten als chipmarkering/pinout bevestigd zijn en scanproef slaagt. Dit is geen ADC of I/O-expander. |
| BOM-04 | [B07ZCQZYW1](https://www.amazon.de/dp/B07ZCQZYW1) | Zoekaanwijzing: Youmile TCA9548A I²C-multiplexermodules. | Optioneel voor I²C-adresconflicten. Leest geen encodercontacten en vervangt geen GPIO-expander. |
| BOM-05 | [B09TVDZ8P2](https://www.amazon.de/dp/B09TVDZ8P2) | Zoekaanwijzing: RUNCCI-YUN mini-SPDT-schuifschakelaars, SS12D10-G5-achtig. Exact type OPEN. | Voor digitale tweestandenfuncties na contact- en passingtest. Geen netspanningsschakelaar ontwerpen op basis van de winkeltekst. |
| BOM-06 | [B0CJY1C287](https://www.amazon.de/dp/B0CJY1C287) | Zoekaanwijzing: Hailege MAX98357-module. A/B-variant en revisie OPEN. | Optionele luidspreker, geen lijnuitgang. I²S-compatibiliteit vereist controle van variant en straps. |
| BOM-07 | [B09SG3HF9N](https://www.amazon.de/dp/B09SG3HF9N) | **BEVESTIGD gebruiker:** kale encoders zonder breakout, monteerbaar op eigen PCB. Zoekaanwijzing: RUNCCI-YUN EC11 met drukschakelaar. | Meet pinnen, ankerlippen, as, bus, detents, pulsen en drukschakelaar. EC11 is een familie, geen unieke footprint. |
| BOM-08 | PCM5102A-module; ASIN nog niet gekoppeld | **BEVESTIGD gebruiker:** besteld. | Verplichte lijnaudio. Foto, leverancier, pinout, regulator, FMT/XSMT/SCK-configuratie en afmetingen nog nodig. |

Catalogusaanwijzingen zijn bewust niet opgewaardeerd tot geverifieerde BOM. Er is nog geen ontvangen fysieke component ingemeten. Aantallen per verpakking zijn niet gelijk aan aantallen beschikbaar voor dit project.

### 3.2 Ontbrekende of aanvullende onderdelen

| Onderdeel | Hoeveelheid / besluit | Reden |
|---|---|---|
| ESP32-S3-board | 1 functioneel exemplaar + eventueel reserve | Eerst BOM-01 verifiëren |
| Kale EC11-encoders | 27 hoofdpaneelposities; 28 inclusief aparte LFO-rate | Ontwerpaantal wanneer alle draaibedieningen encoders zijn; beschikbare voorraad tellen |
| Tweestandencontacten | 15 hoofdpaneelfuncties + glide + decay + LFO-shape = 18 | Power apart; extra encoderdrukcontacten tellen afzonderlijk |
| Digitale ingangsuitbreiding | VOORSTEL: parallel-in/serial-out registers op 3,3 V | Deterministisch alle encoderfasen tegelijk bemonsteren; exact bestelnummer/package nog kiezen |
| USB-A-hostconnector of passende hostadapter | 1 | Keyboard verbinden; mechaniek/footprint nog selecteren |
| USB-VBUS-loadswitch met stroombegrenzing, foutsignaal en terugstroombeveiliging | 1 circuit | Hostvoeding, loskoppelen bij fout; exacte onderdelen en stroomgrens na keyboardgegevens |
| Externe laagspanningsvoeding | 1; uitgang/budget nog dimensioneren | ESP32, USB-keyboard, DAC, ADC en eventueel speaker |
| Audio-ADC/codec + ingangscircuit | 1 pad | Echte externe audio via DSP. Een PCM5102A heeft geen audio-ingang |
| Hoofdtelefoonversterker + eigen volumeregeling | 1 stereopad of dual mono | Onafhankelijk volume; kies hardwarematige attenuatie of aparte digitaal geregelde gain |
| Audiojacks, kabels, headers, bevestigingen | Volgens definitief schema/CAD | Geen gatenpatronen aannemen |
| Ontkoppeling, bias/pull-ups, bescherming, connectoren | Per circuit dimensioneren | Nog geen afgeronde inkoop-BOM |
| LEDs en begrenzingsweerstanden | Power + overload, overige optioneel | Waarden berekenen op voedingsspanning/LED-stroom |

Voorstel volledig scannetwerk: 28 encoders × 2 fasen = 56 bits; 28 drukcontacten = 28 bits; 18 schakelaars = 18 bits; samen 102 bits. Reserveer **112 bits**, bijvoorbeeld 14 registers van 8 bits. Power niet als gewoon scancontact opnemen als het de voeding fysiek onderbreekt. Zonder onafhankelijke drukcontacten kan het aantal registers omlaag. Exact MPN en timing vóór schemafreeze vastleggen.

### 3.3 Componentdossier verplicht

Per onderdeel: ID, status, fabrikant/MPN indien bekend, winkel-ASIN, werkelijk aantal, foto's voor/achter, markeringen, datasheet/revisie, gemeten maten, pin-to-net-mapping, voedingsbereik, KiCad-symbol/footprint en verificatiedatum. Leveranciersmodule en kale IC als verschillende onderdelen registreren.

## 4. Bedieningsinventaris en gedrag

De foto bepaalt de sectievolgorde: **Controllers → Oscillator Bank → Mixer → Modifiers → Output**, met houten omlijsting. De extra modulatiekeuzeschakelaars wijzen op een uitgebreidere Model D-uitvoering; geen jaartal vastleggen op basis van de foto. Exacte afmetingen zijn niet uit de afbeelding af te leiden.

### 4.1 Hoofdpaneel: 27 draaibedieningen

Onderstaande numerieke bereiken zijn **VOORSTEL voor deze digitale implementatie**, tenzij anders aangegeven. Het zijn geen gegarandeerde schalen van een historisch instrument. Gebruik stabiele parameter-ID's in firmware, tests en CAD-mapping.

| Sectie | Parameter-ID / paneeltekst | Aantal | Implementatiecontract |
|---|---|---:|---|
| Controllers | `master.tune` / Tune | 1 | −100…+100 cent, nul exact bereikbaar; alle keyboard-gestuurde oscillatoren |
| Controllers | `glide.time` / Glide | 1 | 0…10 s als instelbare tijdconstante; glide-enable apart; digitale benadering documenteren |
| Controllers | `mod.mix` / Modulation Mix | 1 | 0…1, lineaire balans tussen bron A en B |
| Oscillators | `osc[1..3].range` / Range | 3 | Zes discrete standen: LO, 32′, 16′, 8′, 4′, 2′; geen wrap bij grens |
| Oscillators | `osc[2..3].detune` / Frequency | 2 | Voorstel ±7 semitonen, fijn instelbaar tot 1 cent; osc. 3 krijgt eigen vrije frequentiemapping bij keyboard-control uit |
| Oscillators | `osc[1..3].wave` / Waveform | 3 | Zes standen; waveformsets hieronder; uitsluitend stappen, geen continue morph |
| Mixer | `mix.osc[1..3]` / Volume | 3 | Onafhankelijke gain 0…1, gaincurve vastleggen |
| Mixer | `mix.external` / External Input Volume | 1 | ADC-signaalgain; alleen werkzaam als ADC-pad bestaat en input-enable aan staat |
| Mixer | `mix.noise` / Noise Volume | 1 | Gain 0…1; noisegenerator blijft beschikbaar voor modulatie bij audiomute |
| Filter | `filter.cutoff` / Cutoff Frequency | 1 | Logaritmisch 20 Hz…20 kHz nominaal; daadwerkelijke DSP-grens afhankelijk van samplefrequentie/stabiliteit |
| Filter | `filter.resonance` / Emphasis | 1 | 0…1 → gevalideerde feedbackmapping; zelfoscillatie als klankdoel |
| Filter | `filter.env_amount` / Amount of Contour | 1 | Positieve envelopinvloed; voorstel 0…8 octaven, begrenzen vóór filtercoëfficiënten |
| Filter contour | `env.filter.attack/decay/sustain` | 3 | Attack/decay 1 ms…10 s logaritmisch; sustain 0…1 |
| Loudness contour | `env.amp.attack/decay/sustain` | 3 | Dezelfde eenheden; onafhankelijk van filtercontour |
| Output | `output.main_volume` / Volume | 1 | −60…0 dB plus echte mute-stand; klikarme gainramp |
| Output | `output.phones_volume` / Phones Volume | 1 | Onafhankelijke hoofdtelefoongain; vereist aanvullende hardware, zie §7 |
| **Totaal** | | **27** | Waarvan 6 discrete selectors en 21 overige draaiparameters |

Waveformset als projectdoel: osc. 1/2: triangle, triangle/saw-hybrid, saw, square, brede pulse, smalle pulse. Osc. 3 vervangt de hybrid door reverse saw. Voorstel pulse duty 50%, 25%, 12,5%; exacte historische duty en hybridvorm worden pas als authentiek aangeduid na verdere onderbouwing. Oscillatoren lopen vrij, ook wanneer hun mixerschakelaar uit staat. Geen hard-sync of PWM toevoegen aan de basisbediening.

### 4.2 Hoofdpaneel: 15 tweestandenfuncties plus power

| ID | Functie | Gedrag |
|---|---|---|
| `mod.osc_enable` | Oscillator Modulation | VOORSTEL: moduleert osc. 1 en 2 via modwheel; osc. 3 blijft in dit profiel ongemoduleerd als stabiele bron. Afwijkende authentieke routering alleen na broncontrole als apart profiel |
| `osc3.keyboard` | Osc. 3 Control | Aan: volgt note/glide. Uit: vrijlopende frequentie, onafhankelijk van gespeelde note |
| `mod.source_a` | Osc. 3 / Filter EG | Linker bron van modulation mix |
| `mod.source_b` | Noise / LFO | Rechter bron van modulation mix |
| `mix.osc1_enable` | Osc. 1 On | Alleen bijdrage aan audiomixer muten |
| `mix.osc2_enable` | Osc. 2 On | Idem |
| `mix.osc3_enable` | Osc. 3 On | Idem; osc. 3-modulatie blijft functioneren |
| `mix.external_enable` | External Input On | Externe audio wel/niet vóór filter mengen |
| `mix.noise_enable` | Noise On | Audiobijdrage aan/uit; modulatiepad apart |
| `noise.type` | White / Pink | Selectie audioruis; modulatiekleur hieronder |
| `mod.filter_enable` | Filter Modulation | Gemengde bron via modwheel naar cutoff |
| `filter.keytrack1` | Keyboard Control 1 | Draagt 1/3 octaaf/octaaf bij |
| `filter.keytrack2` | Keyboard Control 2 | Draagt 2/3 octaaf/octaaf bij; samen 1 octaaf/octaaf |
| `output.main_enable` | Main Output On | Alleen lijnuitgang muten; phones onafhankelijk |
| `output.a440` | A-440 | Onafhankelijke sinus van 440 Hz naar outputbus, voorstel −18 dBFS vóór outputvolume; geen MIDI-noot nodig |
| `power` | Power + LED | Fysieke laagspanningsvoeding schakelen of gecontroleerd enablecircuit; elektrische uitvoering OPEN |

### 4.3 Performancefuncties buiten de getoonde uitsnede

- `glide.enable`: glide aan/uit, bereikbaar als fysieke schakelaar op een extra bedieningsstrook of achter/zijpaneel; ook via MIDI.
- `env.decay_enable`: bepaalt release van **beide** contouren. Aan: release gebruikt de eigen decaytijd. Uit: korte klikarme release, voorstel 3 ms. Geen afzonderlijke releaseknop op hoofdpaneel.
- `lfo.rate`: voorstel 0,05…30 Hz, extra encoderpositie; `lfo.shape`: triangle/square via eigen schakelaar of drukactie met zichtbaar feedbackmechanisme.
- Pitchbend en modwheel via USB-keyboard verplicht. Fysieke wielen optioneel; eigenschappen en maten nog niet vastgelegd.
- Een geïntegreerd klavier is niet bevestigd. Begin met desktopmodule plus extern USB-keyboard. Laat definitieve kastvorm nog niet afhangen van een verzonnen klaviermaat.

### 4.4 Encoderervaring

Encoders zijn relatieve quadratuurcontacten, geen potentiometers. Een vast pijltje op een eindeloos draaiende knop geeft geen betrouwbare parameterwaarde. Behoud referentie-indeling, maar leg dit verschil uit in de gebruikershandleiding. Voorstel: één klein, apart geplaatst waardedisplay voor laatst bewogen parameter; type en plaats OPEN, niet automatisch 27 LED-ringen ontwerpen.

Eén detent geeft één selectorstap. Continue parameters gebruiken fijne stappen en optionele snelheidsversnelling; drukken-en-draaien mag fijnregeling geven, geen essentiële verborgen functie. Voor sustain/gains voorstel 1% per detent, tune 1 cent, detune 5 cent met 1 cent fijnstand; logparameters gebruiken een tabel met 256 posities. Defaults en resetwaarden uit één parameterregister halen. Drukcontacten blijven beschikbaar maar alle 28 hoeven geen functie te krijgen.

Fysieke schakelstand prevaleert bij opstarten. Bij externe parameterwijzigingen of presetladen blijft een latching switch softwarematig op de geladen waarde tot de gebruiker die schakelaar bedient; toon afwijking waar mogelijk. Encoderwaarden hoeven geen pickupgedrag te hebben. Zonder display eerst een bruikbare diagnose-interface leveren; definitieve bediening pas na een proefpaneel vastzetten.

## 5. Synthese- en DSP-contract

### 5.1 Signaalpad

`USB-MIDI → note/gate/pitch/performance → 3 oscillatoren + white/pink noise + externe ADC → bron-gains/mutes → mixer/drive → 4-pole low-pass → amplitude contour/VCA → outputbus (+ A440) → uitgangsgains/mutes → I²S-DAC`

Filtercontour, modulatiemix en keytracking beïnvloeden cutoff; osc. 3 en LFO lopen ook zonder gate. Hoofdtelefoon volgt dezelfde muzikale bus met eigen gain. Optionele speaker krijgt dezelfde bus; eigen mute/gain mag via de versterker worden geregeld.

### 5.2 Numerieke standaard — VOORSTEL

- Audio 48.000 samples/s, mono synthese; stereo-I²S met dezelfde mono-inhoud op L/R. Interne berekening float32, uitvoer in 32-bit slots met correct uitgelijnde 24 betekenisvolle bits.
- Start met blokken van 64 frames, dus 1,333 ms per blok. DMA-bufferdiepte afstemmen op gemeten latency. MIDI-events krijgen sampletimestamps voor plaatsing binnen een blok.
- 8′ = MIDI-note pitch; 32′/16′/4′/2′ = −24/−12/+12/+24 semitonen. `f = 440 * 2^((note-69+offset+bend+mod)/12)`. Tune in cent omzetten naar semitonen.
- LO krijgt een eigen lage mapping. Eerste voorstel: keyboard-pitch gedeeld door 128 indien tracking aan; bij osc. 3 tracking uit een logregelbare 0,05…30 Hz in LO en 20…2000 Hz buiten LO met range-offset. Dit is een digitale keuze, nog geen historische kalibratie.
- PolyBLEP/minBLEP of bandlimited wavetable-oscillatoren. Triangle/hybrid moeten eveneens een onderbouwde anti-aliasingstrategie hebben. Audio-rate pitchmodulatie vraagt een afzonderlijke aliasingtest.
- Vierpolig resonant filter met verzadiging en begrensde feedback; keuze uit aantoonbaar stabiele ladderbenadering na benchmark. Zelfoscillatie mag, ongecontroleerde amplitude/NaN niet. Niet enkel vier ongecorrigeerde éénpolers met willekeurige feedback als eindmodel opleveren.
- Doel: niet-lineair mixer/filterpad op 2× oversampling, inclusief anti-imaging/decimationfilters. CPU-metingen bepalen haalbaarheid; lagere kwaliteit expliciet als prototypeprofiel labelen.
- Mixer behoudt headroom bij meerdere bronnen; gainstaging vastleggen met een referentiesinus. Optionele drive is vaste modelinstelling, geen extra hoofdpaneelknop. Outputbeveiliging voorkomt digitale overflow, maar vervangt geen stabiel filter.
- White noise met reproduceerbare seed in tests; pink via gedocumenteerd filter. Voor modulatie bij white-audio pink-noise gebruiken, bij pink-audio red-noise als doel voor het gekozen reissuegedrag. Normalisatie en DC-verwijdering vastleggen.
- EG's hebben attack, decay, sustain en release volgens decay-switch. Exponentiële curves als voorstel, tijden definiëren tot 99%/1% van eindwaarde. Retrigger start vanaf actuele waarde om sprongen te voorkomen.
- MIDI-legato: voorstel low-note priority en single trigger; eerste ingedrukte noot opent gate, overlappende noten wijzigen pitch zonder nieuwe attack. Optionele last-note priority/multitrigger via configuratie.
- Glide: exponentiële overgang in semitoondomein met ingestelde tijdconstante; aan/uit testbaar. Niet als gemeten originele glidecurve presenteren.
- Modbus: `m = (1-x)*A + x*B`; `depth = CC1/127`. Filter-EG-bron unipolair; oscillator/LFO/ruis bipolair. Pitchmodulatie voorstel maximaal ±12 semitonen op osc. 1 en 2; filtermodulatie maximaal ±4 octaven. Dit zijn kalibreerbare projectwaarden. Osc. 3 ontvangt in het basisprofiel geen pitchmodulatie en krijgt geen algebraïsche zelfmodulatielus.
- Keytracking: `k = switch1/3 + 2*switch2/3`; cutoff-octaven krijgen `k*(note-60)/12`. Contour en modulatie erbij optellen en dan naar veilige cutoff vertalen. Beslis expliciet of glide/keybend keytracking beïnvloeden; prototype: glided note wel, pitchbend niet.
- Gain/cutoff/modulatiediepte gladstrijken, voorstel 5 ms; mute 3 ms. Toonhoogte-events blijven snel; geen algemene smoothing die de timing van MIDI-noten onvoorspelbaar maakt.

### 5.3 Echtetijdeisen

Geen heapallocatie, flashwrite, display-update, USB-enumeratie, blokkerende bus-I/O of logging in de audiolus. Coëfficiënten veilig berekenen; alle parameters begrenzen; denormals/NaN/Inf afvangen. Parameterwijzigingen via begrensde queue of dubbelbuffer-snapshot. Audio en hardware-I/O gebruiken geen gedeelde lock die de audio kan laten wachten.

DMA-buffers in geheugen dat de gekozen ESP-IDF-configuratie expliciet ondersteunt. PSRAM is geen veronderstelde oplossing voor deadlines; plaats kritische data eerst in intern RAM. Wi-Fi/BLE standaard uit. Taak-/core-affiniteit na metingen vastzetten, met audio hoogste passende prioriteit. Controleer releasebuild, stack-watermarks en geheugengebruik.

## 6. MIDI en USB

### 6.1 Verplichte hostmodus

De ESP32-S3 bezit USB-OTG, maar een developmentboard met USB-connector is daarmee nog geen complete gevoede keyboardhost. Ontwerp een hostconnector met 5 V VBUS, begrensde stroom, foutafhandeling, ESD en terugstroompreventie. D−/D+ via de interne PHY gebruiken GPIO19/20; die pinnen reserveren. De interne PHY wordt gedeeld met USB-Serial/JTAG. Gebruik voor programmeren bij voorkeur de aparte USB-UART-brug indien BOM-01 die werkelijk heeft. [Espressif USB Host](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/usb_host.html?highlight=usb+serial).

**Geen gelijktijdige USB-MIDI-host én USB-MIDI-device op dezelfde OTG-controller plannen.** Extra externe PHY maakt daarvan geen tweede OTG-controller. Een tweede host/device-controller of aparte processor is een uitbreiding. Native USB-Serial/JTAG en OTG delen zonder extra PHY evenmin gelijktijdig dezelfde verbinding.

Voorkeur prototype: bestaande native USB-poort met gecontroleerde hostadapter en apart bewezen voedingspad; daarna pas geïntegreerde hostpoort ontwerpen. Geen twee fysieke poorten parallel op D+/D− bedraden. USB-C-rollen/CC en VBUS niet oplossen met alleen een willekeurige verloopkabel. USB-keyboard kan een eigen voeding hebben; model en werkelijk verbruik blijven OPEN.

Ondersteun als basis USB MIDI 1.0 class-compliant full-speed apparatuur met bulk-MIDI-endpoints. HID-computertoetsenbord is geen MIDI-keyboard. MIDI 2.0/UMP, vendor-drivers, high-speed-only apparatuur, hubs en samengestelde audio/MIDI-apparaten alleen na aparte compatibiliteitstest. USB-hostbibliotheek alleen is onvoldoende: MIDI-class parser/driver en vierbyte USB-MIDI-eventpacketverwerking horen bij de implementatie.

USB disconnect: maak alle noten van die bron vrij, sluit gate, herstel VBUS-fout veilig en blijf audio renderen. Herhaald aansluiten moet zonder reboot werken. Bewaar VID/PID, interface/endpoints en fouten in diagnosegegevens. Exact keyboardmodel is nog nodig voor eindacceptatie; niet universele compatibiliteit claimen.

### 6.2 MIDI-berichten

| Bericht | Vereist gedrag |
|---|---|
| Note On/Off | Kanaal 1 standaard, instelbaar 1…16; velocity 0 als Note Off; monofone held-note-administratie, inclusief herhaalde note-ons |
| Velocity | Standaard geen invloed op klank voor basisgedrag; optioneel configureerbare amp/filtergevoeligheid |
| Pitch Bend | 14 bit, midden 8192; standaard ±2 semitonen; bereik configureerbaar en RPN 0,0 ondersteunen |
| CC1 | Modwheel 0…1; noodzakelijk voor modulatiebediening met extern keyboard |
| CC5 / CC65 | Glide-tijd / glide-enable |
| CC64 | Sustainpedaal; loslaten ruimt uitgestelde note-offs correct op |
| CC7 / CC11 | Kanaalvolume / expression; multiplicatief bovenop paneelvolume, niet stilzwijgend paneelparameter overschrijven |
| CC120 | All Sound Off: directe korte veiligheidsramp, held-note-state legen |
| CC123 | All Notes Off: notes vrijgeven met normale sustain/releasepolicy; policy testen |
| CC121 | Controllers resetten; bend/mod/expression/sustain herstellen, geen paneelpatch wissen |
| Program Change | Pas actief bij geïmplementeerde presets; anders gedocumenteerd negeren |
| Clock/aftertouch/SysEx | Niet crashen; standaard negeren tenzij expliciet gemapt; SysEx begrensd parsen |

Voor DIN-uitbreiding: 31.250 baud 8-N-1, correcte optisch geïsoleerde MIDI-IN volgens geldende MIDI-elektrische specificatie. Geen DIN-pinnen rechtstreeks naar ESP32-GPIO. Exact schakeling/waarden later verifiëren; DIN is geen vervanging voor de verplichte USB-host.

### 6.3 Eigen parameter-CC-mapping — VOORSTEL

Deze mapping is project-eigen, geen claim van compatibiliteit met Moog-hardware of plugins. CC1/5/7/11/64/65 en RPN-functies hierboven reserveren. Overige paneelparameters standaard alleen ontvangen; MIDI-zenden optioneel om feedbacklussen te vermijden.

| CC | Parameter | CC | Parameter |
|---:|---|---:|---|
| 20 | master.tune | 21 | mod.mix |
| 22/23/24 | osc. 1/2/3 range | 25/26 | osc. 2/3 detune |
| 27/28/29 | osc. 1/2/3 wave | 30/31/33 | mix osc. 1/2/3 |
| 34/35 | external/noise level | 36/37/38 | osc. 1/2/3 enable |
| 39/40 | external/noise enable | 41 | noise.type |
| 42/43/44 | osc-mod/osc3-key/filter-mod | 45/46 | mod source A/B |
| 47/48 | keytrack1/keytrack2 | 49 | filter.env_amount |
| 50/51/52 | filter A/D/S | 53/54/55 | amp A/D/S |
| 56 | decay-enable | 57/58 | LFO rate/shape |
| 59 | main-enable | 60 | phones-volume |
| 71/74 | resonance/cutoff | — | A440 alleen lokaal, voorkomt onverwachte referentietoon |

Continu: normaliseer 0…127 en gebruik parametercurve; switches: <64 uit, ≥64 aan; selectors met N waarden: `min(N-1, floor(value*N/128))`. Midden van bipolar tune/detune bij 64 exact nul maken. MIDI-uitvoer alleen bij lokale wijzigingen, nooit automatisch ontvangen CC terugzenden. Kanaal, mapping en schema-versie opslaan.

## 7. Audio-elektronica

### 7.1 PCM5102A als lijn-DAC

Chipdocumentatie beschrijft een stereo-lijn-DAC met PLL en nominale 2,1 Vrms full-scale-uitgang. Dit zijn chipgegevens; de modulevoeding, filters en connectors moeten afzonderlijk worden gecontroleerd. [TI PCM5102A datasheet](https://www.ti.com/lit/ds/symlink/pcm5102a.pdf).

Verbinding logisch: ESP32 I²S-BCLK → BCK; LRCLK → LCK/LRCK; DATA → DIN; gemeenschappelijke signaalmassa. Geen definitieve GPIO-nummers of headerpinnummers invullen vóór pinplancontrole. SCK/MCLK-behandeling, FMT voor standaard I²S, XSMT/mute, DEMP/FLT en voedingspinnen volgens datasheet én werkelijk moduleschema vastleggen. Nooit onbekende straps zwevend laten of een module-VIN als kale chip-voeding behandelen.

48 kHz × 2 kanalen × 32 bits geeft 3,072 MHz BCLK en 48 kHz LRCLK als prototypeconfiguratie. Controleer met logic analyzer bitdelay, slotlengte en data-uitlijning. Breng dezelfde mono-inhoud op L/R; niet de analoge uitgangen rechtstreeks samenknopen. Selecteer één kanaal voor mono TS, of afzonderlijke L/R-jacks. Connectorindeling expliciet tekenen; een TRS-stereojack is geen gebalanceerde mono-uitgang.

Ontwerp mute bij boot/clockverlies, digitaal volumeramp en eventuele uitgangsbeveiliging/buffering volgens belasting. Lijnuitgang is geen speakerdriver en niet automatisch geschikt voor hoofdtelefoonbelasting. Meet werkelijke uitgangsamplitude, DC, ruis en clipping met hoogohmige lijningang.

### 7.2 Onafhankelijke hoofdtelefoon

Twee gelijke DAC-kanalen met dezelfde samples geven geen onafhankelijk digitaal main/phonesvolume. Voorkeursoplossing: neem een gedeeld audiosignaal vóór de onafhankelijke analoge uitgangsregelingen; hoofdtelefoonversterker heeft eigen regelbare gain/attenuator, main heeft eigen mute/gain. Alternatief: aparte DAC-kanalen als twee mono-bussen, waarvan het phoneskanaal naar twee correct gebufferde oorkanalen gaat. Dan wordt de I²S-kanaalinhoud bewust verschillend en moet het hele outputcontract worden aangepast.

Kies één oplossing vóór audioschemafreeze; leg meetbare belasting, maximaal niveau, gain en mute vast. Headphone-regelaar als encoder vereist een digitaal bestuurbare gaintrap of eigen DAC-bus; een kale analoge pot is een expliciete alternatieve ontwerpkeuze. Geen hoofdtelefoon direct aan PCM5102A of MAX98357-speakeruitgangen aansluiten.

### 7.3 Externe audio

Externe audio moet vóór de digitale filter/VCA worden gemengd. Daarvoor is een audio-ADC/codec nodig met geschikt lijn-ingangsnetwerk, bias, anti-aliasfilter en bescherming. Gebruik geen ESP32-langzame potmeter-ADC of CD74HC4067 als vervanging voor dit audiopad. ADC heeft passende klok/samplerate en synchrone I²S-RX of aantoonbare driftcompensatie nodig. Benchmark gelijktijdige RX/TX en USB-host voordat pinplan wordt vrijgegeven.

Overload-LED: voorstel aan boven −1 dBFS op ADC of bij te grote pre-filtermix, met circa 100 ms zichtbare hold; onderscheid ADC-clipping en gewenste model-drive in diagnose. Specificatie van toegestane ingangsniveaus en connector is OPEN. Tot ADC is toegevoegd toont de firmware external-input als niet beschikbaar; geen nep-werkende knop.

### 7.4 Optionele MAX98357

MAX98357A ondersteunt I²S; B gebruikt left-justified. Variant identificeren vóór gedeelde aansluiting met PCM5102A. BCLK/LRCLK/DATA kunnen bij compatibele configuratie beide ontvangermodules voeden; valideer bekabeling/klokken. SD/gain/kanaalselectie volgens werkelijk circuit. [Analog Devices MAX98357A](https://www.analog.com/en/products/max98357a.html).

De klasse-D-luidsprekeruitgang is een bruguitgang: speaker tussen OUT+ en OUT−. Geen van beide aansluitingen aan massa, lijnjack, hoofdtelefoon of geaarde oscilloscoopclip leggen. Meet differentieel waar vereist. Speakerimpedantie, vermogen en voeding selecteren vóór montage. De commerciële aanduiding “3W” is geen garantie onder elke voeding/belasting. Versterker optioneel afschakelbaar en stroompad weg van de lijn-DAC houden.

## 8. Besturingselektronica en pinplan

### 8.1 Voorkeursarchitectuur

Splits in sectieprinten achter het paneel en een compacte core/audio-print. Alle encoders blijven kale componenten op eigen gefreesde printen; geen gekochte encoderbreakouts nodig. Een enkele brede PCB alleen kiezen als werkbereik, materiaal en vlakheid dat aantoonbaar toelaten.

Voorstel: 3,3V-ingangsregisters in een keten met gezamenlijke parallel-load, clock en data. Capture alle bits tegelijk en lees de keten daarna uit. Bij 112 bits en 1 MHz duurt serialisatie 112 µs; bij 1 kHz capture circa 11,2% busbezetting zonder overhead. Gebruik dit als rekenvoorbeeld, niet als gegarandeerde bekabelingslimiet. Scanpriority mag audiodeadlines niet blokkeren.

Iedere encoder A/B heeft een eigen pull-up; common naar GND pas na continuïteitstest. Drukschakelaar apart. Beginvoorstel pull-ups 10 kΩ naar 3,3 V, daarna contactstromen en ruis controleren; module-interne weerstanden kunnen dit veranderen. Mechanische metalen lippen niet automatisch als elektrische common modelleren. Filterwaarden kiezen na bounceproef; zware RC mag quadratuurfase niet uitwissen.

Decoder: volledige Gray-state-transitiontabel, geldige overgangen accumuleren, ongeldige sprongen tellen/verwerpen. Detentrelatie proefondervindelijk vastleggen; niet aannemen dat iedere EC11 vier overgangen per klik heeft. Debounce van drukknoppen/schakelaars circa 5…10 ms als voorstel. Geen 10ms-blokkering op iedere encoderfase.

Stresstestdoel: twee encoders tegelijk, ieder 30 detents/s, zonder foutieve richting of verloren detents, gedurende minimaal 60 s. Verifieer ook snellere overgangen met generator/logic analyzer. Pas samplefrequentie aan als de fysieke pulsen korter blijken dan betrouwbaar te vangen.

### 8.2 Gebruik aangeleverde multiplexers

**CD74HC4067:** 16:1 bidirectionele analoge schakelaar, geen opslag en geen ADC. Bruikbaar voor latere potmeters of bewezen digitale scanning. Voor 28 encoders is 56-fasen-scanning nodig; afzonderlijk multiplexen van A/B kan overgangen missen. Niet de standaardroute totdat een complete scan- en contacttest gelijkwaardige betrouwbaarheid aantoont. Voed logica voor dit ontwerp op 3,3 V na chipcontrole; HC en HCT niet verwarren. [TI CD74HC4067](https://www.ti.com/product/CD74HC4067).

**TCA9548A:** I²C-busschakelaar voor acht takken; maakt geen encoder-GPIO. Alleen gebruiken bij adresconflicten of noodzakelijke bussegmentatie; anders weglaten. Bij gebruik per tak pull-ups, capaciteitsbudget, reset en recovery vastleggen. [TI TCA9548A](https://www.ti.com/product/TCA9548A).

### 8.3 Pinplan als apart verplicht ontwerpbestand

Registreer per signaal: functie, ESP32-GPIO, boardheaderpin, richting, spanningsdomein, boottoestand, connectorpin, bron en verificatiestatus. Reserveer USB GPIO19/20; I²S-TX minimaal drie signalen; RX/ADC-klokken aanvullend; scanbus minimaal load/clock/data; UART-debug, VBUS-enable/fault en mute. Reserveer toekomstige I²C/display alleen als werkelijk gekozen.

Voor een mogelijke N16R8-uitvoering mogen geheugenpinnen niet blind als vrije GPIO worden gebruikt; onder meer GPIO35–37 kunnen door octal geheugen bezet zijn. Vermijd boot-strapbelasting en controleer onboard LED/USB-UART-conflicten. Een officiële DevKitC-pinout is geen bewijs voor een clone-footprint. [Espressif DevKit-documentatie](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp-dev-kits-en-master-esp32s3.pdf).

Pinplan inclusief ADC/phones-optie moet sluitend zijn vóór definitieve PCB-routing. USB-signalen kort en met geschikte impedantie/retourpad ontwerpen; gebruik in prototype liever de bestaande modulepoort dan een lange gefreesde uitbreiding.

## 9. Voeding, massa en aansluitingen

Alleen externe laagspanningsvoeding in de kast. Maak een stroomtabel met ESP32-pieken, keyboard descriptor/werkelijke stroom, DAC/ADC, display, phones en optionele speaker, plus voorstel 30% marge. Geen definitieve voeding kopen alleen op basis van een fictieve 5V/2A-aanname.

Leg hoofdrail, 3,3V-regeling en module-VIN's afzonderlijk vast. ESP32-GPIO zijn geen 5V-ingangen. Voorkom terugvoeding tussen externe voeding, programmeer-USB en host-VBUS. Overstroom, ompoling waar relevant en inschakelgedrag testen. Gebruik de developmentboardregelaar niet automatisch voor het hele paneel of keyboard.

Ontkoppel lokale IC's volgens datasheets, startvoorstel 100 nF per digitale voedingspin met lokale bulk waar nodig. Houd speakerstromen en digitale klokretouren uit gevoelige audioroutes; behoud een doordacht doorlopend retourpad en maak geen willekeurige gescheiden massa-eilanden. Definieer aansluiting van jackhulzen, metalen paneel en afscherming. Audio- en voedingskabels mechanisch ontlasten.

Per connector: unieke referentie, sleutel/orientatie, tabel met pin/net/spanning, kabeltype, lengte, mating part en servicefunctie. Geen ongedefinieerde “JST”-footprints. BOOT/RESET en programmeren bereikbaar zonder de houten kast uiteen te nemen.

## 10. Firmwareproject en gegevensmodel

VOORSTEL: ESP-IDF met C++ voor DSP en hardwareabstractie; concrete stabiele SDK-versie kiezen na host-MIDI/I²S-prototype en in lock/config vastleggen. Geen fictieve library/API gebruiken. MIDI-hostondersteuning van gekozen versie werkelijk bouwen en testen; bibliotheeklicenties opnemen.

Voorgestelde bronstructuur:

```text
firmware/
  main/                 boot en samenstelling
  components/audio/     I2S, DMA, outputrouting, diagnostiek
  components/dsp/       oscillators, mixer, ladder, EG, noise, LFO
  components/midi/      USB-host MIDI, parser, note allocator
  components/controls/  scan, quadrature, switches, mapping
  components/state/     parameters, presets, versie/migratie
  components/board/     bevestigde pinmap en hardwareconfiguratie
  test/                 host-DSP en protocoltests
hardware/               KiCad + lokale libraries + meetdossiers
mechanical/             parametrische CAD en paneel-master
manufacturing/          revisiegebonden exports en CAM
docs/                   BOM, bedrading, build, assemblage, testlogs
```

Eén parameterregister bevat ID, type, eenheid, minimum/maximum, default, curve, encoderstap, smoothing, MIDI-map en persistentie. Daaruit waar praktisch documentatie/mapping genereren. Geen verschillende schaalformules verspreid over UI en DSP.

Boot: outputs muten → power/USB/scan initialiseren → fysieke switches lezen → initpatch laden → I²S met nuldata starten → state valideren → output gecontroleerd vrijgeven. USB-keyboard mag later verbinden. Fout in opslag of keyboard mag audio-init niet blokkeren.

Initpatch voorstel: osc.1 8′ saw aan op gematigde gain, osc.2/3/noise/external uit; cutoff 5 kHz, resonance laag, contouramount 0; amp A=5 ms D=200 ms S=0,8; filter A=5 ms D=200 ms S=0; modwheel=0; glide uit; main-volume −18 dB. Definitieve mute/enable volgt fysieke schakelstanden. A440 volgt eigen schakelaar. Tune/detune nul.

Presets zijn optioneel maar architectuur moet ze toelaten. NVS-opslag versiebeheer, boundscheck, dubbele/atomische commit en migratie; nooit op elke encoderpuls schrijven. Alleen expliciete save of uitgestelde niet-audiotaak. Diagnose: CPU piek, blokdeadline, underruns, queue-overflows, scanfrequentie, ongeldige encodertransities, USB-status en voedingsfouten.

## 11. Tweezijdige Carvera-PCB

### 11.1 Ontwerpregels

- Twee koperlagen, lokaal gefreesde isolatie. Ga uit van **niet-doorgemetalliseerde** gaten.
- Elke laagovergang expliciet als draad-via/rivet met assemblage-instructie. Pad aan beide zijden betekent niet dat er automatisch elektrisch contact tussen zit.
- Through-hole-pinnen kunnen alleen als laagverbinding dienen als beide zijden echt soldeerbaar zijn. Onder encoderhuizen, sockets en vlak gemonteerde modules dus geen verborgen verplichte top-soldeerverbinding ontwerpen.
- Voorkeur ruime THT en soldeerbare SMD-packages boven zeer fijne pitch. Modulegebruik kan kale audio-IC-packages vermijden. Vereiste registerpackages eerst op freesbaarheid toetsen.
- Kies spoorbreedte, clearance, padannulus en boorgat op basis van freesdiameter, runout, koper, z-nauwkeurigheid en registratiecoupon. Voorstel startcoupon 0,4 mm signaalsporen en 0,4 mm clearance; geen vrijgegeven machinecapaciteit. Voedingssporen volgens stroom/temperatuur dimensioneren.
- Mechanische encoderankers en panel-load met steunen opvangen. Koper/FR4 niet alle druk- en draaikrachten laten dragen.
- Maak testpunten voor rails/GND, I²S, scan en mute; houd ze bereikbaar.

### 11.2 Registratie en freesvolgorde

1. Meet werkelijk machinewerkbereik, fixture, gereedschappen, plaatdikte en koper. Leg Carvera-uitvoering en CAM/postprocessorversie vast; Carvera en Carvera Air niet uitwisselen zonder controle.
2. Maak een dubbelzijdige testcoupon met fijne/grove isolatie, gaten, via's en minimaal één encoder en moduleheader.
3. Definieer één CAD-oorsprong, flips-as en asymmetrische herkenning. Zet registratiegaten buiten de uiteindelijke printcontour; gebruik een gedocumenteerde pen-/fixturemethode.
4. Produceer top, gaten en bottom in de volgorde die bij de bewezen fixture past. Noteer welke gaten in welke opstelling worden gemaakt. Hoogtemeting per zijde indien vereist.
5. Controleer spiegeling in CAM met herkenbare tekst/asymmetrische testvorm; vertrouw niet op een generieke “bottom altijd spiegelen”-regel.
6. Houd contour vast met tabs of passend fixtureprincipe; contour pas losmaken nadat registratiewerk klaar is.
7. Ontbramen/reinigen; isolatie en top/bottom-uitlijning meten vóór solderen.
8. Via's/rivets aanbrengen, continuïteit per net en shorts tussen naburige netten testen. Soldeerbaarheid van beide zijden inspecteren.

Freesdiepten, toerental, feeds, toolnumbers en nulpunten zijn **OPEN** tot coupon/procesvalidatie. Geen machineklare G-code uit alleen deze tekst genereren. Stofafzuiging, materiaalhantering en machinegebruik volgens actuele Makera-handleiding en beschikbare tooling uitvoeren.

### 11.3 Productiepakket

KiCad-project, schema-PDF, 1:1 top/bottom-assemblagetekeningen, F.Cu/B.Cu/Edge.Cuts Gerbers, gescheiden relevante drillbestanden, drillmap, netlist/controlebestand, BOM, via-/rivetlijst, CAM-project, gevalideerde toolpaths en setupblad met oriëntatiefoto. Gerbers zijn overdrachtsbestanden; een reproduceerbaar CAM-project en bewezen postprocessor blijven nodig voor Carvera.

ERC/DRC zonder onverklaarde fouten. Iedere waiver heeft reden en revisie. Eigen CNC-regels expliciet meenemen, ook waar KiCad standaardfabrieksregels iets toestaan dat thuis niet assembleerbaar is.

## 12. Paneel, mechaniek en houten kast

Gebruik één parametrische paneel-master als bron voor encoderassen, schakelaars, LEDs, jacks, PCB-bevestigingen en gravure. Coördinaten in mm; definieer frontaanzicht, datum en positieve assen. Exporteer dezelfde oorsprong naar PCB-plaatsing en paneel-DXF/STEP. Geen afzonderlijk overgetypte gatenlijsten zonder vergelijking.

De foto is visuele stijlreferentie: secties, labels, kleuraccenten en relatieve ordening. Afmetingen, paneeldikte, hoek, houtsoort, wanddikte en buitenmaat blijven OPEN. Kies schaal pas na knopdiameters, vrije vingerruimte en machinewerkbereik. Een breed paneel of print kan in secties worden gemaakt; de voegen moeten mechanisch/visueel worden ontworpen.

Per encoder meten: asdiameter/-vorm/-lengte, schroefbusdiameter/-lengte, bodyhoogte, voetvlak, signaalpinnen, montageankers en drukweg. Controleer of paneeldikte + ringen + moer voldoende schroefdraad overlaten en knoppen niet tegen het paneel lopen. Voor mini-schuifschakelaars bepalen of de actuator lang genoeg is; eventueel paneeluitsparing/uitsparing achterzijde of andere schakelaar nodig.

Maak een stack-uptekening: voorkant knop → paneel → moer/ring → encoderbody → PCB → standoff → achterwand. Leg tolerantie per maat vast en bereken slechtste passing; geen generieke gatdiameter als definitieve maat. Elektrische en mechanische boorgaten afzonderlijk specificeren.

Houten kast: verwijderbaar servicepaneel, standoffvoorzieningen, kabelroutes, ventilatie indien metingen dat vereisen, bereikbare USB-hostpoort en voeding, trekontlasting, vrije ruimte rond jacks/moeren. Metalen paneelrand en hout mogen geen PCB of soldeerpennen raken. Houd de ESP32-antenne vrij volgens het bevestigde moduletype. Optionele speaker heeft eigen bevestiging/rooster en mag geen ongewenste mechanische resonantie of bedrading tegen de conus veroorzaken.

Eerst 1:1 papieren boormal en goedkoop proefpaneel maken; alle echte onderdelen plaatsen en bediening voelen. Daarna houten proefpassing, pas vervolgens definitieve gravure en afwerking. Geen Moog-logo als standaard productmarkering opnemen; gebruik eigen projectnaam, behoud functionele labels.

Mechanische bronnen VOORSTEL: FreeCAD-parametrisch project met benoemde parameters; exports STEP voor volume, DXF voor frezen en SVG/PDF voor labels/boormal. Andere CAD mag als bron volledig bewerkbaar en reproduceerbaar wordt meegeleverd. Placeholder-3D-modellen duidelijk als zodanig markeren.

## 13. Validatie en acceptatie

Alle getallen hieronder zijn **projectdoelen**, geen gemeten prestaties. Houd testopstelling, firmwarecommit, hardware-revisie, instellingen en resultaten bij.

| Fase | Werk | Exitcriterium |
|---|---|---|
| V0 — Inventaris | Foto's, markeringen, voorraad, componentdossiers, pinouts | Geen onbekende footprint gebruikt; BOM-02 geïdentificeerd of expliciet buiten ontwerp gehouden |
| V1 — Core/audio | ESP32, PCM5102A, sinus, I²S-decodering, rails/voeding | 48 kHz/slotformaat bewezen; geen clipping/DC-fout; reproduceerbare build/flash |
| V2 — USB-keyboard | Hostvoeding, enumeration, MIDI-parser, hotplug | Werkelijk gebruikerskeyboard speelt zonder PC; minimaal 20 connect/disconnectcycli zonder vastlopen; fout-VBUS getest |
| V3 — DSP | Drie oscillatoren, noise, filter/EG/mod/glide | Alle parameterpaden getest, geen NaN/Inf/instabiliteit bij volledige parameter- en notensweep |
| V4 — Bedieningscoupon | Eén sectie met echte encoders/switches, registerbus | Richting/detents juist; simultane draaiproef §8 slaagt; bootstanden en debounce kloppen |
| V5 — PCB/paneelcoupon | Dubbelzijdig frezen, registreren, via's, 1:1 passing | Continuïteit/isolatie en beide zijden soldeerbaar; encoder-/module-/paneelpassing bewezen |
| V6 — Volledige PCB | Alle secties, voeding, audio, USB, chassisbedrading | ERC/DRC-waivers beoordeeld; geen netfouten; alle functies bereikbaar en gedocumenteerd |
| V7 — Volledige audio | ADC-input, onafhankelijke phones, eventuele speaker | External door filter/VCA hoorbaar; main-mute laat phones intact; belasting en niveaus gemeten |
| V8 — Kast/duurtest | Proef- en eindkast, stressbelasting | Geen mechanische interferentie; stabiel na 60 min worst-case synth/USB/bediening, geen underruns of watchdog-reset |

Aanvullende meetcriteria:

- MIDI-ingang-tot-analoog-onset doel ≤10 ms; meet met gesynchroniseerde inputreferentie en audio, vermeld meetmethode en percentielen over minimaal 100 noten. Niet alleen softwaretijd meten.
- Audio-render worst-case doel <70% van bloktijd met volledige functies, inclusief gekozen oversampling. CPU-piek en buffer-underruns rapporteren.
- Digitale pitchfout doel <1 cent voor on-gemoduleerde testnoten MIDI 36…96; afwijkende LO- en aliasinggevallen apart. A440 doel ±0,1% op analoge meting, nauwkeurigheid klok/meetapparaat vermelden.
- Keytrackstanden 0, 1/3, 2/3, 1 aantonen met cutoff-/zelfoscillatiefrequenties. Filterzelfoscillatie blijft begrensd over instelbereik.
- Enveloptijd doel binnen ±5% of één audioblok, grootste marge geldt; meet volgens gedefinieerde 99%/1%-conventie. Note-off, sustain en legato afzonderlijk testen.
- Noteparser: overlappende noten, herhaalde note-on, velocity-zero, kanaalfilter, sustain, bend, panic, malformed packets en USB-verlies. Geen hangende noten.
- Uitgangsniveau/DC/ruis/THD+N meten en rapporteren; numerieke analoge limieten pas vastzetten na keuze uitgangscircuit en meetapparatuur. De chipdatasheet is geen prestatiebewijs voor de complete kast.
- Anti-aliasing aantonen met spectra over toonhoogte en modulatiediepte, inclusief hoge resonantie. Vergelijk bandlimited en naïeve testreferentie; “klinkt goed” alleen is onvoldoende.
- Vergelijk representatieve bass/lead/noise/percussion-patches met een vastgelegde Model D-referentie waar beschikbaar. Zonder referentie alleen functionele/subjectieve beoordeling rapporteren.

## 14. Open punten en ontwerpblokkades

| Open punt | Benodigde actie | Blokkeert |
|---|---|---|
| B0GMQ92458 onbekend | Producttitel/foto/markering verkrijgen | Alleen inzet van dit onderdeel; ander werk kan door |
| Exact ESP32-board/revisie | Boardfoto's, modulemarkering, pinout, geheugen/programeerproef | Definitief schema, pinplan, footprint |
| Exact USB-keyboard | Merk/model, class-compliance, connector, stroom en praktijktest | Compatibiliteitsclaim en hostvoedingfreeze |
| PCM5102A-module onbekend | Foto, schema/straps, voeding en meten | Definitieve DAC-aansluiting/footprint |
| EC11-afmetingen en puls/detentverhouding | Schuifmaat, continuïteits- en logic-analyzertest | Paneel/encoderfootprint/decoderconfig |
| Hoeveel encoders/schakelaars beschikbaar | Fysieke telling | Inkoop en volledig paneel |
| Switchtype/actuator | Meten en proefpaneel | Switchfootprint en paneeluitsparing |
| MAX98357-variant | Markering/format-test | Alleen optionele speaker |
| Scanneronderdelen nog te kiezen | MPN/package, 3,3V-timing, coupon | Volledige besturingsprint |
| Externe ADC en phones-gaintrap ontbreken | Selectie, benchtest, pin- en budgetcontrole | Volledige foto-functionaliteit |
| Desktopmodule of later eigen klavier | Gebruikerskeuze; nu desktop als voorstel | Definitieve kastmaat/klaviermechaniek |
| Display/waarde-indicatie | Proefbediening en plaatsingskeuze | Definitieve bruikbaarheid en paneelvorm |
| Paneelmaten/knoppen/materialen | Metingen, parametrisch ontwerp, proefpassing | Definitief CAD/freeswerk |
| Carvera-opstelling/tooling/coupon | Werkbereik, dubbelzijdige registratie, procesmeting | Alle machineklare freesbestanden |
| Uitgangsniveaus/connectoren/voeding | Schema en loadtests | Analoge acceptatielimieten en fabricagefreeze |

**Regel:** geen open punt stilzwijgend als opgelost behandelen. Softwaremocks en concept-CAD zijn toegestaan wanneer hun aannames zichtbaar zijn. Een schematische connector mag voorlopig functionele netnamen hebben; een fysiek te produceren footprint niet.

## 15. Werkopdracht voor Codex

1. Maak een repository met deze specificatie, besluitenlog en openpuntenregister. Behoud bron/aanname/status bij iedere keuze.
2. Start onafhankelijk voortgangsbaar werk: parameterregister, portable DSP-core, MIDI-state-machine, tests, hardwareabstractie en componentmeetformulieren.
3. Bouw zo vroeg mogelijk USB-host-MIDI en PCM5102A-audio samen op echte hardware. Bewijs keyboardverbinding en CPU-marge vóór uitgebreide PCB-routing.
4. Ontwerp de scan-/encoder-coupon en dubbelzijdige fabricagecoupon. Gebruik gemeten onderdelen om lokale KiCad-symbols/footprints te maken. Bewijs dat padnummers, gaten en aspositie overeenkomen.
5. Rond audio-ADC, phones-volume en hostvoeding af voor de volledige versie. Presenteer een werkend prototype niet als compleet zolang zichtbare functies ontbreken.
6. Maak schema en pinplan; voer ERC uit. Maak parametrisch mechanisch proefontwerp uit dezelfde coördinatenbron. Review de volledige stack-up vóór routing.
7. Routeer sectieprinten voor bewezen Carvera-proces; voeg handmatige via's, assemblagevolgorde en testpunten toe. Voer DRC en fysieke couponcontrole uit.
8. Lever revisiegebonden productie-export pas na de relevante gates. Houd bronbestanden bewerkbaar en alle dependencies/versies vastgelegd.
9. Documenteer build/flash, bedrading, bring-up, meetresultaten, bekende beperkingen en gebruik. Wijzig geen eisen op eigen initiatief om een prototype “af” te verklaren.

### Definitie van gereed

De volledige versie speelt vanaf het USB-MIDI-keyboard zonder computer; alle verplichte paneelfuncties werken, inclusief echte externe input en onafhankelijke phones; de mechaniek past met echte onderdelen; de tweezijdige print is lokaal reproduceerbaar gemaakt en getest; alle bronbestanden en montage-/meetgegevens zijn beschikbaar. Een open hardwarekeuze wordt als open afgeleverd, niet met verzonnen maat of footprint dichtgeschreven.

## 16. Bronnen en bewijskracht

Controle uitgevoerd op 26 oktober 2026. Online pagina's en indexen kunnen veranderen. Download bij implementatie de gebruikte fabrikantdocumentatie en leg revisie vast.

- **Gebruikersbewijs:** deze sessie en [referentiegesprek](chatgpt-conversation://6adfcacd-4b50-83eb-a71a-aae70fe39633): kale encoders zonder printje; PCM5102A besteld; aangeleverde ASINs en paneelfoto. Laatste bevestiging: USB-MIDI-keyboard. De foto vormt de basis van de eigen paneelinventaris.
- **Model D-functies:** [Moog officiële downloads](https://www.moogmusic.com/downloads/) en geïndexeerde [Model D-handleiding 2018](https://api.moogmusic.com/sites/default/files/2018-01/Minimoog_Model_D_Manual.pdf). De rechtstreekse oude PDF-link gaf tijdens de controle 404; geïndexeerde passages waren beschikbaar. Gebruik passages over waveformsets, keytracking en bronselectie als referentie, maar haal vóór authenticiteitsclaims een volledig bereikbare handleiding voor de gekozen uitvoering op. De overige numerieke DSP-contracten zijn projectvoorstellen.
- **Processor/module:** [Espressif ESP32-S3 DevKit-documentatie](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp-dev-kits-en-master-esp32s3.pdf) en [USB Host API](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/usb_host.html?highlight=usb+serial). Officieel board is referentie, geen bewijs van clone-afmetingen.
- **Audio-DAC:** [TI PCM5102A datasheet](https://www.ti.com/lit/ds/symlink/pcm5102a.pdf).
- **Speaker:** [Analog Devices MAX98357A productinformatie/datasheet](https://www.analog.com/en/products/max98357a.html).
- **Multiplexers:** [TI CD74HC4067](https://www.ti.com/product/CD74HC4067) en [TI TCA9548A](https://www.ti.com/product/TCA9548A).

De niet-primaire zoekresultaten achter de catalogusaanwijzingen in §3 zijn uitsluitend identificatieleads: [ESP32-ASIN](https://www.a.ubuy.com.kw/en/productde/JSHN1LLQ6-arceli-3pcs-esp32-s3-wroom-1-n16r8-esp32-s3-devkitc-1-development-boards-with-wifi-bluetooth-5-0-for-arduino), [CD74HC4067-ASIN](https://www.odkarla.cz/icquanzx-5ks-16ch-analogovy-digitalni-multiplexer-breakout-board-modul-cd74hc4067-cmos-presny-mod~p1419717), [TCA9548A-ASIN](https://www.ubuy.mq/en/productuk/9IIA4Z64-youmile-5pack-expansion-board-tca9548a-i2c-iic-multiplexer-breakout-board-8-channel-expansion-board-), [switch-ASIN](https://brunei.desertcart.com/products/434820302), [MAX98357-ASIN](https://www.merchantwords.com/asin/uk/B0CJY1C287), [EC11-ASIN](https://www.desertcart.ae/products/444491956-runcci-yun-10pcs-ec11-rotary-encoder-360-degree-rotary-encoder). Hun commerciële technische claims zijn niet gebruikt als elektrische of mechanische ontwerpspecificatie.
