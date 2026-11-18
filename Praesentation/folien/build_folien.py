"""Erzeugt die 2 Folien (16:9) aus der Architektur-Seite Praesentation/index.html.

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
    "Browser und Server": "browser and server",
    "Routing + API auf React": "routing + API on React",
    "führt den Server aus": "runs the server",
    "Routing + API": "Routing + API", "Next.js Routing\u00a0+\u00a0API": "Next.js Routing\u00a0+\u00a0API",
    "Benutzeroberfläche": "User interface", "Sicherheit": "Security", "Daten": "Data",
    "Gast": "Guest", "Mitglied": "Member", "ohne Cookie": "no cookie", "Ohne": "Not", "Login": "logged in",
    "Registriert": "Registered", "+ Login": "+ logged in", "Frontend · Browser": "Frontend · browser",
    "mit Session-Cookie": "with session cookie",
    "Backend · Next.js-Server auf Node.js · für Besucher unsichtbar":
        "Backend · Next.js server on Node.js · hidden from visitors",
    "Einstiegspunkt": "Entry point", "Nimmt jede Anfrage an": "Takes every request",
    "Authentifizierung": "Authentication", "Wer fragt? Gast oder Mitglied": "Who asks? Guest or member",
    "Validierung": "Validation", "Ist die Eingabe gültig?": "Is the input valid?",
    "Autorisierung": "Authorization", "Was darf Gast oder Mitglied sehen?": "What may guest or member see?",
    "Baut sichere": "Builds safe", "SQL-Abfragen": "SQL queries",
    "Datenbank": "Database", "Standorte, Nutzer, Materialien, Angebote, Matches": "Sites, users, materials, offers, matches",
    "Gast sieht": "Guest sees", "Mitglied sieht": "Member sees",
    "• Titel + Material": "• Title + material", "• Menge + Stadt": "• Quantity + city",
    "• Registrieren": "• Sign up", "• Login": "• Log in", "• E-Mail bestätigen": "• Confirm email",
    "• Passwort zurücksetzen,..": "• Reset password,..",
    "• + Preis + Beschreibung": "• + Price + description", "• + Kontakt": "• + Contact",
    "• Match anfragen": "• Request a match", "• Angebote einstellen": "• Post offers",
    "• Eigene Matches,..": "• Own matches,..",
    "Software Architecture Stack: Was jeder Baustein tut": "Software Architecture Stack: What Each Building Block Does",
    "7 Bausteine zwischen Frontend und Datenbank – was sie tun und warum wir sie gewählt haben.":
        "7 building blocks between frontend and database – what they do and why we chose them.",
    "Oben das Backend: TypeScript, Next.js und Node.js tragen alles. Darunter die Kette jeder Anfrage: "
    "Better Auth, Zod, Data Access Layer und Prisma/Drizzle. Links übergibt das Frontend (andere Gruppe), "
    "rechts geht es an die Datenbank (nächster Teil).":
        "Top: the backend. TypeScript, Next.js and Node.js carry everything. Below, the chain of every request: "
        "Better Auth, Zod, Data Access Layer and Prisma/Drizzle. On the left the frontend hands over (other "
        "group), on the right it goes on to the database (next part).",
    "Backend": "Backend", "Jede Anfrage": "Every request",
    "React-Seiten": "React pages",
    "Frontend": "Frontend", "PostgreSQL": "PostgreSQL", "SQL": "SQL", 
    "Framework": "Framework", "ORM": "ORM",
    "JavaScript mit Typangaben. Der Editor meldet Fehler, bevor der Code läuft.":
        "JavaScript with type annotations. The editor reports errors before the code runs.",
    "ein Angebot hat einen Titel (Text) und eine Menge (Zahl)":
        "an offer has a title (text) and a quantity (number)",
    "eine Sprache für Frontend, Backend und Datenzugriff":
        "one language for frontend, backend and data access",
    "Framework auf React für Seiten und API. Jede Datei im Ordner app/ wird zu einer Adresse.":
        "Framework on React for pages and API. Every file in the app/ folder becomes an address.",
    "/offers zeigt die Liste, /offers/[id] ein einzelnes Angebot":
        "/offers shows the list, /offers/[id] a single offer",
    "Frontend und Backend in einem Projekt":
        "frontend and backend in one project",
    "Führt den Server-Code aus: nimmt Anfragen an und hält die Verbindung zur Datenbank.":
        "Runs the server code: takes requests and keeps the connection to the database.",
    "bearbeitet viele Anfragen gleichzeitig, ohne zu blockieren":
        "handles many requests at once without blocking",
    "Standard-Laufzeit für Next.js, gleiche Sprache wie im Browser":
        "standard runtime for Next.js, same language as in the browser",
    "Prüft beim Login das Passwort, setzt ein Session-Cookie und erkennt es bei jeder Anfrage wieder.":
        "Checks the password at login, sets a session cookie and recognises it on every request.",
    "ohne Cookie → Gast,": "no cookie → guest,", "mit Cookie → Mitglied": "with cookie → member",
    "Open Source, Nutzerkonten bleiben in unserer Datenbank":
        "open source, user accounts stay in our database",
    "Prüft jede Eingabe gegen ein festes Schema und lehnt falsche Daten ab, bevor sie die Datenbank erreichen.":
        "Checks every input against a fixed schema and rejects wrong data before it reaches the database.",
    "Menge in kg muss eine positive Zahl sein":
        "quantity in kg must be a positive number",
    "ein Schema liefert Prüfung und TypeScript-Typ":
        "one schema gives the check and the TypeScript type",
    "Eigene Code-Schicht für alle Datenzugriffe. Prüft, ob die Rolle die Daten sehen oder ändern darf.":
        "Own code layer for all data access. Checks whether the role may see or change the data.",
    "Preis und Kontakt nur für Mitglieder; ein Angebot ändert nur der eigene Standort":
        "price and contact for members only; only the own site may change an offer",
    "Zugriffsregeln an einer Stelle statt verteilt":
        "access rules in one place instead of scattered",
    "Bildet die Tabellen als TypeScript-Objekte ab und übersetzt Aufrufe in SQL-Abfragen.":
        "Maps the tables to TypeScript objects and turns calls into SQL queries.",
    "alle Angebote eines Materials laden":
        "load all offers of one material",
    "typsicher, Werte werden sicher eingesetzt (keine SQL-Injection)":
        "type-safe, values are inserted safely (no SQL injection)",
    "Backend · Grundlage für jede Anfrage": "Backend · foundation for every request",
    "Die Bausteine des Stacks: was sie tun, ein Beispiel aus der App und warum wir sie gewählt haben.":
        "The building blocks of the stack: what they do, an example from the app and why we chose them.",
    "Beispiel:": "Example:", "Warum": "Why", "Grundlage": "foundation",
    "App-Architektur": "App Architecture",
}
MISSING = set()

# Farben aus style.css (:root, hell)
BG, SURFACE, LINE, INK = "F2F4F8", "FFFFFF", "D6DCE8", "121A2C"
S1, S2, S3 = "2255D4", "0D7A54", "6A3FD0"  # Frontend, Sicherheit, Daten
ON_INK = "E3E8F2"  # Nebentext auf dunklem Grund
LABEL_ON_INK = "9DBBFF"  # „Beispiel:“/„Warum …?“ auf dunklem Grund: farbig wie auf hellen Karten (Kontrast > 7:1)
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


BR = None  # Zeilenumbruch innerhalb eines Absatzes (für text())


def text(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=0):
    """paras: Liste von Absätzen, jeder Absatz eine Liste von run()-Dicts; BR = Zeilenumbruch im Absatz."""
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
            if r is BR:
                p.add_line_break()
                continue
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


def zone(slide, x, y, w, label, color, ic=None, size=11):
    """Zonen-Titel (Icon + Text) mittig über der Grafik darunter; Icon wächst mit der Schrift."""
    tw = label_width(label, size) + 0.06
    d = 0.24 * size / 11
    gw = tw + (d + 0.07 if ic else 0)
    x0 = x + (w - gw) / 2
    if ic:
        icon(slide, ic, x0, y - 0.01 - (d - 0.24) / 2, d, color)
        x0 += d + 0.07
    text(slide, x0, y - (size - 11) / 144, tw, 0.25 + (size - 11) / 72, [[run(label, size, True, color)]])


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

    # Tech-Stack: 3 Fundament-Karten (dunkel) + 3 Gruppen, alles mittig
    # Reihe mittig zwischen Untertitel und Zonen-Titeln des Anfrage-Wegs: oben = unten
    top = 3.8  # Oberkante des Anfrage-Wegs (Zonen-Titel 0,31 darüber)
    lead_bottom, flow_head = 1.26, top - 0.31
    h = 1.62
    y = lead_bottom + (flow_head - lead_bottom - h) / 2
    fx, fw, bg = 0.5, 4.1, 0.12
    bw3 = (fw - 2 * bg) / 3
    base = [("file-code", "Sprache", "TypeScript", "Browser und Server"),
            ("layers", "Framework", "Next.js", "Routing + API auf React"),
            ("cpu", "Laufzeit", "Node.js", "führt den Server aus")]
    for i, (ic, lab, name, desc) in enumerate(base):
        x = fx + i * (bw3 + bg)
        box(s, x, y, bw3, h, INK)
        icon(s, ic, x + (bw3 - 0.32) / 2, y + 0.12, 0.32, SURFACE)  # gleich groß wie in den Gruppen
        text(s, x, y + 0.52, bw3, 0.2, [[run(lab, 10, True, ON_INK)]], align=C)
        text(s, x, y + 0.71, bw3, 0.3, [[run(name, 12, True, SURFACE, TOOL)]], align=C, anchor=M)
        text(s, x + 0.08, y + 1.03, bw3 - 0.16, 0.42, [[run(desc, 10, False, ON_INK)]], align=C)
    groups = [("monitor", "Benutzeroberfläche", S1, ["React", "Next.js Routing\u00a0+\u00a0API"]),
              ("shield-check", "Sicherheit", S2, ["Better Auth", "Zod", "Data Access Layer"]),
              ("database", "Daten", S3, ["Prisma / Drizzle", "PostgreSQL"])]
    gap = 0.15
    gx = fx + fw + gap
    gw = (12.833 - gx - (len(groups) - 1) * gap) / len(groups)
    gh, pad, isz = 1.5, 0.16, 0.32  # etwas flacher als die dunklen Karten, senkrecht mittig zu ihnen
    gy = y + (h - gh) / 2
    for i, (ic, lab, col, items) in enumerate(groups):
        x = gx + i * (gw + gap)
        box(s, x, gy, gw, gh, tint(col, 0.1))
        icon(s, ic, x + (gw - isz) / 2, gy + 0.13, isz, col)  # Icon + Titel mittig, Liste linksbündig
        ty = gy + 0.13 + isz + 0.08  # Titel mit Abstand unter dem Icon
        text(s, x + pad, ty, gw - 2 * pad, 0.2, [[run(lab, 10, True, col)]], align=C)
        ty += 0.24
        text(s, x + pad, ty, gw - 2 * pad, gy + gh - ty, [[run(it, 10, True, INK, TOOL)] for it in items], space=3)

    # Weg einer Anfrage: Browser → 5 Stationen → Datenbank (Frontend links, Datenbank rechts)
    fh = 2.2
    bw, dbw = 1.6, 1.55
    ch = (fh - 0.15) / 2
    fex, dbx = 0.5, 12.833 - dbw
    sx = fex + bw + 0.42
    sw = dbx - 0.42 - sx
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
    divider(fex + bw + 0.21, [(m - 0.14, m + 0.14) for m in card_mid])
    divider(sx + sw + 0.21, [(mid - 0.26, mid + 0.22)])

    zone(s, fex, top - 0.3, bw, "Frontend · Browser", S1, "monitor")
    people = [("user", "Gast", "ohne Cookie", "Ohne\nLogin"),
              ("user-check", "Mitglied", "mit Session-Cookie", "Registriert\n+ Login")]
    for i, (ic, who, how, state) in enumerate(people):
        cy = top + i * (ch + 0.15)
        # Kontostand senkrecht links neben der Karte (Textfeld um 270° gedreht, Mitte bleibt)
        vh = 0.38
        tb = text(s, fex - 0.21 - ch / 2, cy + ch / 2 - vh / 2, ch, vh, lines(state, 10, True, S1),
                  align=C, anchor=M)
        tb.rotation = 270
        box(s, fex, cy, bw, ch, tint(S1, 0.1))
        icon(s, ic, fex + (bw - 0.28) / 2, cy + 0.12, 0.28, S1)
        text(s, fex + 0.05, cy + 0.44, bw - 0.1, ch - 0.48, [[run(who, 14, True)], [run(how, 11)]], align=C, space=1)

    zone(s, sx, top - 0.3, sw, "Backend · Next.js-Server auf Node.js · für Besucher unsichtbar", S2, "server")
    box(s, sx, top, sw, fh, tint(S2, 0.1))
    for m in card_mid:
        arrow(s, fex + bw + 0.04, m, sx - 0.02, m, S1, width=2.5)

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
        x = sx + pad + i * (stw + ag)  # Station 1 links am Browser, Station 5 rechts an der Datenbank
        box(s, x, sty, stw, sth, SURFACE)
        icon(s, ic, x + stw / 2 - 0.42, my - 0.16, 0.32, S2)  # Icon links, Nummer rechts
        step(s, x + stw / 2 + 0.06, sty + 0.14, i + 1, S2, d=d)
        text(s, x + 0.04, sty + 0.6, stw - 0.08, 0.22, [[run(role, 10.5, True, S2)]], align=C)
        text(s, x + 0.04, sty + 0.82, stw - 0.08, 0.46, lines(name, 12, True, INK, TOOL), align=C, anchor=M)
        text(s, x + 0.06, sty + 1.32, stw - 0.12, 0.6, lines(desc, 11), align=C)
        if i:  # Pfeil von der vorigen Station (links) nach rechts, senkrecht mittig zur Karte
            arrow(s, x - ag + 0.03, sty + sth / 2, x - 0.03, sty + sth / 2, S2, width=2.5)

    zone(s, dbx, top - 0.3, dbw, "Datenbank", S3, "database")
    db = box(s, dbx, top, dbw, fh, tint(S3, 0.12), S3, shape=MSO_SHAPE.CAN)
    db.adjustments[0] = 0.14
    db.line.width = Pt(1.25)
    text(s, dbx + 0.1, top + 0.3, dbw - 0.2, fh - 0.4,
         [[run("PostgreSQL", 13, True, INK, TOOL)], [run("Standorte, Nutzer, Materialien, Angebote, Matches", 11)]], align=C, anchor=M, space=4)
    arrow(s, sx + sw + 0.03, mid - 0.12, dbx - 0.03, mid - 0.12, S3, both=True, width=2.5)
    text(s, sx + sw - 0.02, mid - 0.04, 0.46, 0.22, [[run("SQL", 10.5, True, S3)]], align=PP_ALIGN.CENTER)

    # Antwort nach Rolle: Gast und Mitglied nebeneinander, als Paar mittig auf der Folie
    ry, rh = 6.16, 1.06
    rw = (12.333 - 2 * 0.2) / 3
    def bullets(x, y, w, cols, color, size=10.5):
        """Stichpunkte in 2 Spalten, linksbündig; linke Spalte so breit wie ihr längster Punkt."""
        c1 = max(label_width("• " + t, size, bold=False) for t in cols[0]) + 0.22
        for j, items in enumerate(cols):
            cx, cw = (x, c1) if j == 0 else (x + c1, w - c1)
            text(s, cx, y, cw, rh - 0.4, [[run("• " + t, size, False, color)] for t in items], space=1)

    # Gast / Mitglied als Browserfenster: Titelleiste mit Punkten + Adresszeile, darunter die Seite
    windows = [("user", "Gast sieht", "/offers",
                [["Titel + Material", "Menge + Stadt", "Registrieren"],
                 ["Login", "E-Mail bestätigen", "Passwort zurücksetzen,.."]]),
               ("user-check", "Mitglied sieht", "/offers/[id]",
                [["+ Preis + Beschreibung", "+ Kontakt", "Match anfragen"],
                 ["Angebote einstellen", "Eigene Matches,.."]])]
    def text_w(cols, size=10.5):
        """Breite der beiden Stichpunkt-Spalten zusammen (wie in bullets())."""
        return sum(max(label_width("• " + t, size, bold=False) for t in c) for c in cols) + 0.22

    bar = 0.3
    # großes Icon in beiden Fenstern gleich groß: so groß, wie die engste freie Fläche erlaubt (≤ 0.46")
    big = min(0.46, min(rw - 0.2 - text_w(c) for *_, c in windows) - 0.24)
    for i, (ic, head, field, cols) in enumerate(windows):
        x = 0.5 + (12.333 - 2 * rw - 0.2) / 2 + i * (rw + 0.2)
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
        # dasselbe Icon groß, mittig in der freien Fläche rechts neben den Stichpunkten
        free_x = x + 0.2 + text_w(cols)
        icon(s, ic, free_x + (x + rw - free_x - big) / 2, ry + bar + (rh - bar - big) / 2, big, tint(S1, 0.55))
        bullets(x + 0.2, ry + bar + 0.08, rw - 0.3, cols, INK)



# Folie 2: die 7 Bausteine des Stacks, je Karte Rolle, Name, was er tut, Alltagsvergleich, Grund der Wahl
STACK = {  # Schlüssel: (Name, Rolle, Icon, Farbe, was er tut, Beispiel im Projekt, Grund der Wahl)
    "ts": ("TypeScript", "Sprache", "file-code", INK,
        "JavaScript mit Typangaben. Der Editor meldet Fehler, bevor der Code läuft.",
        "ein Angebot hat einen Titel (Text) und eine Menge (Zahl)", "eine Sprache für Frontend, Backend und Datenzugriff"),
    "next": ("Next.js", "Framework", "layers", INK,
        "Framework auf React für Seiten und API. Jede Datei im Ordner app/ wird zu einer Adresse.",
        "/offers zeigt die Liste, /offers/[id] ein einzelnes Angebot", "Frontend und Backend in einem Projekt"),
    "node": ("Node.js", "Laufzeit", "cpu", INK,
        "Führt den Server-Code aus: nimmt Anfragen an und hält die Verbindung zur Datenbank.",
        "bearbeitet viele Anfragen gleichzeitig, ohne zu blockieren", "Standard-Laufzeit für Next.js, gleiche Sprache wie im Browser"),
    "auth": ("Better Auth", "Authentifizierung", "key-round", S2,
        "Prüft beim Login das Passwort, setzt ein Session-Cookie und erkennt es bei jeder Anfrage wieder.",
        "ohne Cookie → Gast,\nmit Cookie → Mitglied", "Open Source, Nutzerkonten bleiben in unserer Datenbank"),
    "zod": ("Zod", "Validierung", "list-checks", S2,
        "Prüft jede Eingabe gegen ein festes Schema und lehnt falsche Daten ab, bevor sie die Datenbank erreichen.",
        "Menge in kg muss eine positive Zahl sein", "ein Schema liefert Prüfung und TypeScript-Typ"),
    "dal": ("Data Access Layer", "Autorisierung", "eye", S2,
        "Eigene Code-Schicht für alle Datenzugriffe. Prüft, ob die Rolle die Daten sehen oder ändern darf.",
        "Preis und Kontakt nur für Mitglieder; ein Angebot ändert nur der eigene Standort", "Zugriffsregeln an einer Stelle statt verteilt"),
    "orm": ("Prisma / Drizzle", "ORM", "database", S3,
        "Bildet die Tabellen als TypeScript-Objekte ab und übersetzt Aufrufe in SQL-Abfragen.",
        "alle Angebote eines Materials laden", "typsicher, Werte werden sicher eingesetzt (keine SQL-Injection)"),
}


def line_count(t, width, size):
    """Zeilen, die ein Arial-Text (Liberation Sans, maßgleich) bei Wortumbruch in width Zoll braucht."""
    from PIL import ImageFont
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", size * 10)
    n, cur = 1, ""
    for word in tr(t).split():
        trial = f"{cur} {word}".strip()
        if cur and font.getlength(trial) / 10 / 72 > width:
            n, cur = n + 1, word
        else:
            cur = trial
    return n


def fit_size(label, width, sizes=(12, 11.5, 11, 10.5)):
    """Größte Schriftgröße, bei der ein Tool-Name (Verdana, gerendert als DejaVu Sans) in eine Zeile passt."""
    from PIL import ImageFont
    for size in sizes:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size * 10)
        if font.getlength(tr(label)) / 10 / 72 <= width:
            return size
    return sizes[-1]


def stack_card(s, x, y, w, h, key, what_lines=1):
    """Karte: Icon + Rolle + Name oben, darunter ein Textfluss (was · Beispiel · „Warum <Name>?“) – nichts überlappt.
    Fundament-Bausteine (Farbe INK) dunkel wie auf Folie 1. what_lines = Zeilen des längsten „was“ der Reihe:
    kürzere Texte werden mit Leerzeilen aufgefüllt, damit „Beispiel:“ in der ganzen Reihe auf einer Linie steht."""
    name, role, ic, col, what, example, why = STACK[key]
    dark = col == INK
    fill, ink, accent = (INK, SURFACE, ON_INK) if dark else (tint(col, 0.1), INK, col)
    p, nx = 0.14, 0.58
    box(s, x, y, w, h, fill)
    icon(s, ic, x + p, y + 0.14, 0.34, ink if dark else col)
    text(s, x + nx, y + 0.08, w - nx - 0.06, 0.2, [[run(role, 10, True, accent)]])
    text(s, x + nx, y + 0.28, w - nx - 0.06, 0.28,
         [[run(name, fit_size(name, w - nx - 0.1), True, ink, TOOL)]])
    label = LABEL_ON_INK if dark else col  # „Beispiel:“ und „Warum …?“ farbig, Text darunter in Textfarbe
    body_y, body_h = y + 0.62, h - 0.62 - 0.12
    text(s, x + p, body_y, w - 2 * p, body_h, [
        [run(what, 10.5, False, ink)] + [BR, run(" ", 10.5)] * (what_lines - line_count(what, w - 2 * p, 10.5)),
        [run("Beispiel:", 10, True, label)]
        + [r for part in example.split("\n") for r in (BR, run(part, 10, False, ink))]], space=5)  # \n = fester Umbruch
    # „Warum <Name>?“ unten in der Karte, linksbündig; Name fett in Textfarbe (Arial, damit er in eine Zeile passt)
    text(s, x + p, body_y, w - 2 * p, body_h, [
        [run("Warum", 10, True, label), run(" "), run(name.replace(" ", "\u00a0"), 10, True, ink),
         run("?", 10, True, label), BR, run(why, 10, False, ink)]], anchor=MSO_ANCHOR.BOTTOM)


def handover(s, x, y, w, h, ic, head, what, col):
    """Gestrichelte Leiste: Teil, den eine andere Person vorstellt."""
    r = box(s, x, y, w, h, tint(col, 0.08), tint(col, 0.45))
    r.line.dash_style = 4
    icon(s, ic, x + (w - 0.32) / 2, y + h / 2 - 0.5, 0.32, col)
    text(s, x + 0.03, y + h / 2 - 0.1, w - 0.06, 1.0,
         [[run(head, 11, True, col)], [run(what, 10.5, True, INK, TOOL)]], align=PP_ALIGN.CENTER, space=4)


def slide_stack(prs):
    s = new_slide(
        prs,
        "Software Architecture Stack: Was jeder Baustein tut",
        "Die Bausteine des Stacks: was sie tun, ein Beispiel aus der App und warum wir sie gewählt haben.",
        "Oben das Backend: TypeScript, Next.js und Node.js tragen alles. Darunter die Kette jeder Anfrage: "
        "Better Auth, Zod, Data Access Layer und Prisma/Drizzle. Links übergibt das Frontend (andere Gruppe), "
        "rechts geht es an die Datenbank (nächster Teil).",
    )
    # Zwei Reihen: 3 Fundament-Karten (Backend) über der Kette jeder Anfrage, senkrecht mittig unter dem Untertitel
    zl, bh, zg, rh = 0.32, 2.4, 0.4, 2.85
    y0 = 1.38 + (7.35 - 1.38 - (zl + bh + zg + rh)) / 2
    top_base = y0 + zl
    y1, rw, rg = top_base + bh + zg + rh, 1.05, 0.34
    handover(s, 0.5, top_base, rw, y1 - top_base, "monitor", "Frontend", "React-Seiten", S1)
    dbx = 12.833 - rw
    handover(s, dbx, top_base, rw, y1 - top_base, "database", "Datenbank", "PostgreSQL", S3)
    x0, x1 = 0.5 + rw + rg, dbx - rg
    sw = x1 - x0

    # Reihe 1: Sprache, Framework, Laufzeit als einzelne dunkle Karten
    bg = 0.26
    bw = (sw - 2 * bg) / 3
    zone(s, x0, top_base - 0.3, sw, "Backend · Grundlage für jede Anfrage", INK, "server", size=13)
    row = ["ts", "next", "node"]
    n = max(line_count(STACK[k][4], bw - 0.28, 10.5) for k in row)  # 0.28 = 2 × Innenabstand p der Karte
    for j, key in enumerate(row):
        stack_card(s, x0 + j * (bw + bg), top_base, bw, bh, key, n)

    # Reihe 2: Kette jeder Anfrage mit Pfeilen
    ag = 0.26
    cw = (sw - 3 * ag) / 4
    y = top_base + bh + zg
    zone(s, x0, y - 0.3, sw, "Jede Anfrage", S2, "shield-check", size=13)
    row = ["auth", "zod", "dal", "orm"]
    n = max(line_count(STACK[k][4], cw - 0.28, 10.5) for k in row)
    for j, key in enumerate(row):
        x = x0 + j * (cw + ag)
        stack_card(s, x, y, cw, rh, key, n)
        if j:
            arrow(s, x - ag + 0.03, y + rh / 2, x - 0.03, y + rh / 2, S2, width=2.5)
    mid = y + rh / 2

    # Übergaben: Frontend → erste Karte, ORM ↔ Datenbank (SQL)
    arrow(s, 0.5 + rw + 0.03, mid, x0 - 0.03, mid, S1, width=2.5)
    arrow(s, x1 + 0.03, mid, dbx - 0.03, mid, S3, both=True, width=2.5)
    text(s, x1 - 0.06, mid - 0.3, rg + 0.12, 0.22, [[run("SQL", 10.5, True, S3)]], align=PP_ALIGN.CENTER)


def main():
    global LANG
    for LANG in ("de", "en"):
        prs = Presentation()
        prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)  # 16:9, 13,333 × 7,5 Zoll
        slide_request(prs)
        slide_stack(prs)
        prs.core_properties.title = tr("App-Architektur")
        prs.core_properties.language = {"de": "de-DE", "en": "en-US"}[LANG]
        prs.save(OUT[LANG])
        print(OUT[LANG])
    print("ohne Übersetzung:", sorted(MISSING))


if __name__ == "__main__":
    main()
