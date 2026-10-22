[Claude] [KreiswertS] Section Prinzip animieren + Farben prüfen
Rückmeldung an: dev-ws-27
Kontext: KreiswertS-Prototyp (~/__project_applied_research, Stand 069e296),
  Section „Prinzip“ (#prinzip, index.html Z. 63-83) hat 3 Kacheln:
  „Kreislauf der drei Rollen“ (SVG #cycle, app.js ab Z. 441),
  „Heute: Einbahnstraße“ (#vsToday) und „Mit KreiswertS: Kreislauf“ (#vsNet).
  Alles statisch; Pfeile/Kreise nur gelb bzw. orange (Entsorgung).
  Screenshot des Users: /tmp/claude-1000/-home-mk-dev-ws/49a76799-9b21-4dc1-8f5c-026fbff3dbcd/images/1.png
Aufgabe: Animation für die 3 Kacheln einbauen und abstimmen
  (z. B. Material fließt entlang der Pfeile, Kreislauf läuft sichtbar um,
  Heute vs. Kreislauf als Kontrast). Mehr Farben für Pfeile oder Kreise
  nur, wenn sie eine Bedeutung tragen (z. B. je Rolle die Farbe der
  Rollen-Legende) – sonst bei den jetzigen Farben bleiben.
Dateien:
  - projekt-a-materialfluss/karte/app.js (Zeichnen #cycle, #vsToday, #vsNet)
  - projekt-a-materialfluss/karte/kreiswerts.css
  - projekt-a-materialfluss/karte/index.html (nur falls nötig)
Beachten:
  - Skills soft-motion (Dauern, Kurven), motion-diagrams (Pakete auf Pfaden)
  - UI-Grundregeln RULES.md §3: Farbe nur mit Bedeutung, nie Farbe allein;
    Erweiterung → erst Vorschau (Skill preview), wenn Varianten nötig
  - prefers-reduced-motion: keine bewegten Punkte, Endzustand statisch
  - DoD laut AGENTS.md §5: Headless Chrome hell + dunkel, 1280 + 360 px,
    keine Konsolenfehler, Selbsttest 6/6
  - Server läuft schon: http://localhost:8096/projekt-a-materialfluss/karte/
