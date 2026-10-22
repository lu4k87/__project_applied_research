[Claude] [Applied Research] KreiswertS: echte Karte mit Zoom Deutschland → Land → Kreis → Gemeinde
Rückmeldung an: dev-ws-1e
Kontext: KreiswertS-Prototyp in projekt-a-materialfluss/karte/ (Stand
  bc3ef06). Karte heute = selbst gezeichnetes SVG (drawMap in app.js,
  region + region.decor in daten.js), Look „Karte:C“ (App-Karte:
  Orte grau mit Straßenraster, Wald grün, helle Straßen mit Rand,
  Maßstab, Hinweis „schematisch · KreiswertS“), gewählt in Vorschau
  __treasury__allprojects/applied_research/vorschauen/
  2026-10-22-kreiswerts-karte-mehr-wie-eine-karte. Genutzt an 3 Stellen:
  Lagebild #mapStart, Plattform #mapPlat (klickbar), Szenarien #mapScn.
  User 2026-10-22: „verwende die echte Karte von Kamp-Lintfort und
  Umgebung, Zoom bis ganz Deutschland, Bundesländer-Linien, weiter
  interaktiv; Klick auf Land → Kreis → Gemeinde wie bei Google Maps“.
Entschieden (User 2026-10-22):
  - Profi-Weg: MapLibre GL JS + selbst gehostete OSM-Vektorkacheln
    (PMTiles: Deutschland grob, Region Kamp-Lintfort detailliert) +
    amtliche Grenzen BKG VG250 (Länder, Kreise, Gemeinden, vereinfacht)
    als eigene Klick-/Hover-Ebene; keine Laufzeit-Abrufe bei Dritten
  - Ebenen: Land → Kreis → Gemeinde, „Zurück“ je eine Ebene hinaus;
    bei Kamp-Lintfort Firmen-Symbole + Routen wie heute
  - Look bleibt Karte:C (Farben aus kreiswerts.css, hell + dunkel)
Aufgabe: 1) kleine Vorschau (Skill preview, 1–2 Bilder je Ebene:
  Deutschland → NRW → Kreis Wesel → Kamp-Lintfort) mit offenen Fragen
  (z. B. Datei-Größe, Ladeweise je Land) 2) nach Abnahme einbauen,
  Firmen/Routen/Matching/Selbsttest unverändert lauffähig (6/6).
Dateien:
  - projekt-a-materialfluss/karte/app.js (drawMap, renderStart/Plat/Scn)
  - projekt-a-materialfluss/karte/daten.js (region)
  - projekt-a-materialfluss/karte/kreiswerts.css (.m-*)
  - neu: Kartendaten (PMTiles/GeoJSON) + MapLibre lokal (kein CDN)
Beachten:
  - Quellenangabe Pflicht: „© OpenStreetMap-Mitwirkende · © GeoBasis-DE / BKG“
  - Lizenzen: OSM ODbL, VG250 dl-de/by-2.0; Datenmenge im Git klein
    halten (grob/vereinfacht, ggf. Git LFS erst nach Rückfrage)
  - Firmen bleiben fiktiv und gekennzeichnet (AGENTS.md §0)
  - Prüfung laut AGENTS.md des Projekts (Headless, hell/dunkel,
    1280/360, reduced motion, Selbsttest 6/6); eigener Port, nicht 8096
