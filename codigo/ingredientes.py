# -*- coding: utf-8 -*-
"""Los insertos de ingredientes y el frasco. Van como cuadros fijos: el movimiento
lo pone ffmpeg en montar.py, que sale gratis y no deforma las plantas."""
import os, sys
sys.path.insert(0, r"C:\JUEGOS APP\bangover-identidad\scripts")
import kie

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "planos")

MACRO = ("Extreme macro product photography, shot on a 100mm macro lens, shallow depth of field, "
         "dramatic single-source lighting, fine dust motes floating in the beam, deep black "
         "background falling off into shadow. Photorealistic, no text, no labels, no packaging, "
         "no logos, no lettering anywhere in the image.")

CUADROS = [
 # zinc y magnesio: se nombran al final de la frase de la carbonilla
 ("i01-zinc-magnesio", "nano-banana-2", [],
  "Two raw mineral specimens resting on a dark oiled steel surface: on the left a jagged crystalline "
  "chunk of raw zinc metal with a bluish-grey metallic sheen and visible crystal facets, on the right "
  "a bright silvery-white magnesium ingot with a scatter of fine silver powder spilling from it. "
  "Cold hard blue-white light rakes across them, catching the metallic glitter. " + MACRO),

 # maca negra y huanarpo macho: se nombran al inicio de la frase del aceite
 ("i02-maca-huanarpo", "nano-banana-2", [],
  "A still life arrangement on dark weathered wood: three whole black maca roots, small and dense "
  "with dark purple-black skin and pale wrinkled root tails, beside several woody reddish-brown "
  "huanarpo macho branch cuttings with dark red bark. A small mound of fine dark brown root powder "
  "sits in front of them and a wisp of it lifts into the air. Warm golden light from one side, "
  "rich and earthy. " + MACRO),

 # achiote y uña de gato: se nombran al inicio de la frase de los filtros
 ("i03-achiote-una-gato", "nano-banana-2", [],
  "A still life arrangement on dark weathered wood: two spiky crimson achiote seed pods, one split "
  "wide open spilling dozens of vivid orange-red annatto seeds, beside curled strips of rough grey-"
  "brown cat claw vine bark with visible woody hooked thorns. Scattered seeds and bark fragments "
  "around them. Warm golden light from one side, deep saturated reds. " + MACRO),
]

FRASCO = (
  "Product photograph of the exact supplement jar from the reference photographs, standing upright "
  "dead centre on the flat top of a polished mirror-black motorcycle fuel tank in a warm workshop. "
  "Reproduce the jar faithfully: a clear transparent plastic jar with a smooth white screw-on lid, "
  "filled to the top with translucent bright red gummies, wrapped in a matte black label. On the "
  "label, from top to bottom: a red rectangle containing the word BANGOVER in bold white letters "
  "with a small gold crown above it, the word LEVANTATE in small white spaced capitals beneath it, "
  "then the word LAZARO very large in bold rounded bright yellow letters, then a small illustration "
  "of a peeled banana, and a circular gold guarantee seal to the right. "
  "The jar is lit by the warm pendant lamps overhead, with a soft reflection of the jar on the glossy "
  "black tank beneath it and a contact shadow. Everything behind falls into dark bokeh. "
  "Photorealistic product photography, 85mm lens, shallow depth of field.")


def main():
    print("creditos antes:", kie.creditos(), flush=True)
    for nombre, modelo, usa, prompt in CUADROS:
        print("[cuadro]", nombre, flush=True)
        t = kie.crear(modelo, {"prompt": prompt, "aspect_ratio": "9:16", "resolution": "2K",
                               "output_format": "png"})
        u = kie.urls(kie.esperar(t, etiqueta=nombre))[0]
        kie.descargar(u, os.path.join(SAL, nombre + ".png"))
        kie.anotar(trabajo="lazaro-ingredientes", plano=nombre, modelo=modelo, costo=12, url=u)
        print("  ok", flush=True)

    print("[cuadro] i04-frasco", flush=True)
    refs = [kie.subir(os.path.join(BASE, f), "lazaro") for f in
            ("WhatsApp Image 2026-09-12 at 9.43.54 AM (1).jpeg",
             "WhatsApp Image 2026-09-12 at 9.43.54 AM.jpeg")]
    refs.append(kie.subir(os.path.join(SAL, "p13-tanque-limpio.png"), "lazaro"))
    t = kie.crear("nano-banana-pro", {"prompt": FRASCO, "aspect_ratio": "9:16", "resolution": "2K",
                                      "output_format": "png", "image_input": refs})
    u = kie.urls(kie.esperar(t, etiqueta="frasco"))[0]
    kie.descargar(u, os.path.join(SAL, "i04-frasco.png"))
    kie.anotar(trabajo="lazaro-ingredientes", plano="i04-frasco", modelo="nano-banana-pro",
               costo=18, url=u)
    print("  ok", flush=True)
    print("creditos despues:", kie.creditos(), flush=True)


if __name__ == "__main__":
    main()
