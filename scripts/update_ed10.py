"""
update_ed10.py — Actualiza precios.html, proyecciones.html e index.html para Ed.010
Ejecutar desde: C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero/
"""

import re

BASE = "C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero"

# ─── 1. precios.html ──────────────────────────────────────────────────────────

print("[1/3] Actualizando precios.html...")
f = f'{BASE}/precios.html'
with open(f, encoding='utf-8') as fh:
    html = fh.read()

# Agregar Ed.10 a EDITIONS
html = html.replace(
    "    { id: 9, label: 'Ed.9', date: '28/04' }\n];",
    "    { id: 9, label: 'Ed.9', date: '28/04' },\n    { id: 10, label: 'Ed.10', date: '05/05' }\n];"
)

# Cobre USD/t
html = html.replace(
    "prices: [12400, 12530, 12678, 12201, 12200, 12424, 12630, 13320, 13076]",
    "prices: [12400, 12530, 12678, 12201, 12200, 12424, 12630, 13320, 13076, 13007]"
)
# Cobre USD/lb
html = html.replace(
    "prices: [5.63, 5.68, 5.75, 5.45, 5.55, 5.90, 5.81, 6.04, 5.93]",
    "prices: [5.63, 5.68, 5.75, 5.45, 5.55, 5.90, 5.81, 6.04, 5.93, 5.90]"
)
# Litio
html = html.replace(
    "prices: [18500, 19200, 20256, 24086, 20100, 21650, 21650, 22500, 24500]",
    "prices: [18500, 19200, 20256, 24086, 20100, 21650, 21650, 22500, 24500, 25790]"
)
# Platino
html = html.replace(
    "prices: [1580, 1610, 1650, 1905, 1978, 1991, 2044, 2074, 1959]",
    "prices: [1580, 1610, 1650, 1905, 1978, 1991, 2044, 2074, 1959, 1980]"
)
# Paladio
html = html.replace(
    "prices: [1640, 1655, 1685, 1388, 1523, 1501, 1507, 1576, 1490]",
    "prices: [1640, 1655, 1685, 1388, 1523, 1501, 1507, 1576, 1490, 1540]"
)
# Rodio
html = html.replace(
    "prices: [11200, 11500, 11700, 10000, 10250, 10350, 10100, 9800, 9900]",
    "prices: [11200, 11500, 11700, 10000, 10250, 10350, 10100, 9800, 9900, 10200]"
)
# NdPr
html = html.replace(
    "prices: [96.5, 102.0, 108.64, 108.64, 108.64, 124.87, 126.0, 126.0, 137.0]",
    "prices: [96.5, 102.0, 108.64, 108.64, 108.64, 124.87, 126.0, 126.0, 137.0, 126.0]"
)
# Cobalto
html = html.replace(
    "prices: [54800, 55500, 56290, 56290, 56290, 56290, 56290, 56290, 56290]",
    "prices: [54800, 55500, 56290, 56290, 56290, 56290, 56290, 56290, 56290, 56290]"
)
# Oro
html = html.replace(
    "prices: [5350, 5114, 5025, 4419, 4747, 4656, 4735, 4782, 4600]",
    "prices: [5350, 5114, 5025, 4419, 4747, 4656, 4735, 4782, 4600, 4527]"
)
# Plata
html = html.replace(
    "prices: [88.20, 83.97, 80.10, 69.54, 75.07, 72.26, 75.55, 79.50, 73.5]",
    "prices: [88.20, 83.97, 80.10, 69.54, 75.07, 72.26, 75.55, 79.50, 73.5, 73.96]"
)
# CLP/USD
html = html.replace(
    "prices: [885, 898, 908, 915, 924, 917, 902, 881, 889]",
    "prices: [885, 898, 908, 915, 924, 917, 902, 881, 889, 883]"
)
# H2SO4
html = html.replace(
    "prices: [149, 149, 149, 149, 140, 171, 246, 270, 300]",
    "prices: [149, 149, 149, 149, 140, 171, 246, 270, 300, 405]"
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(html)

print("  [OK] precios.html actualizado.")
print("  Ed.10 en EDITIONS:", "{ id: 10, label: 'Ed.10'" in html)
print("  Cobre 5.90:", "5.93, 5.90]" in html)
print("  Litio 25790:", "25790]" in html)
print("  NdPr 126:", "137.0, 126.0]" in html)
print("  H2SO4 405:", "300, 405]" in html)


# ─── 2. proyecciones.html ─────────────────────────────────────────────────────

print("\n[2/3] Actualizando proyecciones.html...")
f = f'{BASE}/proyecciones.html'
with open(f, encoding='utf-8') as fh:
    html = fh.read()

# Cobre USD/lb — spot y referencia de fecha
html = html.replace(
    '<tr class="highlight"><td>Cobre</td><td>5.93</td>',
    '<tr class="highlight"><td>Cobre</td><td>5.90</td>'
)
html = html.replace(
    '<tr class="highlight"><td>Cobre</td><td>13,076</td>',
    '<tr class="highlight"><td>Cobre</td><td>13,007</td>'
)
# Actualizar referencias de fecha 28/04 → 05/05 en filas de cobre
html = html.replace(
    '<td>LME 28/04 (-1.8% semanal, +24% YTD)</td>',
    '<td>LME 05/05 (-0.5% semanal, +22% YTD)</td>'
)
# Oro
html = html.replace(
    '<tr><td>Oro</td><td>',
    '<tr><td>Oro</td><td>'  # placeholder, use the actual values below
)
html = html.replace(
    '<td>Kitco 28/04 — correccion -7.5% semanal</td>',
    '<td>Kitco 05/05 — correccion -7.5% semanal</td>'
)
html = html.replace(
    '<tr><td>Plata</td><td>73.50</td>',
    '<tr><td>Plata</td><td>73.96</td>'
)
html = html.replace(
    '<td>Kitco 28/04 — correccion -7.5% semanal</td>',
    '<td>Kitco 05/05 — estabilizacion +0.6% semanal</td>'
)
html = html.replace(
    '<tr><td>Platino</td><td>1,959</td>',
    '<tr><td>Platino</td><td>1,980</td>'
)
html = html.replace(
    '<td>Kitco 28/04 — correccion -5.6% / deficit 4o ano</td>',
    '<td>Kitco 05/05 — recupera +1.1% / deficit 4o ano consecutivo</td>'
)
html = html.replace(
    '<tr><td>NdPr Oxido</td><td>137.00</td>',
    '<tr><td>NdPr Oxido</td><td>126.00</td>'
)
html = html.replace(
    '<td>MacroMicro 27/04 — +8.7% semanal, +40% YTD</td>',
    '<td>MacroMicro 05/05 — -8.0% semanal (toma ganancias), +37% YTD</td>'
)
html = html.replace(
    '<td>H2SO4 Chile</td><td>300</td>',
    '<td>H2SO4 Chile</td><td>405</td>'
)
html = html.replace(
    '<td>&#128680; S&P Global 15/04 — ban chino mayo + Ormuz</td>',
    '<td>&#128680; S&P Global 05/05 — doble shock: ban chino activo + Ormuz bloqueado</td>'
)
html = html.replace(
    '<td>Petroleo Brent</td><td>110</td>',
    '<td>Petroleo Brent</td><td>115</td>'
)
html = html.replace(
    '<td>Fortune 28/04 — +14.2% semanal por Ormuz</td>',
    '<td>Reuters 05/05 — +4.5% semanal, acumula +45% desde bloqueo Ormuz (4 mar)</td>'
)

# Actualizar gold row (la tabla tiene el valor de Oro separado)
# Buscar y reemplazar la fila de Oro
html = re.sub(
    r'(<tr><td>Oro</td><td>)4[,.]600(</td>)',
    r'\g<1>4,527\2',
    html
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(html)

print("  [OK] proyecciones.html actualizado.")
print("  Cobre 5.90:", '5.90' in html)
print("  NdPr 126:", '126.00' in html)
print("  H2SO4 405:", '405' in html)
print("  Brent 115:", '115' in html)


# ─── 3. index.html ───────────────────────────────────────────────────────────

print("\n[3/3] Actualizando index.html...")
f = f'{BASE}/index.html'
with open(f, encoding='utf-8') as fh:
    html = fh.read()

# 3a. Semáforo de precios
# Cobre: down → flat, $5,93 → $5,90, -1.8% → -0,5%
html = html.replace(
    '<span class="signal-dot down"></span>\n            <span class="signal-label">Cobre</span>\n            <span class="signal-price">$5,93/lb</span>\n            <span class="signal-change down">-1.8%</span>',
    '<span class="signal-dot flat"></span>\n            <span class="signal-label">Cobre</span>\n            <span class="signal-price">$5,90/lb</span>\n            <span class="signal-change flat">-0,5%</span>'
)
# Litio: up, $24.500 → $25.790, +8.9% → +5,3%
html = html.replace(
    '<span class="signal-price">$24.500/t</span>\n            <span class="signal-change up">+8.9%</span>',
    '<span class="signal-price">$25.790/t</span>\n            <span class="signal-change up">+5,3%</span>'
)
# NdPr: up → down, $137 → $126, +8.7% → -8,0%
html = html.replace(
    '<span class="signal-dot up"></span>\n            <span class="signal-label">NdPr</span>\n            <span class="signal-price">$137/kg</span>\n            <span class="signal-change up">+8.7%</span>',
    '<span class="signal-dot down"></span>\n            <span class="signal-label">NdPr</span>\n            <span class="signal-price">$126/kg</span>\n            <span class="signal-change down">-8,0%</span>'
)
# Platino: down → up, $1.959 → $1.980, -5.6% → +1,1%
html = html.replace(
    '<span class="signal-dot down"></span>\n            <span class="signal-label">Platino</span>\n            <span class="signal-price">$1.959/oz</span>\n            <span class="signal-change down">-5.6%</span>',
    '<span class="signal-dot up"></span>\n            <span class="signal-label">Platino</span>\n            <span class="signal-price">$1.980/oz</span>\n            <span class="signal-change up">+1,1%</span>'
)
# Oro: down, $4.600 → $4.527, -3.8% → -1,6%
html = html.replace(
    '<span class="signal-price">$4.600/oz</span>\n            <span class="signal-change down">-3.8%</span>',
    '<span class="signal-price">$4.527/oz</span>\n            <span class="signal-change down">-1,6%</span>'
)
# Plata: down → flat, $73,5 → $73,96, -7.5% → +0,6%
html = html.replace(
    '<span class="signal-dot down"></span>\n            <span class="signal-label">Plata</span>\n            <span class="signal-price">$73,5/oz</span>\n            <span class="signal-change down">-7.5%</span>',
    '<span class="signal-dot flat"></span>\n            <span class="signal-label">Plata</span>\n            <span class="signal-price">$73,96/oz</span>\n            <span class="signal-change flat">+0,6%</span>'
)
# CLP/USD: up → down, $889 → $883, +0.9% → -0,7%
html = html.replace(
    '<span class="signal-dot flat"></span>\n            <span class="signal-label">Cobalto</span>\n            <span class="signal-price">$56.290/t</span>\n            <span class="signal-change flat">0%</span>\n        </div>\n        <div class="signal-item">\n            <span class="signal-dot up"></span>\n            <span class="signal-label">CLP/USD</span>\n            <span class="signal-price">$889</span>\n            <span class="signal-change up">+0.9%</span>',
    '<span class="signal-dot flat"></span>\n            <span class="signal-label">Cobalto</span>\n            <span class="signal-price">$56.290/t</span>\n            <span class="signal-change flat">0%</span>\n        </div>\n        <div class="signal-item">\n            <span class="signal-dot down"></span>\n            <span class="signal-label">CLP/USD</span>\n            <span class="signal-price">$883</span>\n            <span class="signal-change down">-0,7%</span>'
)

# 3b. Frase de la semana
html = html.replace(
    '<p class="quote-text">La guerra en el Golfo no es solo una crisis energética — es una crisis de insumos para la minería chilena: sin azufre no hay ácido, sin ácido no hay lixiviación, y sin lixiviación no hay un millón de toneladas de cobre.</p>\n        <p class="quote-author">— Análisis Noticiero Minero Ed.009</p>',
    '<p class="quote-text">Anglo y Teck crean el segundo productor mundial de cobre, el déficit global se duplica a 333.000 toneladas, y el ácido sulfúrico llega a US$405/t en Chile. El cobre tiene demanda — lo que no tiene es oferta.</p>\n        <p class="quote-author">— Análisis Noticiero Minero Ed.010</p>'
)

# 3c. Degradar badge de Ed.9 de "NUEVA" a "Ed. 009"
html = html.replace(
    '<span class="badge latest">NUEVA</span>\n            </div>\n            <div class="card-emphasis">La guerra en el Golfo convierte al ácido sulfúrico',
    '<span class="badge">Ed. 009</span>\n            </div>\n            <div class="card-emphasis">La guerra en el Golfo convierte al ácido sulfúrico'
)

# 3d. Insertar card de Ed.10 antes de la card de Ed.9
new_card = '''        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">Edicion N. 10 &mdash; Semana del 28/04/2026 al 05/05/2026</div>
                    <div class="card-meta">Publicado: 05 de Mayo de 2026</div>
                </div>
                <span class="badge latest">NUEVA</span>
            </div>
            <div class="card-emphasis">Anglo-Teck recibe aprobaci&oacute;n final: nace el segundo productor mundial de cobre. El d&eacute;ficit global se duplica a 333.000 t y el &aacute;cido sulf&uacute;rico alcanza US$405/t CFR Chile.</div>
            <ul class="card-bullets">
                <li><span class="tag">[Cu/M&amp;A]</span> Anglo-Teck: Competition Tribunal aprueba la fusi&oacute;n. Nace el segundo mayor productor mundial con 900.000...</li>
                <li><span class="tag">[Cu]</span> D&eacute;ficit global de cobre se duplica a 333.000 t — el mayor desde 2021. Pipeline de proyectos no alcanza...</li>
                <li><span class="tag">[H&#x2082;SO&#x2084;]</span> &Aacute;cido sulf&uacute;rico CFR Chile US$380-430/t (+35% vs Ed.9). Doble shock: ban chino + bloqueo Ormuz...</li>
                <li><span class="tag">[REE]</span> NdPr corrige -8% a US$126/kg (primera correcci&oacute;n tras 5 semanas de rally); USA Rare Earth +72% en bolsa...</li>
                <li><span class="tag">[Chile]</span> Codelco Pedernales litio al SEIA, cartera minera r&eacute;cord US$104,5B, AMSA costos -30%, QB2 EBITDA +125%...</li>
            </ul>
            <div class="card-actions">
                <a class="card-btn primary" href="Noticiero_Minero_Ed010_2026-05-05.html"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Informe</a>
                <a class="card-btn secondary" href="escuela.html#leccion-10"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg> Clase de la semana</a>
            </div>
        </div>
'''

html = html.replace(
    '        <div class="card">\n            <div class="card-header">\n                <div>\n                    <div class="card-title">Edicion N. 9 &mdash;',
    new_card + '        <div class="card">\n            <div class="card-header">\n                <div>\n                    <div class="card-title">Edicion N. 9 &mdash;'
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(html)

print("  [OK] index.html actualizado.")
print("  Semaforo Cobre 5,90:", '$5,90/lb' in html)
print("  Semaforo NdPr down:", 'signal-label">NdPr</span>\n            <span class="signal-price">$126/kg' in html)
print("  Frase Ed.010:", 'Ed.010' in html)
print("  Card Ed.10:", 'Edicion N. 10' in html)
print("  Badge Ed.9 degradado:", 'badge">Ed. 009' in html)

print("\n[DONE] Todos los archivos actualizados.")