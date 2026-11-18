---
name: app-architektur-datenmodell
description: Tabellen, Felder und Begriffe des KreiswertS-Datenmodells (ER-Diagramm 2026-11-18) als Hintergrund für die 2 App-Architektur-Folien; Folien sagen bewusst „Matches“, ohne E-Mail-Funktion
metadata:
  type: project
---

Das Deck in `Praesentation/folien/` hat 3 Folien: Folie 1 (Tech-Stack + Weg einer Anfrage), Folie 2 (Software Architecture Stack: 7 Bausteine), Folie 3 (ER-Diagramm „Erstes Datenmodell“, alle Felder + Typen 1:1 aus dem Bild des Users, Krähenfuß-Linien; `slide_db`). Die alte UML-Folie war am 2026-11-18 gestrichen, Folie 3 hat der User am selben Tag ausdrücklich neu bestellt. Die Datenbank präsentiert eine andere Person direkt danach, das Frontend eine andere Gruppe.

**Why:** User: „UML-Folie kann weg, nur Tabellen und Namen/Begriffe merken für die 2 Folien.“ Abgleich mit dem ER-Diagramm am 2026-11-18: Tabelle heißt dort `agreements`, die Folien bleiben trotzdem bei „Matches“ (User-Entscheidung). Die Funktion „Automatische E-Mails“ (7-Tage-Erinnerung, BullMQ, Redis, React Email, Mail-Dienst) hat der User am selben Tag ganz aus den Folien entfernt.
**How to apply:** Texte auf Folie 1/2 gegen diese Liste prüfen; „Matches“ nicht in „Vereinbarungen“ ändern; E-Mail-Zeile und 7-Tage-Job nicht wieder einbauen; Folie 3 zeigt die Tabellennamen wie im ER-Diagramm (`agreements`, Untertitel „Match: Käufer + Angebot“); sites–users ist dort 1:1 (beide Enden ||).

PostgreSQL, 5 Tabellen (ER-Diagramm 2026-11-18):
- **users** (Login eines Standorts): id PK, site_id FK→sites, email (U), password, account_status – kein created_at
- **sites** (Betrieb mit Standort): id PK, company_name, branch_name, description (N), street_address, postal_code, city (Gast), latitude/longitude, contact_name/email/phone (Mitglied)
- **materials** (Materialkatalog): id PK, code (U), name (Gast), category, impact_factor_kg_co2e_per_kg
- **offers** (Angebot eines Standorts): id PK, seller_site_id FK→sites, material_id FK→materials, title (Gast), available_quantity_kg (Gast), price_eur_per_kg (Mitglied), available_from, status, created_at, updated_at – keine eigene Beschreibung
- **agreements** (auf den Folien „Matches“, vom Mitglied angefragt): id PK, offer_id FK→offers, buyer_site_id FK→sites, agreed_quantity_kg, agreed_price_eur_per_kg, status, buyer_confirmed_at/seller_confirmed_at/actual_quantity_kg/completed_at/impact_factor_used (N), created_at

Beziehungen: sites 1:n users · sites 1:n offers (Verkäufer) · sites 1:n agreements (Käufer) · materials 1:n offers · offers 1:n agreements. Kein Zugriff aus dem Browser, nur das Backend liest/schreibt.

Begriffe: **Gast** (ohne Login: Titel, Material, Menge, Stadt) · **Mitglied** (Standort + Login: zusätzlich Preis, Beschreibung, Kontakt, Match anfragen, Angebote einstellen, eigene Matches) · **Match** = Agreement Käufer–Angebot.

Offen im ER-Diagramm (dem User gemeldet 2026-11-18): „Beschreibung“ auf der Folie gibt es nur als sites.description; price_eur_per_kg FLOAT vs. agreed_price_eur_per_kg INTEGER.

Verwandt: [[project-kreiswerts]]
