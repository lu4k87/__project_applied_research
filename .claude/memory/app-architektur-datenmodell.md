---
name: app-architektur-datenmodell
description: Tabellen, Felder und Begriffe des KreiswertS-Datenmodells als Hintergrund für die 2 App-Architektur-Folien (UML-Folie selbst ist gestrichen)
metadata:
  type: project
---

Die UML-Folie hat der User am 2026-11-18 gestrichen; das Deck in `Praesentation/folien/` hat nur Folie 1 (Tech-Stack + Weg einer Anfrage) und Folie 2 (Software Architecture Stack: 11 Bausteine). Das Datenmodell bleibt nur als Wissen, damit Begriffe auf beiden Folien dazu passen. Die Datenbank präsentiert eine andere Person direkt danach, das Frontend eine andere Gruppe.

**Why:** User: „UML-Folie kann weg, nur Tabellen und Namen/Begriffe merken für die 2 Folien.“
**How to apply:** Texte auf Folie 1/2 (z. B. „Standorte, Nutzer, Materialien, Angebote, Matches“, Gast/Mitglied, 7-Tage-Erinnerung) gegen diese Liste prüfen; keine eigene Datenbank-Folie mehr bauen.

PostgreSQL, 5 Tabellen (UML-Datenmodell):
- **users** (Login eines Standorts): id PK, site_id FK→sites, email (eindeutig), password_hash, account_status, created_at (Start der 7-Tage-Frist)
- **sites** (Betrieb mit Standort): id PK, business_name, branch_name, city (Gast), latitude/longitude, contact_email,.. (Mitglied)
- **materials** (Materialkatalog): id PK, code (eindeutig), name (Gast), category, impact_factor_* (optional)
- **offers** (Angebot eines Standorts): id PK, seller_site_id FK→sites, material_id FK→materials, title (Gast), available_quantity_kg (Gast), price_eur_per_kg (Mitglied), description (Mitglied), status,..
- **matches** (vom Mitglied angefragt): id PK, offer_id FK→offers, buyer_site_id FK→sites, agreed_quantity_kg, agreed_price_eur_per_kg, status, completed_at (optional), actual_quantity_kg,..

Beziehungen: users 1:1 sites (Zugang) · sites 1:n offers (Verkäufer) · sites 1:n matches (Käufer) · materials 1:n offers (ordnet ein) · offers 1:n matches (Vereinbarung). Kein Zugriff aus dem Browser, nur das Backend liest/schreibt.

Begriffe: **Gast** (ohne Login: Titel, Material, Menge, Stadt) · **Mitglied** (Standort + Login: zusätzlich Preis, Beschreibung, Kontakt, Match anfragen, Angebote einstellen) · **Match** = Vereinbarung Käufer–Angebot.

7-Tage-Job: BullMQ Queue plant bei Registrierung (Frist ab users.created_at) → Redis hält den Job → BullMQ Worker zählt Matches nach 7 Tagen → nur bei 0 Matches: React Email baut die Erinnerung → Mail-Dienst (noch offen: Resend, Postmark oder Amazon SES) verschickt. Ab 1 Match endet der Job.

Verwandt: [[project-kreiswerts]]
