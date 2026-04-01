"""
completar_leccion4.py
Agrega a la Leccion 04 (TC/RC):
- Caso de estudio
- Vocabulario tecnico bilingue
- Ejercicio mental
- Datos que pocos saben
- Elimina .lesson-nav (link a otras lecciones)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero"

with open(f"{BASE}/escuela.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. ELIMINAR .lesson-nav de la leccion-4 ──────────────────────────────────
html = html.replace(
    '\n        <div class="lesson-nav">\n            <a href="#leccion-1" class="ln-next">Leccion anterior: Del PEA al Feasibility Study &rarr;</a>\n        </div>\n    </div>\n\n',
    '\n    </div>\n\n'
)

# ── 2. CONTENIDO ADICIONAL para insertar ANTES del </div> final de leccion-4 ─
# Buscar el cierre de lesson-body de leccion-4
# El key-takeaway es lo ultimo antes del cierre

contenido_extra = """
            <h3>Caso real</h3>

            <div class="case-study">
                <div class="cs-header">
                    <span class="cs-icon">&#9874;</span>
                    <span class="cs-label">Caso de estudio</span>
                </div>
                <div class="cs-title">Benchmark 2016: TC/RC en maximos historicos — el otro extremo</div>
                <p>En 2016, el benchmark anual se nego con TC de US$97,35/t y RC de 9,735 cents/lb — los niveles mas altos en decadas. Ese ano, las mineras debian pagar casi US$100 por cada tonelada de concentrado que enviaban a fundir. ¿Por que? Porque habia exceso de concentrado en el mercado (expansion de minas en Peru y Chile) y deficit de capacidad de fundicion. Las fundidoras tenian el poder.</p>
                <p>Diez anos despues, en 2026, la situacion es exactamente la inversa: TC/RC = 0. El mismo indicador que en 2016 favorecia a las fundidoras hoy favorece completamente a las mineras. <strong>Leccion:</strong> el TC/RC es un pendulo que mide donde esta el poder en la cadena del cobre. Saber leerlo te dice quien gana y quien pierde en cada ciclo del mercado.</p>
                <p>Para Chile especificamente: en 2016, Codelco y AMSA pagaban US$97/t por fundir su concentrado. En 2026, lo funden practicamente gratis. En terminos de margen operacional, esa diferencia de US$97/t sobre millones de toneladas de concentrado equivale a <strong>cientos de millones de dolares adicionales de flujo de caja al ano</strong> para las mineras chilenas.</p>
                <p class="cs-source">Fuentes: Metal Bulletin Concentrates Conference 2016; IEA Copper Commentary marzo 2026; AMSA Annual Report 2026</p>
            </div>

            <h3>Vocabulario tecnico</h3>

            <table class="vocab-table">
                <thead>
                    <tr><th>Espanol</th><th>English</th><th>Contexto de uso</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Tarifa de tratamiento</td>
                        <td><span class="v-english">Treatment Charge (TC)</span></td>
                        <td><div class="v-context">"The 2026 benchmark TC was set at zero for the first time, reflecting extreme concentrate tightness."</div></td>
                    </tr>
                    <tr>
                        <td>Tarifa de refinacion</td>
                        <td><span class="v-english">Refining Charge (RC)</span></td>
                        <td><div class="v-context">"Spot RC turned negative in Q1 2026 as smelters competed for scarce concentrate."</div></td>
                    </tr>
                    <tr>
                        <td>Concentrado de cobre</td>
                        <td><span class="v-english">Copper concentrate</span></td>
                        <td><div class="v-context">"The mine ships 35% copper concentrate via slurry pipeline to the port of Mejillones."</div></td>
                    </tr>
                    <tr>
                        <td>Fundicion</td>
                        <td><span class="v-english">Smelter / Smelting plant</span></td>
                        <td><div class="v-context">"Jiangxi Copper operates the largest copper smelter in China with 900,000 t/year of capacity."</div></td>
                    </tr>
                    <tr>
                        <td>Ajuste de penalidades</td>
                        <td><span class="v-english">Penalty deductions</span></td>
                        <td><div class="v-context">"The off-take agreement includes penalty deductions for arsenic above 0.3% in the concentrate."</div></td>
                    </tr>
                    <tr>
                        <td>Precio neto de fundicion</td>
                        <td><span class="v-english">Net smelter return (NSR)</span></td>
                        <td><div class="v-context">"The royalty is calculated as 2% of NSR, after deducting TC/RC and penalty deductions."</div></td>
                    </tr>
                    <tr>
                        <td>Cuota de produccion coordinada</td>
                        <td><span class="v-english">Coordinated production cut (CSPT)</span></td>
                        <td><div class="v-context">"The CSPT announced a voluntary 10% production cut to reduce concentrate demand and recover TC/RC levels."</div></td>
                    </tr>
                </tbody>
            </table>

            <h3>Ejercicio mental</h3>

            <div class="exercise-box">
                <div class="ex-header">Piensa como el CFO de una minera de concentrados</div>
                <p>Tu minera produce 200.000 toneladas de concentrado de cobre al ano (con 30% de cobre contenido = 60.000 t de cobre fino). Compara los dos escenarios:</p>
                <ul>
                    <li><strong>Escenario A (2016):</strong> TC = US$97/t de concentrado; RC = 9,7 cents/lb de Cu fino</li>
                    <li><strong>Escenario B (2026):</strong> TC = US$0/t de concentrado; RC = 0 cents/lb de Cu fino</li>
                </ul>
                <p><strong>Pregunta 1:</strong> ¿Cuanto paga tu minera en TC en el Escenario A? ¿Y en el B?</p>
                <p><strong>Pregunta 2:</strong> Si el precio del cobre es US$5/lb en ambos escenarios y tu costo operacional es US$2/lb, ¿cual es tu margen neto por libra en cada escenario?</p>
                <p><strong>Pregunta 3:</strong> Si la fundidora tiene un costo fijo de US$60/t de concentrado para operar, ¿cuanto tiempo puede sobrevivir con TC = 0 antes de cerrar? ¿Que senial envia ese cierre al precio del cobre?</p>
            </div>

            <h3>Datos que pocos saben</h3>

            <div class="concept-box">
                <div class="cb-term">El TC/RC tiene un "precio sombra" de escasez</div>
                <div class="cb-def">Cuando el TC cae por debajo de US$20/t, las fundidoras tipicamente empiezan a operar en margen negativo. Sin embargo, no cierran de inmediato porque el costo de apagar y relanzar una fundidora de gran escala supera los US$50M y toma entre 3 y 6 meses de operacion deficitaria. Este umbral "de aguante" de las fundidoras es lo que permite al TC/RC llegar a cero o negativo durante periodos de tiempo, creando una burbuja de soporte artificial para los productores de concentrado.</div>
            </div>

            <div class="concept-box">
                <div class="cb-term">Las fundidoras chinas pierden, pero sus minas ganan</div>
                <div class="cb-def">Muchas de las grandes fundidoras chinas (Jiangxi Copper, Tongling) son tambien companias mineras con activos en Chile, Peru y Africa. Cuando los TC/RC son bajos, la division de fundicion pierde margen, pero la division minera (que vende concentrado al mercado) gana exactamente esa diferencia. Por eso, el verdadero impacto de TC/RC = 0 para una empresa integrada verticalmente es mas complejo que para una minera pura o una fundidora pura.</div>
            </div>

            <div class="concept-box">
                <div class="cb-term">El "precio del maquilaje" en Chile</div>
                <div class="cb-def">Codelco envia parte de su concentrado a la fundidora de Chuquicamata (propia) y otra parte a fundidoras en Asia via contratos de largo plazo. Cuando los benchmarks anuales se firman a TC bajos, Codelco se beneficia doblemente: no paga el maquila externo (o lo paga minimo) y el precio spot del cobre catodo refleja la escasez de oferta. En 2026, este efecto combinado equivale a un "subsidio implicito" de varias centenas de millones de dolares sobre los estados de resultados de Codelco.</div>
            </div>

"""

# Insertar antes del key-takeaway (que es lo ultimo en lesson-body de leccion-4)
old_anchor = '            <div class="key-takeaway">\n                <h4>Para llevarte a una reunion</h4>'
html = html.replace(old_anchor, contenido_extra + '            <div class="key-takeaway">\n                <h4>Para llevarte a una reunion</h4>', 1)

with open(f"{BASE}/escuela.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Leccion 4 completada. Largo total: {len(html)}")
print("Caso de estudio:", 'Benchmark 2016' in html)
print("Vocabulario:", 'Treatment Charge (TC)' in html)
print("Ejercicio:", 'CFO de una minera' in html)
print("Datos pocos saben:", 'precio sombra' in html)
print("Lesson-nav eliminado:", 'Leccion anterior: Del PEA' not in html)
