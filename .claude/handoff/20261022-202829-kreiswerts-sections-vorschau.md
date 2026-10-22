[Claude] [Applied Research] KreiswertS: übrige Sections per Vorschau
Rückmeldung an: dev-ws-b3
Kontext: Section „Projekt“ der KreiswertS-Karte ist neu gestaltet
  und gepusht (890434b, Repo __project_applied_research): volle
  Kopfleiste je Kachel-Thema mit Icon-Chip (Petrol/Indigo/Blau/
  Violett; Variablen --c-ph, --c-out, --c-tst, --c-per, --bar-ink,
  --bar-mix in kreiswerts.css), Status-Legende ✓ fertig · ◐ in
  Arbeit · ○ offen im Kopf der Section (stChip in app.js), Icons
  per ICO/ico() in app.js und data-ic im HTML.
  Vorbild: Schatzkammer applied_research/vorschauen/
  2026-10-22-kreiswerts-redesign-der-kacheln-in-der-section-projekt
Aufgabe: Für die übrigen Sections (start, prinzip, plattform,
  szenarien, einordnung) per Skill preview je Section Varianten im
  selben Stil zeigen (Kopfleisten, Legende wo Status vorkommt,
  Icons); User wählt in der Vorschau, danach umsetzen, prüfen,
  committen + pushen.
Dateien:
  - projekt-a-materialfluss/karte/index.html
  - projekt-a-materialfluss/karte/app.js
  - projekt-a-materialfluss/karte/kreiswerts.css
  - projekt-a-materialfluss/karte/daten.js
Beachten:
  - Haupt-Chat auf Opus (User 2026-10-22: „OPUS!“), nicht Sonnet
  - erst Vorschau, dann Code; Varianten-Keys Bereich:A
    (z. B. Plattform:A, Einordnung:B)
  - Tests auf eigenem Port (nicht 8096): hell/dunkel 1280 + 360,
    Selbsttest 6/6, keine Konsolenfehler, reduced motion
  - Karte (MapLibre) nur ohne captureBeyondViewport aufnehmen,
    fertig bei .geo-map[data-ready]
  - UI-Regeln: kein einseitiger Rand ab 2 px, keine graue Schrift,
    Radius ≤ 8 px, Statusfarben nur grün/orange/rot
