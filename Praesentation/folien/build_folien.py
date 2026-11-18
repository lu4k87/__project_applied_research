"""Erzeugt die 2 Folien (16:9) aus der Architektur-Seite Praesentation/index.html.

Ausgabe: App-Architektur.pptx (deutsch) und App-Architecture-EN.pptx (englisch);
PNGs (1920 × 1080) per LibreOffice:
    python build_folien.py            # braucht python-pptx + cairosvg (Icons aus icons/)
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
    "Hintergrund & E-Mail": "Background & email", "Mail-Dienst": "Email service",
    "Gast": "Guest", "ohne Login": "not logged in",
    "Mitglied": "Member", "mit Session-Cookie": "with session cookie",
    "Next.js-Server auf Node.js · für Besucher unsichtbar": "Next.js server on Node.js · hidden from visitors",
    "Einstiegspunkt": "Entry point", "Nimmt jede Anfrage an": "Takes every request",
    "Authentifizierung": "Authentication", "Wer fragt? Gast oder Mitglied": "Who asks? Guest or member",
    "Validierung": "Validation", "Ist die Eingabe gültig?": "Is the input valid?",
    "Autorisierung": "Authorization", "Was darf diese Rolle (User) sehen?": "What may this role (user) see?",
    "Baut sichere": "Builds safe", "SQL-Abfragen": "SQL queries",
    "Datenbank": "Database", "Konten, Logins, Angebote, Trades": "Accounts, logins, offers, trades",
    "→ Folie 2": "→ slide 2",
    "Gast sieht": "Guest sees", "öffentliche Vorschau,..": "public preview,..",
    "Mitglied sieht": "Member sees", "alle Details, Handel,..": "all details, trading,..",
    "Merke": "Note",
    "Der Browser spricht nur mit dem Server. Scheitert eine Prüfung, endet die Anfrage dort.":
        "The browser only talks to the server. If a check fails, the request stops there.",
    "Datenbank und 7-Tage-Job": "Database and 7-Day Job",
    "PostgreSQL hält 6 Tabellen. Ein Hintergrund-Job erinnert nach 7 Tagen alle, die noch nicht gehandelt haben.":
        "PostgreSQL holds 6 tables. A background job reminds everyone who has not traded after 7 days.",
    "Links die sechs Tabellen: vier legt Better Auth an, zwei gehören zur App. Rechts der zeitgesteuerte Job: "
    "BullMQ plant ihn bei der Registrierung, Redis hält ihn, der Worker zählt nach 7 Tagen die Trades "
    "und verschickt nur bei 0 Trades eine Erinnerung.":
        "Left: the six tables. Better Auth creates four, two belong to the app. Right: the timed job. "
        "BullMQ plans it at sign-up, Redis keeps it, after 7 days the worker counts the trades "
        "and sends a reminder only if there are 0.",
    "PostgreSQL · 6 Tabellen": "PostgreSQL · 6 tables",
    "Ein Eintrag pro Person": "One row per person", "Anzeigename": "display name", "eindeutig": "unique",
    "ja/nein": "yes/no", "7-Tage-Frist": "7-day timer",
    "Aktive Logins, je Gerät": "Active logins, per device", "steht im Cookie": "stored in the cookie",
    "Ablaufdatum": "expiry date",
    "Passwort oder z. B. Google": "Password or e.g. Google",
    "Login-Art": "login type", "nur als Hash": "hash only",
    "Codes für E-Mail und Reset": "Codes for email and reset",
    "wofür": "purpose", "der Code": "the code", "läuft ab": "expires",
    "Angebote, zwei Sichtbarkeiten": "Offers, two visibility levels",
    "öffentlich": "public", "Mitglieder": "members",
    "Abgeschlossene Trades": "Finished trades", "Abschluss": "finished at",
    "Primärschlüssel: eindeutige ID": "Primary key: unique ID",
    "Fremdschlüssel: verweist auf eine andere Tabelle": "Foreign key: points to another table",
    "Kein Zugriff aus dem Browser: nur die Stationen im Backend lesen und schreiben.":
        "No access from the browser: only the backend steps read and write.",
    "7-Tage-Job · zeitgesteuert, ohne Browser": "7-day job · on a timer, no browser",
    "Job einplanen": "Plan the job",
    "Bei der Registrierung: Job anlegen, fällig in 7\u00a0Tagen": "At sign-up: add a job, due in 7\u00a0days",
    "Job-Speicher": "Job storage",
    "Hält den Job, auch über Neustarts": "Keeps the job, even across restarts",
    "Inaktivität prüfen": "Check inactivity",
    "Eigener Node.js-Prozess: zählt die Trades, ab\u00a01\u00a0Trade endet der Job":
        "Its own Node.js process: counts the trades, from 1 trade on the job ends",
    "E-Mail bauen": "Build the email",
    "React-Komponente, gerendert zu HTML": "React component, turned into HTML",
    "Versand ins Postfach": "Delivery to the inbox",
    "Noch offen: z. B. Resend, Postmark oder Amazon SES": "Not chosen yet: e.g. Resend, Postmark or Amazon SES",
    "7 Tage warten": "wait 7 days", "fällig": "due",
    "nur bei 0 Trades": "only if 0 trades", "fertige E-Mail": "finished email",
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


def zone(slide, x, y, w, label, color, ic=None):
    if ic:
        icon(slide, ic, x, y - 0.01, 0.24, color)
        x, w = x + 0.31, w - 0.31
    text(slide, x, y, w, 0.25, [[run(label, 11, True, color)]])


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
    y, h = 1.62, 1.68
    fx, fw, bg = 0.5, 4.1, 0.12
    bw3 = (fw - 2 * bg) / 3
    base = [("file-code", "Sprache", "TypeScript", "Browser, Server, Hintergrund-Jobs"),
            ("layers", "Framework", "Next.js", "Routing + API auf React"),
            ("cpu", "Laufzeit", "Node.js", "Server und Hintergrund-Jobs")]
    for i, (ic, lab, name, desc) in enumerate(base):
        x = fx + i * (bw3 + bg)
        box(s, x, y, bw3, h, INK)
        icon(s, ic, x + (bw3 - 0.3) / 2, y + 0.15, 0.3, SURFACE)
        text(s, x, y + 0.52, bw3, 0.2, [[run(lab, 10.5, True, ON_INK)]], align=C)
        text(s, x, y + 0.74, bw3, 0.34, [[run(name, 13, True, SURFACE, TOOL)]], align=C, anchor=M)
        text(s, x + 0.08, y + 1.1, bw3 - 0.16, 0.45, [[run(desc, 10.5, False, ON_INK)]], align=C)
    groups = [("monitor", "Benutzeroberfläche", S1, ["React", "Next.js Routing\u00a0+\u00a0API"]),
              ("shield-check", "Sicherheit", S2, ["Better Auth", "Zod", "Data Access Layer"]),
              ("database", "Daten", S3, ["Prisma / Drizzle", "PostgreSQL"]),
              ("mail", "Hintergrund & E-Mail", S4, ["BullMQ", "Redis", "React Email", "Mail-Dienst"])]
    gap = 0.15
    gx, gw = fx + fw + gap, (12.833 - (fx + fw + gap) - 3 * gap) / 4
    for i, (ic, lab, col, items) in enumerate(groups):
        x = gx + i * (gw + gap)
        box(s, x, y, gw, h, tint(col, 0.1))
        edge = box(s, x, y, gw, 0.08, col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)  # Farbkante = Gruppe
        edge.adjustments[0] = 0.5
        icon(s, ic, x + (gw - 0.26) / 2, y + 0.16, 0.26, col)
        text(s, x + 0.08, y + 0.48, gw - 0.16, h - 0.5,
             [[run(lab, 11, True, col)]] + [[run(it, 11, True, INK, TOOL)] for it in items],
             align=C, space=2)

    # Weg einer Anfrage: Browser → 5 Stationen → Datenbank
    top, fh = 3.8, 2.2
    zone(s, 0.5, top - 0.3, 1.6, "Browser", S1, "monitor")
    bw = 1.6
    ch = (fh - 0.15) / 2
    for i, (ic, who, how) in enumerate([("user", "Gast", "ohne Login"), ("user-check", "Mitglied", "mit Session-Cookie")]):
        cy = top + i * (ch + 0.15)
        box(s, 0.5, cy, bw, ch, tint(S1, 0.1))
        icon(s, ic, 0.5 + (bw - 0.28) / 2, cy + 0.12, 0.28, S1)
        text(s, 0.55, cy + 0.44, bw - 0.1, ch - 0.48, [[run(who, 14, True)], [run(how, 11)]], align=C, space=1)

    dbw = 1.55
    dbx = 12.833 - dbw
    sx = 0.5 + bw + 0.42
    sw = dbx - 0.42 - sx
    zone(s, sx, top - 0.3, sw, "Next.js-Server auf Node.js · für Besucher unsichtbar", S2, "server")
    box(s, sx, top, sw, fh, tint(S2, 0.1))
    for i in range(2):
        cy = top + i * (ch + 0.15) + ch / 2
        arrow(s, 0.5 + bw + 0.04, cy, sx - 0.02, cy, S1, width=2.5)

    stations = [("log-in", "Next.js\nRouting + API", "Einstiegspunkt", "Nimmt jede Anfrage an"),
                ("key-round", "Better Auth", "Authentifizierung", "Wer fragt? Gast oder Mitglied"),
                ("list-checks", "Zod", "Validierung", "Ist die Eingabe gültig?"),
                ("eye", "Data Access Layer", "Autorisierung", "Was darf diese Rolle (User) sehen?"),
                ("database", "Prisma / Drizzle", "ORM", "Baut sichere\nSQL-Abfragen")]
    pad, ag, d = 0.12, 0.26, 0.4
    stw = (sw - 2 * pad - 4 * ag) / 5
    sty, sth = top + pad, fh - 2 * pad
    my = sty + 0.14 + d / 2  # Mittellinie der Nummern = Höhe der Pfeile
    for i, (ic, name, role, desc) in enumerate(stations):
        x = sx + pad + i * (stw + ag)
        box(s, x, sty, stw, sth, SURFACE)
        step(s, x + stw / 2 - d - 0.06, sty + 0.14, i + 1, S2, d=d)
        icon(s, ic, x + stw / 2 + 0.1, my - 0.16, 0.32, S2)
        text(s, x + 0.04, sty + 0.6, stw - 0.08, 0.22, [[run(role, 10.5, True, S2)]], align=C)
        text(s, x + 0.04, sty + 0.82, stw - 0.08, 0.46, lines(name, 12, True, INK, TOOL), align=C, anchor=M)
        text(s, x + 0.06, sty + 1.32, stw - 0.12, 0.6, lines(desc, 11), align=C)
        if i:
            arrow(s, x - ag + 0.03, my, x - 0.03, my, S2, width=2.5)

    zone(s, dbx, top - 0.3, dbw, "Datenbank", S3, "database")
    db = box(s, dbx, top, dbw, fh, tint(S3, 0.12), S3, shape=MSO_SHAPE.CAN)
    db.adjustments[0] = 0.14
    db.line.width = Pt(1.25)
    text(s, dbx + 0.1, top + 0.3, dbw - 0.2, fh - 0.4,
         [[run("PostgreSQL", 13, True, INK, TOOL)], [run("Konten, Logins, Angebote, Trades", 11)],
          [run("→ Folie 2", 11, True, S3)]], align=C, anchor=M, space=4)
    arrow(s, sx + sw + 0.03, my, dbx - 0.03, my, S3, both=True, width=2.5)
    text(s, sx + sw - 0.02, my + 0.08, 0.46, 0.3, [[run("SQL", 10.5, True, S3)]], align=C)

    # Antwort nach Rolle + Merksatz: Icon links, Text mittig daneben
    ry, rh = 6.16, 1.06
    rw = (12.333 - 2 * 0.2) / 3
    code = lambda t: run(t, 12, True, INK, MONO)
    cards = [(tint(S1, 0.1), INK, S1, "eye", "Gast sieht",
              [[code("previewText")], [run("öffentliche Vorschau,..", 12)]]),
             (tint(S1, 0.1), INK, S1, "lock-open", "Mitglied sieht",
              [[code("previewText"), run(" + ", 12, True, S1), code("memberDetails")],
               [run("alle Details, Handel,..", 12)]]),
             (INK, SURFACE, ON_INK, "lightbulb", "Merke",
              [[run("Der Browser spricht nur mit dem Server. Scheitert eine Prüfung, endet die Anfrage dort.",
                    12, False, ON_INK)]])]
    for i, (fill, ink, icol, ic, head, body) in enumerate(cards):
        x = 0.5 + i * (rw + 0.2)
        box(s, x, ry, rw, rh, fill)
        icon(s, ic, x + 0.25, ry + (rh - 0.44) / 2, 0.44, icol)
        text(s, x + 0.85, ry, rw - 1.1, rh, [[run(head, 13.5, True, ink)]] + body, align=C, anchor=M, space=3)


def slide_data_job(prs):
    s = new_slide(
        prs,
        "Datenbank und 7-Tage-Job",
        "PostgreSQL hält 6 Tabellen. Ein Hintergrund-Job erinnert nach 7 Tagen alle, die noch nicht gehandelt haben.",
        "Links die sechs Tabellen: vier legt Better Auth an, zwei gehören zur App. Rechts der zeitgesteuerte Job: "
        "BullMQ plant ihn bei der Registrierung, Redis hält ihn, der Worker zählt nach 7 Tagen die Trades "
        "und verschickt nur bei 0 Trades eine Erinnerung.",
    )
    C, M = PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE

    lx, lw = 0.5, 7.7
    zone(s, lx, 1.6, lw, "PostgreSQL · 6 Tabellen", S3, "database")
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
        ("session", BA, "Aktive Logins, je Gerät",
         [col("id", tag("PK")), col("userId", tag("FK"), note("→ user")), col("token", note("steht im Cookie")),
          col("expiresAt", note("Ablaufdatum"))]),
        ("account", BA, "Passwort oder z. B. Google",
         [col("id", tag("PK")), col("userId", tag("FK"), note("→ user")), col("providerId", note("Login-Art")),
          col("password", tag("nur als Hash", S4))]),
        ("verification", BA, "Codes für E-Mail und Reset",
         [col("id", tag("PK")), col("identifier", note("wofür")), col("value", note("der Code")),
          col("expiresAt", note("läuft ab"))]),
        ("listings", APP, "Angebote, zwei Sichtbarkeiten",
         [col("id", tag("PK")), col("ownerId", tag("FK"), note("→ user")), col("previewText", tag("öffentlich", S2)),
          col("memberDetails", tag("Mitglieder", S4))]),
        ("trades", APP, "Abgeschlossene Trades",
         [col("id", tag("PK")), col("listingId", tag("FK"), note("→ listings")),
          col("sellerId", tag("FK"), note("→ user")), col("buyerId", tag("FK"), note("→ user")),
          col("completedAt", note("Abschluss"))]),
    ]
    tw, gap = (lw - 2 * 0.2) / 3, 0.2
    ty0, th, hh = 1.95, 2.25, 0.66
    for i, (name, (origin, ocol), desc, cols) in enumerate(tables):
        x, y = lx + (i % 3) * (tw + gap), ty0 + (i // 3) * (th + gap)
        box(s, x, y, tw, th, SURFACE, LINE)
        head = box(s, x, y, tw, hh, tint(ocol, 0.14), shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
        head.adjustments[0] = 0.09 / hh
        text(s, x + 0.1, y, tw - 0.2, hh, [[run(origin, 9.5, True, ocol, TOOL)], [run(name, 15, True, INK, MONO)]],
             align=C, anchor=M, space=1)
        text(s, x + 0.16, y + hh + 0.1, tw - 0.32, th - hh - 0.15,
             [[run(desc, 11, True)]] + cols, space=3)

    ly = ty0 + 2 * th + gap + 0.15
    text(s, lx, ly, lw, 0.45, [[
        run("PK", 11, True, S3), run(" Primärschlüssel: eindeutige ID   ", 11),
        run("FK", 11, True, S3), run(" Fremdschlüssel: verweist auf eine andere Tabelle", 11)], [
        run("Kein Zugriff aus dem Browser: nur die Stationen im Backend lesen und schreiben.", 11)]],
        align=C, space=2)

    # 7-Tage-Job, senkrecht
    rx = lx + lw + 0.4
    rw = 12.833 - rx
    zone(s, rx, 1.6, rw, "7-Tage-Job · zeitgesteuert, ohne Browser", S4, "clock")
    icons = ["clock", "hard-drive", "search", "mail", "send"]
    steps = [("BullMQ Queue", "Job einplanen", "Bei der Registrierung: Job anlegen, fällig in 7\u00a0Tagen"),
             ("Redis", "Job-Speicher", "Hält den Job, auch über Neustarts"),
             ("BullMQ Worker", "Inaktivität prüfen", "Eigener Node.js-Prozess: zählt die Trades, ab\u00a01\u00a0Trade endet der Job"),
             ("React Email", "E-Mail bauen", "React-Komponente, gerendert zu HTML"),
             ("Mail-Dienst", "Versand ins Postfach", "Noch offen: z. B. Resend, Postmark oder Amazon SES")]
    hops = ["7 Tage warten", "fällig", "nur bei 0 Trades", "fertige E-Mail"]
    sy0, sh, d = 1.95, 0.8, 0.4
    sgap = (ly + 0.45 - sy0 - 5 * sh) / 4
    ax = rx + 0.16 + d / 2
    for i, (name, role, desc) in enumerate(steps):
        y = sy0 + i * (sh + sgap)
        box(s, rx, y, rw, sh, tint(S4, 0.1))
        step(s, rx + 0.16, y + (sh - d) / 2, i + 1, S4, d=d)
        icon(s, icons[i], rx + rw - 0.5, y + (sh - 0.32) / 2, 0.32, S4)
        text(s, rx + 0.72, y, rw - 1.3, sh,
             [[run(name, 12, True, INK, TOOL), run("  " + role, 11, True, S4)], [run(desc, 11)]],
             anchor=M, space=2)
        if i < 4:
            arrow(s, ax, y + sh + 0.03, ax, y + sh + sgap - 0.03, S4, width=2.5)
            text(s, ax + 0.2, y + sh, rw - 0.6, sgap, [[run(hops[i], 11, True, S4)]], anchor=M)

    # trades → Worker (gestrichelt: Worker liest die Anzahl der Trades)
    trades_y = ty0 + th + gap
    worker_y = sy0 + 2 * (sh + sgap)
    ay = (max(trades_y, worker_y) + min(trades_y + th, worker_y + sh)) / 2
    arrow(s, lx + lw + 0.04, ay, rx - 0.04, ay, S4, dashed=True, width=2.25)


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
