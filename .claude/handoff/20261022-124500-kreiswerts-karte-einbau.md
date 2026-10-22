[Claude] [Applied Research] KreiswertS: echte Karte einbauen (MapLibre, Ebenen Land → Kreis → Gemeinde)
übernommen von dev-ws-e8 am 2026-10-22 13:18
Rückmeldung an: dev-ws-ea
Kontext: Vorschau abgenommen (User 2026-10-22), Prototyp läuft:
  Schatzkammer __treasury__allprojects/applied_research/vorschauen/
  2026-10-22-kreiswerts-echte-karte-mit-zoom-deutschland-land-kreis-gemei/
  (index.html = Vorschau, prototyp/ = Code geo.js/geo.css/index.html +
  README.md mit allen Befehlen zum Erzeugen der Daten). Heute zeichnet
  drawMap in app.js ein schematisches SVG (Look Karte:C) an 3 Stellen:
  #mapStart, #mapPlat (klickbar), #mapScn.
Entschieden (User 2026-10-22):
  - F1 Navigation: Nav:A Pfadleiste + Nav:B Zurück-Knopf mit Ebenen-Titel
    (beides zusammen, oben links auf der Karte); Esc = eine Ebene hinaus
  - F2 Datenmenge „groß“: Deutschland bis Zoom 8 (≈ 25 MB), Region bis
    Zoom 14 (≈ 11 MB); kein Git LFS (beide Dateien < 50 MB)
  - F3 Gemeinde-Grenzen je Land nachladen (Länder + Kreise sofort, 0,8 MB)
  - F4 Detailgebiet = Rechteck um Kamp-Lintfort (6.33,51.40 – 6.78,51.62)
  - F5 Ebenen-Zoom nur in der Plattform (#mapPlat); Lagebild + Szenarien
    bekommen die echte Grundkarte, fest auf der Region
Aufgabe: einbauen in projekt-a-materialfluss/karte/:
  1) Daten erzeugen (README im prototyp/), ablegen z. B. karte/geo/
     (de.pmtiles, region.pmtiles, grenzen/, fonts/) + MapLibre/pmtiles lokal
     unter karte/vendor/ (Lizenztexte mitnehmen)
  2) MapLibre-Grundkarte hinter der bestehenden SVG-Ebene; Projektion von
     drawMap (proj/pt) auf map.project umstellen, bei move neu zeichnen →
     Firmen-Symbole, Routen, animierte Punkte, Tastatur, Selbsttest bleiben
  3) Region-Datei erst beim Hineinzoomen laden; ganze Datei per fetch +
     FileSource (python http.server kann keine Byte-Bereiche)
  4) Hell/Dunkel: Stil aus den CSS-Tokens neu bauen bei Theme-Wechsel
     (Knopf #themeBtn + prefers-color-scheme)
  5) DE/EN: Texte der Pfadleiste/Hinweise in die T()-Tabellen von app.js
  6) gewählte Nav als UI-Baustein ins Repertoire (Skill preview „Repertoire“)
Dateien: karte/app.js (drawMap, renderStart/Plat/Scn), karte/index.html,
  karte/kreiswerts.css (.m-*), neu karte/geo/, karte/vendor/
Beachten:
  - Quellenangabe Pflicht: „© OpenStreetMap-Mitwirkende · © GeoBasis-DE / BKG (2026)“;
    Lizenzen OSM ODbL, VG250 dl-de/by-2.0
  - Aufnahmen: capture.py zeigt bei WebGL nur ein Eckstück
    (captureBeyondViewport) → prototyp/shoot.py-Verfahren oder
    preserveDrawingBuffer nur im Aufnahme-Modus
  - Firmen bleiben fiktiv und gekennzeichnet (AGENTS.md §0)
  - Prüfung laut AGENTS.md des Projekts (Headless, hell/dunkel, 1280/360,
    reduced motion, Selbsttest 6/6); eigener Port, nicht 8096
