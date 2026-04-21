f = 'C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero/precios.html'
with open(f, encoding='utf-8') as fh:
    html = fh.read()

# 1. Add Ed.8 to EDITIONS array
html = html.replace(
    "    { id: 7, label: 'Ed.7', date: '14/04' }\n];",
    "    { id: 7, label: 'Ed.7', date: '14/04' },\n    { id: 8, label: 'Ed.8', date: '21/04' }\n];"
)

# 2. Push Ed.8 prices to each COMMODITIES array
# Cobre USD/t
html = html.replace(
    "prices: [12400, 12530, 12678, 12201, 12200, 12424, 12630]",
    "prices: [12400, 12530, 12678, 12201, 12200, 12424, 12630, 13320]"
)
# Cobre USD/lb
html = html.replace(
    "prices: [5.63, 5.68, 5.75, 5.45, 5.55, 5.90, 5.81]",
    "prices: [5.63, 5.68, 5.75, 5.45, 5.55, 5.90, 5.81, 6.04]"
)
# Litio Carbonato
html = html.replace(
    "prices: [18500, 19200, 20256, 24086, 20100, 21650, 21650]",
    "prices: [18500, 19200, 20256, 24086, 20100, 21650, 21650, 22500]"
)
# Platino
html = html.replace(
    "prices: [1580, 1610, 1650, 1905, 1978, 1991, 2044]",
    "prices: [1580, 1610, 1650, 1905, 1978, 1991, 2044, 2074]"
)
# Paladio
html = html.replace(
    "prices: [1640, 1655, 1685, 1388, 1523, 1501, 1507]",
    "prices: [1640, 1655, 1685, 1388, 1523, 1501, 1507, 1576]"
)
# Rodio
html = html.replace(
    "prices: [11200, 11500, 11700, 10000, 10250, 10350, 10100]",
    "prices: [11200, 11500, 11700, 10000, 10250, 10350, 10100, 9800]"
)
# NdPr Oxido
html = html.replace(
    "prices: [96.5, 102.0, 108.64, 108.64, 108.64, 124.87, 126.0]",
    "prices: [96.5, 102.0, 108.64, 108.64, 108.64, 124.87, 126.0, 126.0]"
)
# Cobalto
html = html.replace(
    "prices: [54800, 55500, 56290, 56290, 56290, 56290, 56290]",
    "prices: [54800, 55500, 56290, 56290, 56290, 56290, 56290, 56290]"
)
# Oro
html = html.replace(
    "prices: [5350, 5114, 5025, 4419, 4747, 4656, 4735]",
    "prices: [5350, 5114, 5025, 4419, 4747, 4656, 4735, 4782]"
)
# Plata
html = html.replace(
    "prices: [88.20, 83.97, 80.10, 69.54, 75.07, 72.26, 75.55]",
    "prices: [88.20, 83.97, 80.10, 69.54, 75.07, 72.26, 75.55, 79.50]"
)
# CLP/USD
html = html.replace(
    "prices: [885, 898, 908, 915, 924, 917, 902]",
    "prices: [885, 898, 908, 915, 924, 917, 902, 881]"
)
# H2SO4
html = html.replace(
    "prices: [149, 149, 149, 149, 140, 171, 246]",
    "prices: [149, 149, 149, 149, 140, 171, 246, 270]"
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(html)

print('precios.html updated.')
print('Ed.8 in EDITIONS:', "{ id: 8, label: 'Ed.8'" in html)
print('Cobre USD/lb 6.04:', '6.04]' in html)
print('Oro 4782:', '4782]' in html)
print('H2SO4 270:', '270]' in html)