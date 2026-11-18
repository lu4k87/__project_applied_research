[Claude] [Präsentation] Volle Breite + Vorschau mit Bausteinen
übernommen von dev-ws-52 am 2026-11-18 10:49
Rückmeldung an: dev-ws-71
Kontext: Präsentation/ im Repo __project_applied_research
  (index.html, style.css, script.js; Stand 09707c2).
  Erklärseite App-Architektur (Next.js, Better Auth, PostgreSQL,
  BullMQ) mit Wege-Umschalter, Verbindungslinien, DE/EN, Hell/Dunkel.
  .page ist auf max-width 1360px begrenzt.
  Server läuft: http://localhost:8096/Pr%C3%A4sentation/index.html
Aufgabe:
  - Seite übersichtlicher und breiter: gesamte Bildschirmbreite nutzen
  - erst Vorschau (Skill preview): Varianten je Komponente
    (z. B. Kopf + Stack-Leiste, Diagramm-Ebenen, Verbindungen,
    Glossar-Karten), die der User einzeln zusammenklicken kann
    (Auswahl je Bereich, Keys wie Layout:A, Glossar:B)
  - nach Auswahl umsetzen, prüfen (hell + dunkel, 1280/1920/360 px,
    keine Konsolenfehler, keine Überlappung), committen + pushen
Dateien:
  - Präsentation/index.html
  - Präsentation/style.css
  - Präsentation/script.js
Beachten:
  - DE/EN-Übersetzung läuft über Wörterbuch EN in script.js
    (Textknoten-Schlüssel) → neue Texte dort eintragen
  - Verbindungslinien (draw() in script.js) messen Boxen; nach
    Layout-Änderung prüfen, dass sie passen
  - Vorschauen in die Schatzkammer applied_research, Links über 8085
