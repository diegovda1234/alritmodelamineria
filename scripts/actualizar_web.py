"""
actualizar_web.py — Auto-actualiza precios.html, proyecciones.html e historial_precios.json.

Uso:
    python scripts/actualizar_web.py Noticiero_Minero_Ed014_2026-06-02.md
    python scripts/actualizar_web.py Noticiero_Minero_Ed014_2026-06-02.md --dry-run

El script:
1. Parsea la tabla "## 📊 DASHBOARD DE PRECIOS SPOT" del .md
2. Agrega la edición nueva a precios.html (EDITIONS array + 12 COMMODITIES arrays)
3. Actualiza la columna Spot Actual en proyecciones.html + cabeceras cs-spot
4. Actualiza historial_precios.json con la serie histórica (usado por análisis multi-semana)
5. Reporta cada cambio antes de aplicarlo
"""

import re
import sys
import os
import json

# Forzar UTF-8 en stdout para Windows (evita UnicodeEncodeError con tildes/flechas)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURACIÓN ----------------------------------------------------------

BASE_DIR          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRECIOS_HTML      = os.path.join(BASE_DIR, "precios.html")
PROYECCIONES_HTML = os.path.join(BASE_DIR, "proyecciones.html")
HISTORIAL_JSON    = os.path.join(BASE_DIR, "historial_precios.json")

# Mapeo: nombre en el dashboard .md → clave interna
MINERAL_MAP = {
    "cobre":           "cu_t",
    "cu usd/t":        "cu_t",
    "cu usd/lb":       "cu_lb",
    "litio":           "li",
    "litio carbonato": "li",
    "platino":         "pt",
    "paladio":         "pd",
    "rodio":           "rh",
    "ndpr":            "ndpr",
    "ndpr óxido": "ndpr",
    "ndpr oxido":      "ndpr",
    "cobalto":         "co",
    "oro":             "au",
    "plata":           "ag",
    "clp/usd":         "clp",
    "clp":             "clp",
    "brent":           "brent",
    "h2so4":           "h2so4",
    "h₂so₄":  "h2so4",   # subscript variant H₂SO₄
    "ácido sulfúrico": "h2so4",
    "acido sulfurico":  "h2so4",
}

# Orden de los 12 commodities en precios.html (debe coincidir con el array COMMODITIES)
COMMODITIES_ORDER = ["cu_t", "cu_lb", "li", "pt", "pd", "rh", "ndpr", "co", "au", "ag", "clp", "h2so4"]

# Textos de búsqueda únicos en proyecciones.html para cada commodity (params-table)
PROYECCIONES_ROWS = {
    "cu_lb":  ("<td>Cobre</td>",           lambda v: f"<td>Cobre</td><td>{v}</td>",   r"<td>Cobre</td><td>[0-9.,]+</td>"),
    "cu_t":   ("<td>Cobre</td>",           None, None),   # se actualiza via cu_lb row + cs-spot
    "li":     ("<td>Litio Carbonato</td>", lambda v: f"<td>Litio Carbonato</td><td>{fmt_num(v, comma=True)}</td>",
                                            r"<td>Litio Carbonato</td><td>[0-9.,]+</td>"),
    "au":     ("<td>Oro</td>",             lambda v: f"<td>Oro</td><td>{fmt_num(v, comma=True)}</td>",
                                            r"<td>Oro</td><td>[0-9.,]+</td>"),
    "ag":     ("<td>Plata</td>",           lambda v: f"<td>Plata</td><td>{v}</td>",
                                            r"<td>Plata</td><td>[0-9.,]+</td>"),
    "pt":     ("<td>Platino</td>",         lambda v: f"<td>Platino</td><td>{fmt_num(v, comma=True)}</td>",
                                            r"<td>Platino</td><td>[0-9.,]+</td>"),
    "pd":     ("<td>Paladio</td>",         lambda v: f"<td>Paladio</td><td>{fmt_num(v, comma=True)}</td>",
                                            r"<td>Paladio</td><td>[0-9.,]+</td>"),
    "co":     ("<td>Cobalto</td>",         lambda v: f"<td>Cobalto</td><td>{fmt_num(v, comma=True)}</td>",
                                            r"<td>Cobalto</td><td>[0-9.,]+</td>"),
    "ndpr":   ("<td>NdPr Oxido</td>",      lambda v: f"<td>NdPr Oxido</td><td>{v}</td>",
                                            r"<td>NdPr Oxido</td><td>[0-9.,]+</td>"),
    "h2so4":  ("<td>H2SO4 Chile</td>",     lambda v: f"<td>H2SO4 Chile</td><td>{int(float(v))}</td>",
                                            r"<td>H2SO4 Chile</td><td>[0-9.,]+</td>"),
    "brent":  ("<td>Petroleo Brent</td>",  lambda v: f"<td>Petroleo Brent</td><td>{int(float(v))}</td>",
                                            r"<td>Petroleo Brent</td><td>[0-9.,]+</td>"),
    "clp":    ("<td>CLP/USD</td>",         lambda v: f"<td>CLP/USD</td><td>{int(float(v))}</td>",
                                            r"<td>CLP/USD</td><td>[0-9.,]+</td>"),
}

# --- HELPERS ----------------------------------------------------------------

def fmt_num(val, comma=False):
    """Formatea número con separador de miles si es >= 1000."""
    try:
        n = float(str(val).replace(",", ""))
        if comma and n >= 1000:
            return f"{n:,.0f}".replace(",", ",")  # Mantener coma como sep de miles
        return str(val)
    except:
        return str(val)

def parse_price_raw(s):
    """Extrae número limpio. Maneja formato europeo: '6,36' → '6.36', '14.015' → '14015'."""
    s = re.sub(r'\*+', '', s)   # strip markdown bold
    s = s.replace('~', '')       # strip approximate
    m = re.search(r'([\d.,]+)', s)
    if not m:
        return ""
    num_str = m.group(1).strip('.,')
    has_comma  = ',' in num_str
    has_period = '.' in num_str
    if has_comma and not has_period:
        after = num_str.split(',')[-1]
        if len(after) <= 2:                       # decimal europeo: "6,36"
            return str(round(float(num_str.replace(',', '.')), 2))
        else:                                      # miles inglés: "14,015"
            return num_str.replace(',', '')
    elif has_period and not has_comma:
        after = num_str.split('.')[-1]
        if len(after) == 3:                        # miles europeo: "14.015"
            return num_str.replace('.', '')
        else:                                      # decimal inglés: "6.36"
            return num_str
    elif has_comma and has_period:
        if num_str.rfind(',') > num_str.rfind('.'):
            return str(round(float(num_str.replace('.','').replace(',','.')), 2))
        else:
            return str(round(float(num_str.replace(',','')), 2))
    else:
        return num_str

# --- PARSER DEL MARKDOWN ----------------------------------------------------

def parse_md_prices(md_path):
    """Lee el .md y extrae precios de la tabla DASHBOARD DE PRECIOS SPOT."""
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    # Extraer número de edición y fecha
    ed_match = re.search(r'\*\*Edici[oó]n N[°º]?:?\*\*\s*(\d+)', content)
    date_match = re.search(r'\*\*Fecha de publicaci[oó]n:\*\*\s*(.+)', content)
    ed_num = int(ed_match.group(1)) if ed_match else None
    pub_date = date_match.group(1).strip() if date_match else ""

    # Parsear fecha a DD/MM
    months = {"enero":"01","febrero":"02","marzo":"03","abril":"04","mayo":"05",
              "junio":"06","julio":"07","agosto":"08","septiembre":"09",
              "octubre":"10","noviembre":"11","diciembre":"12"}
    date_label = ""
    dm = re.search(r'(\d{1,2})\s+de\s+(\w+)', pub_date, re.IGNORECASE)
    if dm:
        day, mon = dm.group(1), dm.group(2).lower()
        date_label = f"{int(day):02d}/{months.get(mon,'??')}"

    # Encontrar tabla de precios
    prices = {}
    in_table = False
    for line in content.split("\n"):
        if "DASHBOARD DE PRECIOS SPOT" in line or "DASHBOARD DE PRECIOS" in line:
            in_table = True
            continue
        if in_table:
            if re.match(r'^## ', line) and "DASHBOARD" not in line:
                break
            if not line.startswith("|") or "---" in line or "Mineral" in line:
                continue
            cols = [c.strip() for c in line.split("|")]
            cols = [c for c in cols if c]
            if len(cols) < 2:
                continue
            mineral_raw = cols[0].lower().strip()
            # Col 3 (index 2) = precio actual (Ed.N, bold); col 2 = precio anterior
            price_raw = cols[2].strip() if len(cols) > 2 else (cols[1].strip() if len(cols) > 1 else "")

            # Normalizar nombre de mineral
            key = None
            for k, v in MINERAL_MAP.items():
                if k in mineral_raw:
                    key = v
                    break

            # Detectar si es USD/lb o USD/t para cobre (leer del precio actual)
            if "cobre" in mineral_raw:
                price_lower = price_raw.lower()
                if "lb" in price_lower:
                    key = "cu_lb"
                elif "/t" in price_lower or "usd/t" in price_lower:
                    key = "cu_t"

            if key and price_raw:
                val = parse_price_raw(price_raw)
                if val:
                    prices[key] = val

    return ed_num, date_label, prices

# --- ACTUALIZAR PRECIOS.HTML ------------------------------------------------

def update_precios(content, ed_num, date_label, prices, dry_run):
    changes = []

    # 1. Agregar entrada a EDITIONS
    last_ed_pat = re.compile(r"\{ id: \d+, label: 'Ed\.\d+', date: '[^']+' \}")
    matches = list(last_ed_pat.finditer(content))
    if matches:
        last = matches[-1]
        last_id_m = re.search(r"id: (\d+)", last.group())
        last_id = int(last_id_m.group(1)) if last_id_m else 0
        if last_id < ed_num:
            new_entry = f",\n    {{ id: {ed_num}, label: 'Ed.{ed_num}', date: '{date_label}' }}"
            changes.append(f"EDITIONS: agregar Ed.{ed_num} ({date_label})")
            if not dry_run:
                content = content[:last.end()] + new_entry + content[last.end():]
        else:
            print(f"  [!] Ed.{ed_num} ya existe en EDITIONS — saltando")

    # 2. Agregar precio a cada COMMODITY array
    # Buscar cada prices: [...] por orden de COMMODITIES_ORDER
    commodity_prices_pat = re.compile(r"prices: \[([^\]]+)\]")
    com_matches = list(commodity_prices_pat.finditer(content))

    if len(com_matches) < len(COMMODITIES_ORDER):
        print(f"  [!] Se esperaban {len(COMMODITIES_ORDER)} arrays de prices, se encontraron {len(com_matches)}")

    for i, key in enumerate(COMMODITIES_ORDER):
        if i >= len(com_matches):
            break
        m = com_matches[i]
        # Ajustar posición por inserciones previas
        # Encontrar el array actual en el contenido modificado
        actual_match = list(commodity_prices_pat.finditer(content))[i] if not dry_run else m

        val = prices.get(key)
        if not val:
            print(f"  [!] Sin precio para {key} — saltando")
            continue

        # Verificar que no esté ya
        arr_content = actual_match.group(1) if not dry_run else m.group(1)
        last_vals = arr_content.strip().split(",")
        last_num = len(last_vals)

        if last_num >= ed_num:
            print(f"  [!] {key}: ya tiene {last_num} valores — saltando")
            continue

        new_arr = actual_match.group(1).rstrip() + f", {val}"
        changes.append(f"COMMODITIES[{key}]: agregar {val}")
        if not dry_run:
            new_str = f"prices: [{new_arr}]"
            content = content[:actual_match.start()] + new_str + content[actual_match.end():]

    return content, changes

# --- ACTUALIZAR PROYECCIONES.HTML -------------------------------------------

def update_proyecciones(content, prices, dry_run):
    changes = []

    updates = {
        "cu_lb":  (prices.get("cu_lb"), r"(<td>Cobre</td><td>)[0-9.,]+(<\/td>)", 1),
        "cu_t":   (prices.get("cu_t"),  r"(<td>Cobre</td><td>)[0-9.,]+(<\/td><td>[0-9.,]+<\/td><td>[0-9.,]+<\/td><td>USD\/t<\/td>)", 1),
        "li":     (prices.get("li"),    r"(<td>Litio Carbonato<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "au":     (prices.get("au"),    r"(<td>Oro<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "ag":     (prices.get("ag"),    r"(<td>Plata<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "pt":     (prices.get("pt"),    r"(<td>Platino<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "pd":     (prices.get("pd"),    r"(<td>Paladio<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "co":     (prices.get("co"),    r"(<td>Cobalto<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "ndpr":   (prices.get("ndpr"),  r"(<td>NdPr Oxido<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "h2so4":  (prices.get("h2so4"), r"(<td>H2SO4 Chile<\/td><td>)[0-9.,]+(<\/td>)", 1),
        "clp":    (prices.get("clp"),   r"(<td>CLP\/USD<\/td><td>)[0-9.,]+(<\/td>)", 1),
    }

    # Brent viene de la tabla, no del dashboard estándar — buscarlo en el md si está
    # (no es crítico, se puede actualizar manual)

    for key, (val, pattern, _) in updates.items():
        if not val:
            continue
        # Para cu_t en params table, es la segunda fila de Cobre (USD/t)
        if key == "cu_t":
            # Más específico: buscar la fila con USD/t
            pat = r"(<td>Cobre<\/td><td>)[0-9.,]+(<\/td><td>[0-9.,]+<\/td><td>[0-9.,]+<\/td><td>[0-9.,]+<\/td><td>USD\/t<\/td>)"
            m = re.search(pat, content)
            if m:
                new_content = re.sub(pat, lambda x: x.group(1) + fmt_num(val, comma=True) + x.group(2), content, count=1)
                if new_content != content:
                    changes.append(f"proyecciones Spot {key}: → {val}")
                    if not dry_run:
                        content = new_content
            continue

        m = re.search(pattern, content)
        if m:
            new_val = fmt_num(val, comma=True) if float(val.replace(",","")) >= 1000 else val
            new_content = re.sub(pattern, lambda x: x.group(1) + new_val + x.group(2), content, count=1)
            if new_content != content:
                changes.append(f"proyecciones Spot {key}: → {new_val}")
                if not dry_run:
                    content = new_content

    # Actualizar cs-spot headers
    cu_lb = prices.get("cu_lb")
    cu_t  = prices.get("cu_t")
    if cu_lb and cu_t:
        spot_cu = f"${cu_lb}/lb — ${fmt_num(cu_t, comma=True)}/t"
        pat = r'(\$[\d.,]+/lb — \$[\d.,]+/t)'
        if re.search(pat, content):
            changes.append(f"cs-spot Cobre: → {spot_cu}")
            if not dry_run:
                content = re.sub(pat, spot_cu, content)

    li = prices.get("li")
    if li:
        pat2 = r'(id="cs-li"[^>]*>.*?<span class="cs-spot">)\$[\d.,]+/t'
        m2 = re.search(pat2, content, re.DOTALL)
        if m2:
            new_li_spot = f"${fmt_num(li, comma=True)}/t"
            changes.append(f"cs-spot Litio: → {new_li_spot}")
            if not dry_run:
                content = re.sub(pat2, lambda x: x.group(1) + new_li_spot, content, flags=re.DOTALL, count=1)

    au = prices.get("au")
    if au:
        pat = r'(id="cs-gold"[^>]*>.*?<span class="cs-spot">)\$[\d.,]+/oz'
        m = re.search(pat, content, re.DOTALL)
        if m:
            new_au = f"${fmt_num(au, comma=True)}/oz"
            changes.append(f"cs-spot Oro: → {new_au}")
            if not dry_run:
                content = re.sub(pat, lambda x: x.group(1) + new_au, content, flags=re.DOTALL, count=1)

    pt  = prices.get("pt")
    pd  = prices.get("pd")
    rh  = prices.get("rh")
    if pt and pd and rh:
        new_pgm = f"Pt ${fmt_num(pt,comma=True)} | Pd ${fmt_num(pd,comma=True)} | Rh ${fmt_num(rh,comma=True)}"
        pat = r'Pt \$[\d.,]+ \| Pd \$[\d.,]+ \| Rh \$[\d.,]+'
        if re.search(pat, content):
            changes.append(f"cs-spot PGM: → {new_pgm}")
            if not dry_run:
                content = re.sub(pat, new_pgm, content)

    h2so4 = prices.get("h2so4")
    if h2so4:
        pat = r'H2SO4 \$[\d.,]+/t'
        if re.search(pat, content):
            changes.append(f"cs-spot H2SO4: → H2SO4 ${h2so4}/t")
            if not dry_run:
                content = re.sub(pat, f"H2SO4 ${h2so4}/t", content)

    clp = prices.get("clp")
    if clp:
        pat = r'CLP [\d.]+'
        if re.search(pat, content):
            changes.append(f"cs-spot CLP: → CLP {clp}")
            if not dry_run:
                content = re.sub(pat, f"CLP {clp}", content)

    return content, changes

# --- HISTORIAL DE PRECIOS ---------------------------------------------------

def update_historial(ed_num, date_label, prices, dry_run=False):
    """
    Mantiene historial_precios.json con la serie histórica de precios por edición.
    Usado por el análisis de tendencia multi-semana del skill NoticieroMinero.

    Estructura JSON:
    {
      "ediciones": [
        {"ed": 13, "date": "26/05", "cu_lb": "6.36", "cu_t": "14015", ...},
        ...
      ]
    }
    Las ediciones están ordenadas de más antigua a más reciente.
    """
    # Leer historial existente
    if os.path.exists(HISTORIAL_JSON):
        with open(HISTORIAL_JSON, encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = {"ediciones": []}

    # Verificar si esta edición ya está registrada
    existing = [e for e in historial["ediciones"] if e.get("ed") == ed_num]
    if existing:
        return f"historial_precios.json: Ed.{ed_num} ya registrada — sin cambios"

    # Agregar entrada nueva
    entry = {"ed": ed_num, "date": date_label}
    entry.update(prices)

    historial["ediciones"].append(entry)
    # Mantener orden por número de edición
    historial["ediciones"].sort(key=lambda x: x["ed"])

    if not dry_run:
        with open(HISTORIAL_JSON, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)

    return f"historial_precios.json: Ed.{ed_num} agregada ({len(historial['ediciones'])} ediciones totales)"


# --- MAIN -------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/actualizar_web.py <archivo.md> [--dry-run]")
        sys.exit(1)

    md_file  = sys.argv[1]
    dry_run  = "--dry-run" in sys.argv

    if not os.path.isabs(md_file):
        md_file = os.path.join(BASE_DIR, md_file)

    if not os.path.exists(md_file):
        print(f"[ERROR] Archivo no encontrado: {md_file}")
        sys.exit(1)

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Procesando: {os.path.basename(md_file)}")
    print("-" * 60)

    # Parsear precios del markdown
    ed_num, date_label, prices = parse_md_prices(md_file)

    if not ed_num:
        print("[ERROR] No se encontró número de edición en el .md")
        sys.exit(1)

    print(f"Edición detectada: Ed.{ed_num} ({date_label})")
    print(f"Precios encontrados: {len(prices)}")
    for k, v in prices.items():
        print(f"  {k:8s} → {v}")

    if len(prices) < 8:
        print(f"\n[ADVERTENCIA] Solo se encontraron {len(prices)} precios.")
        print("Verificar que la tabla DASHBOARD DE PRECIOS SPOT esté en el formato correcto.")
        if not dry_run:
            resp = input("¿Continuar de todos modos? (s/N): ")
            if resp.lower() != "s":
                sys.exit(0)

    print()

    # Actualizar precios.html
    print("=== precios.html ===")
    with open(PRECIOS_HTML, encoding="utf-8") as f:
        precios_content = f.read()

    precios_new, precios_changes = update_precios(precios_content, ed_num, date_label, prices, dry_run)

    if precios_changes:
        for ch in precios_changes:
            print(f"  {'[DRY] ' if dry_run else '[OK] '}{ch}")
        if not dry_run:
            with open(PRECIOS_HTML, "w", encoding="utf-8") as f:
                f.write(precios_new)
            print(f"  Guardado: {PRECIOS_HTML}")
    else:
        print("  Sin cambios necesarios.")

    print()

    # Actualizar proyecciones.html
    print("=== proyecciones.html ===")
    with open(PROYECCIONES_HTML, encoding="utf-8") as f:
        proy_content = f.read()

    proy_new, proy_changes = update_proyecciones(proy_content, prices, dry_run)

    if proy_changes:
        for ch in proy_changes:
            print(f"  {'[DRY] ' if dry_run else '[OK] '}{ch}")
        if not dry_run:
            with open(PROYECCIONES_HTML, "w", encoding="utf-8") as f:
                f.write(proy_new)
            print(f"  Guardado: {PROYECCIONES_HTML}")
    else:
        print("  Sin cambios necesarios.")

    # Actualizar historial_precios.json
    print("=== historial_precios.json ===")
    msg = update_historial(ed_num, date_label, prices, dry_run)
    print(f"  {'[DRY] ' if dry_run else '[OK] '}{msg}")

    print()
    if dry_run:
        print("=== DRY RUN completado — ningún archivo fue modificado ===")
    else:
        print(f"=== Actualización completada — Ed.{ed_num} incorporada ===")
        print("Próximos pasos: generar_pdf.py → rebuild_index.py → github_deploy.py")

if __name__ == "__main__":
    main()
