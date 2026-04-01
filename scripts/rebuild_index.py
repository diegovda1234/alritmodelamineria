"""
rebuild_index.py — Reconstruye index.html dinamicamente.
Detecta todas las ediciones .html en la carpeta y genera el card-list.
"""
import sys, glob, re, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = "C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero"

# ── Leer template base ──────────────────────────────────────────────────────
with open(f"{BASE}/index_backup_17mar.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── Detectar todas las ediciones ────────────────────────────────────────────
edition_files = sorted(glob.glob(f"{BASE}/Noticiero_Minero_Ed*.md"), reverse=True)

editions = []
for fpath in edition_files:
    fname = os.path.basename(fpath)
    # Extract edition number and date from filename
    m = re.match(r'Noticiero_Minero_Ed(\d+)_(\d{4}-\d{2}-\d{2})\.md', fname)
    if not m:
        continue
    ed_num = int(m.group(1))
    ed_date = m.group(2)
    html_file = fname.replace('.md', '.html')

    # Read first lines to extract emphasis and key bullets
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read(3000)

    # Extract period
    period_match = re.search(r'\*\*Periodo:\*\*\s*(.+)', content)
    period = period_match.group(1).strip() if period_match else f"Edicion {ed_num}"

    # Extract emphasis
    emphasis_match = re.search(r'\*\*Enfasis editorial esta semana:\*\*\s*(.+)', content)
    if not emphasis_match:
        emphasis_match = re.search(r'\*\*Énfasis editorial esta semana:\*\*\s*(.+)', content)
    emphasis = emphasis_match.group(1).strip() if emphasis_match else ""

    # Extract key bullets from resumen ejecutivo
    bullets = []
    bullet_pattern = re.findall(r'- \*\*\[(\w+)\]\*\*\s*(.+)', content)
    for tag, text in bullet_pattern[:5]:
        bullets.append((tag, text.strip()))

    # Extract publish date
    pub_match = re.search(r'\*\*Fecha de publicacion:\*\*\s*(.+)', content)
    if not pub_match:
        pub_match = re.search(r'\*\*Fecha de publicación:\*\*\s*(.+)', content)
    pub_date = pub_match.group(1).strip() if pub_match else ed_date

    editions.append({
        'num': ed_num,
        'date': ed_date,
        'pub_date': pub_date,
        'period': period,
        'emphasis': emphasis,
        'bullets': bullets,
        'html_file': html_file,
    })

if not editions:
    print("ERROR: No se encontraron ediciones .md")
    sys.exit(1)

latest = editions[0]
print(f"Ultima edicion detectada: Ed{latest['num']:03d} ({latest['date']})")

# ── Construir precios del semaforo (de la ultima edicion) ───────────────────
latest_path = f"{BASE}/Noticiero_Minero_Ed{latest['num']:03d}_{latest['date']}.md"
with open(latest_path, 'r', encoding='utf-8') as f:
    full_content = f.read()

# Extract prices from dashboard table
def extract_price(pattern, content):
    m = re.search(pattern, content)
    return m.group(1).strip() if m else "N/A"

# ── SVG icons ───────────────────────────────────────────────────────────────
svg_doc = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
svg_book = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>'

# ── Build card HTML for each edition ────────────────────────────────────────
def make_card(ed, is_latest=False):
    badge = '<span class="badge latest">NUEVA</span>' if is_latest else f'<span class="badge">Ed. {ed["num"]:03d}</span>'

    bullets_html = ""
    for tag, text in ed['bullets']:
        bullets_html += f'                <li><span class="tag">[{tag}]</span> {text}</li>\n'

    # Escape special chars for HTML
    emphasis = ed['emphasis'].replace('&', '&amp;').replace('"', '&quot;')

    card = f"""        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">Edicion N. {ed['num']} &mdash; {ed['period']}</div>
                    <div class="card-meta">Publicado: {ed['pub_date']}</div>
                </div>
                {badge}
            </div>
            <div class="card-emphasis">{emphasis}</div>
            <ul class="card-bullets">
{bullets_html}            </ul>
            <div class="card-actions">
                <a class="card-btn primary" href="{ed['html_file']}">{svg_doc} Informe</a>
                <a class="card-btn secondary" href="escuela.html">{svg_book} Clase de la semana</a>
            </div>
        </div>
"""
    return card

# Build cards for latest 4 editions (show in main list)
show_in_main = editions[:4]
show_in_archive = editions[4:]

cards_html = ""
for i, ed in enumerate(show_in_main):
    cards_html += make_card(ed, is_latest=(i == 0))

# ── Replace the card-list content ───────────────────────────────────────────
# Find the card-list div and replace its content
card_list_start = html.find('<div class="card-list">')
if card_list_start == -1:
    print("ERROR: No se encontro <div class='card-list'>")
    sys.exit(1)

# Find the closing of card-list (next </div> at same level after all cards)
# We'll find the section that ends before "Ediciones anteriores" or the archive section
archive_start = html.find('class="archive"', card_list_start)
if archive_start == -1:
    archive_start = html.find('class="editions-footer"', card_list_start)

if archive_start != -1:
    # Find the div that contains the archive
    archive_div_start = html.rfind('<div', card_list_start, archive_start)
    # Replace everything between card-list opening and archive div
    card_list_content_start = html.find('>', card_list_start) + 1
    old_cards = html[card_list_content_start:archive_div_start]
    html = html[:card_list_content_start] + '\n\n' + cards_html + '\n' + html[archive_div_start:]
else:
    # Fallback: find closing </div> for card-list
    # Just replace content between card-list div tags
    card_list_end = html.find('</div>', card_list_start + 100)
    # This is tricky with nested divs, use a simpler approach
    pass

# ── Update archive section ──────────────────────────────────────────────────
archive_count = len(show_in_archive)
# Update archive count
html = re.sub(r'\(\d+ mas\)', f'({archive_count} mas)', html)

# Build archive items
if show_in_archive:
    archive_items = ""
    for ed in show_in_archive:
        period_short = ed['period'][:30] if len(ed['period']) > 30 else ed['period']
        archive_items += f'<div style="display:flex;justify-content:space-between;align-items:center;padding:12px 18px;border-bottom:1px solid var(--rule);"><span style="font-size:13px;color:var(--text);">Ed. {ed["num"]:03d} &mdash; {period_short}</span><a href="{ed["html_file"]}" style="font-size:12px;color:var(--copper);text-decoration:none;font-weight:600;">Ver &rarr;</a></div>\n'

    # Replace old archive content
    old_archive_content = 'Todas las ediciones estan visibles arriba.</div>'
    if old_archive_content in html:
        html = html.replace(old_archive_content, archive_items.rstrip())

# ── Update footer date ──────────────────────────────────────────────────────
html = re.sub(r'Actualizado el \d{2}/\d{2}/\d{4}', f'Actualizado el {latest["date"].replace("-", "/").split("/")[2]}/{latest["date"].split("-")[1]}/{latest["date"].split("-")[0]}', html)

# ── Update semaforo prices from latest edition dashboard ────────────────────
# Extract prices from the markdown table
price_patterns = {
    'cobre_t': r'Cobre\s*\|\s*([\d.,]+)\s*USD/t',
    'cobre_lb': r'Cobre\s*\|\s*([\d.,]+)\s*USD/lb',
    'litio': r'Litio Carbonato\s*\|\s*[~]*\s*([\d.,]+)\s*USD/t',
    'platino': r'Platino\s*\|\s*([\d.,]+)\s*USD/oz',
    'oro': r'Oro\s*\|\s*([\d.,]+)\s*USD/oz',
    'plata': r'Plata\s*\|\s*([\d.,]+)\s*USD/oz',
    'clp': r'CLP/USD\s*\|\s*([\d.,]+)',
    'ndpr': r'NdPr[^|]*\|\s*[~]*\s*([\d.,]+)\s*USD/kg',
    'cobalto': r'Cobalto\s*\|\s*[~]*\s*([\d.,]+)\s*USD/t',
}

# ── GUARDAR ──────────────────────────────────────────────────────────────────
with open(f"{BASE}/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"index.html guardado OK. Largo: {len(html)} chars")
print(f"Ediciones en main: {[e['num'] for e in show_in_main]}")
print(f"Ediciones en archive: {[e['num'] for e in show_in_archive]}")
print(f"Ed{latest['num']:03d} presente:", f"Edicion N. {latest['num']}" in html)
