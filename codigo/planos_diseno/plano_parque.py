# -*- coding: utf-8 -*-
"""Parque del Reloj. 11-parque-del-reloj.png

POR QUE EXISTE: el plano urbano decia "Mz. G - Parque del Reloj" y nada mas. Una
manzana verde con una torre no es un diseno: es un hueco donde cada toma pone lo
que quiere. Y el parque sale en camara, porque es la plaza del pueblo.

COMO SE DISENA UNA PLAZA DE PUEBLO COSTENO, que es lo que se copia aqui:
  banda dura en todo el perimetro, que es por donde camina la gente
  dos diagonales de esquina a esquina, que cruzan en una rotonda
  cuatro cuadrantes de cesped entre las diagonales
  los usos repartidos para que no se estorben entre si
  sombra de verdad: arbol grande, no arbusto decorativo

Escala 1:200. 1 m = 16 px. Manzana G, 100,00 x 44,00 m.
"""
from PIL import Image, ImageDraw

from comun import destino, fuente, TINTA

PX = 16
ANCHO_M, FONDO_M = 100.0, 44.0
MARG = 170
PIE = 500
AN = int(ANCHO_M * PX) + MARG * 2
AL = int(FONDO_M * PX) + MARG + PIE

PAPEL = "#f4f1e8"
CESPED = "#93a877"
ADOQUIN = "#bdb5a4"
ADOQUIN2 = "#cdc6b6"
LOSA = "#a4aeb4"
ARENA = "#d8c9a4"
AGUA = "#8fa9c4"
HORM = "#c9c2b2"

im = Image.new("RGB", (AN, AL), PAPEL)
d = ImageDraw.Draw(im, "RGBA")

f_tit = fuente("serif_bold", 40)
f_sub = fuente("sans", 19)
f_cap = fuente("sans_bold", 21)
f_med = fuente("sans", 15)
f_peq = fuente("sans", 13)
f_min = fuente("sans", 11)


def Q(x, z):
    return (MARG + x * PX, MARG + z * PX)


def rect(x0, z0, x1, z1, fill, out=None, w=1):
    a, b = Q(x0, z0)
    c, e = Q(x1, z1)
    d.rectangle([a, b, c, e], fill=fill, outline=out, width=w)


def linea(p0, p1, col, w=2):
    d.line([Q(*p0), Q(*p1)], fill=col, width=w)


def circ(x, z, r, fill, out=None, w=1):
    a, b = Q(x - r, z - r)
    c, e = Q(x + r, z + r)
    d.ellipse([a, b, c, e], fill=fill, outline=out, width=w)


def txt(x, z, s, f=f_peq, col=TINTA, anc="mm"):
    d.text(Q(x, z), s, font=f, fill=col, anchor=anc)


def cota(x0, z0, x1, z1, s, col="#b3261e", lado=1):
    a, b = Q(x0, z0)
    c, e = Q(x1, z1)
    d.line([(a, b), (c, e)], fill=col, width=2)
    if z0 == z1:
        for xx in (a, c):
            d.line([(xx, b - 6), (xx, b + 6)], fill=col, width=2)
        an = d.textlength(s, font=f_min)
        d.rectangle([(a + c) / 2 - an / 2 - 4, b - 10, (a + c) / 2 + an / 2 + 4, b + 10], fill=PAPEL)
        d.text(((a + c) / 2, b), s, font=f_min, fill=col, anchor="mm")
    else:
        for yy in (b, e):
            d.line([(a - 6, yy), (a + 6, yy)], fill=col, width=2)
        an = d.textlength(s, font=f_min)
        d.rectangle([a - an / 2 - 4, (b + e) / 2 - 10, a + an / 2 + 4, (b + e) / 2 + 10], fill=PAPEL)
        d.text((a, (b + e) / 2), s, font=f_min, fill=col, anchor="mm")


def arbol(x, z, r, col, borde, etiq=None):
    circ(x, z, r, col, borde, 2)
    circ(x, z, 0.3, borde)
    if etiq:
        txt(x, z + r + 1.0, etiq, f_min, "#3e5c34")


# ---------------------------------------------------------------- base
rect(0, 0, ANCHO_M, FONDO_M, CESPED, TINTA, 3)

# banda perimetral dura de 3,00 m
for a, b, c, e in [(0, 0, ANCHO_M, 3), (0, FONDO_M - 3, ANCHO_M, FONDO_M),
                   (0, 0, 3, FONDO_M), (ANCHO_M - 3, 0, ANCHO_M, FONDO_M)]:
    rect(a, b, c, e, ADOQUIN, "#8e8878", 1)

# las dos diagonales, 3,20 m
CX, CZ = ANCHO_M / 2, FONDO_M / 2
for ex, ez in [(3, 3), (ANCHO_M - 3, 3), (3, FONDO_M - 3), (ANCHO_M - 3, FONDO_M - 3)]:
    dx, dz = CX - ex, CZ - ez
    L = (dx * dx + dz * dz) ** 0.5
    nx, nz = -dz / L * 1.6, dx / L * 1.6
    d.polygon([Q(ex + nx, ez + nz), Q(CX + nx, CZ + nz), Q(CX - nx, CZ - nz), Q(ex - nx, ez - nz)],
              fill=ADOQUIN2, outline="#8e8878")

# rotonda y torre del reloj
circ(CX, CZ, 8, ADOQUIN, "#8e8878", 2)
circ(CX, CZ, 2.4, HORM, TINTA, 2)
rect(CX - 1.25, CZ - 1.25, CX + 1.25, CZ + 1.25, "#e8e0cc", TINTA, 2)
linea((CX - 1.25, CZ - 1.25), (CX + 1.25, CZ + 1.25), TINTA, 1)
linea((CX + 1.25, CZ - 1.25), (CX - 1.25, CZ + 1.25), TINTA, 1)
txt(CX, CZ - 4.4, u"TORRE DEL RELOJ", f_peq, TINTA)
txt(CX, CZ - 2.9, u"2,50 × 2,50 · h 12,20 m", f_min, "#5a554c")
txt(CX, CZ + 4.2, u"ROTONDA Ø 16,00", f_min, "#5a554c")

# cancha de ecuavoley, al oeste
rect(12, 12, 30, 32, LOSA, TINTA, 2)
linea((21, 12), (21, 32), "#ffffff", 3)
linea((12, 22), (30, 22), "#ffffff", 1)
txt(21, 18, u"ECUAVÓLEY", f_peq, "#33414a")
txt(21, 20.2, u"18,00 × 20,00", f_min, "#33414a")
txt(21, 26, u"red a 2,85 m", f_min, "#33414a")

# juegos infantiles, al este, sobre arena
rect(68, 6, 88, 20, ARENA, TINTA, 2)
rect(72, 10, 78, 16, "#c9a227", TINTA, 1)
rect(80, 11, 86, 15, "#b4332b", TINTA, 1)
txt(78, 22.2, u"JUEGOS INFANTILES · piso de arena", f_min, "#6a5a2c")

# concha acustica, al este
d.polygon([Q(70, 28), Q(88, 28), Q(88, 39), Q(70, 39)], fill=HORM, outline=TINTA)
d.arc([Q(70, 22), Q(88, 39)], 0, 180, fill=TINTA, width=3)
txt(79, 33, u"CONCHA ACÚSTICA", f_peq, TINTA)
txt(79, 35.4, u"tarima 16,00 × 6,00", f_min, "#5a554c")
txt(79, 41.4, u"aquí se hace la fiesta patronal", f_min, "#6a6456")

# busto y astabandera, al oeste
circ(7.5, 22, 1.2, HORM, TINTA, 2)
txt(7.5, 25.2, u"BUSTO", f_min, "#5a554c")
circ(7.5, 8, 0.5, "#8a8f94", TINTA, 1)
txt(7.5, 10.4, u"ASTA", f_min, "#5a554c")

# bancas: 24, contra las diagonales y el perimetro
BANCAS = []
for i in range(9):
    BANCAS += [(9 + i * 9.5, 4.4), (9 + i * 9.5, FONDO_M - 4.4)]
for i in range(3):
    BANCAS += [(4.4, 12 + i * 10), (ANCHO_M - 4.4, 12 + i * 10)]
for bx, bz in BANCAS:
    rect(bx - 0.9, bz - 0.25, bx + 0.9, bz + 0.25, "#b9b2a2", TINTA, 1)

# faroles de 4,20 m
FAROLES = [(10, 8), (10, 36), (90, 8), (90, 36), (CX - 12, CZ), (CX + 12, CZ), (34, 4), (66, 40)]
for fx, fz in FAROLES:
    circ(fx, fz, 0.55, "#e8e4d8", TINTA, 2)
    linea((fx - 0.8, fz), (fx + 0.8, fz), TINTA, 1)
    linea((fx, fz - 0.8), (fx, fz + 0.8), TINTA, 1)

# arbolado
ARBOLES = [
    (8, 8, 3.2, "mango"), (8, 36, 3.2, "mango"), (38, 6, 3.4, "mango"),
    (38, 38, 3.4, "mango"), (62, 24, 3.2, "mango"), (24, 38, 2.8, "almendro"),
    (52, 4, 2.8, "almendro"), (92, 24, 2.8, "almendro"), (92, 38, 2.6, "almendro"),
    (2.5, 22, 2.2, "guayacan"), (97.5, 22, 2.2, "guayacan"),
    (50, 1.5, 2.2, "guayacan"), (50, 42.5, 2.2, "guayacan"),
    (46, 31, 1.8, "palma"), (54, 31, 1.8, "palma"),
]
COL = {"mango": ("#3f6236", "#2b4a28"), "almendro": ("#4f7340", "#3e5c34"),
       "guayacan": ("#d8b53a", "#a8861c"), "palma": ("#54743f", "#3e5c34")}
for ax, az, ar, esp in ARBOLES:
    c1, c2 = COL[esp]
    arbol(ax, az, ar, c1 + "cc", c2)

# cotas
cota(0, -3.2, ANCHO_M, -3.2, u"100,00 m")
cota(-3.2, 0, -3.2, FONDO_M, u"44,00 m")
cota(0, -1.4, 3, -1.4, u"3,00")
cota(12, 34.4, 30, 34.4, u"18,00")

# ---------------------------------------------------------------- cajetin
d.rectangle([0, 0, AN, MARG - 84], fill="#eae5d8")
d.line([(0, MARG - 84), (AN, MARG - 84)], fill=TINTA, width=3)
d.text((MARG, 26), u"PARQUE DEL RELOJ · Mz. G · 100,00 × 44,00 m", font=f_tit, fill=TINTA)
d.text((MARG, 74), u"Escala 1:200 · propuesta de diseño · el reloj de la torre atrasa, y eso no se arregla nunca",
       font=f_sub, fill="#5a554c")

# ---------------------------------------------------------------- pie
py = MARG + int(FONDO_M * PX) + 58
d.text((MARG, py), u"POR QUÉ ESTÁ REPARTIDO ASÍ", font=f_cap, fill=TINTA)
py += 34
for tit, cuerpo in [
    (u"La cancha al oeste", u"El ecuavóley hace ruido y junta gente de pie. Va lejos de la concha\n"
                            u"acústica y lejos de los juegos, para que no se estorben."),
    (u"Los juegos al este", u"Sobre arena, a la vista desde las bancas del norte y del sur, y con\n"
                            u"los tres mangos grandes dando sombra encima."),
    (u"La concha al fondo", u"Mira hacia adentro del parque: el público se para en el césped y en\n"
                            u"la diagonal. Es donde se hace la fiesta de la Virgen del Carmen."),
    (u"La torre en el cruce", u"Se ve desde las cuatro esquinas y desde la avenida. Es la referencia\n"
                              u"que necesita una toma de la ciudad para saber dónde está."),
]:
    d.text((MARG, py), tit, font=f_med, fill=TINTA)
    d.multiline_text((MARG + 190, py), cuerpo, font=f_peq, fill="#5a554c", spacing=5)
    py += 52

px2 = MARG + 700
py2 = MARG + int(FONDO_M * PX) + 58
d.text((px2, py2), u"VEGETACIÓN", font=f_cap, fill=TINTA)
py2 += 34
for c1, nom, nota in [
    ("#3f6236", u"Mango · 5 unidades", u"la sombra de verdad; copa densa de 6 a 7 m"),
    ("#4f7340", u"Almendro · 4", u"en el perímetro, copa baja sobre la banda dura"),
    ("#d8b53a", u"Guayacán · 4", u"uno en cada entrada; florece amarillo en verano"),
    ("#54743f", u"Palma · 2", u"flanquean la torre, y solo ahí"),
]:
    d.ellipse([px2, py2, px2 + 22, py2 + 22], fill=c1, outline=TINTA, width=1)
    d.text((px2 + 34, py2), nom, font=f_med, fill=TINTA)
    d.text((px2 + 34, py2 + 19), nota, font=f_min, fill="#6a6456")
    py2 += 40

py2 += 14
d.text((px2, py2), u"MOBILIARIO", font=f_cap, fill=TINTA)
d.multiline_text((px2, py2 + 30),
                 u"24 bancas de hormigón prefabricado de 1,80 m  ·  8 faroles de 4,20 m\n"
                 u"6 basureros  ·  sin cerramiento: el parque no se cierra con reja, se cruza\n\n"
                 u"PAVIMENTO: adoquín de hormigón en dos tonos, el claro en las diagonales y el\n"
                 u"oscuro en la banda perimetral, para que el cruce se lea desde el aire.",
                 font=f_peq, fill="#5a554c", spacing=6)

d.line([(0, AL - 80), (AN, AL - 80)], fill=TINTA, width=2)
d.multiline_text((MARG, AL - 64),
                 u"PENDIENTE DE VALIDAR: la advocación de la iglesia (Virgen del Carmen) y por lo tanto la fecha de la fiesta patronal. "
                 u"El resto del diseño es propuesta de este plano: la biblia solo\n"
                 u"decía «Parque del Reloj, con su torre que atrasa». Las medidas de la manzana sí salen del plano urbano y no se tocan.",
                 font=f_peq, fill="#5a554c", spacing=7)

im.save(destino("11-parque-del-reloj.png"))
print(u"11-parque-del-reloj.png  %d x %d" % (AN, AL))
