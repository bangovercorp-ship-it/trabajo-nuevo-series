# -*- coding: utf-8 -*-
"""Plano urbano del Barrio El Cruce, Puerto Candela, provincia del Guayas.
A escala. Todas las medidas en metros.

Version Ecuador (24 de septiembre de 2026). La traza NO cambia respecto de la
version anterior: manzanas de 100 x 44 m con dos filas de lotes, vias locales de
12 m, colectora de 20 m, avenida de 40 m con parterre central y pasaje de 5 m.
Cambian los nombres de las calles, los negocios y el marco normativo.

Normativa: NEC (Norma Ecuatoriana de la Construccion) mas la ordenanza del canton.
VALIDAR: retiros municipales, secciones viales minimas y el porcentaje de area
verde exigido. Las secciones de aqui son HIPOTESIS DE TRABAJO heredadas del
trazado anterior, no una norma ecuatoriana verificada.

Nota de lotes: la manzana de 100 m se divide en 12 lotes por fila, o sea 8,33 m
de frente, no 8,00 m. El total de 496 lotes sale de ahi.
"""
from PIL import Image, ImageDraw

from comun import destino, fuente

PX = 4                       # pixeles por metro
MX, MY = 260, 400            # margenes (px) para el contexto alrededor
ANCHO_M, ALTO_M = 600, 299
W, H = ANCHO_M * PX + 2 * MX, ALTO_M * PX + 2 * MY + 180

FONDO, MANZANA, LOTE, CALLE = "#efe6cf", "#e2d3ae", "#bda97c", "#fbf8ef"
TINTA, ORO, BRASA, GATA = "#2a2622", "#a07a2c", "#b3261e", "#c2185b"
VERDE, AZUL, GRIS = "#9dbb78", "#6f8fb5", "#9c9488"

f_tit, f_sub = fuente("sans_bold", 54), fuente("sans", 26)
f_calle, f_av = fuente("sans_bold", 22), fuente("sans_bold", 30)
f_mz, f_lug, f_peq = fuente("sans_bold", 20), fuente("sans_bold", 17), fuente("sans", 15)
f_min, f_micro = fuente("sans", 12), fuente("sans", 10)

im = Image.new("RGB", (W, H), FONDO)
d = ImageDraw.Draw(im)


def P(x, y):
    return (MX + x * PX, MY + y * PX)


def rect(x0, y0, x1, y1, fill, out=None, w=1):
    d.rectangle([P(x0, y0), P(x1, y1)], fill=fill, outline=out, width=w)


def texto(x, y, s, f, fill=TINTA, ancla="mm"):
    d.text(P(x, y), s, font=f, fill=fill, anchor=ancla)


def texto_vertical(x, y, s, f, fill=TINTA):
    ancho = int(d.textlength(s, font=f)) + 8
    capa = Image.new("RGBA", (ancho, f.size + 10), (0, 0, 0, 0))
    ImageDraw.Draw(capa).text((4, 2), s, font=f, fill=fill)
    capa = capa.rotate(90, expand=True)
    cx, cy = P(x, y)
    im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa)


# --- vias -----------------------------------------------------------------------
# Nombres del santoral civico ecuatoriano, que es lo que hay en cualquier pueblo
# del pais. La Calle Olmedo es la colectora: nadie la llama asi, todos le dicen
# "la calle de los mecanicos".
COLS = [(12, 112), (124, 224), (244, 344), (356, 456), (468, 588)]
V_CALLES = [(0, 12, "CALLE LOS CEIBOS"), (112, 124, "CALLE BUENAVISTA"), (224, 244, "CALLE OLMEDO"),
            (344, 356, "CALLE 10 DE AGOSTO"), (456, 468, "CALLE LOS ALMENDROS"), (588, 600, "CALLE EL PUERTO")]
FILAS = {"1": (12, 56), "2": (68, 112), "3": (152, 187), "4": (187, 231), "5": (243, 287)}
H_CALLES = [(0, 12, "CALLE ROCAFUERTE"), (56, 68, "CALLE SUCRE"), (231, 243, "CALLE ELOY ALFARO"),
            (287, 299, "CALLE JUAN MONTALVO")]

rect(0, 0, ANCHO_M, ALTO_M, CALLE)                       # todo es calle; encima van manzanas

lotes_total = 0
letras = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def manzana_residencial(x0, y0, x1, y1, frente=8):
    """dos filas de lotes: la de arriba mira al norte, la de abajo al sur"""
    global lotes_total
    rect(x0, y0, x1, y1, MANZANA, TINTA, 2)
    medio = (y0 + y1) / 2
    d.line([P(x0, medio), P(x1, medio)], fill=LOTE, width=1)
    n = max(1, round((x1 - x0) / frente))
    paso = (x1 - x0) / n
    for i in range(1, n):
        xx = x0 + i * paso
        d.line([P(xx, y0), P(xx, y1)], fill=LOTE, width=1)
    lotes_total += 2 * n


def franja_comercial(x0, y0, x1, y1, frente=10):
    """una sola fila de lotes de fondo completo, mirando a la avenida"""
    global lotes_total
    rect(x0, y0, x1, y1, MANZANA, TINTA, 2)
    n = max(1, round((x1 - x0) / frente))
    paso = (x1 - x0) / n
    for i in range(1, n):
        d.line([P(x0 + i * paso, y0), P(x0 + i * paso, y1)], fill=LOTE, width=1)
    lotes_total += n


def _mayor_que_quepa(s, ancho_px, opciones):
    """la fuente mas grande de la lista con la que el texto no se desborda"""
    for f in opciones:
        if d.textlength(s, font=f) <= ancho_px - 10:
            return f
    return opciones[-1]


def lugar(x0, y0, x1, y1, nombre, color, sub=None, borde=TINTA):
    rect(x0, y0, x1, y1, color, borde, 3)
    ancho = (x1 - x0) * PX
    col = "#ffffff" if color in (BRASA, GATA, AZUL) else TINTA
    texto((x0 + x1) / 2, (y0 + y1) / 2 - (7 if sub else 0), nombre,
          _mayor_que_quepa(nombre, ancho, [f_lug, f_peq, f_min, f_micro]), col)
    if sub:
        texto((x0 + x1) / 2, (y0 + y1) / 2 + 9, sub,
              _mayor_que_quepa(sub, ancho, [f_peq, f_min, f_micro]), col)


manzanas = {}
for fila, (y0, y1) in FILAS.items():
    for c, (x0, x1) in enumerate(COLS):
        if fila == "4" and c == 4:
            continue                                    # el hospital ocupa dos manzanas
        if fila == "5" and c == 4:
            continue
        if fila == "3":
            if c == 2:
                franja_comercial(x0, y0, x1, 182)       # detras corre el Pasaje La Esperanza
            else:
                franja_comercial(x0, y0, x1, y1)
        elif fila == "4" and c == 2:
            manzana_residencial(x0, 187, x1, y1)
        else:
            manzana_residencial(x0, y0, x1, y1)
        manzanas[(fila, c)] = next(letras)

# --- avenida con parterre central -----------------------------------------------
rect(0, 112, ANCHO_M, 152, "#f6f1e3")
rect(0, 130, ANCHO_M, 134, "#b8c79c")
for xx in range(4, ANCHO_M, 14):
    d.line([P(xx, 121), P(xx + 6, 121)], fill=GRIS, width=2)
    d.line([P(xx, 143), P(xx + 6, 143)], fill=GRIS, width=2)
texto(300, 126, "AV. EL CRUCE  ·  la via vieja a Guayaquil  ·  sección 40 m (2 carriles por lado + parterre)", f_av)

# pasaje detras del taller
rect(244, 182, 344, 187, "#d9cdb0", TINTA, 1)
texto(294, 184.6, "PASAJE LA ESPERANZA (5 m)", f_peq)

# --- equipamiento ----------------------------------------------------------------
lugar(124, 12, 224, 56, "ESCUELA FISCAL", "#e9c98a", "Vicente Rocafuerte · losa deportiva")
lugar(244, 12, 344, 56, "MERCADO MUNICIPAL", "#e7b27c", "84 puestos · abierto 6 a 14 h")
lugar(124, 68, 224, 112, "", VERDE)
d.ellipse([P(166, 82), P(182, 98)], fill="#c9d9ad", outline=TINTA, width=2)
rect(172, 87, 176, 93, ORO, TINTA, 2)
texto(174, 76, "PARQUE DEL RELOJ", f_lug)
texto(174, 104, "torre del reloj (atrasa) · juegos · bancas", f_peq)
lugar(76, 68, 112, 92, "IGLESIA", "#d8c3e0", "Virgen del Carmen")
lugar(356, 90, 392, 112, "UPC", AZUL, "El Cruce")
lugar(398, 90, 428, 112, "CENTRO DE", "#cfe3e8", "SALUD · MSP")
lugar(494, 88, 534, 112, "HOSTAL", "#e6d3b3", "El Descanso")
lugar(540, 84, 588, 112, "HOTEL", "#e6d3b3", "Panamericano")
rect(244, 92, 256, 112, GATA, TINTA, 3)                  # casona de esquina 12 x 20 m
texto(260, 99, "BAR LA GATA", f_lug, GATA, "lm")
texto(260, 107, "12 × 20 m · Micaela vive arriba", f_peq, TINTA, "lm")
lugar(468, 187, 588, 287, "HOSPITAL DE EMERGENCIAS", "#f3f0f0", "El Cruce · 3 pisos · 60 camas")
d.line([P(520, 250), P(536, 250)], fill=BRASA, width=6)
d.line([P(528, 242), P(528, 258)], fill=BRASA, width=6)
lugar(540, 152, 588, 187, "GASOLINERA", "#f0e08a", "El Último")
lugar(244, 243, 290, 287, "LOSA", "#c9d9ad", "deportiva")

# franja comercial de la avenida, de oeste a este
lugar(40, 152, 76, 187, "TIENDA", "#e8dcc0", "de barrio")
lugar(124, 152, 154, 187, "PICANTERÍA", "#f1c7b1", "aquí almuerza el taller")
lugar(156, 152, 178, 187, "ASADERO", "#f1c7b1")
lugar(180, 152, 204, 187, "FARMACIA", "#dfe9d3")
lugar(206, 152, 224, 187, "TERCENA", "#f1c7b1", "(carnicería)")
lugar(356, 152, 398, 187, "BODEGA DE", "#e0cfa8", "LUBRICANTES")
lugar(400, 152, 428, 187, "FERRETERÍA", "#e0cfa8")
lugar(468, 152, 530, 187, "ENDEREZADA Y PINTURA", "#d8cdb8", "el compadre · a dos cuadras")

# la cuadra de repuestos y la vulcanizadora, sobre la Calle Olmedo
lugar(270, 152, 318, 182, "REPUESTOS", "#e0cfa8", "6 almacenes")
lugar(320, 152, 344, 182, "VULCANIZADORA", "#e0cfa8", "parcha llantas")

# el taller: lote de esquina de 24 x 30 m, esquina sureste de la avenida con Olmedo
rect(244, 152, 268, 182, BRASA, "#000000", 4)
texto(256, 163, "TALLER", f_lug, "#ffffff")
texto(256, 171, "GALLARDO", f_lug, "#ffffff")
texto(256, 178, "24 × 30 m", f_peq, "#ffffff")

# casas de los personajes
for (x, y, s, dy) in [(100, 200, "Casa de Porfirio", 6), (136, 214, "Casa de Toribio", 6),
                      (196, 200, "Casa de Yadira", 6), (400, 200, "Casa de Kevin", 6)]:
    d.ellipse([P(x - 2, y - 2), P(x + 2, y + 2)], fill=BRASA)
    texto(x, y + dy, s, f_peq)

# paraderos
for (x, y) in [(60, 150), (520, 150), (212, 114)]:
    rect(x - 4, y - 1.2, x + 4, y + 1.2, "#3c5a80")
    texto(x, y - 3.5 if y > 130 else y + 4.5, "paradero", f_peq)

# --- nombres de calles -----------------------------------------------------------
for (a, b, n) in V_CALLES:
    for yy in (56, 232):
        texto_vertical((a + b) / 2, yy, n, f_calle if b - a >= 20 else f_peq)
texto_vertical(234, 168, "la calle de los mecánicos", f_peq, BRASA)
for (a, b, n) in H_CALLES:
    for xx in (62, 294, 518):
        if n == "CALLE ELOY ALFARO" and xx == 518:
            continue                    # ahi esta el hospital
        texto(xx, (a + b) / 2, n, f_calle)

# letras de manzana
for (fila, c), letra in manzanas.items():
    x0, x1 = COLS[c]
    y0, y1 = FILAS[fila]
    if fila == "3":
        continue
    d.text(P(x0 + 3, y0 + 3), "Mz. " + letra, font=f_mz, fill=TINTA)

# --- contexto alrededor -------------------------------------------------------------
cerro = [P(-40, -8), P(60, -40), P(160, -28), P(260, -48), P(380, -34), P(480, -44), P(640, -22), P(640, -8)]
d.polygon(cerro, fill="#d9c9a3", outline=TINTA)
texto(300, -18, "CERRO EL MIRADOR  ·  asentamiento humano en la ladera", f_calle)
rect(-40, 306, 640, 340, "#d6d0c4", TINTA, 1)
texto(300, 323, "ZONA INDUSTRIAL  ·  bodegas, camaroneras y talleres grandes", f_calle)
d.polygon([P(-42, 132), P(-20, 118), P(-20, 146)], fill=TINTA)
texto(-30, 116, "AL CENTRO DE", f_calle)
texto(-30, 148, "PUERTO CANDELA", f_calle)
d.polygon([P(642, 132), P(620, 118), P(620, 146)], fill=TINTA)
texto(625, 116, "A GUAYAQUIL", f_calle)
texto(625, 148, "(poco más de 1 h)", f_calle)

# --- rotulos, norte, escala y cuadro de datos ---------------------------------------
d.text((MX, 34), "PLANO URBANO · BARRIO EL CRUCE", font=f_tit, fill=TINTA)
d.text((MX, 96), "Puerto Candela, provincia del Guayas · El Taller del Tío Gallín", font=f_sub, fill=TINTA)
d.text((MX, 132), "escala gráfica · medidas en metros · norte arriba", font=f_sub, fill=TINTA)
nx, ny = W - 150, 90
d.polygon([(nx, ny - 50), (nx - 22, ny + 20), (nx, ny + 5), (nx + 22, ny + 20)], fill=TINTA)
d.text((nx, ny + 45), "N", font=f_tit, fill=TINTA, anchor="mm")

ex, ey = MX, H - 150
d.rectangle([ex, ey, ex + 50 * PX, ey + 14], fill=TINTA)
d.rectangle([ex + 50 * PX, ey, ex + 100 * PX, ey + 14], fill="#ffffff", outline=TINTA, width=2)
for m in (0, 50, 100):
    d.text((ex + m * PX, ey + 32), "%d m" % m, font=f_peq, fill=TINTA, anchor="mm")

habitantes = lotes_total * 4.5
datos = ["%d manzanas  ·  %d lotes (vivienda y comercio)" % (len(manzanas) + 2, lotes_total),
         "unos %s habitantes (4,5 por lote)" % format(int(round(habitantes, -2)), ",").replace(",", "."),
         "área urbana: 600 × 299 m = 17,9 ha  ·  lote tipo 8,33 × 22 m",
         "parque + losa: 6.400 m² (≈ 8 % del área útil · VALIDAR con la ordenanza del cantón)"]
for i, s in enumerate(datos):
    d.text((ex + 520, ey - 16 + i * 30), s, font=f_sub, fill=TINTA)

im.save(destino("01-plano-urbano-el-cruce.png"), optimize=True)
print("lotes:", lotes_total, "| habitantes aprox:", int(habitantes), "| manzanas:", len(manzanas) + 2)
