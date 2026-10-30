#!/usr/bin/env python3
"""Control de nivel de un explainer vertical: ritmo, quietud, sonido y tiempo de lectura.

Uso:
  python3 medir_nivel.py video.mp4                  # ritmo, quietud y sonido
  python3 medir_nivel.py video.mp4 --html index.html  # además, tiempo de lectura de cada texto

Umbrales (de explainers de referencia medidos y de la crítica del terremoto v5):
  - nada quieto más de 2 s (lo que más se nota en un celular);
  - cada texto en pantalla dura al menos 0,5 s + 0,3 s por palabra;
  - sonoridad cerca de -14 LUFS y señal audible por encima de 200 Hz
    (lo que está por debajo de ~110 Hz no se oye en parlantes de celular).

El número de cortes se informa pero no se exige: en la v5 del terremoto, perseguir
cortes empeoró la legibilidad. El ritmo puede estar adentro de cada escena.
Necesita ffmpeg y ffprobe en el PATH.
"""
import argparse
import html
import re
import statistics
import subprocess
import sys

QUIETO_MAX = 2.0
UMBRAL_CORTE = 0.3
UMBRAL_QUIETO = 0.002
FPS = 10


def correr(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def ritmo(video):
    salida = correr(["ffmpeg", "-hide_banner", "-i", video, "-vf",
                     f"fps={FPS},select='gte(scene,0)',metadata=print:key=lavfi.scene_score",
                     "-an", "-f", "null", "-"])
    s = [float(x) for x in re.findall(r"scene_score=([0-9.]+)", salida)]
    if not s:
        sys.exit("No pude leer cuadros del video.")
    dur = len(s) / FPS
    cortes = []
    for i, v in enumerate(s):
        t = i / FPS
        if v > UMBRAL_CORTE and (not cortes or t - cortes[-1] > 0.3):
            cortes.append(t)
    planos = [b - a for a, b in zip([0] + cortes, cortes + [dur])]
    corrida = mejor = 0
    fin = 0.0
    for i, v in enumerate(s):
        corrida = corrida + 1 if v < UMBRAL_QUIETO else 0
        if corrida > mejor:
            mejor, fin = corrida, i / FPS
    return {
        "duracion": dur,
        "cortes": len(cortes),
        "mediana_plano": statistics.median(planos),
        "plano_max": max(planos),
        "quietos_pct": 100 * sum(1 for v in s if v < UMBRAL_QUIETO) / len(s),
        "quieto_max": mejor / FPS,
        "quieto_max_termina": fin,
    }


def sonido(video):
    pistas = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                             "stream=codec_name", "-of", "csv=p=0", video],
                            capture_output=True, text=True).stdout.strip()
    if not pistas:
        return None
    lufs = re.findall(r"I:\s+(-?[0-9.]+) LUFS", correr(["ffmpeg", "-hide_banner", "-i", video, "-vn",
                                                         "-af", "ebur128", "-f", "null", "-"]))
    audible = correr(["ffmpeg", "-hide_banner", "-i", video, "-vn", "-af",
                      "highpass=f=200,asetnsamples=48000,astats=metadata=1:reset=1,"
                      "ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"])
    rms = [float(x) if x != "-inf" else -200.0 for x in re.findall(r"RMS_level=(-?[0-9.]+|-inf)", audible)]
    rms = rms[:-1]  # el último segundo viene incompleto
    mudos = [i for i, v in enumerate(rms) if v < -40]
    return {"lufs": float(lufs[-1]) if lufs else None, "segundos_mudos": mudos}


def lectura(ruta_html):
    """Aproximado: cada texto (p, h1, h2) contra la duración del clip que lo contiene.

    No ve las entradas animadas: un texto que entra tarde tiene menos tiempo que el que
    se informa acá. Créditos y fuentes no cuentan (son chicos y se leen en pausa).
    """
    fuente = open(ruta_html, encoding="utf-8").read()
    fuente = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", fuente, flags=re.S)
    problemas = []
    for m in re.finditer(r"<(section|p|h1|h2)\b([^>]*data-duration=\"([0-9.]+)\"[^>]*)>(.*?)</\1>", fuente, flags=re.S):
        etiqueta, atributos, dur, cuerpo = m.group(1), m.group(2), float(m.group(3)), m.group(4)
        if re.search(r"class=\"[^\"]*(credito|fuente)", atributos):
            continue
        if etiqueta == "section":
            textos = [(t.group(2), t.group(3)) for t in re.finditer(r"<(p|h1|h2)\b([^>]*)>(.*?)</\1>", cuerpo, flags=re.S)]
        else:
            textos = [(atributos, cuerpo)]
        for attrs, contenido in textos:
            if re.search(r"class=\"[^\"]*(credito|fuente)", attrs):
                continue
            palabras = len(html.unescape(re.sub(r"<[^>]+>", " ", contenido)).split())
            if not palabras:
                continue
            hace_falta = 0.5 + 0.3 * palabras
            ident = re.search(r"id=\"([^\"]+)\"", attrs)
            if hace_falta > dur:
                problemas.append((ident.group(1) if ident else "?", palabras, dur, hace_falta))
    return problemas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--html", help="composición HyperFrames, para el tiempo de lectura")
    a = ap.parse_args()

    r = ritmo(a.video)
    print(f"Duración {r['duracion']:.1f} s")
    print(f"Cortes {r['cortes']} · mediana entre cortes {r['mediana_plano']:.2f} s · plano más largo {r['plano_max']:.1f} s  (referencia The Economist: 1,4 s de mediana)")
    print(f"Cuadros quietos {r['quietos_pct']:.0f} % · tramo quieto más largo {r['quieto_max']:.1f} s (termina en t={r['quieto_max_termina']:.1f} s)")
    fallas = []
    if r["quieto_max"] > QUIETO_MAX:
        fallas.append(f"hay {r['quieto_max']:.1f} s seguidos sin movimiento (máximo {QUIETO_MAX:.0f} s)")

    snd = sonido(a.video)
    if snd is None:
        print("Sonido: el video no tiene pista de audio.")
    else:
        print(f"Sonido: {snd['lufs']} LUFS integrados (objetivo −14)")
        if snd["lufs"] is not None and abs(snd["lufs"] + 14) > 1.5:
            fallas.append(f"sonoridad {snd['lufs']} LUFS, lejos de −14")
        if snd["segundos_mudos"]:
            fallas.append("sin señal audible en celular (por encima de 200 Hz) en los segundos "
                          + ", ".join(str(x) for x in snd["segundos_mudos"]))

    if a.html:
        for ident, palabras, dur, falta in lectura(a.html):
            fallas.append(f"#{ident}: {palabras} palabras en {dur:.1f} s; hacen falta {falta:.1f} s")

    print()
    if fallas:
        print("NO ESTÁ AL NIVEL:")
        for f in fallas:
            print(f"  - {f}")
        sys.exit(1)
    print("OK: pasa el control de nivel. Falta la crítica adversarial: este control no ve errores de contenido.")


if __name__ == "__main__":
    main()
