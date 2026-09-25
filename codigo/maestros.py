# -*- coding: utf-8 -*-
"""Genera los 4 activos maestros del spot Lazaro con nano-banana-pro."""
import os, sys, json
sys.path.insert(0, r"C:\JUEGOS APP\bangover-identidad\scripts")
import kie

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "maestros")
REF_TALLER = os.path.join(BASE, "Mechanic_workshop_interior_view_2K_20260920000613.jpeg")
REF_MOTO = os.path.join(BASE, u"Vintage_motorcycle_parked_on_con\u2026_2K_20260920000604.jpeg")

LUZ = ("Lit only by two vintage industrial pendant lamps with exposed warm tungsten bulbs, "
       "pools of amber light and deep chiaroscuro shadows, volumetric haze with floating dust "
       "particles visible in the light beams.")
REAL = ("Photorealistic, shot on 35mm film, shallow depth of field, cinematic color grading, "
        "no text, no logos, no watermarks, no lettering anywhere in the image.")

TALLER = (
    "Interior of a gritty underground motorcycle repair workshop, completely empty, not a single "
    "person or animal anywhere in frame. Stained concrete floor with old oil patches and tire marks, "
    "bare concrete walls, a pegboard covered in wrenches and screwdrivers, metal shelves holding "
    "motorcycle parts, stacked motorcycle tires, coiled hoses and chains hanging. A low motorcycle "
    "service bay in the centre with an empty steel workbench beside it. No cars, no car lifts. "
    + LUZ + " " + REAL)

MOTO = (
    "The exact same 1970s vintage cruiser motorcycle from the first reference image, now parked "
    "inside the workshop from the second reference image, on its kickstand in the centre service bay. "
    "Matte black fuel tank with heavy orange rust oxidation patches, exposed air-cooled V-twin engine "
    "with finned cylinders and carburettor, dulled grimy chrome exhaust pipes, cracked black leather "
    "seat, classic spoked wheels, thick grease and dust on the engine cases. "
    "CRITICAL: the fuel tank is completely blank bare rusted metal with absolutely no logo, no brand "
    "name, no emblem and no lettering of any kind on it. "
    + LUZ + " Warm amber rim light along the chrome and the tank edge. " + REAL)

GALLO = (
    "Character reference sheet on a plain neutral dark grey studio background: one single "
    "hyperrealistic rooster shown three times in a row, identical in every detail, in front view, "
    "three-quarter view and side profile. Full body from head to feet in all three views. "
    "He stands upright on two legs at adult human height. Completely authentic photorealistic rooster "
    "anatomy: real glossy iridescent black and dark green neck hackles and sickle tail feathers, a "
    "large deep red comb and wattles, a round amber eye with a wet reflective surface, a sharp "
    "horn-coloured beak, scaly yellow legs with real spurs. "
    "He wears an oil-stained heavy black canvas mechanic's apron over his chest feathers, and grips a "
    "worn steel wrench in one wing. Posture proud and upright, chest out, head high, confident. "
    "NOT a cartoon, NOT Pixar, NOT 3D animation, NOT a man in a costume, no human facial features, "
    "no human skin. Real bird, wildlife photography level of feather detail. "
    "Soft even studio lighting so every feather is readable. " + REAL)

CHANCHO = (
    "Character reference sheet on a plain neutral dark grey studio background: one single "
    "hyperrealistic overweight domestic pig shown three times in a row, identical in every detail, in "
    "front view, three-quarter view and side profile. Full body from head to feet in all three views. "
    "He stands upright on two legs at adult human height. Completely authentic photorealistic pig "
    "anatomy: pale pink bristled skin with dirt and grease smudges, floppy ears, a wet snout, small "
    "tired watery eyes with heavy lids, real cloven hooves, a heavy sagging belly. "
    "He wears a sweat-stained white tank top stretched tight over his belly. Posture defeated and "
    "slumped: shoulders down, belly out, head low, exhausted and embarrassed expression. "
    "NOT a cartoon, NOT Pixar, NOT 3D animation, NOT a man in a costume, no human facial features. "
    "Real animal, wildlife photography level of skin and bristle detail. "
    "Soft even studio lighting. " + REAL)


def imagen(nombre, prompt, refs=(), aspecto="9:16"):
    entrada = {"prompt": prompt, "aspect_ratio": aspecto, "resolution": "2K", "output_format": "png"}
    if refs:
        entrada["image_input"] = list(refs)
    t = kie.crear("nano-banana-pro", entrada)
    print("  tarea", t, "...", flush=True)
    u = kie.urls(kie.esperar(t, etiqueta=nombre))[0]
    ruta = kie.descargar(u, os.path.join(SAL, nombre + ".png"))
    kie.anotar(trabajo="lazaro-maestros", activo=nombre, modelo="nano-banana-pro", costo=18, url=u)
    print("  listo:", ruta, flush=True)
    return u


if __name__ == "__main__":
    print("creditos antes:", kie.creditos(), flush=True)
    print("subiendo referencias...", flush=True)
    ref_taller = kie.subir(REF_TALLER, "lazaro")
    ref_moto = kie.subir(REF_MOTO, "lazaro")

    print("\n[1/4] TALLER", flush=True)
    url_taller = imagen("01-taller", TALLER, [ref_taller])

    print("\n[2/4] MOTO", flush=True)
    imagen("02-moto", MOTO, [ref_moto, url_taller])

    print("\n[3/4] GALLO", flush=True)
    imagen("03-gallo", GALLO, aspecto="16:9")

    print("\n[4/4] CHANCHO", flush=True)
    imagen("04-chancho", CHANCHO, aspecto="16:9")

    print("\ncreditos despues:", kie.creditos(), flush=True)
