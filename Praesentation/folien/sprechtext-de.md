# Sprechtexte (deutsch) – Folie 1 und 2

Stand 2026-11-18. Zusammen ca. 3 min (rund 500 Wörter).

Regeln für diese Texte: Projekt-Memory `sprechtexte-ohne-ansprache` (kein wir/ihr/du/man, sachlich ohne Floskeln, Einstieg über die Folienüberschrift, jedes Tool bei der ersten Nennung kurz erklärt, ORM ausgeschrieben). Folie 3 (Datenbank) präsentiert eine andere Person.


## Folie 1 – App-Architektur: Tech-Stack und Weg einer Anfrage (ca. 1:30 min)

### Einstieg

Nach dem Frontend folgt das **Backend**: der Teil der App, der auf dem Server läuft und für Besucher unsichtbar bleibt.

Die Folie zur **App-Architektur** zeigt dazu zwei Dinge: oben den **Tech-Stack**, darunter den **Weg einer Anfrage**.


### Tech-Stack

- Die App ist in **TypeScript** geschrieben, einer Programmiersprache, die JavaScript um feste Datentypen ergänzt.

- Das Framework ist **Next.js**. Es liefert Webseiten und Server-Schnittstellen aus einem gemeinsamen Projekt.

- Der Server läuft auf **Node.js**, einer Laufzeitumgebung, die JavaScript und TypeScript außerhalb des Browsers ausführt.

- Die übrigen Werkzeuge sind nach ihrer Aufgabe gruppiert: Benutzeroberfläche, Backend und Sicherheit, Daten.


### Weg einer Anfrage

Es gibt zwei Rollen:

- Der **Gast** ist nicht eingeloggt.

- Das **Mitglied** ist eingeloggt und sendet mit jeder Anfrage ein Session-Cookie, eine kleine Kennung, an der der Server das Mitglied wiedererkennt.

Jede Anfrage durchläuft **fünf Stationen** auf dem Server:

1. **Next.js** nimmt sie an.

2. **Better Auth**, eine Bibliothek für Login und Nutzerkonten, stellt fest, ob ein Gast oder ein Mitglied anfragt.

3. **Zod**, eine Bibliothek zur Prüfung von Daten, kontrolliert, ob die Eingabe dem erwarteten Format entspricht.

4. Der **Data Access Layer**, eine eigene Code-Schicht der App, legt fest, welche Daten diese Rolle sehen darf.

5. Zuletzt übersetzt das **Object-Relational Mapping**, kurz ORM, den Programmcode in eine SQL-Abfrage, also in die Sprache der Datenbank.

Der Browser hat keinen direkten Zugriff auf die Datenbank.


### Ergebnis je Rolle

Was zurückkommt, hängt von der Rolle ab:

- Der **Gast** sieht Titel, Material, Menge und Stadt eines Angebots und kann sich registrieren.

- Das **Mitglied** sieht zusätzlich Preis und Kontakt, kann Matches anfragen und eigene Angebote einstellen.


## Folie 2 – Software Architecture Stack: Was jeder Baustein tut (ca. 1:30 min)

### Einstieg

Diese Folie zeigt, **was jeder Baustein** des Software Architecture Stacks in der App tut und warum die Wahl auf ihn fiel.


### Grundlage jeder Anfrage

- **TypeScript** sorgt zum Beispiel dafür, dass ein Angebot immer einen Titel als Text und eine Menge als Zahl hat. Der Vorteil: Frontend, Backend und Datenzugriff nutzen dieselbe Sprache.

- **Next.js** macht aus jeder Datei im Ordner app eine Adresse. `/offers` zeigt die Liste, `/offers/[id]` ein einzelnes Angebot. So entsteht ein Projekt statt zwei: Seiten und API teilen Code, Typen und ein Deployment.

- **Node.js** bearbeitet viele Anfragen gleichzeitig, ohne zu blockieren. Es ist die Standard-Laufzeit für Next.js und nutzt dieselbe Sprache wie der Browser.


### Die vier Bausteine ab dem Frontend

Darunter die vier Bausteine, die jede Anfrage vom Frontend aus durchläuft:

- **Better Auth**: Ohne Cookie gilt die Anfrage als Gast, mit Cookie als Mitglied. Gewählt, weil es Open Source ist und die Nutzerkonten in der eigenen Datenbank bleiben.

- **Zod**: Eine Menge in Kilogramm muss eine positive Zahl sein, sonst wird die Eingabe abgelehnt. Ein einziges Schema liefert dabei die Prüfung und den TypeScript-Typ.

- **Data Access Layer**: Preis und Kontakt sehen nur Mitglieder, ein Angebot ändert nur der eigene Standort. Diese Zugriffsregeln stehen an einer Stelle statt verteilt im Code.

- **Object-Relational Mapping** mit Prisma oder Drizzle: Es lädt zum Beispiel alle Angebote eines Materials. Gewählt, weil es typsicher ist und Werte sicher einsetzt. Das verhindert SQL-Injection.


### Übergabe

Bis hierhin das Backend. Was in der Datenbank steckt, zeigt jetzt **[Name]**.
