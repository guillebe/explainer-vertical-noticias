#!/usr/bin/env python3
"""Busca imágenes y videos en Wikimedia Commons con los datos para verificarlos y acreditarlos.

Uso:
  python3 buscar_commons.py --categoria "2026 Panama earthquake"
  python3 buscar_commons.py --buscar "Panama earthquake 2026" --tipo video
  python3 buscar_commons.py --categoria "..." --filtro "collapsed|damage" --licencia "Public domain"

Imprime, por archivo: título, licencia, fecha de toma, autor, tamaño, descripción y URL de la página.
Esa ficha es la que va a source.md: lugar y fecha verificados, licencia y crédito.
Por qué: un plano sin lugar ni fecha verificados fue un P0 en la crítica del terremoto (v11).
"""
import argparse
import json
import re
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "explainer-vertical-noticias/1.0 (taller Media Party)"}


def pedir(params):
    url = API + "?" + urllib.parse.urlencode({"action": "query", **params, "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def limpiar(v):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", v or "")).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--categoria", help="nombre de la categoría, sin «Category:»")
    g.add_argument("--buscar", help="texto a buscar en los archivos")
    ap.add_argument("--tipo", choices=["todo", "imagen", "video"], default="todo")
    ap.add_argument("--filtro", help="regex sobre la descripción (por ejemplo «collapsed|damage»)")
    ap.add_argument("--licencia", help="regex sobre la licencia (por ejemplo «Public domain|CC BY»)")
    ap.add_argument("--max", type=int, default=50)
    a = ap.parse_args()

    base = {"prop": "imageinfo", "iiprop": "extmetadata|size|url|mime"}
    if a.categoria:
        base |= {"generator": "categorymembers", "gcmtitle": "Category:" + a.categoria,
                 "gcmtype": "file", "gcmlimit": min(a.max, 200)}
    else:
        base |= {"generator": "search", "gsrsearch": a.buscar, "gsrnamespace": 6, "gsrlimit": min(a.max, 50)}
    paginas, cont = {}, {}
    while True:  # la API da los metadatos de a 50 archivos: seguir la paginación
        datos = pedir({**base, **cont})
        for k, v in datos.get("query", {}).get("pages", {}).items():
            if "imageinfo" in v or k not in paginas:
                paginas[k] = v
        if "continue" not in datos or len(paginas) >= a.max * 4:
            break
        cont = datos["continue"]

    n = 0
    for p in paginas.values():
        if "imageinfo" not in p:
            continue
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        dato = lambda k: limpiar(m.get(k, {}).get("value"))
        mime = ii.get("mime", "")
        if a.tipo == "imagen" and not mime.startswith("image"):
            continue
        if a.tipo == "video" and not mime.startswith("video"):
            continue
        desc, lic = dato("ImageDescription"), dato("LicenseShortName")
        if a.filtro and not re.search(a.filtro, desc, re.I):
            continue
        if a.licencia and not re.search(a.licencia, lic, re.I):
            continue
        n += 1
        print(f"■ {p['title'][5:]}")
        print(f"  Licencia: {lic} · Fecha: {dato('DateTimeOriginal') or 's/d'} · Autor: {dato('Artist') or 's/d'}")
        print(f"  {ii.get('width')}×{ii.get('height')} · {round(ii.get('size', 0) / 1e6, 1)} MB · {mime}")
        print(f"  {desc[:300]}")
        print(f"  {ii.get('descriptionurl')}")
    print(f"\n{n} archivo(s). Verificá lugar y fecha en la descripción antes de usarlos.")


if __name__ == "__main__":
    main()
