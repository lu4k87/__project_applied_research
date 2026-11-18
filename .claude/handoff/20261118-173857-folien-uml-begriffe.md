[Folien] App-Architektur-Folien auf UML-Datenmodell umbauen
übernommen von dev-ws-d5 am 2026-11-18 17:40
Rückmeldung an: [Claude] dev-ws-2f

Kontext: Repo ~/__project_applied_research, Folien in Praesentation/folien/. build_folien.py erzeugt App-Architektur.pptx (DE) + App-Architecture-EN.pptx (EN); PNGs per `soffice --headless --convert-to pdf` → `pdftoppm -png -scale-to-x 1920 -scale-to-y 1080` (folie-1/2.png, slide-1/2-en.png). Braucht python-pptx, cairosvg, Pillow (venv anlegen). Stand 3fde587. Links für den User: Kopien in ~/ai_dev_workflow_global/__treasury__allprojects/applied_research/folien/2026-11-18-app-architektur/ (4 PNG + 2 PPTX), dann `python3 bin/treasury.py save "<Nachricht>"` im globalen Repo; URLs http://localhost:8085/__treasury__allprojects/applied_research/folien/2026-11-18-app-architektur/<datei>.

Aufgabe: Begriffe und Folie 2 auf das UML-Datenmodell des Users umstellen (Entscheidungen stehen fest):
- 5 Tabellen statt Better-Auth-Tabellen + listings/trades:
  - sites: id PK, business_name, branch_name, description, street_address, postal_code, city, country_code, latitude, longitude, contact_name, contact_email, contact_phone, created_at
  - users: id PK, site_id FK UNIQUE NOT NULL, email UNIQUE NOT NULL, password_hash, account_status, created_at
  - materials: id PK, code UNIQUE, name, category, impact_factor_kg_co2e_per_kg nullable, impact_factor_reference nullable, impact_factor_version nullable
  - offers: id PK, seller_site_id FK, material_id FK, title, description, available_quantity_kg, price_eur_per_kg, available_from, status, created_at, updated_at
  - matches: id PK, offer_id FK, buyer_site_id FK, agreed_quantity_kg, agreed_price_eur_per_kg, status, agreed_at (nullable bis agreed), actual_quantity_kg (nullable bis completed), completed_at (nullable bis completed), estimated_avoided_kg_co2e nullable, impact_factor_used nullable, impact_factor_reference nullable, impact_factor_version nullable
- Beziehungen zeigen: sites 1:1 users (branch login) · sites 1:n offers (seller) · materials 1:n offers (classifies) · sites 1:n matches (buyer) · offers 1:n matches (agreements).
- Feldnamen in snake_case wie im UML (bei vielen Feldern sinnvoll kürzen, Rest mit „,..“).
- Sichtbarkeit: Gast sieht title, Material, Menge, Stadt; Mitglied zusätzlich Preis, Beschreibung, Kontakt, Match anfragen. Ersetzt previewText/memberDetails überall (Station 4, Browserfenster Gast/Mitglied inkl. Adresszeile, Folie 2).
- Überall trades → matches, listings → offers; Mitglied = Standort-Login (users ↔ sites 1:1). Folie 1 DB-Zylinder „Konten, Logins, Angebote, Trades“ → Standorte, Nutzer, Materialien, Angebote, Matches; Mitglied-Fenster „Eigene Trades/Handeln“ → Matches; 7-Tage-Job: zählt Matches, „nur bei 0 Matches“, Frist aus users.created_at.
- Außerdem freigegeben: Station 4 „Was darf Gast oder Mitglied sehen?“ statt „Rolle (User)“; Job-Hops „7 Tage verzögert“, „Job fällig“, „Erinnerungs-E-Mail“; gestrichelten Pfeil Tabellen → Worker mit „Anzahl Matches“ beschriften (Lücke Tabellen ↔ Job-Kette verbreitern); Benefits „Erinnerungs-E-Mails,..“ statt „Automatische E-Mails,..“; Zonen-Titel „Frontend · Browser“ und „Hintergrund-Job · 7 Tage, ohne Browser“.
- Alles auch Englisch (EN-Dict in build_folien.py; Ausgabe „ohne Übersetzung“ darf nur Eigennamen/Feldnamen enthalten).

Dateien: Praesentation/folien/build_folien.py, App-Architektur.pptx, App-Architecture-EN.pptx, folie-1.png, folie-2.png, slide-1-en.png, slide-2-en.png

Beachten: Erst Layout-Vorschlag für Folie 2 (5 Tabellen + Beziehungslinien) zeigen, dann bauen. Jede Änderung DE + EN rendern und ansehen (kein Überlauf, Zero Overlap). Beibehalten: Zentrierung, Lucide-Icons (icons/), Tool-Schrift Verdana, Browserfenster-Look, Benefits-Karte links + 2 Spalten. Die 2 PPTX liegen uncommittiert nur neu erzeugt (Inhalt unverändert) → der nächste Build überschreibt sie. Am Ende die 4 PNG-Links nennen.
