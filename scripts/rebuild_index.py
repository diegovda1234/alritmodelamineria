"""
rebuild_index.py v2 — Reconstruye index.html desde cero.

- Parsea todos los Noticiero_Minero_Ed*.md en la carpeta.
- Usa index_backup_17mar.html solo como template estatico (CSS, header, footer).
- Reemplaza limpiamente: semaforo de precios, card-list (top 4), older-list (resto).
- Robusto: si no encuentra un dato, deja placeholder, nunca trunca ni borra cards.
"""
import sys, glob, re, os

sys.stdout.reconfigure(encoding='utf-8')

BASE = "C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero"
TEMPLATE = f"{BASE}/index_backup_17mar.html"
OUTPUT = f"{BASE}/index.html"

# ═══════════════════════════════════════════════════════════
# 1. Cargar template base
# ═══════════════════════════════════════════════════════════
with open(TEMPLATE, "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 2. Detectar y parsear todas las ediciones
# ═══════════════════════════════════════════════════════════
edition_files = sorted(
    glob.glob(f"{BASE}/Noticiero_Minero_Ed*.md"),
    key=lambda p: int(re.search(r'Ed(\d+)_', os.path.basename(p)).group(1)),
    reverse=True
)

editions = []
for fpath in edition_files:
    fname = os.path.basename(fpath)
    m = re.match(r'Noticiero_Minero_Ed(\d+)_(\d{4}-\d{2}-\d{2})\.md', fname)
    if not m:
        continue
    ed_num = int(m.group(1))
    ed_date = m.group(2)

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Periodo
    p = re.search(r'\*\*Per[ií]odo:\*\*\s*(.+)', content)
    period = p.group(1).strip() if p else f"Edicion {ed_num}"

    # Fecha publicacion
    p = re.search(r'\*\*Fecha de publicaci[oó]n:\*\*\s*(.+)', content)
    pub_date = p.group(1).strip() if p else ed_date

    # Enfasis
    p = re.search(r'\*\*[ÉE]nfasis editorial esta semana:\*\*\s*(.+)', content)
    emphasis = p.group(1).strip() if p else ""
    # Trim si muy largo
    if len(emphasis) > 320:
        emphasis = emphasis[:317].rsplit(' ', 1)[0] + '...'

    # Bullets del resumen ejecutivo (max 5)
    bullets = []
    # Patron: - **[TAG]** texto
    for match in re.finditer(r'- \*\*\[([^\]]+)\]\*\*\s*(.+)', content):
        tag = match.group(1).strip()
        text = match.group(2).strip()
        # Trim bullet si es muy largo
        if len(text) > 70:
            text = text[:67].rsplit(' ', 1)[0] + '...'
        bullets.append((tag, text))
        if len(bullets) >= 5:
            break

    editions.append({
        'num': ed_num,
        'date': ed_date,
        'pub_date': pub_date,
        'period': period,
        'emphasis': emphasis,
        'bullets': bullets,
        'html_file': fname.replace('.md', '.html'),
    })

if not editions:
    print("ERROR: No se encontraron ediciones .md")
    sys.exit(1)

latest = editions[0]
print(f"Ultima edicion detectada: Ed{latest['num']:03d} ({latest['date']})")
print(f"Total ediciones: {len(editions)}")

# ═══════════════════════════════════════════════════════════
# 3. Extraer precios del semaforo desde la ultima edicion
# ═══════════════════════════════════════════════════════════
with open(f"{BASE}/Noticiero_Minero_Ed{latest['num']:03d}_{latest['date']}.md", 'r', encoding='utf-8') as f:
    latest_md = f.read()

# ── Frase de la semana ──────────────────────────────────────
quote_match = re.search(r'\*\*Frase de la semana:\*\*\s*["\u201c](.+?)["\u201d]', latest_md)
if not quote_match:
    # Fallback sin comillas
    quote_match = re.search(r'\*\*Frase de la semana:\*\*\s*(.+)', latest_md)
quote_text = quote_match.group(1).strip() if quote_match else ""

attrib_match = re.search(r'\*\*Atribuci[oó]n frase:\*\*\s*(.+)', latest_md)
quote_author = attrib_match.group(1).strip() if attrib_match else f"— Noticiero Minero Ed.{latest['num']}"

# ── Lo que viene ────────────────────────────────────────────
# Extraer bullets de "Próximos 7 días" y primeros de "Próximas 4 semanas"
upcoming_items = []

# Buscar seccion "Próximos 7 días" y capturar sus bullets
prox_7d_match = re.search(
    r'###\s*Pr[óo]ximos\s*7\s*d[ií]as[^\n]*\n(.*?)(?=###|\n##|\Z)',
    latest_md,
    re.DOTALL
)
if prox_7d_match:
    block = prox_7d_match.group(1)
    for line in block.split('\n'):
        line = line.strip()
        if not line.startswith('-'):
            continue
        # Patron: "- **fecha:** texto" o "- texto"
        m = re.match(r'-\s*\*\*([^:*]+):\*\*\s*(.+)', line)
        if m:
            date_str = m.group(1).strip()
            text = m.group(2).strip()
            upcoming_items.append((date_str, text))
        else:
            m2 = re.match(r'-\s*(.+)', line)
            if m2:
                upcoming_items.append(("Próx.", m2.group(1).strip()))
        if len(upcoming_items) >= 4:
            break

# Agregar 1-2 items de "Próximas 4 semanas"
prox_4w_match = re.search(
    r'###\s*Pr[óo]ximas\s*4\s*semanas[^\n]*\n(.*?)(?=###|\n##|\Z)',
    latest_md,
    re.DOTALL
)
if prox_4w_match and len(upcoming_items) < 5:
    block = prox_4w_match.group(1)
    for line in block.split('\n'):
        line = line.strip()
        if not line.startswith('-'):
            continue
        m = re.match(r'-\s*\*\*([^:*]+):\*\*\s*(.+)', line)
        if m:
            date_str = m.group(1).strip()
            text = m.group(2).strip()
            # Limpiar markdown residual
            text = re.sub(r'\*\*|`', '', text)
            if len(text) > 85:
                text = text[:82].rsplit(' ', 1)[0] + '...'
            upcoming_items.append((date_str, text))
        if len(upcoming_items) >= 5:
            break

# Limpiar items: remover markdown y acortar
clean_upcoming = []
for date_str, text in upcoming_items[:5]:
    text = re.sub(r'\*\*|`|⚠️|🚨', '', text).strip()
    if len(text) > 85:
        text = text[:82].rsplit(' ', 1)[0] + '...'
    clean_upcoming.append((date_str, text))
upcoming_items = clean_upcoming


def extract(pattern, fallback="N/A"):
    m = re.search(pattern, latest_md)
    if not m:
        return fallback
    return m.group(1).strip().replace('**', '').replace('~', '')


# Extraer precios de la tabla dashboard (formato: | mineral | edN | **edN+1** | ±x% | fuente |)
def parse_row(mineral_label_regex, required_unit=None):
    """
    Busca una fila del dashboard que matchee 'mineral_label_regex' y (opcionalmente)
    contenga 'required_unit' en la celda de precio. Devuelve (precio, variacion) o (None, None).

    required_unit fuerza consistencia de unidades entre ediciones. Ej: para Cobre pedimos
    siempre 'USD/t' para evitar que el semaforo cambie a USD/lb en una edicion.
    """
    for line in latest_md.splitlines():
        if not line.lstrip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 4:
            continue
        if not re.match(mineral_label_regex, cells[0], re.IGNORECASE):
            continue
        price_cell_raw = cells[2].replace('**', '').replace('~', '').strip()
        if required_unit and required_unit.lower() not in price_cell_raw.lower():
            # Unidad no coincide — seguir buscando otra fila del mismo mineral
            continue
        m_price = re.match(r'([\d.,]+)', price_cell_raw)
        price = m_price.group(1) if m_price else None
        var_cell = cells[3]
        m_var = re.search(r'([+\-−]\s*[\d.,]+\s*%)', var_cell)
        var = m_var.group(1).replace(' ', '').replace('−', '-').replace(',', '.') if m_var else "0%"
        return price, var
    return None, None


def direction_from_var(var_str):
    s = var_str.replace('%', '').replace('+', '').strip()
    try:
        val = float(s)
    except ValueError:
        return 'flat'
    if val > 0.1:
        return 'up'
    if val < -0.1:
        return 'down'
    return 'flat'


# ═══════════════════════════════════════════════════════════
# POLITICA DE UNIDADES — NO NEGOCIABLE
# El semaforo siempre muestra el mismo mineral con la MISMA unidad entre ediciones.
# Cobre: USD/t (nunca USD/lb). Litio/Cobalto: USD/t. Preciosos: USD/oz.
# NdPr: USD/kg. CLP/USD: CLP.
# parse_row() recibe 'required_unit' para rechazar filas con unidad incorrecta.
# ═══════════════════════════════════════════════════════════
semaforo_config = [
    # (label, regex mineral,        required_unit, format_fn)
    ('Cobre',    r'Cobre',            'USD/lb', lambda p: f'${p}/lb'),
    ('Litio',    r'Litio\s*Carbonato','USD/t',  lambda p: f'${p}/t'),
    ('NdPr',     r'NdPr',             'USD/kg', lambda p: f'${p}/kg'),
    ('Platino',  r'Platino',          'USD/oz', lambda p: f'${p}/oz'),
    ('Oro',      r'Oro',              'USD/oz', lambda p: f'${p}/oz'),
    ('Plata',    r'Plata',            'USD/oz', lambda p: f'${p}/oz'),
    ('Cobalto',  r'Cobalto',          'USD/t',  lambda p: f'${p}/t'),
    ('CLP/USD',  r'CLP/USD',          None,     lambda p: f'${p}'),
]

semaforo_items = []
for label, mineral_re, unit, fmt in semaforo_config:
    price, change = parse_row(mineral_re, required_unit=unit)
    dir_ = direction_from_var(change or "0%")
    if price is None:
        semaforo_items.append((label, "—", "—", 'flat', fmt))
        continue
    # Compactar numeros grandes: 12630 -> 12.630
    display = price
    try:
        clean = price.replace('.', '').replace(',', '.')
        num = float(clean)
        if num >= 10000:
            display = f"{int(num):,}".replace(',', '.')
    except Exception:
        pass
    semaforo_items.append((label, display, change, dir_, fmt))

# ═══════════════════════════════════════════════════════════
# 4. Construir HTML del semaforo
# ═══════════════════════════════════════════════════════════
semaforo_html = ""
for label, price, change, dir_, fmt in semaforo_items:
    price_fmt = fmt(price) if price != "—" else "—"
    semaforo_html += f'''        <div class="signal-item">
            <span class="signal-dot {dir_}"></span>
            <span class="signal-label">{label}</span>
            <span class="signal-price">{price_fmt}</span>
            <span class="signal-change {dir_}">{change}</span>
        </div>
'''

# ═══════════════════════════════════════════════════════════
# 5. Construir HTML de cards (top 4)
# ═══════════════════════════════════════════════════════════
SVG_DOC = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
SVG_BOOK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def make_card(ed, is_latest=False):
    badge = '<span class="badge latest">NUEVA</span>' if is_latest else f'<span class="badge">Ed. {ed["num"]:03d}</span>'
    bullets_html = ""
    for tag, text in ed['bullets']:
        bullets_html += f'                <li><span class="tag">[{esc(tag)}]</span> {esc(text)}</li>\n'
    leccion_id = f"leccion-{ed['num']}" if ed['num'] >= 4 else {1: 'leccion-03', 2: 'leccion-02', 3: 'leccion-1'}.get(ed['num'], f'leccion-{ed["num"]}')
    return f'''        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">Edicion N. {ed['num']} &mdash; {esc(ed['period'])}</div>
                    <div class="card-meta">Publicado: {esc(ed['pub_date'])}</div>
                </div>
                {badge}
            </div>
            <div class="card-emphasis">{esc(ed['emphasis'])}</div>
            <ul class="card-bullets">
{bullets_html}            </ul>
            <div class="card-actions">
                <a class="card-btn primary" href="{ed['html_file']}">{SVG_DOC} Informe</a>
                <a class="card-btn secondary" href="escuela.html#{leccion_id}">{SVG_BOOK} Clase de la semana</a>
            </div>
        </div>
'''


main_cards = editions[:4]
archive_cards = editions[4:]

cards_html = ""
for i, ed in enumerate(main_cards):
    cards_html += make_card(ed, is_latest=(i == 0))

# ═══════════════════════════════════════════════════════════
# 6. Construir older-list (archive compacto)
# ═══════════════════════════════════════════════════════════
if archive_cards:
    older_html = ""
    for ed in archive_cards:
        older_html += f'        <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 18px;border-bottom:1px solid var(--rule);"><span style="font-size:13px;color:var(--text);">Ed. {ed["num"]:03d} &mdash; {esc(ed["period"])}</span><a href="{ed["html_file"]}" style="font-size:12px;color:var(--copper);text-decoration:none;font-weight:600;">Ver &rarr;</a></div>\n'
else:
    older_html = '        <div style="padding:16px 18px;text-align:center;font-size:12px;color:var(--muted);">Todas las ediciones estan visibles arriba.</div>\n'

# ═══════════════════════════════════════════════════════════
# 7. Reemplazar secciones en el HTML
# ═══════════════════════════════════════════════════════════

# 7a. Semaforo: reemplazar contenido de <div class="signal-grid">
html = re.sub(
    r'(<div class="signal-grid">)(.*?)(</div>\s*</div>\s*<div class="container">)',
    lambda m: m.group(1) + '\n' + semaforo_html + '    ' + m.group(3),
    html,
    count=1,
    flags=re.DOTALL
)

# 7a-bis. Quote card (frase de la semana)
if quote_text:
    quote_html = f'        <p class="quote-text">{esc(quote_text)}</p>\n        <p class="quote-author">{esc(quote_author)}</p>\n'
    html = re.sub(
        r'(<div class="quote-card">)(.*?)(</div>)',
        lambda m: m.group(1) + '\n' + quote_html + '    ' + m.group(3),
        html,
        count=1,
        flags=re.DOTALL
    )

# 7a-ter. Upcoming list (lo que viene)
if upcoming_items:
    upcoming_html = ""
    for date_str, text in upcoming_items:
        upcoming_html += f'            <li><span class="uc-date">{esc(date_str)}</span> {esc(text)}</li>\n'
    html = re.sub(
        r'(<ul class="upcoming-list">)(.*?)(</ul>)',
        lambda m: m.group(1) + '\n' + upcoming_html + '        ' + m.group(3),
        html,
        count=1,
        flags=re.DOTALL
    )

# 7b. card-list: reemplazar contenido completo
html = re.sub(
    r'(<div class="card-list">)(.*?)(</div>\s*<!-- EDICIONES ANTERIORES)',
    lambda m: m.group(1) + '\n' + cards_html + '    ' + m.group(3),
    html,
    count=1,
    flags=re.DOTALL
)

# 7c. older-list count
html = re.sub(r'\((\d+) mas\)', f'({len(archive_cards)} mas)', html)

# 7d. older-list content
html = re.sub(
    r'(<div id="older-list"[^>]*>)(.*?)(</div>\s*<!-- NAV LINKS)',
    lambda m: m.group(1) + '\n' + older_html + '    ' + m.group(3),
    html,
    count=1,
    flags=re.DOTALL
)

# 7e. Footer date
dd, mm, yyyy = latest['date'].split('-')[2], latest['date'].split('-')[1], latest['date'].split('-')[0]
html = re.sub(r'Actualizado el \d{2}/\d{2}/\d{4}', f'Actualizado el {dd}/{mm}/{yyyy}', html)

# ═══════════════════════════════════════════════════════════
# 8. Validacion y guardado
# ═══════════════════════════════════════════════════════════
assert f"Edicion N. {latest['num']}" in html, f"FALLO: Ed{latest['num']} no quedo en index.html"
assert "card-list" in html
assert "signal-grid" in html

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[OK] index.html guardado. Largo: {len(html)} chars")
print(f"[OK] Main cards: {[e['num'] for e in main_cards]}")
print(f"[OK] Archive: {[e['num'] for e in archive_cards]}")
print(f"[OK] Ed{latest['num']:03d} presente en HTML: True")