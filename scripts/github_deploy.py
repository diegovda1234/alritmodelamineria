"""
github_deploy.py — Sube el noticiero a GitHub Pages via API REST.
No requiere git instalado. Solo Python + requests.

Uso:
    python scripts/github_deploy.py

Requiere:
    pip install requests
    GITHUB_TOKEN, GITHUB_USER y GITHUB_REPO en scripts/config.txt
"""

import sys
import base64
import time
from pathlib import Path

CARPETA = Path(__file__).parent.parent          # Noticiero_Minero/
CONFIG  = Path(__file__).parent / "config.txt"

EXTENSIONES_INCLUIR = {".html", ".css", ".js", ".svg", ".png", ".jpg", ".py", ".md", ".yml"}
ARCHIVOS_EXCLUIR   = {"config.txt", "ultimo_log.txt", "actualizar_noticiero.bat", "netlify_deploy.py"}


# ── CARGAR CONFIG ─────────────────────────────────────────────────────────────
def cargar_config():
    if not CONFIG.exists():
        print(f"[ERROR] No se encontro el archivo de configuracion: {CONFIG}")
        sys.exit(1)

    cfg = {}
    for linea in CONFIG.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            clave, valor = linea.split("=", 1)
            cfg[clave.strip()] = valor.strip()

    token = cfg.get("GITHUB_TOKEN", "")
    user  = cfg.get("GITHUB_USER", "")
    repo  = cfg.get("GITHUB_REPO", "")

    if not token or not user or not repo:
        print("[ERROR] Faltan GITHUB_TOKEN, GITHUB_USER o GITHUB_REPO en scripts/config.txt")
        sys.exit(1)

    return token, user, repo


# ── OBTENER SHA ACTUAL DEL ARCHIVO EN GITHUB ──────────────────────────────────
def _request_con_reintento(fn, intentos=4, espera=3):
    """Ejecuta una llamada HTTP reintentando ante errores de conexion transitorios."""
    import requests
    ultimo_error = None
    for i in range(intentos):
        try:
            return fn()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as e:
            ultimo_error = e
            if i < intentos - 1:
                time.sleep(espera * (i + 1))
    raise ultimo_error


def obtener_sha(session, api_base: str, ruta_repo: str) -> str | None:
    """Retorna el SHA del archivo si ya existe en el repo, o None si no existe."""
    resp = _request_con_reintento(
        lambda: session.get(f"{api_base}/contents/{ruta_repo}", timeout=30)
    )
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


# ── SUBIR UN ARCHIVO ──────────────────────────────────────────────────────────
def subir_archivo(session, api_base: str, ruta_repo: str, contenido_bytes: bytes, mensaje: str):
    sha_actual = obtener_sha(session, api_base, ruta_repo)
    contenido_b64 = base64.b64encode(contenido_bytes).decode("utf-8")

    body = {
        "message": mensaje,
        "content": contenido_b64,
    }
    if sha_actual:
        body["sha"] = sha_actual  # requerido para actualizar un archivo existente

    resp = _request_con_reintento(
        lambda: session.put(f"{api_base}/contents/{ruta_repo}", json=body, timeout=30)
    )
    return resp.status_code in (200, 201), resp.status_code


# ── LISTAR ARCHIVOS A SUBIR ───────────────────────────────────────────────────
def listar_archivos() -> list[tuple[str, Path]]:
    """Retorna lista de (ruta_en_repo, Path_local)."""
    archivos = []
    for filepath in CARPETA.rglob("*"):
        if not filepath.is_file():
            continue
        if filepath.suffix not in EXTENSIONES_INCLUIR:
            continue
        partes = filepath.relative_to(CARPETA).parts
        # Excluir archivos sensibles o innecesarios
        if filepath.name in ARCHIVOS_EXCLUIR:
            continue
        # Excluir PDFs y archivos de respaldo
        if filepath.suffix in {".pdf", ".txt", ".bat", ".log"}:
            continue
        ruta_repo = "/".join(partes)
        archivos.append((ruta_repo, filepath))
    return archivos


# ── DEPLOY ────────────────────────────────────────────────────────────────────
def deploy(token: str, user: str, repo: str):
    try:
        import requests
    except ImportError:
        print("[ERROR] Falta la libreria 'requests'. Instala con:")
        print("        pip install requests")
        sys.exit(1)

    api_base = f"https://api.github.com/repos/{user}/{repo}"
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })

    archivos = listar_archivos()
    print(f"[1/2] Archivos encontrados: {len(archivos)}")

    print("[2/2] Subiendo a GitHub...")
    ok = 0
    for ruta_repo, filepath in archivos:
        contenido = filepath.read_bytes()
        try:
            exito, codigo = subir_archivo(
                session, api_base, ruta_repo, contenido,
                mensaje=f"deploy: {filepath.name}"
            )
            estado = "[OK]" if exito else f"[!] codigo {codigo}"
        except Exception as e:
            exito = False
            estado = f"[!] error conexion: {type(e).__name__}"
        print(f"      {estado} {ruta_repo}")
        if exito:
            ok += 1

    url = f"https://{user}.github.io/{repo}/"
    print()
    print("=" * 55)
    print(f"  Deploy completado: {ok}/{len(archivos)} archivos subidos")
    print(f"  URL: {url}")
    print("  (GitHub Pages puede tardar 1-2 minutos en publicar)")
    print("=" * 55)


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    token, user, repo = cargar_config()
    deploy(token, user, repo)
