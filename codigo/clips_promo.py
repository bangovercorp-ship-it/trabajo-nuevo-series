# -*- coding: utf-8 -*-
"""Clips del promocional del bar: Veo 3.1 Fast desde cada cuadro clave (4 creditos c/u, 8 s, 9:16, 1080p).

Uso: python clips_promo.py k1-llega k3-bota ...   (sin argumentos: los que falten)
"""
import os, sys
import snapgen as sg

SAL = r"C:\pesonajes para videos\promo-bar"
COMUN = (" Handheld wide-angle 16mm vertical phone video, realistic motion, the same people and clothes as in the first frame all "
         "the time, faces stay consistent; the advisor's black polo only ever shows the small gold teardrop logo, no other logo or text on any clothing. Ambient street and bar sound only, no music, no dialogue, no text on screen.")

MOV = {
 "k1-llega": "The camera walks backwards in front of the man as he walks slowly toward the bar door, tired; the woman at "
   "the door smiles and waves at him playfully, the other two giggle.",
 "k2-lata": "He opens the can with a click and lifts it toward his mouth, sighing, looking tired.",
 "k3-bota": "The advisor snatches the can from his hand and tosses it into the trash bin in one smooth move, then smiles "
   "and raises one finger as if saying 'not that'. Quick whip pan following the can into the bin.",
 "k4-gomitas": "Only the three red gummies rest in the open palm, never more than three, nothing else falls; slow motion; after a moment the hand closes around the three gummies.",
 "k5-confianza": "He pops the gummies in his mouth, chews, and his posture changes: shoulders back, chest up, he fixes his "
   "collar and smiles with confidence; the advisor pats his shoulder and nods.",
 "k6-entran": "The two men walk toward the door with swagger in slow motion; the women turn and smile at them; the camera "
   "follows low behind them.",
 "k7-baila": "He dances with rhythm and confidence, the women dance around him laughing, fast energetic moves, the camera "
   "circles around them.",
 "k8-guino": "The advisor looks into the camera, winks and gives a small nod, then raises his glass slightly.",
 "k9-grupo": "The whole group dances the same simple fun step toward the camera, in sync, smiling.",
}

if __name__ == "__main__":
    claves = sys.argv[1:] or [k for k in MOV if not os.path.exists(os.path.join(SAL, k + ".mp4"))]
    antes = sg.creditos()
    for c in claves:
        for intento in (1, 2):
            try:
                r = sg.video(MOV[c] + COMUN, imagenes=[os.path.join(SAL, c + ".png")])
                e = sg.esperar(r["uuid"], limite=1200, cada=10)
                print("  ok", sg.descargar(sg.url_video(e), os.path.join(SAL, c + ".mp4")), flush=True)
                break
            except BaseException as ex:
                print("  FALLO %s (%d): %s" % (c, intento, str(ex)[:120]), flush=True)
    print("costo:", antes - sg.creditos(), "| quedan", sg.creditos(), flush=True)
