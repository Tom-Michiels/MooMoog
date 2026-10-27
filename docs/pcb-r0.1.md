# PCB R0.1 — ontwerp en assemblagecontract

## Wat er ligt

SCAN8 is een tweelaagse contactscanner met een SN74HC165N in PDIP-16, elf 10k-weerstanden, één 100nF- en één 1µF-keramische condensator. J1/J2 zijn **soldeerdraadinterfaces**, geen als passend verklaarde stekkerheaders. De print meet 91,44 × 58,42 mm. Coördinaten zijn KiCad-frontaanzicht, oorsprong linksboven in het document, +X rechts en +Y omlaag; de printcontour begint op (5,08; 5,08) mm.

De IC-pinout is gecontroleerd tegen TI SCLS116H. De geometrie is een ontwerpvoorstel: PDIP 7,62 mm rijafstand / 2,54 mm steek, weerstand 7,62 mm steek, condensator 2,54 mm steek. Controleer gekozen componenten vóór bestelling en couponfabricage. De eigen footprints bevatten een grove F.Fab-zone; dat is geen exact bodymodel of EC11-footprint. Geen IC-socket is meegemodelleerd.

## Aansluitingen

J1: 1 = +3V3; 2 = GND; 3 = LOAD_N; 4 = CLK; 5 = DATA; 6 = SER. J1 is uitsluitend een interne laagspanningsinterface. De GPIO-nummers aan de ESP32-zijde blijven OPEN. Verbind geen 5 V met deze contacten. Gebruik één bewezen, begrensde 3,3V-testvoeding; vermijd een tweede parallelle voeding via de ontwikkelprint.

J2: pinnen 1…8 = IN0…IN7; pin 9 = GND. Alle contacten schakelen naar GND. Voorgestelde couponmapping:

| J2-pin | Logisch contact | IC-ingang/pin |
|---|---|---|
| 1 | Encoder 1 A | A / 11 |
| 2 | Encoder 1 B | B / 12 |
| 3 | Encoder 2 A | C / 13 |
| 4 | Encoder 2 B | D / 14 |
| 5 | Encoder 1 druk | E / 3 |
| 6 | Encoder 2 druk | F / 4 |
| 7 | Schakelaar 1 | G / 5 |
| 8 | Schakelaar 2 | H / 6 |
| 9 | Contact-common | GND / 8 |

Dit zijn **geen fysieke EC11-pinnummers**. Meet common/A/B en de geïsoleerde drukschakelaar eerst met continuïteit. Metalen ankers zijn niet automatisch massa. Gebruik van een SPDT: common naar GND, één worp naar ingang; andere worp vrij. Werkelijke contactvolgorde meten.

U1 pin 15 (clock inhibit) is laag; pin 7 (complementaire uitgang) is bewust niet aangesloten. R9 houdt LOAD_N hoog, R10 CLK laag en R11 SER laag. SER blijft op een losstaande coupon via R11 gedefinieerd; in een keten komt SER van de QH-uitgang van de volgende scanner.

Capture: CLK laag houden, LOAD_N laag pulsen, vervolgens hoog. Lees **H eerst vóór de eerste stijgende klokflank**, dan G…A na opeenvolgende stijgende flanken. Daarmee is de uitleesvolgorde IN7…IN0. Timing bij 3,3 V moet op de echte keten worden gemeten; 1 MHz en 1 kHz capture zijn startvoorstellen. Neem de 2V-datasheetgrenzen conservatief als startpunt en verifieer met logic analyzer. Firmware/SPI-mode is nog niet geïmplementeerd of bewezen.

## CNC en assemblage

Spoorbreedte 0,4 mm en clearance 0,4 mm zijn couponvoorstellen. Componentpaden landen op B.Cu; laagwissels gebruiken losse, toegankelijke draad-via's. KiCad tekent deze als through-vias, maar een Carvera maakt geen geleidende gatwand: **iedere via in `wire-vias.csv` vereist een draad aan beide zijden gesoldeerd**.

De huidige layout bevat 36 draad-via's. Dat is veel voor acht ingangen; deze eerste versie dient voor elektrisch en procesonderzoek. Vermindering van via's en kortere retourpaden zijn een vervolgstap vóór de paneelprinten. Deze layout is geen geoptimaliseerd productieontwerp. Decoupling/kloksignaalkwaliteit en scanbetrouwbaarheid zijn nog niet fysiek getest.

1. Verifieer componentmaten, bitvolgorde en pinout op papier/breadboard.
2. Bewijs eerst de Carvera-registratie op een afzonderlijke procescoupon. De huidige scanprint heeft nog geen gevalideerde fixture of registratiegaten.
3. Pas CAM, flip-as en gerelateerde gaten pas toe nadat tooling, werkbereik en plaatdikte bekend zijn.
4. Controleer isolatie en gatposities; soldeer alle draad-via's vóór de IC en draadbundels. Controleer elke via van topkoper naar bottomkoper.
5. Monteer passieven. Meet weerstand +3V3–GND en controleer ieder pad tegen `connectivity.json`.
6. Breng begrensde 3,3 V aan, controleer voedingspinnen en idle-netten. Monteer U1 alleen spanningsloos.
7. Controleer elk individueel contact, simultane encodertransities en bounce; noteer de echte detentrelatie.
8. Stressproef: twee encoders ieder 30 detents/s gedurende 60 s. Resultaat is nog OPEN.

C1/C2 zijn elektrisch parallel aan de voeding. Er zijn geen grote RC-filters op encoderfasen: debounce en Gray-decoding worden later in de firmware uitgevoerd.

## Volledige printopdeling

Het voorstel reserveert vijf mechanisch onafhankelijke secties:

| Sectie | Encoders incl. druk | Schakelaars | Bits nodig | Registers × 8 |
|---|---:|---:|---:|---:|
| Controllers + LFO | 4 | 6 | 18 | 3 |
| Oscillator Bank | 8 | 1 | 25 | 4 |
| Mixer | 5 | 6 | 21 | 3 |
| Modifiers | 9 | 3 | 30 | 4 |
| Output | 2 | 2 | 8 | 1 |
| Totaal | 28 | 18 | 102 | 15 |

120 bits in plaats van het 112-bit rekenvoorbeeld in de specificatie: afronden per sectie houdt aansluitingen binnen de eigen print. Dit is een **VOORSTEL**, geen wijziging aan het aantal bedieningen. 120 bits bij 1 MHz kost theoretisch 120 µs exclusief capture/overhead. De definitieve keten, kabels en klokbuffering zijn nog te valideren.

Het systeemschema bevat alleen functionele blokken, geen uitgewerkte USB-voeding of audioversterker. Zijn terminalnummers zijn geen pinout van de Amazon-modules. De onafhankelijke main/phones-regeling blijft expliciet in scope; de gedeelde DAC-uitgang vraagt nog echte regelbare gaintrappen. COMMON_AUDIO staat voor twee gescheiden L/R-kanalen, nooit kortsluiten.
