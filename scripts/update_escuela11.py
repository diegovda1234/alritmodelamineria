"""
update_escuela11.py — Agrega Leccion 11 a escuela.html (Ed.011, Gobernanza corporativa)
Ejecutar desde: C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero/
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero"
f = f'{BASE}/escuela.html'

with open(f, encoding='utf-8') as fh:
    html = fh.read()

# 1. Actualizar label "Clase de la semana"
html = html.replace(
    'class="current-label">Clase de la semana &mdash; Edicion N.10',
    'class="current-label">Clase de la semana &mdash; Edicion N.11'
)

# 2. Agregar al indice de lecciones (antes de leccion-10)
html = html.replace(
    '        <a class="archive-item lesson-card" href="#leccion-10">',
    '        <a class="archive-item lesson-card" href="#leccion-11"><span class="ai-dot ed"></span><span class="ai-pillar">Gestion</span><span class="ai-title">Gobernanza en empresas mineras estatales: teoria del agente-principal</span><span class="ai-ed">Ed.11</span></a>\n        <a class="archive-item lesson-card" href="#leccion-10">'
)

# 3. HTML completo de la leccion 11
LECCION_11 = '''    <!-- LECCION 11 - EDICION N.11 -->
    <div class="lesson" id="leccion-11">
        <div class="lesson-hero">
            <div class="lh-num">Leccion 11 &middot; Edicion N.11</div>
            <h2>Gobernanza en empresas mineras estatales: teoria del agente-principal y por que importa cuando el cobre esta en maximos historicos</h2>
            <div class="lh-english">Corporate Governance in State Mining Companies: Principal-Agent Theory and Why It Matters When Copper Hits Record Highs</div>
            <span class="lh-pillar">Gestion y Finanzas</span>
        </div>
        <div class="lesson-body">
            <a class="btn-ver-todas" onclick="verTodas()" href="javascript:void(0)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg> Ver todas las lecciones</a>

            <h3>El concepto central</h3>
            <p>En toda organizacion existe una relacion entre quien toma las decisiones (el <strong>agente</strong>) y quien soporta las consecuencias de esas decisiones (el <strong>principal</strong>). Cuando sus incentivos no estan alineados, el agente puede actuar en beneficio propio en detrimento del principal. Esta es la <strong>teoria del agente-principal</strong>, y es el marco conceptual central para entender por que las empresas mineras estatales como Codelco enfrentan desafios estructurales que las empresas privadas no tienen.</p>

            <div class="concept-box">
                <div class="cb-term">El Principal</div>
                <div class="cb-def">Quien es dueno del activo y soporta el riesgo financiero. En Codelco: el Estado chileno, representado por el gobierno de turno y los ciudadanos que dependen de los aportes de Codelco al Fisco. El principal quiere maximizar el valor del activo en el largo plazo, pero tambien necesita flujo de caja inmediato para financiar el presupuesto fiscal.</div>
            </div>

            <div class="concept-box">
                <div class="cb-term">El Agente</div>
                <div class="cb-def">Quien toma las decisiones operativas en nombre del principal. En Codelco: el directorio y la gerencia general. Su mandato formal es administrar la empresa en beneficio del dueno-Estado, pero sus incentivos reales pueden divergir: mandatos cortos (2-4 anos), metas de corto plazo, presion politica de turno, objetivos multiples y contradictorios.</div>
            </div>

            <div class="concept-box">
                <div class="cb-term">El Problema del Agente</div>
                <div class="cb-def">Cuando los incentivos del agente no estan alineados con los del principal, el agente toma decisiones que lo benefician a el o al gobierno de turno pero perjudican al principal de largo plazo. Ejemplos en mineria estatal: diferir mantenimientos para mejorar EBITDA, maximizar produccion a corto plazo a costa de la reserva, o priorizar el aporte al Fisco sobre la inversion en reposicion de capacidad.</div>
            </div>

            <h3>Por que Codelco es el caso de estudio perfecto</h3>
            <p>Codelco enfrenta el problema del agente en su forma mas aguda porque tiene <strong>multiples principales con intereses distintos</strong>: el Fisco (quiere dividendos ahora), el gobierno de turno (quiere logros politicos visibles), los trabajadores (quieren estabilidad y bonos), la sociedad (quiere sustentabilidad), y el Estado como dueno de largo plazo (quiere que Codelco siga produciendo en 2050). Un directorio que intente satisfacer a todos simultaneamente enfrenta una tarea imposible, y el resultado historico ha sido decisiones de compromiso que acumuladas en el tiempo generan caidas de produccion, sobrecostos en proyectos y deuda creciente.</p>

            <div class="case-study">
                <div class="cs-header"><span class="cs-icon">&#9874;</span><span class="cs-label">Caso de estudio: exito</span></div>
                <div class="cs-title">Norsk Hydro (Noruega) — como resolver el problema del agente en una empresa estatal</div>
                <p>Norsk Hydro es 34% propiedad del Estado noruego pero opera con plena autonomia corporativa. El modelo se basa en tres principios: (1) el directorio se elige por competencias tecnicas, no por afiliacion politica; (2) los mandatos son de 5-6 anos, mas largos que los ciclos electorales de 4 anos, reduciendo la presion de corto plazo; (3) el Estado cobra dividendos segun una politica predefinida (porcentaje del EBITDA), no segun las necesidades del presupuesto fiscal del ano. Resultado: Norsk Hydro puede planificar inversiones de 10-15 anos con certeza, sus directores pueden tomar decisiones impopulares de corto plazo sin presion politica directa, y el Estado recibe un flujo de dividendos predecible y creciente en el tiempo.</p>
                <p class="cs-source">Fuente: OCDE "Corporate Governance of State-Owned Enterprises", Norsk Hydro Annual Reports 2020-2025</p>
            </div>

            <div class="case-study">
                <div class="cs-header"><span class="cs-icon">&#9888;</span><span class="cs-label">Caso de estudio: crisis</span></div>
                <div class="cs-title">Codelco 2015-2025: diez anos de produccion declinante con precio del cobre creciente</div>
                <p>Entre 2015 y 2025, la produccion de Codelco cayo desde 1,8 millones de toneladas hasta 1,33 millones, una caida del 26% en una decada en la que el precio del cobre paso de US$2,50/lb a US$5,90/lb. En una empresa privada, el ciclo de precios altos deberia haber financiado la inversion de reposicion que mantiene la produccion. En Codelco ocurrio lo contrario: el Fisco capturo los flujos excepcionales via dividendos y aportes especiales, dejando a la empresa con deuda creciente y proyectos de reposicion financiados con endeudamiento. Codelco cerro 2025 con deuda de US$24.658 millones, la mas alta de su historia, mientras su produccion era la mas baja en 25 anos.</p>
                <p class="cs-source">Fuente: Memorias Anuales Codelco 2015-2025, COCHILCO, Bloomberg, The Clinic (abril 2026)</p>
            </div>

            <h3>Los cinco instrumentos de la buena gobernanza</h3>
            <ol>
                <li><strong>Mandatos largos y no politicos:</strong> Directores con periodos de 5-6 anos (mayor que el ciclo electoral) y seleccion basada en competencias.</li>
                <li><strong>Separacion entre gobierno accionista y gobierno corporativo:</strong> El ministerio que representa al Estado no debe tener influencia directa en las decisiones operativas del directorio.</li>
                <li><strong>Politica de dividendos predefinida:</strong> Un porcentaje fijo del EBITDA (no un monto variable segun el presupuesto fiscal) protege la inversion de largo plazo.</li>
                <li><strong>Metricas de desempeno de largo plazo:</strong> Incluir KPIs como "reservas repuestas" o "vida util de la mina", no solo EBITDA del ano.</li>
                <li><strong>Transparencia e informacion publica:</strong> La publicacion regular de datos operacionales detallados crea presion de mercado y reduce la asimetria de informacion.</li>
            </ol>

            <h3>Vocabulario tecnico</h3>
            <table class="vocab-table">
                <thead><tr><th>Espanol</th><th>English</th><th>Contexto de uso</th></tr></thead>
                <tbody>
                    <tr><td>Teoria agente-principal</td><td><span class="v-english">Principal-agent theory</span></td><td><div class="v-context">"The principal-agent problem at state-owned enterprises is exacerbated when the government acts as both regulator and shareholder."</div></td></tr>
                    <tr><td>Gobierno corporativo</td><td><span class="v-english">Corporate governance</span></td><td><div class="v-context">"Weak corporate governance at the state miner has contributed to cost overruns and declining production over the past decade."</div></td></tr>
                    <tr><td>Directorio independiente</td><td><span class="v-english">Independent board of directors</span></td><td><div class="v-context">"An independent board with long-term mandates would reduce short-term political pressure on investment decisions."</div></td></tr>
                    <tr><td>Asimetria de informacion</td><td><span class="v-english">Information asymmetry</span></td><td><div class="v-context">"Information asymmetry between management and the government shareholder allows the former to defer costly but necessary capital expenditures."</div></td></tr>
                    <tr><td>Politica de dividendos</td><td><span class="v-english">Dividend policy</span></td><td><div class="v-context">"A fixed-ratio dividend policy would protect Codelco's reinvestment capacity during high copper price cycles."</div></td></tr>
                    <tr><td>Aporte al fisco</td><td><span class="v-english">Fiscal contribution / state transfer</span></td><td><div class="v-context">"The annual state transfer from Codelco has historically consumed 40-70% of the company's free cash flow, limiting reinvestment."</div></td></tr>
                    <tr><td>Vida util de la mina</td><td><span class="v-english">Mine life</span></td><td><div class="v-context">"The approved mine plan extends the ore body mine life to 2048, subject to permitting and capital allocation."</div></td></tr>
                    <tr><td>Reposicion de reservas</td><td><span class="v-english">Reserve replacement</span></td><td><div class="v-context">"A reserve replacement ratio below 1.0 means the company is depleting its mineral base faster than it is finding new resources."</div></td></tr>
                </tbody>
            </table>

            <div class="key-takeaway">
                <h4>Dato que pocos saben</h4>
                <p>Entre 1990 y 2023, Codelco transfrio al Estado chileno mas de US$130.000 millones en aportes, impuestos y dividendos, el equivalente a tres fondos soberanos del tamano del FEES. Sin embargo, en el mismo periodo, la empresa acumulo una deuda neta de US$24.658 millones y su produccion cayo 26% desde los maximos de 2018. El monto total transferido al Estado habria sido suficiente para construir dos nuevas Codelcos. El problema de gobernanza no es cuanto aporta la empresa al Estado: es que ese aporte historicamente no ha tenido una politica de dividendos que proteja la capacidad de reposicion de la empresa que genera ese valor.</p>
                <p><em>Fuente: Memorias Anuales Codelco, DIPRES, Bloomberg, OCDE "Corporate Governance of SOEs: A Review of Policies and Practices"</em></p>
            </div>
        </div>
    </div>

'''

# Insertar ANTES de la leccion-10 (leccion actual mas reciente)
html = html.replace(
    '    <!-- LECCION 10 - EDICION N.10 -->',
    LECCION_11 + '    <!-- LECCION 10 - EDICION N.10 -->'
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(html)

print("[OK] escuela.html actualizado con Leccion 11")
print("  label actualizado:", 'Edicion N.11' in html)
print("  href leccion-11:", 'href="#leccion-11"' in html)
print("  div leccion-11:", 'id="leccion-11"' in html)