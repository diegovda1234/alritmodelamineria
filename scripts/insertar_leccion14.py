import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('escuela.html', encoding='utf-8') as f:
    content = f.read()

# 1. Nueva entrada en el archivo (antes de leccion-13)
old_archive = '<a class="archive-item lesson-card" href="#leccion-13">'
new_entry = '<a class="archive-item lesson-card" href="#leccion-14"><span class="ai-dot ed"></span><span class="ai-pillar">Operaciones mineras</span><span class="ai-title">Procurement Estrategico de Insumos — por que las mineras no se cubren y cuanto les cuesta</span><span class="ai-ed">Ed.14</span></a>\n        ' + old_archive
content = content.replace(old_archive, new_entry, 1)

# 2. Actualizar contador
content = content.replace('(11 mas)', '(12 mas)', 1)

# 3. Colapsar leccion-13
content = content.replace('<div class="lesson" id="leccion-13">', '<div class="lesson collapsed" id="leccion-13">', 1)

# 4. Bloque leccion 14
leccion14 = """    <div class="lesson" id="leccion-14">
        <div class="lesson-hero">
            <div class="lh-num">Leccion 14 &middot; Edicion N.14</div>
            <h2>Procurement Estrategico de Insumos — por que las mineras no se cubren y cuanto les cuesta</h2>
            <div class="lh-english">Strategic Procurement in Mining — The Hidden Cost of Reactive Purchasing</div>
            <span class="lh-pillar">Operaciones mineras</span>
        </div>
        <div class="lesson-body">
            <a class="btn-ver-todas" onclick="verTodas()" href="javascript:void(0)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg> Ver todas las lecciones</a>

            <h3>El concepto central</h3>
            <p>El <strong>procurement estrategico</strong> es la gestion activa del suministro de insumos criticos con el objetivo de reducir la volatilidad de costos y garantizar la continuidad operacional. A diferencia del procurement tactico (comprar cuando necesito, al precio del mercado), el estrategico anticipa: identifica la cadena de suministro de cada insumo critico, diversifica fuentes, y establece contratos de largo plazo para los mas volatiles.</p>

            <div class="concept-box">
                <div class="cb-term">Procurement Estrategico vs Tactico</div>
                <div class="cb-def">Tactico: comprar cuando necesito, al precio spot. Predecible solo en el corto plazo. | Estrategico: definir con 12-24 meses de anticipacion cuanto voy a necesitar, con que proveedores, y a que precio fijo. El objetivo no es el precio mas bajo en cada compra — es garantizar continuidad operacional y acotar la volatilidad del margen.</div>
            </div>

            <h3>Por que las mineras no se cubren</h3>

            <div class="vocab-wrap">
                <table class="vocab-table">
                    <thead><tr><th>Razon</th><th>Mecanismo</th><th>Consecuencia</th></tr></thead>
                    <tbody>
                        <tr><td><strong>Competencia de capital</strong></td><td>El capital para contratos anticipados compite con el capex de produccion. Produccion siempre gana en el corto plazo.</td><td>Los contratos de largo plazo de acido se postergan indefinidamente.</td></tr>
                        <tr><td><strong>Sesgo del precio bajo</strong></td><td>Con acido a USD 130-190/t en 2023-2024, nadie queria pagar USD 220/t por cobertura. El seguro siempre parece caro antes del siniestro.</td><td>H2 2026 sin cobertura cuando el precio llego a USD 380/t.</td></tr>
                        <tr><td><strong>Responsabilidad fragmentada</strong></td><td>Compras negocia. Operaciones consume. Finanzas aprueba. Ningun area tiene incentivo para proponer contratos de 3 anos a precio fijo mayor al spot.</td><td>El problema no tiene dueno — nadie lo resuelve.</td></tr>
                        <tr><td><strong>Acceso limitado</strong></td><td>La mediana mineria no tiene el volumen ni la tesoreria para acceder a swaps de materias primas o derivados OTC de insumos.</td><td>La herramienta mas efectiva no esta disponible para quienes mas la necesitan.</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="vocab-cards">
                <div class="vc-item"><div class="vc-es">Competencia de capital</div><div class="vc-en">Capital allocation conflict</div><div class="vc-ctx">El procurement compite con produccion por el mismo presupuesto. Siempre pierde.</div></div>
                <div class="vc-item"><div class="vc-es">Sesgo del precio bajo</div><div class="vc-en">Spot price anchoring</div><div class="vc-ctx">Cuando el insumo esta barato, nadie paga prima por cobertura. El seguro parece caro antes del accidente.</div></div>
                <div class="vc-item"><div class="vc-es">Responsabilidad fragmentada</div><div class="vc-en">Diffuse ownership</div><div class="vc-ctx">Si todos son responsables, nadie lo es. El procurement estrategico no tiene dueno.</div></div>
                <div class="vc-item"><div class="vc-es">Acceso limitado</div><div class="vc-en">Instrument access gap</div><div class="vc-ctx">Los hedging sofisticados requieren volumen y tesoreria que la mediana mineria no tiene.</div></div>
            </div>

            <div class="case-study">
                <div class="cs-header"><span class="cs-icon">&#9874;</span><span class="cs-label">Caso de estudio</span></div>
                <div class="cs-title">Crisis de Acido Sulfurico 2026 — el H2 descubierto y el costo de no haberse cubierto</div>
                <p>En febrero de 2026, el cierre del Estrecho de Hormuz elimino el 45% del comercio maritimo global de azufre. China, que proveia el 37% de las importaciones chilenas de acido sulfurico, suspendio sus exportaciones desde el 1 de mayo. El precio CFR Mejillones paso de USD 190/t en febrero a USD 380/t al 15 de abril — 100% de aumento en 7 semanas, antes de que el ban fuera efectivo.</p>
                <p>Las mineras chilenas habian cubierto el <strong>H1 2026</strong> con contratos negociados en octubre-noviembre 2025 — antes del shock. Pero el <strong>H2 2026</strong> quedo mayoritariamente descubierto: los contratos de H2 se negocian en marzo-abril, cuando el precio ya habia subido 100%. Los compradores esperaron que bajara — y no bajo.</p>
                <p>El costo concreto para una minera mediana con consumo de 5.000 t/mes: un incremento de USD 100/t equivale a USD 500.000/mes adicionales, o USD 3MM solo en H2 2026. Goldman Sachs estima ~200.000 t de cobre en riesgo directo; Morgan Stanley eleva la cifra a 1,1MM t por lixiviacion SX-EW. Ese es el costo exacto de no haber firmado contratos de largo plazo en octubre 2025.</p>
                <p class="cs-source">Fuentes: S&amp;P Global Platts (abr 2026), Bloomberg (abr 2026), Goldman Sachs, Morgan Stanley, Noticiero Minero Ed.014.</p>
            </div>

            <h3>Vocabulario tecnico bilingue</h3>

            <div class="vocab-wrap">
                <table class="vocab-table">
                    <thead><tr><th>Espanol</th><th>English</th><th>Contexto de uso</th></tr></thead>
                    <tbody>
                        <tr><td>Contrato de suministro de largo plazo</td><td><span class="v-english">Supply / offtake agreement</span></td><td><div class="v-context">"We locked in a three-year sulfuric acid supply agreement at fixed price, insulating our SX-EW operations from spot market volatility."</div></td></tr>
                        <tr><td>Precio spot</td><td><span class="v-english">Spot price</span></td><td><div class="v-context">"The spot price for sulfuric acid CFR Chile jumped 100% in seven weeks as China's export ban took effect."</div></td></tr>
                        <tr><td>Cobertura de insumos</td><td><span class="v-english">Input cost hedging</span></td><td><div class="v-context">"Input cost hedging through forward contracts or price collars protects EBITDA margins when commodity input prices spike."</div></td></tr>
                        <tr><td>Descubierto (sin cobertura)</td><td><span class="v-english">Open / uncovered position</span></td><td><div class="v-context">"Our H2 acid requirements are uncovered — fully exposed to spot market prices for the second half."</div></td></tr>
                    </tbody>
                </table>
            </div>
            <div class="vocab-cards">
                <div class="vc-item"><div class="vc-es">Contrato de suministro</div><div class="vc-en">Supply / offtake agreement</div><div class="vc-ctx">"3-year acid agreement at fixed price insulates SX-EW from spot volatility."</div></div>
                <div class="vc-item"><div class="vc-es">Precio spot</div><div class="vc-en">Spot price</div><div class="vc-ctx">"CFR Chile jumped 100% in 7 weeks as China's export ban took effect."</div></div>
                <div class="vc-item"><div class="vc-es">Cobertura de insumos</div><div class="vc-en">Input cost hedging</div><div class="vc-ctx">"Forward contracts or collars protect EBITDA when commodity input prices spike."</div></div>
                <div class="vc-item"><div class="vc-es">Descubierto</div><div class="vc-en">Open / uncovered position</div><div class="vc-ctx">"H2 acid requirements uncovered — fully exposed to spot for the second half."</div></div>
            </div>

            <div class="key-takeaway">
                <h4>Lo que pocos saben en la sala de directorio</h4>
                <p>El precio del acido sulfurico esta estructuralmente vinculado al precio del azufre, que a su vez es un <strong>subproducto del gas natural licuado</strong> (el azufre se extrae cuando se trata el gas para eliminar el H2S). Cuando el mercado de LNG se tensiona — como en 2022 post-Ucrania o 2026 post-Hormuz — el azufre disponible para exportacion cae, y el acido sube con rezago de 3-6 meses. Quien entiende esa cadena (LNG → azufre → acido → costo SX-EW) puede anticipar el shock con meses de ventaja. Las refinerias de cobre europeas y japonesas venden acido como subproducto a precios mas estables que el spot asiatico — son la fuente mas predecible para compradores con capacidad logistica de largo recorrido. El hedging formal de insumos de proceso no existe en Chile para la mediana mineria: es uno de los pocos mercados donde no hay intermediarios financieros. Quien construya ese servicio tiene barreras de entrada altas, demanda estructural asegurada y un problema real que resolver.</p>
                <p><em>Fuentes: S&amp;P Global Platts, Bloomberg, Morgan Stanley, Goldman Sachs; Noticiero Minero Ed.014 analisis editorial.</em></p>
            </div>
        </div>
    </div>

    <!-- LECCION 13 - EDICION N.13 -->
"""

content = content.replace('    <!-- LECCION 13 - EDICION N.13 -->\n    <div class="lesson collapsed" id="leccion-13">',
                           leccion14 + '    <div class="lesson collapsed" id="leccion-13">', 1)

with open('escuela.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verificar
with open('escuela.html', encoding='utf-8') as f:
    c = f.read()

checks = [
    ('leccion-14' in c, 'leccion-14 presente'),
    ('Procurement Estrategico' in c, 'Titulo leccion 14 OK'),
    ('Operaciones mineras' in c, 'Pilar correcto'),
    ('lesson collapsed" id="leccion-13"' in c, 'leccion-13 colapsada'),
    ('(12 mas)' in c, 'Contador actualizado a 12'),
    ('href="#leccion-14"' in c and 'archive-item' in c, 'Entry en archivo OK'),
]
for ok, msg in checks:
    print(f"  [{'OK' if ok else 'FAIL'}] {msg}")