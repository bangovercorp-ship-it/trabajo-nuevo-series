# -*- coding: utf-8 -*-
"""Laminas de expresiones y de poses para cada personaje (Nano Banana Pro en SnapGen)."""
import os, sys
import snapgen as sg

SAL = r"C:\pesonajes para videos\gallin"
FIEL = ("the exact same character as the reference image: identical face, hair, animal features, body and clothes. ")
FIN = ("Photorealistic human-animal hybrid, cinematic character design, highly detailed. Plain neutral mid-grey "
       "studio background, soft even light. No text, no labels, no numbers, no logos, no watermark.")

# hoja de referencia, 6 expresiones, 3 poses
DATOS = {
 "gallin": ("03-hoja-tio-gallin",
   "listening seriously, a wise knowing half-smile, a hard disappointed stare, laughing genuinely, "
   "sad and far away remembering a lost love, tender and soft looking at someone he cares about",
   "arms crossed leaning against a car lift; crouching with one hand on a car hood listening to the engine; "
   "pointing a steel wrench forward while delivering a verdict"),
 "porfirio": ("04-hoja-porfirio",
   "huge happy grin, about to tell a secret with a hand over his mouth, scared by a stern look, proud, "
   "confused, excited",
   "waving cheerfully behind a shop counter; covering his mouth after saying too much; proudly showing a "
   "tighter belt notch on his slimmer waist"),
 "toribio": ("05-hoja-toribio",
   "shy, deeply concentrated on delicate work, angry, embarrassed, a tender gentle smile, surprised",
   "lifting a car engine with his bare hands; holding tiny tweezers over a circuit board with extreme care; "
   "standing awkwardly with his huge hands clasped in front"),
 "renzo": ("06-hoja-renzo",
   "charming salesman smile, cold calculating look reading someone, nervous in silence, fake loud laugh, "
   "sincere and serious, a sly wink",
   "leaning on a counter; sweeping one arm like a butler to open a hidden door; talking fast with his hands"),
 "micaela": ("07-hoja-micaela",
   "ironic half-smile, wise knowing look, hidden jealousy, laughing, quietly sad, elegant and alluring",
   "behind a bar pouring a drink; standing in a doorway with arms crossed looking across the street; "
   "sitting on a bar stool holding a glass"),
 "aurora": ("08-hoja-aurora",
   "reserved and guarded, surprised, laughing for the first time in years, suspicious, sad, shy and falling "
   "in love",
   "standing beside a flat tyre of a luxury car at night; walking into a workshop looking around with "
   "curiosity; sitting on a workshop bench holding a coffee cup"),
 "pavon": ("09-hoja-fausto-pavon",
   "big fake smile, arrogant sneer, furious, desperate and broke, flirtatious, mocking laugh",
   "fanning his peacock tail wide to show off; leaning on a flashy luxury car; pointing with contempt"),
}


def lamina(clave, tipo):
    hoja, gestos, poses = DATOS[clave]
    ref = [os.path.join(SAL, hoja + ".png")]
    if tipo == "expresiones":
        texto = ("Facial expression sheet of " + FIEL + "Six head-and-shoulders portraits arranged in a 3 by 2 grid, "
                 "same framing and light in all six, with these expressions in order: " + gestos + ". ")
    else:
        texto = ("Pose sheet of " + FIEL + "Three full-body poses side by side showing his or her attitude, same "
                 "outfit in all three: " + poses + ". ")
    r = sg.imagen(texto + FIN, aspecto="16:9", resolucion="2K", imagenes=ref)
    e = sg.esperar(r["uuid"], limite=600, cada=6)
    nombre = "%s-%s.png" % (hoja, tipo)
    return sg.descargar(sg.url_imagen(e), os.path.join(SAL, "laminas", nombre))


if __name__ == "__main__":
    claves = sys.argv[1:] or list(DATOS)
    antes = sg.creditos()
    for c in claves:
        for tipo in ("expresiones", "poses"):
            for intento in (1, 2):                 # SnapGen a veces corta con 524
                try:
                    print("  ok", lamina(c, tipo), flush=True)
                    break
                except BaseException as ex:
                    print("  FALLO %s %s (intento %d): %s" % (c, tipo, intento, str(ex)[:120]), flush=True)
    print("costo:", antes - sg.creditos(), "| quedan", sg.creditos(), flush=True)
