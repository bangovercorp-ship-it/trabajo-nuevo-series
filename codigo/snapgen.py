# -*- coding: utf-8 -*-
"""Cliente minimo de SnapGen (Veo 3.1 con audio). La clave vive en
C:\\JUEGOS APP\\.secretos\\snapgen.env y nunca se imprime."""
import io, json, os, time, urllib.request
import requests

ENV = r"C:\JUEGOS APP\.secretos\snapgen.env"
API = "https://api.snapgen.ai/uapi/v1"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def _clave():
    for l in io.open(ENV, encoding="utf-8-sig"):
        if l.strip().startswith("SNAPGEN_API_KEY="):
            return l.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no hay clave en " + ENV)


def _h():
    return {"x-api-key": _clave(), "User-Agent": UA}


def creditos():
    r = requests.get(API + "/account", headers=_h(), timeout=30)
    r.raise_for_status()
    return r.json()["user_credit"]["available_credit"]


def video(prompt, modelo="veo-3.1-fast", resolucion="1080p", aspecto="9:16",
          duracion=8, imagenes=(), modo="frame"):
    """lanza la generacion y devuelve el uuid. imagenes = rutas locales o urls"""
    datos = [("prompt", prompt), ("model", modelo), ("resolution", resolucion),
             ("duration", str(duracion)), ("aspect_ratio", aspecto), ("mode_image", modo)]
    archivos, abiertos = [], []
    for img in imagenes:
        if img.startswith("http"):
            datos.append(("ref_images", img))
        else:
            f = open(img, "rb")
            abiertos.append(f)
            archivos.append(("ref_images", (os.path.basename(img), f)))
    try:
        r = requests.post(API + "/video-gen/veo", headers=_h(), data=datos,
                          files=archivos or None, timeout=120)
    finally:
        for f in abiertos:
            f.close()
    if r.status_code >= 400:
        raise SystemExit("SnapGen %d: %s" % (r.status_code, r.text[:400]))
    return r.json()


def imagen(prompt, modelo="nano-banana-pro", aspecto="9:16", resolucion="2K",
           estilo="Photorealistic", formato="png", imagenes=()):
    """lanza una imagen y devuelve la respuesta (con uuid). imagenes = rutas o urls"""
    datos = [("prompt", prompt), ("model", modelo), ("aspect_ratio", aspecto),
             ("resolution", resolucion), ("style", estilo), ("output_format", formato)]
    archivos, abiertos = [], []
    for img in imagenes:
        if img.startswith("http"):
            datos.append(("file_urls", img))
        else:
            f = open(img, "rb")
            abiertos.append(f)
            archivos.append(("files", (os.path.basename(img), f)))
    try:
        r = requests.post(API + "/generate_image", headers=_h(), data=datos,
                          files=archivos or None, timeout=120)
    finally:
        for f in abiertos:
            f.close()
    if r.status_code >= 400:
        raise SystemExit("SnapGen %d: %s" % (r.status_code, r.text[:400]))
    return r.json()


def estado(uuid):
    r = requests.get(API + "/history/" + uuid, headers=_h(), timeout=30)
    r.raise_for_status()
    return r.json()


def esperar(uuid, limite=900, cada=10):
    inicio = time.time()
    while True:
        e = estado(uuid)
        if e.get("status") == 2:
            return e
        if e.get("status") == 3:
            raise RuntimeError("fallo: %s %s" % (e.get("error_code"), e.get("error_message")))
        if time.time() - inicio > limite:
            raise RuntimeError("mas de %d s esperando" % limite)
        time.sleep(cada)


def url_imagen(e):
    if isinstance(e.get("generate_result"), str) and e["generate_result"].startswith("http"):
        return e["generate_result"]
    for k in ("generated_image", "generated_images", "images"):
        v = e.get(k)
        if isinstance(v, list) and v:
            v = v[0]
        if isinstance(v, dict):
            for c in ("image_url", "url", "file_download_url"):
                if v.get(c):
                    return v[c]
    return None


def url_video(e):
    """busca la url del mp4 en la respuesta, se llame como se llame el campo"""
    for k in ("generated_video", "generated_videos", "videos", "media"):
        v = e.get(k)
        if isinstance(v, list) and v:
            v = v[0]
        if isinstance(v, dict):
            for c in ("video_url", "url", "file_download_url", "download_url"):
                if v.get(c):
                    return v[c]
        if isinstance(v, str) and v.startswith("http"):
            return v
    for k, v in e.items():
        if isinstance(v, str) and v.startswith("http") and ".mp4" in v:
            return v
    return None


def descargar(url, salida):
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r, open(salida, "wb") as f:
        f.write(r.read())
    return salida
