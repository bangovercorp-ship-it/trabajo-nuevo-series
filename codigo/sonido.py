# -*- coding: utf-8 -*-
"""Diseno de sonido del spot. Efectos literales, sin una nota de musica.

Todo sintetizado con numpy. Lo importante:
- el motor es un V-twin de verdad: tren de explosiones desparejo pasado por
  resonadores, con la mezcla de admision subiendo con las vueltas.
- las voces de los animales son fuente armonica con jitter mas formantes.
Los tiempos salen de las marcas de la locucion, palabra por palabra.
"""
import wave
import numpy as np

SR = 48000
DUR = 51.70
SALIDA = r"C:\pesonajes para videos\efectos.wav"
rng = np.random.default_rng(11)
bed = np.zeros(int(DUR * SR))


def t(dur):
    return np.linspace(0, dur, int(dur * SR), endpoint=False)


def n(dur):
    return rng.uniform(-1, 1, int(dur * SR))


def lp(x, fc, orden=2):
    """pasa bajos por fft: rapido y limpio incluso en senales largas"""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** (2 * orden)), n=len(x))


def hp(x, fc, orden=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / SR)
    r = (f / fc) ** orden
    return np.fft.irfft(X * r / np.sqrt(1 + r ** 2), n=len(x))


def bp(x, lo, hi):
    return lp(hp(x, lo), hi)


def resonar(x, f, q=12.0, g=1.0):
    """realza una banda: asi se hacen los formantes de una garganta"""
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1.0 / SR)
    campana = g / (1 + ((fr - f) / (f / q)) ** 2)
    return np.fft.irfft(X * (1 + campana), n=len(x))


def sobre(dur, ataque, caida, sostiene=1.0):
    """envolvente ataque / sostenido / caida"""
    x = t(dur)
    a = np.clip(x / max(ataque, 1e-4), 0, 1)
    c = np.clip((dur - x) / max(caida, 1e-4), 0, 1)
    return np.minimum(a, c) * sostiene


def decae(dur, tau):
    return np.exp(-t(dur) / tau)


def suave(x, ventana):
    k = np.ones(int(ventana * SR)) / int(ventana * SR)
    return np.convolve(x, k, mode="same")


def poner(x, cuando, vol=1.0):
    i = int(cuando * SR)
    if i >= len(bed):
        return
    j = min(i + len(x), len(bed))
    bed[i:j] += x[:j - i] * vol


# --- el motor ----------------------------------------------------------------

def motor(vueltas, aspereza=1.0):
    """V-twin. 'vueltas' son las rpm cuadro a cuadro; de ahi sale todo lo demas.

    Un bicilindrico en V enciende desparejo: por eso el 'potato-potato'.
    Se generan los impulsos de explosion y se excita un banco de resonadores.
    """
    dur = len(vueltas) / SR
    fase = np.cumsum(vueltas / 60.0 / SR)          # revoluciones acumuladas
    imp = np.zeros(len(vueltas))
    for desfase in (0.0, 0.45):                    # las dos explosiones, desparejas
        k = np.floor(fase - desfase).astype(np.int64)
        salto = np.empty(len(k), dtype=bool)
        salto[0] = False
        salto[1:] = k[1:] > k[:-1]
        imp[salto] = 1.0
    imp *= rng.uniform(0.75, 1.0, len(imp))        # ninguna explosion es igual

    kt = t(0.07)
    nucleo = (np.sin(2 * np.pi * 88 * kt) * np.exp(-kt / 0.014)
              + 0.70 * np.sin(2 * np.pi * 176 * kt) * np.exp(-kt / 0.009)
              + 0.40 * np.sin(2 * np.pi * 305 * kt) * np.exp(-kt / 0.005)
              + 0.22 * np.sin(2 * np.pi * 520 * kt) * np.exp(-kt / 0.003))
    nucleo += aspereza * 0.55 * rng.uniform(-1, 1, len(kt)) * np.exp(-kt / 0.0035)

    y = np.convolve(imp, nucleo)[:len(vueltas)]
    admision = lp(n(dur), 500) * (vueltas / max(vueltas.max(), 1)) * 0.40 * aspereza
    return y * 0.9 + admision


def arranque_fallido(dur=1.15):
    """la patada: el motor gira dos o tres veces, tose y se apaga"""
    v = np.concatenate([
        np.linspace(60, 430, int(0.16 * SR)),      # la patada lo lanza
        np.linspace(430, 300, int(0.30 * SR)),     # da dos vueltas
        np.linspace(300, 90, int(0.40 * SR)),      # se ahoga
        np.linspace(90, 0, int(dur * SR) - int(0.86 * SR)),
    ])
    y = motor(v, aspereza=1.3) * np.concatenate([
        np.ones(int(0.60 * SR)), np.linspace(1, 0, len(v) - int(0.60 * SR))])
    golpe = bp(n(0.05), 900, 7000) * np.exp(-t(0.05) / 0.008)   # el fierro del pedal
    y[:len(golpe)] += golpe * 1.1
    return y


def arranca_y_ruge(dur):
    """prende, se estabiliza y sube de vueltas hasta el final"""
    tramos = [(0.18, 60, 500), (0.12, 500, 950), (0.55, 950, 880),
              (0.95, 880, 3100), (0.60, 3100, 2600)]
    v = [np.linspace(a, b, int(d * SR)) for d, a, b in tramos]
    v = np.concatenate(v)
    if len(v) < int(dur * SR):
        v = np.concatenate([v, np.full(int(dur * SR) - len(v), 2600.0)])
    v = v[:int(dur * SR)]
    y = motor(v, aspereza=1.1)
    return y * np.minimum(t(dur) / 0.05, 1) * np.linspace(0.75, 1.15, len(v))


def agoniza(dur=1.6):
    """el motor fundiendose: metal rayando y el golpe seco de la biela"""
    v = np.linspace(950, 0, int(dur * SR))
    y = motor(v, aspereza=1.6) * np.linspace(1, 0.2, int(dur * SR))
    raya = bp(n(dur), 1400, 6500) * sobre(dur, 0.05, 0.9) * 0.55
    raya *= 0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 7 * t(dur)))
    seco = np.sin(2 * np.pi * 70 * t(0.4)) * decae(0.4, 0.06)
    y = y + raya
    y[int(1.0 * SR):int(1.0 * SR) + len(seco)] += seco * 0.9
    return y


# --- los animales ------------------------------------------------------------

def voz(dur, f0, formantes, jitter=0.05, armonicos=14):
    """fuente armonica con temblor + formantes: sirve para cualquier garganta"""
    x = t(dur)
    f = f0 * (1 + jitter * suave(rng.uniform(-1, 1, len(x)), 0.004))
    fase = 2 * np.pi * np.cumsum(f) / SR
    y = sum(np.sin(k * fase) / (k ** 0.85) for k in range(1, armonicos + 1))
    y += 0.25 * lp(n(dur), 3000)                    # aire de la garganta
    for fr, g in formantes:
        y = resonar(y, fr, q=9, g=g)
    return y


def chancho(clase="gruñido"):
    """gruñidos del chancho: esfuerzo, queja o resoplido"""
    if clase == "esfuerzo":
        dur, f0 = 0.55, 165
        y = voz(dur, f0, [(480, 4), (1150, 2.2)], jitter=0.10)
        y *= sobre(dur, 0.06, 0.18) * (0.7 + 0.3 * np.sin(2 * np.pi * 5 * t(dur)))
    elif clase == "queja":
        dur = 0.42
        f = np.linspace(255, 195, int(dur * SR))
        y = voz(dur, 1.0, [(520, 4), (1250, 2.0)], jitter=0.07)
        y = voz(dur, f, [(520, 4), (1250, 2.0)], jitter=0.07)
        y *= sobre(dur, 0.05, 0.22)
    else:                                            # resoplido por la nariz
        dur = 0.30
        y = bp(n(dur), 400, 3200) * sobre(dur, 0.02, 0.20)
        y = resonar(y, 900, q=6, g=3)
    return y


def gallo_canta(dur=1.60):
    """ki-ki-ri-kiiii. Un gallo real es ronco, no un sintetizador: la mitad de
    lo que sale de esa garganta es ruido, y el borde se satura."""
    y = np.zeros(int(dur * SR))
    tramos = [(0.00, 0.15, 520, 560), (0.19, 0.33, 590, 570),
              (0.37, 0.54, 500, 460), (0.60, 1.48, 700, 545)]
    for a, b, fa, fb in tramos:
        d = b - a
        f = np.linspace(fa, fb, int(d * SR))
        if d > 0.5:                                  # el grito final se quiebra
            f = f * (1 + 0.045 * np.sin(2 * np.pi * 6.5 * t(d)))
            f *= np.concatenate([np.ones(int(len(f) * 0.7)),
                                 np.linspace(1, 0.88, len(f) - int(len(f) * 0.7))])
        tono = voz(d, f, [(820, 3.5), (1900, 2.2)], jitter=0.06, armonicos=9)
        # el aire rasposo: ruido que sigue la misma envolvente
        aire = bp(n(d), 600, 4800) * (0.55 + 0.45 * np.sin(2 * np.pi * f * 0 + 1))
        s = tono * 0.55 + aire * 0.75
        s = np.tanh(s * 1.8) / 1.8                   # satura: de ahi sale lo ronco
        s = lp(s, 4600)
        s *= sobre(d, 0.025, min(0.22, d * 0.5))
        y[int(a * SR):int(a * SR) + len(s)] += s
    return y


def subidon(dur=1.6):
    """el riser antes de una revelacion: ruido que sube y se abre"""
    x = t(dur)
    fc = 300 * (5000 / 300) ** (x / dur)
    a = np.exp(-2 * np.pi * fc / SR)
    ru = n(dur)
    y = np.empty_like(ru)
    acc = 0.0
    for i in range(len(ru)):
        acc = a[i] * acc + (1 - a[i]) * ru[i]
        y[i] = acc
    tono = np.sin(2 * np.pi * np.cumsum(np.linspace(110, 900, len(x))) / SR) * 0.35
    return (y + tono) * (x / dur) ** 2.2


def impacto(dur=0.9):
    """el golpe del corte seco: sub grave + aire"""
    x = t(dur)
    sub = np.sin(2 * np.pi * np.linspace(90, 38, len(x)) * x) * np.exp(-x / 0.13)
    aire = bp(n(dur), 400, 9000) * np.exp(-x / 0.05) * 0.5
    cola = lp(n(dur), 180) * np.exp(-x / 0.30) * 0.35
    return sub + aire + cola


def plumas(dur=0.35):
    """el roce de las plumas cuando se sacude"""
    y = bp(n(dur), 1200, 9000) * sobre(dur, 0.02, 0.22)
    return y * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 13 * t(dur))))


# --- el mundo ----------------------------------------------------------------

def viento(dur):
    x = t(dur)
    base = lp(n(dur), 420)
    silbo = bp(n(dur), 700, 2600) * 0.35
    rafaga = 0.55 + 0.45 * suave(rng.uniform(0, 1, len(x)), 0.8)
    return (base + silbo) * rafaga * sobre(dur, 1.2, 1.2)


def empuja_moto(dur, paso=0.66):
    """pisadas en la grava, la rueda rodando y el respirar cansado"""
    y = lp(n(dur), 150) * 0.5                        # la rueda
    y *= 0.7 + 0.3 * np.sin(2 * np.pi * 1.6 * t(dur))
    for cuando in np.arange(0.15, dur - 0.2, paso):  # pisadas
        cru = bp(n(0.13), 700, 6000) * np.exp(-t(0.13) / 0.022)
        i = int(cuando * SR)
        y[i:i + len(cru)] += cru[:len(y) - i] * rng.uniform(0.7, 1.0)
    for cuando in np.arange(0.5, dur - 0.5, 1.5):    # resoplidos
        s = chancho("resoplido") * 0.5
        i = int(cuando * SR)
        y[i:i + len(s)] += s[:len(y) - i]
    return y * sobre(dur, 0.3, 0.5)


def humo(dur):
    """el vapor saliendo del motor reventado"""
    y = hp(n(dur), 1600) * 0.6
    x = t(dur)
    return y * (0.35 + 0.65 * suave(rng.uniform(0, 1, len(x)), 0.5)) * sobre(dur, 0.25, 0.8)


def taller(dur):
    """el zumbido de fondo del taller: fluorescentes y aire quieto"""
    return (lp(n(dur), 120) * 0.8 + np.sin(2 * np.pi * 50 * t(dur)) * 0.10) * sobre(dur, 1.0, 1.0)


def chorro(dur, espeso=False):
    y = lp(n(dur), 700 if espeso else 1500)
    x = t(dur)
    burbuja = np.zeros(len(x))
    for cuando in np.arange(0.1, dur - 0.1, 0.11):   # el glugluteo
        b = np.sin(2 * np.pi * rng.uniform(180, 420) * t(0.05)) * decae(0.05, 0.012)
        i = int((cuando + rng.uniform(0, 0.04)) * SR)
        burbuja[i:i + len(b)] += b[:len(burbuja) - i]
    return (y + burbuja * 0.5) * sobre(dur, 0.25, 0.4)


def zumbido_motor(dur):
    """estar adentro del bloque: presion y metal"""
    x = t(dur)
    y = np.sin(2 * np.pi * 42 * x) + 0.55 * np.sin(2 * np.pi * 63 * x)
    y *= 1 + 0.22 * np.sin(2 * np.pi * 0.6 * x)
    return y * sobre(dur, 0.6, 0.6)


def raspado(dur):
    y = bp(n(dur), 1800, 5600)
    rasp = 0.3 + 0.7 * (np.abs(((t(dur) * 8.5) % 1) - 0.5) * 2)
    return y * rasp * sobre(dur, 0.12, 0.25)


def whoosh(dur=0.45, subiendo=True):
    x = n(dur)
    fc = np.linspace(300, 6500, len(x)) if subiendo else np.linspace(6500, 300, len(x))
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = a[i] * acc + (1 - a[i]) * x[i]
        y[i] = acc
    return y * (np.sin(np.pi * np.linspace(0, 1, len(y))) ** 1.5)


def golpe_seco(dur=0.45, f=62):
    cuerpo = np.sin(2 * np.pi * f * t(dur)) * decae(dur, 0.08)
    click = hp(n(0.012), 1800) * np.linspace(1, 0, int(0.012 * SR))
    cuerpo[:len(click)] += click * 0.7
    return cuerpo


def tilin(dur=0.55):
    x = t(dur)
    y = (np.sin(2 * np.pi * 2350 * x) + 0.5 * np.sin(2 * np.pi * 3520 * x)
         + 0.25 * np.sin(2 * np.pi * 4900 * x))
    return y * decae(dur, 0.14)


def destello(dur=1.4):
    y = np.zeros(int(dur * SR))
    for k, f in enumerate([3200, 4300, 5500, 7100]):
        d = np.sin(2 * np.pi * f * t(dur)) * decae(dur, 0.45)
        r = int(k * 0.055 * SR)
        y[r:] += d[:len(y) - r] * (0.88 ** k)
    return y


def plop(dur=0.28):
    x = t(dur)
    f = 460 * np.exp(-x / 0.045) + 105
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * decae(dur, 0.07)


def granos(dur=0.5):
    """semillas y polvo cayendo"""
    y = np.zeros(int(dur * SR))
    for _ in range(45):
        g = bp(n(0.02), 1500, 9000) * np.exp(-t(0.02) / 0.004)
        i = int(rng.uniform(0, dur - 0.03) * SR)
        y[i:i + len(g)] += g * rng.uniform(0.3, 1.0)
    return y * sobre(dur, 0.01, 0.25)


# --- el guion de sonido, pegado a la locucion --------------------------------

# fondo del taller en todas las escenas de taller
for a, b in ((0.0, 15.68), (42.48, 51.70)):
    poner(taller(b - a), a, 0.10)

poner(plumas(), 1.85, 0.75)                     # el gallo gira a camara

poner(whoosh(), 3.45, 0.30)
poner(chorro(3.50), 3.72, 0.90)                 # la gasolina turbia entrando

poner(whoosh(), 7.10, 0.30)
for cuando in (7.86, 9.46, 11.06):              # las tres patadas al arranque
    poner(chancho("esfuerzo"), cuando - 0.30, 0.50)
    poner(arranque_fallido(), cuando, 0.95)
poner(chancho("queja"), 12.35, 0.22)            # se rinde

poner(whoosh(), 12.70, 0.28)
poner(plumas(0.3), 13.05, 0.55)                 # el gallo lo encara
poner(chancho("queja"), 13.70, 0.17)            # el chancho se queja
poner(chancho("resoplido"), 14.90, 0.60)        # y resopla

poner(whoosh(0.7, subiendo=False), 15.38, 0.34)
poner(zumbido_motor(23.00 - 15.68), 15.68, 0.30)
poner(raspado(2.0), 16.10, 0.26)                # la carbonilla
poner(tilin(), 19.36, 0.13)                     # ZINC / MAGNESIO
poner(raspado(23.00 - 20.84), 20.84, 0.50)      # valvulas secas

poner(granos(), 23.20, 1.10)                    # la maca en polvo
poner(tilin(), 23.36, 0.13)
poner(plop(), 25.50, 0.80)                      # la gomita cae al tanque
poner(chorro(3.40, espeso=True), 26.55, 0.80)   # el aceite bajando
poner(destello(1.2), 27.00, 0.14)

poner(granos(0.6), 30.20, 1.00)                 # las semillas de achiote
poner(tilin(), 30.68, 0.13)
poner(destello(), 32.35, 0.30)                  # el filtro quedando limpio

poner(whoosh(0.8, subiendo=False), 34.65, 0.38)
poner(agoniza(), 35.00, 0.55)                   # el motor se funde
poner(humo(42.48 - 35.20), 35.20, 0.60)         # el vapor saliendo
poner(viento(42.48 - 35.00), 35.00, 0.55)       # la carretera vacia
poner(empuja_moto(42.48 - 38.70), 38.70, 0.90)  # el chancho arrastrando

poner(whoosh(), 42.30, 0.30)
poner(humo(1.6), 42.55, 0.45)                   # el humo que se disipa
poner(plumas(0.3), 43.40, 0.55)

poner(destello(1.0), 45.10, 0.18)               # el tanque pulido
poner(whoosh(0.35), 47.43, 0.34)
poner(golpe_seco(0.55, 70), 47.60, 0.65)        # el frasco apoyando
poner(destello(1.0), 47.66, 0.20)

poner(arranca_y_ruge(51.70 - 48.30), 48.30, 0.60)   # el motor rugiendo
poner(gallo_canta(), 50.55, 0.30)                   # y el gallo cantando

# --- los golpes del montaje: cada corte seco y cada zoom rapido tiene sonido ---

poner(impacto(), 0.00, 0.95)                    # el acercamiento de arranque
for cuando in (12.88, 20.84, 25.30, 30.00, 42.48, 48.30):
    poner(impacto(), cuando, 0.80)              # cortes de golpe
poner(subidon(1.9), 33.10, 0.85)                # sube antes del futuro malo
poner(subidon(1.3), 46.28, 0.95)                # sube antes del frasco


# --- a disco -----------------------------------------------------------------

pico = float(np.max(np.abs(bed)))
bed = bed / pico * 0.30 if pico > 0 else bed        # queda por debajo de la voz
datos = (np.clip(bed, -1, 1) * 32767).astype(np.int16)

with wave.open(SALIDA, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(datos.tobytes())

print("listo:", SALIDA, "| pico antes de normalizar %.2f" % pico)
