# -*- coding: utf-8 -*-
"""Planta y fachada del Bar La Gata, y plano del Pasaje La Esperanza. Medidas en metros.

Bar: lote de esquina 12 x 20 m al norte de la avenida (la fachada mira al sur, al taller).
Coordenadas con el norte arriba: X oeste->este, Y fondo(0)->avenida(20).
Pasaje: 100 x 5 m detras del taller, de Jr. Los Mecanicos (X=0) a Calle San Martin (X=100).
"""
from PIL import Image, ImageDraw, ImageFont

F = "C:/Windows/Fonts/"
def fuente(n, s): return ImageFont.truetype(F + n, s)
f_tit, f_sub, f_zona = fuente("arialbd.ttf", 44), fuente("arial.ttf", 21), fuente("arialbd.ttf", 17)
f_med, f_peq, f_calle = fuente("arial.ttf", 15), fuente("arial.ttf", 13), fuente("arialbd.ttf", 21)
TINTA, MURO, ORO = "#26221e", "#3a3530", "#b8923a"
VERDE, CREMA, GATA, MADERA = "#1f4d3a", "#efe6d2", "#e0529a", "#6b4a2e"


def lienzo(w, h, fondo="#efe7d4"):
    im = Image.new("RGB", (w, h), fondo)
    return im, ImageDraw.Draw(im)


def cotas(d, P):
    def cota_h(x0, x1, y, s):
        d.line([P(x0, y), P(x1, y)], fill=TINTA, width=1)
        for x in (x0, x1):
            d.line([P(x, y - 0.2), P(x, y + 0.2)], fill=TINTA, width=2)
        d.text(P((x0 + x1) / 2, y - 0.35), s, font=f_med, fill=TINTA, anchor="mm")
    return cota_h


# ======================================================= PLANTA DEL BAR
PX, MX, MY = 42, 150, 210
im, d = lienzo(int(12 * PX + 2 * MX + 470), int(20 * PX + MY + 190))
P = lambda x, y: (MX + x * PX, MY + y * PX)
R = lambda x0, y0, x1, y1, f=None, o=TINTA, w=2: d.rectangle([P(x0, y0), P(x1, y1)], fill=f, outline=o, width=w)
T = lambda x, y, s, f=f_zona, c=TINTA, a="mm": d.text(P(x, y), s, font=f, fill=c, anchor=a)
cota_h = cotas(d, P)

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
T(6.6, 16.6, "SALÓN · 12,0 × 12,0 m", f_zona)
T(6.6, 17.3, "piso de losetas en damero", f_peq)
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
T(8.7, 19.2, "la mesa de la ventana", f_peq)
d.line([P(11.9, 9.5), P(11.9, 16.0)], fill=ORO, width=8)                 # pared de fotos
T(11.6, 12.8, "fotos", f_peq, TINTA, "rm")
R(10.8, 8.3, 11.8, 9.1, "#b3261e", TINTA, 2)
T(10.2, 8.7, "rocola", f_peq, TINTA, "rm")
# muros, puerta y vitrina
for (a, b) in [((0, 0), (12, 0)), ((12, 0), (12, 20)), ((0, 0), (0, 18)), ((0, 18), (2, 20)), ((2, 20), (3.5, 20)),
               ((4.7, 20), (6.5, 20)), ((11, 20), (12, 20))]:
    d.line([P(*a), P(*b)], fill=MURO, width=9)
d.line([P(3.5, 20), P(4.7, 20)], fill="#c79a4a", width=9)
d.line([P(6.5, 20), P(11, 20)], fill="#9fc3d6", width=9)
T(4.1, 20.7, "puerta 1,20 × 2,60", f_peq)
T(8.75, 20.7, "vitrina 4,50 × 1,90", f_peq)
# calles
T(6, 22.0, "AV. EL CRUCE  (enfrente: el taller)", f_calle)
capa = Image.new("RGBA", (300, 30), (0, 0, 0, 0))
ImageDraw.Draw(capa).text((4, 2), "JR. LOS MECÁNICOS", font=f_calle, fill=TINTA)
capa = capa.rotate(90, expand=True)
im.paste(capa, (int(P(-2.7, 0)[0]), int(P(0, 5)[1])), capa)
cota_h(0, 12, 23.3, "12,00 m")
# cuadro
cx = MX + 12 * PX + 110
d.text((cx, MY - 10), "BAR LA GATA", font=f_tit, fill=TINTA)
for i, s in enumerate(["lote de esquina 12 × 20 m (240 m²)", "primer piso 3,60 m · segundo 3,00 m",
                       "arriba vive Micaela (balcón al frente)", "", "barra de 8 m y 8 taburetes",
                       "5 mesas · 18 sillas", "pared de fotos antiguas (pista ep. 5)", "rocola junto a la pared de fotos",
                       "", "la mesa de la ventana mira", "de frente al portón del taller"]):
    d.text((cx, MY + 50 + i * 33), s, font=f_sub, fill=TINTA)
d.text((MX, 40), "BAR LA GATA · PLANTA DEL PRIMER PISO", font=f_tit, fill=TINTA)
d.text((MX, 98), "escala gráfica · medidas en metros · norte arriba · la fachada mira al sur, al taller", font=f_sub, fill=TINTA)
im.save(r"C:\pesonajes para videos\planos_diseno\04-planta-bar.png", optimize=True)

# ======================================================= FACHADA DEL BAR
PX2, MX2, BASE = 70, 150, 760
im2, e = lienzo(int(12 * PX2 + 2 * MX2 + 300), BASE + 200, "#1f2530")
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
# neon: gata sentada + LA GATA
nx, nz = 6.0, 2.95
gata = [(0.0, 0.0), (0.35, 0.0), (0.4, 0.3), (0.32, 0.55), (0.38, 0.72), (0.34, 0.8), (0.28, 0.72), (0.2, 0.74),
        (0.14, 0.8), (0.12, 0.7), (0.08, 0.55), (0.02, 0.3), (-0.12, 0.12), (-0.2, 0.2), (-0.05, 0.02)]
e.line([Q(nx + a * 0.9, nz + b * 0.9) for a, b in gata] + [Q(nx, nz)], fill=GATA, width=6)
e.text(Q(8.4, 3.25), "LA GATA", font=fuente("georgiab.ttf", 44), fill=GATA, anchor="mm")
# balcon de madera del segundo piso
R2(3.0, 3.95, 9.0, 5.1, None, MADERA, 5)
for i in range(1, 16):
    xx = 3.0 + i * 6.0 / 16
    e.line([Q(xx, 3.95), Q(xx, 5.1)], fill=MADERA, width=4)
for x0 in (3.8, 6.4):
    R2(x0, 3.95, x0 + 1.8, 6.4, "#3a2a1e", CREMA, 3)
R2(10.0, 4.8, 11.2, 6.2, "#3a2a1e", CREMA, 3)
def cz(z0, z1, x, s):
    e.line([Q(x, z0), Q(x, z1)], fill="#dddddd", width=1)
    for z in (z0, z1):
        e.line([Q(x - 0.15, z), Q(x + 0.15, z)], fill="#dddddd", width=2)
    e.text((Q(x, (z0 + z1) / 2)[0] + 12, Q(x, (z0 + z1) / 2)[1]), s, font=f_med, fill="#dddddd", anchor="lm")
cz(0, 3.6, 12.5, "primer piso 3,60")
cz(3.9, 6.9, 12.5, "segundo piso 3,00")
cz(0, 7.5, 14.3, "total 7,50")
cz(2.95, 3.55, -0.9, "")
e.text((Q(-0.9, 3.25)[0] - 10, Q(0, 3.25)[1]), "neón", font=f_med, fill="#dddddd", anchor="rm")
e.text((MX2, 30), "BAR LA GATA · FACHADA A LA AV. EL CRUCE (DE NOCHE)", font=f_tit, fill="#f0f0f0")
e.text((MX2, 88), "casona verde botella · cornisas crema · balcón de madera · neón rosado de la gata frente al gallo rojo",
       font=f_sub, fill="#dddddd")
im2.save(r"C:\pesonajes para videos\planos_diseno\05-fachada-bar.png", optimize=True)

# ======================================================= PASAJE LA ESPERANZA
PX3, MX3, MY3 = 16, 140, 250
im3, g = lienzo(int(100 * PX3 + 2 * MX3), 1180)
S = lambda x, y: (MX3 + x * PX3, MY3 + y * PX3)
RS = lambda x0, y0, x1, y1, f, o=TINTA, w=2: g.rectangle([S(x0, y0), S(x1, y1)], fill=f, outline=o, width=w)
TS = lambda x, y, s, f=f_peq, c=TINTA, a="mm": g.text(S(x, y), s, font=f, fill=c, anchor=a)
RS(0, -6, 24, 0, "#b3261e")
TS(12, -3, "ESPALDA DEL TALLER GALLARDO", f_zona, "#ffffff")
RS(24, -6, 100, 0, "#d8ccb0")
TS(62, -3, "espaldas de las 6 tiendas de repuestos", f_zona)
RS(0, 5, 100, 11, "#d8ccb0")
TS(50, 8, "espaldas de las casas de la Mz. R (12 lotes de 8 m)", f_zona)
for i in range(1, 12):
    g.line([S(i * 100 / 12, 5), S(i * 100 / 12, 11)], fill="#bda97c", width=1)
RS(0, 0, 100, 5, "#8c8a86", None)
g.line([S(0, 2.5), S(100, 2.5)], fill="#5b5a58", width=4)                # canaleta central
RS(21.8, -0.25, 22.8, 0, "#9a9a9a", TINTA, 2)
TS(22.3, -1.0, "puerta gris sin manija", f_peq, "#ffffff")
RS(12.5, -0.2, 13.5, 0, "#3f3f3f", TINTA, 1)
TS(13, -1.8, "rejilla del compresor", f_peq, "#ffffff")
for (x, estado, col) in [(20, "farol · funciona", "#ffd23f"), (55, "farol · apagado", "#555555"), (88, "farol · parpadea", "#c9a03a")]:
    g.ellipse([S(x - 0.5, 4.2), S(x + 0.5, 5.0)], fill=col, outline=TINTA)
    TS(x, 12.3, estado)
for x in (31, 47, 72):
    RS(x, 3.6, x + 0.9, 4.6, "#3b5a3b", TINTA, 1)
TS(47, 3.2, "tachos", f_peq)
TS(40, 10.2, "grafiti", f_peq)
TS(65, 12.3, "gato en el muro", f_peq)
TS(-4.5, 2.5, "JR. LOS", f_zona)
TS(-4.5, 3.6, "MECÁNICOS", f_zona)
TS(104.5, 2.5, "CALLE", f_zona)
TS(104.5, 3.6, "SAN MARTÍN", f_zona)
RS(0.3, 0.2, 2.8, 1.2, "#2f5aa0", "#ffffff", 2)
TS(1.55, 0.7, "letrero", f_peq, "#ffffff")
g.line([S(0, 14.2), S(100, 14.2)], fill=TINTA, width=1)
TS(50, 15.1, "100,00 m", f_med)
g.line([S(101.5, 0), S(101.5, 5)], fill=TINTA, width=1)
TS(101.5, -0.8, "5,00", f_med)
# corte transversal
cx0, cy0, k = MX3 + 60, 1110, 48
def C(x, z): return (cx0 + x * k, cy0 - z * k)
def caja(p0, p1, **kw):
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
g.text((cx0 + 2.5 * k, cy0 + 30), "corte: 5,00 m de ancho, canaleta al centro, farol a 4,2 m", font=f_med, fill=TINTA, anchor="mm")
g.text((MX3, 40), "PASAJE LA ESPERANZA · PLANTA Y CORTE", font=f_tit, fill=TINTA)
g.text((MX3, 98), "peatonal · 100 × 5 m · detrás del taller, de Jr. Los Mecánicos a Calle San Martín · norte arriba",
       font=f_sub, fill=TINTA)
im3.save(r"C:\pesonajes para videos\planos_diseno\06-plano-pasaje.png", optimize=True)
print("ok")
