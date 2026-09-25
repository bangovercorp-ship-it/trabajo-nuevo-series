# -*- coding: utf-8 -*-
"""Planta y fachada del Taller Gallardo, a escala. Medidas en metros.
Version Ecuador, con las nueve zonas que pidio la oficina de talleres.

Lote de esquina 24 x 30 m. Norte (arriba) = Av. El Cruce; oeste (izquierda) =
Calle Olmedo, la de los mecanicos; sur (abajo) = Pasaje La Esperanza; este =
almacenes de repuestos. Los carros entran por la avenida y salen por la Calle
Olmedo: circulacion en L, sin retroceso.

LAS NUEVE ZONAS NUEVAS
  1 Bahia 0 de recepcion e inspeccion   6 Servicio de aire acondicionado
  2 Puesto de diagnostico (bahia 3)     7 Puestos de espera bajo toldo
  3 Area de residuos peligrosos         8 Zona limpia de electronica
  4 Canaleta y trampa de grasas         9 Control de calidad (regla, no metros)
  5 Extraccion de gases

DOS DESVIACIONES respecto del expediente, con su motivo:

a) La bahia 0 NO va bajo el toldo. El toldo esta sobre la Calle Olmedo, que es
   por donde el carro SALE. Recibir en la salida invierte el flujo: el carro
   tendria que cruzar el taller entero antes de ser recibido. Va contra el borde
   oeste del pasillo, apenas pasada la rampa, donde no estorba el giro a las
   bahias. Cuesta: el pasillo baja de 7,50 a 5,50 m libres en 4,5 m de recorrido.

b) El area de residuos NO sale del almacen de repuestos. El expediente pide dos
   cosas incompatibles: ponerla "junto al porton de salida" y sacarla del almacen,
   que esta en la esquina opuesta. Ademas achicar el almacen de 5,50 x 3,00 a
   5,50 x 2,20 libera 4,4 m2, y el area necesita 7,5. Sale del extremo oeste de la
   zona de motos, que queda junto a la salida (el gestor entra por ahi), lejos de
   la soldadura y lejos de la mesa de electronica. El almacen conserva sus
   5,50 x 3,00 m y con eso el metro libre del riel, que ya costo encontrar.

NIVEL +0,40. El piso interior sube 0,40 m sobre la vereda por riesgo de
inundacion, con rampa 1:10 (4,00 m de desarrollo) en los dos portones. La fachada
NO cambia de medidas: los 0,40 se absorben en el canto de la estructura, y la
altura libre interior queda en 5,50 m.

VALIDAR: zona sismica, tipo de suelo, retiros municipales (el toldo ocupa retiro),
y el tramite de residuos peligrosos con el organismo ecuatoriano.
"""
import math

from PIL import Image, ImageDraw

from comun import destino, fuente

f_tit, f_sub, f_zona = fuente("sans_bold", 46), fuente("sans", 22), fuente("sans_bold", 17)
f_med, f_peq, f_calle = fuente("sans", 15), fuente("sans", 13), fuente("sans_bold", 22)
f_min = fuente("sans", 11)

TINTA, MURO, PISO, PASILLO = "#26221e", "#3a3530", "#f4f0e6", "#e9e3d3"
ORO, BRASA, AMARILLO = "#b8923a", "#b3261e", "#e0b422"
NUEVO, VERDE = "#1d6a6a", "#2f7d32"          # turquesa = zona nueva

# ================================================================== PLANTA
PX, MX, MY = 36, 340, 300
W, H = int(24 * PX + 2 * MX + 620), int(30 * PX + MY + 250)
im = Image.new("RGB", (W, H), "#efe7d4")
d = ImageDraw.Draw(im)
P = lambda x, y: (MX + x * PX, MY + y * PX)


def rect(x0, y0, x1, y1, fill=None, out=TINTA, w=2):
    d.rectangle([P(x0, y0), P(x1, y1)], fill=fill, outline=out, width=w)


def txt(x, y, s, f=f_zona, fill=TINTA, a="mm"):
    d.text(P(x, y), s, font=f, fill=fill, anchor=a)


def cota_h(x0, x1, y, etiqueta):
    d.line([P(x0, y), P(x1, y)], fill=TINTA, width=1)
    for x in (x0, x1):
        d.line([P(x, y - 0.25), P(x, y + 0.25)], fill=TINTA, width=2)
    txt((x0 + x1) / 2, y - 0.35, etiqueta, f_med)


def cota_v(y0, y1, x, etiqueta):
    d.line([P(x, y0), P(x, y1)], fill=TINTA, width=1)
    for y in (y0, y1):
        d.line([P(x - 0.25, y), P(x + 0.25, y)], fill=TINTA, width=2)
    capa = Image.new("RGBA", (int(d.textlength(etiqueta, font=f_med)) + 6, 22), (0, 0, 0, 0))
    ImageDraw.Draw(capa).text((3, 2), etiqueta, font=f_med, fill=TINTA)
    capa = capa.rotate(90, expand=True)
    cx, cy = P(x - 0.45, (y0 + y1) / 2)
    im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa)


def carro(x0, y0, x1, y1):
    d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=14, fill="#cfd5dc", outline="#6b7684", width=2)
    d.rounded_rectangle([P(x0 + 1.3, y0 + 0.35), P(x1 - 1.6, y1 - 0.35)], radius=8, fill="#aeb8c4")


def carro_v(x0, y0, x1, y1):
    """igual que carro(), pero de pie: el eje largo va en y"""
    d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=14, fill="#cfd5dc", outline="#6b7684", width=2)
    d.rounded_rectangle([P(x0 + 0.3, y0 + 1.3), P(x1 - 0.3, y1 - 1.6)], radius=8, fill="#aeb8c4")


def moto(x, y):
    d.rounded_rectangle([P(x, y), P(x + 2.2, y + 0.7)], radius=6, fill="#c9c2b2", outline="#6b6358", width=2)


def rampa(x0, y0, x1, y1, horizontal):
    """rampa 1:10 rayada, 4,00 m de desarrollo para subir los 0,40 m"""
    rect(x0, y0, x1, y1, "#dcd2bb", "#8a8174", 2)
    n = 9
    for i in range(1, n):
        if horizontal:
            yy = y0 + (y1 - y0) * i / n
            d.line([P(x0, yy), P(x1, yy)], fill="#a89e8c", width=1)
        else:
            xx = x0 + (x1 - x0) * i / n
            d.line([P(xx, y0), P(xx, y1)], fill="#a89e8c", width=1)


def etiqueta_nueva(x, y, n):
    """circulo turquesa numerado: marca una de las nueve zonas nuevas"""
    d.ellipse([P(x - 0.42, y - 0.42), P(x + 0.42, y + 0.42)], fill=NUEVO, outline="#ffffff", width=2)
    txt(x, y, str(n), f_peq, "#ffffff")


# piso y muros perimetrales
rect(0, 0, 24, 30, PISO, None)
d.polygon([P(0, 0), P(3, 0), P(0, 3)], fill="#efe7d4")                  # ochavo de esquina 3 x 3
rect(7.5, 0, 15, 21, PASILLO, None)                                      # pasillo de maniobra
rect(0, 15.8, 7.5, 21, PASILLO, None)                                    # salida a la Calle Olmedo
for (a, b) in [((3, 0), (9, 0)), ((14, 0), (24, 0)), ((24, 0), (24, 30)), ((0, 30), (24, 30)),
               ((0, 3), (0, 16)), ((0, 20.5), (0, 30)), ((0, 3), (3, 0))]:
    d.line([P(*a), P(*b)], fill=MURO, width=9)

# --- canaleta perimetral con rejilla y trampa de grasas (zona 4) ------------------
for (a, b) in [((7.7, 0.6), (7.7, 20.8)), ((14.8, 0.6), (14.8, 20.8)), ((0.6, 20.8), (22.6, 20.8))]:
    d.line([P(*a), P(*b)], fill="#8c8478", width=7)
    d.line([P(*a), P(*b)], fill="#cfc7b8", width=3)
rect(5.5, 19.3, 7.0, 20.3, "#b9b0a0", TINTA, 2)
for k in range(5):
    d.line([P(5.6 + k * 0.3, 19.35), P(5.6 + k * 0.3, 20.25)], fill=TINTA, width=2)
txt(6.25, 18.85, "trampa de grasas", f_min)
etiqueta_nueva(7.9, 19.8, 4)

# rampas y portones
rampa(9, 0, 14, 4, True)
rampa(0, 16, 4, 20.5, False)
txt(11.5, 2.0, "rampa 1:10", f_min)
txt(2.0, 16.6, "rampa 1:10", f_min)
d.line([P(9, 0), P(14, 0)], fill=AMARILLO, width=9)
d.line([P(0, 16), P(0, 20.5)], fill=AMARILLO, width=9)
txt(11.5, -0.9, "ENTRADA VEHICULAR · portón enrollable 5,00 × 4,50 m", f_zona, BRASA)
d.polygon([P(11.5, 5.0), P(11.0, 4.0), P(12.0, 4.0)], fill=BRASA)
cota_v(16, 20.5, -6.0, "SALIDA 4,50 × 4,50 m")
d.polygon([P(0.8, 18.25), P(1.8, 17.75), P(1.8, 18.75)], fill=BRASA)
d.line([P(11.5, 5.2), P(11.5, 18.2), P(2, 18.2)], fill=BRASA, width=3)     # recorrido del carro
txt(0.2, -1.9, "ingreso peatonal por el ochavo", f_peq, TINTA, "lm")

# --- zona 1: bahia 0 de recepcion e inspeccion -----------------------------------
rect(7.6, 5.5, 9.5, 10.0, "#dff0ef", NUEVO, 3)
carro_v(7.65, 5.6, 9.45, 9.9)
capa = Image.new("RGBA", (150, 26), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((2, 2), "BAHÍA 0 · RECEPCIÓN", font=f_peq, fill=NUEVO)
capa = capa.rotate(90, expand=True)
cx, cy = P(8.55, 7.75)
im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa)
etiqueta_nueva(9.1, 5.95, 1)
txt(9.7, 10.5, "inspección, fotos, kilometraje", f_min, NUEVO, "lm")
cota_h(9.6, 15, 11.5, "5,50 m libres de pasillo")

# --- bahias al este --------------------------------------------------------------
bahias = [(1.0, 5.0, "BAHÍA 1 · elevador 2 columnas"), (5.0, 9.0, "BAHÍA 2 · elevador 2 columnas"),
          (9.0, 13.5, "BAHÍA 3 · elevador 4 postes"), (13.5, 17.0, "BAHÍA 4 · trabajo en piso"),
          (17.0, 20.5, "BAHÍA 5 · trabajo en piso")]
for y0, y1, nombre in bahias:
    rect(15, y0, 22.5, y1, "#f7f4ec", "#8a8174", 2)
    d.line([P(15, y0), P(15, y1)], fill=AMARILLO, width=4)
    carro(16.2, y0 + 0.95, 21.3, y1 - 0.35)
    txt(18.75, y0 + 0.12, nombre, f_peq, TINTA, "mt")
    if "2 columnas" in nombre:
        # Los dos postes van a los COSTADOS del carro, a media eslora: es lo que
        # sujeta un elevador de dos columnas. Separacion entre postes: 2,90 m.
        yc = (y0 + y1) / 2 + 0.3                      # eje del carro dentro de la bahia
        for yy in (yc - 1.45, yc + 1.45):
            rect(18.3, yy - 0.15, 18.9, yy + 0.15, BRASA, None)
    if "4 postes" in nombre:
        for (xx, yy) in [(15.6, y0 + 0.25), (21.6, y0 + 0.25), (15.6, y1 - 0.55), (21.6, y1 - 0.55)]:
            rect(xx, yy, xx + 0.3, yy + 0.3, BRASA, None)
# zona 2: la bahia 3 hace doble turno como puesto de diagnostico
rect(15, 9.0, 22.5, 13.5, None, NUEVO, 3)
txt(18.75, 9.62, "+ puesto de diagnóstico · escáner", f_min, NUEVO)
etiqueta_nueva(15.5, 9.5, 2)
# zona 5: manguera de extraccion de gases en la bahia 1
d.arc([P(20.5, 1.2), P(23.4, 4.1)], 250, 20, fill=NUEVO, width=5)
etiqueta_nueva(22.0, 1.5, 5)
rect(22.5, 1.0, 24, 20.5, "#e7e0cf", None)
capa = Image.new("RGBA", (110, 22), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((2, 2), "circulación", font=f_min, fill=TINTA)
capa = capa.rotate(90, expand=True)
cx, cy = P(23.25, 15.5)
im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa)
# zona 6: maquina de aire acondicionado junto a la bahia 2
rect(22.6, 5.6, 23.7, 7.6, "#dff0ef", NUEVO, 3)
etiqueta_nueva(23.15, 5.2, 6)
capa = Image.new("RGBA", (120, 24), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((2, 2), "A/C recarga", font=f_min, fill=NUEVO)
capa = capa.rotate(90, expand=True)
cx, cy = P(23.15, 6.6)
im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa)
cota_h(15, 22.5, 0.75, "7,50 m")
cota_v(1, 5, 14.4, "4,00")

# --- franja oeste ----------------------------------------------------------------
rect(0, 3, 7.5, 7.0, "#efe1c4")
txt(3.8, 4.4, "RECEPCIÓN Y CAJA")
txt(3.8, 5.3, "Porfirio · mostrador 3,0 m", f_peq)
txt(3.8, 6.8, "tablero de OT · 4 ganchos", f_min, NUEVO)
rect(0.9, 6.0, 3.9, 6.6, "#b58a55", None)
rect(0, 7.0, 7.5, 10.5, "#f1e9d8")
txt(3.8, 8.3, "SALA DE ESPERA")
txt(3.8, 9.2, "Renzo · escritorio y 4 sillas", f_peq)
rect(0, 10.5, 7.5, 15.8, "#f6efe0")
txt(3.8, 12.1, "BANCO PRINCIPAL DE GALLÍN")
txt(3.8, 13.0, "mesa 4,0 × 1,0 m · 2 lámparas ámbar", f_peq)
rect(1.8, 13.5, 5.8, 14.5, "#9aa1a8", TINTA, 2)
for xx in (2.8, 4.8):
    d.ellipse([P(xx - 0.35, 13.65), P(xx + 0.35, 14.35)], fill=ORO, outline=TINTA)
d.line([P(0.15, 10.8), P(0.15, 15.5)], fill=ORO, width=10)
txt(0.9, 15.2, "pared de herramientas 6 m", f_peq, TINTA, "lm")

# --- franja sur ------------------------------------------------------------------
zonas_sur = [
    (0, 21, 1.3, 27, "#ddd3bd", "", ""),
    (1.3, 21, 5.5, 24, "#dff0ef", "ZONA LIMPIA", "Toribio · mesa antiestática"),
    (1.3, 24, 5.5, 27, "#f3e6d0", "CAFÉ", "radio · calendario"),
    (0, 27, 5.5, 30, "#dde7ec", "BAÑOS Y VESTIDOR", "2 duchas · casilleros"),
    (5.5, 21, 8.0, 24, "#dff0ef", "RESIDUOS", "peligrosos"),
    (8.0, 21, 11.5, 24, "#e4ece4", "LAVADO DE PIEZAS", "separado de motos"),
    (5.5, 24, 11.5, 30, "#f1ece0", "ZONA DE MOTOS", "4 puestos · 6,0 × 6,0 m"),
    (11.5, 21, 17, 24, "#e7ddc6", "ALMACÉN", "repuestos · 5,50 × 3,00 m"),
    (11.5, 25, 14.5, 30, "#dcd6ca", "COMPRESOR", "300 L · a pasaje"),
    (14.5, 25, 17, 30, "#e2d8c3", "PAÑOL", "herr. pesada"),
    (17, 21, 24, 24, "#eee6d4", "ZONA DE LLANTAS", "desmontadora · balanceadora"),
]
for x0, y0, x1, y1, col, n, s in zonas_sur:
    rect(x0, y0, x1, y1, col, NUEVO if col == "#dff0ef" else TINTA, 3 if col == "#dff0ef" else 2)
    if n:
        f = f_zona if d.textlength(n, font=f_zona) <= (x1 - x0) * PX - 10 else f_peq
        txt((x0 + x1) / 2, (y0 + y1) / 2 - 0.35, n, f)
        fs = f_peq if d.textlength(s, font=f_peq) <= (x1 - x0) * PX - 10 else f_min
        txt((x0 + x1) / 2, (y0 + y1) / 2 + 0.45, s, fs)
etiqueta_nueva(1.8, 21.5, 8)
etiqueta_nueva(6.0, 21.5, 3)
# tambores del area de residuos
for k in range(3):
    d.ellipse([P(5.85 + k * 0.7, 23.35), P(6.4 + k * 0.7, 23.9)], fill="#c0713a", outline=TINTA, width=2)
for k in range(8):
    d.line([P(0.1, 21.3 + k * 0.7), P(1.2, 21.3 + k * 0.7)], fill=TINTA, width=2)   # escalera
txt(0.65, 26.6, "esc.", f_peq)
for i in range(4):
    moto(6.2 + (i % 2) * 2.7, 25.2 + (i // 2) * 3.4)

# estanteria de llantas sobre rieles y la puerta roja
rect(11.5, 24, 17, 25, "#d8d0bf", TINTA, 1)
for zz in (24.15, 24.85):
    d.line([P(11.5, zz), P(24, zz)], fill="#7a7266", width=2)
txt(14.25, 24.5, "riel: la estantería se corre 4,6 m", f_peq)
rect(17, 24, 24, 25, "#4a4540", TINTA, 2)
for xx in range(0, 14):
    d.ellipse([P(17.15 + xx * 0.49, 24.15), P(17.55 + xx * 0.49, 24.85)], outline="#9c948a", width=2)
txt(20.5, 23.78, "estantería sobre rieles 7 × 1 × 5 m", f_min, TINTA)
rect(19.9, 25.0, 21.1, 25.18, BRASA, None)
rect(17, 25.18, 24, 30, "#5b1d1d", TINTA, 3)
txt(20.5, 27.1, "CUARTO DE AFINAMIENTO", f_zona, "#f4e3b0")
txt(20.5, 27.9, "7,0 × 4,8 m · techo bajo a 3,0 m", f_peq, "#f4e3b0")
txt(20.5, 25.55, "puerta roja 1,20 × 2,40", f_peq, "#f4e3b0")
rect(21.8, 29.82, 22.8, 30.0, "#8c8c8c", None)
txt(22.3, 29.4, "salida secreta", f_peq, "#f4e3b0")

# --- zona 7: toldo de espera sobre el retiro de la Calle Olmedo --------------------
for k in range(12):
    d.line([P(-5, 3 + k), P(0, 3 + k)], fill="#b6ab95", width=1)
d.rectangle([P(-5, 3), P(0, 15)], outline=NUEVO, width=3)
capa = Image.new("RGBA", (330, 30), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((2, 2), "TOLDO DE ESPERA · 12 × 5 m · 4 puestos", font=f_peq, fill=NUEVO)
capa = capa.rotate(90, expand=True)
cx, cy = P(-3.4, 9)
im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa)
etiqueta_nueva(-1.0, 3.7, 7)
txt(-2.5, 15.7, "ocupa retiro · VALIDAR", f_min, BRASA)

# calles alrededor
txt(12, -2.5, "AV. EL CRUCE", f_calle)
txt(12, 31.3, "PASAJE LA ESPERANZA", f_calle)
capa = Image.new("RGBA", (420, 32), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((4, 2), "CALLE OLMEDO", font=f_calle, fill=TINTA)
capa = capa.rotate(90, expand=True)
im.paste(capa, (int(P(-8.4, 0)[0]), int(P(0, 8)[1])), capa)

# cotas generales
cota_h(0, 24, 32.7, "24,00 m (frente a la avenida)")
cota_v(0, 30, 25.7, "30,00 m (frente a la Calle Olmedo)")

# --- cuadro lateral ---------------------------------------------------------------
cx = MX + 24 * PX + 150
d.text((cx, MY - 20), "LAS NUEVE ZONAS NUEVAS", font=f_tit, fill=NUEVO)
nuevas = ["1 · Bahía 0 de recepción e inspección", "2 · Puesto de diagnóstico (bahía 3)",
          "3 · Residuos peligrosos 2,5 × 3,0 m", "4 · Canaleta y trampa de grasas",
          "5 · Extracción de gases (turbinas + manguera)", "6 · Servicio de aire acondicionado",
          "7 · Puestos de espera bajo toldo", "8 · Zona limpia de electrónica",
          "9 · Control de calidad: el que repara no aprueba"]
for i, s in enumerate(nuevas):
    d.text((cx, MY + 44 + i * 32), s, font=f_sub, fill=NUEVO)

y0 = MY + 44 + len(nuevas) * 32 + 30
filas = ["CAPACIDAD", "5 bahías + bahía 0 de recepción", "4 puestos de motos",
         "20,3 h vendibles/día (ver nota)", "capacidad teórica: 12 vehículos",
         "capacidad operativa: 8 o 9",
         "", "ÁREAS", "lote: 720 m² (con ochavo)", "bahías: 146 m²", "pasillo y salida: 196 m²",
         "Cuarto de Afinamiento: 34 m²", "almacén + pañol + compresor: 44 m²",
         "residuos + lavado de piezas: 18 m²",
         "", "NIVELES", "piso interior: +0,40 m sobre la vereda", "rampa 1:10 en los dos portones",
         "altura libre: 5,50 m", "Cuarto: cielo raso a 3,00 m",
         "casa de Gallín: 7,5 × 21 m sobre la franja oeste"]
for i, s in enumerate(filas):
    fnt = f_zona if s in ("ÁREAS", "NIVELES", "CAPACIDAD") else f_sub
    d.text((cx, y0 + i * 32), s, font=fnt, fill=TINTA)

d.text((MX, 34), "TALLER GALLARDO · PLANTA DEL PRIMER PISO", font=f_tit, fill=TINTA)
d.text((MX, 92), "Puerto Candela, Guayas · escala gráfica · medidas en metros · norte arriba", font=f_sub, fill=TINTA)
d.text((MX, 128), "entran por la avenida y salen por la Calle Olmedo · en turquesa, las nueve zonas nuevas",
       font=f_sub, fill=NUEVO)
ex, ey = MX, H - 80
d.rectangle([ex, ey, ex + 5 * PX, ey + 12], fill=TINTA)
d.rectangle([ex + 5 * PX, ey, ex + 10 * PX, ey + 12], fill="#ffffff", outline=TINTA, width=2)
for m in (0, 5, 10):
    d.text((ex + m * PX, ey + 28), "%d m" % m, font=f_peq, fill=TINTA, anchor="mm")
im.save(destino("02-planta-taller.png"), optimize=True)
print("planta ok")

# ================================================================== FACHADA
# La fachada NO cambia de medidas al subir el piso a +0,40: esos 0,40 se absorben
# en el canto de la estructura del techo y la altura libre interior queda en 5,50 m.
# Lo que cambia es ecuatoriano: cubierta de zinc, turbinas de extraccion girando,
# el zocalo y la rampa del nivel +0,40, y la marca del agua de una creciente vieja.
PX2, MX2, BASE = 60, 170, 880
W2, H2 = int(24 * PX2 + 2 * MX2 + 360), BASE + 260
im2 = Image.new("RGB", (W2, H2), "#dfe6ea")
e = ImageDraw.Draw(im2)
Q = lambda x, z: (MX2 + x * PX2, BASE - z * PX2)


def r2(x0, z0, x1, z1, fill, out=TINTA, w=2):
    e.rectangle([Q(x0, z1), Q(x1, z0)], fill=fill, outline=out, width=w)


def t2(x, z, s, f, fill=TINTA, a="mm"):
    e.text(Q(x, z), s, font=f, fill=fill, anchor=a)


r2(-2, -0.4, 26, 0, "#9e9a92", None)                             # vereda
r2(0, 0, 24, 7.25, "#1d1b19")                                    # cuerpo negro onix
r2(0, 5.75, 7.5, 9.75, "#efe6d2")                                # segundo piso crema
for z in (0.05, 7.2):
    e.line([Q(0, z), Q(24, z)], fill=ORO, width=4)
e.line([Q(7.5, 7.25), Q(24, 7.25)], fill=ORO, width=4)

# cubierta de zinc a dos aguas asomando sobre el cuerpo
e.polygon([Q(7.5, 7.25), Q(24.5, 7.25), Q(24.5, 7.55), Q(7.5, 7.55)], fill="#8f959b", outline=TINTA)
for xx in range(0, 34):
    e.line([Q(7.5 + xx * 0.5, 7.25), Q(7.5 + xx * 0.5, 7.55)], fill="#6f767c", width=1)
e.polygon([Q(-0.5, 9.75), Q(7.8, 9.75), Q(7.8, 10.05), Q(-0.5, 10.05)], fill="#8f959b", outline=TINTA)
for xx in range(0, 17):
    e.line([Q(-0.5 + xx * 0.5, 9.75), Q(-0.5 + xx * 0.5, 10.05)], fill="#6f767c", width=1)
t2(3.6, 10.4, "cubierta de zinc a dos aguas", f_peq, TINTA)

# zona 5: turbinas eolicas de extraccion sobre la cubierta
for xx in (9.0, 12.0, 18.5, 21.5):
    e.ellipse([Q(xx - 0.45, 8.45), Q(xx + 0.45, 7.55)], fill="#b9c0c6", outline=TINTA, width=2)
    for k in range(6):
        a = k * math.pi / 3
        e.line([Q(xx, 8.0), Q(xx + 0.45 * math.cos(a), 8.0 + 0.45 * math.sin(a))], fill="#7d858c", width=2)
    r2(xx - 0.12, 7.25, xx + 0.12, 7.55, "#7d858c", None)
t2(20.0, 8.85, "turbinas de extracción de gases (zona 5)", f_peq, NUEVO)

# zocalo del nivel +0,40 y rampa de acceso
r2(0, 0, 24, 0.4, "#2f2c29", ORO, 2)
e.polygon([Q(9, 0.4), Q(14, 0.4), Q(14, 0), Q(9.0, 0)], fill="#6b645c", outline=TINTA)
e.polygon([Q(8.6, 0), Q(9, 0.4), Q(9, 0)], fill="#8a8178", outline=TINTA)
t2(11.5, 0.75, "piso interior +0,40 · rampa 1:10", f_peq, "#f0e3c2")
# canaleta de la vereda
e.line([Q(-2, -0.12), Q(26, -0.12)], fill="#6f6a63", width=5)
t2(21.0, -0.32, "canaleta perimetral (zona 4)", f_peq, "#2b2b2b")
# marca del agua de una creciente vieja
e.line([Q(0, 0.95), Q(24, 0.95)], fill="#5c6a5c", width=3)
t2(2.6, 1.18, "marca de agua", f_peq, "#9fb09f")

# ventana con rejas de la casa de Gallin
r2(2.0, 6.8, 5.5, 8.0, "#6f7c86")
for i in range(1, 9):
    xx = 2.0 + i * 3.5 / 9
    e.line([Q(xx, 6.8), Q(xx, 8.0)], fill="#2b2b2b", width=3)
# puerta peatonal y porton
r2(0.3, 0.4, 1.5, 2.8, "#2d2a27", ORO, 3)
t2(0.9, 3.15, "puerta del ochavo", f_peq, "#d4ad52")
r2(9, 0.4, 14, 4.9, "#2b2926", ORO, 3)
for k in range(1, 30):
    e.line([Q(9, 0.4 + k * 0.15), Q(14, 0.4 + k * 0.15)], fill="#403c38", width=1)
# letrero
r2(8.0, 4.9, 22.0, 6.2, "#121110", ORO, 4)
t2(15.0, 5.72, "TALLER GALLARDO", fuente("serif_bold", 58), "#d4ad52")
t2(15.0, 5.17, "SE ARREGLA TODO", fuente("serif", 24), "#d4ad52")
# el gallo: silueta metalica 2,00 x 2,20 m parada al centro del letrero. No se toca.
gx, gz = 15.0, 6.2
SIL = [(0.40, 0.00), (0.44, 0.00), (0.45, 0.18), (0.52, 0.18), (0.53, 0.00), (0.57, 0.00), (0.58, 0.22),
       (0.70, 0.30), (0.85, 0.35), (0.95, 0.50), (1.00, 0.75), (0.92, 0.95), (0.85, 0.80), (0.80, 0.98),
       (0.72, 0.78), (0.66, 0.70), (0.55, 0.62), (0.45, 0.72), (0.40, 0.86), (0.42, 0.92), (0.38, 0.97),
       (0.34, 0.93), (0.30, 0.99), (0.27, 0.93), (0.23, 0.96), (0.22, 0.89), (0.18, 0.86), (0.10, 0.83),
       (0.18, 0.80), (0.20, 0.76), (0.23, 0.70), (0.27, 0.74), (0.28, 0.62), (0.25, 0.48), (0.30, 0.34),
       (0.40, 0.24)]
e.polygon([Q(gx - 1.0 + a * 2.0, gz + b * 2.2) for a, b in SIL], fill="#c62828", outline="#ff8a80", width=3)


def cota_z(z0, z1, x, s):
    e.line([Q(x, z0), Q(x, z1)], fill=TINTA, width=1)
    for z in (z0, z1):
        e.line([Q(x - 0.2, z), Q(x + 0.2, z)], fill=TINTA, width=2)
    e.text((Q(x, (z0 + z1) / 2)[0] + 12, Q(x, (z0 + z1) / 2)[1]), s, font=f_med, fill=TINTA, anchor="lm")


cota_z(0, 0.4, 24.6, "zócalo 0,40")
cota_z(0.4, 4.9, 24.6, "portón 4,50")
cota_z(4.9, 6.2, 24.6, "letrero 1,30")
cota_z(6.2, 8.4, 24.6, "gallo 2,20 (sobresale 1,15 del techo)")
cota_z(0, 7.25, 27.2, "fachada 7,25 · no cambia")
e.text((Q(-1.2, 4.9)[0] - 12, Q(0, 4.9)[1]), "9,75 total", font=f_med, fill=TINTA, anchor="rm")
e.line([Q(-1.2, 0), Q(-1.2, 9.75)], fill=TINTA, width=1)
for z in (0, 9.75):
    e.line([Q(-1.4, z), Q(-1.0, z)], fill=TINTA, width=2)


def cota_x(x0, x1, z, s):
    e.line([Q(x0, z), Q(x1, z)], fill=TINTA, width=1)
    for x in (x0, x1):
        e.line([Q(x, z - 0.2), Q(x, z + 0.2)], fill=TINTA, width=2)
    t2((x0 + x1) / 2, z - 0.35, s, f_med)


cota_x(0, 7.5, -1.3, "casa de Gallín arriba · 7,50")
cota_x(9, 14, -1.3, "portón 5,00")
cota_x(8, 22, -2.3, "letrero 14,00")
cota_x(0, 24, -3.2, "frente 24,00 m")

e.text((MX2, 34), "TALLER GALLARDO · FACHADA A LA AV. EL CRUCE", font=f_tit, fill=TINTA)
e.text((MX2, 92), "Puerto Candela, Guayas · el gallo es una silueta de metal con tubos de neón: de día se ve rojo "
       "sin luz, de noche el neón se prende", font=f_sub, fill=TINTA)
e.text((MX2, 128), "mismo objeto, mismo lugar · el toldo de espera va en la fachada de la Calle Olmedo, no en esta",
       font=f_sub, fill=NUEVO)
im2.save(destino("03-fachada-taller.png"), optimize=True)
print("fachada ok")
