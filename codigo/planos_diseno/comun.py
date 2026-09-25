# -*- coding: utf-8 -*-
"""Utilidades comunes a los tres planos: fuentes y carpeta de salida.

Los planos tienen que dibujarse igual en la maquina de trabajo (Windows) y en una
sesion en la nube (Linux). Las unicas dos diferencias son donde estan las fuentes
y donde se guarda el PNG, y las resuelve este modulo.

En Windows no cambia nada: usa las fuentes de siempre y guarda donde siempre.
"""
import math
import os

from PIL import ImageDraw, ImageFont

# ---------------------------------------------------------------- salida
# Se puede forzar con la variable de entorno PLANOS_SALIDA.
SALIDA = os.environ.get("PLANOS_SALIDA") or (
    r"C:\pesonajes para videos\planos_diseno" if os.name == "nt"
    else os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida")
)


def destino(nombre):
    """Ruta completa del PNG de salida, creando la carpeta si hace falta."""
    os.makedirs(SALIDA, exist_ok=True)
    return os.path.join(SALIDA, nombre)


# ---------------------------------------------------------------- fuentes
# Liberation es metricamente igual a Arial, y Liberation Serif reemplaza a Georgia.
_PISTAS = {
    "sans": ["C:/Windows/Fonts/arial.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "sans_bold": ["C:/Windows/Fonts/arialbd.ttf",
                  "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "serif": ["C:/Windows/Fonts/georgia.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
    "serif_bold": ["C:/Windows/Fonts/georgiab.ttf",
                   "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
}


def fuente(clase, tam):
    for ruta in _PISTAS[clase]:
        if os.path.exists(ruta):
            return ImageFont.truetype(ruta, tam)
    raise FileNotFoundError("no hay ninguna fuente %r disponible" % clase)


# ---------------------------------------------------------------- elevaciones
# Paleta comun a los planos de fachada. El taller y el bar comparten el zocalo del
# nivel +0,40, la marca de agua, el zinc y la vereda: si se dibujan por separado se
# separan con el tiempo, y entonces los escenarios dejan de pegar entre si.
TINTA = "#26221e"
ONIX, CREMA, ORO = "#1d1b19", "#efe6d2", "#b8923a"
VERDE_BAR, GATA = "#1f4d3a", "#e0529a"
BLOQUE, ZINC, VEREDA = "#b9b3a6", "#8f959b", "#9e9a92"
BRASA, NUEVO, AGUA = "#b3261e", "#1d6a6a", "#5c6a5c"


class Elevacion:
    """Un panel de fachada. (0,0) es el pie de la cara y z crece hacia arriba.

    El rotulo se dibuja con rotulo(), AL FINAL: si se dibuja antes, el edificio lo
    tapa. Es el error que costo dos pasadas la primera vez.
    """

    def __init__(self, d, ox, oy, largo, px, titulo, sub, fuentes):
        self.d, self.ox, self.oy, self.largo, self.px = d, ox, oy, largo, px
        self.titulo, self.sub = titulo, sub
        self.f = fuentes              # dict con cara, med, peq, min

    def Q(self, x, z):
        return (self.ox + x * self.px, self.oy - z * self.px)

    def r(self, x0, z0, x1, z1, fill, out=TINTA, w=2):
        self.d.rectangle([self.Q(x0, z1), self.Q(x1, z0)], fill=fill, outline=out, width=w)

    def t(self, x, z, s, f=None, fill=TINTA, a="mm"):
        self.d.text(self.Q(x, z), s, font=f or self.f["peq"], fill=fill, anchor=a)

    def base(self, color, alto, filete=True, zocalo="#2f2c29"):
        """vereda, zocalo del +0,40, cuerpo y marca de agua"""
        L = self.largo
        self.r(-1.2, -0.45, L + 1.2, 0, VEREDA, None)
        self.r(0, 0, L, alto, color)
        if filete:
            for z in (0.05, alto - 0.05):
                self.d.line([self.Q(0, z), self.Q(L, z)], fill=ORO, width=3)
        self.r(0, 0, L, 0.4, zocalo, ORO if filete else TINTA, 2)
        self.d.line([self.Q(0, 0.95), self.Q(L, 0.95)], fill=AGUA, width=2)
        self.t(L - 0.2, 1.22, "marca de agua", self.f["min"], AGUA if filete else "#5f6b5f", "rm")
        self.d.line([self.Q(-1.2, -0.13), self.Q(L + 1.2, -0.13)], fill="#6f6a63", width=4)

    def zinc(self, z0, z1, x0=None, x1=None):
        x0 = 0 if x0 is None else x0
        x1 = self.largo if x1 is None else x1
        self.r(x0 - 0.4, z0, x1 + 0.4, z1, ZINC)
        for k in range(int((x1 - x0 + 0.8) / 0.5) + 1):
            xx = x0 - 0.4 + k * 0.5
            self.d.line([self.Q(xx, z0), self.Q(xx, z1)], fill="#6f767c", width=1)

    def turbina(self, x, z0):
        self.r(x - 0.12, z0 - 0.3, x + 0.12, z0, "#7d858c", None)
        self.d.ellipse([self.Q(x - 0.45, z0 + 0.9), self.Q(x + 0.45, z0)],
                       fill="#b9c0c6", outline=TINTA, width=2)
        for k in range(6):
            a = k * math.pi / 3
            self.d.line([self.Q(x, z0 + 0.45),
                         self.Q(x + 0.45 * math.cos(a), z0 + 0.45 + 0.45 * math.sin(a))],
                        fill="#7d858c", width=2)

    def reja(self, x0, z0, x1, z1, paso=0.22, col="#9fb0a6"):
        k = 0
        while x0 + k * paso < x1:
            self.d.line([self.Q(x0 + k * paso, z0), self.Q(x0 + k * paso, z1)], fill=col, width=2)
            k += 1

    def cota_x(self, x0, x1, z, s):
        self.d.line([self.Q(x0, z), self.Q(x1, z)], fill=TINTA, width=1)
        for x in (x0, x1):
            self.d.line([self.Q(x, z - 0.18), self.Q(x, z + 0.18)], fill=TINTA, width=2)
        self.t((x0 + x1) / 2, z - 0.42, s, self.f["med"])

    def cota_z(self, z0, z1, x, s):
        self.d.line([self.Q(x, z0), self.Q(x, z1)], fill=TINTA, width=1)
        for z in (z0, z1):
            self.d.line([self.Q(x - 0.16, z), self.Q(x + 0.16, z)], fill=TINTA, width=2)
        p = self.Q(x, (z0 + z1) / 2)
        self.d.text((p[0] + 9, p[1]), s, font=self.f["med"], fill=TINTA, anchor="lm")

    def rotulo(self):
        self.d.text((self.ox, self.oy - 330), self.titulo, font=self.f["cara"], fill=TINTA)
        self.d.text((self.ox, self.oy - 296), self.sub, font=self.f["peq"], fill=TINTA)
