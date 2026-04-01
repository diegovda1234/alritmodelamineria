"""
generar_pdf.py — Convierte el informe NoticiasMineras (Markdown) a PDF profesional.

Uso:
    python generar_pdf.py <archivo.md> [--output <archivo.pdf>]

Requiere (instalar una vez):
    pip install markdown weasyprint
    o
    pip install markdown pdfkit   (+ wkhtmltopdf instalado en el sistema)
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

# ── CSS BRAND ────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:wght@300;400;600&display=swap');

:root {
    /* Brand palette — Al Ritmo de la Minería */
    --night:      #0F1C2E;   /* Azul Noche — fondo oscuro principal */
    --slate:      #3B5070;   /* Azul Pizarra */
    --mid-blue:   #4B6280;   /* Azul Medio */
    --light-blue: #8FA3BC;   /* Azul Claro */
    --cold-white: #F7F9FC;   /* Blanco Frío */
    /* Acento minero */
    --copper:     #B87333;
    --gold:       #e2b96f;
    /* Tipografía */
    --text:       #1A2535;
    --muted:      #5B6E84;
    --rule:       #D1D8E0;
    /* Feedback */
    --green:      #2a7a3b;
    --red:        #b52b2b;
    /* Aliases */
    --dark:       var(--night);
    --bg:         var(--cold-white);
    --light:      #EEF2F7;
    --black:      #0A1220;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'DM Sans', 'Segoe UI', sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: var(--text);
    background: var(--cold-white);
    padding: 0;
}

/* ══════════════════════════════════════
   PORTADA — BRAND COVER
══════════════════════════════════════ */
.cover {
    background: var(--night);
    color: white;
    padding: 0;
    page-break-after: always;
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 360px;
    border-bottom: 3px solid var(--copper);
}

/* Franja superior con logo + nombre */
.cover-header {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 36px 52px 28px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.cover-logo {
    flex-shrink: 0;
    width: 80px;
    height: 80px;
}

.cover-logo svg {
    width: 80px;
    height: 80px;
    display: block;
}

.cover-logo svg path {
    fill: white !important;
}

.cover-brand {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.cover-brand-name {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 34pt;
    font-weight: 900;
    color: white;
    letter-spacing: -0.5px;
    line-height: 1.05;
}

.cover-brand-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 8pt;
    color: var(--light-blue);
    letter-spacing: 1.4px;
    text-transform: uppercase;
    font-weight: 300;
    margin-top: 4px;
}

/* Cuerpo de la portada */
.cover-body {
    padding: 28px 52px 36px;
    flex: 1;
}

.cover h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 13pt;
    font-weight: 400;
    font-style: italic;
    color: var(--light-blue);
    border: none;
    margin-bottom: 20px;
    letter-spacing: 0.2px;
    line-height: 1.4;
}

.cover-edition-badge {
    display: inline-block;
    background: var(--slate);
    border: none;
    color: var(--light-blue);
    font-family: 'DM Sans', sans-serif;
    font-size: 7pt;
    font-weight: 600;
    padding: 4px 14px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    border-radius: 2px;
    margin-bottom: 0;
}

.cover-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.12);
    margin: 20px 0;
}

.cover-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
}

.cover-meta-item {
    padding: 12px 18px 12px 0;
    border-right: 1px solid rgba(255,255,255,0.1);
}

.cover-meta-item:last-child { border-right: none; padding-right: 0; }
.cover-meta-item:not(:first-child) { padding-left: 18px; }

.cover-meta-item .label {
    font-family: 'DM Sans', sans-serif;
    font-size: 6.5pt;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    color: var(--light-blue);
    font-weight: 600;
    margin-bottom: 5px;
    opacity: 0.8;
}

.cover-meta-item .value {
    font-family: 'DM Sans', sans-serif;
    font-size: 9.5pt;
    color: rgba(255,255,255,0.85);
    font-weight: 300;
    line-height: 1.4;
}

.cover .tagline {
    display: none; /* replaced by cover-brand-sub */
}

/* ══════════════════════════════════════
   RESUMEN EJECUTIVO
══════════════════════════════════════ */
.executive-summary {
    background: white;
    border-top: 3px solid var(--night);
    border-bottom: 1px solid var(--rule);
    padding: 32px 52px 36px;
    margin: 0;
    page-break-after: always;
}
.executive-summary h2 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 15pt;
    font-weight: 700;
    color: var(--night);
    border: none;
    background: none;
    padding: 0;
    margin: 0 0 20px 0;
    letter-spacing: -0.2px;
    text-transform: none;
}
.es-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 18px;
}
.es-card {
    background: var(--cold-white);
    border: 1px solid var(--rule);
    border-left: 3px solid var(--slate);
    padding: 12px 14px;
}
.es-card .es-mineral {
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted);
    font-weight: 600;
    margin-bottom: 4px;
}
.es-card .es-highlight {
    font-size: 10pt;
    color: var(--text);
    line-height: 1.5;
}
.es-footer-note {
    font-size: 8.5pt;
    color: var(--muted);
    border-top: 1px solid var(--rule);
    padding-top: 10px;
    margin-top: 6px;
}
.page-info {
    float: right;
    font-size: 8pt;
    color: var(--muted);
    font-style: italic;
}

/* ══════════════════════════════════════
   CONTENIDO PRINCIPAL
══════════════════════════════════════ */
.content { padding: 36px 52px 52px; }

h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 18pt;
    font-weight: 700;
    color: var(--night);
    border-bottom: 2px solid var(--night);
    padding-bottom: 8px;
    margin: 36px 0 16px;
}
h2 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 11.5pt;
    font-weight: 700;
    color: white;
    background: var(--night);
    border: none;
    padding: 11px 52px;
    margin: 40px -52px 18px;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}
h3 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 12pt;
    font-weight: 700;
    color: var(--night);
    background: var(--light);
    border-left: 4px solid var(--slate);
    padding: 9px 52px 9px 48px;
    margin: 30px -52px 14px;
    letter-spacing: 0.1px;
    text-transform: none;
}
h4 {
    font-family: 'DM Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: var(--night);
    border-left: 3px solid var(--copper);
    padding: 6px 0 6px 12px;
    margin: 20px 0 6px;
    letter-spacing: 0.1px;
    background: none;
}

p { margin-bottom: 10px; }

/* ── TABLAS ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 22px;
    font-size: 9.5pt;
    font-family: 'DM Sans', sans-serif;
}
thead tr { background: var(--night); color: white; }
thead th {
    padding: 9px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 7.5pt;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
tbody tr:nth-child(even) { background: var(--light); }
tbody tr { border-bottom: 1px solid var(--rule); }
tbody td {
    padding: 8px 12px;
    vertical-align: top;
}
tbody td:first-child { font-weight: 500; color: var(--night); }

/* ── BLOCKQUOTES ── */
blockquote {
    background: var(--light);
    border-left: 3px solid var(--slate);
    margin: 16px 0;
    padding: 10px 18px;
    font-size: 10.5pt;
    font-style: italic;
    color: var(--slate);
}
blockquote p { margin: 0; }

/* ── CÓDIGO ── */
code {
    background: var(--light);
    border: 1px solid var(--rule);
    padding: 1px 4px;
    font-size: 9pt;
    font-family: 'Cascadia Code', 'Consolas', monospace;
}
pre {
    background: var(--black);
    color: #eee;
    padding: 12px 16px;
    overflow-x: auto;
    margin: 10px 0;
    font-size: 8.5pt;
}
pre code { background: none; border: none; color: inherit; padding: 0; }

/* ── LISTAS ── */
ul, ol { margin: 7px 0 10px 20px; padding-left: 4px; }
li { margin-bottom: 4px; }
li > ul, li > ol { margin-top: 4px; }

/* ── SEPARADORES ── */
hr { border: none; border-top: 1px solid var(--rule); margin: 22px 0; }

/* ── TIPOGRAFÍA ── */
strong { color: var(--black); font-weight: 600; }
em { color: var(--mid-blue); font-style: italic; }

/* ── IMÁGENES ── */
img { max-width: 100%; height: auto; display: block; margin: 12px auto; }

/* ══════════════════════════════════════
   CONFIGURACIÓN DE PÁGINA
══════════════════════════════════════ */
@page {
    size: A4;
    margin: 20mm 18mm 24mm 18mm;
    @bottom-left {
        content: "AL RITMO DE LA MINERIA";
        font-size: 7pt;
        color: #aaa;
        font-family: 'Source Sans 3', sans-serif;
    }
}

@page :first {
    margin: 0;
    @bottom-left { content: none; }
    @bottom-right { content: none; }
    @top-right { content: none; }
}

/* ── SALTO DE PAGINA ── */
h2 { page-break-after: avoid; }
h3 { page-break-after: avoid; }
table { page-break-inside: avoid; }
blockquote { page-break-inside: avoid; }
.executive-summary { page-break-inside: avoid; }

/* ══════════════════════════════════════
   RESPONSIVE MOVIL
══════════════════════════════════════ */
@media screen and (max-width: 700px) {
    body { font-size: 13pt; }

    .cover-header {
        padding: 24px 20px 20px;
        gap: 14px;
    }
    .cover-logo { width: 60px; height: 60px; }
    .cover-logo svg { width: 60px; height: 60px; }
    .cover-brand-name { font-size: 17pt; }
    .cover-body { padding: 20px 20px 28px; }

    .cover-meta { grid-template-columns: 1fr; }
    .cover-meta-item {
        border-right: none;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding: 10px 0;
    }
    .cover-meta-item:not(:first-child) { padding-left: 0; }

    .executive-summary { padding: 22px 18px 26px; }
    .es-grid { grid-template-columns: 1fr; }

    .content { padding: 20px 18px 32px; }

    table {
        font-size: 10pt;
        display: block;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    h1 { font-size: 16pt; }
    h2 { font-size: 13pt; padding: 11px 18px; margin: 32px -18px 14px; }
    h3 { font-size: 13pt; padding: 9px 18px 9px 14px; margin: 26px -18px 12px; }
    h4 { font-size: 12pt; }
}

/* ══════════════════════════════════════
   BARRA DE NAVEGACIÓN RÁPIDA (solo pantalla)
══════════════════════════════════════ */
@media print {
    .quick-nav, .nav-dropdown { display: none !important; }
    body { padding-top: 0 !important; }
}

@media screen {
    body { padding-top: 50px; }
}

.quick-nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    height: 50px;
    background: rgba(15, 28, 46, 0.97);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 0 14px;
    display: flex;
    flex-wrap: nowrap;
    gap: 10px;
    align-items: center;
    box-shadow: 0 2px 14px rgba(0,0,0,0.4);
    font-family: 'DM Sans', 'Segoe UI', sans-serif;
    border-bottom: 1px solid rgba(143,163,188,0.2);
}

.nav-brand {
    color: var(--gold);
    font-size: 8.5pt;
    font-weight: 700;
    white-space: nowrap;
    letter-spacing: 0.3px;
    flex-shrink: 0;
}

.nav-search-wrap {
    display: flex;
    align-items: center;
    gap: 4px;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 5px 12px;
    flex: 1;
    max-width: 380px;
}

.nav-search-wrap input {
    background: none;
    border: none;
    outline: none;
    color: white;
    font-size: 10pt;
    width: 100%;
    min-width: 60px;
    font-family: inherit;
}

.nav-search-wrap input::placeholder { color: rgba(255,255,255,0.4); }

.nav-search-wrap .search-count {
    font-size: 8pt;
    color: var(--gold);
    white-space: nowrap;
    min-width: 36px;
    text-align: center;
}

.nav-search-wrap button {
    background: none;
    border: none;
    color: rgba(255,255,255,0.55);
    cursor: pointer;
    font-size: 12pt;
    padding: 0 3px;
    line-height: 1;
    transition: color 0.15s;
}

.nav-search-wrap button:hover { color: white; }

/* Botón hamburger */
.nav-hamburger {
    margin-left: auto;
    flex-shrink: 0;
    background: none;
    border: 2px solid rgba(226,185,111,0.45);
    border-radius: 8px;
    color: var(--gold);
    font-size: 18pt;
    line-height: 1;
    cursor: pointer;
    padding: 1px 10px 3px;
    transition: background 0.15s, border-color 0.15s;
    -webkit-tap-highlight-color: transparent;
}

.nav-hamburger:hover,
.nav-hamburger.active {
    background: rgba(226,185,111,0.15);
    border-color: var(--gold);
}

/* Dropdown de secciones */
.nav-dropdown {
    position: fixed;
    top: 50px;
    left: 0; right: 0;
    z-index: 9998;
    background: rgba(16, 24, 52, 0.98);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.55);
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.28s cubic-bezier(0.4,0,0.2,1);
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

.nav-dropdown.open {
    max-height: 80vh;
    overflow-y: auto;
}

.nav-dropdown-inner {
    padding: 14px 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.nav-group {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.nav-h2-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: rgba(255,255,255,0.92);
    text-decoration: none;
    font-size: 10pt;
    font-weight: 600;
    padding: 12px 16px;
    border-radius: 7px;
    background: rgba(255,255,255,0.08);
    border-left: 3px solid var(--copper);
    transition: background 0.15s, color 0.15s;
    line-height: 1.3;
    -webkit-tap-highlight-color: transparent;
    letter-spacing: 0.2px;
}

.nav-h2-link:hover,
.nav-h2-link:active {
    background: rgba(184,115,51,0.25);
    color: white;
}

.nav-arrow {
    font-size: 8pt;
    opacity: 0.6;
    transition: transform 0.2s;
    flex-shrink: 0;
    margin-left: 6px;
}

.nav-sub-group {
    display: none;
    flex-direction: column;
    gap: 2px;
    padding: 4px 0 6px 12px;
}

.nav-sub-group.open {
    display: flex;
}

.nav-sub-link {
    display: block;
    color: rgba(255,255,255,0.72);
    text-decoration: none;
    font-size: 9.5pt;
    font-weight: 400;
    padding: 9px 14px;
    border-radius: 6px;
    background: rgba(255,255,255,0.04);
    border-left: 2px solid rgba(184,115,51,0.4);
    transition: background 0.12s, color 0.12s;
    line-height: 1.3;
    -webkit-tap-highlight-color: transparent;
}

.nav-sub-link:hover,
.nav-sub-link:active {
    background: rgba(184,115,51,0.18);
    color: white;
    border-color: var(--copper);
}

/* Resultados de búsqueda */
mark.search-hl {
    background: rgba(226, 185, 111, 0.45);
    color: inherit;
    border-radius: 2px;
    padding: 0 1px;
}

mark.search-hl.current {
    background: var(--gold);
    color: var(--dark);
    font-weight: 600;
}

@media screen and (max-width: 700px) {
    .nav-brand { display: none; }
    .nav-search-wrap { max-width: none; }
    .nav-dropdown-inner { grid-template-columns: 1fr; }
    .nav-h2-link { font-size: 12pt; padding: 14px 16px; }
    .nav-sub-link { font-size: 11pt; padding: 11px 14px; }
}
"""

# ── TEMPLATE HTML ────────────────────────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>

<!-- PORTADA -->
<div class="cover">
    <div class="cover-header">
        <div class="cover-logo">__LOGO_SVG__</div>
        <div class="cover-brand">
            <span class="cover-brand-name">Al Ritmo de la Minería</span>
            <span class="cover-brand-sub">Generado por Diego Varleta</span>
        </div>
    </div>
    <div class="cover-body">
        <div class="cover-edition-badge">Edición N° {numero_edicion}</div>
        <hr class="cover-divider">
        <div class="cover-meta">
            <div class="cover-meta-item">
                <div class="label">Período cubierto</div>
                <div class="value">{edicion}</div>
            </div>
            <div class="cover-meta-item">
                <div class="label">Fecha de publicación</div>
                <div class="value">{fecha_publicacion}</div>
            </div>
            <div class="cover-meta-item">
                <div class="label">Énfasis editorial</div>
                <div class="value">{enfasis}</div>
            </div>
        </div>
    </div>
</div>

<!-- RESUMEN EJECUTIVO -->
<div class="executive-summary">
    <h2>Resumen Ejecutivo</h2>
    {resumen_ejecutivo_html}
    <p class="es-footer-note">
        Este informe contiene {n_noticias} noticias analizadas, precios spot actualizados para {n_minerales} minerales y {n_conceptos} concepto(s) educativo(s) de la semana.
        Fuentes verificadas al {fecha_publicacion}.
    </p>
</div>

<!-- CONTENIDO PRINCIPAL -->
<div class="content">
    {body}
</div>

</body>
</html>
"""


# ── JAVASCRIPT DE NAVEGACIÓN Y BÚSQUEDA ──────────────────────────────────────
NAV_JS = r"""
(function () {
    var highlights = [];
    var currentIdx = -1;

    function clearHighlights() {
        highlights.forEach(function (el) {
            var parent = el.parentNode;
            if (parent) {
                parent.replaceChild(document.createTextNode(el.textContent), el);
                parent.normalize();
            }
        });
        highlights = [];
        currentIdx = -1;
        updateCount();
    }

    function updateCount() {
        var counter = document.getElementById('search-count');
        if (!counter) return;
        counter.textContent = highlights.length > 0 ? (currentIdx + 1) + '/' + highlights.length : '';
    }

    function walkTextNodes(node, term, termLower, found) {
        if (node.nodeType === 3) {
            var text = node.textContent;
            var idx = text.toLowerCase().indexOf(termLower);
            if (idx !== -1) {
                var before = document.createTextNode(text.slice(0, idx));
                var mark = document.createElement('mark');
                mark.className = 'search-hl';
                mark.textContent = text.slice(idx, idx + term.length);
                var after = document.createTextNode(text.slice(idx + term.length));
                var parent = node.parentNode;
                parent.insertBefore(before, node);
                parent.insertBefore(mark, node);
                parent.insertBefore(after, node);
                parent.removeChild(node);
                found.push(mark);
                if (after.textContent.toLowerCase().indexOf(termLower) !== -1) {
                    walkTextNodes(after, term, termLower, found);
                }
            }
        } else if (node.nodeType === 1 &&
                   node.nodeName !== 'MARK' &&
                   node.nodeName !== 'SCRIPT' &&
                   node.nodeName !== 'STYLE' &&
                   node.nodeName !== 'NAV') {
            Array.prototype.slice.call(node.childNodes).forEach(function (child) {
                walkTextNodes(child, term, termLower, found);
            });
        }
    }

    function highlightAll(term) {
        clearHighlights();
        if (!term || term.length < 2) return;
        var content = document.querySelector('.content');
        if (!content) return;
        var termLower = term.toLowerCase();
        walkTextNodes(content, term, termLower, highlights);
        if (highlights.length > 0) {
            currentIdx = 0;
            highlights[0].classList.add('current');
            highlights[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        updateCount();
    }

    function goNext() {
        if (!highlights.length) return;
        highlights[currentIdx].classList.remove('current');
        currentIdx = (currentIdx + 1) % highlights.length;
        highlights[currentIdx].classList.add('current');
        highlights[currentIdx].scrollIntoView({ behavior: 'smooth', block: 'center' });
        updateCount();
    }

    function goPrev() {
        if (!highlights.length) return;
        highlights[currentIdx].classList.remove('current');
        currentIdx = (currentIdx - 1 + highlights.length) % highlights.length;
        highlights[currentIdx].classList.add('current');
        highlights[currentIdx].scrollIntoView({ behavior: 'smooth', block: 'center' });
        updateCount();
    }

    var input = document.getElementById('search-input');
    if (input) {
        input.addEventListener('input', function () { highlightAll(this.value.trim()); });
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') { e.preventDefault(); if (e.shiftKey) goPrev(); else goNext(); }
            else if (e.key === 'Escape') { this.value = ''; clearHighlights(); }
        });
    }
    var btnNext = document.getElementById('btn-next');
    var btnPrev = document.getElementById('btn-prev');
    var btnClear = document.getElementById('btn-clear');
    if (btnNext) btnNext.addEventListener('click', goNext);
    if (btnPrev) btnPrev.addEventListener('click', goPrev);
    if (btnClear) btnClear.addEventListener('click', function () {
        if (input) input.value = '';
        clearHighlights();
    });

    /* Ctrl+F / Cmd+F → foco en buscador propio */
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            if (input) { e.preventDefault(); input.focus(); input.select(); }
        }
    });

    /* ── Hamburger menu ── */
    var hamburger = document.getElementById('nav-hamburger');
    var dropdown  = document.getElementById('nav-dropdown');

    function closeNavMenu() {
        if (!dropdown) return;
        dropdown.classList.remove('open');
        dropdown.setAttribute('aria-hidden', 'true');
        if (hamburger) {
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    }

    /* Expandir/colapsar sub-secciones */
    window.toggleSub = function(subId) {
        var sub = document.getElementById(subId);
        if (!sub) return;
        var arrow = sub.previousElementSibling ? sub.previousElementSibling.querySelector('.nav-arrow') : null;
        if (sub.classList.contains('open')) {
            sub.classList.remove('open');
            if (arrow) arrow.style.transform = '';
        } else {
            sub.classList.add('open');
            if (arrow) arrow.style.transform = 'rotate(180deg)';
        }
    };

    if (hamburger && dropdown) {
        hamburger.addEventListener('click', function (e) {
            e.stopPropagation();
            var isOpen = dropdown.classList.contains('open');
            if (isOpen) {
                closeNavMenu();
            } else {
                dropdown.classList.add('open');
                dropdown.setAttribute('aria-hidden', 'false');
                hamburger.classList.add('active');
                hamburger.setAttribute('aria-expanded', 'true');
            }
        });

        /* Cerrar al hacer clic fuera */
        document.addEventListener('click', function (e) {
            if (!dropdown.contains(e.target) && e.target !== hamburger) {
                closeNavMenu();
            }
        });

        /* Cerrar con Escape */
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeNavMenu();
        });
    }
})();
"""


# ── EXTRACCIÓN DE METADATOS DEL MARKDOWN ─────────────────────────────────────
def extraer_metadatos(md_text: str) -> dict:
    """Extrae metadatos del encabezado del informe."""
    meta = {
        "edicion": "—",
        "enfasis": "—",
        "numero_edicion": "1",
        "resumen_ejecutivo": "",
        "n_noticias": "—",
        "n_minerales": "7",
        "n_conceptos": "1",
    }

    lines = md_text.split("\n")
    for line in lines[:15]:
        if "**Periodo:**" in line or "**Período:**" in line:
            meta["edicion"] = line.replace("**Periodo:**", "").replace("**Período:**", "").strip()
        elif "**Edicion:**" in line or "**Edición:**" in line:
            meta["edicion"] = line.replace("**Edicion:**", "").replace("**Edición:**", "").strip()
        if "**Enfasis editorial" in line or "**Énfasis editorial" in line:
            partes = line.split(":**")
            if len(partes) > 1:
                meta["enfasis"] = partes[1].strip()
        if "**Edicion N" in line or "**Edición N" in line or "**N° Edicion:**" in line or "**N° Edición:**" in line or "**Numero de edicion:**" in line:
            nums = re.findall(r'\d+', line)
            if nums:
                meta["numero_edicion"] = nums[0]

    # Extraer bloque de Resumen Ejecutivo si existe en el markdown
    re_match = re.search(
        r'##\s*[📋🗒️]?\s*RESUMEN EJECUTIVO\s*\n(.*?)(?=\n## |\Z)',
        md_text, re.DOTALL | re.IGNORECASE
    )
    if re_match:
        meta["resumen_ejecutivo"] = re_match.group(1).strip()

    # Contar noticias aproximadas (bloques H3 en el cuerpo)
    noticias = len(re.findall(r'^###\s+', md_text, re.MULTILINE))
    meta["n_noticias"] = str(max(noticias - 2, 1))  # descontar secciones no-noticia

    return meta


def md_to_html_body(md_text: str) -> str:
    """Convierte markdown a HTML, excluyendo el bloque de Resumen Ejecutivo (va en portada)."""
    import markdown as md_lib

    # Quitar H1 del cuerpo (ya se muestra en la portada como marca)
    md_limpio = re.sub(r'^#\s+[^\n]+\n?', '', md_text, flags=re.MULTILINE, count=1)

    # Quitar líneas de metadata que ya aparecen en la portada
    md_limpio = re.sub(
        r'^\*\*(Edici[oó]n\s*N[°º]?|Per[ií]odo|Fecha\s+de\s+publicaci[oó]n|[ÉE]nfasis\s+editorial[^\*]*):\*\*[^\n]*\n?',
        '', md_limpio, flags=re.MULTILINE | re.IGNORECASE
    )
    # Quitar el separador --- que queda suelto tras eliminar el bloque de metadata
    md_limpio = re.sub(r'^\s*---\s*\n', '', md_limpio, count=1, flags=re.MULTILINE)

    # Quitar bloque de Resumen Ejecutivo del cuerpo (ya va en la hoja de resumen)
    md_limpio = re.sub(
        r'##\s*[📋🗒️]?\s*RESUMEN EJECUTIVO\s*\n.*?(?=\n## |\Z)',
        '', md_limpio, flags=re.DOTALL | re.IGNORECASE
    )

    extensions = ["tables", "fenced_code", "attr_list", "nl2br"]
    return md_lib.markdown(md_limpio, extensions=extensions)


def _slugify(text: str, counter: list) -> str:
    """Genera un slug URL-safe a partir de texto."""
    ascii_part = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    slug = re.sub(r'\s+', '-', ascii_part.strip()).lower()[:48]
    slug = re.sub(r'[^a-z0-9-]', '', slug) or f"sec-{counter[0]}"
    counter[0] += 1
    return slug


def add_section_ids(html_body: str):
    """Add id attributes to H2, H3, H4 headings.
    Returns (modified_html, sections, h4_sections)
      sections    — H2/H3 dicts for nav: {'id', 'label', 'level'}
      h4_sections — H4 dicts for summary linking: {'id', 'label'}
    """
    sections = []
    h4_sections = []
    counter = [0]

    def replace_heading(m):
        tag = m.group(1)   # '2', '3' or '4'
        inner = m.group(2)
        label = re.sub(r'<[^>]+>', '', inner).strip()
        slug = _slugify(label, counter)
        level = int(tag)
        clean_inner = _strip_emoji(inner)
        clean_label = _strip_emoji(label)
        if level in (2, 3):
            display = clean_label[:50] + ('...' if len(clean_label) > 50 else '')
            sections.append({'id': slug, 'label': display, 'level': level})
        elif level == 4:
            h4_sections.append({'id': slug, 'label': clean_label})
        return f'<h{tag} id="{slug}">{clean_inner}</h{tag}>'

    modified = re.sub(r'<h([234])>(.*?)</h\1>', replace_heading, html_body, flags=re.DOTALL)
    return modified, sections, h4_sections


def _word_overlap(text_a: str, text_b: str) -> float:
    """Jaccard-style word overlap ignoring common stopwords."""
    stop = {'de','la','el','los','las','en','y','a','que','un','una','su','sus',
            'por','para','con','del','al','se','es','no','o','e','como','más',
            'pero','si','lo','le','les','nos','sobre','ante','entre','hasta'}
    def words(t):
        return set(w.lower() for w in re.findall(r'\b\w{3,}\b', t) if w.lower() not in stop)
    wa, wb = words(text_a), words(text_b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))


def link_summary_to_articles(resumen_html: str, h4_sections: list) -> str:
    """Link only the [TAG] badge in each summary <li> to the best-matching H4."""
    if not h4_sections:
        return resumen_html

    def replace_li(m):
        li_inner = m.group(1)
        li_text = re.sub(r'<[^>]+>', '', li_inner)
        best_id, best_score = None, 0.28
        for sec in h4_sections:
            score = _word_overlap(li_text, sec['label'])
            if score > best_score:
                best_score, best_id = score, sec['id']
        if best_id:
            # Wrap only the first <strong>[TAG]</strong> badge, not the whole bullet
            linked = re.sub(
                r'(<strong>)(\[[^\]]+\])(</strong>)',
                rf'\1<a href="#{best_id}" style="color:var(--copper);text-decoration:none;'
                rf'font-weight:700;cursor:pointer">\2</a>\3',
                li_inner, count=1
            )
            return f'<li>{linked}</li>'
        return m.group(0)

    return re.sub(r'<li>(.*?)</li>', replace_li, resumen_html, flags=re.DOTALL)


def build_nav_html(sections: list) -> str:
    """Build sticky nav bar with hamburger dropdown.
    H2 sections are collapsible groups; H3 items nest inside them.
    """
    # Build grouped structure
    groups_html = []
    current_group_items = []
    current_h2 = None

    def flush_group():
        if current_h2 is None:
            return
        h2_id, h2_label = current_h2
        subs_html = ""
        if current_group_items:
            sub_links = "\n".join(
                f'            <a href="#{sid}" class="nav-sub-link" onclick="closeNavMenu()">{lbl}</a>'
                for sid, lbl in current_group_items
            )
            subs_html = f'\n        <div class="nav-sub-group" id="sub-{h2_id}">\n{sub_links}\n        </div>'
        toggle = ' onclick="toggleSub(\'sub-{h2_id}\')"'.format(h2_id=h2_id) if current_group_items else ' onclick="closeNavMenu()"'
        arrow = ' <span class="nav-arrow">&#9660;</span>' if current_group_items else ''
        href = f'href="#{h2_id}"' if not current_group_items else 'href="#"'
        groups_html.append(
            f'        <div class="nav-group">\n'
            f'            <a {href} class="nav-h2-link"{toggle}>{h2_label}{arrow}</a>'
            f'{subs_html}\n'
            f'        </div>'
        )

    for sec in sections:
        if sec['level'] == 2:
            flush_group()
            current_h2 = (sec['id'], sec['label'])
            current_group_items = []
        elif sec['level'] == 3 and current_h2:
            current_group_items.append((sec['id'], sec['label']))

    flush_group()

    dropdown_content = "\n".join(groups_html)

    return f"""<nav class="quick-nav" id="quick-nav" aria-label="Navegacion del informe">
    <span class="nav-brand">AL RITMO DE LA MINERÍA</span>
    <div class="nav-search-wrap">
        <input type="text" id="search-input" placeholder="Buscar en el informe..." aria-label="Buscar en el informe">
        <span class="search-count" id="search-count"></span>
        <button id="btn-prev" title="Anterior" aria-label="Resultado anterior">&#9650;</button>
        <button id="btn-next" title="Siguiente" aria-label="Resultado siguiente">&#9660;</button>
        <button id="btn-clear" title="Limpiar" aria-label="Limpiar">&#10005;</button>
    </div>
    <button class="nav-hamburger" id="nav-hamburger" title="Ver secciones" aria-label="Menu de secciones" aria-expanded="false">&#9776;</button>
</nav>
<div class="nav-dropdown" id="nav-dropdown" aria-hidden="true">
    <div class="nav-dropdown-inner">
{dropdown_content}
    </div>
</div>"""


def construir_resumen_html(md_resumen: str) -> str:
    """Construye el HTML del resumen ejecutivo."""
    import markdown as md_lib

    if md_resumen:
        return md_lib.markdown(md_resumen, extensions=["nl2br"])

    # Fallback si no hay sección de resumen en el markdown
    return """
    <p><em>El resumen ejecutivo se incluye automáticamente cuando el informe
    contiene una sección <code>## RESUMEN EJECUTIVO</code>.</em></p>
    """


def _load_svg_logo() -> str:
    """Carga el SVG del logo desde la carpeta del skill. Retorna string SVG limpio."""
    logo_path = Path(__file__).parent.parent / "logo.svg"
    if not logo_path.exists():
        return ""
    try:
        content = logo_path.read_text(encoding="utf-8")
        # Quitar declaración XML (solo conservar el elemento <svg>...)
        content = re.sub(r'<\?xml[^>]+\?>\s*', '', content).strip()
        # Quitar el path de fondo blanco/casi-blanco que tapa el logo sobre fondos oscuros
        content = re.sub(r'<path[^>]*fill="#(?:FDFDFD|FEFEFE|FFFFFF|F[Ee][Ff][Ee][Ff][Ee])"[^>]*/>', '', content, flags=re.IGNORECASE)
        # Añadir viewBox si no existe (necesario para que el SVG escale con CSS)
        def inject_viewbox(m):
            tag = m.group(0)
            if 'viewBox' not in tag:
                w = re.search(r'width="(\d+)"', tag)
                h = re.search(r'height="(\d+)"', tag)
                if w and h:
                    tag = tag.rstrip('>') + f' viewBox="0 0 {w.group(1)} {h.group(1)}">'
            return tag
        content = re.sub(r'<svg[^>]+>', inject_viewbox, content)
        return content
    except Exception:
        return ""


def _strip_gmlc_footer(md_text: str) -> str:
    """Remove GMLC/job-title footer lines and replace reader references to Diego → el lector."""
    md_text = re.sub(
        r'\*[^\n]*(?:GMLC|Gerente\s+Finanzas|Control\s+de\s+Gesti[oó]n)[^\n]*\*\n?',
        '', md_text, flags=re.IGNORECASE
    )
    # Reemplazar todas las referencias a Diego como lector (excepto "Diego Varleta")
    md_text = re.sub(r'\bDiego\b(?!\s+Varleta)', 'el lector', md_text)
    return md_text


def _strip_emoji(text: str) -> str:
    """Remove emoji and special symbol characters from text."""
    return re.sub(
        r'[\U00010000-\U0010ffff'
        r'\U0001F300-\U0001F9FF'
        r'\u2600-\u27BF'
        r'\u2300-\u23FF'
        r'\u25A0-\u25FF'
        r'\u2700-\u27BF'
        r']',
        '', text, flags=re.UNICODE
    ).strip()


def build_html(md_text: str) -> str:
    md_text = _strip_gmlc_footer(md_text)
    meta = extraer_metadatos(md_text)
    raw_body = md_to_html_body(md_text)
    html_body, sections, h4_sections = add_section_ids(raw_body)
    resumen_html = construir_resumen_html(meta.get("resumen_ejecutivo", ""))
    resumen_html = link_summary_to_articles(resumen_html, h4_sections)
    nav_html = build_nav_html(sections)
    logo_svg = _load_svg_logo()

    fecha_pub = datetime.now().strftime("%d de %B de %Y, %H:%M hrs")
    title = f"Al Ritmo de la Minería — Edición {meta['numero_edicion']} — {meta['edicion']}"

    html = HTML_TEMPLATE.format(
        title=title,
        css=CSS,
        edicion=meta["edicion"],
        enfasis=meta["enfasis"],
        numero_edicion=meta["numero_edicion"],
        fecha_publicacion=fecha_pub,
        resumen_ejecutivo_html=resumen_html,
        n_noticias=meta["n_noticias"],
        n_minerales=meta["n_minerales"],
        n_conceptos=meta["n_conceptos"],
        body=html_body,
    )

    # Inject logo AFTER format() to avoid SVG braces conflicting with str.format()
    html = html.replace('__LOGO_SVG__', logo_svg)

    # Inject nav before first content block and JS before </body>
    html = html.replace(
        '<body>\n\n<!-- PORTADA -->',
        f'<body>\n{nav_html}\n\n<!-- PORTADA -->'
    )
    html = html.replace(
        '</body>\n</html>',
        f'<script>\n{NAV_JS}\n</script>\n</body>\n</html>'
    )
    return html


def convert_to_pdf(html_content: str, output_path: str) -> bool:
    """Intenta convertir HTML a PDF. Retorna True si lo logra."""

    # Intento 1: weasyprint
    try:
        from weasyprint import HTML
        HTML(string=html_content, base_url=None).write_pdf(output_path)
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"[weasyprint] Error: {e}", file=sys.stderr)

    # Intento 2: pdfkit
    try:
        import pdfkit
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '18mm',
            'margin-bottom': '24mm',
            'margin-left': '18mm',
            'encoding': 'UTF-8',
            'enable-local-file-access': None,
        }
        pdfkit.from_string(html_content, output_path, options=options)
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"[pdfkit] Error: {e}", file=sys.stderr)

    return False


def main():
    # Forzar UTF-8 en stdout (evita errores de encoding en terminales Windows cp1252)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Genera PDF del Noticiero Minero")
    parser.add_argument("input", help="Archivo Markdown (.md) de entrada")
    parser.add_argument("--output", "-o", help="Archivo PDF de salida")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: No se encontro '{input_path}'", file=sys.stderr)
        sys.exit(1)

    # Nombre del PDF: mismo que el .md pero con _YYYY-MM-DD.pdf
    fecha_str = datetime.now().strftime("%Y-%m-%d")
    nombre_base = input_path.stem
    output_path = args.output or str(input_path.parent / f"{nombre_base}_{fecha_str}.pdf")
    html_output = str(input_path.with_suffix(".html"))

    print(f"[OK] Procesando: {input_path.name}")
    md_text = input_path.read_text(encoding="utf-8")
    html_content = build_html(md_text)

    # HTML siempre se guarda
    Path(html_output).write_text(html_content, encoding="utf-8")
    print(f"[OK] HTML intermedio: {html_output}")

    # PDF
    if convert_to_pdf(html_content, output_path):
        size_kb = Path(output_path).stat().st_size // 1024
        print(f"[OK] PDF generado: {output_path}  ({size_kb} KB)")
    else:
        print("\n[!] Libreria PDF no encontrada. Para activar:")
        print("    pip install weasyprint        <- Recomendado")
        print("    pip install pdfkit            <- Alternativa (necesita wkhtmltopdf)")
        print(f"\n    HTML disponible en: {html_output}")
        print("    Abre en Chrome/Edge -> Ctrl+P -> Guardar como PDF (A4)")


if __name__ == "__main__":
    main()
