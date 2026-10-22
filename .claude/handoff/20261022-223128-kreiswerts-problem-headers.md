[Claude] [KreiswertS] Problem-Leiste zentrieren + Section-Header neu
übernommen von dev-ws-83 am 2026-10-22 22:39
Rückmeldung an: [Claude] dev-ws-bc
Kontext: KreiswertS-Prototyp (~/__project_applied_research, Stand 2acaf87),
  Seite http://localhost:8096/projekt-a-materialfluss/karte/.
  Kachel „Problem“ (index.html ab Z. 66, Texte pb1–pb3 + Lösung in app.js Z. 28):
  drei Punkte mit kleinem Icon links neben dem Text, rechts die Lösungs-Kachel
  „KreiswertS macht Angebote, Bedarfe und Wege in der Region sichtbar.“ – alles linksbündig.
  Section-Header aller Abschnitte = `.head` mit Kicker-Nummer, h2 und Lead
  (index.html Z. 64, 87, 116, 125, 145; Stil in kreiswerts.css).
Aufgabe (Feedback des Users, wörtlich):
  1) „besser anordnen (icons größer und arbeite mal endlich mehr mit CENTER!)“ –
     Problem-Leiste: Icons deutlich größer, Icon über dem Text, Punkte zentriert
     (Text zentriert, gleiche Spaltenbreiten), Lösungs-Kachel passend dazu.
  2) „die section headers überarbeiten -> redesign (dezenter und nicht so langweilig)“ –
     neues Header-Design für alle Sections: dezenter, aber mit Charakter
     (z. B. zentrierter Kicker + Titel, feine Linie/Akzent, Nummer als Teil des Designs).
Dateien:
  - projekt-a-materialfluss/karte/kreiswerts.css
  - projekt-a-materialfluss/karte/index.html
  - projekt-a-materialfluss/karte/app.js (nur falls Markup/Texte nötig)
Beachten:
  - Header-Redesign = größerer Umbau → erst Vorschau mit 2–3 Varianten (Skill preview,
    Zentrierung als Leitidee), dann umsetzen; Problem-Leiste = kleine Änderung, direkt.
  - UI-Grundregeln RULES.md §3: Zero Overlap, keine graue Schrift, keine Mini-Schrift,
    kein einseitiger Akzent-Rand ≥ 2 px, kleine Kacheln zentriert.
  - DoD laut AGENTS.md des Projekts: Headless Chrome hell + dunkel, 1280 + 360 px,
    keine Konsolenfehler, Selbsttest 6/6.
  - Offener Zettel kreiswerts-prinzip-animation (andere Aufgabe, gleiche Dateien
    app.js/kreiswerts.css) → vor dem Ändern ListAgents + git status, ggf. abstimmen.
  - Bild des Users (Ausschnitt der Problem-Leiste) liegt nur im Chat dev-ws-bc vor;
    Beschreibung oben genügt.
