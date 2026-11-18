---
name: folien-beide-urls
description: Nach jeder Änderung an den App-Architektur-Folien immer die URLs beider Folien nennen (EN + DE), nicht nur die geänderte
metadata:
  type: feedback
---

Nach jeder Änderung an `Praesentation/folien/` immer **beide** Folien-URLs nennen, nicht nur die geänderte Folie:
`http://localhost:8096/Praesentation/folien/slide-1-en.png`, `…/slide-2-en.png` (DE: `folie-1.png`, `folie-2.png`).

**Why:** Der User (2026-11-18): „gib immer beide folien urls!“. Er hatte nachgefragt, weil nur eine Folie verlinkt war.

**How to apply:** Läuft der Server auf 8096 nicht, `python3 -m http.server 8096 -d ~/__project_applied_research` starten und vorher auf HTTP 200 prüfen; je Folie eine `🌐 **Seite öffnen:**`-Zeile. Siehe auch [[app-architektur-datenmodell]].
