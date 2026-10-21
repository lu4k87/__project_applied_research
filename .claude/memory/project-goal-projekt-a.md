---
name: project-goal-projekt-a
description: Projekt A Materialflussanalyse Kehrum – Vorgänger der KreiswertS-Seite (bis 2026-10-22), Doppelarbeit mit Gemini-Chat, echte Firmen nur mit Quelle
metadata:
  type: project
---

Projekt A (Materialflussanalyse Industriepark Kehrum, Kalkar): State-of-the-Art-Vergleich, Kartierung + Branchen-Einordnung, Personas je Branche, interaktive Karte.

Stand 2026-10-19: Prototyp `projekt-a-materialfluss/karte/index.html` mit fiktiven Demo-Daten ([Claude] dev-ws-06). Ein Gemini-Chat (gemini-24750c) baute parallel eine eigene Version (Schatzkammer `dev_ws/vorschauen/2026-10-19-materialflussanalyse-kehrum/`, echte Firmennamen + erfundene Mengen); beste Teile (Sankey, Personas, Tool-Vergleich, Tempo) wurden übernommen.

Seit 2026-10-22 ersetzt **KreiswertS** (Kunststoff-Austausch Kamp-Lintfort, [[project-kreiswerts]]) die Kehrum-Karte unter derselben Adresse (Entscheidung des Users); der Kehrum-Stand bleibt in der Git-Historie (letzter Commit davor `65ba3e1`).

**Why:** Ohne Notiz startet der nächste Chat wieder doppelt, sucht die Kehrum-Seite vergeblich oder übernimmt echte Namen mit erfundenen Zahlen.
**How to apply:** Vor Arbeit an der Karte Gemini-Stand prüfen; echte Firmen nur mit Quelle (AGENTS.md §0); Kehrum-Inhalte nur aus der Git-Historie holen.
