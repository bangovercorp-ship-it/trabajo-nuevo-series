# -*- coding: utf-8 -*-
"""Las cuatro caras del Bar La Gata y su cubierta. Medidas en metros.

El mismo problema que tenia el taller: solo estaba dibujada la fachada de la avenida,
y las otras tres se resolvian de memoria. Aqui quedan fijadas.

Orientacion del lote (la misma de la planta del bar): x = 0 en la Calle Olmedo y 12
en la medianera del este; y = 0 al fondo de la manzana y 20 en la Av. El Cruce. El
ochavo de 2 x 2 m esta en la esquina suroeste, que es Calle Olmedo con la avenida,
mirando en diagonal al taller.

Como se lee cada elevacion:
  SUR    Av. El Cruce      12 m   x 0 a la izquierda  (igual que 05-fachada-bar)
  OESTE  Calle Olmedo      20 m   y 0 a la izquierda, la avenida al fondo derecha
  NORTE  fondo de manzana  12 m   x 0 a la izquierda
  ESTE   medianera ciega   20 m   se lee espejada: la avenida a la izquierda

PROPUESTA DE MATERIALES POR CARA. La biblia define el verde botella con cornisas
crema para la fachada de la avenida, y nada mas. Se propone la misma logica que en el
taller: el verde ENVUELVE LA ESQUINA y cubre tambien la Calle Olmedo, porque son las
dos caras que se ven desde la esquina y porque los dos neones, el gallo y la gata,
tienen que leerse juntos desde ahi; el fondo queda en bloque enlucido sin pintar; y
el este es medianera con el vecino de la Mz. H.

Lo ecuatoriano que aparece en las caras de servicio y que no estaba en ningun plano:
el tanque de agua elevado en la cubierta, el tendedero de Micaela, la campana de
extraccion de la cocina y rejas en todas las ventanas.

VALIDAR: retiros municipales y si el cabildo permite el volado del balcon sobre la
vereda.
"""
from PIL import Image, ImageDraw

from comun import (AGUA, BLOQUE, BRASA, CREMA, Elevacion, GATA, NUEVO, ORO, TINTA,
                   VEREDA, VERDE_BAR, ZINC, destino, fuente)

f_tit, f_sub = fuente("sans_bold", 40), fuente("sans", 20)
f_cara, f_med = fuente("sans_bold", 26), fuente("sans", 15)
f_peq, f_min = fuente("sans", 13), fuente("sans", 11)
FUENTES = {"cara": f_cara, "med": f_med, "peq": f_peq, "min": f_min}

PX, MAR = 30, 90
COL = 20 * PX
W = 2 * COL + 3 * MAR + 140
H = 1800
im = Image.new("RGB", (W, H), "#dfe6ea")
d = ImageDraw.Draw(im)

MADERA, VIDRIO = "#4a2e1f", "#c8d4d6"


class Cara(Elevacion):
    """el bar: dos pisos, 7,50 m en total; 3,60 abajo y 3,00 arriba"""

    def __init__(self, ox, oy, largo, titulo, sub):
        super().__init__(d, ox, oy, largo, PX, titulo, sub, FUENTES)

    def base(self, verde):
        super().base(VERDE_BAR if verde else BLOQUE, 7.5, filete=False,
                     zocalo="#16382a" if verde else "#8f8a80")
        if verde:                                        # cornisas crema
            for z in (3.6, 3.9, 6.9, 7.45):
                self.r(-0.15, z, self.largo + 0.15, z + 0.1, CREMA, None)

    def ventana(self, x0, z0, x1, z1, con_reja=True):
        self.r(x0, z0, x1, z1, "#3a2a1e", CREMA, 2)
        self.r(x0 + 0.12, z0 + 0.12, x1 - 0.12, z1 - 0.12, "#5d6f7a", None)
        if con_reja:
            self.reja(x0 + 0.2, z0 + 0.1, x1 - 0.1, z1 - 0.1, 0.24, "#cfd6cf")


FIL1, FIL2 = 520, 940

# ============================================================ SUR · Av. El Cruce
s = Cara(MAR, FIL1, 12, "SUR · AV. EL CRUCE",
         "la fachada · 12,00 m · verde botella, cornisas crema · mira al taller")
s.base(verde=True)
s.zinc(7.5, 7.8)
s.r(0, 0.4, 2.0, 7.5, "#18402f", None)                            # ochavo de canto
d.line([s.Q(2.0, 0.4), s.Q(2.0, 7.5)], fill=CREMA, width=2)
s.t(1.0, 4.4, "ochavo", f_min, CREMA)
s.r(3.5, 0.4, 4.7, 3.0, MADERA, CREMA, 2)                          # puerta, abierta de par en par
s.r(3.6, 1.8, 4.6, 2.9, VIDRIO, None)
s.t(4.1, 0.75, "puerta 1,20 × 2,60", f_min, CREMA)
s.r(6.5, 1.3, 11, 3.2, "#e3a07a", CREMA, 3)                        # vitrina con luz de adentro
for xx in (8.0, 9.5):
    d.line([s.Q(xx, 1.3), s.Q(xx, 3.2)], fill=CREMA, width=3)
s.reja(6.6, 1.3, 7.5, 3.2, 0.05, "#9fb0a6")                        # reja corrediza, recogida
s.t(7.0, 0.95, "reja recogida", f_min, NUEVO)
s.r(6.4, 3.22, 11.1, 3.4, "#7b8288", CREMA, 2)
s.t(8.75, 3.55, "portón enrollable recogido", f_min, CREMA)
s.r(3.6, 3.9, 8.4, 4.45, "#2a1a24", GATA, 2)                       # neon 4,80 x 0,55
s.t(6.0, 4.17, "LA GATA  ·  neón 4,80 × 0,55", f_min, GATA)
for x0 in (3.8, 6.4):                                              # ventanas primero...
    s.ventana(x0, 4.75, x0 + 1.8, 6.8, con_reja=False)
s.ventana(10.0, 5.2, 11.2, 6.7)
s.r(3.0, 4.75, 9.0, 5.9, None, MADERA, 4)                          # ...y el balcón DELANTE
for i in range(1, 17):
    xx = 3.0 + i * 6.0 / 17
    d.line([s.Q(xx, 4.75), s.Q(xx, 5.9)], fill=MADERA, width=3)
s.t(6.0, 7.12, "balcón de Micaela · mira de frente al gallo", f_min, CREMA)
s.cota_x(0, 12, -1.5, "12,00 m")
s.cota_z(0, 7.5, 13.0, "7,50")
s.rotulo()

# ============================================================ NORTE · fondo
n = Cara(MAR + COL + MAR, FIL1, 12, "NORTE · FONDO DE MANZANA",
         "servicio · 12,00 m · bloque enlucido sin pintar (propuesta)")
n.base(verde=False)
n.zinc(7.5, 7.8)
n.r(9.3, 0.4, 11.5, 2.9, "#6b6259", TINTA, 2)                      # porton del patio
for k in range(1, 13):
    d.line([n.Q(9.3, 0.4 + k * 0.2), n.Q(11.5, 0.4 + k * 0.2)], fill="#544c44", width=1)
n.t(10.4, 3.25, "portón del patio · entra el hielo", f_min, BRASA)
n.ventana(1.2, 1.9, 2.4, 2.9)
n.t(1.8, 3.25, "cocina", f_min)
n.r(2.9, 2.6, 3.9, 3.4, "#4a4a4a", TINTA, 2)                       # campana de la cocina
n.r(3.2, 3.4, 3.6, 5.4, "#4a4a4a", None)
n.t(3.4, 5.75, "campana de extracción", f_min, NUEVO)
for x0 in (5.6, 7.6):
    n.ventana(x0, 4.6, x0 + 1.4, 6.3)
n.t(6.8, 6.75, "dormitorio y baño de Micaela", f_min, "#4b463e")
n.r(0.3, 0.4, 0.46, 7.5, "#7e786d", None)
n.t(0.5, 4.0, "bajante", f_min, TINTA, "lm")
n.t(4.6, 0.72, "MURO DE SERVICIO · nunca se filma de frente", f_min, "#4b463e")
n.cota_x(0, 12, -1.5, "12,00 m")
n.cota_z(0, 7.5, 13.0, "7,50")
n.rotulo()

# ============================================================ OESTE · Calle Olmedo
o = Cara(MAR, FIL2, 20, "OESTE · CALLE OLMEDO",
         "la cara larga · 20,00 m · el verde envuelve la esquina (propuesta)")
o.base(verde=True)
o.zinc(7.5, 7.8)
o.r(18, 0.4, 20, 7.5, "#18402f", None)                             # el ochavo, al fondo derecha
d.line([o.Q(18, 0.4), o.Q(18, 7.5)], fill=CREMA, width=2)
o.t(19, 4.4, "ochavo", f_min, CREMA)
o.r(4.5, 0.4, 5.7, 2.9, MADERA, CREMA, 2)                          # entrega de bebidas al deposito
o.t(5.1, 3.9, "entrega de bebidas · al depósito", f_min, CREMA)
o.ventana(1.4, 1.6, 2.6, 2.9)
o.t(2.0, 3.3, "cocina", f_min, CREMA)
for x0 in (2.5, 7.0, 11.5, 15.0):                                  # ventanas del piso de Micaela
    o.ventana(x0, 4.6, x0 + 2.0, 6.5)
o.t(10, 7.15, "el piso de Micaela: cuatro ventanas con reja a la Calle Olmedo", f_min, CREMA)
o.r(13.4, 0.4, 13.56, 7.5, "#7e786d", None)
o.t(17.8, 1.35, "la avenida →", f_min, CREMA, "rm")
o.cota_x(0, 20, -1.5, "20,00 m")
o.cota_z(0, 7.5, 21.0, "7,50")
o.rotulo()

# ============================================================ ESTE · medianera
e = Cara(MAR + COL + MAR, FIL2, 20, "ESTE · MEDIANERA",
         "ciega · 20,00 m · se lee espejada: la avenida a la izquierda")
e.base(verde=False)
e.zinc(7.5, 7.8)
for k in range(0, 41):
    d.line([e.Q(k * 0.5, 0.4), e.Q(k * 0.5 + 0.28, 1.2)], fill="#a39d90", width=1)
e.t(10, 4.2, "MEDIANERA COMPARTIDA CON EL VECINO DE LA Mz. H", f_peq, "#4b463e")
e.t(10, 3.6, "sin acabado, sin vanos", f_peq, "#4b463e")
e.t(10, 2.6, "solo aparece en tomas aéreas de la manzana", f_min, BRASA)
e.cota_x(0, 20, -1.5, "20,00 m")
e.cota_z(0, 7.5, 21.0, "7,50")
e.rotulo()

# ============================================================ CUBIERTA
CX, CY, CP = MAR + 40, 1230, 22
R = lambda x0, y0, x1, y1, f=None, ou=TINTA, w=2: d.rectangle(
    [(CX + x0 * CP, CY + y0 * CP), (CX + x1 * CP, CY + y1 * CP)], fill=f, outline=ou, width=w)
TC = lambda x, y, s, f=f_peq, c=TINTA, a="mm": d.text((CX + x * CP, CY + y * CP), s, font=f, fill=c, anchor=a)

d.text((CX, CY - 150), "CUBIERTA · PLANTA DE TECHOS", font=f_cara, fill=TINTA)
d.text((CX, CY - 116), "12 × 20 m · lo que ve un dron sobre la esquina", font=f_peq, fill=TINTA)
R(0, 0, 12, 20, ZINC)
for k in range(0, 25):
    d.line([(CX + k * 0.5 * CP, CY), (CX + k * 0.5 * CP, CY + 20 * CP)], fill="#6f767c", width=1)
d.line([(CX + 6 * CP, CY), (CX + 6 * CP, CY + 20 * CP)], fill="#5c6369", width=4)
TC(6, 1.0, "cumbrera", f_min)
R(0.6, 1.2, 2.6, 3.2, "#9fb3bd")                                   # tanque de agua elevado
TC(1.6, 4.0, "tanque de agua", f_min, NUEVO)
TC(1.6, 4.8, "elevado", f_min, NUEVO)
for k in range(4):                                                 # tendedero de Micaela
    d.line([(CX + 8 * CP, CY + (2.2 + k * 0.7) * CP), (CX + 11.4 * CP, CY + (2.2 + k * 0.7) * CP)],
           fill="#cfcabd", width=3)
TC(9.7, 5.4, "tendedero", f_min, NUEVO)
R(3, 20, 9, 21.2, "#6b4a2e", TINTA, 2)                             # balcon volado sobre la vereda
TC(6, 21.9, "balcón volado 1,20 m · VALIDAR con el cabildo", f_min, BRASA)
R(3.6, 20.1, 8.4, 20.5, "#2a1a24", GATA, 2)
TC(11.0, 20.6, "neón", f_min, GATA)
for (xx, yy) in [(0.3, 0.3), (11.7, 0.3), (0.3, 19.7), (11.7, 19.7)]:
    d.ellipse([(CX + (xx - 0.3) * CP, CY + (yy - 0.3) * CP), (CX + (xx + 0.3) * CP, CY + (yy + 0.3) * CP)],
              fill="#7e786d", outline=TINTA, width=2)
TC(6, 18.6, "canaleta perimetral y cuatro bajantes", f_min, "#3a352e")
TC(6, -1.1, "fondo de la Mz. H", f_min)
TC(6, 23.2, "AV. EL CRUCE", f_peq)
capa = Image.new("RGBA", (220, 26), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((2, 2), "CALLE OLMEDO", font=f_peq, fill=TINTA)
capa = capa.rotate(90, expand=True)
im.paste(capa, (int(CX - 2.4 * CP), int(CY + 7 * CP)), capa)

# ============================================================ cuadro de materiales
qx = CX + 12 * CP + 150
d.text((qx, CY - 150), "PROPUESTA DE MATERIALES POR CARA", font=f_cara, fill=NUEVO)
d.text((qx, CY - 116), "La biblia solo definía la fachada de la avenida. Las otras tres se deciden aquí.",
       font=f_peq, fill=TINTA)
bloques = [
    ("SUR · avenida", VERDE_BAR, ["Verde botella con cornisas crema. Neón de la gata,",
                                  "balcón de madera, vitrina y puerta abierta de par",
                                  "en par por el calor. Frente al gallo del taller."]),
    ("OESTE · Calle Olmedo", VERDE_BAR, ["Verde botella también: envuelve la esquina, igual",
                                         "que el ónix en el taller. Las cuatro ventanas con",
                                         "reja del piso de Micaela y la entrega de bebidas."]),
    ("NORTE · fondo", "#5b564d", ["Bloque enlucido sin pintar. Portón del patio por",
                                  "donde entra el hielo, campana de la cocina y las",
                                  "ventanas del dormitorio. Nunca se filma de frente."]),
    ("ESTE · medianera", "#5b564d", ["Sin acabado. Muro compartido con el vecino de la",
                                     "Mz. H. Solo aparece en tomas aéreas."]),
    ("CUBIERTA", "#5b564d", ["Zinc a dos aguas, tanque de agua elevado y el",
                             "tendedero de Micaela. El balcón vuela 1,20 m."]),
    ("LO QUE SE GANA", NUEVO, ["El tanque elevado y el tendedero son lo que hace",
                               "que la esquina se lea costeña desde el aire, y no",
                               "estaban dibujados en ninguna parte."]),
]
yy = CY - 70
for titulo, col, lineas in bloques:
    d.text((qx, yy), titulo, font=fuente("sans_bold", 18), fill=col)
    yy += 26
    for ln in lineas:
        d.text((qx + 10, yy), ln, font=f_peq, fill=TINTA)
        yy += 21
    yy += 14

d.text((MAR, 44), "BAR LA GATA · LAS CUATRO CARAS Y LA CUBIERTA", font=f_tit, fill=TINTA)
d.text((MAR, 96), "Puerto Candela, Guayas · escala gráfica · medidas en metros · casona de esquina de 12 × 20 m",
       font=f_sub, fill=TINTA)
d.text((MAR, 128), "La casona y las medidas no cambian. Lo que se fija aquí es qué hay en cada lado.",
       font=f_sub, fill=NUEVO)
ex, ey = W - 430, H - 90
d.rectangle([ex, ey, ex + 5 * PX, ey + 12], fill=TINTA)
d.rectangle([ex + 5 * PX, ey, ex + 10 * PX, ey + 12], fill="#ffffff", outline=TINTA, width=2)
for m in (0, 5, 10):
    d.text((ex + m * PX, ey + 28), "%d m" % m, font=f_peq, fill=TINTA, anchor="mm")
im.save(destino("08-bar-cuatro-caras.png"), optimize=True)
print("cuatro caras del bar ok")
