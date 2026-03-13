"""
generar_noticiero.py — Genera el noticiero minero semanal usando la API de Anthropic.
Se ejecuta desde GitHub Actions cada martes automáticamente, o manualmente.

Uso:
    python scripts/generar_noticiero.py

Requiere:
    pip install anthropic markdown
    Variable de entorno: ANTHROPIC_API_KEY
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_next_edition_number() -> int:
    """Busca los .md existentes y retorna el siguiente número de edición."""
    existing = sorted(Path(".").glob("Noticiero_Minero_Ed*.md"), reverse=True)
    if not existing:
        return 1
    m = re.search(r"Ed(\d+)", existing[0].name)
    return (int(m.group(1)) + 1) if m else 1


def load_skill_content() -> str:
    skill_path = Path(__file__).parent / "skill_content.md"
    return skill_path.read_text(encoding="utf-8")


def generate_newsletter(edition_num: int, today_display: str) -> str:
    """Llama a la API de Anthropic para generar el noticiero completo."""
    try:
        import anthropic
    except ImportError:
        print("[ERROR] Falta la libreria anthropic. Instala con: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("[ERROR] Falta la variable de entorno ANTHROPIC_API_KEY")
        sys.exit(1)

    skill_content = load_skill_content()
    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = f"""Eres el analista de inteligencia minera estratégica personal de Diego Varleta.

{skill_content}"""

    user_message = (
        f"Hoy es {today_display}. "
        f"Genera la Edición N° {edition_num:03d} del Noticiero Minero completo "
        "siguiendo exactamente la estructura y pautas descritas. "
        "Usa web search extensivamente para buscar noticias de los últimos 7 días. "
        "Responde únicamente con el contenido del informe en Markdown, "
        "comenzando con el título principal del noticiero."
    )

    print("  Llamando a Claude con web search (3-5 minutos)...")
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=16000,
        system=system_prompt,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": user_message}],
    )

    # Extraer solo los bloques de texto (ignorar tool_use/tool_result)
    content = ""
    for block in response.content:
        if block.type == "text":
            content += block.text

    return content.strip()


def main():
    today = datetime.now()
    today_iso = today.strftime("%Y-%m-%d")
    today_display = today.strftime("%d de %B de %Y")

    edition_num = get_next_edition_number()
    print(f"[1/4] Iniciando Edición N° {edition_num:03d} — {today_iso}")

    # ── Paso 1: Generar markdown con Claude ──────────────────────────────────
    md_content = generate_newsletter(edition_num, today_display)

    if not md_content:
        print("[ERROR] La API no retornó contenido.")
        sys.exit(1)

    md_filename = f"Noticiero_Minero_Ed{edition_num:03d}_{today_iso}.md"
    Path(md_filename).write_text(md_content, encoding="utf-8")
    print(f"[OK] Markdown guardado: {md_filename}")

    # ── Paso 2: Convertir a HTML ─────────────────────────────────────────────
    print("[2/4] Convirtiendo a HTML...")
    result = subprocess.run(
        [sys.executable, "scripts/generar_pdf.py", md_filename],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr:
        print(f"[AVISO] {result.stderr[:300]}")

    html_filename = md_filename.replace(".md", ".html")
    if not Path(html_filename).exists():
        print(f"[ERROR] No se generó el HTML: {html_filename}")
        sys.exit(1)
    print(f"[OK] HTML generado: {html_filename}")

    # ── Paso 3: Actualizar index.html ────────────────────────────────────────
    print("[3/4] Actualizando index.html...")
    subprocess.run(
        [sys.executable, "scripts/actualizar_index.py"],
        capture_output=True, text=True
    )
    print("[OK] index.html actualizado.")

    print(f"\n[4/4] Edición {edition_num:03d} generada exitosamente.")
    print(f"      Archivos: {md_filename}, {html_filename}, index.html")


if __name__ == "__main__":
    main()
