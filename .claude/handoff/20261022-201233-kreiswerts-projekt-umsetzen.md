[Claude] [Applied Research] KreiswertS: Section Projekt umsetzen
übernommen von dev-ws-f2 am 2026-10-22 20:13
Rückmeldung an: dev-ws-99
Kontext: Vorschau „Redesign der Kacheln in der Section Projekt“
  entschieden 2026-10-22 (Schatzkammer applied_research/vorschauen/
  2026-10-22-kreiswerts-redesign-der-kacheln-in-der-section-projekt).
  Varianten-Code (CSS + Render-JS, als Overlay erprobt) liegt dort in
  umsetzung/v.css + umsetzung/v.js – Klassen vA-/vB-/vC- je Variante.
Entscheidungen:
  - Farbe:A+C: volle Kopfleiste je Kachel-Thema (Phasen/Ziele Petrol,
    Erfolg/Ergebnisse Indigo, Selbsttest Blau, Zielgruppen Violett)
    mit Icon-Chip; Section-Überschrift + Tabellenköpfe Petrol
  - Phasen:C: Tabelle Phase × Aufgabe / Ergebnis / Offen; Ergebnis und
    Offen getrennt (Daten in v.js PH → nach daten.js, de + en)
  - Abgabe:B: Fortschrittsring „2/4 fertig“ neben der Liste
  - Test:A: Kopfband mit Titel, Erklärung, „6/6 bestanden“ + Zeit,
    3×2 Karten mit Icon, Knöpfe unten
  - Person:A+B+C mischen: Kopf wie A (Kürzel, Name, Rolle, Gruppe
    mit Icon), Zitat groß wie C, Ziel → Hürde → Lösung als Ablauf
    wie B, gefüllter Knopf wie C
  - Legende ja: Status ✓ fertig · ◐ in Arbeit · ○ offen einmal im
    Kopf der Section; alte Wörter (sichtbar, da, teilweise, Entwurf)
    überall durch diese drei ersetzen (I18N de + en)
Aufgabe: Entscheidungen fest in kreiswerts.css, app.js, daten.js,
  index.html einbauen (Render-Vorlagen in app.js statt Overlay),
  responsiv bis 360 px (Phasen-Tabelle ≤ 1099 px als Karten je Phase,
  Ablauf B gestapelt), hell + dunkel
Dateien:
  - projekt-a-materialfluss/karte/kreiswerts.css
  - projekt-a-materialfluss/karte/app.js
  - projekt-a-materialfluss/karte/daten.js
  - projekt-a-materialfluss/karte/index.html
Beachten:
  - Selbsttest nutzt #tests, #testRun, #testSave, #testStamp → bleiben
  - UI-Regeln: kein einseitiger Rand ab 2 px, keine graue Schrift,
    Radius ≤ 8 px, Farbe für Status nur grün/orange/rot
  - Prüfung laut AGENTS.md: eigener Port (nicht 8096), hell/dunkel
    1280 + 360, Selbsttest 6/6, reduced motion, keine Konsolenfehler
  - danach übrige Sections im selben Stil per Vorschau anbieten
  - Zettel kreiswerts-elemente-redesign mit der Arbeit löschen
