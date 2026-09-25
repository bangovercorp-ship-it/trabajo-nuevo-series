# -*- coding: utf-8 -*-
"""Episodio 1 - El Cliente Cero: cuadros y clips.

Once cuadros (3 creditos c/u) y ocho clips (4 creditos c/u) = 65 creditos firmes.
El desglose esta en 12-episodio-1-lista-de-planos.md del repositorio.

Uso:
    python episodio1.py cuadros          # los once cuadros que falten
    python episodio1.py clips            # los ocho clips que falten
    python episodio1.py t1a t2 t7        # solo esas claves, cuadro o clip
    python episodio1.py costo            # que falta y cuanto cuesta, sin gastar

La toma 9 es un cuadro fijo: no tiene clip. El empuje lo hace ffmpeg en el montaje.
"""
import os, sys
import snapgen as sg

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "gallin", "episodio-1")
HOJ = os.path.join(BASE, "gallin")

# Las vistas en version Ecuador viven en el repositorio: se generaron en la nube y
# solo existen como JPG. Se pueden rehacer a resolucion completa con Remotion.
REF = r"C:\Users\HP\OneDrive\Desktop\TIO GALLIN ECUADOR\referencias"
MAQ = os.path.join(REF, "maqueta-ecuador")
PLA = os.path.join(REF, "planos-ecuador")
CIU = os.path.join(REF, "ciudad-ecuador")

GALLIN   = os.path.join(HOJ, "03-hoja-tio-gallin.png")
PORFIRIO = os.path.join(HOJ, "04-hoja-porfirio.png")
BETO     = os.path.join(HOJ, "20-hoja-beto-choez.png")
KEVIN    = os.path.join(HOJ, "11-hoja-kevin.png")

ENTRADA    = os.path.join(MAQ, "taller-1-entrada.jpg")
BANCO      = os.path.join(MAQ, "taller-2-banco.jpg")
ESTANTERIA = os.path.join(MAQ, "taller-4-estanteria.jpg")
PUERTA     = os.path.join(MAQ, "taller-5-puerta.jpg")
FACHADA    = os.path.join(PLA, "03-fachada-taller.jpg")
ESQ_NOCHE  = os.path.join(CIU, "v6-v_esquina_noche.jpg")
CARRETERA  = os.path.join(CIU, "h15-carretera.jpg")

# ---------------------------------------------------------------- bloques comunes

ESTILO = (" Photorealistic cinematic still, vertical 9:16 composition, shallow depth of field, fine film grain, "
          "one single colour grade: cold blue outside, warm amber inside. Photorealistic human-animal hybrids with "
          "real HUMAN faces and human hands, the animal features grown naturally into them; not costumes, not masks, "
          "not cartoon, not Pixar. Full-bleed image edge to edge, no border, no rounded corners, no text, no logos, "
          "no watermark.")

MUNDO = (" Night on the coast of Ecuador, just after a heavy tropical downpour; it is NOT raining any more, everything "
         "is dripping. Outside: wet dirt road, puddles, a single working street lamp. Inside the workshop: pale grey "
         "epoxy floor with yellow bay lines, cream walls with onyx black up to shoulder height and a thin gold line "
         "between them, neutral white work light overhead, and only over the main bench two hanging amber lamps. "
         "Beto Choez is SOAKED from head to toe, hair plastered flat, clothes dark with water; he never dries. His "
         "delivery motorcycle is always the same one and it never runs.")

COMUN = (" Vertical 9:16 cinematic night footage, realistic motion, the same characters, faces and clothes as in the "
         "first frame at all times; Beto stays soaked from head to toe and the motorcycle never starts. Ambient sound "
         "only: wind, dripping water, the workshop. No music, no on-screen text, no subtitles, no captions.")

# ---------------------------------------------------------------- los once cuadros

CUADROS = {
 "t1a": ([BETO],
  "Extreme close-up, vertical: the wet hands of Beto Choez gripping the rubber handlebar grip of a delivery "
  "motorcycle, rainwater running down his knuckles and dripping from his fingers, the short grey-brown velvety hair "
  "on his forearm soaked flat, one black rubber inner-tube strap crossing over the forearm. Behind the hands, deep "
  "dark night and one small distant warm light, far out of focus. His face is NOT visible in this frame."),

 "t1b": ([BETO, ESQ_NOCHE, CARRETERA, FACHADA],
  "Wide vertical low-angle shot from the wet dirt road: Beto Choez, soaked, pushing his dead delivery motorcycle away "
  "from the camera toward the only lit street lamp, the corner workshop glowing ahead of him. He is backlit and reads "
  "almost as a silhouette with a warm rim of light on his shoulders and on his long donkey ears. The street is cold "
  "blue; in the upper third, small and sharp, the red neon rooster sign over the workshop; the puddles reflect it."),

 "t2": ([PORFIRIO, KEVIN, ENTRADA],
  "Vertical medium shot from inside the entrance bay: Porfirio, the pig-human hybrid cashier, has just pushed the "
  "black rolling metal gate up and greets with both arms open and a huge warm smile, the lit workshop behind him. On "
  "the LEFT EDGE of the frame, partly cut off, Kevin, a young monkey-human hybrid, films with a phone held vertically. "
  "In the foreground, out of focus, the soaked shoulder and the transparent plastic rain poncho of Beto."),

 "t3": ([PORFIRIO],
  "Vertical handheld memory shot, heavily desaturated cold grey, strong film grain, rain still falling: the same "
  "pig-human hybrid man, younger and clearly overweight, pushing his own dead motorcycle alone down a wet road at "
  "night, seen from behind and slightly to the side, exhausted, shoulders down. Cold grey only, NO warm colour "
  "anywhere in the frame."),

 "t4": ([GALLIN, BETO, ENTRADA],
  "Vertical low shot at motorcycle height: Tio Gallin, the rooster-human hybrid master mechanic, crouches beside the "
  "dead delivery motorcycle with one hand flat on the engine and his EYES CLOSED, head slightly tilted as if "
  "listening, completely calm. He fills the height of the frame. Behind him, blurred, Beto stands waiting, soaked."),

 "t5": ([GALLIN, BANCO],
  "Vertical tight close-up of Tio Gallin on a long lens, the background completely out of focus with the two hanging "
  "amber lamps as warm bokeh behind him. He looks straight at someone off camera, absolutely still, calm and certain. "
  "The amber light rims one side of his face and his short red crest."),

 "t6": ([BETO, GALLIN, BANCO],
  "Vertical tight close-up of Beto Choez, soaked, looking down and slightly away, mouth just open about to speak, "
  "hesitating and ashamed. In the immediate foreground on the right, out of focus, the shoulder and the black-green "
  "feather mantle of Tio Gallin. The bench area behind them in warm amber."),

 "t7a": ([ESTANTERIA, PUERTA],
  "Vertical shot down the length of the workshop toward the tire rack: a tall metal rack loaded with about a hundred "
  "and twenty tires, and behind a narrow gap between them, FAR AWAY and small, a deep red wooden door with a small "
  "gold crown at its centre, barely visible, catching one glint of light. Nobody in the frame."),

 "t7b": ([PUERTA],
  "Vertical close shot of the small gold crown at the centre of the deep red wooden door: worn wood grain, deep red "
  "paint, no handle on the outside, one hard glint of warm light on the gold leaf. Nobody in the frame."),

 "t8": ([PORFIRIO, GALLIN, BANCO],
  "Vertical low-angle shot from below: Porfirio standing upright, chest up, tightening his belt one hole further with "
  "both hands and looking down at it with quiet pride, warm amber light on him. Behind him and slightly out of focus, "
  "Tio Gallin watches with a small half-smile."),

 "t9": ([BANCO],
  "Vertical extreme macro of an old paper wall calendar hanging on the workshop wall: ONE single day circled hard in "
  "red ballpoint, the paper slightly damp and curled at one corner, every other number in plain black. Shallow focus "
  "so only the circled day is sharp. Dim warm light from the side. No people."),
}

# ---------------------------------------------------------------- los ocho clips

# Las tomas con movimiento de camara se generan con cuadro inicial Y final.
PAREJAS = {"t1": ("t1a", "t1b"), "t7": ("t7a", "t7b")}

MOV = {
 "t1": "The camera pulls back from the hands to reveal the whole man pushing the dead motorcycle away toward the "
       "distant light; heavy slow effort, his breath visible in the cold air, the front wheel rolling through a puddle.",

 "t2": "Porfirio pushes the rolling gate fully up and steps forward with both arms open, smiling. He says in Spanish "
       "with a coastal Ecuadorian accent: \"Bienvenido, bienvenido! Yo llegue igualito, nano, empujando mi moto.\" "
       "On the left edge the young man keeps filming with his phone and does not speak.",

 "t3": "Handheld camera follows the younger overweight man from behind as he pushes his motorcycle three slow steps "
       "through the rain. Nobody speaks.",

 "t4": "Gallin keeps his eyes closed and says in Spanish, low and calm: \"A ver, arrancalo.\" Off camera a kick "
       "starter is stamped down; the engine coughs twice and dies. Gallin does not open his eyes.",

 "t5": "Still on the long lens, Gallin asks in Spanish: \"Dormiste anoche?\" A tired voice off camera answers: \"Tres "
       "horas.\" Gallin holds one beat and says: \"Eso no es el motor.\" He barely moves; only his eyes.",

 "t6": "The camera pushes in very slowly. Beto lowers his voice and says in Spanish: \"Vengo por el afinamiento "
       "completo.\" An older voice off camera asks: \"Y el carro?\" Beto looks up and answers: \"El carro esta bien.\"",

 "t7": "The camera glides slowly forward through the gap between the tires until the small gold crown on the red door "
       "fills the centre of the frame. Nothing else moves in the shot.",

 "t8": "Porfirio pulls his belt one hole tighter, looks down at it, then lifts his chin. An older voice off camera "
       "says in Spanish: \"Aqui no se juzga. Se afina.\"",
}

# ---------------------------------------------------------------- para el montaje

# segundo de entrada, duracion, y la palabra que va en oro en el subtitulo
MONTAJE = [
 ("t1",  0.0, 3.0, ""),
 ("t2",  3.0, 8.0, "igualito"),
 ("t3", 11.0, 6.0, ""),
 ("t4", 17.0, 8.0, "arrancalo"),
 ("t5", 25.0, 8.0, "no es el motor"),
 ("t6", 33.0, 8.0, "EL CARRO ESTA BIEN"),
 ("t7", 41.0, 8.0, ""),
 ("t8", 49.0, 7.0, "se afina"),
 ("t9", 56.0, 4.0, "EL CARRO ESTA BIEN"),   # cuadro fijo, empuje en ffmpeg
]

# ---------------------------------------------------------------- ejecucion

def ruta_cuadro(c):
    return os.path.join(SAL, c + ".png")

def ruta_clip(c):
    return os.path.join(SAL, c + ".mp4")

def faltan_cuadros():
    return [c for c in CUADROS if not os.path.exists(ruta_cuadro(c))]

def faltan_clips():
    return [c for c in MOV if not os.path.exists(ruta_clip(c))]

def falta_referencia(refs):
    return [r for r in refs if not os.path.exists(r)]

def hacer_cuadro(c):
    refs, prompt = CUADROS[c]
    perdidas = falta_referencia(refs)
    if perdidas:
        print("  SALTO %s: falta la referencia %s" % (c, ", ".join(os.path.basename(p) for p in perdidas)))
        return False
    r = sg.imagen(prompt + MUNDO + ESTILO, aspecto="9:16", resolucion="2K", imagenes=refs)
    e = sg.esperar(r["uuid"], limite=600, cada=6)
    print("  ok", sg.descargar(sg.url_imagen(e), ruta_cuadro(c)), flush=True)
    return True

def hacer_clip(c):
    if c in PAREJAS:
        imgs = [ruta_cuadro(k) for k in PAREJAS[c]]
    else:
        imgs = [ruta_cuadro(c)]
    perdidas = falta_referencia(imgs)
    if perdidas:
        print("  SALTO %s: primero hay que generar el cuadro %s" % (c, ", ".join(os.path.basename(p) for p in perdidas)))
        return False
    for intento in (1, 2):
        try:
            r = sg.video(MOV[c] + COMUN, imagenes=imgs)
            e = sg.esperar(r["uuid"], limite=1200, cada=10)
            print("  ok", sg.descargar(sg.url_video(e), ruta_clip(c)), flush=True)
            return True
        except BaseException as ex:
            print("  intento %d fallo en %s: %s" % (intento, c, str(ex)[:160]), flush=True)
    return False

def informe():
    fc, fv = faltan_cuadros(), faltan_clips()
    print("Cuadros por generar: %2d  -> %3d creditos" % (len(fc), 3 * len(fc)))
    print("Clips por generar:   %2d  -> %3d creditos" % (len(fv), 4 * len(fv)))
    print("Firme:                     %3d creditos" % (3 * len(fc) + 4 * len(fv)))
    perdidas = sorted({p for refs, _ in CUADROS.values() for p in falta_referencia(refs)})
    if perdidas:
        print("\nReferencias que todavia no existen:")
        for p in perdidas:
            print("  -", p)

if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True)
    args = sys.argv[1:]
    if not args or args[0] == "costo":
        informe()
        raise SystemExit(0)
    if args == ["cuadros"]:
        claves = faltan_cuadros()
    elif args == ["clips"]:
        claves = faltan_clips()
    else:
        claves = args
    antes = sg.creditos()
    print("creditos antes:", antes, flush=True)
    for c in claves:
        print(c, flush=True)
        if c in CUADROS and not os.path.exists(ruta_cuadro(c)):
            hacer_cuadro(c)
        elif c in MOV:
            hacer_clip(c)
        elif c in CUADROS:
            print("  ya existe")
        else:
            print("  clave desconocida")
    print("creditos despues:", sg.creditos(), flush=True)
