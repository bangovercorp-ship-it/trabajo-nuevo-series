# -*- coding: utf-8 -*-
"""Convierte cada vista de la maqueta 3D en foto realista, sin mover nada."""
import os, sys
import snapgen as sg

MAQ = r"C:\pesonajes para videos\planos_diseno\maqueta"
SAL = r"C:\pesonajes para videos\gallin\escenarios\desde-maqueta"

FIEL = ("Turn this rough 3D blockout render into a photorealistic cinematic photograph. Keep EXACTLY the same camera "
        "position, lens, framing, perspective and layout: every wall, opening, object and car stays in the same place, "
        "same size and same count; only replace the flat grey blocks with real materials and lighting. ")
MATERIALES = ("Materials: a clean modern Peruvian mechanic workshop; polished light grey epoxy floor with yellow safety "
              "lines; walls cream above and matte onyx black up to 2.4 m with a thin gold line between them; exposed "
              "steel roof structure with skylights and white LED strip lights; red two-post car lifts; ")
FIN = "No people, no characters. Photorealistic, 35mm, natural light falloff. No text, no logos, no watermark."

VISTAS = {
 "entrada": MATERIALES + "left: five service bays with cars, one sedan raised on a two-post lift; right: a wooden "
   "reception counter, a waiting area, a steel workbench under two brass industrial pendant lamps glowing warm amber, a "
   "black tool board with tools hung inside painted gold silhouettes, and a staircase going up; at the far back, a tall "
   "steel rack full of tyres. ",
 "banco": MATERIALES + "a long brushed steel workbench under two brass industrial pendant lamps glowing warm amber; behind "
   "it a black tool board with wrenches hung inside painted gold outlines; on the left a closed black roll-up shutter "
   "door and a staircase; on the right a wooden desk and chairs. ",
 "bahias": MATERIALES + "service bays seen from the aisle: two-post red lifts, a red four-post alignment lift with a red "
   "car raised on it, a white car and a grey car, red rolling tool carts against the wall. ",
 "estanteria": MATERIALES + "a tall steel storage rack on floor rails completely filled with black car tyres, lit by one "
   "brass pendant lamp; in front, a blue tyre changer machine and a blue wheel balancer; between the tyres, a thin slice "
   "of a deep red door is barely visible behind the rack. Mysterious. ",
 "puerta": MATERIALES + "the tyre rack has been slid aside on its floor rails, revealing a worn deep red wooden door with a "
   "small gold-leaf crown in its center, set in the black lower wall, lit from above by one brass pendant lamp glowing "
   "warm amber; blue tyre machines in the foreground. Mysterious and inviting. ",
 "cuarto": "Materials: a hidden private lounge like a gentlemen's speakeasy or exclusive old barbershop, never like a sex "
   "shop; dark wood panelled walls and ceiling; two oxblood leather armchairs facing each other across a low dark wood "
   "table with a small black notebook on it; at the back a lit glass display cabinet with small supplement jars with white "
   "lids and black labels lined up like whisky, labels unreadable; a small brass cabinet; warm low amber light; the open "
   "red door at the left edge. ",
}

if __name__ == "__main__":
    claves = sys.argv[1:] or list(VISTAS)
    antes = sg.creditos()
    for c in claves:
        for intento in (1, 2):
            try:
                r = sg.imagen(FIEL + VISTAS[c] + FIN, aspecto="16:9", resolucion="2K",
                              imagenes=[os.path.join(MAQ, c + ".png")])
                e = sg.esperar(r["uuid"], limite=600, cada=6)
                print("  ok", sg.descargar(sg.url_imagen(e), os.path.join(SAL, c + ".png")), flush=True)
                break
            except BaseException as ex:
                print("  FALLO %s (%d): %s" % (c, intento, str(ex)[:100]), flush=True)
    print("costo:", antes - sg.creditos(), "| quedan", sg.creditos(), flush=True)
