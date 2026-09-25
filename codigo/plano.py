# -*- coding: utf-8 -*-
"""Genera un plano completo: cuadro fijo (nano-banana-pro) + clip (seedance-1.5-pro)."""
import os, sys
sys.path.insert(0, r"C:\JUEGOS APP\bangover-identidad\scripts")
import kie

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "planos")
MAESTROS = os.path.join(BASE, "maestros")

# el taller y su luz, identicos en todos los planos
TALLER = ("Inside a gritty underground motorcycle workshop: stained concrete floor with oil patches, "
          "bare concrete walls, pegboard of wrenches, metal shelves of parts, stacked tires, hanging "
          "chains. Two vintage industrial pendant lamps with exposed warm tungsten bulbs overhead, "
          "pools of amber light, deep chiaroscuro shadows, volumetric haze with floating dust.")
REAL = ("Photorealistic, shot on 35mm film, shallow depth of field, cinematic color grading. "
        "No text, no logos, no lettering, no watermarks, no subtitles anywhere in the image.")
# el gallo es negro sobre fondo oscuro: sin esto se pierde
SEPARAR = ("The rooster stands directly inside the warm pool of light from the pendant lamp so his red "
           "comb glows and a warm amber rim light separates his black feathers from the dark background.")


def cuadro(nombre, prompt, refs, aspecto="9:16"):
    t = kie.crear("nano-banana-pro", {"prompt": prompt, "aspect_ratio": aspecto,
                                      "resolution": "2K", "output_format": "png",
                                      "image_input": list(refs)})
    print("  cuadro:", t, flush=True)
    u = kie.urls(kie.esperar(t, etiqueta=nombre))[0]
    kie.descargar(u, os.path.join(SAL, nombre + ".png"))
    kie.anotar(trabajo="lazaro-planos", plano=nombre, tipo="cuadro", costo=18, url=u)
    return u


def clip(nombre, prompt, url_cuadro, segundos=4):
    t = kie.crear("bytedance/seedance-1.5-pro",
                  {"prompt": prompt, "input_urls": [url_cuadro], "aspect_ratio": "9:16",
                   "resolution": "720p", "duration": segundos, "generate_audio": False})
    print("  clip:", t, flush=True)
    u = kie.urls(kie.esperar(t, limite=1800, etiqueta=nombre))[0]
    ruta = kie.descargar(u, os.path.join(SAL, nombre + ".mp4"))
    kie.anotar(trabajo="lazaro-planos", plano=nombre, tipo="clip", costo=segundos * 3.5, url=u)
    return ruta


if __name__ == "__main__":
    print("creditos antes:", kie.creditos(), flush=True)
    ref_gallo = kie.subir(os.path.join(MAESTROS, "03-gallo.png"), "lazaro")
    ref_moto = kie.subir(os.path.join(MAESTROS, "02-moto.png"), "lazaro")

    P1_CUADRO = (
        "The exact hyperrealistic rooster from the first reference image, identical feathers, comb, "
        "eye and oil-stained black canvas apron, standing upright on two legs facing the camera in "
        "the workshop from the second reference image. Medium shot from slightly below eye level, "
        "his head and chest filling the upper third of the vertical frame. He looks straight into "
        "the lens with a flat, unimpressed stare, head tilted very slightly. "
        "Behind him and softly out of focus, the same rusted vintage cruiser motorcycle from the "
        "second reference stands dead on its kickstand. " + SEPARAR + " " + TALLER + " " + REAL)

    print("\n[1/2] cuadro del plano 1", flush=True)
    u = cuadro("p01-gallo-camara", P1_CUADRO, [ref_gallo, ref_moto])

    P1_CLIP = (
        "Live action footage. The rooster holds his stare into the camera and blinks once, slowly. "
        "His head tilts a few degrees and his neck hackles shift as he breathes. The camera does a "
        "very slow push-in toward his face. Dust particles drift through the warm lamp light. "
        "The motorcycle behind him stays perfectly still. "
        "One continuous shot, no cuts, no camera shake, subtle natural movement only.")

    print("\n[2/2] clip del plano 1", flush=True)
    print("  listo:", clip("p01-gallo-camara", P1_CLIP, u), flush=True)
    print("\ncreditos despues:", kie.creditos(), flush=True)
