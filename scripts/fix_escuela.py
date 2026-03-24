"""
fix_escuela.py
- Agrega CSS faltante (.key-takeaway, .lesson-nav, .ln-next)
- Implementa show/hide: al hacer click en una leccion del archivo,
  se ocultan todas las demas y solo se ve la seleccionada
- Agrega boton "Ver todas las lecciones" dentro de cada leccion
- Corrige el label
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "C:/Users/diego.varleta/CLAUDE/Noticiero_Minero"

with open(f"{BASE}/escuela.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. AGREGAR CSS FALTANTE ───────────────────────────────────────────────────
css_extra = """
        /* ═══ KEY TAKEAWAY ═══ */
        .key-takeaway {
            background: linear-gradient(135deg, var(--night) 0%, #16213e 100%);
            border-radius: 10px; padding: 20px 24px; margin: 28px 0 8px;
            border-left: 4px solid var(--copper);
        }
        .key-takeaway h4 {
            font-size: 11px; text-transform: uppercase; letter-spacing: 1px;
            color: var(--gold); font-weight: 700; margin-bottom: 10px;
        }
        .key-takeaway p {
            font-size: 14px; color: rgba(255,255,255,.85);
            line-height: 1.65; font-style: italic;
        }

        /* ═══ LESSON NAV ═══ */
        .lesson-nav {
            display: flex; justify-content: flex-end;
            margin-top: 28px; padding-top: 16px;
            border-top: 1px solid var(--rule);
        }
        .ln-next {
            font-size: 13px; color: var(--copper); text-decoration: none;
            font-weight: 600; display: flex; align-items: center; gap: 6px;
        }
        .ln-next:hover { text-decoration: underline; }

        /* ═══ SHOW/HIDE LECCIONES ═══ */
        .lesson { display: none; }
        .lesson.active { display: block; }
        .lesson-all-view .lesson { display: block; }

        /* Boton volver a todas */
        .btn-ver-todas {
            display: inline-flex; align-items: center; gap: 6px;
            background: var(--light); border: 1px solid var(--rule);
            color: var(--slate); font-size: 12px; font-weight: 600;
            padding: 7px 14px; border-radius: 7px; cursor: pointer;
            text-decoration: none; margin-bottom: 20px;
            transition: background .2s;
        }
        .btn-ver-todas:hover { background: var(--rule); }

        /* Archive item activo */
        .archive-item.selected {
            background: rgba(184,115,51,.08);
            border-left: 3px solid var(--copper);
        }
"""

html = html.replace(
    "        @media(max-width:500px){ .pillar-grid{grid-template-columns:repeat(2,1fr);} }",
    "        @media(max-width:500px){ .pillar-grid{grid-template-columns:repeat(2,1fr);} }" + css_extra
)

# ── 2. AGREGAR ID="leccion-4" AL ARCHIVE (si no esta) ────────────────────────
if 'href="#leccion-4"' not in html:
    html = html.replace(
        '        <a class="archive-item lesson-card" href="#leccion-1">',
        '        <a class="archive-item lesson-card" href="#leccion-4"><span class="ai-dot ed"></span><span class="ai-pillar">Economia</span><span class="ai-title">TC/RC: La cadena del cobre</span><span class="ai-ed">Ed.4</span></a>\n        <a class="archive-item lesson-card" href="#leccion-1">'
    )
    # Actualizar conteo
    html = html.replace('(6 mas)', '(7 mas)')
    print("leccion-4 agregada al archivo OK")

# ── 3. BOTON "VER TODAS LAS LECCIONES" en cada leccion ───────────────────────
# Agregar al inicio de cada lesson-body (solo si no existe)
btn_volver = '<a class="btn-ver-todas" onclick="verTodas()" href="javascript:void(0)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg> Ver todas las lecciones</a>\n\n            '
if 'btn-ver-todas' not in html:
    html = html.replace('<div class="lesson-body">\n\n            <h3>', '<div class="lesson-body">\n\n            ' + btn_volver + '<h3>')
    print("Boton 'Ver todas' agregado OK")

# ── 4. JAVASCRIPT SHOW/HIDE ───────────────────────────────────────────────────
js_code = """
<script>
(function() {
    // Al cargar: mostrar solo la leccion activa (la primera = Ed.4)
    const lecciones = document.querySelectorAll('.lesson');
    const archiveItems = document.querySelectorAll('.archive-item');

    function mostrarLeccion(id) {
        // Ocultar todas
        lecciones.forEach(l => l.classList.remove('active'));
        archiveItems.forEach(a => a.classList.remove('selected'));

        // Mostrar la seleccionada
        const target = document.getElementById(id);
        if (target) {
            target.classList.add('active');
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // Marcar item del archivo como activo
        archiveItems.forEach(a => {
            if (a.getAttribute('href') === '#' + id) {
                a.classList.add('selected');
            }
        });

        // Actualizar el label
        const num = target ? target.querySelector('.lh-num') : null;
        const label = document.querySelector('.current-label');
        if (label && num) label.textContent = num.textContent;
    }

    window.verTodas = function() {
        lecciones.forEach(l => l.classList.add('active'));
        archiveItems.forEach(a => a.classList.remove('selected'));
        const label = document.querySelector('.current-label');
        if (label) label.textContent = 'Todas las lecciones';
    };

    // Interceptar clicks en archive items
    archiveItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                mostrarLeccion(href.slice(1));
            }
        });
    });

    // Mostrar la leccion mas reciente por defecto
    const primeraLeccion = lecciones[0];
    if (primeraLeccion) {
        primeraLeccion.classList.add('active');
        const id = primeraLeccion.id;
        archiveItems.forEach(a => {
            if (a.getAttribute('href') === '#' + id) a.classList.add('selected');
        });
    }
})();
</script>
"""

if 'window.verTodas' not in html:
    html = html.replace('</body>', js_code + '\n</body>')
    print("JavaScript show/hide agregado OK")

# ── 5. GUARDAR ────────────────────────────────────────────────────────────────
with open(f"{BASE}/escuela.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nescuela.html guardado. Largo: {len(html)}")
print("CSS key-takeaway:", '.key-takeaway {' in html)
print("CSS lesson-nav:", '.lesson-nav {' in html)
print("JS show/hide:", 'verTodas' in html)
print("Btn volver:", 'btn-ver-todas' in html)
