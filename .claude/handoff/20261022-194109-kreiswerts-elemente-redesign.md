[Claude] [Applied Research] KreiswertS: Untersections + Elemente redesignen
Rückmeldung an: dev-ws-2e
Kontext: Die Anordnung der 6 Hauptsections ist entschieden und umgesetzt
  (Commits 82b9a44, dcc9e63; TODO A1 erledigt): Start:B (Banner +
  Lagebild volle Breite), Prinzip:A (Problem-Leiste, Kreislauf links,
  Heute/Mit KreiswertS rechts gestapelt), Plattform bleibt wie sie ist,
  Szenarien:A (Schritte ohne Rahmen, Karte 2/3), Projekt:C (Phasen oben,
  Selbsttest 3×2, Zielgruppen 2×2), Einordnung:C (Lücke + Grenzen in
  einer Kachel, Leitfaden 4 + 3). Vorschau dazu:
  __treasury__allprojects/applied_research/vorschauen/
  2026-10-22-kreiswerts-hauptsections-sinnvoller-anordnen/
Aufgabe: Wunsch des Users 2026-10-22: „Redesign der einzelnen
  Untersections und deren Elemente“ – Gestaltung der Kacheln und ihrer
  Bausteine in allen Sections (z. B. Kennzahl-Kacheln, Problem-Leiste,
  Heute/Netz-Diagramme, Plattform-Panel + Listen, Szenario-Schritte +
  Plausibilitäts-Check, Phasen, Soll/Ist-Tabelle, Badges, Selbsttest,
  Personas, State-of-the-Art-Tabelle, Leitfaden).
  Größerer Umbau → erst Vorschau (Skill preview, vorher variation),
  je Bereich eine options-Section mit 3 Varianten (Keys Bereich:A),
  Vorher/Nachher-Ausschnitte; nach der Wahl umsetzen
Dateien:
  - projekt-a-materialfluss/karte/kreiswerts.css (Tokens + Bausteine)
  - projekt-a-materialfluss/karte/index.html
  - projekt-a-materialfluss/karte/app.js (Render-Vorlagen, I18N de/en)
Beachten:
  - Anordnung der Sections nicht wieder umbauen (gerade entschieden)
  - UI-Grundregeln: kein einseitiger Akzent-Rand ab 2 px, keine graue
    Schrift, keine Mini-Schrift, Farbe nur für Abweichung, Radius ≤ 8 px
  - Firmen bleiben fiktiv und gekennzeichnet (AGENTS.md §0)
  - Prüfung laut AGENTS.md des Projekts: eigener Port (nicht 8096),
    Headless hell/dunkel 1280/360, Selbsttest 6/6, reduced motion;
    Karten-Aufnahmen siehe AGENTS.md §5 „Karten-Aufnahmen“
  - Klassen, die der Selbsttest nutzt (.m-firm, #tests …), bleiben
