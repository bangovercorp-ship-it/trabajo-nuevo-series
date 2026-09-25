# -*- coding: utf-8 -*-
"""Monta el spot con lenguaje de cine de accion y suspenso.

Estructura: apertura en caliente (el desastre primero) -> la historia con la voz
-> remate con el gallo cantando y el disparador para compartir.
Por plano: recorte al milisegundo, camara propia, camara lenta o sacudon.
Sobre todo junto: grado de color, viñeta, subtitulos, textos y grano.
"""
import os, subprocess

BASE = r"C:\pesonajes para videos"
PLANOS = os.path.join(BASE, "planos")
TMP = os.path.join(BASE, "tmp")
VOZ = "Generated Audio September 19, 2026 - 8_30PM.wav"
FINAL = os.path.join(BASE, "lazaro-spot.mp4")
ANTON = "fuentes/Anton-Regular.ttf"
ORO = "0xDDAA3F"
OFFSET = 1.50            # lo que dura la apertura en caliente
TOTAL = 53.20 + OFFSET   # la voz termina en 51,14: queda aire para el gallo

# cada plano: nombre, entra, sale (en tiempo de la voz), y opciones:
#   c  = cuadro fijo (png) en vez de clip
#   e  = (encuadre inicial, encuadre final); 1.00 = lo mas cerrado posible
#   r  = camara que arranca rapido y se asienta
#   v  = velocidad (0.5 = camara lenta)
#   s  = sacudones: segundos (desde el inicio del plano) donde pega el golpe
#   d  = desde que segundo del clip arrancar
#   f  = entrada con destello: ("white"|"black", segundos)
#   p  = congelar el ultimo cuadro para estirar el plano
PAUTA = [
    ("p01-gallo-camara",     0.00,  3.63, dict(e=(0.80, 1.00), r=1)),
    ("p02-gasolina",         3.63,  7.28, dict(e=(1.00, 0.84))),
    ("p03-chancho-patada",   7.28, 12.88, dict(e=(0.90, 1.00), s=(0.58, 2.18, 3.78))),
    ("p04-gallo-chancho",   12.88, 15.68, dict(e=(0.95, 0.95))),
    ("p05-carbonilla",      15.68, 18.80, dict(e=(0.86, 1.00))),
    ("i01-zinc-magnesio",   18.80, 20.84, dict(c=1, e=(0.88, 1.00))),
    ("p06-valvulas-secas",  20.84, 23.00, dict(e=(0.85, 1.00), r=1, s=(0.0,))),
    ("i02-maca-huanarpo",   23.00, 25.30, dict(c=1, e=(0.88, 1.00))),
    ("p07-gomita-roja",     25.30, 26.50, dict(e=(0.92, 1.00), v=0.5)),
    ("p08-aceite-dorado",   26.50, 30.00, dict(e=(1.00, 0.86), f=("white", 0.10))),
    ("i03-achiote-una-gato",30.00, 32.30, dict(c=1, e=(1.00, 0.88))),
    ("p09-filtro",          32.30, 35.00, dict(e=(0.88, 1.00))),
    ("p10-motor-fundido",   35.00, 38.70, dict(e=(1.00, 0.86), s=(0.0,), f=("black", 0.18))),
    ("p11-chancho-empuja",  38.70, 42.48, dict(e=(0.92, 0.92))),
    ("p12-gallo-humo",      42.48, 44.76, dict(e=(0.84, 1.00), r=1, f=("black", 0.12))),
    ("p13-tanque-limpio",   44.76, 47.58, dict(e=(0.90, 1.00))),
    ("i04-frasco",          47.58, 48.30, dict(c=1, e=(0.82, 1.00), r=1, s=(0.0,), f=("white", 0.08))),
    ("p14-gallo-orgulloso", 48.30, 53.20, dict(e=(1.00, 0.80), r=1, p=1.0)),
]

# la apertura en caliente: tiempo absoluto del video
APERTURA = [
    ("p10-motor-fundido",  0.00, 0.70, dict(e=(0.86, 1.00), r=1, s=(0.02,), d=2.2)),
    ("p11-chancho-empuja", 0.70, 1.40, dict(e=(1.00, 0.90), s=(0.0,), d=1.2, f=("white", 0.06))),
]

# textos sueltos, en tiempo absoluto: (texto, entra, sale, alto, y, color)
TEXTOS = [
    (u"NO ES LA MOTO.",                    0.08,  1.42, 78,  880, "white"),
    (u"COMENTA \u00abL\u00c1ZARO\u00bb",   49.30 + OFFSET, TOTAL - 0.05, 58, 1000, ORO),
    (u"ETIQUETA AL PATA QUE LO NECESITA",  50.30 + OFFSET, TOTAL - 0.05, 40, 1085, "white"),
]

GRADO = (
    "eq=contrast=1.07:saturation=1.10:gamma=0.98,"
    "colorbalance=rs=-0.045:gs=-0.010:bs=0.060:rm=0.025:bm=-0.020:rh=0.055:bh=-0.055,"
    "curves=master='0/0.016 0.20/0.170 0.50/0.505 0.80/0.850 1/0.985',"
    "unsharp=5:5:0.55:5:5:0.0,"
    "vignette=PI/4.2"
)
GRANO = "noise=alls=5:allf=t+u"


def corre(*args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=BASE)
    if r.returncode:
        raise SystemExit("ffmpeg fallo:\n" + r.stderr[-1800:])


def sacudon(golpes, k):
    """desplazamiento que tiembla fuerte en cada golpe y se apaga en ~0,2 s"""
    if not golpes:
        return "0"
    amp = 16 * k
    partes = ["%.1f*sin(on*2.7)*exp(-(on-%d)/5)*gte(on,%d)" % (amp, int(g * 30), int(g * 30))
              for g in golpes]
    return "+".join(partes)


def tramo(nombre, dur, o, salida):
    es_cuadro = o.get("c", 0)
    k = 2.0 if es_cuadro else 1.25
    ancho, alto = int(1080 * k), int(1920 * k)
    e0, e1 = o.get("e", (1.0, 1.0))
    tot = max(int(round(dur * 30)) - 1, 1)
    p = "on/%d" % tot
    if o.get("r"):
        p = "(1-pow(1-%s,3))" % p
    z = "%.4f+(%.4f)*%s" % (k * e0, k * (e1 - e0), p)
    sx, sy = sacudon(o.get("s"), k), sacudon(o.get("s"), k * 0.6)

    vf = []
    if o.get("v"):
        vf.append("setpts=%.3f*PTS" % (1.0 / o["v"]))
    vf.append("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d"
              % (ancho, alto, ancho, alto))
    # fps=30 ANTES del zoom: zoompan cuenta cuadros de entrada y los clips vienen a 24
    vf.append("fps=30")
    if o.get("p"):
        vf.append("tpad=stop_mode=clone:stop_duration=%s" % o["p"])
    vf.append("zoompan=z='%s':x='iw/2-(iw/zoom/2)+(%s)':y='ih/2-(ih/zoom/2)+(%s)':"
              "d=1:s=1080x1920:fps=30" % (z, sx, sy))
    if o.get("f"):
        vf.append("fade=t=in:st=0:d=%s:color=%s" % (o["f"][1], o["f"][0]))

    fuente = os.path.join(PLANOS, nombre + (".png" if es_cuadro else ".mp4"))
    if es_cuadro:
        entrada = ["-loop", "1", "-framerate", "30", "-t", str(dur), "-i", fuente]
    else:
        entrada = ["-ss", str(o.get("d", 0)), "-i", fuente]
    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", *entrada, "-t", str(dur),
          "-vf", ",".join(vf), "-an", "-c:v", "libx264", "-preset", "medium",
          "-crf", "16", "-pix_fmt", "yuv420p", salida)


def main():
    os.makedirs(TMP, exist_ok=True)
    lista = os.path.join(TMP, "lista.txt")
    with open(lista, "w", encoding="utf-8") as f:
        todos = [("ap-%d-%s" % (i, n), n, a, b, o) for i, (n, a, b, o) in enumerate(APERTURA)]
        # un instante de negro entre la apertura y la historia
        todos.append(("ap-negro", None, 1.40, OFFSET, {}))
        todos += [(n, n, a, b, o) for n, a, b, o in PAUTA]
        for clave, nombre, entra, sale, o in todos:
            dur = round(sale - entra, 3)
            corte = os.path.join(TMP, clave + "-corte.mp4")
            if nombre is None:
                corre("ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "lavfi",
                      "-i", "color=c=black:s=1080x1920:r=30", "-t", str(dur),
                      "-c:v", "libx264", "-pix_fmt", "yuv420p", corte)
            else:
                tramo(nombre, dur, o, corte)
            f.write("file '%s'\n" % corte.replace("\\", "/"))
            print("  %-26s %5.2f s" % (clave, dur), flush=True)

    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", lista, "-c", "copy", "tmp/pegado.mp4")

    cadena = [GRADO, "subtitles=subs.ass:fontsdir=fuentes"]
    for txt, a, b, alto, y, color in TEXTOS:
        cadena.append(
            "drawtext=fontfile='%s':text='%s':fontsize=%d:fontcolor=%s:"
            "x=(w-text_w)/2:y=%d:borderw=5:bordercolor=black@0.9:"
            "shadowx=0:shadowy=3:shadowcolor=black@0.5:"
            "enable='between(t,%.2f,%.2f)'" % (ANTON, txt, alto, color, y, a, b))
    cadena.append(GRANO)
    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", "tmp/pegado.mp4",
          "-vf", ",".join(cadena),
          "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
          "-an", "tmp/acabado.mp4")

    # la voz entra despues de la apertura; los efectos ya vienen con el desfase
    ms = int(OFFSET * 1000)
    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", "tmp/acabado.mp4",
          "-i", VOZ, "-i", "efectos.wav",
          "-filter_complex",
          "[1:a]aformat=sample_rates=48000:channel_layouts=mono,adelay=%d,apad[v];"
          "[2:a]aformat=sample_rates=48000:channel_layouts=mono[e];"
          "[v][e]amix=inputs=2:duration=shortest:normalize=0,"
          "alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11,"
          "aformat=channel_layouts=stereo[a]" % ms,
          "-map", "0:v:0", "-map", "[a]", "-t", "%.2f" % TOTAL,
          "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", FINAL)
    print("\nlisto:", FINAL, flush=True)


if __name__ == "__main__":
    main()
