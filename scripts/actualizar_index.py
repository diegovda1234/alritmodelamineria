"""
actualizar_index.py — Regenera index.html con la lista de todas las ediciones disponibles.
Se llama automáticamente desde actualizar_noticiero.bat después de generar el HTML.
"""

import re
from pathlib import Path
from datetime import datetime

CARPETA = Path(__file__).parent.parent  # Noticiero_Minero/

HTML_INDEX = """\
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Al Ritmo de la Minería — Diego Varleta</title>
    <style>
        :root {{
            --copper: #B87333;
            --dark:   #1a1a2e;
            --gold:   #e2b96f;
            --bg:     #f8f9fa;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', Inter, sans-serif;
            background: var(--bg);
            color: #212529;
            min-height: 100vh;
        }}
        header {{
            background: linear-gradient(135deg, var(--dark) 0%, #0f3460 100%);
            color: white;
            padding: 28px 24px 24px;
            text-align: center;
        }}
        header h1 {{
            font-size: clamp(20px, 5vw, 32px);
            letter-spacing: -0.5px;
            color: var(--gold);
            margin-bottom: 6px;
        }}
        header p {{
            font-size: 13px;
            color: rgba(255,255,255,0.6);
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }}
        .container {{
            max-width: 720px;
            margin: 32px auto;
            padding: 0 16px 48px;
        }}
        .section-title {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #6c757d;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        .card-list {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .card {{
            background: white;
            border: 1px solid #dee2e6;
            border-left: 4px solid var(--copper);
            border-radius: 8px;
            padding: 16px 20px;
            text-decoration: none;
            color: inherit;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: box-shadow 0.15s, transform 0.1s;
        }}
        .card:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.10);
            transform: translateY(-1px);
        }}
        .card-title {{
            font-weight: 600;
            font-size: 15px;
            color: var(--dark);
        }}
        .card-meta {{
            font-size: 12px;
            color: #6c757d;
            margin-top: 3px;
        }}
        .badge {{
            background: var(--copper);
            color: white;
            font-size: 10px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 12px;
            white-space: nowrap;
        }}
        .badge.latest {{
            background: #28a745;
        }}
        footer {{
            text-align: center;
            font-size: 11px;
            color: #adb5bd;
            padding: 20px;
        }}
        @media (max-width: 500px) {{
            .card {{ flex-direction: column; align-items: flex-start; gap: 8px; }}
        }}
    </style>
</head>
<body>
<header>
    <h1>Al Ritmo de la Minería</h1>
    <p>Inteligencia Minera Estratégica · Diego Varleta</p>
</header>
<div class="container">
    <p class="section-title">Ediciones disponibles</p>
    <div class="card-list">
{cards}
    </div>
</div>
<footer>Actualizado el {fecha_update} · Uso personal y confidencial</footer>
</body>
</html>
"""

CARD_TEMPLATE = """\
        <a class="card" href="{filename}">
            <div>
                <div class="card-title">Edición N° {num} — {periodo}</div>
                <div class="card-meta">Publicado: {fecha_archivo}</div>
            </div>
            <span class="badge{badge_class}">{badge_label}</span>
        </a>"""


def extraer_info_md(md_path: Path) -> dict:
    """Lee el .md para extraer período y énfasis editorial."""
    info = {"periodo": "—", "enfasis": "—"}
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
        for line in text.split("\n")[:15]:
            if "**Período:**" in line:
                info["periodo"] = line.replace("**Período:**", "").strip().strip("*")
            elif "**Énfasis editorial" in line:
                parts = line.split(":**")
                if len(parts) > 1:
                    info["enfasis"] = parts[1].strip().strip("*")
    except Exception:
        pass
    return info


def main():
    # Buscar todos los HTMLs de ediciones
    htmls = sorted(CARPETA.glob("Noticiero_Minero_Ed*.html"), reverse=True)

    if not htmls:
        print("[AVISO] No se encontraron archivos HTML de ediciones.")
        return

    cards = []
    for i, html_path in enumerate(htmls):
        # Extraer número de edición del nombre de archivo
        m = re.search(r"Ed(\d+)", html_path.name)
        num = int(m.group(1)) if m else 0

        # Extraer fecha del nombre de archivo
        m_date = re.search(r"(\d{4}-\d{2}-\d{2})", html_path.name)
        fecha_archivo = m_date.group(1) if m_date else "—"

        # Leer .md correspondiente para el período
        md_path = html_path.with_suffix(".md")
        info = extraer_info_md(md_path) if md_path.exists() else {"periodo": "—"}

        is_latest = (i == 0)
        badge_class = " latest" if is_latest else ""
        badge_label = "ÚLTIMA EDICIÓN" if is_latest else f"Ed. {num:03d}"

        cards.append(CARD_TEMPLATE.format(
            filename=html_path.name,
            num=num,
            periodo=info["periodo"],
            fecha_archivo=fecha_archivo,
            badge_class=badge_class,
            badge_label=badge_label,
        ))

    index_html = HTML_INDEX.format(
        cards="\n".join(cards),
        fecha_update=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )

    index_path = CARPETA / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    print(f"[OK] index.html actualizado con {len(htmls)} edicion(es).")


if __name__ == "__main__":
    main()
