# -*- coding: utf-8 -*-
"""Busca y baja efectos reales de Freesound. Solo licencia CC0: uso comercial
sin atribucion. Baja la preview HQ en mp3, que con el token no pide OAuth2."""
import io, json, os, sys, urllib.parse, urllib.request

ENV = r"C:\JUEGOS APP\.secretos\freesound.env"
API = "https://freesound.org/apiv2"
DESTINO = r"C:\pesonajes para videos\sonidos"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def clave():
    for l in io.open(ENV, encoding="utf-8-sig"):
        if l.strip().startswith("FREESOUND_API_KEY="):
            return l.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no hay clave en " + ENV)


def pedir(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def buscar(texto, dmin=0.2, dmax=30, n=6):
    filtro = 'license:"Creative Commons 0" duration:[%s TO %s]' % (dmin, dmax)
    q = urllib.parse.urlencode({
        "query": texto, "filter": filtro, "sort": "downloads_desc", "page_size": n,
        "fields": "id,name,duration,avg_rating,num_downloads,previews",
        "token": clave()})
    return json.loads(pedir(API + "/search/text/?" + q))["results"]


def bajar(sonido, nombre):
    os.makedirs(DESTINO, exist_ok=True)
    ruta = os.path.join(DESTINO, nombre + ".mp3")
    url = sonido["previews"]["preview-hq-mp3"] + "?token=" + clave()
    with open(ruta, "wb") as f:
        f.write(pedir(url))
    return ruta


if __name__ == "__main__":
    for texto in sys.argv[1:]:
        print("\n== %s" % texto)
        for s in buscar(texto):
            print("  %7d  %5.1fs  %4.1f*  %6d desc  %s" % (
                s["id"], s["duration"], s.get("avg_rating") or 0,
                s["num_downloads"], s["name"][:55]))
