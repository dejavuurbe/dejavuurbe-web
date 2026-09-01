from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if old not in text:
        print(f'No encontrado en {path}: {old[:70]}')
        return False
    p.write_text(text.replace(old, new), encoding='utf-8')
    print(f'Actualizado: {path}')
    return True

# 1) Recuperar el hover aprobado antes del último cambio accidental.
replace(
    'assets/css/desktop-tuning.css',
    '''  .catalog-visual .track-card:hover,\n  .catalog-visual .track-card:focus-visible{\n    transform:translateY(-5px) scale(1.05);\n    box-shadow:0 0 0 3px #ff6a32,0 18px 38px rgba(0,0,0,.54),0 0 22px rgba(255,90,31,.16);\n    filter:brightness(1.07) saturate(1.04);\n    z-index:30;\n  }\n  .catalog-visual:has(.track-card:hover) .track-card:not(:hover){\n    transform:scale(.99);\n    filter:brightness(.9);\n    opacity:.95;\n  }''',
    '''  .catalog-visual .track-card:hover,\n  .catalog-visual .track-card:focus-visible{\n    transform:translateY(-9px) scale(1.10);\n    box-shadow:0 0 0 3px #ff6a32,0 24px 50px rgba(0,0,0,.62),0 0 30px rgba(255,90,31,.20);\n    filter:brightness(1.10) saturate(1.06);\n    z-index:30;\n  }\n  .catalog-visual:has(.track-card:hover) .track-card:not(:hover){\n    transform:scale(.985);\n    filter:brightness(.86);\n    opacity:.93;\n  }'''
)

# 2) Quitar de Música una nota que explicaba decisiones internas del sitio.
replace(
    'musica/index.html',
    '<div class="section-note"><p>Los identificadores oficiales, fechas y fuentes externas siguen disponibles dentro de cada canción, sin interrumpir la experiencia principal de escucha y descubrimiento.</p></div>',
    ''
)

# 3) Quitar la nota técnica visible de todas las páginas individuales.
technical = '<p class="technical-note">Los identificadores y enlaces de referencia se mantienen disponibles para documentación, buscadores e información musical.</p>'
for page in sorted((ROOT / 'musica').glob('*/index.html')):
    text = page.read_text(encoding='utf-8')
    if technical in text:
        page.write_text(text.replace(technical, ''), encoding='utf-8')
        print(f'Nota técnica retirada: {page.relative_to(ROOT)}')

# 4) Videos: cambiar texto de planificación interna por lenguaje para visitantes.
replace(
    'videos/index.html',
    'La mejor forma de recorrer el material audiovisual es por tipo de contenido: canciones, piezas breves y registros de escenario.',
    'Videos, shorts y registros de escenario reunidos en el canal oficial de DejavuUrbe.'
)
replace(
    'videos/index.html',
    '<div class="video-current"><div class="eyebrow">Ahora</div><h2>El próximo material también se está construyendo.</h2><p>DejavuUrbe se encuentra actualmente grabando nuevas canciones. A medida que ese proceso genere material audiovisual publicable, esta sección servirá también como acceso a esa etapa de estudio.</p>',
    '<div class="video-current"><div class="eyebrow">Ahora</div><h2>Nuevas canciones en proceso.</h2><p>DejavuUrbe está grabando nuevas canciones y documentando esta nueva etapa de estudio.</p>'
)

# 5) Enlaces: quitar explicaciones de jerarquía editorial y hablar directamente al visitante.
replace('enlaces/index.html', 'Primero, los canales principales.', 'Canales oficiales')
replace(
    'enlaces/index.html',
    'YouTube, Instagram y Facebook concentran hoy la presencia pública principal de DejavuUrbe. Después aparecen las demás plataformas y referencias.',
    'YouTube, Instagram, Facebook y Bandcamp reúnen la música, los videos y la actividad de DejavuUrbe.'
)
replace('enlaces/index.html', 'Identidad y catálogo.', 'Discografía y referencias musicales')
replace(
    'enlaces/index.html',
    'Fuentes públicas que ayudan a relacionar a DejavuUrbe con su discografía y su identidad musical.',
    'Discografía y referencias de DejavuUrbe en servicios especializados de información musical.'
)

# Completar metadatos visuales básicos que faltaban en Enlaces.
p = ROOT / 'enlaces/index.html'
text = p.read_text(encoding='utf-8')
needle = '<link rel="canonical" href="https://dejavuurbe.github.io/dejavuurbe-web/enlaces/"><link rel="stylesheet"'
if needle in text:
    text = text.replace(
        needle,
        '<link rel="canonical" href="https://dejavuurbe.github.io/dejavuurbe-web/enlaces/"><link rel="icon" href="../assets/brand/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#080808"><link rel="stylesheet"'
    )
    p.write_text(text, encoding='utf-8')
    print('Metadatos visuales completados: enlaces/index.html')
