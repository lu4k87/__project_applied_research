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
| `karte/index.html` | Gerüst: Logo (S-Schleife, auch `favicon.svg`), Schritt-Leiste + 7 Bereiche (Überblick, Prinzip, Plattform, Szenarien, Projekt, Einordnung, Funktionen) |
| `karte/daten.js` | alle Daten der Region (DE/EN): Karte, Firmen, Angebote, Bedarfe, Matching-Regeln, Szenarien, Projekttexte, Personas, Plattform-Vergleich |
| `karte/app.js` | Matching, Karte (SVG-Lage: Wege, Firmen; ohne Grundkarte schematisch), Plattform, Scrollytelling, Selbsttest, Sprache + Theme |
| `karte/grundkarte.js` | echte Grundkarte (MapLibre + PMTiles): Lagebild + Szenarien fest auf der Region, Plattform mit Ebenen Deutschland → Land → Kreis → Gemeinde (Pfadleiste + Zurück, Esc) |
| `karte/geo/` | Kartendaten: `de.pmtiles` (bis Zoom 8), `region.pmtiles` (Region bis Zoom 14, lädt erst beim Hineinzoomen), `grenzen/` (VG250, Gemeinden je Land), `fonts/`; Herkunft, Lizenzen, Befehle: [`QUELLEN.md`](karte/geo/QUELLEN.md) |
| `karte/vendor/` | MapLibre GL 6.15 + pmtiles 4.5 lokal, mit Lizenztexten |
| `karte/kreiswerts.css` | Look: hell = Aqua-Weiß mit Petrol, dunkel = Nachtblau mit Gold |
| `karte/matching.js` | Matching-Regel (Pflicht + Wert), gemeinsam für Karte und simuliertes Backend |
| `karte/konto.html`, `konto.js`, `konto.css` | Konten: Anmeldung (Login:B), Firmenbereich mit Treffer-Postfach (Kunde:B), Verwaltung für das Plattform-Team (Admin:A) |
| `karte/api.js` | simuliertes Backend `KW_API`: async Funktionen, Zustand in localStorage, Rechte je Rolle – wird später 1:1 gegen ein echtes Backend getauscht |
| `karte/api-test.html` | Test der Mock-API im Browser (Rechte, Anmeldung, Anonymität, Eingabeprüfung); setzt die Demo-Daten zurück |

**Matching:** Pflicht = gleiches Polymer, passende Form und Qualität; Wert = Qualität 30 % + Menge 35 % + Nähe 35 % (Luftlinie, ab 25 km null). Rechnerisches Austauschpotenzial: Paare nach Wert, jede Tonne Angebot und Bedarf nur einmal vergeben.

**Konten (simuliert, Entscheidung 2026-11-01):** `konto.html` – Anmeldung per Passkey oder Anmeldelink (15 min, kein Passwort); Postfach und Passkey-Auswahl sind Demo-Schritte. Demo-Konten je Rolle: Gast (öffentliche Karte), Firmen-Mitglied, Firmen-Admin, Plattform-Team. Neue Firmen sind sofort aktiv, das Team prüft nachträglich und kann sperren. Treffer zeigen nur Rolle, Gemeinde und Entfernung – Firmennamen erst nach angenommener Anfrage. Rechte prüft `api.js` wie ein Backend (Gast: grob · Mitglied: Inserate + Anfragen · Firmen-Admin: + Team und Profil · Plattform-Team: Prüfen, Sperren, Moderation, Matching-Regeln). Technik für das echte Backend (Django/Supabase/Directus) ist noch offen. Die öffentliche Karte bleibt ohne Anmeldung nutzbar.

**Replikation:** eine andere Region ersetzt `daten.js` (inkl. `region.ags` = Startebene) und `geo/region.pmtiles` (Befehl in `geo/QUELLEN.md`) – Karte, Matching, Szenarien und Selbsttest passen sich an. `?schematic` zeigt die eigene schematische Karte ohne Grundkarte.

## Daten

- Alle Firmen, Mengen, Wege und Personas sind **fiktiv** (auf der Seite gekennzeichnet).
- Echte Firmen kommen nur mit Quelle hinzu; Mengen bleiben als Annahme gekennzeichnet, bis Firmen sie bestätigen.
- Plattform-Vergleich (State of the Art): Recherche vom 2026-10-22, Quellen auf der Seite verlinkt – vor der Abgabe beim Anbieter prüfen.
