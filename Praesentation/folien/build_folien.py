"""Erzeugt die 3 Folien (16:9) aus der Architektur-Seite Praesentation/index.html.

Ausgabe: App-Architektur.pptx (deutsch) und App-Architecture-EN.pptx (englisch);
PNGs (1920 × 1080) per LibreOffice:
    python build_folien.py            # braucht python-pptx, cairosvg, Pillow (Icons aus icons/)
    soffice --headless --convert-to pdf App-Architektur.pptx
    pdftoppm -png -scale-to-x 1920 -scale-to-y 1080 App-Architektur.pdf folie
Inhalt und Farben folgen index.html / style.css (helles Schema). Schrift Arial:
liegt in jedem PowerPoint und rendert in LibreOffice maßgleich (Liberation Sans).
"""
import io
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
    "Next.js + TypeScript. Jede Anfrage passiert fünf Stationen auf dem Server – erst dann fließen Daten.":
        "Next.js + TypeScript. Every request passes five steps on the server – only then does data move.",
    "Oben der Tech-Stack nach Oberbegriffen. Darunter der Weg einer Anfrage: Browser, fünf Stationen "
    "auf dem Next.js-Server, Datenbank. Unten, was Gast und Mitglied zurückbekommen.":
        "Top: the tech stack by group. Middle: the path of a request: browser, five steps on the Next.js "
        "server, database. Bottom: what guest and member get back.",
    "Sprache": "Language", "Laufzeit": "Runtime",
    "Browser, Server, Hintergrund-Jobs": "browser, server, background jobs",
    "Routing + API auf React": "routing + API on React",
    "Server und Hintergrund-Jobs": "server and background jobs",
    "Routing + API": "Routing + API", "Next.js Routing\u00a0+\u00a0API": "Next.js Routing\u00a0+\u00a0API",
    "Benutzeroberfläche": "User interface", "Sicherheit": "Security", "Daten": "Data",
    "Funktion:": "Function:", "Automatische E-Mails": "Automated emails", "Mail-Dienst": "Email service",
    "Gast": "Guest", "ohne Cookie": "no cookie", "Ohne": "Not", "Login": "logged in",
    "Standort": "Site", "+ Login": "+ logged in", "Frontend · Browser": "Frontend · browser",
    "mit Session-Cookie": "with session cookie",
    "Next.js-Server auf Node.js · für Besucher unsichtbar": "Next.js server on Node.js · hidden from visitors",
    "Einstiegspunkt": "Entry point", "Nimmt jede Anfrage an": "Takes every request",
    "Authentifizierung": "Authentication", "Wer fragt? Gast oder Mitglied": "Who asks? Guest or member",
    "Validierung": "Validation", "Ist die Eingabe gültig?": "Is the input valid?",
    "Autorisierung": "Authorization", "Was darf Gast oder Mitglied sehen?": "What may guest or member see?",
    "Baut sichere": "Builds safe", "SQL-Abfragen": "SQL queries",
    "Datenbank": "Database", "Standorte, Nutzer, Materialien, Angebote, Matches": "Sites, users, materials, offers, matches",
    "→ Folie 3": "→ slide 3",
    "Gast sieht": "Guest sees", "Mitglied sieht": "Member sees",
    "• Titel + Material": "• Title + material", "• Menge + Stadt": "• Quantity + city",
    "• Registrieren": "• Sign up", "• Login": "• Log in", "• E-Mail bestätigen": "• Confirm email",
    "• Passwort zurücksetzen,..": "• Reset password,..",
    "• + Preis + Beschreibung": "• + Price + description", "• + Kontakt": "• + Contact",
    "• Match anfragen": "• Request a match", "• Angebote einstellen": "• Post offers",
    "• Eigene Matches": "• Own matches", "• E-Mail-Erinnerung,..": "• Email reminder,..",
    "• Industriestandard": "• Industry standard", "• Sicherer Login + Rechte": "• Secure login + access",
    "• Zeitgesteuerte Jobs": "• Scheduled jobs", "• TypeScript überall": "• TypeScript everywhere",
    "• Typsichere Datenbank": "• Type-safe database", "• Erinnerungs-E-Mails,..": "• Reminder emails,..",
    "Datenbank und 7-Tage-Job": "Database and 7-Day Job",
    "PostgreSQL hält 5 Tabellen. Ein Hintergrund-Job erinnert nach 7 Tagen jeden Standort ohne Match.":
        "PostgreSQL holds 5 tables. A background job reminds every site without a match after 7 days.",
    "Links die fünf Tabellen nach dem UML-Datenmodell: Standorte (sites) mit genau einem Login (users), "
    "Materialkatalog, Angebote und Matches; Linien zeigen die Beziehungen. Rechts der zeitgesteuerte Job: "
    "BullMQ plant ihn bei der Registrierung, Redis hält ihn, der Worker zählt nach 7 Tagen die Matches "
    "und verschickt nur bei 0 Matches eine Erinnerung.":
        "Left: the five tables of the UML data model: sites with exactly one login (users), the material "
        "catalog, offers and matches; lines show the relations. Right: the timed job. BullMQ plans it at "
        "sign-up, Redis keeps it, after 7 days the worker counts the matches and sends a reminder only if there are 0.",
    "PostgreSQL · 5 Tabellen": "PostgreSQL · 5 tables",
    "Login eines Standorts": "Login of a site", "Betrieb mit Standort": "Business with its site",
    "Materialkatalog": "Material catalog", "Angebot eines Standorts": "Offer of a site",
    "Vom Mitglied angefragt": "Requested by a member",
    "eindeutig": "unique", "7-Tage-Frist": "7-day timer", "optional": "optional",
    "Mitglied": "Member",
    "Primärschlüssel": "primary key", "verweist auf Tabelle": "points to a table",
    "eins zu vielen": "one to many", "öffentlich sichtbar": "public", "nach Login": "after login",
    "Kein Zugriff aus dem Browser: nur das Backend liest und schreibt.":
        "No access from the browser: only the backend reads and writes.",
    "Zugang": "login", "ordnet ein": "classifies", "Vereinbarung": "agreement",
    "Verkäufer": "seller", "Käufer": "buyer",
    "Hintergrund-Job · 7 Tage, ohne Browser": "Background job · 7 days, no browser",
    "Job einplanen": "Plan the job",
    "Bei der Registrierung, Frist ab users.created_at": "At sign-up, timer from users.created_at",
    "Job-Speicher": "Job storage",
    "Hält den Job, auch über Neustarts": "Keeps the job, even across restarts",
    "Inaktivität prüfen": "Check inactivity",
    "Zählt Matches, ab\u00a01\u00a0Match endet der Job": "Counts matches, ends at the first match",
    "E-Mail bauen": "Build the email",
    "React-Komponente, gerendert zu HTML": "React component, turned into HTML",
    "Versand ins Postfach": "Delivery to the inbox",
    "Noch offen: z. B. Resend, Postmark oder Amazon SES": "Not chosen yet: e.g. Resend, Postmark or Amazon SES",
    "7 Tage verzögert": "7-day delay", "Job fällig": "job due",
    "nur bei 0 Matches": "only if 0 matches", "Erinnerungs-E-Mail": "reminder email",
    "Anzahl": "Match", "Matches": "count",
    "Software Architecture Stack: Was jeder Baustein tut": "Software Architecture Stack: What Each Building Block Does",
    "11 Bausteine zwischen Frontend und Datenbank – was sie tun und warum wir sie gewählt haben.":
        "11 building blocks between frontend and database – what they do and why we chose them.",
    "Oben das Backend: TypeScript, Next.js und Node.js tragen alles. Darunter zwei Ketten: jede Anfrage "
    "passiert Better Auth, Zod, Data Access Layer und Prisma/Drizzle; die automatischen E-Mails laufen über "
    "BullMQ, Redis, React Email und den Mail-Dienst. Links übergibt das Frontend (andere Gruppe), rechts "
    "geht es an die Datenbank (nächster Teil).":
        "Top: the backend. TypeScript, Next.js and Node.js carry everything. Below, two chains: every request "
        "passes Better Auth, Zod, Data Access Layer and Prisma/Drizzle; the automatic emails run through BullMQ, "
        "Redis, React Email and the email service. On the left the frontend hands over (other group), on the "
        "right it goes on to the database (next part).",
    "Funktion: Automatische E-Mails": "Function: Automated emails",
    "Backend": "Backend", "trägt alles": "carries everything", "Jede Anfrage": "Every request",
    "andere Gruppe": "other group", "nächster Teil": "next part", "React-Seiten": "React pages",
    "Frontend": "Frontend", "PostgreSQL": "PostgreSQL", "SQL": "SQL", "≈": "≈", "✓ Gewählt:": "✓ Chosen:",
    "Framework": "Framework", "ORM": "ORM",
    "Job-Warteschlange": "Job queue", "Job-Speicher": "Job storage", "E-Mail-Vorlage": "Email template",
    "Versand": "Delivery",
    "JavaScript mit Typen: Fehler zeigt schon der Editor.": "JavaScript with types: the editor shows errors early.",
    "Rechtschreibprüfung für Code": "spell checker for code",
    "eine Sprache für Browser, Server, Jobs": "one language for browser, server, jobs",
    "Liefert Seiten und API aus einem Projekt, auf React.": "Serves pages and API from one project, on React.",
    "Rezeption für alle Anfragen": "front desk for all requests", "Seiten + API in einem Repo": "pages + API in one repo",
    "Führt TypeScript auf dem Server aus.": "Runs TypeScript on the server.",
    "Motor, der den Code antreibt": "engine that drives the code",
    "gleiche Sprache wie im Browser": "same language as in the browser",
    "Login, Session-Cookie, Passwort-Reset.": "Login, session cookie, password reset.",
    "Ausweiskontrolle": "ID check at the door", "geprüft, Konten in unserer DB": "proven, accounts stay in our DB",
    "Prüft jede Eingabe gegen ein Schema.": "Checks every input against a schema.",
    "Türsteher mit Checkliste": "bouncer with a checklist", "Schema = Prüfung + Typ": "schema = check + type",
    "Jeder Datenzugriff läuft hier durch.": "Every data access passes through here.",
    "Akten nur mit Erlaubnis": "files only with permission", "Rechte an einer Stelle": "access rules in one place",
    "Übersetzt TypeScript in SQL-Abfragen.": "Turns TypeScript into SQL queries.",
    "Dolmetscher Code ↔ SQL": "interpreter code ↔ SQL", "typsicher, keine SQL-Injection": "type-safe, no SQL injection",
    "Plant Aufgaben für später, z. B. in 7 Tagen.": "Schedules tasks for later, e.g. in 7 days.",
    "Wecker für Aufgaben": "alarm clock for tasks", "wiederholt bei Fehlern": "retries on errors",
    "Schneller Speicher für geplante Jobs.": "Fast storage for scheduled jobs.",
    "Terminkalender der Jobs": "calendar of the jobs", "Jobs überleben Neustarts": "jobs survive restarts",
    "E-Mails als React-Komponenten, als HTML.": "Emails as React components, as HTML.",
    "Briefvorlage": "letter template", "gleiche Bausteine wie die App": "same building blocks as the app",
    "Stellt die E-Mail zuverlässig zu.": "Delivers the email reliably.",
    "die Post": "the postal service", "hohe Zustellrate, Anbieter offen": "high delivery rate, provider open",
    "App-Architektur": "App Architecture",
}
MISSING = set()

# Farben aus style.css (:root, hell)
BG, SURFACE, LINE, INK = "F2F4F8", "FFFFFF", "D6DCE8", "121A2C"
S1, S2, S3, S4 = "2255D4", "0D7A54", "6A3FD0", "A25A00"  # Frontend, Sicherheit, Daten, Hintergrund
ON_INK = "E3E8F2"  # Nebentext auf dunklem Grund
SANS, MONO = "Arial", "Courier New"
TOOL = "Verdana"  # Tools, Frameworks, Datenbank: klar erkennbar, in jedem PowerPoint vorhanden
ICONS = Path(__file__).with_name("icons")
_ICON_CACHE = {}


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


def slide_line(slide, x1, y1, x2, y2, color, width=1.5):
    """Gerade Linie ohne Spitzen (Beziehung zwischen Tabellen)."""
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width)
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
    r.font.size, r.font.bold, r.font.name = Pt(round(d * 38)), True, SANS
    r.font.color.rgb = rgb(SURFACE)


def icon(slide, name, x, y, size, color):
    """Lucide-Icon in Farbe als PNG (256 px) einsetzen."""
    key = (name, color)
    if key not in _ICON_CACHE:
        import cairosvg  # nur hier gebraucht
        svg = (ICONS / f"{name}.svg").read_text().replace("currentColor", "#" + color)
        _ICON_CACHE[key] = cairosvg.svg2png(bytestring=svg.encode(), output_width=256, output_height=256)
    return slide.shapes.add_picture(io.BytesIO(_ICON_CACHE[key]), Inches(x), Inches(y), Inches(size), Inches(size))


def label_width(label, size=11, bold=True):
    """Breite eines Arial-Texts in Zoll (Liberation Sans ist maßgleich)."""
    from PIL import ImageFont
    face = "Bold" if bold else "Regular"
    font = ImageFont.truetype(f"/usr/share/fonts/truetype/liberation2/LiberationSans-{face}.ttf", size * 10)
    return font.getlength(tr(label)) / 10 / 72


def zone(slide, x, y, w, label, color, ic=None):
    """Zonen-Titel (Icon + Text) mittig über der Grafik darunter."""
    tw = label_width(label) + 0.06
    gw = tw + (0.31 if ic else 0)
    x0 = x + (w - gw) / 2
    if ic:
        icon(slide, ic, x0, y - 0.01, 0.24, color)
        x0 += 0.31
    text(slide, x0, y, tw, 0.25, [[run(label, 11, True, color)]])


def new_slide(prs, title, lead, notes):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(BG)
    text(s, 0.5, 0.4, 12.33, 0.55, [[run(title, 30, True)]])
    text(s, 0.5, 1.0, 12.33, 0.35, [[run(lead, 15)]])
    s.notes_slide.notes_text_frame.text = tr(notes)
    return s


def lines(t, size, bold=False, color=INK, font=SANS):
    """Text mit festen Umbrüchen (\\n) als eigene Absätze; jede Zeile wird einzeln übersetzt."""
    return [[run(part, size, bold, color, font)] for part in t.split("\n")]


def slide_request(prs):
    s = new_slide(
        prs,
        "App-Architektur: Tech-Stack und Weg einer Anfrage",
        "Next.js + TypeScript. Jede Anfrage passiert fünf Stationen auf dem Server – erst dann fließen Daten.",
        "Oben der Tech-Stack nach Oberbegriffen. Darunter der Weg einer Anfrage: Browser, fünf Stationen "
        "auf dem Next.js-Server, Datenbank. Unten, was Gast und Mitglied zurückbekommen.",
    )
    C, M = PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE

    # Tech-Stack: 3 Fundament-Karten (dunkel) + 4 Gruppen, alles mittig
    # Reihe mittig zwischen Untertitel und Zonen-Titeln des Anfrage-Wegs: oben = unten
    top = 3.8  # Oberkante des Anfrage-Wegs (Zonen-Titel 0,31 darüber)
    lead_bottom, flow_head = 1.26, top - 0.31
    h = 1.62
    y = lead_bottom + (flow_head - lead_bottom - h) / 2
    fx, fw, bg = 0.5, 4.1, 0.12
    bw3 = (fw - 2 * bg) / 3
    base = [("file-code", "Sprache", "TypeScript", "Browser, Server, Hintergrund-Jobs"),
            ("layers", "Framework", "Next.js", "Routing + API auf React"),
            ("cpu", "Laufzeit", "Node.js", "Server und Hintergrund-Jobs")]
    for i, (ic, lab, name, desc) in enumerate(base):
        x = fx + i * (bw3 + bg)
        box(s, x, y, bw3, h, INK)
        icon(s, ic, x + (bw3 - 0.26) / 2, y + 0.16, 0.26, SURFACE)
        text(s, x, y + 0.52, bw3, 0.2, [[run(lab, 10, True, ON_INK)]], align=C)
        text(s, x, y + 0.71, bw3, 0.3, [[run(name, 12, True, SURFACE, TOOL)]], align=C, anchor=M)
        text(s, x + 0.08, y + 1.03, bw3 - 0.16, 0.42, [[run(desc, 10, False, ON_INK)]], align=C)
    groups = [("monitor", "Benutzeroberfläche", S1, ["React", "Next.js Routing\u00a0+\u00a0API"]),
              ("shield-check", "Sicherheit", S2, ["Better Auth", "Zod", "Data Access Layer"]),
              ("database", "Daten", S3, ["Prisma / Drizzle", "PostgreSQL"]),
              ("mail", "Funktion:\nAutomatische E-Mails", S4, ["BullMQ", "Redis", "React Email", "Mail-Dienst"])]
    gap = 0.15
    gx, gw = fx + fw + gap, (12.833 - (fx + fw + gap) - 3 * gap) / 4
    for i, (ic, lab, col, items) in enumerate(groups):
        x = gx + i * (gw + gap)
        box(s, x, y, gw, h, tint(col, 0.1))
        edge = box(s, x, y, gw, 0.07, col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)  # Farbkante = Gruppe
        edge.adjustments[0] = 0.5
        icon(s, ic, x + (gw - 0.24) / 2, y + 0.13, 0.24, col)
        text(s, x + 0.08, y + 0.4, gw - 0.16, h - 0.42,  # Titel mit \n = fester Umbruch
             [[run(t, 10, True, col)] for t in lab.split("\n")] + [[run(it, 10, True, INK, TOOL)] for it in items],
             align=C, space=1)

    # Weg einer Anfrage: Datenbank ← 5 Stationen ← Browser (Frontend rechts, Datenbank links)
    fh = 2.2
    bw, dbw = 1.6, 1.55
    ch = (fh - 0.15) / 2
    dbx, fex = 0.5, 12.833 - bw
    sx = dbx + dbw + 0.42
    sw = fex - 0.42 - sx
    mid = top + fh / 2  # Pfeil + Label gemeinsam auf der senkrechten Mitte von Server und Datenbank
    card_mid = [top + i * (ch + 0.15) + ch / 2 for i in range(2)]

    # Spalten Datenbank | Server | Frontend: dezente gestrichelte Linien mittig in den Lücken,
    # zuerst gezeichnet (liegen hinten) und dort unterbrochen, wo Pfeile oder „SQL“ kreuzen
    def divider(x, holes):
        y0 = top - 0.34
        for a, b in sorted(holes) + [(top + fh, top + fh)]:
            c = slide_line(s, x, y0, x, a, tint(INK, 0.28), width=1)
            etree.SubElement(c.line._get_or_add_ln(), qn("a:prstDash")).set("val", "dash")
            y0 = b
    divider(dbx + dbw + 0.21, [(mid - 0.26, mid + 0.22)])
    divider(sx + sw + 0.21, [(m - 0.14, m + 0.14) for m in card_mid])

    zone(s, fex, top - 0.3, bw, "Frontend · Browser", S1, "monitor")
    people = [("user", "Gast", "ohne Cookie", "Ohne\nLogin"),
              ("user-check", "Mitglied", "mit Session-Cookie", "Standort\n+ Login")]
    for i, (ic, who, how, state) in enumerate(people):
        cy = top + i * (ch + 0.15)
        # Kontostand senkrecht rechts neben der Karte (Textfeld um 270° gedreht, Mitte bleibt)
        vh = 0.38
        tb = text(s, fex + bw + 0.21 - ch / 2, cy + ch / 2 - vh / 2, ch, vh, lines(state, 10, True, S1),
                  align=C, anchor=M)
        tb.rotation = 270
        box(s, fex, cy, bw, ch, tint(S1, 0.1))
        icon(s, ic, fex + (bw - 0.28) / 2, cy + 0.12, 0.28, S1)
        text(s, fex + 0.05, cy + 0.44, bw - 0.1, ch - 0.48, [[run(who, 14, True)], [run(how, 11)]], align=C, space=1)

    zone(s, sx, top - 0.3, sw, "Next.js-Server auf Node.js · für Besucher unsichtbar", S2, "server")
    box(s, sx, top, sw, fh, tint(S2, 0.1))
    for m in card_mid:
        arrow(s, fex - 0.04, m, sx + sw + 0.02, m, S1, width=2.5)

    stations = [("log-in", "Next.js\nRouting + API", "Einstiegspunkt", "Nimmt jede Anfrage an"),
                ("key-round", "Better Auth", "Authentifizierung", "Wer fragt? Gast oder Mitglied"),
                ("list-checks", "Zod", "Validierung", "Ist die Eingabe gültig?"),
                ("eye", "Data Access Layer", "Autorisierung", "Was darf Gast oder Mitglied sehen?"),
                ("database", "Prisma / Drizzle", "ORM", "Baut sichere\nSQL-Abfragen")]
    pad, ag, d = 0.12, 0.26, 0.4
    stw = (sw - 2 * pad - 4 * ag) / 5
    sty, sth = top + pad, fh - 2 * pad
    my = sty + 0.14 + d / 2  # Mittellinie von Icon und Nummer
    for i, (ic, name, role, desc) in enumerate(stations):
        x = sx + pad + (4 - i) * (stw + ag)  # Station 1 rechts am Browser, Station 5 links an der Datenbank
        box(s, x, sty, stw, sth, SURFACE)
        icon(s, ic, x + stw / 2 - 0.42, my - 0.16, 0.32, S2)  # Icon links, Nummer rechts
        step(s, x + stw / 2 + 0.06, sty + 0.14, i + 1, S2, d=d)
        text(s, x + 0.04, sty + 0.6, stw - 0.08, 0.22, [[run(role, 10.5, True, S2)]], align=C)
        text(s, x + 0.04, sty + 0.82, stw - 0.08, 0.46, lines(name, 12, True, INK, TOOL), align=C, anchor=M)
        text(s, x + 0.06, sty + 1.32, stw - 0.12, 0.6, lines(desc, 11), align=C)
        if i:  # Pfeil von der vorigen Station (rechts) nach links, senkrecht mittig zur Karte
            arrow(s, x + stw + ag - 0.03, sty + sth / 2, x + stw + 0.03, sty + sth / 2, S2, width=2.5)

    zone(s, dbx, top - 0.3, dbw, "Datenbank", S3, "database")
    db = box(s, dbx, top, dbw, fh, tint(S3, 0.12), S3, shape=MSO_SHAPE.CAN)
    db.adjustments[0] = 0.14
    db.line.width = Pt(1.25)
    text(s, dbx + 0.1, top + 0.3, dbw - 0.2, fh - 0.4,
         [[run("PostgreSQL", 13, True, INK, TOOL)], [run("Standorte, Nutzer, Materialien, Angebote, Matches", 11)],
          [run("→ Folie 3", 11, True, S3)]], align=C, anchor=M, space=4)
    arrow(s, dbx + dbw + 0.03, mid - 0.12, sx - 0.03, mid - 0.12, S3, both=True, width=2.5)
    text(s, dbx + dbw - 0.02, mid - 0.04, 0.46, 0.22, [[run("SQL", 10.5, True, S3)]], align=C)

    # Antwort nach Rolle + Merksatz: Icon links, Text mittig daneben
    ry, rh = 6.16, 1.06
    rw = (12.333 - 2 * 0.2) / 3
    def bullets(x, y, w, cols, color, size=10.5):
        """Stichpunkte in 2 Spalten, linksbündig; linke Spalte so breit wie ihr längster Punkt."""
        c1 = max(label_width("• " + t, size, bold=False) for t in cols[0]) + 0.22
        for j, items in enumerate(cols):
            cx, cw = (x, c1) if j == 0 else (x + c1, w - c1)
            text(s, cx, y, cw, rh - 0.4, [[run("• " + t, size, False, color)] for t in items], space=1)

    # Gast / Mitglied als Browserfenster: Titelleiste mit Punkten + Adresszeile, darunter die Seite
    windows = [("eye", "Gast sieht", "/offers",
                [["Titel + Material", "Menge + Stadt", "Registrieren"],
                 ["Login", "E-Mail bestätigen", "Passwort zurücksetzen,.."]]),
               ("lock-open", "Mitglied sieht", "/offers/[id]",
                [["+ Preis + Beschreibung", "+ Kontakt", "Match anfragen"],
                 ["Angebote einstellen", "Eigene Matches", "E-Mail-Erinnerung,.."]])]
    bar = 0.3
    for i, (ic, head, field, cols) in enumerate(windows):
        x = 0.5 + i * (rw + 0.2)
        frame = box(s, x, ry, rw, rh, SURFACE, tint(S1, 0.45))
        frame.line.width = Pt(1.25)
        top_bar = box(s, x, ry, rw, bar, tint(S1, 0.14), shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
        top_bar.adjustments[0] = 0.09 / bar
        for k in range(3):
            box(s, x + 0.14 + k * 0.13, ry + (bar - 0.08) / 2, 0.08, 0.08, tint(S1, 0.45), shape=MSO_SHAPE.OVAL)
        url = box(s, x + 0.58, ry + 0.05, rw - 1.06, bar - 0.1, SURFACE, radius=0.1)
        url.line.fill.background()
        text(s, x + 0.7, ry + 0.05, rw - 1.2, bar - 0.1,
             [[run(head, 10.5, True), run("  ·  ", 10.5, True, S1), run(field, 10, True, INK, MONO)]], anchor=M)
        icon(s, ic, x + rw - 0.36, ry + 0.05, 0.2, S1)
        bullets(x + 0.2, ry + bar + 0.08, rw - 0.3, cols, INK)

    # Benefits: Kopf mit Icon, darunter 2 Spalten Stichpunkte, linksbündig
    x = 0.5 + 2 * (rw + 0.2)
    box(s, x, ry, rw, rh, INK)
    hw = label_width("Benefits", 13.5) + 0.06
    text(s, x + 0.22, ry + 0.06, hw, 0.28, [[run("Benefits", 13.5, True, SURFACE)]], anchor=M)
    icon(s, "badge-check", x + 0.22 + hw + 0.08, ry + 0.07, 0.26, ON_INK)  # Icon rechts neben dem Titel
    benefits = [["Industriestandard", "Sicherer Login + Rechte", "Zeitgesteuerte Jobs"],
                ["TypeScript überall", "Typsichere Datenbank", "Erinnerungs-E-Mails,.."]]
    bullets(x + 0.22, ry + 0.44, rw - 0.32, benefits, ON_INK)  # oben = unten, Luft unter dem Titel


# Folie 2: die 11 Bausteine des Stacks, je Karte Rolle, Name, was er tut, Alltagsvergleich, Grund der Wahl
STACK = {  # Schlüssel: (Name, Rolle, Icon, Farbe, was er tut, Alltagsvergleich, gewählt weil)
    "ts": ("TypeScript", "Sprache", "file-code", INK, "JavaScript mit Typen: Fehler zeigt schon der Editor.",
           "Rechtschreibprüfung für Code", "eine Sprache für Browser, Server, Jobs"),
    "next": ("Next.js", "Framework", "layers", INK, "Liefert Seiten und API aus einem Projekt, auf React.",
             "Rezeption für alle Anfragen", "Seiten + API in einem Repo"),
    "node": ("Node.js", "Laufzeit", "cpu", INK, "Führt TypeScript auf dem Server aus.",
             "Motor, der den Code antreibt", "gleiche Sprache wie im Browser"),
    "auth": ("Better Auth", "Authentifizierung", "key-round", S2, "Login, Session-Cookie, Passwort-Reset.",
             "Ausweiskontrolle", "geprüft, Konten in unserer DB"),
    "zod": ("Zod", "Validierung", "list-checks", S2, "Prüft jede Eingabe gegen ein Schema.",
            "Türsteher mit Checkliste", "Schema = Prüfung + Typ"),
    "dal": ("Data Access Layer", "Autorisierung", "eye", S2, "Jeder Datenzugriff läuft hier durch.",
            "Akten nur mit Erlaubnis", "Rechte an einer Stelle"),
    "orm": ("Prisma / Drizzle", "ORM", "database", S3, "Übersetzt TypeScript in SQL-Abfragen.",
            "Dolmetscher Code ↔ SQL", "typsicher, keine SQL-Injection"),
    "bull": ("BullMQ", "Job-Warteschlange", "clock", S4, "Plant Aufgaben für später, z. B. in 7 Tagen.",
             "Wecker für Aufgaben", "wiederholt bei Fehlern"),
    "redis": ("Redis", "Job-Speicher", "hard-drive", S4, "Schneller Speicher für geplante Jobs.",
              "Terminkalender der Jobs", "Jobs überleben Neustarts"),
    "remail": ("React Email", "E-Mail-Vorlage", "mail", S4, "E-Mails als React-Komponenten, als HTML.",
               "Briefvorlage", "gleiche Bausteine wie die App"),
    "mail": ("Mail-Dienst", "Versand", "send", S4, "Stellt die E-Mail zuverlässig zu.",
             "die Post", "hohe Zustellrate, Anbieter offen"),
}


def fit_size(label, width, sizes=(12, 11.5, 11, 10.5)):
    """Größte Schriftgröße, bei der ein Tool-Name (Verdana, gerendert als DejaVu Sans) in eine Zeile passt."""
    from PIL import ImageFont
    for size in sizes:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size * 10)
        if font.getlength(tr(label)) / 10 / 72 <= width:
            return size
    return sizes[-1]


def stack_card(s, x, y, w, h, key):
    """Karte: Icon + Rolle + Name oben, darunter ein Textfluss (was · Vergleich · Grund) – nichts überlappt."""
    name, role, ic, col, what, like, why = STACK[key]
    p, nx = 0.12, 0.56
    box(s, x, y, w, h, tint(col, 0.1))
    icon(s, ic, x + p, y + 0.13, 0.34, col)
    text(s, x + nx, y + 0.08, w - nx - 0.06, 0.2, [[run(role, 10, True, col)]])
    text(s, x + nx, y + 0.28, w - nx - 0.06, 0.28,
         [[run(name, fit_size(name, w - nx - 0.1), True, INK, TOOL)]])
    text(s, x + p, y + 0.66, w - 2 * p, h - 0.74, [
        [run(what, 10.5)],
        [run("≈ ", 10.5, True, col), run(like, 10.5, True, col)],
        [run("✓ Gewählt:", 10, True, col), run(" " + why, 10)]], space=3)


def handover(s, x, y, w, h, ic, head, who, what, col):
    """Gestrichelte Leiste: Teil, den eine andere Person vorstellt."""
    r = box(s, x, y, w, h, tint(col, 0.08), tint(col, 0.45))
    r.line.dash_style = 4
    icon(s, ic, x + (w - 0.32) / 2, y + h / 2 - 0.9, 0.32, col)
    text(s, x + 0.03, y + h / 2 - 0.5, w - 0.06, 1.4,
         [[run(head, 11, True, col)], [run(who, 10)], [run(what, 10.5, True, INK, TOOL)]], align=PP_ALIGN.CENTER, space=4)


def slide_stack(prs):
    s = new_slide(
        prs,
        "Software Architecture Stack: Was jeder Baustein tut",
        "11 Bausteine zwischen Frontend und Datenbank – was sie tun und warum wir sie gewählt haben.",
        "Oben das Backend: TypeScript, Next.js und Node.js tragen alles. Darunter zwei Ketten: jede Anfrage "
        "passiert Better Auth, Zod, Data Access Layer und Prisma/Drizzle; die automatischen E-Mails laufen über "
        "BullMQ, Redis, React Email und den Mail-Dienst. Links übergibt das Frontend (andere Gruppe), rechts "
        "geht es an die Datenbank (nächster Teil).",
    )
    C, M = PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE
    y0, y1, rw, rg = 1.55, 7.2, 1.05, 0.34
    handover(s, 0.5, y0, rw, y1 - y0, "monitor", "Frontend", "andere Gruppe", "React-Seiten", S1)
    dbx = 12.833 - rw
    handover(s, dbx, y0, rw, y1 - y0, "database", "Datenbank", "nächster Teil", "PostgreSQL", S3)
    x0, x1 = 0.5 + rw + rg, dbx - rg
    sw = x1 - x0

    # Backend-Band oben: Sprache, Framework, Laufzeit tragen beide Ketten
    bh = 1.2
    box(s, x0, y0, sw, bh, INK)
    lw = 1.25
    icon(s, "server", x0 + (lw - 0.32) / 2, y0 + 0.2, 0.32, SURFACE)
    text(s, x0, y0 + 0.58, lw, 0.5, [[run("Backend", 13, True, SURFACE)], [run("trägt alles", 10, False, ON_INK)]],
         align=C, space=1)
    iw = (sw - lw - 0.1) / 3
    for j, key in enumerate(["ts", "next", "node"]):
        name, role, ic, _, what, like, why = STACK[key]
        x = x0 + lw + j * iw
        icon(s, ic, x + 0.04, y0 + 0.16, 0.3, SURFACE)
        text(s, x + 0.44, y0 + 0.08, iw - 0.5, 0.2, [[run(role, 10, True, ON_INK)]])
        text(s, x + 0.44, y0 + 0.26, iw - 0.5, 0.26, [[run(name, 12, True, SURFACE, TOOL)]])
        text(s, x + 0.04, y0 + 0.6, iw - 0.12, bh - 0.66, [
            [run("≈ ", 10.5, True, ON_INK), run(like, 10.5, True, ON_INK)],
            [run("✓ Gewählt:", 10, True, ON_INK), run(" " + why, 10, False, SURFACE)]], space=2)

    # Zwei Ketten mit Pfeilen: jede Anfrage · automatische E-Mails
    ag, zg = 0.26, 0.36
    cw = (sw - 3 * ag) / 4
    top = y0 + bh + zg
    rh = (y1 - top - zg) / 2
    rows = [("Jede Anfrage", S2, ["auth", "zod", "dal", "orm"], "shield-check"),
            ("Funktion: Automatische E-Mails", S4, ["bull", "redis", "remail", "mail"], "mail")]
    mids = []
    for i, (lab, col, keys, ic) in enumerate(rows):
        y = top + i * (rh + zg)
        zone(s, x0, y - 0.3, sw, lab, col, ic)
        for j, key in enumerate(keys):
            x = x0 + j * (cw + ag)
            stack_card(s, x, y, cw, rh, key)
            if j:
                arrow(s, x - ag + 0.03, y + rh / 2, x - 0.03, y + rh / 2, col, width=2.5)
        mids.append(y + rh / 2)

    # Übergaben: Frontend → erste Karte, ORM ↔ Datenbank (SQL)
    arrow(s, 0.5 + rw + 0.03, mids[0], x0 - 0.03, mids[0], S1, width=2.5)
    arrow(s, x1 + 0.03, mids[0], dbx - 0.03, mids[0], S3, both=True, width=2.5)
    text(s, x1 - 0.06, mids[0] - 0.3, rg + 0.12, 0.22, [[run("SQL", 10.5, True, S3)]], align=C)


def slide_data_job(prs):
    s = new_slide(
        prs,
        "Datenbank und 7-Tage-Job",
        "PostgreSQL hält 5 Tabellen. Ein Hintergrund-Job erinnert nach 7 Tagen jeden Standort ohne Match.",
        "Links die fünf Tabellen nach dem UML-Datenmodell: Standorte (sites) mit genau einem Login (users), "
        "Materialkatalog, Angebote und Matches; Linien zeigen die Beziehungen. Rechts der zeitgesteuerte Job: "
        "BullMQ plant ihn bei der Registrierung, Redis hält ihn, der Worker zählt nach 7 Tagen die Matches "
        "und verschickt nur bei 0 Matches eine Erinnerung.",
    )
    C, M, R = PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, PP_ALIGN.RIGHT
    FS = 9  # Feldzeilen

    def col(name, *rest):
        return [run(name, FS, True, INK, MONO)] + list(rest)

    def tag(t, color=S3):
        return run(" " + t, FS, True, color)

    def note(t):
        return run(" " + t, FS)

    def fk(target):
        return [tag("FK"), note("→ " + target)]

    GUEST, MEMBER = (lambda: tag("Gast", S2)), (lambda: tag("Mitglied", S4))

    # Raster: 3 Spalten × 2 Reihen, rechts daneben der Job; breite Lücke für den Pfeil „Anzahl Matches“
    rw = 4.1
    rx = 12.833 - rw
    W, G = [1.85, 2.2, 2.0], [0.66, 0.9]
    X = [0.5, 0.5 + W[0] + G[0], 0.5 + W[0] + G[0] + W[1] + G[1]]
    lw = X[2] + W[2] - 0.5
    Y, H = [1.95, 4.75], [2.1, 2.5]
    zone(s, 0.5, 1.6, lw, "PostgreSQL · 5 Tabellen", S3, "database")

    tables = {
        "users": (0, 0, "Login eines Standorts",
                  [col("id", tag("PK")), col("site_id", *fk("sites")), col("email", note("eindeutig")),
                   col("password_hash"), col("account_status"), col("created_at", tag("7-Tage-Frist", S4))]),
        "sites": (1, 0, "Betrieb mit Standort",
                  [col("id", tag("PK")), col("business_name"), col("branch_name"), col("city", GUEST()),
                   col("latitude, longitude"), col("contact_email,..", MEMBER())]),
        "materials": (0, 1, "Materialkatalog",
                      [col("id", tag("PK")), col("code", note("eindeutig")), col("name", GUEST()),
                       col("category"), col("impact_factor_*", note("optional"))]),
        "offers": (1, 1, "Angebot eines Standorts",
                   [col("id", tag("PK")), col("seller_site_id", *fk("sites")),
                    col("material_id", *fk("materials")), col("title", GUEST()),
                    col("available_quantity_kg", GUEST()), col("price_eur_per_kg", MEMBER()),
                    col("description", MEMBER()), col("status,..")]),
        "matches": (2, 1, "Vom Mitglied angefragt",
                    [col("id", tag("PK")), col("offer_id", *fk("offers")), col("buyer_site_id", *fk("sites")),
                     col("agreed_quantity_kg"), col("agreed_price_eur_per_kg"), col("status"),
                     col("completed_at", note("optional")), col("actual_quantity_kg,..")]),
    }
    hh = 0.62
    for name, (c, r, desc, cols) in tables.items():
        x, y, w, h = X[c], Y[r], W[c], H[r]
        box(s, x, y, w, h, SURFACE, LINE)
        head = box(s, x, y, w, hh, tint(S3, 0.14), shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
        head.adjustments[0] = 0.09 / hh
        text(s, x + 0.08, y, w - 0.16, hh, [[run(name, 14, True, INK, MONO)], [run(desc, 10, True, S3)]],
             align=C, anchor=M, space=1)
        text(s, x + 0.12, y + hh + 0.1, w - 0.2, h - hh - 0.15, cols, space=2)

    # Legende oben rechts
    lx_, ly_ = X[2], Y[0]
    box(s, lx_, ly_, W[2], H[0], tint(S3, 0.06), LINE)
    text(s, lx_ + 0.14, ly_ + 0.12, W[2] - 0.24, H[0] - 0.2, [
        [run("PK", 10, True, S3), run(" Primärschlüssel", 10)],
        [run("FK", 10, True, S3), run(" verweist auf Tabelle", 10)],
        [run("1:n", 10, True, S3), run(" eins zu vielen", 10)],
        [run("Gast", 10, True, S2), run(" öffentlich sichtbar", 10)],
        [run("Mitglied", 10, True, S4), run(" nach Login", 10)],
        [run("Kein Zugriff aus dem Browser: nur das Backend liest und schreibt.", 10)]], space=3)

    def link(x1, y1, x2, y2):
        c = slide_line(s, x1, y1, x2, y2, S3)
        return c

    def hlabel(x1, x2, y, card, role):
        """Kardinalität über, Rolle unter einer waagerechten Linie."""
        text(s, x1, y - 0.25, x2 - x1, 0.22, [[run(card, 10, True, S3)]], align=C)
        text(s, x1, y + 0.04, x2 - x1, 0.22, [[run(role, 9, True, S3)]], align=C)

    # users 1:1 sites · materials 1:n offers · offers 1:n matches (waagerecht)
    for (c, r, card, role) in [(0, 0, "1:1", "Zugang"), (0, 1, "1:n", "ordnet ein"), (1, 1, "1:n", "Vereinbarung")]:
        x1, x2, y = X[c] + W[c], X[c + 1], Y[r] + (0.95 if r == 0 else 1.1)
        link(x1, y, x2, y)
        hlabel(x1, x2, y, card, role)
    # sites 1:n offers (senkrecht) · sites 1:n matches (Winkel durch die Lücke zwischen den Reihen)
    gy0, gy1 = Y[0] + H[0], Y[1]
    vx = X[1] + 0.5 * W[1]
    link(vx, gy0, vx, gy1)
    text(s, X[1], gy0 + 0.08, vx - X[1] - 0.08, gy1 - gy0 - 0.16,
         [[run("1:n", 10, True, S3), run(" Verkäufer", 9.5, True, S3)]], align=R, anchor=M)
    ex, my, tx = X[1] + 0.85 * W[1], (gy0 + gy1) / 2, X[2] + W[2] / 2
    link(ex, gy0, ex, my)
    link(ex, my, tx, my)
    link(tx, my, tx, gy1)
    text(s, ex + 0.1, my - 0.26, tx - ex - 0.2, 0.22,
         [[run("1:n", 10, True, S3), run(" Käufer", 9.5, True, S3)]], align=C)

    # 7-Tage-Job, senkrecht
    zone(s, rx, 1.6, rw, "Hintergrund-Job · 7 Tage, ohne Browser", S4, "clock")
    icons = ["clock", "hard-drive", "search", "mail", "send"]
    steps = [("BullMQ Queue", "Job einplanen", "Bei der Registrierung, Frist ab users.created_at"),
             ("Redis", "Job-Speicher", "Hält den Job, auch über Neustarts"),
             ("BullMQ Worker", "Inaktivität prüfen", "Zählt Matches, ab\u00a01\u00a0Match endet der Job"),
             ("React Email", "E-Mail bauen", "React-Komponente, gerendert zu HTML"),
             ("Mail-Dienst", "Versand ins Postfach", "Noch offen: z. B. Resend, Postmark oder Amazon SES")]
    hops = ["7 Tage verzögert", "Job fällig", "nur bei 0 Matches", "Erinnerungs-E-Mail"]
    sy0, sh, d = 1.95, 0.8, 0.4
    sgap = (Y[1] + H[1] - sy0 - 5 * sh) / 4
    ax = rx + 0.16 + d / 2
    for i, (name, role, desc) in enumerate(steps):
        y = sy0 + i * (sh + sgap)
        box(s, rx, y, rw, sh, tint(S4, 0.1))
        step(s, rx + 0.16, y + (sh - d) / 2, i + 1, S4, d=d)
        icon(s, icons[i], rx + rw - 0.44, y + (sh - 0.3) / 2, 0.3, S4)
        text(s, rx + 0.68, y, rw - 1.18, sh,
             [[run(name, 12, True, INK, TOOL), run("  " + role, 11, True, S4)], [run(desc, 11)]],
             anchor=M, space=2)
        if i < 4:
            arrow(s, ax, y + sh + 0.03, ax, y + sh + sgap - 0.03, S4, width=2.5)
            text(s, ax + 0.2, y + sh, rw - 0.6, sgap, [[run(hops[i], 11, True, S4)]], anchor=M)

    # matches → Worker (gestrichelt: der Worker liest die Anzahl der Matches)
    worker_y = sy0 + 2 * (sh + sgap)
    ay = (max(Y[1], worker_y) + min(Y[1] + H[1], worker_y + sh)) / 2
    x1, x2 = X[2] + W[2], rx
    arrow(s, x1 + 0.04, ay, x2 - 0.04, ay, S4, dashed=True, width=2.25)
    text(s, x1, ay - 0.5, x2 - x1, 0.44, lines("Anzahl\nMatches", 10, True, S4), align=C, anchor=MSO_ANCHOR.BOTTOM)


def main():
    global LANG
    for LANG in ("de", "en"):
        prs = Presentation()
        prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)  # 16:9, 13,333 × 7,5 Zoll
        slide_request(prs)
        slide_stack(prs)
        slide_data_job(prs)
        prs.core_properties.title = tr("App-Architektur")
        prs.core_properties.language = {"de": "de-DE", "en": "en-US"}[LANG]
        prs.save(OUT[LANG])
        print(OUT[LANG])
    print("ohne Übersetzung:", sorted(MISSING))


if __name__ == "__main__":
    main()
