# -*- coding: utf-8 -*-
"""Los 13 cuadros fijos que faltan del spot Lazaro. El plano 1 ya esta hecho."""
import os, sys
sys.path.insert(0, r"C:\JUEGOS APP\bangover-identidad\scripts")
import kie

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "planos")
MAESTROS = os.path.join(BASE, "maestros")

TALLER = ("Inside a gritty underground motorcycle workshop: stained concrete floor with oil patches, "
          "bare concrete walls, pegboard of wrenches, metal shelves, stacked tires, hanging chains. "
          "Two vintage industrial pendant lamps with warm tungsten bulbs overhead, pools of amber "
          "light, deep chiaroscuro shadows, volumetric haze with floating dust.")
REAL = ("Photorealistic, shot on 35mm film, shallow depth of field, cinematic color grading. "
        "No text, no logos, no lettering, no watermarks anywhere in the image.")
SEPARAR = ("He stands inside the warm pool of lamp light so his red comb glows and a warm amber rim "
           "light separates his black feathers from the dark background.")
TRES_D = ("Hyper-detailed 3D industrial cutaway animation still, cross-section x-ray view, Unreal "
          "Engine 5 render, volumetric god rays through the internal cavity, micro dust and metal "
          "particles floating, extreme macro lens. Photorealistic metal textures. No text, no labels, "
          "no logos, no lettering, no measurement markings anywhere.")
GALLO = ("the exact hyperrealistic black rooster from the reference sheet, identical iridescent "
         "feathers, large red comb, amber eye and oil-stained black canvas apron with a steel wrench "
         "in the pocket, standing upright on two legs")
CHANCHO = ("the exact hyperrealistic overweight pig from the reference sheet, identical pale pink "
           "bristled skin, floppy ears, wet snout, tired eyes and sweat-stained white tank top "
           "stretched over his belly, standing upright on two legs")

# nombre, modelo, referencias, prompt
CUADROS = [
 ("p02-gasolina", "nano-banana-2", ["moto"],
  "Top-down overhead macro shot looking straight down into the open fuel filler neck of the rusted "
  "vintage motorcycle from the reference image. A stream of cloudy, murky brown-yellow contaminated "
  "gasoline pours into the opening, with visible sediment and grime suspended in it, foam and dirty "
  "bubbles forming on the surface. The rusted metal tank fills the frame. " + TALLER + " " + REAL),

 ("p03-chancho-patada", "nano-banana-pro", ["chancho", "moto"],
  "Full body wide shot from an extremely low camera angle at floor level: " + CHANCHO + ", straddling "
  "the rusted vintage motorcycle from the second reference image, stamping down hard on the kickstarter "
  "pedal with one hoof, his whole weight on it, face straining. The engine has not started. "
  "His belly hangs over the seat. " + TALLER + " " + REAL),

 ("p04-gallo-chancho", "nano-banana-pro", ["gallo", "chancho"],
  "Over-the-shoulder two shot: in the foreground and out of focus, the back and slumped shoulder of "
  + CHANCHO + "; facing him in sharp focus a few steps away, " + GALLO + ", one wing raised pointing "
  "a single feathered finger at the pig chest, beak slightly open, an unimpressed lecturing "
  "expression. " + SEPARAR + " " + TALLER + " " + REAL),

 ("p05-carbonilla", "nano-banana-2", ["moto"],
  "Extreme macro cutaway view deep inside the cylinder head of the V-twin engine of the motorcycle "
  "from the reference image. Two intake valves and the piston crown are completely encrusted in "
  "thick, black, tar-like carbon buildup, crusty and matte, choking the port. Camera positioned "
  "inside the combustion chamber looking up at the valve seats. Cold hard blue-grey industrial "
  "lighting from within, deep black shadows. " + TRES_D),

 ("p06-valvulas-secas", "nano-banana-2", ["moto"],
  "Extreme macro side cutaway of a single engine valve stem sliding in its dry guide, bone dry metal "
  "on metal with no oil film anywhere, the surface scored with hot scratch marks and glowing faintly "
  "orange from friction, tiny metal shavings breaking off. Harsh raking side light across the "
  "scratched steel. " + TRES_D),

 ("p07-gomita-roja", "nano-banana-2", ["moto"],
  "Top-down overhead macro shot looking down into the open fuel filler neck of the rusted vintage "
  "motorcycle from the reference image. A single translucent BRIGHT RED gummy candy, glossy and "
  "jewel-like with light refracting through it, falls through the air in the centre of frame toward "
  "the dark opening, caught mid-fall and slightly motion blurred. The gummy is unmistakably red, not "
  "golden. Warm amber lamp light catches its wet surface. " + TALLER + " " + REAL),

 ("p08-aceite-dorado", "nano-banana-2", ["moto"],
  "Extreme macro cutaway inside the same engine cylinder head, now flooded with a thick stream of "
  "radiant molten golden oil pouring down over the valve stems and piston crown, washing the black "
  "carbon crust away in dark ribbons as it flows. The gold is warm and luminous, throwing light "
  "caustics that dance across the surrounding polished metal. " + TRES_D),

 ("p09-filtro", "nano-banana-2", ["moto"],
  "Symmetrical head-on extreme macro of a circular pleated engine filter element seen from directly "
  "in front, filling the frame. A sharp pulse of golden-white light sweeps across it left to right, "
  "and everything the light has passed is pristine clean bright metal and crisp white pleats, while "
  "the half not yet reached is still choked with dark grime. A clean dividing line between filthy "
  "and spotless runs down the middle. " + TRES_D),

 ("p10-motor-fundido", "nano-banana-2", ["moto"],
  "High angle shot looking down from above at the rusted vintage motorcycle stopped dead on the "
  "gravel shoulder of an empty road at dusk. Thick grey smoke pours out of the engine cases and "
  "billows upward. Heavily desaturated, cold blue-grey colour grade, overcast flat light, bleak and "
  "joyless, nothing warm anywhere in frame. Photorealistic, 35mm, no text, no logos, no lettering."),

 ("p11-chancho-empuja", "nano-banana-pro", ["chancho", "moto"],
  "Wide exterior shot at night: " + CHANCHO + ", seen in near silhouette from behind and to the side, "
  "pushing the dead rusted motorcycle from the second reference image along an empty dark road, head "
  "hanging, shoulders collapsed, exhausted. A single cold streetlight far behind rims him in pale "
  "blue. Heavily desaturated cold blue-grey colour grade, no warm light anywhere. Photorealistic, "
  "35mm, shallow depth of field, no text, no logos, no lettering."),

 ("p12-gallo-humo", "nano-banana-pro", ["gallo", "moto"],
  "Medium shot from a low angle looking up at " + GALLO + ", back inside the warm workshop, staring "
  "straight into the lens with a hard, serious expression, beak closed. A last wisp of grey smoke "
  "drifts and dissipates through the lamp light behind his shoulder. The motorcycle sits out of "
  "focus behind him. " + SEPARAR + " " + TALLER + " " + REAL),

 ("p13-tanque-limpio", "nano-banana-pro", ["moto"],
  "Low three-quarter angle close shot of the same vintage cruiser motorcycle from the reference "
  "image, now fully restored: the fuel tank is deep glossy black, flawless, mirror polished, with "
  "zero rust and zero oxidation, reflecting the warm pendant lamps overhead. The engine cases and "
  "chrome exhaust are spotless and gleaming. "
  "CRITICAL: the tank is completely blank with no logo, no emblem, no brand name and no lettering, "
  "and the top surface of the tank is clear and empty with nothing resting on it. " + TALLER + " " + REAL),

 ("p14-gallo-orgulloso", "nano-banana-pro", ["gallo", "moto"],
  "Full body hero shot from a low heroic camera angle: " + GALLO + ", standing beside the fully "
  "restored glossy black motorcycle from the second reference image, wings folded across his chest "
  "like crossed arms, chest puffed out, head high, supremely confident. Warm amber light rakes across "
  "both him and the polished tank. " + SEPARAR + " " + TALLER + " " + REAL),
]


def main():
    print("creditos antes:", kie.creditos(), flush=True)
    refs = {n: kie.subir(os.path.join(MAESTROS, a), "lazaro") for n, a in
            (("gallo", "03-gallo.png"), ("chancho", "04-chancho.png"),
             ("moto", "02-moto.png"), ("taller", "01-taller.png"))}

    for i, (nombre, modelo, usa, prompt) in enumerate(CUADROS, 1):
        print("\n[%d/%d] %s (%s)" % (i, len(CUADROS), nombre, modelo), flush=True)
        entrada = {"prompt": prompt, "aspect_ratio": "9:16", "resolution": "2K",
                   "output_format": "png", "image_input": [refs[u] for u in usa]}
        try:
            t = kie.crear(modelo, entrada)
            u = kie.urls(kie.esperar(t, etiqueta=nombre))[0]
            kie.descargar(u, os.path.join(SAL, nombre + ".png"))
            kie.anotar(trabajo="lazaro-cuadros", plano=nombre, modelo=modelo,
                       costo=18 if "pro" in modelo else 12, url=u)
            print("  ok", flush=True)
        except Exception as e:
            print("  FALLO:", e, flush=True)

    print("\ncreditos despues:", kie.creditos(), flush=True)


if __name__ == "__main__":
    main()
