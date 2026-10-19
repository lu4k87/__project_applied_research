# Projekt A: Materialflussanalyse

**Fragestellung:** Wie bewegen sich Materialien durch den Industriepark Kehrum (Kalkar), und wo lassen sie sich effizienter nutzen?

## Aufgaben

| Aufgabe | Inhalt | Stand |
|---|---|---|
| State of the Art | bestehende Analyse-Tools vergleichen (STAN, Umberto, e!Sankey, openLCA, QGIS, SankeyMATIC, SYNERGie) | erster Vergleich im Reiter „Tool-Vergleich“ der Karte |
| Kartierung | Industriepark Kehrum kartieren, Firmen einordnen: Materialproduzent, Hersteller, Handel/Logistik, Recycling, Entsorgung | offen – bisher nur fiktive Firmen |
| Personas | eine Persona je Branche | 5 Personas (Reiter „Personas“) |
| Design & Prototyp | interaktive Karte der Materialflüsse zwischen den Firmen | Prototyp mit Demo-Daten: `karte/index.html` |

## Karte öffnen

```bash
python3 -m http.server 8096 -d ~/__project_applied_research
# → http://localhost:8096/projekt-a-materialfluss/karte/
```

Direktlinks: `?mode=pot` (Potenzial), `?sel=beton` (Firma), `?tab=sankey|personas|tools`, `?theme=dark|light`.

## Daten

- Alle Firmen, Personas und Mengen in `karte/index.html` sind **fiktiv** (Demo-Daten, auf der Seite gekennzeichnet).
- Echte Firmen aus der Kartierung kommen mit Quelle hinzu; Mengen bleiben als Annahme gekennzeichnet, bis Firmen sie bestätigen.
