import re

f = 'C:/Users/diego.varleta/CLAUDE/02_Noticiero_Minero/proyecciones.html'
with open(f, encoding='utf-8') as fh:
    html = fh.read()

# Update Spot Actual values (column 2 in params-table)
# Pattern: <tr class="highlight"><td>Cobre</td><td>OLD</td>
replacements = [
    # Cobre USD/lb (highlight row)
    ('<tr class="highlight"><td>Cobre</td><td>5.81</td>', '<tr class="highlight"><td>Cobre</td><td>6.04</td>'),
    # Cobre USD/t (highlight row)
    ('<tr class="highlight"><td>Cobre</td><td>12,630</td>', '<tr class="highlight"><td>Cobre</td><td>13,320</td>'),
    # Litio Carbonato
    ('<tr><td>Litio Carbonato</td><td>21,650</td>', '<tr><td>Litio Carbonato</td><td>22,500</td>'),
    # Oro
    ('<tr><td>Oro</td><td>4,735</td>', '<tr><td>Oro</td><td>4,782</td>'),
    # Plata
    ('<tr><td>Plata</td><td>75.55</td>', '<tr><td>Plata</td><td>79.50</td>'),
    # Platino - also update optimista scenario given 4th consecutive deficit
    ('<tr><td>Platino</td><td>2,044</td><td>1,400</td><td>1,900</td><td>2,450</td>',
     '<tr><td>Platino</td><td>2,074</td><td>1,500</td><td>2,000</td><td>2,700</td>'),
    # Paladio
    ('<tr><td>Paladio</td><td>1,507</td>', '<tr><td>Paladio</td><td>1,576</td>'),
    # H2SO4 - update spot and scenarios (China ban efectivo mayo)
    ('<tr><td>H2SO4 Chile</td><td>246</td><td>180</td><td>260</td><td>380</td><td>USD/t CFR</td><td>🚨 China ban desde mayo (+44% mes)</td>',
     '<tr><td>H2SO4 Chile</td><td>270</td><td>220</td><td>310</td><td>450</td><td>USD/t CFR</td><td>&#128680; China ban efectivo mayo (+54% desde dic)</td>'),
    # Brent
    ('<tr><td>Petroleo Brent</td><td>102</td><td>75</td><td>95</td><td>125</td>',
     '<tr><td>Petroleo Brent</td><td>96</td><td>70</td><td>90</td><td>120</td>'),
    # CLP/USD
    ('<tr><td>CLP/USD</td><td>902</td><td>840</td><td>890</td><td>950</td>',
     '<tr><td>CLP/USD</td><td>881</td><td>830</td><td>875</td><td>930</td>'),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new, 1)
        print(f'Updated: {old[:50]}...')
    else:
        print(f'NOT FOUND: {old[:60]}')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(html)

print('proyecciones.html saved.')