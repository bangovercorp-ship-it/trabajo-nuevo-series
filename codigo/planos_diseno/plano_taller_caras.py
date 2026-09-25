# -*- coding: utf-8 -*-
"""Las cuatro caras del Taller Gallardo y su cubierta. Medidas en metros.

Existe para que ningun plano de ningun episodio tenga que inventar un lado.
Hasta ahora solo estaba dibujada la cara norte (la de la avenida, que es la imagen
insignia). Las otras tres y el techo se resolvian de memoria, y eso es justo lo que
hace que un escenario cambie de un video a otro.

Orientacion del lote (la misma de la planta): x = 0 en la Calle Olmedo y 24 en la
medianera del este; y = 0 en la Av. El Cruce y 30 en el Pasaje La Esperanza.

Como se lee cada elevacion, y por que:
  NORTE  Av. El Cruce      24 m   x 0 a la izquierda  (igual que 03-fachada-taller)
  OESTE  Calle Olmedo      30 m   y 0 a la izquierda  (el ochavo pega con el norte)
  SUR    Pasaje            24 m   x 0 a la izquierda  (igual que el plano del pasaje)
  ESTE   medianera ciega   30 m   y 30 a la izquierda (se ve espejado, y se dice)

PROPUESTA DE MATERIALES POR CARA. La biblia define el negro onix para la fachada de
la avenida. Las otras tres nunca se definieron, y hay que decidirlas o alguien las
inventa. Lo que se propone, y que es como se comporta un negocio de barrio de verdad:
el onix envuelve las DOS caras de calle (norte y oeste), porque son las que el cliente
ve al llegar a la esquina y porque el neon de noche necesita esa envolvente; la cara
del pasaje queda en bloque enlucido sin pintar, gris cemento, que es lo que se hace
cuando nadie la mira; y la del este es medianera compartida con los almacenes de
repuestos, sin acabado.

VALIDAR: retiros municipales (el toldo ocupa retiro), anclaje del gallo en zona
sismica y de viento, y el tramite del ducto de residuos.
"""
import math

from PIL import Image, ImageDraw

from comun import (AGUA, BLOQUE, BRASA, CREMA, Elevacion, NUEVO, ONIX, ORO,
                   TINTA, VEREDA, ZINC, destino, fuente)

f_tit, f_sub = fuente("sans_bold", 40), fuente("sans", 20)
f_cara, f_med, f_peq, f_min = fuente("sans_bold", 26), fuente("sans", 15), fuente("sans", 13), fuente("sans", 11)

PX = 26                       # pixeles por metro
MAR = 90                      # aire entre paneles
COL = 30 * PX                 # el panel mas ancho: 30 m
W = 2 * COL + 3 * MAR + 120
H = 1840
im = Image.new("RGB", (W, H), "#dfe6ea")
d = ImageDraw.Draw(im)


FUENTES = {"cara": f_cara, "med": f_med, "peq": f_peq, "min": f_min}


class Cara(Elevacion):
    """el taller: cuerpo de 7,25 m, con o sin el ónix de las caras de calle"""

    def __init__(self, ox, oy, largo, titulo, sub):
        super().__init__(d, ox, oy, largo, PX, titulo, sub, FUENTES)

    def base(self, onix):
        super().base(ONIX if onix else BLOQUE, 7.25, filete=onix,
                     zocalo="#2f2c29" if onix else "#8f8a80")

    def zinc(self, z0=7.25, z1=7.55, x0=None, x1=None):
        super().zinc(z0, z1, x0, x1)

    def turbina(self, x, z0=7.55):
        super().turbina(x, z0)


FIL1, FIL2 = 530, 960

# ============================================================ NORTE · Av. El Cruce
n = Cara(MAR, FIL1, 24, "NORTE · AV. EL CRUCE", "la imagen insignia · 24,00 m · negro ónix")
n.base(onix=True)
n.r(0, 5.75, 7.5, 9.75, CREMA)                                  # casa de Gallin
n.zinc(x0=7.5)
n.zinc(9.75, 10.05, 0, 7.5)
for xx in (9, 12, 18.5, 21.5):
    n.turbina(xx)
n.r(2.0, 6.8, 5.5, 8.0, "#6f7c86")
for i in range(1, 9):
    xx = 2.0 + i * 3.5 / 9
    d.line([n.Q(xx, 6.8), n.Q(xx, 8.0)], fill="#2b2b2b", width=2)
n.r(0.3, 0.4, 1.5, 2.8, "#2d2a27", ORO, 2)
n.r(9, 0.4, 14, 4.9, "#2b2926", ORO, 2)
for k in range(1, 22):
    d.line([n.Q(9, 0.4 + k * 0.2), n.Q(14, 0.4 + k * 0.2)], fill="#403c38", width=1)
n.r(8.0, 4.9, 22.0, 6.2, "#121110", ORO, 3)
n.t(15.0, 5.72, "TALLER GALLARDO", fuente("serif_bold", 26), "#d4ad52")
n.t(15.0, 5.2, "SE ARREGLA TODO", fuente("serif", 12), "#d4ad52")
SIL = [(0.40, 0.00), (0.44, 0.00), (0.45, 0.18), (0.52, 0.18), (0.53, 0.00), (0.57, 0.00), (0.58, 0.22),
       (0.70, 0.30), (0.85, 0.35), (0.95, 0.50), (1.00, 0.75), (0.92, 0.95), (0.85, 0.80), (0.80, 0.98),
       (0.72, 0.78), (0.66, 0.70), (0.55, 0.62), (0.45, 0.72), (0.40, 0.86), (0.42, 0.92), (0.38, 0.97),
       (0.34, 0.93), (0.30, 0.99), (0.27, 0.93), (0.23, 0.96), (0.22, 0.89), (0.18, 0.86), (0.10, 0.83),
       (0.18, 0.80), (0.20, 0.76), (0.23, 0.70), (0.27, 0.74), (0.28, 0.62), (0.25, 0.48), (0.30, 0.34),
       (0.40, 0.24)]
d.polygon([n.Q(15.0 - 1.0 + a * 2.0, 6.2 + b * 2.2) for a, b in SIL], fill="#c62828", outline="#ff8a80", width=2)
n.t(11.5, 0.72, "rampa 1:10 · piso +0,40", f_min, "#f0e3c2")
n.cota_x(0, 24, -1.5, "24,00 m")
n.cota_z(0, 7.25, 25.0, "7,25")
n.rotulo()

# ============================================================ SUR · Pasaje
s = Cara(MAR + COL + MAR, FIL1, 24, "SUR · PASAJE LA ESPERANZA",
         "espalda · 24,00 m · bloque enlucido sin pintar (propuesta)")
s.base(onix=False)
s.zinc()
for xx in (9, 12, 18.5, 21.5):
    s.turbina(xx)
s.r(21.8, 0.4, 22.8, 2.5, "#8c8c8c", TINTA, 2)
s.t(22.3, 2.85, "puerta gris sin manija", f_min, BRASA)
s.t(22.3, 3.3, "salida secreta del Cuarto", f_min, BRASA)
s.r(12.5, 2.2, 13.5, 2.8, "#3f3f3f", TINTA, 2)
s.t(13.0, 3.15, "rejilla del compresor", f_min, NUEVO)
s.r(0.3, 2.6, 2.8, 3.1, "#2f5aa0", "#ffffff", 2)
s.t(1.55, 2.85, "letrero", f_min, "#ffffff")
for xx in (5.5, 17.0):                                          # bajantes de la cubierta
    s.r(xx, 0.4, xx + 0.16, 7.25, "#7e786d", None)
s.t(5.6, 4.2, "bajante", f_min, TINTA, "lm")
s.t(12, 6.2, "MURO CIEGO: aquí no hay ventanas ni vanos", f_peq, "#4b463e")
s.t(12, 5.6, "solo la puerta gris y la rejilla del compresor", f_peq, "#4b463e")
s.cota_x(0, 24, -1.5, "24,00 m")
s.cota_z(0, 7.25, 25.0, "7,25")
s.rotulo()

# ============================================================ OESTE · Calle Olmedo
o = Cara(MAR, FIL2, 30, "OESTE · CALLE OLMEDO",
         "la cara larga · 30,00 m · el ónix envuelve la esquina (propuesta)")
o.base(onix=True)
o.r(0, 5.75, 21, 9.75, CREMA)                                   # la casa de Gallin corre 21 m
o.zinc(x0=21)
o.zinc(9.75, 10.05, 0, 21)
for yy in (6, 12, 18):
    o.turbina(yy + 3)
o.r(0, 0.4, 3.0, 7.25, "#2a2724", None)                         # ochavo visto de canto
d.line([o.Q(3.0, 0.4), o.Q(3.0, 7.25)], fill=ORO, width=2)
o.t(1.5, 3.6, "ochavo", f_min, "#d4ad52")
o.r(16, 0.4, 20.5, 4.9, "#2b2926", ORO, 2)                      # porton de salida
for k in range(1, 22):
    d.line([o.Q(16, 0.4 + k * 0.2), o.Q(20.5, 0.4 + k * 0.2)], fill="#403c38", width=1)
o.t(18.25, 5.35, "PORTÓN DE SALIDA 4,50 × 4,50", f_min, BRASA)
o.t(18.25, 0.72, "rampa 1:10", f_min, "#f0e3c2")
for (a, b) in [(3.5, 6.5), (8.0, 11.0), (13.0, 16.0)]:          # ventanas de la casa
    o.r(a, 6.8, b, 8.4, "#6f7c86")
    for i in range(1, 7):
        xx = a + i * (b - a) / 7
        d.line([o.Q(xx, 6.8), o.Q(xx, 8.4)], fill="#2b2b2b", width=2)
o.t(9.5, 8.75, "casa de Gallín: 21,00 m de largo sobre esta cara", f_peq, TINTA)
for k in range(13):                                             # toldo de espera, en el retiro
    d.line([o.Q(3 + k, 3.2), o.Q(3 + k, 3.2)], fill=NUEVO, width=1)
d.line([o.Q(3, 3.2), o.Q(15, 3.2)], fill=NUEVO, width=4)
for xx in (3, 15):
    d.line([o.Q(xx, 0), o.Q(xx, 3.2)], fill=NUEVO, width=4)
o.t(9, 2.7, "TOLDO DE ESPERA · 12 × 5 m · ocupa retiro · VALIDAR", f_min, NUEVO)
o.r(23, 0.4, 23.16, 7.25, "#7e786d", None)
o.t(26.5, 3.6, "aquí ya es\nel pasaje", f_min, TINTA)
o.cota_x(0, 30, -1.5, "30,00 m")
o.cota_z(0, 9.75, 31.0, "9,75 con la casa")
o.rotulo()

# ============================================================ ESTE · medianera
e = Cara(MAR + COL + MAR, FIL2, 30, "ESTE · MEDIANERA",
         "ciega · 30,00 m · se lee espejada: el pasaje a la izquierda, la avenida a la derecha")
e.base(onix=False)
e.zinc()
e.r(9, 5.75, 30, 9.75, "#e4dbc6")                                # la casa asoma DETRAS
e.zinc(9.75, 10.05, 9, 30)
for yy in (12, 18, 24):
    e.turbina(yy)
for k in range(0, 60):                                          # hachurado de medianera
    d.line([e.Q(k * 0.5, 0.4), e.Q(k * 0.5 + 0.28, 1.1)], fill="#a39d90", width=1)
e.t(15, 3.6, "MEDIANERA COMPARTIDA CON LOS ALMACENES DE REPUESTOS", f_peq, "#4b463e")
e.t(15, 4.2, "sin acabado, sin vanos · nunca se ve desde la calle", f_peq, "#4b463e")
e.t(15, 2.6, "solo aparece en tomas aéreas de la manzana", f_min, BRASA)
e.t(20, 8.6, "detrás asoma la casa de Gallín, que está en la cara opuesta", f_min, "#6b6250")
e.cota_x(0, 30, -1.5, "30,00 m")
e.cota_z(0, 7.25, 31.0, "7,25")
e.rotulo()

# ============================================================ CUBIERTA
CX, CY, CP = MAR + 60, 1240, 18
R = lambda x0, y0, x1, y1, f=None, ou=TINTA, w=2: d.rectangle(
    [(CX + x0 * CP, CY + y0 * CP), (CX + x1 * CP, CY + y1 * CP)], fill=f, outline=ou, width=w)
TC = lambda x, y, s, f=f_peq, c=TINTA, a="mm": d.text((CX + x * CP, CY + y * CP), s, font=f, fill=c, anchor=a)

d.text((CX, CY - 168), "CUBIERTA · PLANTA DE TECHOS", font=f_cara, fill=TINTA)
d.text((CX, CY - 134), "24 × 30 m · lo que ve un dron o una toma desde el Cerro El Mirador", font=f_peq, fill=TINTA)
R(0, 0, 24, 30, ZINC)
for k in range(0, 49):                                          # nervaduras del zinc
    d.line([(CX + k * 0.5 * CP, CY), (CX + k * 0.5 * CP, CY + 30 * CP)], fill="#6f767c", width=1)
R(0, 0, 7.5, 21, "#c9c3b6")                                     # techo de la casa, 2,50 m mas alto
TC(3.75, 8.6, "TECHO DE", f_min)
TC(3.75, 9.7, "LA CASA", f_min)
TC(3.75, 10.8, "+9,75", f_min)
d.line([(CX, CY + 15 * CP), (CX + 24 * CP, CY + 15 * CP)], fill="#5c6369", width=4)
TC(19, 14.4, "cumbrera", f_min)
for yy in (4, 11, 18, 25):                                      # tragaluces
    R(9, yy, 22, yy + 1.2, "#eef3f7", "#8f959b", 2)
TC(15.5, 4.6, "tragaluz", f_min, "#5c6369")
for (xx, yy) in [(9, 6), (12, 14), (18.5, 6), (21.5, 14)]:      # turbinas
    d.ellipse([(CX + (xx - 0.45) * CP, CY + (yy - 0.45) * CP), (CX + (xx + 0.45) * CP, CY + (yy + 0.45) * CP)],
              fill="#b9c0c6", outline=TINTA, width=2)
TC(12, 15.9, "4 turbinas eólicas de extracción", f_min, NUEVO)
for yy in (0, 30):                                              # canaletas
    d.line([(CX, CY + yy * CP), (CX + 24 * CP, CY + yy * CP)], fill="#6f6a63", width=5)
for (xx, yy) in [(5.5, 30), (17, 30), (23.1, 0)]:
    d.ellipse([(CX + (xx - 0.3) * CP, CY + (yy - 0.3) * CP), (CX + (xx + 0.3) * CP, CY + (yy + 0.3) * CP)],
              fill="#7e786d", outline=TINTA, width=2)
TC(11, 29.2, "canaleta y bajantes", f_min, "#3a352e")
d.polygon([(CX + 15 * CP, CY - 0.2 * CP), (CX + 14.2 * CP, CY - 2.4 * CP), (CX + 15.8 * CP, CY - 2.4 * CP)],
          fill="#c62828", outline=TINTA)
TC(15, -3.4, "el gallo sobresale 1,15 m", f_min, BRASA)
TC(12, 31.4, "PASAJE LA ESPERANZA", f_peq)
TC(12, -5.4, "AV. EL CRUCE", f_peq)

# ============================================================ cuadro de materiales
qx = CX + 24 * CP + 120
d.text((qx, CY - 168), "PROPUESTA DE MATERIALES POR CARA", font=f_cara, fill=NUEVO)
d.text((qx, CY - 134), "La biblia solo definía la cara de la avenida. Las otras tres se deciden aquí.",
       font=f_peq, fill=TINTA)
bloques = [
    ("NORTE · avenida", ONIX, ["Negro ónix mate, filete dorado arriba y abajo.",
                               "Letrero, gallo de neón y portón de entrada.",
                               "Es la imagen insignia de la serie."]),
    ("OESTE · Calle Olmedo", ONIX, ["Negro ónix también: el ónix envuelve la esquina.",
                                    "Portón de salida, ochavo, y los 21 m de la casa",
                                    "de Gallín en crema sobre el ónix."]),
    ("SUR · pasaje", "#5b564d", ["Bloque de cemento enlucido SIN PINTAR, gris.",
                                 "Nadie lo mira, y eso es exactamente lo que",
                                 "cuenta de un taller de barrio."]),
    ("ESTE · medianera", "#5b564d", ["Sin acabado. Muro compartido con los almacenes",
                                     "de repuestos. Solo aparece en tomas aéreas."]),
    ("CUBIERTA", "#5b564d", ["Zinc o galvalume a dos aguas, 4 tragaluces y",
                             "4 turbinas. Es lo que se ve desde el Cerro."]),
    ("LAS CUATRO", NUEVO, ["Zócalo del nivel +0,40 y la marca de agua de una",
                           "creciente vieja a 0,95 m. Canaleta perimetral al pie."]),
]
yy = CY - 88
for titulo, col, lineas in bloques:
    d.text((qx, yy), titulo, font=fuente("sans_bold", 18), fill=col)
    yy += 26
    for ln in lineas:
        d.text((qx + 10, yy), ln, font=f_peq, fill=TINTA)
        yy += 21
    yy += 14

d.text((MAR, 44), "TALLER GALLARDO · LAS CUATRO CARAS Y LA CUBIERTA", font=f_tit, fill=TINTA)
d.text((MAR, 96), "Puerto Candela, Guayas · escala gráfica · medidas en metros · nivel +0,40 sobre la vereda en las cuatro",
       font=f_sub, fill=TINTA)
d.text((MAR, 128), "Existe para que ningún plano de ningún episodio tenga que inventar un lado.",
       font=f_sub, fill=NUEVO)
ex, ey = MAR + 700, H - 120
d.rectangle([ex, ey, ex + 5 * PX, ey + 12], fill=TINTA)
d.rectangle([ex + 5 * PX, ey, ex + 10 * PX, ey + 12], fill="#ffffff", outline=TINTA, width=2)
for m in (0, 5, 10):
    d.text((ex + m * PX, ey + 28), "%d m" % m, font=f_peq, fill=TINTA, anchor="mm")
im.save(destino("07-taller-cuatro-caras.png"), optimize=True)
print("cuatro caras ok")
