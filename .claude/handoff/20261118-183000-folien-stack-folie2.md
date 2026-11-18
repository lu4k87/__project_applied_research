[Folien] Neue Folie 2: Software Architecture Stack erklären
übernommen von dev-ws-4c am 2026-11-18 17:54
Rückmeldung an: [Claude] dev-ws-d5
Kontext: Repo ~/__project_applied_research, Folien in
  Praesentation/folien/ (build_folien.py → App-Architektur.pptx DE +
  App-Architecture-EN.pptx EN, PNGs per soffice → pdftoppm 1920×1080;
  braucht python-pptx, cairosvg, Pillow im venv). Stand 2bfb3bf.
  Folie 1 = Tech-Stack + Weg einer Anfrage (5 Stationen),
  Folie 2 = UML-Datenmodell (5 Tabellen) + 7-Tage-Job.
  Präsentation des Users: Teil „Software Architecture Stack“.
  Frontend stellt eine andere Gruppe vor, die Datenbank präsentiert
  direkt danach eine andere Person.
Aufgabe: neue sinnvolle Folie 2 für den Stack-Teil entwerfen:
  - Begriffe des Stacks verständlich erklären + begründen
    (warum gewählt): TypeScript, Next.js, Node.js, Better Auth, Zod,
    Data Access Layer, ORM Prisma/Drizzle, BullMQ, Redis,
    React Email, Mail-Dienst
  - Frontend und Datenbank nur als Schnittstelle/Übergabe zeigen
  - bisherige UML-Folie nur zur Information behalten (z. B. als
    Folie 3 / Anhang), nicht löschen
  - erst Vorschau-Varianten (Skill preview): je Baustein der Folie
    (z. B. Aufbau, Erklärform, Begründung, Übergang zur DB-Person)
    eigene Varianten mit Bild, User klickt sich die Komponenten
    zusammen, „An Chat senden“ → dann bauen
  - genau zeigen, was wie eingebaut wird (Inhalt je Karte)
Dateien:
  - Praesentation/folien/build_folien.py
  - Praesentation/folien/App-Architektur.pptx
  - Praesentation/folien/App-Architecture-EN.pptx
  - Praesentation/folien/folie-*.png, slide-*-en.png
Beachten:
  - Stil von Folie 1 beibehalten: Zentrierung, Lucide-Icons
    (icons/), Tool-Schrift Verdana, Farben S1–S4, Benefits-Look
  - jede Änderung DE + EN rendern und ansehen (kein Überlauf,
    Zero Overlap); EN-Dict vollständig
  - Links für den User: Kopien nach ~/ai_dev_workflow_global/
    __treasury__allprojects/applied_research/folien/
    2026-11-18-app-architektur/, dann bin/treasury.py save
