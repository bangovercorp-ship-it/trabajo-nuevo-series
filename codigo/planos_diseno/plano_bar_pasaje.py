# -*- coding: utf-8 -*-
"""Planta y fachada del Bar La Gata, y plano del Pasaje La Esperanza. Medidas en metros.
Version Ecuador.

Bar: lote de esquina 12 x 20 m al norte de la avenida (la fachada mira al sur, al taller).
Coordenadas con el norte arriba: X oeste->este, Y fondo(0)->avenida(20).
La casona y las medidas NO cambian. Cambia como se vive adentro, que es lo que se filma:
porton enrollable y puertas abiertas por el calor, reja, ventilador de pie apuntando a la
barra, hielera con la cerveza grande, tele colgada en la esquina para el partido, y los
sabados el puesto de encebollado en la vereda, con el bar cerrado.

Pasaje: 100 x 5 m detras del taller, de la Calle Olmedo (X=0) a la Calle 10 de Agosto (X=100).
La rejilla del compresor y la puerta gris caen donde las pone la planta del taller.
Tres faroles y solo funciona el de la puerta gris, como manda la biblia.
"""
import math

from PIL import Image, ImageDraw

from comun import destino, fuente

f_tit, f_sub, f_zona = fuente("sans_bold", 44), fuente("sans", 21), fuente("sans_bold", 17)
f_med, f_peq, f_calle = fuente("sans", 15), fuente("sans", 13), fuente("sans_bold", 21)
f_min = fuente("sans", 11)
TINTA, MURO, ORO = "#26221e", "#3a3530", "#b8923a"
VERDE, CREMA, GATA, MADERA = "#1f4d3a", "#efe6d2", "#e0529a", "#6b4a2e"
NUEVO = "#1d6a6a"


def lienzo(w, h, fondo="#efe7d4"):
    im = Image.new("RGB", (w, h), fondo)
    return im, ImageDraw.Draw(im)


# ======================================================= PLANTA DEL BAR
PX, MX, MY = 42, 150, 210
im, d = lienzo(int(12 * PX + 2 * MX + 470), int(20 * PX + MY + 320))
P = lambda x, y: (MX + x * PX, MY + y * PX)
R = lambda x0, y0, x1, y1, f=None, o=TINTA, w=2: d.rectangle([P(x0, y0), P(x1, y1)], fill=f, outline=o, width=w)
T = lambda x, y, s, f=f_zona, c=TINTA, a="mm": d.text(P(x, y), s, font=f, fill=c, anchor=a)


def cota_h(x0, x1, y, s):
    d.line([P(x0, y), P(x1, y)], fill=TINTA, width=1)
    for x in (x0, x1):
        d.line([P(x, y - 0.2), P(x, y + 0.2)], fill=TINTA, width=2)
    T((x0 + x1) / 2, y - 0.35, s, f_med)


R(0, 0, 12, 20, "#f3ece0", None)
d.polygon([P(0, 18), P(0, 20), P(2, 20)], fill="#efe7d4")              # ochavo 2 x 2
zonas = [
    (0, 0, 4, 4, "#e9e1d0", "COCINA", "4,0 × 4,0"),
    (0, 4, 4, 8, "#e3d9c4", "DEPÓSITO", "bebidas · 4,0 × 4,0"),
    (4, 0, 6, 6, "#dde7ec", "DAMAS", "2,0 × 6,0"),
    (6, 0, 8, 6, "#dde7ec", "CABALLEROS", "2,0 × 6,0"),
    (9.3, 0, 12, 4, "#dfe6d6", "PATIO", "salida trasera"),
    (9.3, 4, 12, 8, "#e8dcc9", "OFICINA", "caja fuerte"),
]
for x0, y0, x1, y1, c, n, s in zonas:
    R(x0, y0, x1, y1, c)
    T((x0 + x1) / 2, (y0 + y1) / 2 - 0.3, n, f_zona if x1 - x0 > 2.5 else f_peq)
    T((x0 + x1) / 2, (y0 + y1) / 2 + 0.45, s, f_peq)
R(4, 6, 9.3, 8, "#efe7d8", None)
T(6.65, 7.0, "pasillo", f_peq)
for k in range(9):                                                      # escalera
    d.line([P(8.05, 1.3 + k * 0.65), P(9.25, 1.3 + k * 0.65)], fill=TINTA, width=2)
T(8.65, 0.6, "esc.", f_peq)

# salon
R(0, 8, 12, 20, "#f6efe2", None)
T(6.2, 15.7, "SALÓN · 12,0 × 12,0 m", f_zona)
T(6.2, 16.4, "piso de losetas en damero", f_peq)
R(0.05, 9, 0.55, 17, "#8a6a3e", None)                                   # contrabarra con botellas
R(1.3, 9, 2.0, 17, MADERA, TINTA, 2)                                    # barra de 8 m
T(0.95, 17.6, "barra 8,0 m", f_peq)
for i in range(8):
    cy = 9.5 + i * 1.0
    d.ellipse([P(2.35, cy - 0.22), P(2.8, cy + 0.22)], fill="#9b2f2f", outline=TINTA)
for (cx, cy) in [(5.0, 11.0), (8.0, 11.0), (5.0, 14.2), (8.0, 14.2), (8.7, 18.2)]:
    d.ellipse([P(cx - 0.45, cy - 0.45), P(cx + 0.45, cy + 0.45)], fill="#c9a877", outline=TINTA, width=2)
    for (dx, dy) in [(-0.8, 0), (0.8, 0)]:
        d.ellipse([P(cx + dx - 0.2, cy + dy - 0.2), P(cx + dx + 0.2, cy + dy + 0.2)], fill="#7a5a3a")
T(5.8, 19.3, "la mesa de la ventana", f_peq)
d.line([P(11.9, 9.5), P(11.9, 16.0)], fill=ORO, width=8)                 # pared de fotos
T(11.6, 12.8, "fotos", f_peq, TINTA, "rm")
R(10.8, 8.3, 11.8, 9.1, "#b3261e", TINTA, 2)
T(10.2, 8.7, "rocola", f_peq, TINTA, "rm")

# --- lo ecuatoriano de adentro ----------------------------------------------------
# hielera con la cerveza grande, detras de la barra
R(2.4, 17.3, 3.6, 18.3, "#5d8fb3", TINTA, 2)
T(3.0, 17.8, "hielera", f_min, "#ffffff")
# ventilador de pie apuntando a la barra, con las cintas en la rejilla
d.ellipse([P(3.3, 12.4), P(4.1, 13.2)], fill="#d9d4c8", outline=NUEVO, width=3)
for k in range(5):
    a = -0.9 + k * 0.45
    d.line([P(3.7, 12.8), P(3.7 + 0.38 * math.cos(a), 12.8 + 0.38 * math.sin(a))], fill="#9aa39a", width=2)
T(3.7, 11.95, "ventilador de pie", f_min, NUEVO)
# la tele de la esquina: cuando hay partido, la rocola se calla
R(11.2, 18.4, 11.85, 19.4, "#2b2b2b", NUEVO, 3)
T(11.5, 18.05, "tele", f_min, NUEVO)

# muros, puerta, vitrina y porton enrollable
for (a, b) in [((0, 0), (12, 0)), ((12, 0), (12, 20)), ((0, 0), (0, 18)), ((0, 18), (2, 20)), ((2, 20), (3.5, 20)),
               ((4.7, 20), (6.5, 20)), ((11, 20), (12, 20))]:
    d.line([P(*a), P(*b)], fill=MURO, width=9)
d.line([P(3.5, 20), P(4.7, 20)], fill="#c79a4a", width=9)
d.line([P(6.5, 20), P(11, 20)], fill="#9fc3d6", width=9)
# la reja: cualquier negocio de la costa cierra con reja
for k in range(19):
    xx = 6.6 + k * 0.23
    d.line([P(xx, 19.82), P(xx, 20.18)], fill=NUEVO, width=2)
T(9.5, 19.6, "reja corrediza · se recoge de día", f_min, NUEVO)

# --- la vereda: donde de verdad pasa la escena ------------------------------------
R(-1.0, 20.2, 13.0, 22.0, "#ded8cc", None)
T(0.6, 20.55, "vereda", f_min, TINTA, "lm")
for (cx, cy) in [(4.2, 21.1), (5.9, 21.1)]:                              # mesas de plastico al atardecer
    d.ellipse([P(cx - 0.38, cy - 0.38), P(cx + 0.38, cy + 0.38)], fill="#e8e3d6", outline=NUEVO, width=3)
T(5.05, 21.9, "dos mesas de plástico salen al atardecer", f_min, NUEVO)
R(8.4, 20.5, 12.2, 21.6, "#f0e2c4", NUEVO, 3)                            # puesto de encebollado
T(10.3, 20.85, "ENCEBOLLADO", f_peq, NUEVO)
T(10.3, 21.3, "sábados · el bar no abre", f_min, NUEVO)
T(2.8, 20.6, "puerta 1,20 × 2,60", f_min)
T(8.75, 22.35, "vitrina 4,50 × 1,90 · portón enrollable sobre el vano", f_min)

# calles
T(6, 23.4, "AV. EL CRUCE  (enfrente: el taller)", f_calle)
capa = Image.new("RGBA", (300, 30), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((4, 2), "CALLE OLMEDO", font=f_calle, fill=TINTA)
capa = capa.rotate(90, expand=True)
im.paste(capa, (int(P(-2.9, 0)[0]), int(P(0, 5)[1])), capa)
cota_h(0, 12, 24.6, "12,00 m")

# cuadro
cx = MX + 12 * PX + 110
d.text((cx, MY - 10), "BAR LA GATA", font=f_tit, fill=TINTA)
for i, s in enumerate(["lote de esquina 12 × 20 m (240 m²)", "primer piso 3,60 m · segundo 3,00 m",
                       "arriba vive Micaela (balcón al frente)", "", "barra de 8 m y 8 taburetes",
                       "5 mesas · 18 sillas", "pared de fotos antiguas (pista ep. 5)",
                       "rocola junto a la pared de fotos",
                       "", "la mesa de la ventana mira", "de frente al portón del taller"]):
    d.text((cx, MY + 50 + i * 33), s, font=f_sub, fill=TINTA)
d.text((cx, MY + 50 + 12 * 33), "LO QUE CAMBIA EN ECUADOR", font=f_zona, fill=NUEVO)
for i, s in enumerate(["se abre a la calle: portón enrollable", "y puertas de par en par por el calor",
                       "reja corrediza para cerrar", "ventilador de pie a la barra",
                       "hielera: la cerveza grande y helada,", "en un vaso que va rotando",
                       "tele en la esquina para el partido", "sábados: encebollado en la vereda",
                       "el neón de la gata no se toca"]):
    d.text((cx, MY + 50 + 13 * 33 + i * 31), s, font=f_sub, fill=NUEVO)
d.text((MX, 34), "BAR LA GATA · PLANTA DEL PRIMER PISO", font=f_tit, fill=TINTA)
d.text((MX, 92), "Puerto Candela, Guayas · escala gráfica · medidas en metros · norte arriba", font=f_sub, fill=TINTA)
d.text((MX, 126), "la fachada mira al sur, al taller · en turquesa, lo que cambia en la versión Ecuador",
       font=f_sub, fill=NUEVO)
im.save(destino("04-planta-bar.png"), optimize=True)
print("planta del bar ok")

# ======================================================= FACHADA DEL BAR
PX2, MX2, BASE = 70, 150, 700
im2, e = lienzo(int(12 * PX2 + 2 * MX2 + 320), BASE + 130, "#1f2530")
Q = lambda x, z: (MX2 + x * PX2, BASE - z * PX2)
R2 = lambda x0, z0, x1, z1, f, o=TINTA, w=2: e.rectangle([Q(x0, z1), Q(x1, z0)], fill=f, outline=o, width=w)
R2(-1.5, -0.3, 13.5, 0, "#5a5a5a", None)
R2(0, 0, 12, 7.5, VERDE)
for z in (3.6, 3.9, 6.9, 7.5):
    e.line([Q(0, z), Q(12, z)], fill=CREMA, width=5)
R2(3.5, 0, 4.7, 2.6, "#4a2e1f", CREMA, 3)
R2(3.6, 1.4, 4.6, 2.5, "#c8d4d6", None)
R2(6.5, 0.9, 11, 2.8, "#e3a07a", CREMA, 4)                             # vitrina con luz roja de adentro
for xx in (8.0, 9.5):
    e.line([Q(xx, 0.9), Q(xx, 2.8)], fill=CREMA, width=3)
# caja del porton enrollable, recogido: de dia el bar se abre de par en par
R2(6.4, 2.82, 11.1, 3.00, "#7b8288", CREMA, 2)
e.text(Q(6.3, 2.91), "portón enrollable recogido", font=f_min, fill="#cfe0d4", anchor="rm")
# la reja, delante del vano
for k in range(20):
    xx = 6.6 + k * 0.225
    e.line([Q(xx, 0.9), Q(xx, 2.8)], fill="#9fb0a6", width=2)
e.text(Q(8.75, 0.62), "reja corrediza · de día va recogida", font=f_min, fill="#cfe0d4", anchor="mm")
# neon: gata sentada + LA GATA
# El neon mide 4,80 x 0,55 m y va a 3,00 m de altura (biblia). La gata ocupa el
# extremo izquierdo de esa banda y el resto es el rotulo. Silueta llena, que es lo
# unico que se lee a este tamano.
NX0, NZ0, NL, NH = 3.6, 3.0, 4.8, 0.55
e.rectangle([Q(NX0, NZ0 + NH), Q(NX0 + NL, NZ0)], outline="#4a3a44", width=2)
G = lambda u, v: Q(NX0 + 0.06 + u * 0.62, NZ0 + v * NH)
e.polygon([G(0.30, 0.02), G(0.80, 0.02), G(0.74, 0.30), G(0.63, 0.50), G(0.47, 0.57),
           G(0.35, 0.44), G(0.29, 0.20)], fill=GATA)                    # cuerpo sentado
e.ellipse([G(0.38, 0.92), G(0.80, 0.55)], fill=GATA)                    # cabeza
e.polygon([G(0.42, 0.82), G(0.40, 1.00), G(0.56, 0.88)], fill=GATA)     # oreja izquierda
e.polygon([G(0.66, 0.88), G(0.80, 1.00), G(0.78, 0.80)], fill=GATA)     # oreja derecha
e.line([G(0.30, 0.06), G(0.12, 0.16), G(0.05, 0.40), G(0.16, 0.50)],
       fill=GATA, width=5, joint="curve")                               # cola enroscada
e.text(Q(NX0 + 1.05, NZ0 + NH / 2), "LA GATA", font=fuente("serif_bold", 34), fill=GATA, anchor="lm")
e.text(Q(NX0 + NL / 2, NZ0 + NH + 0.20), "neón 4,80 × 0,55 m, a 3,00 m", font=f_min, fill="#cfe0d4", anchor="mm")
# balcon de madera del segundo piso
for x0 in (3.8, 6.4):
    R2(x0, 4.25, x0 + 1.8, 6.4, "#3a2a1e", CREMA, 3)
R2(10.0, 4.8, 11.2, 6.2, "#3a2a1e", CREMA, 3)
R2(3.0, 4.25, 9.0, 5.4, None, MADERA, 5)                               # balcon, delante
for i in range(1, 16):
    xx = 3.0 + i * 6.0 / 16
    e.line([Q(xx, 4.25), Q(xx, 5.4)], fill=MADERA, width=4)
# dos mesas de plastico en la vereda
for cx0 in (1.2, 2.5):
    e.ellipse([Q(cx0 - 0.3, 0.75), Q(cx0 + 0.3, 0.6)], fill="#e8e3d6", outline="#9aa39a", width=2)
    e.line([Q(cx0, 0.6), Q(cx0, 0)], fill="#cfcabd", width=3)
e.text(Q(1.85, 1.0), "mesas de plástico", font=f_min, fill="#cfe0d4", anchor="mm")


def cz(z0, z1, x, s):
    e.line([Q(x, z0), Q(x, z1)], fill="#dddddd", width=1)
    for z in (z0, z1):
        e.line([Q(x - 0.15, z), Q(x + 0.15, z)], fill="#dddddd", width=2)
    e.text((Q(x, (z0 + z1) / 2)[0] + 12, Q(x, (z0 + z1) / 2)[1]), s, font=f_med, fill="#dddddd", anchor="lm")


cz(0, 3.6, 12.6, "primer piso 3,60")
cz(3.9, 6.9, 12.6, "segundo piso 3,00")
cz(0, 7.5, 14.5, "total 7,50")
e.text((MX2, 30), "BAR LA GATA · FACHADA A LA AV. EL CRUCE (DE NOCHE)", font=f_tit, fill="#f0f0f0")
e.text((MX2, 88), "casona verde botella · cornisas crema · balcón de madera · neón rosado de la gata frente al gallo rojo",
       font=f_sub, fill="#dddddd")
e.text((MX2, 122), "Ecuador: portón enrollable recogido, reja y mesas de plástico en la vereda. Las medidas no cambian.",
       font=f_sub, fill="#7fd0c4")
im2.save(destino("05-fachada-bar.png"), optimize=True)
print("fachada del bar ok")

# ======================================================= PASAJE LA ESPERANZA
PX3, MX3, MY3 = 16, 160, 250
im3, g = lienzo(int(100 * PX3 + 2 * MX3), 1010)
S = lambda x, y: (MX3 + x * PX3, MY3 + y * PX3)
RS = lambda x0, y0, x1, y1, f, o=TINTA, w=2: g.rectangle([S(x0, y0), S(x1, y1)], fill=f, outline=o, width=w)
TS = lambda x, y, s, f=f_peq, c=TINTA, a="mm": g.text(S(x, y), s, font=f, fill=c, anchor=a)
RS(0, -6, 24, 0, "#b3261e")
TS(12, -3, "ESPALDA DEL TALLER GALLARDO", f_zona, "#ffffff")
RS(24, -6, 100, 0, "#d8ccb0")
TS(62, -3, "espaldas de los 6 almacenes de repuestos", f_zona)
RS(0, 5, 100, 11, "#d8ccb0")
TS(50, 8, "espaldas de las casas de la Mz. R · bloque enlucido, dos pisos, reja y zinc", f_zona)
for i in range(1, 12):
    g.line([S(i * 100 / 12, 5), S(i * 100 / 12, 11)], fill="#bda97c", width=1)
RS(0, 0, 100, 5, "#8c8a86", None)
g.line([S(0, 2.5), S(100, 2.5)], fill="#5b5a58", width=4)                # canaleta central
RS(21.8, -0.25, 22.8, 0, "#9a9a9a", TINTA, 2)
TS(22.3, -1.0, "puerta gris sin manija", f_peq, "#ffffff")
RS(12.5, -0.2, 13.5, 0, "#3f3f3f", TINTA, 1)
TS(13, -1.8, "rejilla del compresor", f_peq, "#ffffff")
# tres faroles, y SOLO funciona el de la puerta gris
for (x, estado, col) in [(20, "farol · el único que funciona", "#ffd23f"),
                         (55, "farol · quemado", "#555555"),
                         (88, "farol · quemado", "#555555")]:
    g.ellipse([S(x - 0.5, 4.2), S(x + 0.5, 5.0)], fill=col, outline=TINTA)
    TS(x, 12.4, estado)
for x in (31, 47, 72):
    RS(x, 3.6, x + 0.9, 4.6, "#3b5a3b", TINTA, 1)
TS(47, 1.6, "tachos", f_peq)
TS(20, 10.3, "grafiti", f_peq)
TS(72, 13.3, "gato en el muro", f_peq)
# cables cruzando, que es lo que hay en cualquier pasaje de la costa
for x in (18, 44, 70, 93):
    g.line([S(x - 1.5, 0), S(x + 1.5, 5)], fill="#4a463f", width=2)
TS(82, 6.3, "cables cruzados", f_min)
TS(-5.0, 2.5, "CALLE", f_zona)
TS(-5.0, 3.6, "OLMEDO", f_zona)
TS(105.5, 2.5, "CALLE", f_zona)
TS(105.5, 3.6, "10 DE AGOSTO", f_zona)
RS(0.3, 0.2, 2.8, 1.2, "#2f5aa0", "#ffffff", 2)
TS(1.55, 0.7, "letrero", f_peq, "#ffffff")
g.line([S(0, 14.3), S(100, 14.3)], fill=TINTA, width=1)
TS(50, 15.2, "100,00 m", f_med)
g.line([S(101.5, 0), S(101.5, 5)], fill=TINTA, width=1)
TS(101.5, -0.8, "5,00", f_med)

# corte transversal
cx0, cy0, k = MX3 + 60, 910, 48
def C(x, z): return (cx0 + x * k, cy0 - z * k)
def caja(p0, p1):
    (x0, y0), (x1, y1) = p0, p1
    return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
g.rectangle(caja(C(-0.3, 0), C(0, 7.25)), fill="#b3261e")
g.text((C(-0.4, 3.6)[0] - 6, C(0, 3.6)[1]), "taller 7,25 m", font=f_med, fill=TINTA, anchor="rm")
g.rectangle(caja(C(5, 0), C(5.3, 5.6)), fill="#d8ccb0", outline=TINTA)
g.text((C(5.4, 2.8)[0] + 6, C(0, 2.8)[1]), "casas de dos pisos 5,60 m", font=f_med, fill=TINTA, anchor="lm")
g.rectangle(caja(C(0, -0.1), C(5, 0)), fill="#8c8a86")
g.line([C(0, 0), C(5, 0)], fill=TINTA, width=2)
g.rectangle(caja(C(2.35, -0.1), C(2.65, 0.02)), fill="#5b5a58")
g.rectangle(caja(C(0.02, 0), C(0.12, 2.1)), fill="#9a9a9a", outline=TINTA)
g.line([C(4.6, 0), C(4.6, 4.2)], fill="#555555", width=4)
g.ellipse(caja(C(4.3, 4.35), C(4.9, 4.05)), fill="#ffd23f")
g.text((cx0 + 2.5 * k, cy0 + 30), "corte: 5,00 m de ancho, canaleta al centro, farol a 4,2 m",
       font=f_med, fill=TINTA, anchor="mm")
g.text((MX3, 34), "PASAJE LA ESPERANZA · PLANTA Y CORTE", font=f_tit, fill=TINTA)
g.text((MX3, 92), "peatonal · 100 × 5 m · detrás del taller, de la Calle Olmedo a la Calle 10 de Agosto · norte arriba",
       font=f_sub, fill=TINTA)
g.text((MX3, 126), "la rejilla del compresor y la puerta gris caen donde las pone la planta del taller",
       font=f_sub, fill=NUEVO)
im3.save(destino("06-plano-pasaje.png"), optimize=True)
print("pasaje ok")
