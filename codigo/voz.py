# -*- coding: utf-8 -*-
"""Cliente minimo de ElevenLabs. La clave vive en
C:\\JUEGOS APP\\.secretos\\elevenlabs.env y nunca se imprime.

Uso:  python voz.py cuenta           ve el plan y los creditos que quedan
      python voz.py voces            lista las voces disponibles
      python voz.py di <voz> <salida.mp3> "el texto que dice"
"""
import io, os, sys
import requests

ENV = r"C:\JUEGOS APP\.secretos\elevenlabs.env"
API = "https://api.elevenlabs.io/v1"
MODELO = "eleven_multilingual_v2"      # el que habla espanol con acento natural


def _clave():
    for l in io.open(ENV, encoding="utf-8-sig"):
        if l.strip().startswith("ELEVENLABS_API_KEY="):
            c = l.split("=", 1)[1].strip().strip('"').strip("'")
            if c:
                return c
    raise SystemExit("falta la clave en " + ENV)


def _h(extra=None):
    h = {"xi-api-key": _clave()}
    h.update(extra or {})
    return h


def cuenta():
    r = requests.get(API + "/user/subscription", headers=_h(), timeout=30)
    r.raise_for_status()
    d = r.json()
    return {"plan": d.get("tier"), "usados": d.get("character_count"),
            "tope": d.get("character_limit"), "reinicio": d.get("next_character_count_reset_unix")}


def voces():
    r = requests.get(API + "/voices", headers=_h(), timeout=30)
    r.raise_for_status()
    return [(v["voice_id"], v["name"], v.get("labels", {})) for v in r.json()["voices"]]


def di(voz, texto, salida, estabilidad=0.45, parecido=0.8, estilo=0.35):
    """genera el audio y lo guarda; devuelve la ruta"""
    r = requests.post("%s/text-to-speech/%s" % (API, voz), headers=_h({"Content-Type": "application/json"}),
                      json={"text": texto, "model_id": MODELO,
                            "voice_settings": {"stability": estabilidad, "similarity_boost": parecido,
                                               "style": estilo, "use_speaker_boost": True}},
                      timeout=180)
    if r.status_code >= 400:
        raise SystemExit("ElevenLabs %d: %s" % (r.status_code, r.text[:300]))
    with open(salida, "wb") as f:
        f.write(r.content)
    return salida


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else "cuenta"
    if orden == "cuenta":
        print(cuenta())
    elif orden == "voces":
        for vid, nombre, etiquetas in voces():
            print("%-24s %-22s %s" % (vid, nombre, etiquetas))
    elif orden == "di":
        print(di(sys.argv[2], sys.argv[4], sys.argv[3]))
    else:
        raise SystemExit(__doc__)
