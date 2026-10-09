# -*- coding: utf-8 -*-
"""Guion 2 (la nariz que se acostumbra): 13 clips verticales con Veo 3.1 Fast desde SnapGen.
8 s, 9:16, 1080p, 4 creditos c/u = 52 creditos. Sin caras reconocibles ni logos ni texto.

Uso:  python guion2_planos.py costo            # cuanto cuesta, sin gastar nada
      python guion2_planos.py                   # los que falten
      python guion2_planos.py c01 c09           # solo esos
Salen en C:\\pesonajes para videos\\guion2\\  (suben ese folder a la sesion para montar).
"""
import os, sys
import snapgen as sg

SAL = r"C:\pesonajes para videos\guion2"
COMUN = (" Vertical phone-camera look, realistic motion, cinematic shallow depth of field, natural light. "
         "No readable text, no logos, no watermarks, no identifiable faces. No music, no dialogue; only natural ambient sound.")

# clave: (frase de la voz que apoya, prompt)
PLANOS = {
 "c01-alcantarilla": ("quien trabaja en una alcantarilla",
   "Inside a large underground sewer tunnel, a worker in orange coveralls and a helmet with a headlamp walks away from the camera along a narrow walkway, water dripping, light mist, echoing space, dark and moody."),
 "c02-reloj": ("se acostumbra en minutos",
   "Extreme close-up of a simple wall clock, the minute hand moving fast in time-lapse over a warm kitchen, steam rising from a pot in the soft-focus background, golden light."),
 "c03-casa": ("tampoco hueles tu propia casa",
   "First-person view opening a front door and walking into a cozy lived-in home, warm lamp light, dust motes floating in sunbeams, calm and familiar."),
 "c04-gas": ("gases que apagan el olfato",
   "A handheld gas detector in a gloved hand flashing a red alarm light next to an industrial pipe, a yellow hazard sign blurred behind, faint fog drifting, tense."),
 "c05-nariz": ("cuatrocientos tipos de receptores",
   "Extreme macro of a human nose and nostrils inhaling slowly, skin texture, soft side light, the rest of the face out of frame and soft."),
 "c06-perfumista": ("los perfumistas",
   "A perfumer's hands dipping thin paper scent strips into small amber glass bottles on a lab bench, fanning one strip slowly, shallow depth of field, elegant warm light, no faces."),
 "c07-cerebro": ("zonas de emocion y recompensa",
   "Cinematic translucent 3D brain on a dark background, a thin line of golden light travels from the nose area to the deep emotional center which glows and pulses, neurons firing, slow camera push-in."),
 "c08-flores": ("un recuerdo en un segundo",
   "Close-up of two hands holding fresh white jasmine flowers lifting toward a softly blurred face out of focus, sunlight through leaves, gentle smile suggested, nostalgic warm tone."),
 "c09-barro": ("entre barro y malos olores",
   "Close-up of a worker's rubber boots and hands covered in thick mud, the mud being rinsed by a strong stream of water and swirling down a drain, steam rising, gritty realistic."),
 "c10-ducha": ("un buen baño",
   "Back view of a person's shoulders under a hot shower, water streaming, thick steam, soap foam sliding down, bright clean light, relief and relaxation, no face."),
 "c11-jabon": ("un jabon",
   "Slow motion macro of a bar of soap with rich white foam and iridescent bubbles floating up, bright clean bathroom light, satisfying."),
 "c12-perfume": ("un perfume",
   "Slow motion of a plain unlabeled glass perfume bottle spraying a fine golden-lit mist against a dark background, backlit droplets sparkling, luxurious."),
 "c13-celebracion": ("tus mejores momentos",
   "Silhouettes of a group of friends cheering and hugging on a rooftop at golden-hour sunset, city lights starting to glow, warm lens flare, joyful, nobody facing the camera."),
}

if __name__ == "__main__":
    pedir = [a for a in sys.argv[1:] if a != "costo"]
    claves = [k for k in PLANOS if any(k.startswith(p) for p in pedir)] if pedir else \
             [k for k in PLANOS if not os.path.exists(os.path.join(SAL, k + ".mp4"))]
    print("%d clips x 4 creditos = %d creditos" % (len(claves), 4 * len(claves)))
    if "costo" in sys.argv[1:]:
        raise SystemExit(0)
    print("creditos antes:", sg.creditos())
    for i, c in enumerate(claves, 1):
        print("[%d/%d] %s  (%s)" % (i, len(claves), c, PLANOS[c][0]), flush=True)
        for intento in (1, 2):
            try:
                r = sg.video(PLANOS[c][1] + COMUN)
                e = sg.esperar(r["uuid"], limite=1200, cada=10)
                print("  ok", sg.descargar(sg.url_video(e), os.path.join(SAL, c + ".mp4")), flush=True)
                break
            except BaseException as ex:
                print("  intento %d fallo: %s" % (intento, ex), flush=True)
    print("creditos despues:", sg.creditos())
