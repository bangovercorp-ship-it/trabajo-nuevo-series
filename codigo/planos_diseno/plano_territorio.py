# -*- coding: utf-8 -*-
"""Puerto Candela en su territorio. 09-territorio-puerto-candela.png

POR QUE EXISTE: la biblia describe el barrio con detalle y del territorio solo dice
cuatro cosas (llanura aluvial del Guayas, 15 km del mar, lluvia de enero a abril,
salitre). Cuando un capitulo abre con la ciudad desde el aire, eso no alcanza: hay
que saber que hay alrededor, o cada toma lo inventa distinto.

Este plano propone el territorio completo y etiqueta cada pieza:
    DATO        esta escrito en la biblia
    PROPUESTA   lo decide este plano, es coherente con el dato y no lo contradice
    HIPOTESIS   habria que validarlo antes de darlo por cierto

LA PIEZA QUE ORDENA TODO ES EL ESTERO. Explica el nombre del pueblo, explica la
Calle El Puerto que ya estaba en el plano urbano, explica de que vive la gente
(camaron y arroz) y explica el salitre a 15 km del mar sin necesidad de playa.

Escala 1:2000 aprox. 1 px = 2 m.
"""
import math

from PIL import Image, ImageDraw

from comun import destino, fuente, TINTA

PX = 0.5                       # pixeles por metro
X0, X1 = -3000, 3800           # limites del territorio dibujado, en metros
Z0, Z1 = -2100, 2500
MARG_X, MARG_SUP, MARG_INF = 70, 210, 150
LEYENDA = 560

AN = int((X1 - X0) * PX) + MARG_X * 2 + LEYENDA
AL = int((Z1 - Z0) * PX) + MARG_SUP + MARG_INF

# paleta del territorio
AGUA = "#7d949b"
MANGLAR = "#4e6b4a"
CAMARON = "#8fa3a2"
ARROZ = "#89a05e"
MONTE = "#6f7d4c"
LLANO = "#b3ad84"
PUEBLO = "#cfc4ae"
VIA = "#5f5b54"
LOMA = "#a99a74"
PAPEL = "#f4f1e8"

im = Image.new("RGB", (AN, AL), PAPEL)
d = ImageDraw.Draw(im, "RGBA")

f_tit = fuente("serif_bold", 44)
f_sub = fuente("sans", 21)
f_cap = fuente("sans_bold", 22)
f_med = fuente("sans", 17)
f_peq = fuente("sans", 14)
f_min = fuente("sans", 12)
f_rot = fuente("sans_bold", 16)


def Q(x, z):
    """metros del territorio -> pixeles del dibujo"""
    return (MARG_X + (x - X0) * PX, MARG_SUP + (z - Z0) * PX)


def rect(x0, z0, x1, z1, fill, out=None, w=1):
    a, b = Q(x0, z0)
    c, e = Q(x1, z1)
    d.rectangle([min(a, c), min(b, e), max(a, c), max(b, e)], fill=fill, outline=out, width=w)


def poly(pts, fill, out=None, w=1):
    d.polygon([Q(x, z) for x, z in pts], fill=fill, outline=out, width=w)


def linea(pts, col, w=2):
    d.line([Q(x, z) for x, z in pts], fill=col, width=w, joint="curve")


def texto(x, z, s, f=f_med, col=TINTA, anc="lt"):
    d.text(Q(x, z), s, font=f, fill=col, anchor=anc)


def etiqueta(x, z, titulo, clase, detalle="", f=f_rot):
    """rotulo con su etiqueta de certeza: nada se presenta como dato si no lo es"""
    px, py = Q(x, z)
    col = {"DATO": "#1d6a6a", "PROPUESTA": "#8a5a1c", "HIPOTESIS": "#8a2b2b"}[clase]
    an = max(d.textlength(titulo, font=f), d.textlength(detalle, font=f_min) if detalle else 0)
    alto = 22 + (15 if detalle else 0) + 14
    d.rectangle([px - 6, py - 5, px + an + 10, py + alto], fill=(255, 255, 255, 214),
                outline=col, width=2)
    d.text((px, py), titulo, font=f, fill=TINTA)
    d.text((px, py + 20), clase, font=f_min, fill=col)
    if detalle:
        d.text((px + d.textlength(clase, font=f_min) + 10, py + 20), detalle, font=f_min, fill="#5a554c")


# ---------------------------------------------------------------- la llanura
rect(X0, Z0, X1, Z1, LLANO)

# manchas de monte, con la misma semilla que la maqueta 3D para que peguen
sem = 20260925


def rnd(n):
    t = (int(n) * 1103515245 + sem) & 0xFFFFFFFF
    t ^= t >> 15
    t = (t * 2246822507) & 0xFFFFFFFF
    t ^= t >> 13
    return t / 4294967296.0


for i in range(22):
    mx = -3000 + rnd(i * 13) * 6600
    mz = -2600 + rnd(i * 19) * 5200
    an = 240 + rnd(i * 7) * 700
    fo = 200 + rnd(i * 11) * 620
    if -700 < mx < 1300 and -600 < mz < 800:
        continue
    if mz + fo < -480 and -1700 < mx < 2700:      # ahi va el arrozal del norte
        continue
    if -2900 < mx < -900 and -520 < mz < 800:     # y ahi el del oeste
        continue
    rect(mx, mz, mx + an, mz + fo, MONTE)

# arrozales al norte y al oeste
rect(-1600, -2600, 2600, -520, ARROZ)
rect(-2800, -420, -980, 760, ARROZ)
for x in range(-1600, 2600, 120):          # el damero de las piscinas
    linea([(x, -2600), (x, -520)], "#7b9153", 1)
for z in range(-2600, -520, 90):
    linea([(-1600, z), (2600, z)], "#7b9153", 1)
for x in range(-2800, -980, 120):
    linea([(x, -420), (x, 760)], "#7b9153", 1)
for z in range(-420, 760, 90):
    linea([(-2800, z), (-980, z)], "#7b9153", 1)

# camaroneras
for cx0, cz0, cx1, cz1 in [(-900, 440, 420, 640), (760, 380, 2600, 780), (-1200, 880, 500, 1380)]:
    rect(cx0, cz0, cx1, cz1, CAMARON)
    for x in range(int(cx0), int(cx1), 170):
        linea([(x, cz0), (x, cz1)], "#a69a74", 3)
    for z in range(int(cz0), int(cz1), 130):
        linea([(cx0, z), (cx1, z)], "#a69a74", 3)

# el Estero Candela, con su comba
TRAMOS = [(-1900, 420, 636, 806, 0.055), (120, 1320, 672, 858, -0.085),
          (1060, 2540, 690, 902, 0.07), (2240, 3900, 742, 1010, -0.05)]
for ex0, ex1, ez0, ez1, rot in TRAMOS:
    cx, cz = (ex0 + ex1) / 2, (ez0 + ez1) / 2
    pts = []
    for sx, sz in [(ex0, ez0), (ex1, ez0), (ex1, ez1), (ex0, ez1)]:
        dx, dz = sx - cx, sz - cz
        pts.append((cx + dx * math.cos(rot) - dz * math.sin(rot),
                    cz + dx * math.sin(rot) + dz * math.cos(rot)))
    poly(pts, MANGLAR)
    pts2 = []
    for sx, sz in [(ex0, ez0 + 40), (ex1, ez0 + 40), (ex1, ez1 - 40), (ex0, ez1 - 40)]:
        dx, dz = sx - cx, sz - cz
        pts2.append((cx + dx * math.cos(rot) - dz * math.sin(rot),
                     cz + dx * math.sin(rot) + dz * math.cos(rot)))
    poly(pts2, AGUA)

# la Loma de la Cruz
for r, col in [(300, LOMA), (215, "#b6a67e"), (130, "#c2b288"), (60, "#cdbd92")]:
    a, b = Q(-470 - r, -420 - r)
    c, e = Q(-470 + r, -420 + r)
    d.ellipse([a, b, c, e], fill=col, outline="#8e8163", width=1)

# ---------------------------------------------------------------- el pueblo
rect(-372, -256, 900, 500, PUEBLO, "#7a7260", 3)   # huella urbana
rect(-24, 300, 640, 640, "#c7bda8")                # el camino al muelle

# vialidad estructurante
rect(X0, 112, X1, 152, VIA)                        # Av. El Cruce y la carretera
rect(224, -260, 244, 640, "#6b6760")               # Calle Olmedo - Calle El Puerto
linea([(588, 300), (598, 660)], "#6b6760", 5)

# la retícula del barrio El Cruce, como referencia
rect(0, 0, 600, 299, "#d8cebb", "#8e8878", 2)
for x in [0, 112, 124, 224, 244, 344, 356, 456, 468, 588, 600]:
    linea([(x, 0), (x, 299)], "#a8a08e", 1)
for z in [0, 12, 56, 68, 112, 152, 187, 231, 243, 287, 299]:
    linea([(0, z), (600, z)], "#a8a08e", 1)
rect(244, 152, 268, 182, "#1d1b19")                # el taller
rect(244, 92, 256, 112, "#1f4d3a")                 # el bar

# muelle
rect(580, 640, 618, 690, "#8a7b62", TINTA, 2)

# ---------------------------------------------------------------- rotulos
etiqueta(-2760, -2020, u"ARROZALES", "PROPUESTA", u"regadío, verdes todo el año")
etiqueta(1450, 320, u"CAMARONERAS", "PROPUESTA", u"de aquí sale el jornal del pueblo")
etiqueta(-1850, 470, u"CAMARONERAS", "PROPUESTA")
etiqueta(700, 1080, u"ESTERO CANDELA", "PROPUESTA", u"marea; sale al Golfo de Guayaquil")
etiqueta(-2500, 980, u"MANGLAR", "PROPUESTA", u"en las dos orillas")
etiqueta(-900, -760, u"LOMA DE LA CRUZ  +96 m", "HIPOTESIS", u"la llanura no la nombra: VALIDAR")
etiqueta(1900, -1500, u"BOSQUE SECO TROPICAL", "DATO", u"ni desierto ni selva")
etiqueta(2450, 60, u"CARRETERA A GUAYAQUIL", "PROPUESTA", u"a 15 km del mar")
etiqueta(-2980, 60, u"VÍA VIEJA AL OESTE", "PROPUESTA")
etiqueta(700, 480, u"MUELLE", "PROPUESTA", u"fibras y camaroneras")

rect(0, 0, 600, 299, None, "#3a352c", 4)
texto(608, 120, u"BARRIO EL CRUCE", f_cap, "#3a352c", "lm")
texto(608, 142, u"2.232 hab · 25 mz · 496 lotes", f_peq, "#5a554c", "lm")
texto(608, 162, u"es el barrio que ve la cámara", f_peq, "#5a554c", "lm")
texto(290, -190, u"NUEVO AMANECER", f_rot, "#4a4436", "mm")
texto(290, -168, u"el pueblo que crece sin asfalto", f_min, "#6a6456", "mm")
texto(-198, -40, u"LOS ALMENDROS", f_rot, "#4a4436", "mm")
texto(-198, -18, u"el barrio viejo", f_min, "#6a6456", "mm")
texto(770, 400, u"EL MUELLE", f_rot, "#4a4436", "mm")
texto(770, 422, u"pescadores y bodegas", f_min, "#6a6456", "mm")
texto(300, 360, u"ZONA INDUSTRIAL", f_rot, "#4a4436", "mm")
texto(-470, -420, u"LA LOMA", f_rot, "#4a4436", "mm")

# flecha norte
nx, ny = Q(X1 - 300, Z0 + 230)
d.polygon([(nx, ny - 78), (nx - 24, ny + 30), (nx, ny + 8), (nx + 24, ny + 30)],
          fill=TINTA)
d.text((nx, ny + 44), "N", font=f_cap, fill=TINTA, anchor="mt")

# escala grafica
ex, ey = Q(X0 + 160, Z1 - 170)
for i in range(4):
    d.rectangle([ex + i * 250, ey, ex + (i + 1) * 250, ey + 17],
                fill=TINTA if i % 2 == 0 else PAPEL, outline=TINTA, width=2)
    d.text((ex + i * 250, ey + 24), "%d" % (i * 500), font=f_peq, fill=TINTA, anchor="mt")
d.text((ex + 1000, ey + 24), "2.000 m", font=f_peq, fill=TINTA, anchor="mt")
d.text((ex, ey - 24), u"ESCALA GRÁFICA", font=f_peq, fill=TINTA)

# ---------------------------------------------------------------- cajetin
d.rectangle([0, 0, AN, MARG_SUP - 40], fill="#eae5d8")
d.line([(0, MARG_SUP - 40), (AN, MARG_SUP - 40)], fill=TINTA, width=3)
d.text((MARG_X, 44), u"PUERTO CANDELA · EL TERRITORIO", font=f_tit, fill=TINTA)
d.text((MARG_X, 104),
       u"Provincia del Guayas · llanura aluvial · 15 km del mar · lluvias de enero a abril",
       font=f_sub, fill="#5a554c")
d.text((MARG_X, 134),
       u"Propuesta de paisaje para las tomas de apertura. Cada pieza va etiquetada: "
       u"DATO es lo que ya dice la biblia, PROPUESTA lo decide este plano, HIPÓTESIS hay que validarlo.",
       font=f_peq, fill="#6a6456")

# ---------------------------------------------------------------- leyenda
lx = MARG_X + int((X1 - X0) * PX) + 40
ly = MARG_SUP + 10
d.text((lx, ly), u"LEYENDA", font=f_cap, fill=TINTA)
ly += 40
for col, nom, nota in [
    (LLANO, u"Llanura de bosque seco", u"pasto seco y matorral"),
    (MONTE, u"Monte cerrado", u"manchas de arbolado"),
    (ARROZ, u"Arrozal", u"damero de piscinas"),
    (CAMARON, u"Camaronera", u"piscinas con muro de tierra"),
    (AGUA, u"Estero Candela", u"agua salobre, con marea"),
    (MANGLAR, u"Manglar", u"franja de las dos orillas"),
    (LOMA, u"Loma de la Cruz", u"HIPÓTESIS, +96 m"),
    (PUEBLO, u"Suelo urbano", u"~8.000 hab en el casco"),
    (VIA, u"Vía asfaltada", u"avenida y carretera"),
]:
    d.rectangle([lx, ly, lx + 44, ly + 26], fill=col, outline=TINTA, width=1)
    d.text((lx + 56, ly), nom, font=f_med, fill=TINTA)
    d.text((lx + 56, ly + 19), nota, font=f_min, fill="#6a6456")
    ly += 42

ly += 22
d.text((lx, ly), u"LAS DOS ESTACIONES", font=f_cap, fill=TINTA)
ly += 34
for tit, cuerpo in [
    (u"Invierno, enero a abril", u"DATO. Llueve de tarde, el monte se pone verde en seis\n"
                                 u"semanas, las calles sin asfaltar se vuelven barro y el\n"
                                 u"estero sube. Cielo cargado, luz suave."),
    (u"Verano, mayo a diciembre", u"DATO. Seco. Todo ocre, el ceibo sin hoja, polvo en la\n"
                                  u"calle. Sol duro de 11 a 15 h y cielo blanco."),
]:
    d.text((lx, ly), tit, font=f_rot, fill=TINTA)
    d.multiline_text((lx, ly + 22), cuerpo, font=f_min, fill="#5a554c", spacing=5)
    ly += 96

ly += 10
d.text((lx, ly), u"DECISIÓN PENDIENTE", font=f_cap, fill="#8a2b2b")
d.multiline_text((lx, ly + 30),
                 u"La temporada 1 se rueda en VERANO, que es la luz que\n"
                 u"ya fijó la biblia: sol duro, cielo blanco, polvo. El\n"
                 u"invierno queda para un capítulo de aguacero.\n"
                 u"Si se prefiere al revés, se cambia una línea del código.",
                 font=f_min, fill="#5a554c", spacing=5)

# ---------------------------------------------------------------- pie
d.line([(0, AL - MARG_INF + 30), (AN, AL - MARG_INF + 30)], fill=TINTA, width=2)
d.multiline_text((MARG_X, AL - MARG_INF + 48),
                 u"Lo que NO está verificado y hay que validar antes de grabar:  "
                 u"la Loma de la Cruz (la biblia dice llanura y no nombra ninguna elevación)  ·  "
                 u"la existencia del estero y del muelle  ·  el peso real del camarón frente al arroz\n"
                 u"en la economía del pueblo  ·  la distancia exacta a Guayaquil.  "
                 u"Todo lo demás sale de la pestaña «Ecuador · taller y barrio» de la biblia o es "
                 u"geografía general de la costa del Guayas.",
                 font=f_peq, fill="#5a554c", spacing=7)

im.save(destino("09-territorio-puerto-candela.png"))
print(u"09-territorio-puerto-candela.png  %d x %d" % (AN, AL))
