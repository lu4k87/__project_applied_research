"""Erzeugt die 2 Folien (16:9) aus der Architektur-Seite Praesentation/index.html.

Ausgabe: App-Architektur.pptx (deutsch) und App-Architecture-EN.pptx (englisch);
PNGs (1920 × 1080) per LibreOffice:
    python build_folien.py            # braucht python-pptx
    soffice --headless --convert-to pdf App-Architektur.pptx
    pdftoppm -png -scale-to-x 1920 -scale-to-y 1080 App-Architektur.pdf folie
Inhalt und Farben folgen index.html / style.css (helles Schema). Schrift Arial:
liegt in jedem PowerPoint und rendert in LibreOffice maßgleich (Liberation Sans).
"""
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

OUT = {"de": Path(__file__).with_name("App-Architektur.pptx"),
       "en": Path(__file__).with_name("App-Architecture-EN.pptx")}
LANG = "de"  # setzt main() je Durchlauf

# Englische Texte, Wortwahl wie die EN-Umschaltung in script.js
EN = {
    "App-Architektur: Tech-Stack und Weg einer Anfrage": "App Architecture: Tech Stack and the Path of a Request",
    "Eine Web-App mit Next.js und TypeScript. Jede Anfrage durchläuft fünf Stationen, bevor Daten fließen.":
        "A web app built with Next.js and TypeScript. Every request passes five steps before any data moves.",
    "Oben der Tech-Stack nach Oberbegriffen. Darunter der Weg einer Anfrage: Browser, fünf Stationen "
    "auf dem Next.js-Server, Datenbank. Unten, was Gast und Mitglied zurückbekommen.":
        "Top: the tech stack by group. Middle: the path of a request: browser, five steps on the Next.js "
        "server, database. Bottom: what guest and member get back.",
    "Sprache": "Language", "Laufzeit": "Runtime",
    "überall: Browser, Server, Worker": "everywhere: browser, server, worker",
    "App Router, auf React-Basis": "App Router, built on React",
    "führt Server und Worker aus": "runs the server and the worker",
    "Benutzeroberfläche": "User interface", "Sicherheit": "Security", "Daten": "Data",
    "Hintergrund & E-Mail": "Background & email", "Mail-Dienst": "Email service",
    "Gast": "Guest", "nicht registriert, ohne Cookie": "not signed up, no cookie",
    "Mitglied": "Member", "eingeloggt, mit Session-Cookie": "logged in, with session cookie",
    "Next.js-Server auf Node.js · für Besucher unsichtbar": "Next.js server on Node.js · hidden from visitors",
    "Einstiegspunkt": "Entry point", "Nimmt Seiten, Formulare und API-Aufrufe an": "Receives pages, forms and API calls",
    "Authentifizierung": "Authentication",
    "Prüft Login und Session-Cookie: Gast oder Mitglied?": "Checks login and session cookie: guest or member?",
    "Validierung": "Validation", "Prüft jede Eingabe gegen ein Schema": "Checks every input against a schema",
    "Autorisierung": "Authorization",
    "Gibt nur Felder frei, die die Rolle sehen darf": "Only lets through the fields this role may see",
    "Baut sichere, typisierte SQL-Abfragen": "Builds safe, typed SQL queries",
    "Datenbank": "Database", "Konten, Sitzungen, Angebote, Trades": "Accounts, logins, offers, trades",
    "→ Folie 2": "→ slide 2",
    "Antwort an den Gast": "Response to the guest", "Station 4 gibt nur": "Step 4 only lets",
    "frei: öffentliche Vorschauen": "through: public previews",
    "Antwort an das Mitglied": "Response to the member", "Zusätzlich": "Also",
    ": alle Details und Handel": ": all details and trading", "Merke": "Note",
    "Der Browser spricht nur mit dem Server. Scheitert eine Prüfung, endet die Anfrage dort.":
        "The browser only talks to the server. If a check fails, the request stops there.",
    "Datenbank und 7-Tage-Job": "Database and 7-Day Job",
    "PostgreSQL speichert Konten und App-Daten. Ein Hintergrund-Job erinnert Nutzer ohne Trade nach 7 Tagen.":
        "PostgreSQL stores accounts and app data. A background job reminds users with no trade after 7 days.",
    "Links die sechs Tabellen: vier legt Better Auth an, zwei gehören zur App. Rechts der zeitgesteuerte Job: "
    "BullMQ plant ihn bei der Registrierung, Redis hält ihn, der Worker zählt nach 7 Tagen die Trades "
    "und verschickt nur bei 0 Trades eine Erinnerung.":
        "Left: the six tables. Better Auth creates four, two belong to the app. Right: the timed job. "
        "BullMQ plans it at sign-up, Redis keeps it, after 7 days the worker counts the trades "
        "and sends a reminder only if there are 0.",
    "PostgreSQL · 6 Tabellen": "PostgreSQL · 6 tables",
    "Ein Eintrag pro Person": "One row per person", "Anzeigename": "display name", "eindeutig": "unique",
    "ja/nein": "yes/no", "7-Tage-Frist": "7-day timer",
    "Aktive Logins, eines pro Gerät": "Active logins, one per device", "steht im Cookie": "stored in the cookie",
    "Ablaufdatum": "expiry date",
    "Login-Methoden: Passwort oder z. B. Google": "Login methods: password or e.g. Google",
    "Login-Art": "login type", "nur als Hash": "hash only",
    "Codes für E-Mail-Bestätigung und Passwort-Reset": "Codes for email checks and password resets",
    "wofür": "purpose", "der Code": "the code", "läuft ab": "expires",
    "Angebote mit zwei Sichtbarkeitsstufen": "Offers with two levels of visibility",
    "öffentlich": "public", "nur\u00a0Mitglieder": "members\u00a0only",
    "Abgeschlossene Trades zwischen zwei Nutzern": "Finished trades between two users", "Abschluss": "finished at",
    "Primärschlüssel: eindeutige ID": "Primary key: unique ID",
    "Fremdschlüssel: verweist auf eine andere Tabelle": "Foreign key: points to another table",
    "Kein Zugriff aus dem Browser: nur die Stationen im Backend lesen und schreiben.":
        "No access from the browser: only the backend steps read and write.",
    "7-Tage-Job · zeitgesteuert, ohne Browser": "7-day job · on a timer, no browser",
    "Job einplanen": "Plan the job",
    "Bei der Registrierung legt der Next.js-Server einen Job an, fällig in 7 Tagen":
        "At sign-up, the Next.js server adds a job, due in 7\u00a0days",
    "Job-Speicher": "Job storage",
    "Bewahrt den Job auf, auch über einen Neustart des Servers": "Keeps the job, even when the server restarts",
    "Inaktivität prüfen": "Check inactivity",
    "Eigener Node.js-Prozess. Zählt die Trades; bei mehr als 0 endet der Job":
        "Its own Node.js process. Counts the trades; if more than 0, the job ends",
    "E-Mail bauen": "Build the email",
    "Vorlage als React-Komponente, gerendert zu HTML": "Template as a React component, turned into HTML",
    "Versand ins Postfach": "Delivery to the inbox",
    "Noch offen: z. B. Resend, Postmark oder Amazon SES": "Not chosen yet: e.g. Resend, Postmark or Amazon SES",
    "7 Tage Verzögerung": "7-day delay", "nach 7 Tagen fällig": "due after 7 days",
    "nur bei 0 Trades": "only if 0 trades", "fertige E-Mail": "finished email",
    "App-Architektur": "App Architecture",
}
MISSING = set()

# Farben aus style.css (:root, hell)
BG, SURFACE, LINE, INK = "F2F4F8", "FFFFFF", "D6DCE8", "121A2C"
S1, S2, S3, S4 = "2255D4", "0D7A54", "6A3FD0", "A25A00"  # Frontend, Sicherheit, Daten, Hintergrund
ON_INK = "E3E8F2"  # Nebentext auf dunklem Grund
SANS, MONO = "Arial", "Courier New"


def tint(hex_color, keep):
    """Mischt eine Farbe mit Weiß; keep = Anteil der Farbe (0..1)."""
    rgb = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(255 - (255 - c) * keep):02X}" for c in rgb)


def tr(s):
    """Deutsch bleibt; Englisch über EN, Leerzeichen am Rand bleiben erhalten."""
    core = s.strip()
    if LANG == "de" or not core:
        return s
    if core not in EN:
        MISSING.add(core)
        return s
    return s[:len(s) - len(s.lstrip())] + EN[core] + s[len(s.rstrip()):]


def rgb(h):
    return RGBColor.from_string(h)


def box(slide, x, y, w, h, fill, line=None, radius=0.09, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius / min(w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(0.75)
    else:
        s.line.fill.background()
    return s


def run(text, size=12, bold=False, color=INK, font=SANS):
    return dict(text=tr(text), size=size, bold=bold, color=color, font=font)


def text(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=0):
    """paras: Liste von Absätzen, jeder Absatz eine Liste von run()-Dicts."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if i:
            p.space_before = Pt(space)
        for r in runs:
            rr = p.add_run()
            rr.text = r["text"]
            f = rr.font
            f.size, f.bold, f.name = Pt(r["size"]), r["bold"], r["font"]
            f.color.rgb = rgb(r["color"])
    return tb


def arrow(slide, x1, y1, x2, y2, color, both=False, dashed=False, width=1.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    if dashed:
        etree.SubElement(ln, qn("a:prstDash")).set("val", "dash")
    ends = ["a:headEnd", "a:tailEnd"] if both else ["a:tailEnd"]
    for tag in ends:
        e = etree.SubElement(ln, qn(tag))
        e.set("type", "triangle")
        e.set("w", "med")
        e.set("h", "med")
    return c


def step(slide, x, y, n, color, d=0.34):
    c = box(slide, x, y, d, d, color, shape=MSO_SHAPE.OVAL)
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(n)
    r.font.size, r.font.bold, r.font.name = Pt(13), True, SANS
    r.font.color.rgb = rgb(SURFACE)


def zone(slide, x, y, w, label, color):
    text(slide, x, y, w, 0.25, [[run(label, 11, True, color)]])


def new_slide(prs, title, lead, notes):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(BG)
    text(s, 0.5, 0.4, 12.33, 0.55, [[run(title, 30, True)]])
    text(s, 0.5, 1.0, 12.33, 0.35, [[run(lead, 15)]])
    s.notes_slide.notes_text_frame.text = tr(notes)
    return s


def slide_request(prs):
    s = new_slide(
        prs,
        "App-Architektur: Tech-Stack und Weg einer Anfrage",
        "Eine Web-App mit Next.js und TypeScript. Jede Anfrage durchläuft fünf Stationen, bevor Daten fließen.",
        "Oben der Tech-Stack nach Oberbegriffen. Darunter der Weg einer Anfrage: Browser, fünf Stationen "
        "auf dem Next.js-Server, Datenbank. Unten, was Gast und Mitglied zurückbekommen.",
    )

    # Tech-Stack: Fundament (dunkel) + 4 Gruppen
    y, h = 1.62, 1.5
    fx, fw = 0.5, 4.1
    box(s, fx, y, fw, h, INK)
    base = [("Sprache", "TypeScript", "überall: Browser, Server, Worker"),
            ("Framework", "Next.js", "App Router, auf React-Basis"),
            ("Laufzeit", "Node.js", "führt Server und Worker aus")]
    cw = (fw - 0.3) / 3
    for i, (lab, name, desc) in enumerate(base):
        text(s, fx + 0.15 + i * cw, y + 0.14, cw - 0.12, h - 0.25,
             [[run(lab, 10.5, True, ON_INK)], [run(name, 16, True, SURFACE)], [run(desc, 11, False, ON_INK)]],
             space=2)
    groups = [("Benutzeroberfläche", S1, ["React", "Next.js App Router"]),
              ("Sicherheit", S2, ["Better Auth", "Zod", "Data Access Layer"]),
              ("Daten", S3, ["Prisma / Drizzle", "PostgreSQL"]),
              ("Hintergrund & E-Mail", S4, ["BullMQ", "Redis", "React Email", "Mail-Dienst"])]
    gap = 0.15
    gx, gw = fx + fw + gap, (12.833 - (fx + fw + gap) - 3 * gap) / 4
    for i, (lab, col, items) in enumerate(groups):
        x = gx + i * (gw + gap)
        box(s, x, y, gw, h, tint(col, 0.09))
        text(s, x + 0.15, y + 0.14, gw - 0.3, h - 0.25,
             [[run(lab, 11, True, col)]] + [[run(it, 12, True)] for it in items], space=3)

    # Weg einer Anfrage: Browser → 5 Stationen → Datenbank
    top, fh = 3.62, 2.15
    zone(s, 0.5, top - 0.32, 1.6, "Browser", S1)
    bw = 1.6
    ch = (fh - 0.15) / 2
    for i, (who, how) in enumerate([("Gast", "nicht registriert, ohne Cookie"),
                                     ("Mitglied", "eingeloggt, mit Session-Cookie")]):
        cy = top + i * (ch + 0.15)
        box(s, 0.5, cy, bw, ch, tint(S1, 0.1))
        text(s, 0.64, cy, bw - 0.28, ch, [[run(who, 14, True)], [run(how, 11)]], anchor=MSO_ANCHOR.MIDDLE, space=2)

    dbw = 1.55
    dbx = 12.833 - dbw
    sx = 0.5 + bw + 0.42
    sw = dbx - 0.42 - sx
    zone(s, sx, top - 0.32, sw, "Next.js-Server auf Node.js · für Besucher unsichtbar", S2)
    box(s, sx, top, sw, fh, tint(S2, 0.1))
    for i in range(2):
        cy = top + i * (ch + 0.15) + ch / 2
        arrow(s, 0.5 + bw + 0.04, cy, sx - 0.02, cy, S1)

    stations = [("Next.js App Router", "Einstiegspunkt", "Nimmt Seiten, Formulare und API-Aufrufe an"),
                ("Better Auth", "Authentifizierung", "Prüft Login und Session-Cookie: Gast oder Mitglied?"),
                ("Zod", "Validierung", "Prüft jede Eingabe gegen ein Schema"),
                ("Data Access Layer", "Autorisierung", "Gibt nur Felder frei, die die Rolle sehen darf"),
                ("Prisma / Drizzle", "ORM", "Baut sichere, typisierte SQL-Abfragen")]
    pad, ag = 0.12, 0.26
    stw = (sw - 2 * pad - 4 * ag) / 5
    sty, sth = top + pad, fh - 2 * pad
    for i, (name, role, desc) in enumerate(stations):
        x = sx + pad + i * (stw + ag)
        box(s, x, sty, stw, sth, SURFACE)
        step(s, x + 0.12, sty + 0.12, i + 1, S2)
        text(s, x + 0.12, sty + 0.56, stw - 0.22, sth - 0.62,
             [[run(role, 10.5, True, S2)], [run(name, 13.5, True)], [run(desc, 11)]], space=3)
        if i:
            arrow(s, x - ag + 0.03, sty + 0.29, x - 0.03, sty + 0.29, S2)

    zone(s, dbx, top - 0.32, dbw, "Datenbank", S3)
    box(s, dbx, top, dbw, fh, tint(S3, 0.1))
    text(s, dbx + 0.14, top + 0.14, dbw - 0.26, fh - 0.25,
         [[run("PostgreSQL", 14, True)], [run("Konten, Sitzungen, Angebote, Trades", 11)],
          [run("→ Folie 2", 11, True, S3)]], space=4)
    arrow(s, sx + sw - pad + 0.03, sty + 0.29, dbx - 0.03, sty + 0.29, S3, both=True)
    text(s, sx + sw + 0.02, sty + 0.36, 0.4, 0.3, [[run("SQL", 10, True, S3)]], align=PP_ALIGN.CENTER)

    # Antwort nach Rolle + Merksatz
    ry, rh = 6.0, 1.0
    rw = (12.333 - 2 * 0.2) / 3
    cards = [(tint(S1, 0.1), INK, "Antwort an den Gast",
              [run("Station 4 gibt nur "), run("previewText", 12, True, INK, MONO), run(" frei: öffentliche Vorschauen")]),
             (tint(S1, 0.1), INK, "Antwort an das Mitglied",
              [run("Zusätzlich "), run("memberDetails", 12, True, INK, MONO), run(": alle Details und Handel")]),
             (INK, SURFACE, "Merke",
              [run("Der Browser spricht nur mit dem Server. Scheitert eine Prüfung, endet die Anfrage dort.", 12, False, ON_INK)])]
    for i, (fill, ink, head, body) in enumerate(cards):
        x = 0.5 + i * (rw + 0.2)
        box(s, x, ry, rw, rh, fill)
        for r in body:
            r["size"] = 12
        text(s, x + 0.18, ry, rw - 0.36, rh, [[run(head, 13, True, ink)], body],
             anchor=MSO_ANCHOR.MIDDLE, space=3)


def slide_data_job(prs):
    s = new_slide(
        prs,
        "Datenbank und 7-Tage-Job",
        "PostgreSQL speichert Konten und App-Daten. Ein Hintergrund-Job erinnert Nutzer ohne Trade nach 7 Tagen.",
        "Links die sechs Tabellen: vier legt Better Auth an, zwei gehören zur App. Rechts der zeitgesteuerte Job: "
        "BullMQ plant ihn bei der Registrierung, Redis hält ihn, der Worker zählt nach 7 Tagen die Trades "
        "und verschickt nur bei 0 Trades eine Erinnerung.",
    )

    lx, lw = 0.5, 7.7
    zone(s, lx, 1.6, lw, "PostgreSQL · 6 Tabellen", S3)
    BA, APP = ("Better Auth", S2), ("App", S3)

    def col(name, *note):
        return [run(name, 10.5, True, INK, MONO)] + list(note)

    def tag(t, color=S3):
        return run(" " + t, 10.5, True, color)

    def note(t):
        return run(" " + t, 10.5)

    tables = [
        ("user", BA, "Ein Eintrag pro Person",
         [col("id", tag("PK")), col("name", note("Anzeigename")), col("email", note("eindeutig")),
          col("emailVerified", note("ja/nein")), col("createdAt", tag("7-Tage-Frist", S4))]),
        ("session", BA, "Aktive Logins, eines pro Gerät",
         [col("id", tag("PK")), col("userId", tag("FK"), note("→ user")), col("token", note("steht im Cookie")),
          col("expiresAt", note("Ablaufdatum"))]),
        ("account", BA, "Login-Methoden: Passwort oder z. B. Google",
         [col("id", tag("PK")), col("userId", tag("FK"), note("→ user")), col("providerId", note("Login-Art")),
          col("password", tag("nur als Hash", S4))]),
        ("verification", BA, "Codes für E-Mail-Bestätigung und Passwort-Reset",
         [col("id", tag("PK")), col("identifier", note("wofür")), col("value", note("der Code")),
          col("expiresAt", note("läuft ab"))]),
        ("listings", APP, "Angebote mit zwei Sichtbarkeitsstufen",
         [col("id", tag("PK")), col("ownerId", tag("FK"), note("→ user")), col("previewText", tag("öffentlich", S2)),
          col("memberDetails", tag("nur\u00a0Mitglieder", S4))]),
        ("trades", APP, "Abgeschlossene Trades zwischen zwei Nutzern",
         [col("id", tag("PK")), col("listingId", tag("FK"), note("→ listings")),
          col("sellerId", tag("FK"), note("→ user")), col("buyerId", tag("FK"), note("→ user")),
          col("completedAt", note("Abschluss"))]),
    ]
    tw, gap = (lw - 2 * 0.2) / 3, 0.2
    ty0, th = 1.95, 2.18
    for i, (name, (origin, ocol), desc, cols) in enumerate(tables):
        x, y = lx + (i % 3) * (tw + gap), ty0 + (i // 3) * (th + gap)
        box(s, x, y, tw, th, SURFACE, LINE)
        text(s, x + 0.16, y + 0.12, tw - 0.32, th - 0.2,
             [[run(origin, 10.5, True, ocol)], [run(name, 15, True, INK, MONO)], [run(desc, 11)]] + cols, space=3)

    ly = ty0 + 2 * th + gap + 0.17
    text(s, lx, ly, lw, 0.5, [[
        run("PK", 11, True, S3), run(" Primärschlüssel: eindeutige ID   ", 11),
        run("FK", 11, True, S3), run(" Fremdschlüssel: verweist auf eine andere Tabelle", 11)], [
        run("Kein Zugriff aus dem Browser: nur die Stationen im Backend lesen und schreiben.", 11)]], space=2)

    # 7-Tage-Job, senkrecht
    rx = lx + lw + 0.4
    rw = 12.833 - rx
    zone(s, rx, 1.6, rw, "7-Tage-Job · zeitgesteuert, ohne Browser", S4)
    steps = [("BullMQ Queue", "Job einplanen", "Bei der Registrierung legt der Next.js-Server einen Job an, fällig in 7 Tagen"),
             ("Redis", "Job-Speicher", "Bewahrt den Job auf, auch über einen Neustart des Servers"),
             ("BullMQ Worker", "Inaktivität prüfen", "Eigener Node.js-Prozess. Zählt die Trades; bei mehr als 0 endet der Job"),
             ("React Email", "E-Mail bauen", "Vorlage als React-Komponente, gerendert zu HTML"),
             ("Mail-Dienst", "Versand ins Postfach", "Noch offen: z. B. Resend, Postmark oder Amazon SES")]
    hops = ["7 Tage Verzögerung", "nach 7 Tagen fällig", "nur bei 0 Trades", "fertige E-Mail"]
    sy0, sh = 1.95, 0.8
    sgap = (ly + 0.5 - sy0 - 5 * sh) / 4
    for i, (name, role, desc) in enumerate(steps):
        y = sy0 + i * (sh + sgap)
        box(s, rx, y, rw, sh, tint(S4, 0.1))
        step(s, rx + 0.16, y + (sh - 0.34) / 2, i + 1, S4)
        text(s, rx + 0.66, y, rw - 0.8, sh,
             [[run(name, 13, True), run("  " + role, 11, True, S4)], [run(desc, 11)]],
             anchor=MSO_ANCHOR.MIDDLE, space=2)
        if i < 4:
            ax = rx + 0.33
            arrow(s, ax, y + sh + 0.03, ax, y + sh + sgap - 0.03, S4)
            text(s, ax + 0.2, y + sh, rw - 0.6, sgap, [[run(hops[i], 10.5, True, S4)]], anchor=MSO_ANCHOR.MIDDLE)

    # trades → Worker (gestrichelt: Worker liest die Anzahl der Trades)
    trades_y = ty0 + th + gap
    worker_y = sy0 + 2 * (sh + sgap)
    ay = (max(trades_y, worker_y) + min(trades_y + th, worker_y + sh)) / 2
    arrow(s, lx + lw + 0.04, ay, rx - 0.04, ay, S4, dashed=True)


def main():
    global LANG
    for LANG in ("de", "en"):
        prs = Presentation()
        prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)  # 16:9, 13,333 × 7,5 Zoll
        slide_request(prs)
        slide_data_job(prs)
        prs.core_properties.title = tr("App-Architektur")
        prs.core_properties.language = {"de": "de-DE", "en": "en-US"}[LANG]
        prs.save(OUT[LANG])
        print(OUT[LANG])
    print("ohne Übersetzung:", sorted(MISSING))


if __name__ == "__main__":
    main()
