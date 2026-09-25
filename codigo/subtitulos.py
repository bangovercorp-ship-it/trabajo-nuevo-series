# -*- coding: utf-8 -*-
"""Genera los subtitulos estilo TikTok: de dos a tres palabras, la clave en oro,
con rebote de entrada. Sale un .ass que ffmpeg quema con libass.

Whisper acierta los tiempos pero escribe mal ("talleno", "guanar pomacho"), asi
que se le impone el texto correcto encima de sus marcas.
"""
import io, json, os

JSON = (r"C:\Users\HP\AppData\Local\Temp\claude\C--JUEGOS-APP"
        r"\651049f2-3a39-403d-b5cd-dbfbf6db141d\scratchpad"
        r"\Generated Audio September 19, 2026 - 8_30PM.json")
SALIDA = r"C:\pesonajes para videos\subs.ass"
OFFSET = 1.50    # la apertura en caliente corre toda la voz

BLANCO = r"&H00FFFFFF&"
ORO = r"&H003FAADD&"      # el #DDAA3F de la marca, en BGR como manda el formato

# el texto correcto, en el orden de los segmentos que detecto whisper
GUION = [
    u"Imagínate que tu moto es una máquina potente,",
    u"pero le estás metiendo gasolina de 84 octanos.",
    u"¿Cómo quieres que suba la pendiente",
    u"si el motor cascabelea apenas intentas acelerar?",
    u"Eso te pasa por dentro, causa.",
    u"Tu sistema está lleno de carbonilla",
    u"por el estrés y la falta de zinc y magnesio.",
    u"Tus válvulas están secas.",
    u"La maca negra y el huanarpo macho",
    u"son como el aceite sintético de alta gama",
    u"que lubrica todo el sistema,",
    u"mientras que el achiote y la uña de gato",
    u"limpian los filtros de impurezas.",
    u"Si sigues así, vas a fundir motor a mitad de camino",
    u"y te vas a quedar tirado cuando el momento demande potencia.",
    u"No esperes a que eche humo.",
    u"Métete al link de mi perfil,",
    u"pide tu afinamiento Lázaro",
    u"y deja esa máquina rugiendo como nueva.",
]

# las que se pintan de oro: lo que el espectador tiene que retener
CLAVES = set(u"""moto máquina potente gasolina octanos pendiente cascabelea acelerar
carbonilla estrés zinc magnesio válvulas secas maca negra huanarpo macho aceite
sintético gama lubrica achiote uña gato filtros impurezas fundir motor tirado
potencia humo link perfil afinamiento lázaro rugiendo nueva causa""".split())


def limpia(p):
    return p.strip(u" ,.;:¿?¡!").lower()


def palabras_con_tiempo():
    """pone el texto correcto sobre las marcas de whisper"""
    d = json.load(io.open(JSON, encoding="utf-8"))
    marcas = []
    for s in d["segments"]:
        marcas.append((s["start"], s["end"], [w for w in s.get("words", [])]))

    # el guion esta partido mas fino que los segmentos: se reparte por duracion
    total_texto = u" ".join(GUION).split()
    todas = []
    for w in marcas:
        todas.extend(w[2])

    salida = []
    if len(todas) == len(total_texto):
        for w, txt in zip(todas, total_texto):          # calce perfecto
            salida.append((w["start"], w["end"], txt))
        return salida

    # si no calza, se reparte cada segmento por largo de palabra
    i = 0
    for ini, fin, ws in marcas:
        n_seg = max(1, int(round(len(ws))))
        trozo = total_texto[i:i + n_seg]
        i += n_seg
        if not trozo:
            continue
        pesos = [len(p) + 1.0 for p in trozo]
        acum, span = 0.0, (fin - ini) / sum(pesos)
        for p, peso in zip(trozo, pesos):
            a = ini + acum * span
            acum += peso
            salida.append((a, ini + acum * span, p))
    if i < len(total_texto):                            # lo que sobre, al final
        ini, fin = marcas[-1][1], marcas[-1][1] + 0.6
        resto = total_texto[i:]
        paso = (fin - ini) / len(resto)
        for k, p in enumerate(resto):
            salida.append((ini + k * paso, ini + (k + 1) * paso, p))
    return salida


def agrupar(pal):
    """de dos a tres palabras por cartel, sin pasar de 1,1 s"""
    grupos, actual = [], []
    for p in pal:
        actual.append(p)
        dur = actual[-1][1] - actual[0][0]
        if len(actual) >= 3 or (len(actual) >= 2 and dur >= 0.75):
            grupos.append(actual)
            actual = []
    if actual:
        if grupos and len(actual) == 1:
            grupos[-1].extend(actual)
        else:
            grupos.append(actual)
    return grupos


def hhmmss(s):
    h = int(s // 3600); s -= h * 3600
    m = int(s // 60); s -= m * 60
    return "%d:%02d:%05.2f" % (h, m, s)


CABECERA = u"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Anton,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,1,0,1,5,3,2,60,60,500,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def main():
    grupos = agrupar(palabras_con_tiempo())
    lineas = []
    for g in grupos:
        ini, fin = g[0][0] + OFFSET, g[-1][1] + OFFSET
        fin = max(fin, ini + 0.25)
        piezas = []
        for _, _, txt in g:
            color = ORO if limpia(txt) in CLAVES else BLANCO
            piezas.append(u"{\\c%s}%s" % (color, txt.upper()))
        cuerpo = u" ".join(piezas)
        # rebote de entrada: nace un poco grande y se asienta
        efecto = u"{\\fad(40,40)\\fscx114\\fscy114\\t(0,90,\\fscx100\\fscy100)}"
        lineas.append(u"Dialogue: 0,%s,%s,Sub,,0,0,0,,%s%s"
                      % (hhmmss(ini), hhmmss(fin), efecto, cuerpo))

    with io.open(SALIDA, "w", encoding="utf-8") as f:
        f.write(CABECERA + u"\n".join(lineas) + u"\n")
    print("carteles:", len(grupos), "->", SALIDA)
    for l in lineas[:4]:
        print("  ", l[:110])


if __name__ == "__main__":
    main()
