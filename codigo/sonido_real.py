# -*- coding: utf-8 -*-
"""Diseno de sonido con grabaciones reales de Freesound (todas CC0).

Cada muestra se recorta, se normaliza a la misma sonoridad y se coloca con
una ganancia en dB. Asi la mezcla se equilibra por oido, no por accidente.
"""
import os, wave
import numpy as np

SR = 48000
OFFSET = 1.50              # la apertura en caliente va antes de que hable la voz
DUR = 53.20 + OFFSET       # y 1,5 s despues de la voz: el gallo canta limpio
SON = r"C:\pesonajes para videos\sonidos"
SALIDA = r"C:\pesonajes para videos\efectos.wav"
bed = np.zeros(int(DUR * SR))
_cache = {}


def cargar(nombre):
    if nombre not in _cache:
        w = wave.open(os.path.join(SON, nombre + ".wav"))
        _cache[nombre] = np.frombuffer(w.readframes(w.getnframes()),
                                       dtype=np.int16).astype(float) / 32768
    return _cache[nombre]


def muestra(nombre, desde=0.0, hasta=None, entra=0.01, sale=0.05, tono=1.0):
    """recorta, suaviza bordes y normaliza a -20 dBFS de RMS"""
    d = cargar(nombre)
    a, b = int(desde * SR), int((hasta if hasta else len(d) / SR) * SR)
    x = d[a:b].copy()
    if tono != 1.0:                            # mas grave = mas espeso
        idx = np.arange(0, len(x) - 1, tono)
        x = np.interp(idx, np.arange(len(x)), x)
    fe, fs = int(entra * SR), int(sale * SR)
    if fe:
        x[:fe] *= np.linspace(0, 1, fe)
    if fs:
        x[-fs:] *= np.linspace(1, 0, fs)
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    x = x * (10 ** (-20 / 20) / rms)
    pico = np.max(np.abs(x))
    return x * (0.35 / pico) if pico > 0.35 else x   # tope para golpes secos


def poner(x, cuando, db=0.0, absoluto=False):
    """cuando va en tiempo de la voz; absoluto=True es tiempo del video"""
    i = int((cuando if absoluto else cuando + OFFSET) * SR)
    if i >= len(bed):
        return
    j = min(i + len(x), len(bed))
    bed[i:j] += x[:j - i] * (10 ** (db / 20))


def zumbido_motor(dur):
    """la presion de estar dentro del bloque: aca no hay grabacion posible"""
    x = np.linspace(0, dur, int(dur * SR), endpoint=False)
    y = np.sin(2 * np.pi * 42 * x) + 0.55 * np.sin(2 * np.pi * 63 * x)
    y *= 1 + 0.22 * np.sin(2 * np.pi * 0.6 * x)
    borde = np.minimum(np.minimum(x / 0.6, (dur - x) / 0.6), 1)
    y = y * borde
    return y * (0.1 / (np.sqrt(np.mean(y ** 2)) + 1e-9))


# --- ambiente ----------------------------------------------------------------
poner(muestra("zumbido-sala", 0.0, 15.68, 0.8, 0.6), 0.00, -20)       # el taller
poner(muestra("zumbido-sala", 2.0, 12.72, 0.5, 1.2), 42.48, -20)

# --- 0 a 7: el gallo y la gasolina ---------------------------------------------
poner(muestra("impacto", 1.58, 3.4, 0.0, 0.9), 0.00, -3)               # golpe de entrada
poner(muestra("aleteo"), 1.80, -10)                                   # gira a camara
poner(muestra("whoosh"), 3.42, -8)
poner(muestra("vertido", 0.0, 2.8, 0.05, 0.4), 3.75, -3)              # gasolina turbia
poner(muestra("vertido", 0.6, 2.8, 0.2, 0.5, tono=0.85), 5.60, -7)

# --- 7 a 13: las tres patadas que no prenden ---------------------------------
poner(muestra("whoosh"), 7.08, -8)
for cuando, grunido in ((7.86, (11.0, 11.5)), (9.46, (4.0, 4.5)), (11.06, (19.4, 19.9))):
    poner(muestra("chancho-gruñidos", *grunido, 0.02, 0.1), cuando - 0.42, -7)   # esfuerzo
    poner(muestra("kickstart-rev", 0.0, 0.55, 0.0, 0.30), cuando, -3)            # patada y tos
    poner(muestra("no-arranca", 1.15, 1.75, 0.02, 0.30), cuando + 0.15, -9)      # se ahoga
poner(muestra("chancho-gruñidos", 17.1, 17.9, 0.05, 0.3), 12.25, -6)  # se rinde

# --- 13 a 16: el gallo lo sermonea -------------------------------------------
poner(muestra("golpe-dramatico", 0.25, 1.5, 0.0, 0.6), 12.86, -8)
poner(muestra("aleteo"), 13.05, -9)
poner(muestra("chancho-gruñidos", 15.2, 15.6, 0.02, 0.1), 13.75, -3)
poner(muestra("chancho-grunt"), 14.95, -3)

# --- 15 a 30: adentro del motor ------------------------------------------------
poner(muestra("woosh-largo"), 15.10, -8)
poner(zumbido_motor(23.00 - 15.68), 15.68, -6)
poner(muestra("metal-arrastre", 0.0, 2.2, 0.1, 0.5, tono=0.8), 16.20, -16)       # la carbonilla
poner(muestra("brillo", 0.0, 0.9, 0.0, 0.5), 19.36, -20)
poner(muestra("impacto", 1.58, 2.8, 0.0, 0.7), 20.80, -9)
poner(muestra("metal-arrastre", 0.0, 2.2, 0.02, 0.3), 20.84, -9)                 # valvulas secas
poner(muestra("semillas", 0.3, 2.3, 0.1, 0.5), 23.10, -2)                       # el polvo de maca
poner(muestra("impacto", 1.58, 2.6, 0.0, 0.6), 25.26, -10)
poner(muestra("plop"), 25.48, -4)                                                # la gomita cae
poner(muestra("vertido", 0.0, 2.8, 0.1, 0.8, tono=0.7), 26.55, -4)               # aceite espeso
poner(muestra("brillo", 0.0, 1.8, 0.1, 1.0), 27.10, -18)

# --- 30 a 35: el filtro --------------------------------------------------------
poner(muestra("impacto", 1.58, 2.6, 0.0, 0.6), 29.96, -10)
poner(muestra("semillas", 2.0, 4.0, 0.1, 0.5), 30.15, -11)                       # achiote
poner(muestra("brillo", 0.0, 2.2, 0.0, 1.2), 32.35, -7)                         # filtro limpio
poner(muestra("riser", 0.0, 3.0, 0.2, 0.05), 32.00, -9)                          # sube al presagio

# --- 35 a 42,5: el futuro malo -------------------------------------------------
poner(muestra("woosh-largo"), 34.40, -8)
poner(muestra("golpe-dramatico", 0.25, 2.8, 0.0, 1.5), 34.98, -4)
poner(muestra("bmw-start-stop", 0.8, 4.2, 0.02, 1.2), 35.00, -6)                 # motor apagandose
poner(muestra("sputter", 0.3, 2.6, 0.05, 0.8), 35.40, -12)                       # y tosiendo
poner(muestra("vapor", 0.0, 7.3, 0.3, 1.0), 35.30, -15)                          # el vapor
poner(muestra("viento", 0.0, 7.5, 1.0, 1.0), 35.00, -11)                         # carretera vacia
poner(muestra("grava", 0.0, 3.8, 0.2, 0.6), 38.70, -10)                          # pisadas
poner(muestra("chancho-gruñidos", 12.3, 13.0, 0.05, 0.2), 39.60, -12)            # jadeos
poner(muestra("chancho-gruñidos", 18.3, 18.7, 0.05, 0.2), 41.20, -12)

# --- 42,5 a 48: vuelta al taller y el frasco ----------------------------------
poner(muestra("whoosh"), 42.28, -8)
poner(muestra("impacto", 1.58, 3.0, 0.0, 0.8), 42.44, -6)
poner(muestra("vapor", 5.0, 7.0, 0.1, 1.5), 42.55, -20)                          # humo disipandose
poner(muestra("aleteo"), 43.40, -11)
poner(muestra("brillo", 0.0, 1.4, 0.0, 0.8), 45.10, -20)                         # tanque pulido
poner(muestra("riser", 0.0, 3.0, 0.2, 0.05), 44.83, -8)                          # sube al frasco
poner(muestra("whoosh"), 47.40, -7)
poner(muestra("frasco-mesa"), 47.58, -4)                                         # el frasco apoya
poner(muestra("brillo", 0.0, 1.6, 0.0, 0.9), 47.62, -14)

# --- 48,3 al final: arranca, ruge y el gallo canta ----------------------------
poner(muestra("kickstart-rev", 0.0, 4.4, 0.0, 0.8), 48.30, 4)                   # patada, prende, sube
poner(muestra("harley-vintage", 2.4, 6.4, 0.4, 1.4), 50.20, 0)                  # el rugido crece
poner(muestra("gallo", 0.0, 2.2, 0.0, 0.2), 51.05, -3)                           # kikiriki limpio


# --- la apertura en caliente: el desastre primero (tiempo absoluto) ----------
poner(muestra("braam", 0.95, 4.5, 0.0, 1.5), 0.00, -1, absoluto=True)          # golpe al primer cuadro
poner(muestra("viento", 8.0, 9.6, 0.1, 0.3), 0.00, -12, absoluto=True)
poner(muestra("vapor", 1.0, 2.5, 0.1, 0.3), 0.05, -14, absoluto=True)
poner(muestra("chancho-gruñidos", 12.3, 13.0, 0.02, 0.2), 0.75, -9, absoluto=True)
poner(muestra("whoosh"), 0.62, -6, absoluto=True)                               # corte entre flashes
poner(muestra("woosh-largo"), 1.05, -8, absoluto=True)                          # al negro

# --- la capa de suspenso -------------------------------------------------------
poner(muestra("tension", 9.5, 15.5, 1.5, 0.05), 29.00, -10)                     # sube hasta el presagio
poner(muestra("braam-corto", 0.0, 3.3, 0.0, 0.8), 33.25, -5)                    # cae en 35,0
poner(muestra("latido", 0.0, 7.5, 0.4, 1.0), 35.00, -9)                         # el miedo del futuro malo
poner(muestra("sub", 0.0, 2.4, 0.3, 0.05), 45.43, -6)                           # el grave que llega al frasco

# --- a disco -----------------------------------------------------------------
pico = float(np.max(np.abs(bed)))
bed = bed / pico * 0.5 if pico > 0.5 else bed
with wave.open(SALIDA, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(bed, -1, 1) * 32767).astype(np.int16).tobytes())
print("listo:", SALIDA, "| %.2f s | pico %.2f" % (DUR, pico))
