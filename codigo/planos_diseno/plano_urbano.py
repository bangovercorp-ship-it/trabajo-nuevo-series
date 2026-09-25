# -*- coding: utf-8 -*-
"""Plano urbano del Barrio El Cruce, a escala. Todas las medidas en metros.

Criterios (RNE Peru): manzanas residenciales de 100 x 44 m con dos filas de lotes
de 8 x 22 m; vias locales de 12 m de seccion, colectora de 20 m, avenida de 40 m
con berma central; pasaje de 5 m; parque = aporte de recreacion publica.
"""
from PIL import Image, ImageDraw, ImageFont

PX = 4                       # pixeles por metro
MX, MY = 260, 400            # margenes (px) para el contexto alrededor
ANCHO_M, ALTO_M = 600, 299
W, H = ANCHO_M * PX + 2 * MX, ALTO_M * PX + 2 * MY + 180

FONDO, MANZANA, LOTE, CALLE = "#efe6cf", "#e2d3ae", "#bda97c", "#fbf8ef"
TINTA, ORO, BRASA, GATA = "#2a2622", "#a07a2c", "#b3261e", "#c2185b"
VERDE, AZUL, GRIS = "#9dbb78", "#6f8fb5", "#9c9488"

F = "C:/Windows/Fonts/"
def fuente(n, s): return ImageFont.truetype(F + n, s)
f_tit, f_sub = fuente("arialbd.ttf", 54), fuente("arial.ttf", 26)
f_calle, f_av = fuente("arialbd.ttf", 22), fuente("arialbd.ttf", 30)
f_mz, f_lug, f_peq = fuente("arialbd.ttf", 20), fuente("arialbd.ttf", 17), fuente("arial.ttf", 15)

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


# --- vias ---------------------------------------------------------------------
COLS = [(12, 112), (124, 224), (244, 344), (356, 456), (468, 588)]
V_CALLES = [(0, 12, "CALLE LOS PINOS"), (112, 124, "CALLE BUENAVISTA"), (224, 244, "JR. LOS MECÁNICOS"),
            (344, 356, "CALLE SAN MARTÍN"), (456, 468, "CALLE LOS OLIVOS"), (588, 600, "CALLE EL PUERTO")]
FILAS = {"1": (12, 56), "2": (68, 112), "3": (152, 187), "4": (187, 231), "5": (243, 287)}
H_CALLES = [(0, 12, "CALLE SANTA ROSA"), (56, 68, "CALLE LIMA"), (231, 243, "CALLE LAS FLORES"),
            (287, 299, "CALLE TÚPAC AMARU")]

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


def lugar(x0, y0, x1, y1, nombre, color, sub=None, borde=TINTA):
    rect(x0, y0, x1, y1, color, borde, 3)
    texto((x0 + x1) / 2, (y0 + y1) / 2 - (7 if sub else 0), nombre, f_lug, "#ffffff" if color in (BRASA, GATA, AZUL) else TINTA)
    if sub:
        texto((x0 + x1) / 2, (y0 + y1) / 2 + 9, sub, f_peq, "#ffffff" if color in (BRASA, GATA, AZUL) else TINTA)


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

# --- avenida con berma central --------------------------------------------------
rect(0, 112, ANCHO_M, 152, "#f6f1e3")
rect(0, 130, ANCHO_M, 134, "#b8c79c")
for xx in range(4, ANCHO_M, 14):
    d.line([P(xx, 121), P(xx + 6, 121)], fill=GRIS, width=2)
    d.line([P(xx, 143), P(xx + 6, 143)], fill=GRIS, width=2)
texto(300, 126, "AV. EL CRUCE  ·  carretera vieja  ·  sección 40 m (2 carriles por lado + berma)", f_av)

# pasaje detras del taller
rect(244, 182, 344, 187, "#d9cdb0", TINTA, 1)
texto(294, 184.6, "PASAJE LA ESPERANZA (5 m)", f_peq)

# --- equipamiento ----------------------------------------------------------------
lugar(124, 12, 224, 56, "I.E. JOSÉ OLAYA", "#e9c98a", "inicial y primaria · losa deportiva")
lugar(244, 12, 344, 56, "MERCADO SANTA ROSA", "#e7b27c", "84 puestos · abierto 6 a 14 h")
lugar(124, 68, 224, 112, "", VERDE)
d.ellipse([P(166, 82), P(182, 98)], fill="#c9d9ad", outline=TINTA, width=2)
rect(172, 87, 176, 93, ORO, TINTA, 2)
texto(174, 76, "PARQUE DEL RELOJ", f_lug)
texto(174, 104, "torre del reloj (atrasa) · juegos · bancas", f_peq)
lugar(80, 68, 112, 92, "PARROQUIA", "#d8c3e0", "Santa Rosa")
lugar(356, 90, 392, 112, "COMISARÍA", AZUL, "El Cruce")
lugar(398, 90, 428, 112, "CENTRO DE", "#cfe3e8", "SALUD")
lugar(494, 88, 534, 112, "HOSTAL", "#e6d3b3", "El Descanso")
lugar(540, 84, 588, 112, "HOTEL", "#e6d3b3", "Panamericano")
lugar(244, 92, 256, 112, "BAR", GATA, "LA GATA")
lugar(468, 187, 588, 287, "HOSPITAL DE EMERGENCIAS", "#f3f0f0", "El Cruce · 3 pisos · 60 camas")
d.line([P(520, 250), P(536, 250)], fill=BRASA, width=6)
d.line([P(528, 242), P(528, 258)], fill=BRASA, width=6)
lugar(540, 152, 588, 187, "GRIFO", "#f0e08a", "El Último")
lugar(356, 152, 396, 187, "LUBRICENTRO", "#e0cfa8")
lugar(124, 152, 150, 187, "CHIFA", "#f1c7b1", "Lung Fung")
lugar(152, 152, 178, 187, "POLLERÍA", "#f1c7b1", "El Leñador")
lugar(180, 152, 206, 187, "BOTICA", "#dfe9d3")
lugar(208, 152, 224, 187, "FERRE-", "#e0cfa8", "TERÍA")
lugar(270, 152, 344, 182, "TIENDAS DE REPUESTOS", "#e0cfa8", "6 locales")
lugar(244, 243, 290, 287, "LOSA", "#c9d9ad", "deportiva")

# el taller: lote de esquina de 24 x 30 m
rect(244, 152, 268, 182, BRASA, "#000000", 4)
texto(256, 163, "TALLER", f_lug, "#ffffff")
texto(256, 171, "GALLARDO", f_lug, "#ffffff")
texto(256, 178, "24 × 30 m", f_peq, "#ffffff")

# casas de los personajes
for (x, y, s, dy) in [(100, 200, "Casa de Porfirio", 6), (136, 214, "Casa de Toribio", 6)]:
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
for (a, b, n) in H_CALLES:
    for xx in (62, 294, 518):
        if n == "CALLE LAS FLORES" and xx == 518:
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
texto(300, 323, "ZONA INDUSTRIAL  ·  almacenes, depósitos y talleres grandes", f_calle)
d.polygon([P(-42, 132), P(-20, 118), P(-20, 146)], fill=TINTA)
texto(-30, 104, "AL CENTRO", f_calle)
texto(-30, 160, "DE LA CIUDAD", f_calle)
d.polygon([P(642, 132), P(620, 118), P(620, 146)], fill=TINTA)
texto(625, 104, "A LA CAPITAL", f_calle)
texto(625, 160, "(3 horas)", f_calle)

# --- rotulos, norte, escala y cuadro de datos ---------------------------------------
d.text((MX, 40), "PLANO URBANO · BARRIO EL CRUCE", font=f_tit, fill=TINTA)
d.text((MX, 108), "El Taller del Tío Gallín · escala gráfica · medidas en metros · norte arriba", font=f_sub, fill=TINTA)
nx, ny = W - 150, 90
d.polygon([(nx, ny - 50), (nx - 22, ny + 20), (nx, ny + 5), (nx + 22, ny + 20)], fill=TINTA)
d.text((nx, ny + 45), "N", font=f_tit, fill=TINTA, anchor="mm")

ex, ey = MX, H - 150
for i, m in enumerate((0, 25, 50, 100)):
    pass
d.rectangle([ex, ey, ex + 50 * PX, ey + 14], fill=TINTA)
d.rectangle([ex + 50 * PX, ey, ex + 100 * PX, ey + 14], fill="#ffffff", outline=TINTA, width=2)
for m in (0, 50, 100):
    d.text((ex + m * PX, ey + 32), "%d m" % m, font=f_peq, fill=TINTA, anchor="mm")

habitantes = lotes_total * 4.5
datos = ["%d manzanas  ·  %d lotes (vivienda y comercio)" % (len(manzanas) + 2, lotes_total),
         "unos %s habitantes (4,5 por lote)" % format(int(round(habitantes, -2)), ",").replace(",", "."),
         "área urbana: 600 × 299 m = 17,9 ha",
         "parque + losa: 6.400 m² (≈ 8 % del área útil, aporte de recreación del RNE)"]
for i, s in enumerate(datos):
    d.text((ex + 520, ey - 16 + i * 30), s, font=f_sub, fill=TINTA)

im.save(r"C:\pesonajes para videos\planos_diseno\01-plano-urbano-el-cruce.png", optimize=True)
print("lotes:", lotes_total, "| habitantes aprox:", int(habitantes), "| manzanas:", len(manzanas))
