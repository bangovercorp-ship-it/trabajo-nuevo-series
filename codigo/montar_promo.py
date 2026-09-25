# -*- coding: utf-8 -*-
"""Montaje del promocional del bar sobre el pulso de la cancion de la referencia (129,2 bpm).

Cada corte cae en un golpe: golpe n = G0 + n*BEAT. Salen dos archivos:
  bangover-bar-tiktok.mp4   sin audio, para poner el sonido original en TikTok desde el segundo 0
  bangover-bar-previa.mp4   con la cancion de la referencia, solo para revisar la sincronia
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "promo-bar")
TMP = os.path.join(SAL, "tmp")
G0, BEAT, TOTAL = 0.267, 0.46445, 42.537
LOGO = r"C:\JUEGOS APP\bangover-identidad\png\gota\gota-insinua.png"
FUENTE = r"C:\JUEGOS APP\bangover-web\fonts\cormorant-700.woff2"
FUENTE2 = r"C:\JUEGOS APP\bangover-web\fonts\cormorant-400i.woff2"
GRADO = ("eq=contrast=1.07:saturation=1.12:gamma=0.98,"
         "colorbalance=rs=-0.03:bs=0.05:rh=0.05:bh=-0.05,"
         "curves=master='0/0.016 0.20/0.170 0.50/0.505 0.80/0.850 1/0.985',"
         "unsharp=5:5:0.5:5:5:0.0,vignette=PI/4.5,noise=alls=4:allf=t+u")

# (clip, segundo de entrada, golpe final, efectos)
#   z=(z0,z1) zoom lento  | p punch de zoom al entrar | b barrido lateral | w destello blanco | v velocidad
HISTORIA = [
    ("k1-llega",     0.3, 6,  dict(z=(1.0, 1.10))),
    ("k2-lata",      0.6, 12, dict(p=1)),
    ("k3-bota",      0.0, 20, dict(p=1, v=0.8, z=(1.0, 1.06))),   # antes del seg. 3, donde el asesor se esfuma
    ("k4-gomitas",   0.0, 22, dict(w=1)),          # frasco 0,93 s en pantalla; despues cae una cuarta gomita
    ("k5-confianza", 0.8, 32, dict(p=1, z=(1.0, 1.08))),
    ("k6-entran",    0.0, 42, dict(v=0.75, b=1)),
    ("k8-guino",     1.4, 46, dict(p=1)),
    ("k9-grupo",     0.4, 52, dict(b=1, w=1)),
]
# montaje explosivo: un corte por golpe, y medio golpe en el remate
RAFAGA = ["k7-baila", "k9-grupo", "k7-baila", "k8-guino", "k7-baila", "k5-confianza", "k9-grupo", "k7-baila"]
RANGO = {"k7-baila": (0.2, 7.0), "k9-grupo": (0.2, 7.0), "k8-guino": (1.0, 6.5), "k5-confianza": (3.0, 7.0)}
FINAL_GOLPE = 84


def corre(*args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=BASE)
    if r.returncode:
        raise SystemExit("ffmpeg fallo:\n" + r.stderr[-1800:])


def golpe(n):
    return 0.0 if n == 0 else G0 + n * BEAT


def entre(a, b):
    """duracion en cuadros enteros medidos desde el inicio, para que 50 cortes no se corran"""
    return (round(b * 30) - round(a * 30)) / 30.0


def tramo(clip, ss, dur, o, salida, cuadro=False):
    k = 1.2
    tot = max(int(round(dur * 30)) - 1, 1)
    z0, z1 = o.get("z", (1.0, 1.0))
    z = "%.4f*(%.4f+%.4f*on/%d)" % (k, z0, z1 - z0, tot)
    if o.get("p"):
        z += "*(1+0.14*exp(-on/3))"
    dx = "380*exp(-on/2.2)" if o.get("b") else "0"
    vf = []
    if o.get("v"):
        vf.append("setpts=%.3f*PTS" % (1.0 / o["v"]))
    vf += ["scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d" % (1080 * k, 1920 * k, 1080 * k, 1920 * k),
           "fps=30",
           "zoompan=z='%s':x='iw/2-(iw/zoom/2)+%s':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30" % (z, dx)]
    if o.get("b"):
        vf.append("gblur=sigma=28:sigmaV=0:enable='lt(t,0.14)'")
    if o.get("w"):
        vf.append("fade=t=in:st=0:d=0.12:color=white")
    if o.get("fin"):
        vf.append("fade=t=in:st=0:d=0.35:color=black")
    if cuadro:
        ent = ["-loop", "1", "-framerate", "30", "-t", "%.3f" % dur, "-i", clip]
    else:
        ent = ["-ss", "%.3f" % ss, "-i", os.path.join(SAL, clip + ".mp4")]
    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", *ent, "-t", "%.3f" % dur, "-vf", ",".join(vf),
          "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", salida)


def placa():
    """pantalla final: la gota y el nombre, con la frase aprobada de la marca"""
    im = Image.new("RGB", (1080, 1920), (11, 10, 9))
    g = Image.open(LOGO).convert("RGB").resize((300, 300), Image.LANCZOS)
    im.paste(g, (390, 640))
    d = ImageDraw.Draw(im)
    f1, f2 = ImageFont.truetype(FUENTE, 118), ImageFont.truetype(FUENTE2, 66)
    for txt, f, y, col in (("BANGOVER", f1, 1000, (221, 170, 63)),
                           (u"No se anuncia. Se recomienda.", f2, 1160, (240, 232, 214))):
        w = d.textlength(txt, font=f)
        d.text(((1080 - w) / 2, y), txt, font=f, fill=col)
    ruta = os.path.join(TMP, "placa.png")
    im.save(ruta)
    return ruta


def main():
    os.makedirs(TMP, exist_ok=True)
    partes = []
    n0 = 0
    for i, (clip, ss, n1, o) in enumerate(HISTORIA):
        partes.append((clip, ss, entre(golpe(n0), golpe(n1)), o, False)); n0 = n1
    usos = {}
    for n in range(n0, FINAL_GOLPE):
        pasos = [n, n + 0.5] if n >= FINAL_GOLPE - 8 else [n]        # remate a medio golpe
        for p in pasos:
            fin = min(p + (0.5 if n >= FINAL_GOLPE - 8 else 1), FINAL_GOLPE)
            clip = RAFAGA[len(partes) % len(RAFAGA)]
            a, b = RANGO[clip]; ss = a + (usos.get(clip, 0) * 1.3) % (b - a); usos[clip] = usos.get(clip, 0) + 1
            fx = [dict(p=1), dict(b=1), dict(p=1, w=1), dict(z=(1.15, 1.0))][len(partes) % 4]
            partes.append((clip, ss, entre(golpe(p), golpe(fin)), fx, False))
    partes.append((placa(), 0, entre(golpe(FINAL_GOLPE), TOTAL), dict(z=(1.0, 1.05), fin=1), True))

    lista = os.path.join(TMP, "lista.txt")
    with open(lista, "w", encoding="utf-8") as f:
        for i, (clip, ss, dur, o, cuadro) in enumerate(partes):
            out = os.path.join(TMP, "t%02d.mp4" % i)
            tramo(clip, ss, dur, o, out, cuadro)
            f.write("file '%s'\n" % out.replace("\\", "/"))
    print(len(partes), "tramos", flush=True)
    pegado = os.path.join(TMP, "pegado.mp4")
    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista,
          "-c", "copy", pegado)
    mudo = os.path.join(SAL, "bangover-bar-tiktok.mp4")
    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", pegado, "-vf", GRADO, "-t", "%.3f" % TOTAL,
          "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mudo)
    corre("ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", mudo, "-i", os.path.join(BASE, "referencias", "ref.wav"),
          "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
          os.path.join(SAL, "bangover-bar-previa.mp4"))
    print("listo", flush=True)


if __name__ == "__main__":
    main()
