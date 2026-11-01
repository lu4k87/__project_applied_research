[Claude] KreiswertS: Anmeldung, Firmenbereich, Verwaltung simuliert
Rückmeldung an: [Claude] dev-ws-ae
Kontext:
  KreiswertS (~/__project_applied_research/projekt-a-materialfluss/
  karte/) soll Konten bekommen. Vorschau vom 2026-11-01 entschieden
  (Schatzkammer d73e765):
  - Login:B – Region links, Anmeldung rechts: Passkey zuerst,
    sonst Anmeldelink per E-Mail (15 min), kein Passwort
  - Kunde:B – Treffer-Postfach: Seitenleiste, Trefferliste nach Wert,
    Detail mit Bedarf | Angebot + Wert-Aufschlüsselung (30/35/35)
  - Admin:A – Kennzahlen mit Ziel oben, Prüf-Warteschlange,
    gemeldete Inserate, Matching-Regeln, Protokoll eingeklappt
  - F1 nein: neue Firmen sofort aktiv, Team prüft nachträglich
    und kann sperren → Warteschlange = „nachträglich prüfen“
  - F3 ja: Treffer zeigt nur Rolle, Gemeinde, Entfernung;
    Firmenname erst nach angenommener Anfrage
  - Technik (Django/Supabase/Directus) bleibt OFFEN
Aufgabe:
  Interfaces funktionsfähig bauen, Backend + Datenbank nur
  simulieren: eine Mock-API-Schicht (z. B. api.js mit async
  Funktionen, Daten aus daten.js, Zustand in localStorage), die
  später 1:1 gegen ein echtes Backend getauscht wird. Anmeldung
  simuliert (Passkey/E-Mail-Link als Demo-Schritt, Demo-Konten je
  Rolle: Gast, Firmen-Mitglied, Firmen-Admin, Plattform-Team).
  Rechte laut Tabelle „Wer darf was“ in der Vorschau.
  Erst kurz planen (Dateien, Aufbau), dann umsetzen, prüfen,
  committen + pushen.
Dateien:
  - Vorschau: http://localhost:8085/__treasury__allprojects/
    applied_research/vorschauen/2026-11-01-kreiswerts-mit-anmeldung-
    firmenbereich-verwaltung-backend/index.html
  - Mockup-HTML als Vorlage: gleicher Ordner, mockup.html
  - karte/index.html, app.js, daten.js, kreiswerts.css
  - AGENTS.md + README.md des Projekts
Beachten:
  - Alle Firmen/Mengen bleiben sichtbar als Demo-Daten markiert
  - hell + dunkel, 1280 + 360 px, Selbsttest 6/6, keine
    Konsolenfehler (AGENTS.md §5); Port 8096 des Users nicht nutzen
  - öffentliche Karte bleibt ohne Anmeldung nutzbar
  - nicht gewählte Varianten optional in ideen.md der Schatzkammer
