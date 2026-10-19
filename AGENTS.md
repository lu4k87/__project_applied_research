# Projekt-Regeln (Applied Research)

Ergänzt die gemeinsamen Regeln aller Projekte (`~/.claude/CLAUDE.md` → `~/ai_dev_workflow_global/rules/RULES.md`, gleiche Abschnittsnummern); bei Widerspruch gilt diese Datei, Sicherheit (§0) hat immer Vorrang. Angelegt am 2026-10-19 mit `~/ai_dev_workflow_global/bin/projects.py new`.

## 0. Sicherheit
- **Arbeitsstand des Users nicht anfassen:** läuft beim User ein Server auf Port 8096, eigene Tests auf anderem Port.
- Zugangsdaten, `.env`, Nutzerdaten nie einchecken, nie in Antworten oder Screenshots zeigen.
- **Daten ehrlich kennzeichnen:** erfundene Mengen nie echten Firmennamen zuordnen, ohne sie sichtbar als Annahme/Demo zu markieren; echte Firmen nur mit Quelle (Entscheidung 2026-10-19).

## 0c. Skill-Finder
- Allgemeine Skills: Tabelle in `RULES.md` §0c; für die Karte vor allem `dataviz`, `soft-motion`, `d3-viz`.

## 4. Projekt-Karte

| Ort | Zweck |
|---|---|
| `README.md` | Übersicht aller Teilprojekte + Start-Befehl |
| `projekt-a-materialfluss/` | Projekt A: `README.md` (Aufgaben, Stand), `karte/index.html` (Prototyp) |
| `projekt-a-materialfluss/karte/index.html` | Prototyp: Karte, Stoffstrombilanz (Sankey), Personas, Tool-Vergleich – eine Datei, Demo-Daten oben im Skript |
| `AGENTS.md` | diese Regeln (`GEMINI.md` = Link darauf) |
| `.claude/memory/` | Projekt-Memory, Index `MEMORY.md` (Claude lädt ihn selbst, Codex/Gemini lesen ihn zu Beginn) |
| Schatzkammer `~/ai_dev_workflow_global/__treasury__allprojects/applied_research/` | Vorschauen, Varianten, Ideen (nicht hier im Repo) |

## 5. Arbeitsweise
- **Start:** `python3 -m http.server 8096 -d ~/__project_applied_research` → `http://localhost:8096/projekt-a-materialfluss/karte/`.
- **Prüfungen (Definition of Done):** Headless Chrome mit eigenem Profil – hell + dunkel, 1280 px und 360 px, keine Konsolenfehler; Klicks auf Szenario, Firma, Maßnahme, Reiter; Endzustand mit `--force-prefers-reduced-motion` ansehen (Einblend-Animationen laufen in virtueller Zeit nicht durch).
- **Commit + Push:** direkt in diesem Repo (`git@github.com:lu4k87/__project_applied_research.git`, privat), Skill `commit`; Liste aller Projekte: `~/ai_dev_workflow_global/config/projects.yaml`.
