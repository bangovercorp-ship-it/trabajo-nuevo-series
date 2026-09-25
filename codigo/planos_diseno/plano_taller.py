# -*- coding: utf-8 -*-
"""Planta y fachada del Taller Gallardo, a escala. Medidas en metros.

Lote de esquina 24 x 30 m. Norte (arriba) = Av. El Cruce; oeste (izquierda) =
Jr. Los Mecanicos; sur (abajo) = Pasaje La Esperanza; este = tiendas de repuestos.
Los carros entran por la avenida y salen por el jiron: circulacion en L, sin retroceso.
"""
from PIL import Image, ImageDraw, ImageFont

F = "C:/Windows/Fonts/"
def fuente(n, s): return ImageFont.truetype(F + n, s)
f_tit, f_sub, f_zona = fuente("arialbd.ttf", 46), fuente("arial.ttf", 22), fuente("arialbd.ttf", 17)
f_med, f_peq, f_calle = fuente("arial.ttf", 15), fuente("arial.ttf", 13), fuente("arialbd.ttf", 22)

TINTA, MURO, PISO, PASILLO = "#26221e", "#3a3530", "#f4f0e6", "#e9e3d3"
ORO, BRASA, AMARILLO = "#b8923a", "#b3261e", "#e0b422"

# ================================================================== PLANTA
PX, MX, MY = 36, 170, 230
W, H = int(24 * PX + 2 * MX + 520), int(30 * PX + MY + 200)
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
    """silueta de carro visto desde arriba"""
    d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=14, fill="#cfd5dc", outline="#6b7684", width=2)
    d.rounded_rectangle([P(x0 + 1.3, y0 + 0.35), P(x1 - 1.6, y1 - 0.35)], radius=8, fill="#aeb8c4")


def moto(x, y):
    d.rounded_rectangle([P(x, y), P(x + 2.2, y + 0.7)], radius=6, fill="#c9c2b2", outline="#6b6358", width=2)


# piso y muros perimetrales
rect(0, 0, 24, 30, PISO, None)
d.polygon([P(0, 0), P(3, 0), P(0, 3)], fill="#efe7d4")                  # ochavo de esquina 3 x 3
rect(7.5, 0, 15, 21, PASILLO, None)                                      # pasillo de maniobra
rect(0, 15.8, 7.5, 21, PASILLO, None)                                    # salida al jiron
for (a, b) in [((3, 0), (9, 0)), ((14, 0), (24, 0)), ((24, 0), (24, 30)), ((0, 30), (24, 30)),
               ((0, 3), (0, 16)), ((0, 20.5), (0, 30)), ((0, 3), (3, 0))]:
    d.line([P(*a), P(*b)], fill=MURO, width=9)

# portones y puertas
d.line([P(9, 0), P(14, 0)], fill=AMARILLO, width=9)
d.line([P(0, 16), P(0, 20.5)], fill=AMARILLO, width=9)
txt(11.5, -0.9, "ENTRADA VEHICULAR · portón enrollable 5,00 × 4,50 m", f_zona, BRASA)
d.polygon([P(11.5, 1.8), P(11.0, 0.8), P(12.0, 0.8)], fill=BRASA)
cota_v(16, 20.5, -1.4, "SALIDA 4,50 × 4,50 m")
d.polygon([P(0.8, 18.25), P(1.8, 17.75), P(1.8, 18.75)], fill=BRASA)
d.line([P(11.5, 2), P(11.5, 18.2), P(2, 18.2)], fill=BRASA, width=3)     # recorrido del carro
txt(0.2, -0.9, "ingreso peatonal por el ochavo", f_peq, TINTA, "lm")

# --- bahias al este ------------------------------------------------------------
bahias = [(1.0, 5.0, "BAHÍA 1 · elevador 2 columnas"), (5.0, 9.0, "BAHÍA 2 · elevador 2 columnas"),
          (9.0, 13.5, "BAHÍA 3 · elevador 4 postes (alineación)"), (13.5, 17.0, "BAHÍA 4 · trabajo en piso"),
          (17.0, 20.5, "BAHÍA 5 · trabajo en piso")]
for y0, y1, nombre in bahias:
    rect(15, y0, 22.5, y1, "#f7f4ec", "#8a8174", 2)
    d.line([P(15, y0), P(15, y1)], fill=AMARILLO, width=4)
    carro(16.2, y0 + 0.95, 21.3, y1 - 0.35)
    txt(18.75, y0 + 0.12, nombre, f_peq, TINTA, "mt")
    if "2 columnas" in nombre:
        for yy in (y0 + 0.25, y1 - 0.55):
            rect(18.3, yy, 18.9, yy + 0.3, BRASA, None)
    if "4 postes" in nombre:
        for (xx, yy) in [(15.6, y0 + 0.25), (21.6, y0 + 0.25), (15.6, y1 - 0.55), (21.6, y1 - 0.55)]:
            rect(xx, yy, xx + 0.3, yy + 0.3, BRASA, None)
rect(22.5, 1.0, 24, 20.5, "#e7e0cf", None)
txt(23.25, 10.7, "circulación", f_peq)
cota_h(15, 22.5, 0.75, "7,50 m")
cota_v(1, 5, 14.4, "4,00")

# --- franja oeste ----------------------------------------------------------------
rect(0, 3, 7.5, 7.0, "#efe1c4")
txt(3.8, 4.4, "RECEPCIÓN Y CAJA")
txt(3.8, 5.3, "Porfirio · mostrador 3,0 m", f_peq)
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
    (1.3, 21, 5.5, 24, "#e8e1f0", "RINCÓN FINO", "Toribio · relojes"),
    (1.3, 24, 5.5, 27, "#f3e6d0", "CAFÉ", "radio · calendario"),
    (0, 27, 5.5, 30, "#dde7ec", "BAÑOS Y VESTIDOR", "2 duchas · casilleros"),
    (5.5, 21, 11.5, 30, "#f1ece0", "ZONA DE MOTOS", "4 puestos · lavadero de piezas"),
    (11.5, 21, 17, 24, "#e7ddc6", "ALMACÉN", "repuestos · estantes 3,5 m"),
    (11.5, 25, 14.5, 30, "#dcd6ca", "COMPRESOR", "a pasaje"),
    (14.5, 25, 17, 30, "#e2d8c3", "PAÑOL", "herr. pesada"),
    (17, 21, 24, 24, "#eee6d4", "ZONA DE LLANTAS", "desmontadora · balanceadora"),
]
for x0, y0, x1, y1, col, n, s in zonas_sur:
    rect(x0, y0, x1, y1, col)
    if n:
        txt((x0 + x1) / 2, (y0 + y1) / 2 - 0.35, n)
        txt((x0 + x1) / 2, (y0 + y1) / 2 + 0.45, s, f_peq)
for k in range(8):
    d.line([P(0.1, 21.3 + k * 0.7), P(1.2, 21.3 + k * 0.7)], fill=TINTA, width=2)   # escalera
txt(0.65, 26.6, "esc.", f_peq)
for i in range(4):
    moto(6.2 + (i % 2) * 2.7, 21.7 + (i // 2) * 6.6)

# estanteria de llantas sobre rieles y la puerta roja
rect(11.5, 24, 17, 25, "#d8d0bf", TINTA, 1)
for zz in (24.15, 24.85):
    d.line([P(11.5, zz), P(24, zz)], fill="#7a7266", width=2)
txt(14.25, 24.5, "riel: la estantería se corre 4,6 m", f_peq)
rect(17, 24, 24, 25, "#4a4540", TINTA, 2)
for xx in range(0, 14):
    d.ellipse([P(17.15 + xx * 0.49, 24.15), P(17.55 + xx * 0.49, 24.85)], outline="#9c948a", width=2)
txt(20.5, 23.62, "estantería sobre rieles 7 × 1 × 5 m", f_peq, TINTA)
rect(19.9, 25.0, 21.1, 25.18, BRASA, None)
rect(17, 25.18, 24, 30, "#5b1d1d", TINTA, 3)
txt(20.5, 27.1, "CUARTO DE AFINAMIENTO", f_zona, "#f4e3b0")
txt(20.5, 27.9, "7,0 × 4,8 m · techo bajo a 3,0 m", f_peq, "#f4e3b0")
txt(20.5, 25.55, "puerta roja 1,20 × 2,40", f_peq, "#f4e3b0")
rect(21.8, 29.82, 22.8, 30.0, "#8c8c8c", None)
txt(22.3, 29.4, "salida secreta", f_peq, "#f4e3b0")

# calles alrededor
txt(12, -2.4, "AV. EL CRUCE", f_calle)
txt(12, 31.2, "PASAJE LA ESPERANZA", f_calle)
capa = Image.new("RGBA", (330, 32), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((4, 2), "JR. LOS MECÁNICOS", font=f_calle, fill=TINTA)
capa = capa.rotate(90, expand=True)
im.paste(capa, (int(P(-3.3, 0)[0]), int(P(0, 6)[1])), capa)

# cotas generales
cota_h(0, 24, 32.6, "24,00 m (frente a la avenida)")
cota_v(0, 30, 25.6, "30,00 m (frente al jirón)")

# cuadro de areas y capacidad
cx = MX + 24 * PX + 140
d.text((cx, MY - 10), "CAPACIDAD", font=f_tit, fill=TINTA)
filas = ["5 bahías de 7,50 × 4,00 m", "   3 con elevador, 2 en piso", "4 puestos de motos",
         "1 o 2 carros esperando en el pasillo", "pasillo de maniobra 7,50 m",
         "", "ÁREAS", "lote: 720 m² (con ochavo)", "bahías: 150 m²", "pasillo y salida: 185 m²",
         "Cuarto de Afinamiento: 34 m²", "almacén + pañol + compresor: 44 m²",
         "", "ALTURAS", "primer piso: 5,50 m libres", "Cuarto: cielo raso a 3,00 m",
         "segundo piso (casa de Gallín): sobre", "la franja oeste, 7,5 × 21 m, 3,00 m"]
for i, s in enumerate(filas):
    fnt = f_zona if s in ("ÁREAS", "ALTURAS") else f_sub
    d.text((cx, MY + 60 + i * 34), s, font=fnt, fill=TINTA)

d.text((MX, 40), "TALLER GALLARDO · PLANTA DEL PRIMER PISO", font=f_tit, fill=TINTA)
d.text((MX, 100), "escala gráfica · medidas en metros · norte arriba · entran por la avenida, salen por el jirón",
       font=f_sub, fill=TINTA)
ex, ey = MX, H - 70
d.rectangle([ex, ey, ex + 5 * PX, ey + 12], fill=TINTA)
d.rectangle([ex + 5 * PX, ey, ex + 10 * PX, ey + 12], fill="#ffffff", outline=TINTA, width=2)
for m in (0, 5, 10):
    d.text((ex + m * PX, ey + 28), "%d m" % m, font=f_peq, fill=TINTA, anchor="mm")
im.save(r"C:\pesonajes para videos\planos_diseno\02-planta-taller.png", optimize=True)

# ================================================================== FACHADA
PX2, MX2, BASE = 60, 150, 830
W2, H2 = int(24 * PX2 + 2 * MX2 + 330), BASE + 240
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
# ventana con rejas de la casa de Gallin
r2(2.0, 6.8, 5.5, 8.0, "#6f7c86")
for i in range(1, 9):
    xx = 2.0 + i * 3.5 / 9
    e.line([Q(xx, 6.8), Q(xx, 8.0)], fill="#2b2b2b", width=3)
# puerta peatonal y porton
r2(0.3, 0, 1.5, 2.4, "#2d2a27", ORO, 3)
t2(0.9, 2.75, "puerta en el ochavo", f_peq, "#d4ad52")
r2(9, 0, 14, 4.5, "#2b2926", ORO, 3)
for k in range(1, 30):
    e.line([Q(9, k * 0.15), Q(14, k * 0.15)], fill="#403c38", width=1)
# letrero
r2(8.0, 4.9, 22.0, 6.2, "#121110", ORO, 4)
t2(15.0, 5.72, "TALLER GALLARDO", fuente("georgiab.ttf", 58), "#d4ad52")
t2(15.0, 5.17, "SE ARREGLA TODO", fuente("georgia.ttf", 24), "#d4ad52")
# el gallo: silueta metalica 2,00 x 2,20 m parada al centro del letrero
gx, gz = 15.0, 6.2
# silueta normalizada (0..1), mirando a la izquierda y cantando; se escala a 2,00 x 2,20 m
SIL = [(0.40, 0.00), (0.44, 0.00), (0.45, 0.18), (0.52, 0.18), (0.53, 0.00), (0.57, 0.00), (0.58, 0.22),
       (0.70, 0.30), (0.85, 0.35), (0.95, 0.50), (1.00, 0.75), (0.92, 0.95), (0.85, 0.80), (0.80, 0.98),
       (0.72, 0.78), (0.66, 0.70), (0.55, 0.62), (0.45, 0.72), (0.40, 0.86), (0.42, 0.92), (0.38, 0.97),
       (0.34, 0.93), (0.30, 0.99), (0.27, 0.93), (0.23, 0.96), (0.22, 0.89), (0.18, 0.86), (0.10, 0.83),
       (0.18, 0.80), (0.20, 0.76), (0.23, 0.70), (0.27, 0.74), (0.28, 0.62), (0.25, 0.48), (0.30, 0.34),
       (0.40, 0.24)]
e.polygon([Q(gx - 1.0 + a * 2.0, gz + b * 2.2) for a, b in SIL], fill="#c62828", outline="#ff8a80", width=3)

# cotas de altura a la derecha
def cota_z(z0, z1, x, s):
    e.line([Q(x, z0), Q(x, z1)], fill=TINTA, width=1)
    for z in (z0, z1):
        e.line([Q(x - 0.2, z), Q(x + 0.2, z)], fill=TINTA, width=2)
    e.text((Q(x, (z0 + z1) / 2)[0] + 12, Q(x, (z0 + z1) / 2)[1]), s, font=f_med, fill=TINTA, anchor="lm")

cota_z(0, 4.5, 24.6, "portón 4,50")
cota_z(4.9, 6.2, 24.6, "letrero 1,30")
cota_z(6.2, 8.4, 24.6, "gallo 2,20 (sobresale 1,15 del techo)")
cota_z(0, 7.25, 26.6, "fachada 7,25")
cota_z(0, 9.75, -1.2, "")
e.text((Q(-1.2, 4.9)[0] - 12, Q(0, 4.9)[1]), "9,75 total", font=f_med, fill=TINTA, anchor="rm")
# cotas horizontales abajo
def cota_x(x0, x1, z, s):
    e.line([Q(x0, z), Q(x1, z)], fill=TINTA, width=1)
    for x in (x0, x1):
        e.line([Q(x, z - 0.2), Q(x, z + 0.2)], fill=TINTA, width=2)
    t2((x0 + x1) / 2, z - 0.35, s, f_med)

cota_x(0, 7.5, -1.1, "casa de Gallín arriba · 7,50")
cota_x(9, 14, -1.1, "portón 5,00")
cota_x(8, 22, -2.1, "letrero 14,00")
cota_x(0, 24, -3.0, "frente 24,00 m")

e.text((MX2, 40), "TALLER GALLARDO · FACHADA A LA AV. EL CRUCE", font=f_tit, fill=TINTA)
e.text((MX2, 100), "el gallo es una silueta de metal con tubos de neón: de día se ve rojo sin luz, de noche el neón "
       "se prende · mismo objeto, mismo lugar", font=f_sub, fill=TINTA)
im2.save(r"C:\pesonajes para videos\planos_diseno\03-fachada-taller.png", optimize=True)
print("ok")
