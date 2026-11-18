[Claude] [Folien] 2 neue Folien Plastik-Hub: je 3 Varianten zeigen
Rückmeldung an: dev-ws-2d
Kontext: Deck Praesentation/folien/ hat 2 Folien (Folie 1 Tech-Stack +
  Weg einer Anfrage, Folie 2 Software Architecture Stack), gebaut mit
  build_folien.py (python-pptx) → App-Architektur.pptx (DE) +
  App-Architecture-EN.pptx, PNGs folie-1/2.png + slide-1/2-en.png.
  Stand 89252dd. Der User hat eine Projektbeschreibung eingefügt
  (unten wörtlich): Circular Polymer Decision Hub, Website-Prototyp
  zu Kunststoffen (PET, HDPE, PP, PVC), Datenbank, Vergleich nach
  Kreislauf-Kriterien, für Bürger und Unternehmen.
Aufgabe: 2 „neue“, angepasste Folien (auf Basis von Folie 1 + 2), die
  Informationen aus der Beschreibung ergänzen. ERST je Folie 3
  Varianten als Vorschau zeigen (Skill preview + variation,
  Keys Folie1:A/B/C, Folie2:A/B/C), umsetzen erst nach Auswahl.
Dateien:
  - Praesentation/folien/build_folien.py
  - Praesentation/index.html (Inhalt, Wortwahl)
  - .claude/memory/app-architektur-datenmodell.md
Beachten:
  - python-pptx fehlt im System-Python → venv im eigenen Scratchpad
    (pip install python-pptx cairosvg Pillow lxml)
  - Rendern: soffice --headless --convert-to pdf, dann pdftoppm
    -png -scale-to-x 1920 -scale-to-y 1080
  - Memory: Folien sagen „Matches“, keine E-Mail-Funktion, keine
    eigene Datenbank-Folie; immer beide Folien-URLs nennen
    (http://localhost:8096/Praesentation/folien/…, Server 8096
    läuft bereits)
  - Bestehende Folien 1 + 2 nicht ändern, bis der User gewählt hat;
    klären, ob die neuen Folien ersetzen oder dazukommen
  - DE + EN, Stil wie bisher (Arial/Verdana, Farben S1/S2/S3)

Projektbeschreibung (vom User eingefügt, wörtlich):

### 1.2 Project Description
This project aims to design and develop a website prototype for the
Circular Polymer Decision Hub, focusing specifically on plastic
materials and their circular economy potential.

The website will provide users with accessible information about
different types of plastics, including their properties, common
applications, recyclability, and possible reuse options.

The prototype will include a plastic material database, a simplified
evaluation system for comparing selected plastic materials, and a
user-friendly interface to present the results. It will demonstrate
how digital solutions can support informed material selection and
promote circular economy awareness.

The primary beneficiaries will be  citizens and businesses interested
in understanding plastic sustainability and recycling opportunities.

### 1.3 Problem Statement
Plastic materials are widely used in industrial and everyday
applications, but information about their recyclability,
environmental characteristics, and circular economy potential is
often difficult to understand or compare.

Users may struggle to identify different plastics and determine
suitable reuse or recycling options. Existing information is
frequently scattered across multiple sources.

A centralized, easy-to-use website prototype can help address this
problem by making basic plastic material information and circularity
assessments more accessible.

### 1.4 Project Targets
The main objectives are to:

1. Develop a functional, user-friendly website prototype.
2. Create a small database containing information about selected
   plastic materials, such as PET, HDPE, PP, and PVC.
3. Provide information on material properties, common applications,
   reuse possibilities, and recyclability.
4. Implement a simplified comparison or assessment feature based on
   clearly defined circularity criteria.
5. Test the website's functionality and usability using selected
   plastic material examples.
