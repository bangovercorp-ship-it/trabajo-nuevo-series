# -*- coding: utf-8 -*-
"""Secciones de las cuatro calles de El Cruce. 10-secciones-viales.png

POR QUE EXISTE: el plano urbano dice donde va cada calle y cuanto mide de ancho,
pero no dice como es por dentro. Sin eso, cada toma inventa el ancho de la vereda,
el pavimento y el arbolado, y a los tres capitulos la misma calle es otra calle.

LA DECISION DE FONDO: en un pueblo de 12.000 habitantes NO esta todo asfaltado, y
eso no es un descuido, es lo que hay. Se propone una jerarquia de tres pavimentos:
asfalto en la avenida, adoquin en la colectora, lastre compactado en las locales.
Ademas da dos climas de imagen: polvo en verano y barro en invierno.

Una especie por jerarquia de via, que ademas hace que cada calle se reconozca desde
el aire sin leer un rotulo: ceibo en la avenida, almendro en Olmedo, mango en las
locales. Escala 1:100. 1 m = 22 px.
"""
from PIL import Image, ImageDraw

from comun import destino, fuente, TINTA, ZINC, BLOQUE

PX = 22
PANEL_H = 420
MARG = 80
TABLA = 700
AN = 40 * PX + MARG * 2 + TABLA
AL = 200 + PANEL_H * 4 + 190
PAPEL = "#f4f1e8"

CALZ = {"asfalto": "#57544e", "adoquin": "#9a9186", "lastre": "#a8a08c"}
VEREDA = "#cdc6b6"
CESPED = "#8fa877"
CIELO = "#e3e9ec"
CASA = "#ddd3bd"

im = Image.new("RGB", (AN, AL), PAPEL)
d = ImageDraw.Draw(im, "RGBA")

f_tit = fuente("serif_bold", 42)
f_sub = fuente("sans", 20)
f_cap = fuente("sans_bold", 24)
f_med = fuente("sans", 16)
f_peq = fuente("sans", 13)
f_min = fuente("sans", 11)


class Seccion(object):
    """Corte transversal. (0,0) es el eje de la calzada, al nivel de la calzada.
    x crece a la derecha en metros, z crece hacia arriba en metros."""

    def __init__(self, oy, ancho, titulo, sub):
        self.ox = MARG + 20 * PX          # el eje, centrado en los 40 m del papel
        self.oy = oy
        self.ancho = ancho
        d.rectangle([MARG - 20, oy - PANEL_H + 128, MARG + 40 * PX + 20, oy + 112],
                    fill=CIELO, outline="#b6b0a2", width=1)
        d.text((MARG - 12, oy - PANEL_H + 138), titulo, font=f_cap, fill=TINTA)
        d.text((MARG - 12, oy - PANEL_H + 166), sub, font=f_peq, fill="#6a6456")

    def Q(self, x, z):
        return (self.ox + x * PX, self.oy - z * PX)

    def r(self, x0, z0, x1, z1, fill, out=TINTA, w=2):
        a, b = self.Q(x0, z0)
        c, e = self.Q(x1, z1)
        d.rectangle([min(a, c), min(b, e), max(a, c), max(b, e)], fill=fill, outline=out, width=w)

    def suelo(self, pav):
        """el cuerpo de tierra bajo la calle, rayado, para que la vereda se separe"""
        m = min(self.ancho / 2 + 2.5, 19.8)
        self.r(-m, -1.15, m, 0, "#8a7f68", None)
        xx = -m
        while xx < m:                                   # rayado de terreno
            a, b = self.Q(xx, 0)
            c, e = self.Q(xx + 0.7, -1.15)
            d.line([(a, b), (c, e)], fill="#756b57", width=1)
            xx += 0.7

    def calzada(self, x0, x1, pav, etiq):
        self.r(x0, 0, x1, 0.14, CALZ[pav])
        if pav == "adoquin":
            xx = x0
            while xx < x1:
                d.line([self.Q(xx, 0), self.Q(xx, 0.14)], fill="#7e766b", width=1)
                xx += 0.3
        if pav == "lastre":
            for hx in (x0 + (x1 - x0) * 0.28, x0 + (x1 - x0) * 0.72):
                self.r(hx - 0.55, 0.02, hx + 0.55, 0.12, "#8f8470", None)
        self.cota(x0, x1, -1.75, etiq)

    def vereda(self, x0, x1, alto=0.16):
        self.r(x0, 0, x1, alto, VEREDA)
        borde = x1 if abs(x1) < abs(x0) else x0            # el bordillo mira a la calzada
        self.r(borde - 0.15, 0, borde + 0.15, alto + 0.02, "#b0a899")
        for i in range(int(abs(x1 - x0))):
            xx = min(x0, x1) + i + 1
            d.line([self.Q(xx, alto), self.Q(xx, alto - 0.09)], fill="#9c9484", width=1)

    def parterre(self, x0, x1):
        self.r(x0, 0, x1, 0.18, VEREDA)
        self.r(x0 + 0.15, 0.18, x1 - 0.15, 0.30, CESPED)

    def arbol(self, x, alto, copa, col="#4f7340", tronco="#6d6152"):
        self.r(x - 0.12, 0.16, x + 0.12, alto, tronco, None)
        a, b = self.Q(x - copa, alto + copa * 1.0)
        c, e = self.Q(x + copa, alto - copa * 0.30)
        d.ellipse([a, b, c, e], fill=col, outline="#3e5c34", width=2)

    def poste(self, x, alto, brazo=0):
        self.r(x - 0.1, 0.18, x + 0.1, alto, "#9a958a")
        if brazo:
            self.r(x, alto - 0.3, x + brazo, alto - 0.15, "#9a958a")
            self.r(x + brazo - 0.3, alto - 0.5, x + brazo + 0.3, alto - 0.3, "#d8d2c4")
        else:
            self.r(x - 0.7, alto - 0.35, x + 0.7, alto - 0.2, "#8c8579")

    def edificio(self, x0, x1, alto, portal=0):
        self.r(x0, 0.16, x1, alto, CASA)
        self.r(x0 - 0.2, alto, x1 + 0.2, alto + 0.22, ZINC)
        if portal:
            self.r(x1 if x0 < 0 else x0 - portal, 3.0, (x1 + portal) if x0 < 0 else x0, 3.22, "#cdc6b6")

    def cota(self, x0, x1, z, txt, col="#b3261e"):
        a, b = self.Q(x0, z)
        c, _ = self.Q(x1, z)
        d.line([(a, b), (c, b)], fill=col, width=2)
        for xx in (a, c):
            d.line([(xx, b - 7), (xx, b + 7)], fill=col, width=2)
        # el texto va DEBAJO de la linea: encima cae sobre el cuerpo de tierra
        an = d.textlength(txt, font=f_peq)
        d.rectangle([(a + c) / 2 - an / 2 - 5, b + 4, (a + c) / 2 + an / 2 + 5, b + 24],
                    fill=PAPEL)
        d.text(((a + c) / 2, b + 6), txt, font=f_peq, fill=col, anchor="mt")

    def total(self, txt):
        self.cota(-self.ancho / 2, self.ancho / 2, -2.95, txt, "#1d6a6a")


# ------------------------------------------------------------------ 1 · avenida
y = 200 + PANEL_H
s = Seccion(y, 40, u"1 · AV. EL CRUCE  ·  40,00 m",
            u"Arterial. Es la única asfaltada. Doble calzada con parterre: el parterre es lo que "
            u"permite plantar el ceibo, que con una calzada sola no cabría.")
s.suelo("asfalto")
s.edificio(-20, -16.5, 6.6, portal=2.6)
s.edificio(16.5, 20, 5.4, portal=2.6)
s.vereda(-20, -13)
s.calzada(-13, -2, "asfalto", u"9,00 m calzada + 2,00 estacionamiento")
s.parterre(-2, 2)
s.calzada(2, 13, "asfalto", u"9,00 m calzada + 2,00 estacionamiento")
s.vereda(13, 20)
s.arbol(0, 4.6, 3.6, "#5d7f4a", "#b9b0a0")
s.arbol(-16.4, 4.2, 2.6, "#5d7f4a", "#b9b0a0")
s.poste(-13.9, 9.2, brazo=1.6)
s.poste(13.9, 9.2, brazo=-1.6)
s.cota(-20, -13, -1.75, u"7,00 vereda")
s.cota(13, 20, -1.75, u"7,00 vereda")
s.cota(-2, 2, -1.75, u"4,00 parterre")
s.total(u"40,00 m  ·  línea de fábrica a línea de fábrica")
d.text((MARG + 40 * PX + 30, y - 150),
       u"Ceibo en el parterre, cada 22 m.\nEs el árbol grande del Guayas y el\núnico que cabe sin levantar la vereda.",
       font=f_med, fill="#5a554c", spacing=6)

# ------------------------------------------------------------------ 2 · Olmedo
y += PANEL_H
s = Seccion(y, 20, u"2 · CALLE OLMEDO  ·  20,00 m  ·  «la calle de los mecánicos»",
            u"Colectora. Adoquín, no asfalto: el adoquín se levanta y se vuelve a poner, "
            u"que es lo que hace falta en una calle donde se abren zanjas todo el tiempo.")
s.suelo("adoquin")
s.edificio(-10, -7, 7.25)
s.edificio(7, 10, 5.0, portal=2.2)
s.vereda(-10, -6)
s.calzada(-6, 6, "adoquin", u"12,00 m calzada")
s.vereda(6, 10)
s.arbol(7.6, 3.4, 3.0)
s.arbol(-7.6, 3.2, 2.6)
s.poste(-6.6, 7.6, brazo=1.4)
s.cota(-10, -6, -1.75, u"4,00")
s.cota(6, 10, -1.75, u"4,00")
s.total(u"20,00 m")
d.text((MARG + 40 * PX + 30, y - 150),
       u"Almendro cada 17 m, alternado a los dos\nlados. Copa baja y ancha: da sombra sobre\nla vereda, que es donde esperan los clientes.\n\n"
       u"Frente al toldo del taller NO se planta.\nAhí el árbol tapaba la toma.",
       font=f_med, fill="#5a554c", spacing=6)

# ------------------------------------------------------------------ 3 · local
y += PANEL_H
s = Seccion(y, 12, u"3 · CALLE LOCAL  ·  12,00 m",
            u"Local. Lastre compactado, sin asfaltar. Es la mayoría de las calles del pueblo y "
            u"la razón del polvo en verano y del barro de enero a abril.")
s.suelo("lastre")
s.edificio(-6, -3.2, 3.5)
s.edificio(3.2, 6, 6.3)
s.vereda(-6, -3.5, 0.13)
s.calzada(-3.5, 3.5, "lastre", u"7,00 m calzada")
s.vereda(3.5, 6, 0.13)
s.arbol(-4.6, 3.0, 2.2, "#3f6236", "#6b5b47")
s.poste(4.7, 7.2, brazo=-1.2)
s.cota(-6, -3.5, -1.75, u"2,50")
s.cota(3.5, 6, -1.75, u"2,50")
s.total(u"12,00 m")
d.text((MARG + 40 * PX + 30, y - 150),
       u"Mango en las esquinas, no en la mitad de\nla cuadra: en 2,50 m de vereda un árbol\ncada 20 m no deja pasar a nadie.\n\n"
       u"Alumbrado en el mismo poste de la luz,\ncada 60 m. Es lo que se hace y se ve.",
       font=f_med, fill="#5a554c", spacing=6)

# ------------------------------------------------------------------ 4 · pasaje
y += PANEL_H
s = Seccion(y, 5, u"4 · PASAJE LA ESPERANZA  ·  5,00 m",
            u"Peatonal, entre la Calle Olmedo y la 10 de Agosto. Adoquín de vereda a vereda, "
            u"sin bordillo. Aquí está la puerta gris del Cuarto.")
s.suelo("adoquin")
s.edificio(-2.5, -0.6, 7.25)
s.edificio(0.6, 2.5, 4.2)
s.calzada(-2.5, 2.5, "adoquin", u"5,00 m, sin bordillo")
s.r(-2.35, 0.14, -1.75, 4.0, "#6f7479")            # la puerta gris del Cuarto
d.text(s.Q(-2.05, 4.55), u"puerta gris", font=f_min, fill="#b3261e", anchor="mb")
d.text(s.Q(-2.05, 4.25), u"del Cuarto", font=f_min, fill="#b3261e", anchor="mb")
s.poste(0.2, 4.4, brazo=0)
s.total(u"5,00 m")
d.text((MARG + 40 * PX + 30, y - 150),
       u"Sin arbolado: no cabe, y además el pasaje\ntiene que quedar oscuro.\n\n"
       u"Tres faroles, y SOLO FUNCIONA EL DE LA\nPUERTA GRIS. Los otros dos están quemados\ny nadie los cambia. Lo fija la biblia.",
       font=f_med, fill="#5a554c", spacing=6)

# ------------------------------------------------------------------ cajetin
d.rectangle([0, 0, AN, 150], fill="#eae5d8")
d.line([(0, 150), (AN, 150)], fill=TINTA, width=3)
d.text((MARG, 36), u"EL CRUCE · SECCIONES DE VÍA", font=f_tit, fill=TINTA)
d.text((MARG, 92), u"Escala 1:100 · medidas en metros · los anchos totales salen del plano urbano y no se tocan",
       font=f_sub, fill="#5a554c")

# tabla resumen
tx = MARG + 40 * PX + 30
ty = 200
d.text((tx, ty - 26), u"RESUMEN DE LA PROPUESTA", font=f_cap, fill=TINTA)
filas = [(u"Vía", u"Ancho", u"Pavimento", u"Árbol", u"Alumbrado"),
         (u"Av. El Cruce", u"40,00", u"asfalto", u"ceibo / 22 m", u"doble, 9,20 m"),
         (u"Calle Olmedo", u"20,00", u"adoquín", u"almendro / 17 m", u"simple, 7,60 m"),
         (u"Calles locales", u"12,00", u"lastre", u"mango en esquina", u"en poste, 7,20 m"),
         (u"Pasaje", u"5,00", u"adoquín", u"ninguno", u"un farol, y quemado")]
anchos = [150, 70, 110, 160, 160]
for i, fila in enumerate(filas):
    cx = tx
    for j, celda in enumerate(fila):
        d.rectangle([cx, ty, cx + anchos[j], ty + 30], fill="#e6e1d2" if i == 0 else None,
                    outline="#a8a294", width=1)
        d.text((cx + 8, ty + 7), celda, font=f_peq if i else fuente("sans_bold", 13),
               fill=TINTA if i else "#3a352c")
        cx += anchos[j]
    ty += 30

d.line([(0, AL - 120), (AN, AL - 120)], fill=TINTA, width=2)
d.multiline_text((MARG, AL - 104),
                 u"PENDIENTE DE VALIDAR: los anchos mínimos de vereda y el retiro frontal los fija la ordenanza del cantón, "
                 u"que no se ha consultado. Lo dibujado cumple lo que se considera razonable\n"
                 u"para un pueblo costeño y es compatible con la traza que ya estaba en el plano urbano. "
                 u"El bombeo de la calzada y el drenaje van al plano de saneamiento, que no existe todavía.",
                 font=f_peq, fill="#5a554c", spacing=7)

im.save(destino("10-secciones-viales.png"))
print(u"10-secciones-viales.png  %d x %d" % (AN, AL))
