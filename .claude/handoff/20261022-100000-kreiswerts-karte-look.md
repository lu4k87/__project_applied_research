[Claude] [Applied Research] KreiswertS: Vorschau Karte mehr wie eine Karte
übernommen von dev-ws-1e am 2026-10-22 10:40
Rückmeldung an: dev-ws-b8
Kontext: KreiswertS = Plattform-Prototyp Kunststoff-Austausch
  Kamp-Lintfort, Seite projekt-a-materialfluss/karte/ im Repo
  ~/__project_applied_research (Stand a08ea42). Die Karte ist ein
  selbst gezeichnetes SVG: drawMap() in karte/app.js zeichnet aus
  daten.js (region: towns, water=Rhein, roads A57/A42/A40, box) nur
  Ortskreise, Rhein-Band, Straßenlinien, Firmen-Symbole (◇ ○ △),
  Routen. Wird an 3 Stellen genutzt: Lagebild (#mapStart),
  Plattform (#mapPlat, klickbar), Szenarien (#mapScn, zoomt).
  Schrift/Symbole in festen Bildschirm-Pixeln (k = SVG-Einheiten je
  px). Look: hell Petrol, dunkel Nachtblau/Gold (Umschalter).
  User 2026-10-22: „die Karte sollte mehr nach Karte/Map aussehen
  → mach Vorschau“.
Aufgabe: Vorschau mit 3 klar verschiedenen Karten-Looks (Skill
  preview + variation), z. B. A schematische Stadtkarte mit
  Siedlungsflächen, Wald/Feld, Nebenstraßen, Bahn, Maßstab +
  Nordpfeil; B topografisch/ruhig mit Geländetönung und
  Gewässernetz; C Vektor-Kacheln wie OSM (nur, wenn ohne fremden
  Kartendienst/Tracking machbar). Je Variante Einzeländerungen mit
  eigenem Bild, hell + dunkel, 1280 + 360 px. Nach Wahl des Users
  umsetzen, Selbsttest der Seite muss 6/6 bleiben.
Dateien:
  - projekt-a-materialfluss/karte/app.js (drawMap)
  - projekt-a-materialfluss/karte/daten.js (region)
  - projekt-a-materialfluss/karte/kreiswerts.css (.m-*)
Beachten:
  - Geometrie bleibt schematisch und ehrlich gekennzeichnet; keine
    echten Firmen, keine Karten-Abrufe bei Dritten ohne Rückfrage
  - Lesbarkeit der Routen + Firmenlogos/Symbole geht vor Deko
  - Prüfung laut AGENTS.md des Projekts (Headless, hell/dunkel,
    1280/360, reduced motion); Server eigener Port, nicht 8096
