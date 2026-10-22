[Claude] [Applied Research] KreiswertS: Scroll-Zoom, Logos, Hover
Rückmeldung an: dev-ws-e8
Kontext: Echte Grundkarte ist eingebaut (Commits 1c4a8fb, d667c33):
  karte/grundkarte.js = MapLibre + PMTiles, Plattform-Karte mit Ebenen
  Deutschland → Land → Kreis → Gemeinde; app.js drawMap zeichnet Wege +
  Firmen als SVG-Lage über der Karte (Projektion KW_GEO[id].project,
  Neuzeichnen bei jeder Kamerabewegung). Wünsche des Users 2026-10-22:
Aufgabe:
  1) Plattform-Karte: Zoom per Mausrad ohne Strg, solange der Zeiger auf
     der Karte ist → grundkarte.js `cooperativeGestures: levels` weg,
     Texte geoCoop* in app.js (I18N de/en) dann löschen
  2) Firmen bekommen LOGOS statt Rolle-Symbol: daten.js firms[].logo
     {c, d} (24er-Pfad, wie logo() in app.js); Rolle als kleines Abzeichen
     am Logo (Vorbild renderVs: vs-badge + shape(role)); Klassen sel/hl/
     dim, Fokus-Halo, tabindex und `.m-firm` (Selbsttest) bleiben
  3) Firmennamen als dezentes Badge: Hintergrund hinter .m-flabel
     (surface, feine line-2-Kante, Radius ≤ 6 px), hell + dunkel
  4) Hover auf andere Fläche auch bei Auswahl sichtbar: in levelLayers
     (grundkarte.js) gewinnt `dim` vor `hover` → abgeblendete Nachbarn
     zeigen keinen Hover; Hover zuerst prüfen + Umriss-Linie für die
     Fläche unter dem Zeiger
Dateien:
  - projekt-a-materialfluss/karte/grundkarte.js
  - projekt-a-materialfluss/karte/app.js (drawMap, I18N)
  - projekt-a-materialfluss/karte/kreiswerts.css (.m-firm, .m-flabel)
Beachten:
  - Firmen bleiben fiktiv und gekennzeichnet (AGENTS.md §0)
  - Prüfung laut AGENTS.md des Projekts: eigener Port (nicht 8096),
    Headless hell/dunkel 1280/360, Selbsttest 6/6, reduced motion;
    Karten-Aufnahmen siehe AGENTS.md §5 „Karten-Aufnahmen“
  - Hover-Text unter der Karte hat eigene Zeile (Fix gegen Springen),
    Leiste nicht wieder umbauen
  - Wünsche sind konkret → direkt umsetzen, Bildbogen nachher
