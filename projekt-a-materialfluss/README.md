# KreiswertS

**Digitaler Plattform-Prototyp für den zirkulären Kunststoff-Materialaustausch in Kamp-Lintfort** – vernetzt kunststoffproduzierende, verarbeitende und recycelnde Unternehmen; Profile, Sekundärmaterialien, Bedarfe und mögliche Austauschwege auf einer Karte. Proof of Concept, kein operativer Marktplatz.

Löst seit 2026-10-22 die Materialflusskarte Kehrum unter derselben Adresse ab (alter Stand: Git-Historie, letzter Commit `65ba3e1`).

## Ziele und Stand

| Ziel (Auftrag) | Stand im Prototyp |
|---|---|
| ≥ 10 regionale Unternehmen recherchiert | 12 fiktive Profile – Recherche echter Firmen offen |
| Profile, Materialübersicht, Suche + Filter | im Bereich „Plattform“ klickbar |
| Materialfluss-Karte mit 3 Szenarien | Bereich „Szenarien“ (Scrollytelling) |
| Tests für ≥ 5 Kernfunktionen + Ergebnissicherung | Selbsttest mit 6 Prüfungen, Ergebnis als JSON |
| Schritt-für-Schritt-Leitfaden | Entwurf mit 7 Schritten im Bereich „Einordnung“ |

## Seite öffnen

```bash
python3 -m http.server 8096 -d ~/__project_applied_research
# → http://localhost:8096/projekt-a-materialfluss/karte/
```

Direktlinks: `?lang=de|en` (ohne Angabe Browsersprache), `?theme=light|dark` (ohne Angabe Systemeinstellung), `?firm=<id>` (Firma in der Plattform, z. B. `regrana`), `?scn=s1|s2|s3` (Szenario).

## Aufbau

| Datei | Inhalt |
|---|---|
| `karte/index.html` | Gerüst: Schritt-Leiste + 6 Bereiche (Überblick, Prinzip, Plattform, Szenarien, Projekt, Einordnung) |
| `karte/daten.js` | alle Daten der Region (DE/EN): Karte, Firmen, Angebote, Bedarfe, Matching-Regeln, Szenarien, Projekttexte, Personas, Plattform-Vergleich |
| `karte/app.js` | Matching, Karte (SVG), Plattform, Scrollytelling, Selbsttest, Sprache + Theme |
| `karte/kreiswerts.css` | Look: hell = Aqua-Weiß mit Petrol, dunkel = Nachtblau mit Gold |

**Matching:** Pflicht = gleiches Polymer, passende Form und Qualität; Wert = Qualität 30 % + Menge 35 % + Nähe 35 % (Luftlinie, ab 25 km null). Rechnerisches Austauschpotenzial: Paare nach Wert, jede Tonne Angebot und Bedarf nur einmal vergeben.

**Replikation:** eine andere Region ersetzt nur `daten.js` – Karte, Matching, Szenarien und Selbsttest passen sich an.

## Daten

- Alle Firmen, Mengen, Wege und Personas sind **fiktiv** (auf der Seite gekennzeichnet).
- Echte Firmen kommen nur mit Quelle hinzu; Mengen bleiben als Annahme gekennzeichnet, bis Firmen sie bestätigen.
- Plattform-Vergleich (State of the Art): Recherche vom 2026-10-22, Quellen auf der Seite verlinkt – vor der Abgabe beim Anbieter prüfen.
