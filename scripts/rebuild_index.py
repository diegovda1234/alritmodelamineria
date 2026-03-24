"""
rebuild_index.py — Reconstruye index.html desde el backup del 17/03
agregando Ed004 y actualizando precios/secciones.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "C:/Users/diego.varleta/CLAUDE/Noticiero_Minero"

with open(f"{BASE}/index_backup_17mar.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. SEMAFORO DE PRECIOS ────────────────────────────────────────────────────
signal_replacements = [
    ('$5.75/lb',    '$5.45/lb'),
    ('$20.3k/t',    '$24.1k/t'),
    ('$108.6/kg',   '$103/kg'),
    ('$1,650/oz',   '$1,905/oz'),
    ('$5,025/oz',   '$4,419/oz'),
    ('$80.1/oz',    '$69.5/oz'),
    ('$908',        '$915'),
    ('>+1.2%<',     '>-3.8%<'),   # cobre variacion
    ('>+2.1%<',     '>+18.9%<'),  # litio variacion
    ('>+3.2%<',     '>-3.0%<'),   # NdPr variacion
    ('>+2.5%<',     '>+15.5%<'),  # platino variacion
    ('>-3.4%<',     '>-12.1%<'),  # oro variacion
    ('>-4.7%<',     '>-13.2%<'),  # plata variacion
    ('>+2.7%<',     '>+0.0%<'),   # cobalto variacion
    # Cambiar dot de cobre a down
    ('signal-dot up"></span>\n            <span class="signal-label">Cobre',
     'signal-dot down"></span>\n            <span class="signal-label">Cobre'),
    # Cambiar dot de NdPr a down
    ('signal-dot up"></span>\n            <span class="signal-label">NdPr',
     'signal-dot down"></span>\n            <span class="signal-label">NdPr'),
    # Cambiar dot de oro a down (ya estaba)
    # Cambiar dot de plata a down (ya estaba)
]
for old, new in signal_replacements:
    html = html.replace(old, new)

# ── 2. LO QUE VIENE ──────────────────────────────────────────────────────────
old_items = [
    '<li><span class="uc-date">17-27 Mar</span> Primera consulta Chile-EEUU sobre minerales criticos y tierras raras</li>',
    '<li><span class="uc-date">19 Mar</span> Vence plazo de comentarios USTR sobre acuerdo de minerales criticos</li>',
    '<li><span class="uc-date">31 Mar</span> Cumbre Trump-Xi en China &mdash; minerales criticos en agenda</li>',
    '<li><span class="uc-date">Abr 2026</span> Inicio negociaciones EEUU-UE-Japon en minerales criticos</li>',
    '<li><span class="uc-date">8-11 Jun</span> EXPONOR 2026, Antofagasta &mdash; principal feria minera de Chile</li>',
]
new_items = [
    '<li><span class="uc-date">~27 Mar</span> Primera consulta tecnica Chile-EEUU sobre minerales criticos (plazo del acuerdo 12/03)</li>',
    '<li><span class="uc-date">26 Mar</span> Sube diesel Chile +CLP 580/litro &mdash; impacto inmediato en costos faenas</li>',
    '<li><span class="uc-date">Fines Abr</span> Cumbre Trump-Xi (postergada) &mdash; minerales criticos en agenda</li>',
    '<li><span class="uc-date">Jun 2026</span> Ingreso EIA Salar Futuro (Novandino Codelco-SQM) al SEIA</li>',
    '<li><span class="uc-date">8-11 Jun</span> EXPONOR 2026, Antofagasta &mdash; principal feria minera de Chile</li>',
]
for old, new in zip(old_items, new_items):
    html = html.replace(old, new)

# ── 3. FRASE DE LA SEMANA ────────────────────────────────────────────────────
html = html.replace(
    'Si China reinstala los controles de exportacion de tierras raras despues de la cumbre, los fabricantes de imanes permanentes fuera de China tienen menos de 5 meses de inventario.',
    'Las tarifas TC/RC del cobre llegaron a cero por primera vez en la historia. Las fundidoras prefieren perder el margen antes que apagar la planta &mdash; el concentrado es tan escaso que parar y relanzar cuesta decenas de millones.'
)
html = html.replace(
    '&mdash; Analisis IEA sobre controles de exportacion de REE, marzo 2026',
    '&mdash; Analisis IEA / Financial Content, 23 de marzo 2026'
)

# ── 4. BADGE DE ED003: NUEVA → Ed. 003 ───────────────────────────────────────
html = html.replace(
    '<span class="badge latest">NUEVA</span>',
    '<span class="badge">Ed. 003</span>',
    1
)

# ── 5. INSERTAR ED004 AL INICIO DEL CARD-LIST ────────────────────────────────
svg_doc = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
svg_book = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>'

ed004_card = f"""        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">Edicion N. 4 &mdash; Semana del 18 al 24 de marzo</div>
                    <div class="card-meta">Publicado: 24/03/2026</div>
                </div>
                <span class="badge latest">NUEVA</span>
            </div>
            <div class="card-emphasis">China confirma el 2\xb0 mayor yacimiento REE del mundo (Maoniuping, 10.4 Mt); TC/RC del cobre llegan a cero por primera vez en la historia; oro cae 12% en la peor semana desde 1983; BHP ingresa US$5.500M al SEIA.</div>
            <ul class="card-bullets">
                <li><span class="tag">[TRR]</span> China: Maoniuping 2\xb0 mayor yacimiento REE del mundo</li>
                <li><span class="tag">[Cu]</span> TC/RC a cero &mdash; deficit global 330.000 t</li>
                <li><span class="tag">[Au]</span> Oro cae 12% &mdash; peor semana desde 1983</li>
                <li><span class="tag">[Chile]</span> BHP ingresa concentradora Escondida al SEIA US$5.5B</li>
                <li><span class="tag">[Li]</span> Litio rebota +18.9% a US$24k/t</li>
            </ul>
            <div class="card-actions">
                <a class="card-btn primary" href="Noticiero_Minero_Ed004_2026-03-24.html">{svg_doc} Informe</a>
                <a class="card-btn secondary" href="escuela.html">{svg_book} Clase: TC/RC y la cadena del cobre</a>
            </div>
        </div>
"""

html = html.replace(
    '    <div class="card-list">\n\n        <div class="card">',
    '    <div class="card-list">\n\n' + ed004_card + '        <div class="card">'
)

# ── 6. ELIMINAR ED001 DEL CARD-LIST PRINCIPAL ────────────────────────────────
# Buscar y eliminar el bloque completo de Ed001
start_marker = '        <div class="card">\n\n            <div class="card-header">\n\n                <div>\n\n                    <div class="card-title">Edicion N. 1'
end_marker = 'Clase: Costos C1, C2 y AISC</a>\n\n            </div>\n\n        </div>'

idx_start = html.find(start_marker)
idx_end = html.find(end_marker)
if idx_start != -1 and idx_end != -1:
    ed001_block = html[idx_start:idx_end + len(end_marker)]
    html = html.replace(ed001_block, '')
    print("Ed001 removida del card-list OK")
else:
    print(f"WARNING: Ed001 block not found. start={idx_start}, end={idx_end}")

# ── 7. ACTUALIZAR CONTADOR Y CONTENIDO DE EDICIONES ANTERIORES ───────────────
html = html.replace(
    '(0 mas)',
    '(1 mas)'
)
html = html.replace(
    '<div style="padding:16px 18px;text-align:center;font-size:12px;color:var(--muted);">Todas las ediciones estan visibles arriba.</div>',
    '<div style="display:flex;justify-content:space-between;align-items:center;padding:12px 18px;border-bottom:1px solid var(--rule);"><span style="font-size:13px;color:var(--text);">Ed. 001 &mdash; Semana 06-12 Mar &middot; Edicion inaugural</span><a href="Noticiero_Minero_Ed001_2026-03-12.html" style="font-size:12px;color:var(--copper);text-decoration:none;font-weight:600;">Ver &rarr;</a></div>'
)

# ── 8. FOOTER ────────────────────────────────────────────────────────────────
html = html.replace(
    'Actualizado el 17/03/2026',
    'Actualizado el 24/03/2026'
)

# ── GUARDAR ──────────────────────────────────────────────────────────────────
with open(f"{BASE}/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"index.html guardado OK. Largo: {len(html)} chars")
print("Ed004 presente:", "Edicion N. 4" in html)
print("Nav links presentes:", "escuela.html" in html and "proyecciones.html" in html and "precios.html" in html)
print("Precios actualizados:", "$5.45/lb" in html and "$4,419/oz" in html)
