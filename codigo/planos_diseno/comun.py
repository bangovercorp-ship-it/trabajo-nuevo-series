# -*- coding: utf-8 -*-
"""Utilidades comunes a los tres planos: fuentes y carpeta de salida.

Los planos tienen que dibujarse igual en la maquina de trabajo (Windows) y en una
sesion en la nube (Linux). Las unicas dos diferencias son donde estan las fuentes
y donde se guarda el PNG, y las resuelve este modulo.

En Windows no cambia nada: usa las fuentes de siempre y guarda donde siempre.
"""
import os

from PIL import ImageFont

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
