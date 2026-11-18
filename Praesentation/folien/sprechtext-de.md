# Sprechtexte (deutsch) – Folie 1 und 2

Stand 2026-11-18. Zusammen ca. 3 min bei ruhigem Tempo (rund 400 Wörter, vorher 486).

Regeln für diese Texte: Projekt-Memory `sprechtexte-ohne-ansprache` (kein wir/ihr/du/man, sachlich ohne Floskeln, Einstieg über die Folienüberschrift, jedes Tool bei der ersten Nennung kurz erklärt, ORM ausgeschrieben). Folie 3 (Datenbank) präsentiert eine andere Person.


## Folie 1 – App-Architektur: Tech-Stack und Weg einer Anfrage (ca. 1:35 min)

### Einstieg

Nach dem Frontend folgt das **Backend**: der Teil der App, der auf dem Server läuft.

Die Folie zur **App-Architektur** zeigt oben den **Tech-Stack**, darunter den **Weg einer Anfrage**.


### Tech-Stack

- Die App ist in **TypeScript** geschrieben, also JavaScript mit festen Datentypen.

- **Next.js** ist das Framework. Es liefert Webseiten und Server-Schnittstellen aus einem gemeinsamen Projekt.

- **Node.js**, die Laufzeitumgebung, führt den Code außerhalb des Browsers auf dem Server aus.

- Die übrigen Werkzeuge sind nach ihrer Aufgabe gruppiert: Benutzeroberfläche, Backend und Sicherheit, Daten.


### Weg einer Anfrage

Es gibt zwei Rollen:

- Der **Gast** ist nicht eingeloggt.

- Das **Mitglied** ist eingeloggt und sendet ein Session-Cookie mit, eine kleine Kennung, an der der Server es wiedererkennt.

Jede Anfrage durchläuft **fünf Stationen**:

1. **Next.js** nimmt sie an.

2. **Better Auth**, eine Bibliothek für Login und Nutzerkonten, erkennt, ob ein Gast oder ein Mitglied anfragt.

3. **Zod**, eine Bibliothek zur Prüfung von Daten, kontrolliert das Format der Eingabe.

4. Der **Data Access Layer**, eine eigene Code-Schicht der App, legt fest, welche Daten diese Rolle sehen darf.

5. Das **Object-Relational Mapping**, kurz ORM, übersetzt den Programmcode in eine SQL-Abfrage, die Sprache der Datenbank.

Der Browser hat keinen direkten Zugriff auf die Datenbank.


### Ergebnis je Rolle

- Der **Gast** sieht Titel, Material, Menge und Stadt eines Angebots und kann sich registrieren.

- Das **Mitglied** sieht zusätzlich Preis und Kontakt, kann Matches anfragen und eigene Angebote einstellen.


## Folie 2 – Software Architecture Stack: Was jeder Baustein tut (ca. 1:25 min)

### Einstieg

Diese Folie zeigt, **was jeder Baustein** des Software Architecture Stacks tut und warum die Wahl auf ihn fiel.


### Grundlage jeder Anfrage

- **TypeScript**: Ein Angebot hat immer einen Titel als Text und eine Menge als Zahl. Frontend, Backend und Datenzugriff nutzen dieselbe Sprache.

- **Next.js**: Jede Datei im Ordner app wird zu einer Adresse, etwa `/offers` für die Liste der Angebote. Seiten und API teilen Code, Typen und ein Deployment.

- **Node.js** bearbeitet viele Anfragen gleichzeitig, ohne zu blockieren, und ist die Standard-Laufzeit für Next.js.


### Die vier Stationen ab dem Frontend

- **Better Auth**: Ohne Cookie gilt die Anfrage als Gast, mit Cookie als Mitglied. Gewählt, weil es Open Source ist und die Nutzerkonten in der eigenen Datenbank bleiben.

- **Zod**: Eine Menge in Kilogramm muss eine positive Zahl sein, sonst wird die Eingabe abgelehnt. Ein einziges Schema liefert Prüfung und TypeScript-Typ zugleich.

- **Data Access Layer**: Preis und Kontakt sehen nur Mitglieder, ein Angebot ändert nur der eigene Standort. Diese Regeln stehen an einer Stelle statt verteilt im Code.

- **Object-Relational Mapping** mit Prisma oder Drizzle: Es lädt zum Beispiel alle Angebote eines Materials. Gewählt, weil es typsicher ist und Werte sicher einsetzt. Das verhindert SQL-Injection.


### Übergabe

Bis hierhin das Backend. Was in der Datenbank steckt, zeigt jetzt **[Name]**.
