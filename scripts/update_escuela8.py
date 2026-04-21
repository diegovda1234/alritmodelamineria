import sys

f = 'C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero/escuela.html'
with open(f, encoding='utf-8') as fh:
    html = fh.read()

# 1. Add Ed.8 card before Ed.7 card in archive-list
old_card = 'href="#leccion-7"><span class="ai-dot ed"></span><span class="ai-pillar">Costos</span>'
new_prefix = 'href="#leccion-8"><span class="ai-dot ed"></span><span class="ai-pillar">Mercados</span><span class="ai-title">Backwardation estructural: cuando el mercado anticipa escasez</span><span class="ai-ed">Ed.8</span></a>\n        <a class="archive-item lesson-card" href="#leccion-7"><span class="ai-dot ed"></span><span class="ai-pillar">Costos</span>'
if old_card in html:
    html = html.replace(old_card, new_prefix, 1)
    print('Card added.')
else:
    print('WARNING: card anchor not found')

# 2. Update current-label (try both variants)
for old_lbl in ['Clase de la semana — Edicion N.6', 'Clase de la semana &mdash; Edicion N.6']:
    if old_lbl in html:
        html = html.replace(old_lbl, old_lbl.replace('N.6', 'N.8'), 1)
        print('Label updated.')

# 3. Collapse lesson 7
target7 = '<div class="lesson" id="leccion-7">'
if target7 in html:
    html = html.replace(target7, '<div class="lesson collapsed" id="leccion-7">', 1)
    print('Lesson 7 collapsed.')
else:
    print('WARNING: lesson-7 not found to collapse')

# 4. Insert lesson 8 block before collapsed lesson 7
lesson8 = '''    <!-- LECCION 08 - EDICION N.8 -->
    <div class="lesson" id="leccion-8">
        <div class="lesson-hero">
            <div class="lh-num">Leccion 08 &middot; Edicion N.8</div>
            <h2>Backwardation estructural: cuando el mercado anticipa escasez prolongada</h2>
            <div class="lh-english">Structural Backwardation: When the Market Prices in Prolonged Scarcity</div>
            <span class="lh-pillar">Mercados de commodities</span>
        </div>
        <div class="lesson-body">
            <a class="btn-ver-todas" onclick="verTodas()" href="javascript:void(0)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg> Ver todas las lecciones</a>

            <h3>El concepto central</h3>
            <p>La <strong>curva de futuros</strong> de un commodity muestra el precio al que el mercado esta dispuesto a comprar ese commodity para entrega en diferentes fechas futuras. Hay dos estados posibles:</p>

            <div class="concept-box">
                <div class="cb-term">Contango</div>
                <div class="cb-def">El precio futuro es <em>mayor</em> que el precio spot. Senala equilibrio o superavit de oferta. Ejemplo: petroleo en 2020 cuando los depositos estaban llenos.</div>
            </div>

            <div class="concept-box">
                <div class="cb-term">Backwardation</div>
                <div class="cb-def">El precio futuro es <em>menor</em> que el precio spot. El mercado valora tener el commodity HOY mas que en el futuro. Senala escasez inmediata o anticipada. Ejemplo: cobre en 2026 con deficit de concentrados y aranceles Section 232 al 50%.</div>
            </div>

            <p>La distincion critica es entre backwardation <strong>coyuntural</strong> (disrupcion temporal) y <strong>estructural</strong> (deficit proyectado varios anos consecutivos). El platino en 2026 es el ejemplo mas claro: cuatro anos consecutivos de deficit sin nueva oferta significativa en el horizonte.</p>

            <h3>La noticia de esta semana: dos backwardations simultaneas</h3>
            <p>En CESCO Week 2026, el cobre registro backwardation con TC/RC negativos: las fundidoras pagan por procesar concentrado porque el mineral escasea. Simultaneamente, el WPIC confirmo el cuarto deficit consecutivo de platino (240.000 oz), con stocks cayendo a apenas 4 meses de demanda global. Dos commodities, dos backwardations, misma lectura: el spot vale mas que el futuro.</p>

            <div class="case-study">
                <div class="cs-header"><span class="cs-icon">&#9874;</span><span class="cs-label">Caso de estudio</span></div>
                <div class="cs-title">Leer la curva de futuros del cobre para anticipar movimientos</div>
                <p>En enero 2026, los futuros de cobre a 12 meses cotizaban con prima sobre el spot (contango leve). En abril, la curva se invirtio a backwardation: (1) aranceles Section 232 al 50% activados el 6 de abril generaron stockpiling masivo; (2) TC/RC cayeron a terreno negativo; (3) ban chino de acido sulfurico tensiono el 20% de la cadena SX-EW.</p>
                <p>El inversor que leyo el cambio de contango a backwardation en marzo-abril pudo anticipar el rally del cobre a US$6/lb. La curva de futuros es informacion publica, gratuita y en tiempo real en LME y CME.</p>
                <p class="cs-source">Fuentes: LME, CME Group, CESCO Week 2026, WPIC (abr 2026)</p>
            </div>

            <h3>Implicancias para el hedging en Chile</h3>
            <p>Chile fija el precio de venta de cobre referenciando el spot LME del mes en los contratos de offtake. En backwardation, el spot esta elevado y los precios forward deprimidos. Fijar precio hoy a futuro via forward sale significa vender mas barato que el spot actual. Por eso en backwardation las mineras prefieren no hacer hedge y capturar el premio spot.</p>

            <h3>Vocabulario tecnico</h3>
            <table class="vocab-table">
                <thead><tr><th>Espanol</th><th>English</th><th>Contexto de uso</th></tr></thead>
                <tbody>
                    <tr><td>Backwardation</td><td><span class="v-english">Backwardation</span></td><td><div class="v-context">"Copper shifted into structural backwardation, signaling the deficit is deeper than expected."</div></td></tr>
                    <tr><td>Contango</td><td><span class="v-english">Contango</span></td><td><div class="v-context">"Nickel was in deep contango during the surplus years, discouraging new mine investment."</div></td></tr>
                    <tr><td>Curva de futuros</td><td><span class="v-english">Forward curve / futures curve</span></td><td><div class="v-context">"The forward curve for platinum has been in backwardation for four consecutive years."</div></td></tr>
                    <tr><td>Prima de conveniencia</td><td><span class="v-english">Convenience yield</span></td><td><div class="v-context">"The convenience yield explains why buyers pay a spot premium to avoid delivery risk."</div></td></tr>
                    <tr><td>Deficit estructural</td><td><span class="v-english">Structural deficit</span></td><td><div class="v-context">"The WPIC confirmed platinum faces a structural deficit for the fourth consecutive year."</div></td></tr>
                    <tr><td>Contrato de offtake</td><td><span class="v-english">Offtake agreement</span></td><td><div class="v-context">"The project secured a 15-year offtake with floor prices backed by the US government."</div></td></tr>
                </tbody>
            </table>

            <h3>Ejercicio mental</h3>
            <div class="exercise-box">
                <div class="ex-header">Eres el tesorero de una minera chilena con produccion de 80.000 t/ano de cobre</div>
                <p>Hoy el cobre LME spot cotiza a US$6.04/lb. El futuro a 12 meses cotiza a US$5.65/lb (backwardation de US$0.39/lb = 6.5%).</p>
                <ul>
                    <li><strong>Opcion A:</strong> No hacer hedge, vender todo al spot mes a mes.</li>
                    <li><strong>Opcion B:</strong> Forward sale a US$5.65/lb para el 50% de la produccion.</li>
                    <li><strong>Opcion C:</strong> Puts con strike US$5.20/lb, prima de US$0.12/lb.</li>
                </ul>
                <p><strong>Pregunta 1:</strong> Si el deficit se profundiza, la backwardation se amplia o se reduce? Que implica para el precio spot en 6 meses?</p>
                <p><strong>Pregunta 2:</strong> Con la curva en backwardation, la Opcion B protege el presupuesto o sacrifica ingresos esperados?</p>
                <p><strong>Pregunta 3:</strong> El platino lleva 4 anos en backwardation pero solo subio +30% desde enero. Por que la backwardation estructural no siempre genera un rally rapido?</p>
            </div>

            <div class="key-takeaway">
                <h4>Takeaway clave</h4>
                <p>La curva de futuros es el mapa de consenso del mercado sobre la escasez futura. Cuando el cobre y el platino estan simultaneamente en backwardation, el mensaje es inequivoco: <strong>el mercado no encuentra oferta suficiente a largo plazo para los dos metales que mas necesita la transicion energetica</strong>. Para Chile, esto es la mejor noticia para los ingresos del sector y la mayor presion para acelerar la meta de 6 millones de toneladas del gobierno Kast.</p>
            </div>
        </div>
    </div>

'''

target_collapsed = '<div class="lesson collapsed" id="leccion-7">'
if target_collapsed in html:
    html = html.replace(target_collapsed, lesson8 + '    ' + target_collapsed, 1)
    print('Lesson 8 block inserted.')
else:
    print('WARNING: collapsed lesson-7 not found for insertion')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(html)

print('escuela.html saved.')
print('Verification:')
print('  leccion-8 card present:', 'href="#leccion-8"' in html)
print('  leccion-8 div present:', 'id="leccion-8"' in html)
print('  leccion-7 collapsed:', 'class="lesson collapsed" id="leccion-7"' in html)