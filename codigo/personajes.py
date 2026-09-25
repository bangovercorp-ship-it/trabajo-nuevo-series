# -*- coding: utf-8 -*-
"""Hojas de personaje del Taller del Tio Gallin (Nano Banana Pro en SnapGen, 3 creditos c/u).

Uso: python personajes.py gallin porfirio toribio ...   (sin argumentos: todos)
"""
import os, sys
import snapgen as sg

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "gallin")
REF_GALLIN = os.path.join(SAL, "02-hoja-tio-gallin-hibrido.png")
GALLIN_V3 = os.path.join(SAL, "03-hoja-tio-gallin.png")

HOJA = ("Character reference sheet on a plain neutral mid-grey studio background: the SAME single character "
        "shown three times side by side, identical in every detail: front view, three-quarter view and side "
        "profile, full body from head to feet in all three views. Soft even studio light. ")
ESTILO = ("Photorealistic human-animal hybrid character design: a real HUMAN face and human body and hands, with "
          "real animal features grown naturally into them. Cinematic, highly detailed skin pores, hair, fur and "
          "feathers. Not cartoon, not Pixar, not a costume, not a mask. No text, no logos, no labels, no watermark.")
SOLO_ESTILO = ("Match ONLY the rendering style, lighting and sheet layout of the reference image; do NOT copy the "
               "rooster features, the face or the clothes of the reference. ")

PERSONAJES = {
 "gallin": ("03-hoja-tio-gallin", [REF_GALLIN],
  "The SAME character as the reference image, Tio Gallin, keeping exactly his wardrobe (clean white ribbed tank top, "
  "dark navy mechanic overalls with the sleeves tied around the waist, worn brown leather work boots, thin steel chain "
  "with an old spark plug pendant), his glossy black-green feather mantle on the shoulders, the long black-green rooster "
  "tail feathers falling from the lower back, and the feathered forearms. Apply these changes: "
  "1) Remove the red wattles from the jaw completely. "
  "2) His beard is short and neatly groomed, salt-and-pepper on the cheeks and jaw, and ONLY the front of the chin is deep "
  "rooster red, shaped into a small elegant pointed tuft like a rooster wattle; the red blends softly into the grey. "
  "3) The red comb is much smaller, sculpted and tidy: a short crest of four rounded points sitting only on the crown and top "
  "of the head, like a styled red crest of hair; it does NOT reach the forehead, the hairline and forehead are clean and "
  "visible, the rest of his hair is short, dark grey and well groomed. "
  "4) Make him handsome and charismatic, a rugged leading man in his late forties: warm intelligent amber eyes, defined "
  "cheekbones, strong but refined jaw, healthy skin, a calm confident half-smile; keep only a thin old scar across the left "
  "eyebrow. 5) Athletic V-shaped torso, broad shoulders, defined arms, narrower waist, tall and upright. "),

 "porfirio": ("04-hoja-porfirio", [GALLIN_V3],
  SOLO_ESTILO + "The character is Porfirio, a man about forty with subtle pig traits, the cashier of a mechanic shop. "
  "His FACE IS A FULLY HUMAN FACE: human nose, human mouth and human jaw, round friendly cheeks, rosy pink skin, small "
  "bright eyes, a big warm smile. The only pig traits: floppy pink pig ears in place of human ears, short light pink "
  "bristly hair, a slightly upturned human nose tip, and a small curly pig tail peeking out at the back. NOT a pig head, "
  "NOT a snout. Slightly overweight with a soft belly but getting in shape, good posture. He wears a navy work shirt "
  "with rolled sleeves and a blank name patch, clean dark jeans and white sneakers. Cheerful, talkative energy. "),

 "toribio": ("05-hoja-toribio", [GALLIN_V3],
  SOLO_ESTILO + "The character is Toribio, a man about thirty-five with bull traits, the muscle of a mechanic shop. "
  "His FACE IS A FULLY HUMAN FACE: human nose, human mouth, strong human jaw and brow, dark brown skin, short black hair, "
  "a short trimmed black beard, and gentle shy kind eyes that contrast with his size. The only bull traits: two short "
  "curved bull horns growing from his temples through the hair, a small brass ring in the septum of his human nose, and "
  "an enormous thick neck. NOT a bull head, NOT a muzzle. Very tall and massive, powerful build. He wears a black tank "
  "top, grey mechanic trousers, heavy black boots and worn leather wrist wraps; huge careful hands. "),

 "renzo": ("06-hoja-renzo", [GALLIN_V3],
  SOLO_ESTILO + "The character is Renzo, a fox-human hybrid man about thirty-three, a charming former car salesman: slim, "
  "handsome and slick, copper-orange hair combed back, pointed fox ears with black tips, sharp narrow amber fox eyes, a thin "
  "clever smile, light stubble, a big bushy orange fox tail with a white tip. He wears a fitted charcoal shirt with rolled "
  "sleeves, a dark waistcoat, tailored trousers and polished brown shoes. Smooth confident pose but restless fingers. "),

 "micaela": ("07-hoja-micaela", [GALLIN_V3],
  SOLO_ESTILO + "The character is Dona Micaela, a cat-human hybrid woman about forty-eight, an elegant widow who owns the bar "
  "across the street: beautiful sharp features, knowing green feline eyes with slit pupils, dark grey cat ears rising from "
  "black hair worn up in an elegant bun, red lips, a slender dark grey cat tail. She wears a fitted black dress with a "
  "burgundy shawl over her shoulders, small gold earrings and low heels. Poised, ironic, all-knowing half-smile. "),

 "aurora": ("08-hoja-aurora", [GALLIN_V3],
  SOLO_ESTILO + "The character is Aurora de la Riva, a rabbit-human hybrid woman about thirty-eight, a millionaire heiress: "
  "very beautiful with soft refined features, warm brown eyes with a guarded, slightly sad look, long cream-white rabbit "
  "ears rising from platinum blonde hair worn loose, a tiny fluffy white rabbit tail. Quiet expensive taste with no logos: "
  "cream wool trench coat, fitted beige turtleneck, tailored camel trousers and low nude heels, one thin gold bracelet. "
  "Elegant, reserved, dignified. "),

 "pavon": ("09-hoja-fausto-pavon", [GALLIN_V3],
  SOLO_ESTILO + "The character is Fausto Pavon, a peacock-human hybrid man about forty-five, a flashy show-off: handsome in a "
  "smug way, perfect teeth in a big fake smile, a small fan crest of iridescent blue-green peacock feathers on top of his "
  "head, a huge peacock tail with eye-spots fanned out behind him like a cape. He wears a white suit, an electric-blue silk "
  "shirt open at the chest, several gold chains and designer sunglasses pushed up on his head. Arrogant chest-out pose. "),
}


def generar(clave):
    nombre, refs, texto = PERSONAJES[clave]
    r = sg.imagen(HOJA + texto + ESTILO, aspecto="16:9", resolucion="2K", imagenes=refs)
    e = sg.esperar(r["uuid"], limite=600, cada=6)
    ruta = sg.descargar(sg.url_imagen(e), os.path.join(SAL, nombre + ".png"))
    print("  ok", clave, "->", ruta, flush=True)


if __name__ == "__main__":
    claves = sys.argv[1:] or list(PERSONAJES)
    antes = sg.creditos()
    for c in claves:
        try:
            generar(c)
        except BaseException as ex:
            print("  FALLO", c, ex, flush=True)
    print("costo total:", antes - sg.creditos(), "| quedan", sg.creditos(), flush=True)
