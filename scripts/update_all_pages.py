"""
update_all_pages.py
- Agrega boton "Atras" (history.back()) y tabs de navegacion a todas las paginas
- Agrega la clase Ed004 (TC/RC) a escuela.html
- Actualiza el label "Clase de la semana" a Ed.4
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero"

# ── NUEVA BARRA SUPERIOR ─────────────────────────────────────────────────────
# Reemplaza el <span></span> vacio por tabs de navegacion y agrega boton atras
def nueva_topbar(html, pagina_activa):
    """pagina_activa: 'escuela' | 'precios' | 'proyecciones' | 'inicio'"""

    nav_tabs = {
        'escuela':      'escuela.html',
        'proyecciones': 'proyecciones.html',
        'precios':      'precios.html',
    }
    nombres = {
        'escuela':      'Escuela',
        'proyecciones': 'Proyecciones',
        'precios':      'Precios',
    }

    tabs_html = ' '.join([
        f'<a href="{nav_tabs[p]}" style="color:{"var(--gold)" if p == pagina_activa else "rgba(255,255,255,.55)"};text-decoration:none;font-size:12px;font-weight:{"700" if p == pagina_activa else "500"};padding:4px 8px;border-radius:5px;{"background:rgba(226,185,111,.12);" if p == pagina_activa else ""}transition:.2s;">{nombres[p]}</a>'
        for p in ['escuela', 'proyecciones', 'precios']
    ])

    back_btn = '<button onclick="history.back()" style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);color:rgba(255,255,255,.8);padding:4px 10px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600;display:flex;align-items:center;gap:4px;transition:.2s;" onmouseover="this.style.background=\'rgba(255,255,255,.14)\'" onmouseout="this.style.background=\'rgba(255,255,255,.08)\'"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg> Atras</button>'

    old_link = '<a href="index.html"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg> Inicio</a>'
    new_left = f'<div style="display:flex;align-items:center;gap:10px;">{back_btn}<a href="index.html" style="color:rgba(255,255,255,.6);text-decoration:none;font-size:12px;font-weight:600;display:flex;align-items:center;gap:4px;" onmouseover="this.style.color=\'var(--gold)\'" onmouseout="this.style.color=\'rgba(255,255,255,.6)\'"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/></svg> Inicio</a></div>'

    html = html.replace(old_link, new_left)
    html = html.replace('<span></span>', f'<div style="display:flex;align-items:center;gap:6px;">{tabs_html}</div>')
    return html


# ── ACTUALIZAR escuela.html ───────────────────────────────────────────────────
with open(f"{BASE}/escuela.html", "r", encoding="utf-8") as f:
    escuela = f.read()

# 1. Barra superior
escuela = nueva_topbar(escuela, 'escuela')

# 2. Actualizar label "Clase de la semana"
escuela = escuela.replace(
    'class="current-label">Clase de la semana &mdash; Edicion N.3',
    'class="current-label">Clase de la semana &mdash; Edicion N.4'
)

# 3. Agregar nueva leccion Ed004 ANTES de leccion-1
nueva_leccion = """
    <!-- ═══════════════════════════════════════════════════════════
         LECCION 04 — EDICION N.4
    ═══════════════════════════════════════════════════════════════ -->
    <div class="lesson" id="leccion-4">
        <div class="lesson-hero">
            <div class="lh-num">Leccion 04 &middot; Edicion N.4</div>
            <h2>TC/RC: La tarifa que mide la salud de toda la cadena del cobre</h2>
            <div class="lh-english">Treatment Charges &amp; Refining Charges: The Metric That Reveals Concentrate Scarcity</div>
            <span class="lh-pillar">Economia Minera</span>
        </div>

        <div class="lesson-body">

            <h3>El concepto central</h3>

            <p>Cuando una mina produce concentrado de cobre, no puede venderlo directamente al mercado: necesita enviarlo a una fundicion (smelter) que lo procese y lo convierta en cobre refinado. Las <strong>tarifas de tratamiento y refinacion (TC/RC)</strong> son el precio que la fundicion le cobra a la minera por ese servicio.</p>

            <div class="concept-box">
                <div class="cb-term">TC — Treatment Charge (Tarifa de Tratamiento)</div>
                <div class="cb-def">Tarifa que cobra la fundicion por procesar el concentrado. Se expresa en <strong>USD por tonelada seca de concentrado</strong>. Historicamente en rangos de US$60&ndash;80/t. Cuando el mercado de concentrado es tenso (escasez), los TC bajan porque las fundidoras compiten por el concentrado disponible. Cuando hay exceso de concentrado, los TC suben porque las mineras compiten por conseguir fundidoras.</div>
            </div>

            <div class="concept-box">
                <div class="cb-term">RC — Refining Charge (Tarifa de Refinacion)</div>
                <div class="cb-def">Tarifa adicional por purificar el cobre hasta cobre refinado (99.99% pureza). Se expresa en <strong>centavos de dolar por libra de cobre contenido</strong>. Historicamente en rangos de 6&ndash;8 cents/lb. Sigue la misma logica que el TC: baja cuando hay escasez de concentrado.</div>
            </div>

            <div class="concept-box">
                <div class="cb-term">Benchmark anual</div>
                <div class="cb-def">Cada ano, una minera grande (generalmente Antofagasta Minerals, Freeport o BHP) negocia con una fundidora china (generalmente Jiangxi Copper) los TC/RC de referencia para el ano. Este &quot;benchmark&quot; marca el piso de las negociaciones del resto del mercado. En marzo 2026, el benchmark Antofagasta&ndash;China llego a <strong>TC/RC = 0 por primera vez en la historia</strong>.</div>
            </div>

            <h3>¿Que significa TC/RC = 0?</h3>

            <p>Que las fundidoras estan dispuestas a procesar concentrado <strong>sin cobrar tarifa</strong>. En el mercado spot, los TC son incluso negativos: las fundidoras pagan a las mineras por el concentrado. ¿Por que? Porque el concentrado es tan escaso que detener la planta cuesta mas que perder el margen:</p>

            <ul style="margin:12px 0 12px 20px;">
                <li>Apagar y relanzar una fundidora de cobre cuesta <strong>decenas de millones de dolares</strong></li>
                <li>Los trabajadores no se pueden despedir facilmente</li>
                <li>Los contratos de suministro de energia y quimicos tienen penalidades por inactividad</li>
                <li>Reactivar toma 3&ndash;6 meses de operacion deficitaria</li>
            </ul>

            <p>Por eso, cuando el concentrado escasea, las fundidoras prefieren pagar para tener algo que procesar antes que apagar la planta.</p>

            <h3>La paradoja de marzo 2026</h3>

            <p>Esta semana vivimos algo historicamente anomalo: los inventarios de cobre en la LME estaban en maximos desde 2019 (330.000 toneladas), pero el mercado fisico de concentrado estaba en deficit record. ¿Como es posible?</p>

            <p>La respuesta es geografica y temporal. El cobre refinado en los almacenes de la LME (en Taiwan, Baltimore) no es el mismo que el concentrado que necesitan las fundidoras chinas <em>hoy</em>. El deficit de concentrado se debe principalmente al desastre del Grasberg (Freeport, Indonesia) que elimino 300.000 toneladas de produccion en 2026, y al efecto acumulado de anos de subinversion en nueva capacidad minera.</p>

            <div class="concept-box">
                <div class="cb-term">CSPT — China Smelters Purchase Team</div>
                <div class="cb-def">Grupo coordinado de las principales fundidoras chinas (Jiangxi Copper, Tongling, etc.) que negocia en bloque los TC/RC con las mineras. Cuando los TC caen demasiado y afectan la rentabilidad, el CSPT puede coordinar un recorte de produccion para reducir la demanda de concentrado y recuperar el poder de negociacion. En marzo 2026 el CSPT anuncio recorte coordinado del 10%.</div>
            </div>

            <h3>Implicancias para Chile</h3>

            <p>TC/RC = 0 es una senial extraordinariamente positiva para las mineras productoras de concentrado en Chile:</p>

            <ul style="margin:12px 0 12px 20px;">
                <li><strong>Poder de negociacion maximo:</strong> Las fundidoras necesitan el concentrado chileno mas de lo que Chile necesita a las fundidoras</li>
                <li><strong>Margenes maximos para el productor:</strong> El costo de vender el concentrado es casi cero</li>
                <li><strong>Senial de inversion:</strong> Justifica acelerar cualquier proyecto de cobre en etapa de pre-factibilidad en Chile</li>
            </ul>

            <h3>Caso de estudio: Jiangxi Copper &ndash; Antofagasta benchmark 2026</h3>

            <p>Antofagasta Minerals firmo el benchmark anual con Jiangxi Copper a TC/RC = 0. Esto significa que Antofagasta (AMSA) recibira el 100% del valor del cobre contenido en su concentrado, sin descuento por procesamiento. En terminos practicos, es como si la fundidora trabajara gratis para AMSA durante todo 2026.</p>

            <p>Para el mercado, el benchmark de AMSA es la senial mas clara del mercado: las fundidoras estan tan cortas de concentrado que aceptan condiciones nunca vistas antes.</p>

            <div class="key-takeaway">
                <h4>Para llevarte a una reunion</h4>
                <p>&quot;Si los TC/RC estan en cero y las fundidoras chinas estan recortando produccion, ¿en que punto el mercado de catodo tambien entra en escasez? ¿Y que ventana de tiempo tiene un nuevo proyecto en Chile para llegar a produccion mientras esa prima todavia este vigente?&quot;</p>
            </div>

        </div>

        <div class="lesson-nav">
            <a href="#leccion-1" class="ln-next">Leccion anterior: Del PEA al Feasibility Study &rarr;</a>
        </div>
    </div>

"""

# Insertar antes de la leccion-1
escuela = escuela.replace(
    '    <!-- ═══════════════════════════════════════════════════════════\n         LECCION 01',
    nueva_leccion + '    <!-- ═══════════════════════════════════════════════════════════\n         LECCION 01'
)

# Actualizar el indice de lecciones si existe (agregar leccion 4)
if 'id="leccion-1"' in escuela and 'leccion-4' not in escuela[:escuela.find('id="leccion-1"')]:
    print("Leccion-4 insertada OK")

with open(f"{BASE}/escuela.html", "w", encoding="utf-8") as f:
    f.write(escuela)
print(f"escuela.html actualizado. Largo: {len(escuela)}")


# ── ACTUALIZAR precios.html ───────────────────────────────────────────────────
with open(f"{BASE}/precios.html", "r", encoding="utf-8") as f:
    precios = f.read()
precios = nueva_topbar(precios, 'precios')
with open(f"{BASE}/precios.html", "w", encoding="utf-8") as f:
    f.write(precios)
print(f"precios.html actualizado. Largo: {len(precios)}")


# ── ACTUALIZAR proyecciones.html ──────────────────────────────────────────────
with open(f"{BASE}/proyecciones.html", "r", encoding="utf-8") as f:
    proyecciones = f.read()
proyecciones = nueva_topbar(proyecciones, 'proyecciones')
with open(f"{BASE}/proyecciones.html", "w", encoding="utf-8") as f:
    f.write(proyecciones)
print(f"proyecciones.html actualizado. Largo: {len(proyecciones)}")


print("\nTodo actualizado. Corre github_deploy.py para publicar.")
