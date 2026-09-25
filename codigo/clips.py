# -*- coding: utf-8 -*-
"""Los 13 clips que faltan. Cada cuadro fijo se pone en movimiento con seedance-1.5-pro.

Se generan con sobrante sobre la duracion que pide la locucion: montar.py recorta.
"""
import os, sys
sys.path.insert(0, r"C:\JUEGOS APP\bangover-identidad\scripts")
import kie

PLANOS = r"C:\pesonajes para videos\planos"
UNA_TOMA = ("One single continuous take, no cuts, no scene changes, no camera shake. "
            "No text, no captions, no logos, no lettering appears at any point.")

# nombre, segundos a generar, movimiento
CLIPS = [
 ("p02-gasolina", 4,
  "The murky brown contaminated gasoline keeps pouring down into the tank opening, dirty foam "
  "building and swirling on the surface, sediment tumbling in the stream. The camera descends very "
  "slowly straight down toward the filler neck. " + UNA_TOMA),

 ("p03-chancho-patada", 6,
  "The pig rises up and stamps his whole weight down hard on the kickstarter pedal. The motorcycle "
  "lurches and rocks on its suspension but the engine does not catch. He heaves himself up and stamps "
  "down a second time, straining, and again nothing. His shoulders drop. The camera dollies in slowly "
  "from low. " + UNA_TOMA),

 ("p04-gallo-chancho", 4,
  "The rooster jabs his raised wing forward twice toward the pig as he lectures him, head bobbing, "
  "hackles flaring. In the blurred foreground the pig's shoulders sink lower. The camera pushes in "
  "slightly past the pig's shoulder. " + UNA_TOMA),

 ("p05-carbonilla", 6,
  "The camera orbits slowly around the carbon-encrusted valves inside the combustion chamber, "
  "revealing the thick black crust from every side. The valves shift a fraction, stiff and choked. "
  "Carbon flakes and dust drift through the cold shafts of light. " + UNA_TOMA),

 ("p06-valvulas-secas", 4,
  "The dry valve stem grinds up and down in its guide, metal scraping metal with no oil. The hot "
  "scratch marks flare brighter orange with each stroke and tiny metal shavings peel off and float "
  "away. The camera pushes in hard on the scored surface. " + UNA_TOMA),

 ("p07-gomita-roja", 4,
  "The single translucent red gummy falls the last stretch and drops cleanly into the dark filler "
  "opening, vanishing inside. A soft warm glow rises out of the opening after it. The camera drifts "
  "down toward the hole. " + UNA_TOMA),

 ("p08-aceite-dorado", 4,
  "The molten golden oil floods down over the valve stems and piston crown, and everywhere it touches "
  "the black carbon crust lifts off and streams away in dark ribbons, leaving bright clean metal "
  "behind. Light caustics ripple across the polished surfaces. The camera tracks fast alongside the "
  "flowing gold. " + UNA_TOMA),

 ("p09-filtro", 6,
  "The sharp pulse of golden-white light sweeps steadily across the circular filter from left to "
  "right, and everything it passes turns from choked dark grime to pristine bright clean pleats. When "
  "the whole filter is clean the camera pulls back quickly to reveal the full spotless filter "
  "spinning up. " + UNA_TOMA),

 ("p10-motor-fundido", 4,
  "Thick grey smoke keeps pouring from the dead engine and billows upward across the frame. The "
  "motorcycle does not move. The camera rises slowly and pulls back, leaving it small and abandoned "
  "on the empty roadside. Cold desaturated blue-grey throughout. " + UNA_TOMA),

 ("p11-chancho-empuja", 4,
  "The pig pushes the dead motorcycle slowly away from the camera down the dark empty road, his "
  "steps heavy and laboured, head hanging. He gets smaller as he goes. The camera holds still and "
  "watches him leave. Cold desaturated blue-grey throughout. " + UNA_TOMA),

 ("p12-gallo-humo", 4,
  "The rooster holds his hard stare straight into the lens and blinks once, slowly. Behind his "
  "shoulder the last wisp of grey smoke curls and dissolves in the lamp light. The camera pushes in "
  "slowly on his face. " + UNA_TOMA),

 ("p13-tanque-limpio", 4,
  "The camera orbits slowly around the polished black fuel tank, the long warm highlight from the "
  "pendant lamp sliding smoothly across the mirror-black surface as the angle changes. Nothing else "
  "moves. The top of the tank stays clear and empty. " + UNA_TOMA),

 ("p14-gallo-orgulloso", 4,
  "The rooster puffs out his chest, lifts his head high and gives one short sharp crow, his hackles "
  "flaring out. The restored motorcycle gleams beside him. The camera pulls back and rises slightly "
  "into a wider hero framing. " + UNA_TOMA),
]


def main():
    print("creditos antes:", kie.creditos(), flush=True)
    for i, (nombre, seg, mov) in enumerate(CLIPS, 1):
        png = os.path.join(PLANOS, nombre + ".png")
        mp4 = os.path.join(PLANOS, nombre + ".mp4")
        if os.path.exists(mp4):
            print("[%d/%d] %s ya existe, salto" % (i, len(CLIPS), nombre), flush=True)
            continue
        print("[%d/%d] %s (%d s)" % (i, len(CLIPS), nombre, seg), flush=True)
        try:
            url = kie.subir(png, "lazaro")
            t = kie.crear("bytedance/seedance-1.5-pro",
                          {"prompt": mov, "input_urls": [url], "aspect_ratio": "9:16",
                           "resolution": "720p", "duration": seg, "generate_audio": False})
            u = kie.urls(kie.esperar(t, limite=1800, etiqueta=nombre))[0]
            kie.descargar(u, mp4)
            kie.anotar(trabajo="lazaro-clips", plano=nombre, segundos=seg, costo=seg * 3.5, url=u)
            print("  ok", flush=True)
        except Exception as e:
            print("  FALLO:", e, flush=True)
    print("creditos despues:", kie.creditos(), flush=True)


if __name__ == "__main__":
    main()
