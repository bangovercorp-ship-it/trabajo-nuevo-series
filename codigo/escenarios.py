# -*- coding: utf-8 -*-
"""Arte de concepto de los escenarios del Taller del Tio Gallin (Nano Banana Pro en SnapGen)."""
import os, sys
import snapgen as sg

SAL = r"C:\pesonajes para videos\gallin\escenarios"
REAL = ("Photorealistic cinematic production design concept, shot on a 35mm lens, rich detail, grounded Peruvian "
        "urban setting on the edge of Lima. No people, no animals, no characters. ")
SIN_TEXTO = "No other text, no watermark, no extra logos. "

TALLER_FACHADA = (
    "A two-storey corner building on the corner of a wide old avenue and a narrow street of auto-parts shops. The ground "
    "floor is a clean modern mechanic workshop: facade painted deep matte onyx black with thin gold trim, a wide black "
    "roll-up metal shutter door raised halfway, a small side pedestrian door. Above the shutter, a long hand-painted "
    "black sign board with elegant gold serif lettering that reads exactly \"TALLER GALLARDO\" and underneath in smaller "
    "gold letters \"SE ARREGLA TODO\". Mounted on top of the sign, a large red neon rooster silhouette, crowing, head "
    "raised. Upper floor: plain cream wall with one window with iron bars. On the corner, a street sign on a pole reading "
    "\"AV. EL CRUCE\" and \"JR. LOS MECANICOS\". ")

ESCENAS = {
 "01-fachada-dia": ("9:16",
   REAL + TALLER_FACHADA + "Daytime, soft overcast Lima grey sky, the neon is off, a few parked cars, auto-parts shops "
   "next door, tangled electric cables overhead, a motorcycle taxi passing blur. " + SIN_TEXTO),
 "02-fachada-noche": ("9:16",
   REAL + TALLER_FACHADA + "Night after rain: wet asphalt reflecting light, the street is dark and empty, the only lights "
   "are the glowing red neon rooster and a warm amber light spilling from inside the half-open shutter. Across the "
   "street at the edge of frame, the faint glow of a pink neon cat sign from a bar. Moody, cinematic, iconic, "
   "volumetric haze. " + SIN_TEXTO),
 "03-interior": ("16:9",
   REAL + "Wide interior of the same clean modern mechanic workshop, seen from the entrance. Polished grey epoxy floor with "
   "yellow safety lines; walls cream on the top half and matte onyx black on the lower half, with thin gold trim. Two "
   "red hydraulic car lifts, one with a sedan raised. Center: a long steel workbench under two vintage industrial pendant "
   "lamps glowing warm amber. Left wall: a black tool board with every wrench hung inside its painted gold silhouette. "
   "Near the entrance: a small wooden reception counter with an old cash register and a glass cookie jar half hidden "
   "underneath. A corner electronics bench with a magnifying lamp, tiny tools and several antique pocket clocks being "
   "repaired. A chrome espresso machine, a vintage radio, a paper wall calendar with one date circled in red. At the far "
   "back wall, a tall floor-to-ceiling rack of stacked tyres. Clean white work lights overhead mixed with the warm amber "
   "lamps. " + SIN_TEXTO),
 "04-puerta-roja": ("9:16",
   REAL + "Inside a clean mechanic workshop, at the back wall, a tall rack of stacked tyres has been slid aside on rails, "
   "revealing a worn deep red wooden door with no handle on the outside. In the center of the door, a small crown painted "
   "in gold leaf. Warm amber light from a pendant lamp above, deep shadows, faint dust in the air, mysterious and "
   "inviting. " + SIN_TEXTO),
 "05-cuarto-afinamiento": ("16:9",
   REAL + "A hidden private room like a gentlemen's speakeasy lounge or an exclusive old barbershop, never like a sex shop. "
   "Two oxblood leather armchairs facing each other across a low dark wood table with a small black notebook stained "
   "with grease lying on it and two cups of black coffee. Walls in dark wood panelling; antique mechanic tools mounted "
   "like trophies. A lit glass display cabinet where small supplement jars with white lids and red gummies stand lined "
   "up like expensive whisky, labels facing away and unreadable. Next to it a few more jars covered with a black cloth "
   "and a small locked brass cabinet. Warm low light, wine red and gold palette, intimate. " + SIN_TEXTO),
 "06-bar-la-gata": ("9:16",
   REAL + "Night, a narrow old corner bar across the street from a mechanic workshop. Facade painted bottle green with "
   "cream trim, wooden door with frosted glass, a pink neon sign of an elegant cat silhouette with the words \"LA GATA\". "
   "Through the window, a warm red interior: a long polished wooden bar, stools, bottles backlit, framed old "
   "photographs on the wall. Wet street reflecting the neon. " + SIN_TEXTO),
 "07-pasaje-esperanza": ("9:16",
   REAL + "Night, a very narrow alley behind a corner building, walls of old brick and peeling paint, a single weak yellow "
   "street lamp, puddles, a closed small grey metal back door with no handle, a stray cat silhouette on a wall, faint "
   "steam. A small old blue street sign on the wall reading \"PASAJE LA ESPERANZA\". Mysterious. " + SIN_TEXTO),
 "08-mapa-el-cruce": ("16:9",
   "An elegant illustrated neighbourhood map in the style of a vintage film production map, top-down, warm paper texture, "
   "ink lines with muted gold, onyx and brick red accents. Nine city blocks around a crossroads. A wide diagonal road "
   "labelled \"AV. EL CRUCE\" with an arrow at one end labelled \"A LA CAPITAL\". A perpendicular street labelled \"JR. LOS "
   "MECANICOS\". Other streets labelled \"CALLE BUENAVISTA\" and \"PASAJE LA ESPERANZA\" (a narrow alley). Small illustrated "
   "landmarks with labels: on the main corner \"TALLER GALLARDO\" with a tiny red rooster icon; directly across the street "
   "\"BAR LA GATA\" with a tiny cat icon; \"MERCADO SANTA ROSA\"; \"GRIFO EL ULTIMO\" gas station at the edge near the "
   "highway; \"PARADERO\" bus stop; \"PARQUE DEL RELOJ\" with a clock tower. A compass rose. Clean, readable, beautiful, "
   "no other text. "),
}


if __name__ == "__main__":
    claves = sys.argv[1:] or list(ESCENAS)
    antes = sg.creditos()
    for c in claves:
        aspecto, prompt = ESCENAS[c]
        for intento in (1, 2):
            try:
                r = sg.imagen(prompt, aspecto=aspecto, resolucion="2K")
                e = sg.esperar(r["uuid"], limite=600, cada=6)
                print("  ok", sg.descargar(sg.url_imagen(e), os.path.join(SAL, c + ".png")), flush=True)
                break
            except BaseException as ex:
                print("  FALLO %s (intento %d): %s" % (c, intento, str(ex)[:120]), flush=True)
    print("costo:", antes - sg.creditos(), "| quedan", sg.creditos(), flush=True)
