# -*- coding: utf-8 -*-
"""Promocional Bangover "el bar": hojas de personaje y cuadros clave (Nano Banana Pro en SnapGen).

Uso: python promo.py asesor cliente ...   (sin argumentos: todo lo que falte)
"""
import os, sys
import snapgen as sg

BASE = r"C:\pesonajes para videos"
SAL = os.path.join(BASE, "promo-bar")
LOGO = r"C:\JUEGOS APP\bangover-identidad\png\gota\gota-insinua.png"
FRASCO = r"C:\PLATAFORMA BANGOVER\plataforma-bangover\productos\LEVANTATE LAZARO\FRASCO LAZARO cuadrado.png"
os.makedirs(SAL, exist_ok=True)
P = lambda n: os.path.join(SAL, n + ".png")

HOJA = ("Character reference sheet on a plain neutral mid-grey studio background: the SAME single person shown three "
        "times side by side, identical in every detail: front view, three-quarter view and side profile, full body head "
        "to feet. Soft even studio light. Photorealistic, real human, cinematic skin detail. No text, no labels. ")
POLO = ("a fitted plain matte BLACK pique polo shirt; on the left chest, small (about 7 cm tall), the logo from the "
        "reference image EMBROIDERED in metallic gold thread: a teardrop with a flame inside, satin-stitch texture, "
        "slightly raised, thread sheen catching the light, following the fabric folds; exactly that shape, nothing "
        "else printed anywhere on the shirt. ")
BAR = ("a fictional upscale neighbourhood cocktail bar in Lima at night, called nothing (no readable signs): dark "
       "wood and black facade, warm amber string lights, a neon glow in magenta and warm gold through the windows, "
       "wet pavement reflecting the lights, a few parked cars. ")
LENTE = "Full-bleed image edge to edge, no border, no rounded corners, no frame. Shot on a wide-angle 16mm lens, handheld vertical 9:16 phone video, realistic, candid, cinematic night colour. "

TRABAJOS = {
 # nombre: (aspecto, referencias, prompt)
 "asesor": ("16:9", [LOGO], HOJA +
   "The person: a Peruvian man about 32, fictional, handsome and friendly, light brown skin, short black hair with a "
   "clean fade, trimmed short beard, confident knowing smile. He wears " + POLO +
   "Dark slim jeans, clean white sneakers, a simple black watch."),
 "cliente": ("16:9", [], HOJA +
   "The person: a Peruvian man about 28, fictional, average build, likeable, light brown skin, messy black hair, "
   "clean shaven, a bit tired eyes. He wears an unbuttoned light blue denim overshirt over a white t-shirt, beige chino "
   "trousers and white sneakers."),
 "chicas": ("16:9", [], "Three fictional Peruvian young women, about 25, standing together side by side on a plain "
   "neutral mid-grey studio background, full body, front view, soft studio light, photorealistic: one with long straight "
   "dark brown hair in a black halter crop top and high-waisted white wide trousers; one with wavy honey-brown hair in "
   "a fitted red satin slip dress; one with a sleek black ponytail in a gold sequin top and black trousers. Elegant "
   "night-out outfits, tasteful, not revealing, confident flirty smiles. No text."),
 "bar": ("9:16", [], "Empty establishing shot, no people. " + BAR + LENTE +
   "The bar entrance in the centre with a short path of lit pavement leading to a glass door."),
}

A, C, CH, B = P("asesor"), P("cliente"), P("chicas"), P("bar")
QUIEN = ("Keep the people EXACTLY as in the reference sheets: same faces, hair, skin and clothes (the advisor's black polo "
         "with the small gold embroidered teardrop-flame logo on the left chest; the client's light blue denim overshirt, "
         "white t-shirt, beige chinos). ")
LATA = "a generic slim energy drink can, matte silver with an abstract lime-green stripe, no brand, no readable text"
DENTRO = ("inside the same fictional bar: dark wood, black walls, warm amber pendant lights, magenta and gold neon glow, a "
          "busy small dance floor, a long bar with bottles out of focus, light haze. ")
TRABAJOS.update({
 "bar-dentro": ("9:16", [B], "Empty establishing shot, no people, " + DENTRO + LENTE),
 "k1-llega": ("9:16", [C, CH, B], "ONLY the client is in this shot, wearing his light blue denim overshirt, white t-shirt and beige chinos; the advisor in the black polo is NOT in this shot. " + QUIEN + LENTE + "Night, the bar from the reference. The client walks toward the entrance, "
   "seen from the front, shoulders a bit slumped, tired. At the glass door the three women from the reference stand "
   "chatting, one looks at him with a playful flirty smile. Wet pavement reflecting the string lights."),
 "k2-lata": ("9:16", [C, B], "ONLY the client is in this shot, wearing his light blue denim overshirt, white t-shirt and beige chinos; the advisor in the black polo is NOT in this shot. " + QUIEN + LENTE + "Medium close-up on the pavement outside the bar at night. The client, tired "
   "and nervous, is about to drink from " + LATA + ", can raised near his mouth. String lights bokeh behind."),
 "k3-bota": ("9:16", [A, C, B], QUIEN + LENTE + "Outside the bar at night. The advisor steps in from the side with a "
   "confident grin and snatches " + LATA + " from the client's hand just before he drinks; the client looks surprised, his hands now empty. There is only ONE can in the whole image, in the advisor's hand. "
   "A metal street trash bin beside them. The gold logo on the black polo is visible."),
 "k4-gomitas": ("9:16", [A, C, FRASCO], "Extreme close-up insert, night, warm light: EXACTLY THREE gummies, no more: the advisor's hand has just tipped "
   "exactly three (3) small red sugar-coated gummies, clearly separated and countable, into the client's open palm from the jar in the reference image (clear jar, white lid, "
   "black label); the jar is only partly in frame at the edge and slightly out of focus, label not readable. Shallow "
   "depth of field, realistic, " + LENTE),
 "k5-confianza": ("9:16", [A, C, B], QUIEN + LENTE + "Outside the bar at night. The client, chewing, stands up straight "
   "with a sudden confident smile and fixes his collar; the advisor, next to him, pats his shoulder and nods."),
 "k6-entran": ("9:16", [A, C, CH, B], QUIEN + LENTE + "Low wide angle from behind, night: the client and the advisor walk "
   "side by side with swagger toward the lit glass door of the bar; the three women at the door turn to look at them, "
   "smiling."),
 "k7-baila": ("9:16", [C, CH, P("bar-dentro")], QUIEN + DENTRO + LENTE + "The client dances with confidence in the centre of the dance "
   "floor, the three women from the reference dance around him laughing. Energetic, fun, tasteful."),
 "k8-guino": ("9:16", [A, P("bar-dentro")], QUIEN + DENTRO + LENTE + "The advisor leans on the bar, looks straight into the camera and "
   "winks with a knowing smile; the gold embroidered logo on his black polo catches the light."),
 "k9-grupo": ("9:16", [A, C, CH, B], QUIEN + LENTE + "Night, in front of the bar entrance, symmetrical wide shot: the "
   "client in the middle with the three women and the advisor, all dancing a simple fun synchronized step toward the "
   "camera, like a TikTok group dance."),
})

if __name__ == "__main__":
    claves = sys.argv[1:] or [k for k in TRABAJOS if not os.path.exists(P(k))]
    antes = sg.creditos()
    for c in claves:
        asp, refs, txt = TRABAJOS[c]
        for intento in (1, 2):
            try:
                r = sg.imagen(txt, aspecto=asp, resolucion="2K", imagenes=refs)
                e = sg.esperar(r["uuid"], limite=600, cada=6)
                print("  ok", sg.descargar(sg.url_imagen(e), P(c)), flush=True)
                break
            except BaseException as ex:
                print("  FALLO %s (%d): %s" % (c, intento, str(ex)[:100]), flush=True)
    print("costo:", antes - sg.creditos(), "| quedan", sg.creditos(), flush=True)
