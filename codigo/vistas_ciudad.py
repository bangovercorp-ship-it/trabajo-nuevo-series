# -*- coding: utf-8 -*-
"""Convierte cada vista de la ciudad en foto realista, sin mover nada.

Mismo metodo que `vistas_reales.py`, aplicado al pueblo entero. La maqueta manda:
el prompt empieza obligando a respetar camara, encuadre, perspectiva y posicion de
cada cosa, y solo pide reemplazar el material.

COMO SE USA, desde la maquina que tiene las claves:

    python vistas_ciudad.py                  # las 24, unos 72 creditos
    python vistas_ciudad.py ciudad_aerea esquina_noche      # solo esas dos

Antes de correrlo hay que tener las vistas renderizadas en MAQ. Eso no cuesta nada:

    npx remotion render src/index.ts Ciudad3D  "<carpeta>" --sequence --image-format=png --gl=swangle
    npx remotion render src/index.ts CiudadVertical "<carpeta>" --sequence --image-format=png --gl=swangle

REGLAS QUE NO SE SALTAN
- Nunca se escribe la palabra de la red social dentro de un prompt: le pone el logo
  a la ropa de los personajes.
- No se piden personas. Una figura humana mal hecha en la referencia se le contagia
  al video generado. Las personas entran despues, con su hoja de personaje.
- No se pide texto ni rotulos legibles: la IA inventa nombres y salen en camara.
"""
import os
import sys

import snapgen as sg

MAQ = r"C:\pesonajes para videos\planos_diseno\ciudad"
SAL = r"C:\pesonajes para videos\gallin\escenarios\ciudad"

# --------------------------------------------------------------- el preambulo
FIEL = ("Turn this rough 3D blockout render into a photorealistic cinematic photograph. "
        "Keep EXACTLY the same camera position, focal length, framing, perspective and layout: "
        "every building, street, tree, vehicle and roof stays in the same place, at the same size "
        "and in the same number. Do not add or remove buildings. Do not move the horizon. "
        "Only replace the flat blocks with real materials and real light. ")

PUEBLO = ("Setting: a small town on the alluvial coastal plain of Guayas province, Ecuador, about "
          "15 km inland from the sea. Architecture: one and two storey cement-block houses, rendered "
          "and painted in strong colours faded by sun and salt, dark painted plinth at the base, damp "
          "staining rising from the ground; corrugated zinc gable roofs in three tones, some new, some "
          "grey, some rusted brown; steel grilles on every ground-floor window; white painted window "
          "frames; electrical cables crossing the street between leaning concrete poles; black plastic "
          "water tanks and TV antennas on the roofs; about one in five two-storey houses unfinished, "
          "with a bare block parapet and steel rebar sticking up waiting for another floor; covered "
          "sidewalk arcades on the commercial fronts for shade. ")

ANCLAS = ("Two buildings and only two are landmarks: the mechanic workshop is matte onyx black with a "
          "cream upper floor, and the bar on the opposite corner is bottle green with cream bands. "
          "NO OTHER BUILDING IN THE TOWN IS BLACK OR BOTTLE GREEN. ")

PAISAJE = ("Landscape beyond the town: flat tropical dry forest, dry grass and scrub, scattered ceiba "
           "trees with pale bottle-shaped trunks, geometric green rice paddies, rectangular shrimp "
           "ponds reflecting the sky, a tidal creek with a dark mangrove fringe. Not desert, not "
           "rainforest. ")

FIN = ("No people, no animals, no characters. No text, no signage lettering, no logos, no watermark. "
       "Photorealistic, natural light falloff, real atmospheric haze with distance. ")

DIA = "Light: hard high sun, white hazy coastal sky, short hard shadows, bleached colours. "
TARDE = "Light: late afternoon, low warm sun, long shadows, warm gold on the walls, deep blue shadow. "
ALBA = "Light: just after sunrise, low mist lying over the plain, cold blue land, warm rim on the roofs. "
NOCHE = ("Light: blue hour just after sunset, deep blue sky with a warm band on the horizon. The town is "
         "lit by warm sodium street lamps, lit windows, and two neon signs: a red rooster over the black "
         "workshop and a pink cat over the green bar, facing each other across the avenue. Not pitch black. ")

# --------------------------------------------------------------- las 16 horizontales
VISTAS = {
 "territorio": (PAISAJE + "Aerial view from 430 m: the whole town small in the middle of the plain, the "
   "tidal creek and its shrimp ponds to the south-east, rice paddies to the north, an isolated scrub-covered "
   "hill to the north-west with shacks on its slope, one asphalt road crossing the frame. " + TARDE),
 "ciudad_aerea": (PUEBLO + PAISAJE + "Aerial view from 215 m over the town: the asphalt avenue cutting it in "
   "two, the grid of blocks, zinc roofs of every tone, a long market shed, a green square with a clock tower. "
   + ANCLAS + TARDE),
 "ciudad_cenital": (PUEBLO + "Top-down aerial view straight down over the town centre: the street grid, the "
   "avenue with its planted central median, the square, the market shed, the school yard. " + ANCLAS + DIA),
 "ciudad_sur": (PUEBLO + PAISAJE + "Aerial view from the south at 125 m: the town with the tidal creek and the "
   "shrimp ponds behind it. " + TARDE),
 "la_cuadra": (PUEBLO + "Aerial view from 96 m over one block: zinc roofs, inner yards with mango trees, the "
   "avenue along the top. " + ANCLAS + TARDE),
 "la_esquina": (PUEBLO + "Eye level in the middle of the 40 m avenue looking east along it: the black workshop "
   "on the right side of the avenue and the green bar on the left, facing each other; ceiba trees in the planted "
   "median; parked pickups and motorcycles. " + ANCLAS + TARDE),
 "avenida": (PUEBLO + "Telephoto from the avenue, compressed perspective: the planted median with its row of "
   "ceiba trees on the left, one-storey shops with metal roll-up shutters and painted sign bands under a "
   "concrete arcade on the right, cables overhead, a parked red pickup. " + DIA),
 "olmedo": (PUEBLO + "Eye level looking north up a 20 m cobblestone street lined with almond trees; small "
   "mechanic workshops with open roller doors on both sides; the black workshop far ahead. " + ANCLAS + TARDE),
 "parque": ("Raised view over the town square, 100 x 44 m: hard paving band around the edge, two diagonal paths "
   "crossing at a round plaza with a white clock tower, four lawn quadrants, a concrete volleyball court, a "
   "children's play area on sand, a small bandstand, concrete benches, yellow-flowering guayacan trees at the "
   "entrances and big dark mango trees for shade. " + TARDE),
 "mercado": (PUEBLO + "Eye level on the street beside the municipal market: a long zinc-roofed market shed with "
   "tall openings, small stalls against its wall, a parked bus. " + DIA),
 "esquina_noche": (PUEBLO + "Eye level at the corner: the black workshop with its red neon rooster on the right, "
   "the green bar with its pink neon cat on the left, wet-looking asphalt reflecting both. " + ANCLAS + NOCHE),
 "ciudad_noche": (PUEBLO + "Aerial view from 200 m over the town at night: street lamps along the avenue, lit "
   "windows scattered through the grid, two small neon glows at the centre, dark plain all around. " + NOCHE),
 "estero": (PAISAJE + "Raised view over the tidal creek: a wooden jetty at the end of the town's last street, "
   "three small fibreglass boats moored, a zinc warehouse, shrimp ponds stretching away, mangrove on both banks. "
   + TARDE),
 "loma": (PUEBLO + PAISAJE + "View from the slope of the hill looking down at the town across the plain, mist "
   "still lying in the fields. " + ALBA),
 "carretera": (PUEBLO + "Eye level in the middle of the asphalt road entering town, ceiba trees down the median, "
   "the petrol station canopy on the right, the hill on the horizon. " + TARDE),
 "nuevo_amanecer": (PUEBLO + "Low aerial over the newest neighbourhood: unpaved gravel streets, more unfinished "
   "block walls and rebar, fewer trees, zinc roofs. " + DIA),
}

# --------------------------------------------------------------- las 8 verticales
VERTICALES = {
 "v_ciudad": VISTAS["ciudad_aerea"],
 "v_avenida": VISTAS["avenida"],
 "v_taller": (PUEBLO + "Eye level close to the workshop front across the street: matte onyx black facade, cream "
   "upper floor, a black sign board with a gold band, a red rooster silhouette on top, a steel roller door, "
   "zinc roof with four spinning roof turbines. " + ANCLAS + TARDE),
 "v_esquina": VISTAS["la_esquina"],
 "v_parque": VISTAS["parque"],
 "v_esquina_noche": VISTAS["esquina_noche"],
 "v_loma": VISTAS["loma"],
 "v_estero": VISTAS["estero"],
}

TODAS = dict(VISTAS)
TODAS.update(VERTICALES)
ASPECTO = {k: ("9:16" if k.startswith("v_") else "16:9") for k in TODAS}

if __name__ == "__main__":
    claves = sys.argv[1:] or list(TODAS)
    antes = sg.creditos()
    for c in claves:
        if c not in TODAS:
            print("  no existe la vista %r" % c, flush=True)
            continue
        ref = os.path.join(MAQ, c + ".png")
        if not os.path.exists(ref):
            print("  falta la vista de la maqueta: %s" % ref, flush=True)
            continue
        for intento in (1, 2):
            try:
                r = sg.imagen(FIEL + TODAS[c] + FIN, aspecto=ASPECTO[c], resolucion="2K", imagenes=[ref])
                e = sg.esperar(r["uuid"], limite=600, cada=6)
                print("  ok", sg.descargar(sg.url_imagen(e), os.path.join(SAL, c + ".png")), flush=True)
                break
            except BaseException as ex:
                print("  FALLO %s (%d): %s" % (c, intento, str(ex)[:100]), flush=True)
    print("costo:", antes - sg.creditos(), "| quedan", sg.creditos(), flush=True)
