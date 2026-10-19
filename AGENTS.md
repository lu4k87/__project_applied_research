# Projekt-Regeln (materialfluss)

Ergänzt die gemeinsamen Regeln aller Projekte (`~/.claude/CLAUDE.md` → `~/ai_dev_workflow_global/rules/RULES.md`, gleiche Abschnittsnummern); bei Widerspruch gilt diese Datei, Sicherheit (§0) hat immer Vorrang. Angelegt am 2026-10-19 mit `~/ai_dev_workflow_global/bin/projects.py new`; Stellen mit „ausfüllen“ klärt der erste Chat mit dem User.

## 0. Sicherheit
- **Arbeitsstand des Users nicht anfassen:** laufende Instanz, Port, Datenordner – ausfüllen; Tests nur mit eigener Instanz.
- Zugangsdaten, `.env`, Nutzerdaten nie einchecken, nie in Antworten oder Screenshots zeigen.

## 0c. Skill-Finder
- Allgemeine Skills: Tabelle in `RULES.md` §0c; eigene Skills dieses Projekts in `.claude/skills/` → hier je eine Zeile.

## 4. Projekt-Karte

| Ort | Zweck |
|---|---|
| `AGENTS.md` | diese Regeln (`GEMINI.md` = Link darauf) |
| `.claude/memory/` | Projekt-Memory, Index `MEMORY.md` (Claude lädt ihn selbst, Codex/Gemini lesen ihn zu Beginn) |

## 5. Arbeitsweise
- **Prüfungen (Definition of Done):** ausfüllen (Tests, Linter, Start-Befehl).
- **Commit + Push:** direkt in diesem Repo (Repo noch offen → URL in `~/ai_dev_workflow_global/config/projects.yaml` eintragen), Skill `commit`; Liste aller Projekte: `~/ai_dev_workflow_global/config/projects.yaml`.
